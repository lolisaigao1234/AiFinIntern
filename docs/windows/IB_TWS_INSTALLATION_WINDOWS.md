# Trader Workstation (TWS) Installation Guide - Windows 11 Pro

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Platform**: Windows 11 Pro
**Target Software**: Interactive Brokers Trader Workstation (Latest Stable)

---

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Download TWS](#download-tws)
4. [Installation Steps](#installation-steps)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Trader Workstation (TWS) is Interactive Brokers' full-featured desktop trading platform. It includes advanced charting, market data, order management, and API capabilities.

### TWS vs IB Gateway

| Feature | TWS | IB Gateway |
|---------|-----|-----------|
| **GUI** | Full trading platform with charts | Minimal login window |
| **Resource Usage** | High (500-800 MB RAM) | Low (50-100 MB RAM) |
| **Features** | Charts, scanners, news, research | API connection only |
| **Ideal For** | Manual trading + automation | Pure API/bot development |
| **Complexity** | High (many features) | Low (simple) |

**Recommendation**:
- Use **IB Gateway** for pure algorithmic trading (recommended for this project)
- Use **TWS** if you need manual trading alongside API

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or Windows 11
- **RAM**: 4 GB (8 GB recommended)
- **Disk Space**: 1 GB free space
- **CPU**: Dual-core processor
- **Java**: Java 11+ (bundled with installer)
- **Display**: 1024x768 minimum (1920x1080 recommended)
- **Internet**: Stable broadband connection

### Recommended Requirements
- **OS**: Windows 11 Pro (64-bit)
- **RAM**: 16 GB or higher
- **Disk Space**: 2 GB free space
- **CPU**: Multi-core processor (AMD Ryzen 7 or Intel i7+)
- **Display**: Multi-monitor setup for optimal workflow
- **Internet**: Low-latency connection (< 50ms to IB servers)

---

## Download TWS

### Official Download Link

**Latest Stable Version** (Recommended):
- **URL**: https://www.interactivebrokers.com/en/trading/tws.php
- **File**: `tws-latest-windows-x64.exe`
- **Size**: ~200 MB
- **Version**: 10.25+ (as of 2025-11-15)

### Download Instructions

```powershell
# Open download page in browser
Start-Process "https://www.interactivebrokers.com/en/trading/tws.php"

# Or navigate to Downloads folder
cd $env:USERPROFILE\Downloads
```

**Verify Download**:
- File size: ~200 MB
- File name: `tws-latest-windows-x64.exe`
- Location: `C:\Users\<YourUsername>\Downloads\`

---

## Installation Steps

### Step 1: Run Installer

```powershell
# Navigate to Downloads
cd $env:USERPROFILE\Downloads

# Run installer as administrator
Start-Process -FilePath ".\tws-latest-windows-x64.exe" -Verb RunAs
```

Or right-click `tws-latest-windows-x64.exe` → "Run as administrator"

### Step 2: Installation Wizard

1. **Welcome Screen**:
   - Click "Next"

2. **License Agreement**:
   - Read and accept IB API License
   - Click "Next"

3. **Installation Folder**:
   - Default: `C:\Jts\<version>\`
   - Click "Next"

4. **Select Components**:
   - ✅ TWS Application (required)
   - ✅ Desktop Shortcut (recommended)
   - ✅ Start Menu Shortcut (recommended)
   - Click "Next"

5. **Installation**:
   - Click "Install"
   - Wait 2-3 minutes

6. **Completion**:
   - Click "Finish"

### Step 3: Verify Installation

```powershell
# Check installation directory
Get-ChildItem "C:\Jts"

# Expected: Version folder (e.g., 1025)
```

---

## Configuration

### Initial Launch

```powershell
# Launch TWS
& "C:\Jts\<version>\tws.exe"
```

Or use Desktop shortcut

### Login

1. **Username**: Your IB username
2. **Password**: Your IB password
3. **Trading Mode**:
   - ☑ **Paper Trading** (for development/testing)
   - ☐ Live Trading (production only)
4. Click "Login"

### API Configuration (For Python Bot)

**Configure → Settings → API**:

1. ✅ **Enable ActiveX and Socket Clients**
2. **Socket Port**:
   - Paper Trading: `7497`
   - Live Trading: `7496`
3. **Trusted IPs**: Add `127.0.0.1`
4. **Click "OK"**

For detailed API configuration, see: [IB_API_CONFIGURATION_WINDOWS.md](./IB_API_CONFIGURATION_WINDOWS.md)

---

## Verification

### Check TWS is Running

```powershell
# Check process
Get-Process | Where-Object {$_.ProcessName -like "*java*" -or $_.MainWindowTitle -like "*TWS*"}

# Check API port
netstat -an | findstr 7497
# Expected: TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING
```

### Test API Connection

```powershell
# Create test script
@"
from ib_insync import IB

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
print(f'✅ Connected to TWS!')
print(f'Account: {ib.managedAccounts()}')
ib.disconnect()
"@ | Out-File -FilePath test_tws.py -Encoding utf8

# Run test
poetry run python test_tws.py
```

---

## Troubleshooting

### Common Issues

**Problem**: "Connection refused"
**Solution**:
1. Ensure TWS is running
2. Check API is enabled in settings
3. Verify port 7497 is open

**Problem**: High memory usage
**Solution**:
1. Close unnecessary charts/windows
2. Reduce market data subscriptions
3. Consider using IB Gateway instead

For detailed troubleshooting, see the IB Gateway guide: [IB_GATEWAY_INSTALLATION_WINDOWS.md](./IB_GATEWAY_INSTALLATION_WINDOWS.md)

---

## Recommendation for This Project

**For algorithmic trading bot development**:
- ✅ Use **IB Gateway** (lightweight, optimized for API)
- ❌ Avoid TWS (unnecessary features, higher resource usage)

See: [IB_GATEWAY_INSTALLATION_WINDOWS.md](./IB_GATEWAY_INSTALLATION_WINDOWS.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Reference Only (IB Gateway recommended for project)
