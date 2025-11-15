# IB Gateway Installation Guide - Windows 11 Pro

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Platform**: Windows 11 Pro
**Target Software**: Interactive Brokers Gateway (Latest Stable)

---

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Prerequisites](#prerequisites)
4. [Download IB Gateway](#download-ib-gateway)
5. [Installation Steps](#installation-steps)
6. [Configuration](#configuration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)
9. [Uninstallation](#uninstallation)

---

## Overview

IB Gateway is a lightweight Java-based application provided by Interactive Brokers for API connections. It's optimized for automated trading and provides a stable, headless connection to IB's trading servers.

### Why IB Gateway vs TWS?

| Feature | IB Gateway | TWS (Trader Workstation) |
|---------|-----------|--------------------------|
| **Resource Usage** | Low (50-100 MB RAM) | High (500+ MB RAM) |
| **GUI** | Minimal login window only | Full trading platform |
| **Ideal For** | Automated trading, bots | Manual trading, charting |
| **Stability** | Excellent | Good |
| **Auto-restart** | Built-in support | Manual configuration |
| **API Performance** | Optimized | Standard |

**Recommendation**: Use IB Gateway for algorithmic trading projects.

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or Windows 11
- **RAM**: 2 GB (4 GB recommended)
- **Disk Space**: 500 MB free space
- **Java**: Java 11+ (bundled with installer)
- **Internet**: Stable broadband connection
- **Firewall**: Ports 4000, 4001 (IB), 7496/7497 (API) open

### Recommended Requirements
- **OS**: Windows 11 Pro (64-bit)
- **RAM**: 8 GB or higher
- **Disk Space**: 1 GB free space
- **CPU**: Multi-core processor (AMD Ryzen 7 or Intel i7+)
- **Internet**: Low-latency connection (< 50ms to IB servers)

---

## Prerequisites

### 1. Interactive Brokers Account

You need an active IB account (live or paper trading):

**Paper Trading Account** (Recommended for Testing):
- Sign up at: https://www.interactivebrokers.com/en/home.php
- Request paper trading access in Client Portal
- Username format: Usually `edemo` or your username with paper suffix
- Note: Paper account replicates live trading without real money

**Live Trading Account**:
- Requires funded account with IB
- Complete verification process
- Not recommended for initial bot development

### 2. Administrator Privileges

You'll need administrator rights on Windows 11 Pro to:
- Install IB Gateway software
- Configure Windows Firewall
- Set up auto-restart (optional)

### 3. Antivirus Considerations

IB Gateway uses Java networking. You may need to:
- Add IB Gateway to antivirus exceptions
- Allow Java processes in Windows Defender Firewall
- Whitelist IB servers in network security software

---

## Download IB Gateway

### Official Download Links

**Latest Stable Version** (Recommended):
- **URL**: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php
- **File**: `ibgateway-stable-latest-windows-x64.exe`
- **Size**: ~150 MB
- **Version**: 10.25+ (as of 2025-11-15)

**Latest Beta Version** (Advanced Users):
- **URL**: https://www.interactivebrokers.com/en/trading/ibgateway-latest.php
- **File**: `ibgateway-latest-windows-x64.exe`
- **Note**: May have new features but less stable

### Download Instructions

1. **Visit Official Website**:
   ```powershell
   # Open in default browser
   Start-Process "https://www.interactivebrokers.com/en/trading/ibgateway-stable.php"
   ```

2. **Download via PowerShell** (Optional):
   ```powershell
   # Set download path
   $DownloadPath = "$env:USERPROFILE\Downloads\ibgateway-latest-windows-x64.exe"

   # Download IB Gateway installer
   # Note: Direct download URL may change, visit website to get latest link
   # Example (URL may vary):
   # Invoke-WebRequest -Uri "https://download2.interactivebrokers.com/installers/ibgateway/stable-standalone/ibgateway-stable-standalone-windows-x64.exe" -OutFile $DownloadPath

   # Verify download
   Get-Item $DownloadPath
   ```

3. **Verify Download**:
   - Check file size: ~150 MB
   - File name: `ibgateway-*-windows-x64.exe`
   - Location: `C:\Users\<YourUsername>\Downloads\`

---

## Installation Steps

### Step 1: Run Installer

1. **Locate Downloaded File**:
   ```powershell
   # Navigate to Downloads
   cd $env:USERPROFILE\Downloads

   # List IB Gateway installer
   Get-ChildItem -Filter "ibgateway*.exe"
   ```

2. **Run as Administrator**:
   - Right-click `ibgateway-latest-windows-x64.exe`
   - Select "Run as administrator"
   - Click "Yes" on UAC prompt

   **Or via PowerShell**:
   ```powershell
   # Run installer as administrator
   Start-Process -FilePath ".\ibgateway-latest-windows-x64.exe" -Verb RunAs
   ```

### Step 2: Installation Wizard

1. **Welcome Screen**:
   - Click "Next" to begin installation

2. **License Agreement**:
   - Read the IB API Non-Commercial License Agreement
   - Check "I accept the terms in the License Agreement"
   - Click "Next"

3. **Select Installation Folder**:
   - **Default**: `C:\Jts\ibgateway\<version>\`
   - **Recommended**: Keep default location
   - **Custom**: Choose if you have specific requirements
   - Click "Next"

4. **Select Components**:
   - ✅ **IB Gateway Application** (required)
   - ✅ **Desktop Shortcut** (recommended)
   - ✅ **Start Menu Shortcut** (recommended)
   - Click "Next"

5. **Ready to Install**:
   - Review installation settings
   - Click "Install"

6. **Installation Progress**:
   - Wait for installation to complete (1-2 minutes)
   - Do not close installer window

7. **Completion**:
   - ✅ "IB Gateway has been successfully installed"
   - ☐ Launch IB Gateway now (optional, uncheck for now)
   - Click "Finish"

### Step 3: Post-Installation

1. **Verify Installation**:
   ```powershell
   # Check installation directory
   Get-ChildItem "C:\Jts\ibgateway"

   # Expected output: Version folder (e.g., 10.25)
   ```

2. **Locate Executable**:
   ```powershell
   # Find ibgateway.exe
   Get-ChildItem -Path "C:\Jts\ibgateway" -Recurse -Filter "ibgateway.exe"

   # Expected: C:\Jts\ibgateway\<version>\ibgateway.exe
   ```

---

## Configuration

### Initial Launch and Setup

1. **Launch IB Gateway**:
   - **Option A**: Double-click Desktop shortcut
   - **Option B**: Start Menu → IB Gateway
   - **Option C**: PowerShell:
     ```powershell
     # Launch IB Gateway
     & "C:\Jts\ibgateway\<version>\ibgateway.exe"
     ```

2. **Login Screen**:
   - **Username**: Your IB username (or paper trading username)
   - **Password**: Your IB password
   - **Trading Mode**:
     - ☑ **Paper Trading** (recommended for development)
     - ☐ Live Trading (production only)
   - Click "Login"

3. **First Login**:
   - May prompt for two-factor authentication (if enabled)
   - May show "Important Notices" - read and accept
   - May show "Release Notes" - click OK

### API Configuration

**IMPORTANT**: Must configure API settings before Python can connect!

1. **Open Configuration**:
   - In IB Gateway window
   - Menu: **Configure** → **Settings**
   - Or: **File** → **Global Configuration**

2. **Navigate to API Settings**:
   - Left panel: Click **API**
   - Click **Settings** tab

3. **Enable API**:
   - ✅ **Enable ActiveX and Socket Clients** (MUST be checked!)
   - ☐ Read-Only API (leave unchecked for trading)

4. **Configure Socket Port**:
   - **Paper Trading**: `7497` (recommended)
   - **Live Trading**: `7496` (use with caution!)
   - Default is usually correct

5. **Trusted IP Addresses**:
   - Click "Configure..." next to "Trusted IPs"
   - Add: `127.0.0.1` (localhost)
   - Optional: Add your local network IP if needed
   - Click "OK"

6. **Master API Client ID** (Optional):
   - Default: `0` (any client ID allowed)
   - Recommended: Leave as `0` or set to `1`
   - This restricts which client IDs can connect

7. **Additional Settings**:
   - ✅ **Allow connections from localhost** (auto-checked if 127.0.0.1 in trusted IPs)
   - ☐ **Expose entire trading schedule** (optional)
   - ✅ **Download open orders on connection** (recommended)
   - ✅ **Allow API account and financial information requests** (recommended)

8. **Auto-Restart Settings** (Recommended):
   - Left panel: Click **Startup**
   - **Auto restart**: Select time (e.g., 11:55 PM EST)
   - ✅ **Auto-logoff time**: 11:50 PM EST
   - ✅ **Auto-restart on disconnection** (optional)
   - This prevents IB Gateway from closing unexpectedly

9. **Apply and Save**:
   - Click "OK" to save all settings
   - Settings are saved to: `%USERPROFILE%\Jts\jts.ini`

### Configuration File Location

```powershell
# View IB Gateway configuration file
$ConfigPath = "$env:USERPROFILE\Jts\jts.ini"
Get-Content $ConfigPath | Select-String -Pattern "port|socket|api"
```

---

## Verification

### Verify IB Gateway is Running

1. **Check Process**:
   ```powershell
   # Check if IB Gateway process is running
   Get-Process | Where-Object {$_.ProcessName -like "*java*" -or $_.ProcessName -like "*ibgateway*"}

   # Expected: javaw.exe or similar Java process
   ```

2. **Check Port 7497 is Open**:
   ```powershell
   # Method 1: Using netstat
   netstat -an | findstr 7497

   # Expected output:
   # TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING

   # Method 2: Using PowerShell cmdlet
   Get-NetTCPConnection -LocalPort 7497 -ErrorAction SilentlyContinue

   # Expected: State = Listen, LocalAddress = 127.0.0.1
   ```

3. **Check IB Gateway Window**:
   - Should see: "IB Gateway is running"
   - Status bar: Connected to IB servers
   - Account info displayed

### Test API Connection with Python

1. **Create Test Script**:
   ```powershell
   # Navigate to project directory
   cd C:\path\to\AiFinIntern

   # Create test script
   @"
   from ib_insync import IB
   import time

   print("Testing IB Gateway connection...")

   ib = IB()
   try:
       ib.connect('127.0.0.1', 7497, clientId=1)
       print("✅ Successfully connected to IB Gateway!")
       print(f"Server time: {ib.reqCurrentTime()}")
       print(f"Managed accounts: {ib.managedAccounts()}")

       # Test account summary
       summary = ib.accountSummary()
       print(f"Account summary items: {len(summary)}")

       ib.disconnect()
       print("✅ Disconnected successfully")
   except Exception as e:
       print(f"❌ Connection failed: {e}")
   "@ | Out-File -FilePath test_ib_gateway.py -Encoding utf8
   ```

2. **Run Test**:
   ```powershell
   # Using Poetry
   poetry run python test_ib_gateway.py

   # Or with pip venv
   python test_ib_gateway.py
   ```

3. **Expected Output**:
   ```
   Testing IB Gateway connection...
   ✅ Successfully connected to IB Gateway!
   Server time: 2025-11-15 20:30:45
   Managed accounts: ['DU123456']
   Account summary items: 15
   ✅ Disconnected successfully
   ```

---

## Troubleshooting

### Connection Issues

#### Problem: "Connection refused"
**Symptoms**:
```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
```

**Solutions**:
1. **Check IB Gateway is running**:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*java*"}
   ```

2. **Verify port 7497**:
   ```powershell
   netstat -an | findstr 7497
   ```

3. **Check API is enabled**:
   - IB Gateway → Configure → Settings → API
   - ✅ "Enable ActiveX and Socket Clients" must be checked

4. **Restart IB Gateway**:
   - Close IB Gateway completely
   - Relaunch and login again

#### Problem: "API client not enabled"
**Symptoms**: IB Gateway shows error "API client not enabled"

**Solutions**:
1. Enable API in settings (see Configuration section above)
2. Ensure port 7497 is configured
3. Restart IB Gateway after enabling

#### Problem: "Not connected"
**Symptoms**: IB Gateway window shows "Not connected" in red

**Solutions**:
1. **Check internet connection**:
   ```powershell
   Test-Connection -ComputerName google.com -Count 2
   ```

2. **Check IB server status**:
   - Visit: https://www.interactivebrokers.com/en/index.php?f=2225
   - Check for system outages

3. **Verify credentials**:
   - Correct username/password
   - Paper trading mode selected (if using paper account)

4. **Check firewall** (see Firewall section below)

### Firewall Issues

#### Windows Defender Firewall Blocking IB Gateway

1. **Add IB Gateway to Firewall Exceptions**:
   ```powershell
   # Run as Administrator

   # Allow IB Gateway executable
   New-NetFirewallRule -DisplayName "IB Gateway - Inbound" `
       -Direction Inbound `
       -Program "C:\Jts\ibgateway\<version>\ibgateway.exe" `
       -Action Allow `
       -Profile Any

   New-NetFirewallRule -DisplayName "IB Gateway - Outbound" `
       -Direction Outbound `
       -Program "C:\Jts\ibgateway\<version>\ibgateway.exe" `
       -Action Allow `
       -Profile Any
   ```

2. **Allow Ports 4000, 4001 (IB Servers)**:
   ```powershell
   # Inbound rules for IB server ports
   New-NetFirewallRule -DisplayName "IB Servers Port 4000" `
       -Direction Inbound `
       -LocalPort 4000 `
       -Protocol TCP `
       -Action Allow

   New-NetFirewallRule -DisplayName "IB Servers Port 4001" `
       -Direction Inbound `
       -LocalPort 4001 `
       -Protocol TCP `
       -Action Allow
   ```

3. **Allow API Ports 7496, 7497** (Localhost only):
   ```powershell
   # Allow API ports for localhost connections only
   New-NetFirewallRule -DisplayName "IB API Port 7497 (Paper)" `
       -Direction Inbound `
       -LocalPort 7497 `
       -Protocol TCP `
       -Action Allow `
       -RemoteAddress 127.0.0.1

   New-NetFirewallRule -DisplayName "IB API Port 7496 (Live)" `
       -Direction Inbound `
       -LocalPort 7496 `
       -Protocol TCP `
       -Action Allow `
       -RemoteAddress 127.0.0.1
   ```

### Java Issues

#### Problem: "Java not found" or outdated Java

**Solutions**:
1. IB Gateway includes bundled Java - should work out of box
2. If issues persist, check Java version:
   ```powershell
   # Check Java version
   java -version

   # Expected: Java 11 or higher
   ```

3. Update Java if needed:
   - Download from: https://www.java.com/en/download/
   - Or install OpenJDK: https://adoptium.net/

### Performance Issues

#### Problem: IB Gateway uses too much RAM/CPU

**Solutions**:
1. **Increase Java heap size** (advanced):
   - Edit: `C:\Jts\ibgateway\<version>\ibgateway.vmoptions`
   - Modify: `-Xmx` parameter (default: 768m)
   - Example: `-Xmx1024m` for 1GB heap

2. **Disable unnecessary features**:
   - Configure → Settings → Display
   - Uncheck "Show news bulletins"
   - Disable market data subscriptions not needed

3. **Use IB Gateway instead of TWS** (already doing this!)

---

## Uninstallation

### Standard Uninstall

1. **Via Windows Settings**:
   ```powershell
   # Open Apps & Features
   Start-Process "ms-settings:appsfeatures"
   ```
   - Search for "IB Gateway"
   - Click "Uninstall"
   - Follow prompts

2. **Via Control Panel**:
   - Control Panel → Programs → Uninstall a program
   - Find "IB Gateway"
   - Click "Uninstall"

### Complete Removal (Clean Uninstall)

```powershell
# Close IB Gateway first
Get-Process | Where-Object {$_.ProcessName -like "*java*"} | Stop-Process -Force

# Remove installation directory
Remove-Item -Path "C:\Jts\ibgateway" -Recurse -Force -ErrorAction SilentlyContinue

# Remove user configuration
Remove-Item -Path "$env:USERPROFILE\Jts" -Recurse -Force -ErrorAction SilentlyContinue

# Remove shortcuts
Remove-Item -Path "$env:USERPROFILE\Desktop\IB Gateway*.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\IB Gateway*.lnk" -Force -ErrorAction SilentlyContinue

# Remove firewall rules (optional)
Remove-NetFirewallRule -DisplayName "IB Gateway*" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "IB API*" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "IB Servers*" -ErrorAction SilentlyContinue
```

---

## Quick Reference

### Key Directories

| Path | Purpose |
|------|---------|
| `C:\Jts\ibgateway\<version>\` | Installation directory |
| `C:\Jts\ibgateway\<version>\ibgateway.exe` | Main executable |
| `%USERPROFILE%\Jts\jts.ini` | Configuration file |
| `%USERPROFILE%\Jts\logs\` | Log files |

### Key Ports

| Port | Purpose | Mode |
|------|---------|------|
| 7497 | API Socket Port | Paper Trading |
| 7496 | API Socket Port | Live Trading |
| 4000 | IB Server Connection | Both |
| 4001 | IB Server Connection | Both |

### Key Commands

```powershell
# Launch IB Gateway
& "C:\Jts\ibgateway\<version>\ibgateway.exe"

# Check if running
Get-Process | Where-Object {$_.ProcessName -like "*java*"}

# Check API port
netstat -an | findstr 7497

# View configuration
Get-Content "$env:USERPROFILE\Jts\jts.ini"

# View logs
Get-ChildItem "$env:USERPROFILE\Jts\logs\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

---

## Next Steps

After successful installation:

1. ✅ IB Gateway installed and configured
2. ✅ API enabled on port 7497
3. ✅ Connection verified with Python test

**Next**:
- Review: [IB API Configuration Guide](./IB_API_CONFIGURATION_WINDOWS.md)
- Review: [Windows Firewall Setup](./WINDOWS_FIREWALL_SETUP.md)
- Start testing: [Quick Start Guide](../QUICK_START_IB_RESEARCH.md)

---

## Additional Resources

- **Official IB Gateway Documentation**: https://www.interactivebrokers.com/en/trading/ibgateway.php
- **IB API Documentation**: https://interactivebrokers.github.io/tws-api/
- **ib_insync Documentation**: https://ib-insync.readthedocs.io/
- **IB System Status**: https://www.interactivebrokers.com/en/index.php?f=2225
- **IB Support**: https://www.interactivebrokers.com/en/support/support.php

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
**Tested On**: Windows 11 Pro (64-bit)
