#!/bin/bash
# Betting Scanner Installer Script

set -e # Exit on any error

REPO_URL="https://github.com/rezwanvaiya2-0/server-betting-scanner.git"
TARGET_DIR="/opt/betting_scanner"
BIN_DIR="/usr/local/bin"

echo "Installing Betting Site Scanner from $REPO_URL"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (use sudo)."
    exit 1
fi

# Install required packages
echo "Installing required system packages (git, python3, pip)..."
if command -v yum &> /dev/null; then
    yum install -y git python3
    pip3 install requests beautifulsoup4
elif command -v apt-get &> /dev/null; then
    apt-get update
    apt-get install -y git python3 python3-pip
    pip3 install requests beautifulsoup4
else
    echo "Warning: Could not automatically install Python dependencies. Please ensure Python 3 and pip are installed."
fi

# Clone the repository
echo "Cloning repository into $TARGET_DIR..."
git clone "$REPO_URL" "$TARGET_DIR" || { echo "Git clone failed. Please check the repository URL."; exit 1; }

# Make all scripts executable
chmod +x "$TARGET_DIR/src/betting_scanner.py"
chmod +x "$TARGET_DIR/bin/"*.sh

# Install the binary symlinks
echo "Installing system commands..."
ln -sf "$TARGET_DIR/bin/sites.betting.sh" "$BIN_DIR/sites"
ln -sf "$TARGET_DIR/bin/update.betting.sh" "$BIN_DIR/update-betting"
ln -sf "$TARGET_DIR/bin/fix_scanner.sh" "$BIN_DIR/fix-betting"

echo "Installation complete!"
echo ""
echo "Usage:"
echo "  Scan your server:      sites"
echo "  Update tool & keywords: update-betting"
echo "  Fix any issues:        fix-betting"
