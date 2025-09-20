#!/bin/bash
# PROPER fix command that actually works

echo "🔧 Running PROPER Betting Scanner Fix..."
echo ""

# First, ensure THIS script is executable
chmod +x /opt/betting_scanner/bin/fix_scanner.sh

# Remove ALL broken symlinks
rm -f /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting

# Create NEW symlinks
ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites
ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
ln -sf /opt/betting_scanner/bin/fix_scanner.sh /usr/local/bin/fix-betting

# Make ORIGINAL scripts executable (this is what matters)
chmod +x /opt/betting_scanner/bin/*.sh
chmod +x /opt/betting_scanner/src/betting_scanner.py

# Ensure symlinks have execute permission (important!)
chmod +x /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting

echo "✅ PROPER Fix completed!"
echo "💡 Now try: sites"
echo ""
echo "📋 Fixed commands:"
echo "   - sites: $(ls -la /usr/local/bin/sites | awk '{print $11}')"
echo "   - update-betting: $(ls -la /usr/local/bin/update-betting | awk '{print $11}')"
echo "   - fix-betting: $(ls -la /usr/local/bin/fix-betting | awk '{print $11}')"
