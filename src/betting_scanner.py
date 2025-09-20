#!/usr/bin/env python3

import subprocess
import sys
import re
from pathlib import Path
import logging

# Try to import external libraries.
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"ERROR: Required Python library not found. {e}", file=sys.stderr)
    print("Please install them using: pip3 install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

# ========== CONFIGURATION ==========
KEYWORDS_FILE = Path('/opt/betting_scanner/src/keywords.txt')
LOG_FILE = '/var/log/betting_scanner.log'
# ===================================

def setup_logging():
    """Sets up logging to both a file and the console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('BettingScanner')

def get_keywords():
    """Reads the list of keywords/patterns from the keywords.txt file."""
    keywords = []
    try:
        with open(KEYWORDS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    keywords.append(line)
    except FileNotFoundError:
        logger.error(f"Keywords file not found at {KEYWORDS_FILE}. Please create it.")
        sys.exit(1)
    return keywords

def get_cpanel_domains():
    """Fetches a list of ALL domains on the server by parsing /etc/localdomains and maps them to users."""
    domains = []
    localdomains_file = Path('/etc/localdomains')
    
    if not localdomains_file.exists():
        logger.error("Domains file not found: /etc/localdomains")
        return domains

    try:
        # Read all domains from /etc/localdomains (includes main, addon, and subdomains)
        with open(localdomains_file, 'r') as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith('#'):  # Skip empty lines and comments
                    # Find which user owns this domain and their document root
                    user_info = find_user_and_docroot_for_domain(domain)
                    if user_info:
                        domains.append({
                            'user': user_info['user'], 
                            'domain': domain, 
                            'document_root': user_info['document_root']
                        })
                    else:
                        logger.debug(f"Could not find user for domain: {domain}")
        
        logger.info(f"Found {len(domains)} domains to scan from /etc/localdomains")
        return domains
        
    except Exception as e:
        logger.error(f"Failed to get domain list from /etc/localdomains: {e}")
        return []

def find_user_and_docroot_for_domain(domain):
    """Finds the cPanel user and document root for any domain (main, addon, or subdomain)."""
    try:
        # Method 1: Check main domains first (fastest)
        user_files_dir = Path('/var/cpanel/users/')
        for user_file in user_files_dir.iterdir():
            if user_file.is_file():
                username = user_file.name
                with open(user_file, 'r') as f:
                    for line in f:
                        if line.startswith('DNS='):
                            main_domain = line.strip().split('=')[1]
                            if domain == main_domain:
                                return {
                                    'user': username,
                                    'document_root': f"/home/{username}/public_html"
                                }
        
        # Method 2: Check addon domains via userdata
        home_dir = Path('/home')
        for user_dir in home_dir.iterdir():
            if user_dir.is_dir():
                username = user_dir.name
                # Check addon domains
                addon_dir = user_dir / '.addondomain'
                if addon_dir.exists():
                    for addon_file in addon_dir.iterdir():
                        if addon_file.name == domain:
                            try:
                                with open(addon_file, 'r') as f:
                                    doc_root = f.read().strip()
                                    return {'user': username, 'document_root': doc_root}
                            except:
                                return {'user': username, 'document_root': f"/home/{username}/public_html/{domain}"}
                
                # Check subdomains
                subdomain_dir = user_dir / '.subdomain'
                if subdomain_dir.exists():
                    for subdomain_file in subdomain_dir.iterdir():
                        if subdomain_file.name == domain:
                            try:
                                with open(subdomain_file, 'r') as f:
                                    doc_root = f.read().strip()
                                    return {'user': username, 'document_root': doc_root}
                            except:
                                subdomain_part = domain.split('.')[0]
                                return {'user': username, 'document_root': f"/home/{username}/public_html/{subdomain_part}"}
        
        # Method 3: Fallback - check domain directory existence
        for user_dir in home_dir.iterdir():
            if user_dir.is_dir():
                username = user_dir.name
                # Check main domain
                if (user_dir / 'public_html').exists():
                    return {'user': username, 'document_root': f"/home/{username}/public_html"}
                
                # Check addon domain path
                domain_path = user_dir / 'public_html' / domain
                if domain_path.exists():
                    return {'user': username, 'document_root': str(domain_path)}
        
        return None
        
    except Exception as e:
        logger.debug(f"Error finding user for domain {domain}: {e}")
        return None

def check_domain(domain_info, keywords):
    """Checks a single domain for matches against the keyword list."""
    domain = domain_info['domain']
    user = domain_info['user']
    doc_root = domain_info['document_root']
    matches_found = []

    # Check 1: SMART DOMAIN NAME matching (partial matches, 3+ letters)
    domain_lower = domain.lower()
    for kw in keywords:
        kw_lower = kw.lower()
        # Skip very short keywords (less than 3 characters)
        if len(kw_lower) < 3:
            continue
            
        # Check for exact match
        if re.search(rf'\b{re.escape(kw_lower)}\b', domain_lower):
            matches_found.append(f"DOMAIN_NAME_EXACT: '{kw}'")
            continue
            
        # Check for partial match (keyword appears anywhere in domain)
        if kw_lower in domain_lower:
            matches_found.append(f"DOMAIN_NAME_PARTIAL: '{kw}'")
            continue
            
        # Advanced: Check for similar patterns (3+ character sequences)
        for i in range(len(kw_lower) - 2):
            segment = kw_lower[i:i+3]
            if segment in domain_lower:
                matches_found.append(f"DOMAIN_NAME_SIMILAR: '{segment}' from '{kw}'")
                break

    # Check 2: Check the WEBSITE CONTENT
    url = f"http://{domain}"
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Server Admin Scanner)'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts and styles to clean up text
        for element in soup(["script", "style"]):
            element.decompose()

        # Get text from the entire page and the title
        page_text = soup.get_text().lower()
        page_title = soup.find('title')
        title_text = page_title.get_text().lower() if page_title else ""

        # Check page title and content for keywords
        for kw in keywords:
            kw_lower = kw.lower()
            if len(kw_lower) < 3:
                continue
                
            # Exact match in title
            if re.search(rf'\b{re.escape(kw_lower)}\b', title_text):
                matches_found.append(f"PAGE_TITLE: '{kw}'")
                
            # Partial match in title
            elif kw_lower in title_text:
                matches_found.append(f"PAGE_TITLE_PARTIAL: '{kw}'")
            
            # Count occurrences in body text
            count = page_text.count(kw_lower)
            if count > 2:
                matches_found.append(f"BODY_TEXT ({count}x): '{kw}'")

    except requests.exceptions.RequestException as e:
        logger.debug(f"Could not fetch {url}: {e}")
        pass

    # If we found any matches, return the results
    if matches_found:
        result_line = f"MATCH - User: {user} | Domain: {domain} | Path: {doc_root}"
        result_line += f" | Reasons: {', '.join(matches_found)}"
        return result_line
    else:
        return None

def main():
    global logger
    logger = setup_logging()
    logger.info("="*50)
    logger.info("Starting Betting Site Scanner")

    keywords = get_keywords()
    logger.info(f"Loaded {len(keywords)} keywords from {KEYWORDS_FILE}")

    domains = get_cpanel_domains()
    logger.info(f"Found {len(domains)} domains to scan.")

    results = []
    for domain_info in domains:
        domain_result = check_domain(domain_info, keywords)
        if domain_result:
            results.append(domain_result)
            print(domain_result)

    if results:
        logger.info("Scan completed. Matches found:\n" + "\n".join(results))
    else:
        logger.info("Scan completed. No matches found.")

if __name__ == "__main__":
    main()
