#!/bin/bash
# Launcher script for the betting site scanner

# Ensure the script is executable
chmod +x /opt/betting_scanner/src/betting_scanner.py >/dev/null 2>&1

# Run the main Python scanner
/opt/betting_scanner/src/betting_scanner.py "$@"
