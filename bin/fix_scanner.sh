# Create a BETTER fix script that actually works
cat > /opt/betting_scanner/bin/fix_scanner.sh << 'EOF'
#!/bin/bash
# PROPER fix command that actually works

echo "🔧 Running PROPER Betting Scanner Fix..."
echo ""

# Remove ALL broken symlinks
rm -f /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting

# Create NEW symlinks
ln -sf /opt/betting_scanner/bin/sites.betting.sh /usr/local/bin/sites
ln -sf /opt/betting_scanner/bin/update.betting.sh /usr/local/bin/update-betting
ln -sf /opt/betting_scanner/bin/fix_scanner.sh /usr/local/bin/fix-betting

# Make ORIGINAL scripts executable (this is what matters)
chmod +x /opt/betting_scanner/bin/*.sh
chmod +x /opt/betting_scanner/src/betting_scanner.py

echo "✅ PROPER Fix completed!"
echo "💡 Now try: sites"
EOF

# Make the new fix script executable
chmod +x /opt/betting_scanner/bin/fix_scanner.sh

# Run the PROPER fix
/opt/betting_scanner/bin/fix_scanner.sh
