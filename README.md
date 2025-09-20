# Server Betting Site Scanner

A tool for server administrators to scan cPanel/WHM accounts for domains hosting gambling-related content.

### 🛠️ **Dependencies Needed to Run the Script:**

#### 1. **System Packages:**
```bash
# Essential system tools
git         # To clone/update from GitHub
python3     # Python 3 interpreter
python3-pip # Python package manager
```

#### 2. **Python Libraries:**
```bash
# Required Python packages
requests        # For HTTP requests to check websites
beautifulsoup4  # For HTML parsing of website content
```

#### 3. **Server Requirements:**
```bash
# Server environment
cPanel/WHM server  # The script uses WHM-specific commands
Root access        # Required to access all user domains
```

---

### 🔧 **Installation Command for Dependencies:**

The installer script **automatically installs** all dependencies, but here's the manual command:

#### For CentOS/CloudLinux/RHEL:
```bash
yum install -y git python3
pip3 install requests beautifulsoup4
```

#### For Ubuntu/Debian: ( Not Tested Yet! )
```bash
apt-get update
apt-get install -y git python3 python3-pip
pip3 install requests beautifulsoup4
```

---

### 📊 **What Each Dependency Does:**

| Dependency | Purpose |
|------------|---------|
| **git** | Clones and updates from GitHub repository |
| **python3** | Runs the main scanner script |
| **requests** | Fetches website content for analysis |
| **beautifulsoup4** | Parses HTML to find gambling keywords |

The **installer script handles everything automatically** - you don't need to manually install dependencies! 🎉


## Installation

Run this command on your server as root:

```bash
bash <(curl -s https://raw.githubusercontent.com/rezwanvaiya2-0/server-betting-scanner/main/src/installer.sh)
```


### 📁 Installation Directory
The script is installed in: `/opt/betting_scanner/`

### 📊 **WHAT EACH COMMAND DOES:**

| Command | Purpose | Frequency |
|---------|---------|-----------|
| **`sites`** | Scan server for gambling sites | Daily/Weekly |
| **`update-betting`** | Get latest keywords & code | If added new keywords |
| **`fix-betting`** | Repair permissions/issues | Only if something breaks |

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

### 📈 **Real-World Performance:**

#### **For 100 domains:**
- ⏱️ **Time:** ~5-10 minutes total
- 💾 **RAM:** < 50MB 
- 🔢 **CPU:** < 5% usage during scan

#### **For 500 domains:**
- ⏱️ **Time:** ~20-30 minutes total  
- 💾 **RAM:** < 50MB (same)
- 🔢 **CPU:** < 5% usage during scan

### ⚡ **Server Load Impact: MINIMAL**

#### 📊 **Resource Usage:**
- **CPU:** Very low (only during scan execution)
- **RAM:** < 50MB (per scan)
- **Disk:** < 5MB total
- **Network:** Minimal (only HTTP requests to your own domains)

### 🎯 **When to Run Scans:**

#### **Recommended Times:**
- ✅ Off-peak hours (2AM-5AM)
- ✅ Low traffic periods
- ✅ During maintenance windows

#### **Avoid:**
- ❌ Peak business hours
- ❌ High traffic times
- ❌ When server is already busy


