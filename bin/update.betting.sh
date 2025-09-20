#!/bin/bash
# Script to update the entire scanner from GitHub with conflict resolution

SCANNER_DIR="/opt/betting_scanner"
LOG_FILE="/var/log/betting_scanner_update.log"

echo "🔄 Checking for updates to the Betting Site Scanner..."
echo "📝 Logging to: $LOG_FILE"

if [ ! -d "$SCANNER_DIR/.git" ]; then
    echo "❌ ERROR: The scanner was not installed via Git. Cannot update automatically."
    exit 1
fi

# Change to the scanner directory
cd "$SCANNER_DIR" || exit 1

# Stash any local changes to avoid conflicts
echo "💾 Stashing any local changes..."
git stash >> "$LOG_FILE" 2>&1

# Fetch the latest changes from GitHub
echo "📥 Fetching latest updates from GitHub..."
git fetch --all >> "$LOG_FILE" 2>&1

# Reset hard to the latest version from GitHub (THIS FIXES THE CONFLICTS)
echo "🔄 Resetting to latest version..."
git reset --hard origin/main >> "$LOG_FILE" 2>&1

# Pull the latest changes
echo "✅ Applying updates..."
if git pull origin main >> "$LOG_FILE" 2>&1; then
    echo "🎉 Successfully updated the betting site scanner!"
    echo "📋 Latest version and keywords are now active."
    
    # Ensure all scripts are executable
    echo "🔧 Setting executable permissions..."
    chmod +x /opt/betting_scanner/bin/*.sh >> "$LOG_FILE" 2>&1
    chmod +x /opt/betting_scanner/src/betting_scanner.py >> "$LOG_FILE" 2>&1
    
    # Check if symlinks exist, create if missing
    if [ ! -L "/usr/local/bin/update-betting" ]; then
        ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
    fi
    if [ ! -L "/usr/local/bin/sites" ]; then
        ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites
    fi
    
    echo "✨ Update completed successfully!"
else
    echo "❌ ERROR: Failed to update from GitHub. Check the log: $LOG_FILE"
    exit 1
fi
