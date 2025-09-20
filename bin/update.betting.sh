#!/bin/bash
# Script to update the entire scanner from GitHub

SCANNER_DIR="/opt/betting_scanner"

echo "Checking for updates to the Betting Site Scanner..."

if [ ! -d "$SCANNER_DIR/.git" ]; then
    echo "ERROR: The scanner was not installed via Git. Cannot update automatically."
    exit 1
fi

# Change to the scanner directory and pull the latest changes
cd "$SCANNER_DIR" || exit 1

# Fetch the latest changes from GitHub
if git pull; then
    echo "Successfully updated the betting site scanner!"
    echo "Latest version and keywords are now active."
else
    echo "ERROR: Failed to update from GitHub. Check your network connection."
    exit 1
fi
