#!/bin/bash
# Script to update the entire scanner from GitHub with complete fix

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

# Reset hard to the latest version from GitHub
echo "🔄 Resetting to latest version..."
git reset --hard origin/main >> "$LOG_FILE" 2>&1

# Pull the latest changes
echo "✅ Applying updates..."
if git pull origin main >> "$LOG_FILE" 2>&1; then
    echo "🎉 Successfully updated the betting site scanner!"
    
    # COMPLETE PERMISSION FIXING
    echo "🔧 Setting executable permissions for all scripts..."
    chmod +x /opt/betting_scanner/bin/*.sh >> "$LOG_FILE" 2>&1
    chmod +x /opt/betting_scanner/src/betting_scanner.py >> "$LOG_FILE" 2>&1
    
    echo "🔗 Repairing symlinks in /usr/local/bin/..."
    # Remove existing symlinks
    rm -f /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting
    
    # Create new symlinks
    ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites
    ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
    ln -sf /opt/betting_scanner/bin/fix_scanner.sh /usr/local/bin/fix-betting
    
    # Ensure symlinks have execute permission
    chmod +x /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting
    
    echo "📋 Latest version and keywords are now active."
    echo "✨ Update completed successfully!"
    echo ""
    echo "💡 Commands available:"
    echo "   sites           - Scan for betting sites"
    echo "   update-betting  - Update scanner from GitHub"
    echo "   fix-betting     - Fix any issues"
    
else
    echo "❌ ERROR: Failed to update from GitHub. Check the log: $LOG_FILE"
    exit 1
fi
