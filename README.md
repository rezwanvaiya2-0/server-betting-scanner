# Server Betting Site Scanner

A tool for server administrators to scan cPanel/WHM accounts for domains hosting gambling-related content.

## Installation

Run this command on your server as root:

```bash
bash <(curl -s https://raw.githubusercontent.com/rezwanvaiya2-0/server-betting-scanner/main/src/installer.sh)
```


### 📁 Installation Directory
The script is installed in: `/opt/betting_scanner/`

### 📊 Log Files Location
The scanner creates logs in: `/var/log/betting_scanner.log`  
The updater creates logs in: `/var/log/betting_scanner_update.log`

### 🗑️ Complete Uninstall Command
Run this **single command** to completely remove everything:

```bash
sudo rm -rf /opt/betting_scanner && \
sudo rm -f /usr/local/bin/sites /usr/local/bin/update-betting /usr/local/bin/fix-betting && \
sudo rm -f /var/log/betting_scanner.log /var/log/betting_scanner_update.log && \
echo "✅ Betting Scanner completely uninstalled"
```

### 🔍 What Gets Removed:
1. **`/opt/betting_scanner/`** - Main installation directory
2. **`/usr/local/bin/sites`** - Scanner command symlink
3. **`/usr/local/bin/update-betting`** - Update command symlink  
4. **`/usr/local/bin/fix-betting`** - Fix command symlink
5. **`/var/log/betting_scanner.log`** - Main scanner log file
6. **`/var/log/betting_scanner_update.log`** - Update log file

### 💾 Storage Space Usage
**Log files won't take much space:** 
- Scanner log grows only when you run `sites` command
- Update log grows only when you run `update-betting`
- Typical log size: **Few KB per scan/update**
- You can safely ignore them as they won't fill your disk

### 📋 To Check Log File Sizes:
```bash
ls -lah /var/log/betting_scanner*
```

### ⚠️ Important Notes:
1. **No user data** is stored by the script
2. **No cache files** are created
3. **No database** is used
4. The script only **reads** your server's domain list, doesn't modify anything
5. Uninstall is **completely safe** and removes everything
