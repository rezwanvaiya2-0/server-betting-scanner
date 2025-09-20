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
                    keywords.append(line.lower())
    except FileNotFoundError:
        logger.error(f"Keywords file not found at {KEYWORDS_FILE}. Please create it.")
        sys.exit(1)
    return keywords

def get_cpanel_domains():
    """Fetches a list of all domains on the server using WHM's wwwacct command."""
    try:
        result = subprocess.run(['/scripts/wwwacct', '--list'], capture_output=True, text=True, check=True)
        domains = []
        for line in result.stdout.splitlines():
            parts = line.split()
            # The wwwacct output format is: username domain IP package
            if len(parts) >= 4 and parts[1] != 'NULL':
                user, domain = parts[0], parts[1]
                domains.append({'user': user, 'domain': domain, 'document_root': f"/home/{user}/public_html"})
        return domains
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get domain list from WHM: {e}")
        return []

def check_domain(domain_info, keywords):
    """Checks a single domain for matches against the keyword list."""
    domain = domain_info['domain']
    user = domain_info['user']
    doc_root = domain_info['document_root']
    matches_found = []

    # Check 1: Check the DOMAIN NAME itself for keyword matches
    for kw in keywords:
        if re.search(rf'\b{re.escape(kw)}\b', domain, re.IGNORECASE):
            matches_found.append(f"DOMAIN_NAME: '{kw}'")

    # Check 2: Check the WEBSITE CONTENT
    url = f"http://{domain}"
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Server Admin Scanner)'})
        response.raise_for_status()  # Raises an exception for bad status codes (4xx, 5xx)

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
            if re.search(rf'\b{re.escape(kw)}\b', title_text):
                matches_found.append(f"PAGE_TITLE: '{kw}'")
            # Count occurrences in body text as a simple measure of density
            count = len(re.findall(rf'\b{re.escape(kw)}\b', page_text))
            if count > 3:  # Arbitrary threshold to avoid minor mentions
                matches_found.append(f"BODY_TEXT ({count}x): '{kw}'")

    except requests.exceptions.RequestException as e:
        logger.debug(f"Could not fetch {url}: {e}")
        # Don't fail the whole script if one site is down
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
            # Print matches to console immediately
            print(domain_result)

    # Also log all results together
    if results:
        logger.info("Scan completed. Matches found:\n" + "\n".join(results))
    else:
        logger.info("Scan completed. No matches found.")

if __name__ == "__main__":
    main()
