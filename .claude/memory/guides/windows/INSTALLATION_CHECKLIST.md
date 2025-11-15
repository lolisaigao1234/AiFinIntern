# IB Gateway Installation Checklist - Windows 11 Pro

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Purpose**: Step-by-step checklist for IB Gateway setup on Windows 11 Pro
**Estimated Time**: 30-45 minutes

---

## Table of Contents
1. [Pre-Installation Checklist](#pre-installation-checklist)
2. [Installation Checklist](#installation-checklist)
3. [Configuration Checklist](#configuration-checklist)
4. [Verification Checklist](#verification-checklist)
5. [Python Integration Checklist](#python-integration-checklist)
6. [Troubleshooting Checklist](#troubleshooting-checklist)

---

## Pre-Installation Checklist

### System Requirements

- [ ] **Operating System**: Windows 11 Pro (64-bit)
  ```powershell
  # Verify Windows version
  Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
  # Expected: Windows 11 Pro, 64-bit
  ```

- [ ] **Administrator Access**: You have admin rights
  ```powershell
  # Check if running as administrator
  ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  # Expected: True
  ```

- [ ] **Disk Space**: At least 1 GB free
  ```powershell
  # Check C: drive free space
  Get-PSDrive C | Select-Object Used, Free
  # Expected: Free > 1 GB
  ```

- [ ] **RAM**: At least 4 GB (8 GB recommended)
  ```powershell
  # Check total RAM
  (Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum / 1GB
  # Expected: >= 4 GB
  ```

- [ ] **Internet Connection**: Stable broadband
  ```powershell
  # Test connectivity
  Test-Connection -ComputerName google.com -Count 2
  # Expected: Successful pings
  ```

### Interactive Brokers Account

- [ ] **IB Account Created**: You have an IB account
  - Live account: https://www.interactivebrokers.com/en/home.php
  - Paper trading: https://www.interactivebrokers.com/en/home.php (request paper access)

- [ ] **Paper Trading Access Requested**: Approved for paper trading
  - Login to Client Portal
  - Navigate to Settings → Paper Trading
  - Request access (usually instant approval)

- [ ] **Credentials Ready**: Username and password accessible
  - Username: _______________
  - Password: (secure location)
  - Trading Mode: ☑ Paper Trading ☐ Live Trading

- [ ] **Two-Factor Authentication**: Know your 2FA method
  - IB Key app installed (if required)
  - Security code card available

### Software Prerequisites

- [ ] **Java**: IB Gateway includes Java (no action needed)
  ```powershell
  # Optional: Check if Java already installed
  java -version 2>&1
  # Note: IB Gateway uses bundled Java
  ```

- [ ] **Python**: Python 3.11+ installed
  ```powershell
  # Check Python version
  python --version
  # Expected: Python 3.11.x or higher
  ```

- [ ] **Poetry**: Poetry installed for dependency management
  ```powershell
  # Check Poetry version
  poetry --version
  # Expected: Poetry (version 2.x.x)
  ```

- [ ] **Git**: Git installed and configured
  ```powershell
  # Check Git version
  git --version
  # Expected: git version 2.x.x
  ```

### Firewall / Security

- [ ] **Windows Defender Firewall**: Status checked
  ```powershell
  # Check firewall status
  Get-NetFirewallProfile | Format-Table Name, Enabled
  # Note: May need to add firewall rules
  ```

- [ ] **Third-Party Antivirus**: Know if installed (Norton, McAfee, etc.)
  ```powershell
  # Check installed security software
  Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct
  ```

- [ ] **VPN**: Note if using VPN (may affect IB connection)

---

## Installation Checklist

### Download IB Gateway

- [ ] **Visit IB Gateway Download Page**
  ```powershell
  # Open download page
  Start-Process "https://www.interactivebrokers.com/en/trading/ibgateway-stable.php"
  ```

- [ ] **Download Latest Stable Version**
  - File: `ibgateway-stable-latest-windows-x64.exe`
  - Size: ~150 MB
  - Location: `C:\Users\<Username>\Downloads\`

- [ ] **Verify Downloaded File**
  ```powershell
  # Check download
  Get-Item "$env:USERPROFILE\Downloads\ibgateway*.exe"
  # Expected: File found, ~150 MB
  ```

### Run Installer

- [ ] **Run as Administrator**
  ```powershell
  # Launch installer as admin
  $Installer = Get-Item "$env:USERPROFILE\Downloads\ibgateway*.exe" | Select-Object -First 1
  Start-Process -FilePath $Installer.FullName -Verb RunAs
  ```
  - Or: Right-click → "Run as administrator"
  - Click "Yes" on UAC prompt

- [ ] **Welcome Screen**: Click "Next"

- [ ] **License Agreement**: Accept terms, click "Next"

- [ ] **Installation Folder**:
  - Default: `C:\Jts\ibgateway\<version>\`
  - Keep default ✅ or choose custom location
  - Click "Next"

- [ ] **Components**:
  - ✅ IB Gateway Application
  - ✅ Desktop Shortcut (recommended)
  - ✅ Start Menu Shortcut (recommended)
  - Click "Next"

- [ ] **Installation**: Click "Install", wait 1-2 minutes

- [ ] **Completion**:
  - ☐ Uncheck "Launch IB Gateway now"
  - Click "Finish"

### Verify Installation

- [ ] **Check Installation Directory**
  ```powershell
  # Verify installation
  Get-ChildItem "C:\Jts\ibgateway"
  # Expected: Version folder (e.g., 10.25)
  ```

- [ ] **Locate Executable**
  ```powershell
  # Find ibgateway.exe
  Get-ChildItem -Path "C:\Jts\ibgateway" -Recurse -Filter "ibgateway.exe"
  # Expected: C:\Jts\ibgateway\<version>\ibgateway.exe
  ```

- [ ] **Desktop Shortcut Created**: Icon on desktop ✅

---

## Configuration Checklist

### Initial Launch

- [ ] **Launch IB Gateway**
  - Double-click Desktop shortcut
  - Or: Start Menu → IB Gateway
  - Or: `& "C:\Jts\ibgateway\<version>\ibgateway.exe"`

- [ ] **Login Screen Appears**: IB Gateway window opens

- [ ] **Enter Credentials**:
  - Username: (your IB username)
  - Password: (your IB password)
  - Trading Mode: ☑ **Paper Trading** (IMPORTANT!)

- [ ] **Two-Factor Authentication**: Complete if prompted

- [ ] **First Login Prompts**:
  - Accept "Important Notices" if shown
  - Click "OK" on "Release Notes"

- [ ] **IB Gateway Running**: Status shows "Connected"

### API Configuration

See: [IB_API_CONFIGURATION_WINDOWS.md](./IB_API_CONFIGURATION_WINDOWS.md)

- [ ] **Open Global Configuration**
  - Menu: Configure → Settings
  - Or: Ctrl + Alt + G

- [ ] **Navigate to API Settings**
  - Left panel: Click **API**
  - Click **Settings** tab

- [ ] **Enable API** (CRITICAL!)
  - ✅ **"Enable ActiveX and Socket Clients"** MUST be checked!

- [ ] **Configure Socket Port**
  - Paper Trading: `7497` ✅
  - Live Trading: `7496` (not for development!)

- [ ] **Trusted IP Addresses**
  - Click "Configure..." next to Trusted IPs
  - Add: `127.0.0.1`
  - Click "OK"

- [ ] **Additional Settings**:
  - ✅ Download open orders on connection
  - ✅ Allow API account and financial information requests
  - Master API Client ID: `0` (default)

- [ ] **Auto-Restart** (Optional but recommended):
  - Left panel: Click **Startup**
  - Auto restart time: `11:55 PM EST`
  - Auto-logoff time: `11:50 PM EST`

- [ ] **Apply Settings**: Click "OK" to save

### Firewall Configuration

See: [WINDOWS_FIREWALL_SETUP.md](./WINDOWS_FIREWALL_SETUP.md)

- [ ] **Open PowerShell as Administrator**
  ```powershell
  Start-Process powershell -Verb RunAs
  ```

- [ ] **Allow IB Gateway Executable**
  ```powershell
  $IBGatewayExe = "C:\Jts\ibgateway\<version>\ibgateway.exe"

  New-NetFirewallRule -DisplayName "IB Gateway - Inbound" `
      -Direction Inbound -Program $IBGatewayExe -Action Allow -Profile Any

  New-NetFirewallRule -DisplayName "IB Gateway - Outbound" `
      -Direction Outbound -Program $IBGatewayExe -Action Allow -Profile Any
  ```

- [ ] **Allow IB Server Ports (4000, 4001)**
  ```powershell
  New-NetFirewallRule -DisplayName "IB Servers - Port 4000" `
      -Direction Outbound -RemotePort 4000 -Protocol TCP -Action Allow

  New-NetFirewallRule -DisplayName "IB Servers - Port 4001" `
      -Direction Outbound -RemotePort 4001 -Protocol TCP -Action Allow
  ```

- [ ] **Allow API Port 7497 (Localhost Only)**
  ```powershell
  New-NetFirewallRule -DisplayName "IB API - Port 7497 (Paper)" `
      -Direction Inbound -LocalPort 7497 -RemoteAddress 127.0.0.1 `
      -Protocol TCP -Action Allow
  ```

- [ ] **Verify Firewall Rules Created**
  ```powershell
  Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"}
  # Expected: 5+ rules
  ```

---

## Verification Checklist

### IB Gateway Running

- [ ] **Process Running**
  ```powershell
  Get-Process | Where-Object {$_.ProcessName -like "*java*"}
  # Expected: javaw.exe or similar
  ```

- [ ] **Port 7497 Listening**
  ```powershell
  netstat -an | findstr 7497
  # Expected: TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING
  ```

- [ ] **IB Gateway Window Shows**:
  - Status: "Connected" (green)
  - Account info displayed
  - No error messages

### Configuration File Check

- [ ] **Configuration File Exists**
  ```powershell
  Test-Path "$env:USERPROFILE\Jts\jts.ini"
  # Expected: True
  ```

- [ ] **API Settings Saved**
  ```powershell
  Get-Content "$env:USERPROFILE\Jts\jts.ini" | Select-String "api|port"
  # Expected: s.SocketPort=7497, s.ApiEnabled=true
  ```

---

## Python Integration Checklist

### Install ib_insync

- [ ] **Navigate to Project Directory**
  ```powershell
  cd C:\path\to\AiFinIntern
  ```

- [ ] **Install ib_insync via Poetry**
  ```powershell
  poetry add ib-insync
  # Expected: ib-insync added to dependencies
  ```

- [ ] **Or Install via pip**
  ```powershell
  pip install ib-insync
  # If not using Poetry
  ```

### Create Test Script

- [ ] **Create Connection Test**
  ```powershell
  @"
  from ib_insync import IB
  import sys

  print("Testing IB Gateway connection...")

  ib = IB()
  try:
      ib.connect('127.0.0.1', 7497, clientId=1)
      print("✅ Connected successfully!")
      print(f"Server time: {ib.reqCurrentTime()}")
      print(f"Managed accounts: {ib.managedAccounts()}")

      # Test account summary
      summary = ib.accountSummary()
      print(f"✅ Account summary: {len(summary)} items")

      ib.disconnect()
      print("✅ All tests passed!")
      sys.exit(0)

  except ConnectionRefusedError:
      print("❌ Connection refused!")
      print("1. Check IB Gateway is running")
      print("2. Check API is enabled in settings")
      print("3. Check port is 7497")
      sys.exit(1)

  except Exception as e:
      print(f"❌ Error: {e}")
      sys.exit(1)
  "@ | Out-File -FilePath test_ib_connection.py -Encoding utf8
  ```

### Run Test

- [ ] **Execute Test Script**
  ```powershell
  poetry run python test_ib_connection.py
  # Or: python test_ib_connection.py
  ```

- [ ] **Verify Output**:
  - ✅ "Connected successfully!"
  - ✅ Server time displayed
  - ✅ Account number shown (e.g., DU123456)
  - ✅ "All tests passed!"

- [ ] **No Errors**: Test completes without exceptions

---

## Troubleshooting Checklist

### If Connection Fails

- [ ] **IB Gateway is running**: Check window is open and "Connected"

- [ ] **API is enabled**: Configure → Settings → API → ✅ "Enable ActiveX and Socket Clients"

- [ ] **Port is correct**: 7497 for paper trading

- [ ] **Firewall allows connection**: Run firewall setup script

- [ ] **Restart IB Gateway**: Close completely and relaunch

- [ ] **Check logs**:
  ```powershell
  Get-ChildItem "$env:USERPROFILE\Jts\logs\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
  ```

### If API Not Enabled Error

- [ ] Open Global Configuration
- [ ] API → Settings
- [ ] ✅ Check "Enable ActiveX and Socket Clients"
- [ ] Click "OK"
- [ ] **Restart IB Gateway** (important!)

### If Port 7497 Not Listening

- [ ] IB Gateway fully started (not just login window)
- [ ] API enabled in settings
- [ ] Configuration saved (click "OK" not "Cancel")
- [ ] Restart IB Gateway

---

## Final Verification Checklist

Before proceeding to development:

- [ ] ✅ IB Gateway installed at `C:\Jts\ibgateway\<version>\`
- [ ] ✅ IB Gateway launches successfully
- [ ] ✅ Login works with paper trading account
- [ ] ✅ API enabled in Global Configuration
- [ ] ✅ Socket Port set to 7497
- [ ] ✅ Trusted IP includes 127.0.0.1
- [ ] ✅ Firewall rules created and active
- [ ] ✅ Port 7497 listening on localhost
- [ ] ✅ Python ib_insync installed
- [ ] ✅ Test script connects successfully
- [ ] ✅ Account data retrieved via API
- [ ] ✅ No errors in test output

---

## Next Steps

After completing this checklist:

1. ✅ IB Gateway fully configured
2. ✅ Python can connect to API
3. ✅ Ready for bot development

**Proceed to**:
- [IB API Testing Setup](../IB_API_TESTING_SETUP_TODOS.md)
- [Quick Start Guide](../QUICK_START_IB_RESEARCH.md)
- Begin implementing test files from Phase 3

---

## Quick Commands Reference

```powershell
# Launch IB Gateway
& "C:\Jts\ibgateway\<version>\ibgateway.exe"

# Check if running
Get-Process | Where-Object {$_.ProcessName -like "*java*"}

# Check port 7497
netstat -an | findstr 7497

# Test Python connection
poetry run python test_ib_connection.py

# View firewall rules
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"}

# View configuration
Get-Content "$env:USERPROFILE\Jts\jts.ini" | Select-String "api|port"
```

---

## Estimated Time Breakdown

| Phase | Estimated Time |
|-------|----------------|
| Pre-Installation Checks | 5 minutes |
| Download & Install | 5-10 minutes |
| Configuration | 10-15 minutes |
| Firewall Setup | 5 minutes |
| Python Integration | 5 minutes |
| Testing & Verification | 5 minutes |
| **Total** | **30-45 minutes** |

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
**Checklist Items**: 100+
