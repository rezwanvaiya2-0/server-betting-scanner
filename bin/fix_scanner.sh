#!/bin/bash
# One-time fix command to repair scanner installation

echo "🔧 Running Betting Scanner Fix..."

# Fix permissions
chmod +x /opt/betting_scanner/bin/*.sh
chmod +x /opt/betting_scanner/src/betting_scanner.py

# Recreate symlinks
rm -f /usr/local/bin/update-betting
rm -f /usr/local/bin/sites
ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites

# Reset any Git issues
cd /opt/betting_scanner
git fetch --all
git reset --hard origin/main

echo "✅ Fix completed! Now run: update-betting"
