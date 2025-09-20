#!/bin/bash
# One-time fix command to repair scanner installation

echo "🔧 Running Betting Scanner Fix..."
echo ""

# Fix permissions for all scripts
echo "📝 Setting executable permissions..."
chmod +x /opt/betting_scanner/bin/*.sh
chmod +x /opt/betting_scanner/src/betting_scanner.py

# Repair symlinks
echo "🔗 Repairing symlinks..."
rm -f /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting
ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites
ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
ln -sf /opt/betting_scanner/bin/fix_scanner.sh /usr/local/bin/fix-betting

# Ensure symlinks have execute permission
chmod +x /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting

# Reset any Git issues
echo "🔄 Resetting Git repository..."
cd /opt/betting_scanner
git fetch --all
git reset --hard origin/main

echo ""
echo "✅ Fix completed!"
echo "💡 Now run: sites"
