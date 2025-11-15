# IB API Configuration Guide - Windows 11 Pro

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Platform**: Windows 11 Pro
**Applies To**: IB Gateway and TWS

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [API Settings Configuration](#api-settings-configuration)
4. [Port Configuration](#port-configuration)
5. [Security Settings](#security-settings)
6. [Auto-Restart Configuration](#auto-restart-configuration)
7. [Advanced Settings](#advanced-settings)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers all API configuration settings for Interactive Brokers Gateway and TWS on Windows 11 Pro. Proper configuration is **mandatory** for Python bot connectivity.

---

## Prerequisites

- IB Gateway or TWS installed ([Installation Guide](./IB_GATEWAY_INSTALLATION_WINDOWS.md))
- Valid IB account (paper or live)
- Administrator access on Windows 11 Pro

---

## API Settings Configuration

### Step 1: Launch IB Gateway/TWS

```powershell
# For IB Gateway
& "C:\Jts\ibgateway\<version>\ibgateway.exe"

# For TWS
& "C:\Jts\<version>\tws.exe"
```

Login with your credentials.

### Step 2: Open Global Configuration

**Method 1**: Via Menu
- Click **Configure** → **Settings**

**Method 2**: Via File Menu
- Click **File** → **Global Configuration**

**Method 3**: Keyboard Shortcut
- Press `Ctrl + Alt + G`

### Step 3: Navigate to API Settings

1. Left sidebar: Click **API**
2. Click **Settings** tab

### Step 4: Enable API

**CRITICAL**: Must enable API for any Python connection!

✅ **Enable ActiveX and Socket Clients**
- This checkbox **MUST** be checked
- If unchecked, all API connections will fail

☐ **Read-Only API** (Optional)
- Check this ONLY if you want read-only access (no order placement)
- Leave unchecked for trading bot (recommended)

☐ **Download open orders on connection** (Recommended: ✅)
- Automatically retrieves open orders when bot connects
- Useful for position tracking

☐ **Use negative numbers to bind automatic orders** (Advanced)
- Leave unchecked unless you have specific requirements

☐ **Expose entire trading schedule** (Optional)
- Provides detailed trading calendar data
- Not required for basic bot operation

☐ **Allow API account and financial information requests** (Recommended: ✅)
- Allows bot to request account summary, positions, P&L
- Required for account monitoring features

---

## Port Configuration

### Socket Port Settings

**Location**: API Settings → Socket Port field

| Trading Mode | Recommended Port | Standard Port |
|--------------|-----------------|---------------|
| **Paper Trading** | `7497` | 7497 |
| **Live Trading** | `7496` | 7496 |

**Configuration**:
```
Socket Port: 7497
```

**IMPORTANT**:
- Paper trading: **Always use 7497**
- Live trading: **Use 7496** (extreme caution!)
- Never confuse ports - using wrong port can result in real trades!

### Verify Port in Configuration File

```powershell
# View IB configuration
$ConfigPath = "$env:USERPROFILE\Jts\jts.ini"
Get-Content $ConfigPath | Select-String -Pattern "port"

# Expected output:
# s.SocketPort=7497
```

---

## Security Settings

### Trusted IP Addresses

**Location**: API Settings → Configure... (next to Trusted IPs field)

**Required Configuration**:
1. Click "**Configure...**" button
2. Add IP address: `127.0.0.1` (localhost)
3. Click "**Add**"
4. Click "**OK**"

**Why 127.0.0.1?**
- Allows connections from same machine only
- Most secure for local development
- Prevents remote attacks

**Additional IPs** (Optional):
- Add your local network IP if running bot on different machine
- Example: `192.168.1.100`
- **WARNING**: Only add IPs you control!

### Master API Client ID

**Location**: API Settings → Master API Client ID field

**Options**:
- **0** (Default) - Any client ID can connect
- **1-9999** - Only specific client ID can connect

**Recommendation**:
- Use `0` for development (flexibility)
- Use `1` for production (additional security)

### Allow Connections from Localhost

**Location**: API Settings

☑ **Allow connections from localhost** (Auto-checked if 127.0.0.1 in trusted IPs)

This should automatically check when you add 127.0.0.1 to trusted IPs.

---

## Auto-Restart Configuration

**Prevents IB Gateway from closing unexpectedly**

### Navigate to Startup Settings

1. Global Configuration → **Startup** (left sidebar)

### Configure Auto-Restart

**Auto restart time**: `11:55 PM EST` (23:55:00)
- IB Gateway will automatically restart at this time
- Choose a time when bot is not actively trading
- Recommended: Late night (11:55 PM EST)

**Auto-logoff time**: `11:50 PM EST` (23:50:00)
- Gateway logs off 5 minutes before restart
- Ensures clean shutdown

☑ **Auto-restart on disconnection** (Optional)
- Automatically restarts if connection to IB servers drops
- Recommended for production bots
- May cause issues during maintenance windows

☑ **Re-login automatically** (Recommended: ✅)
- Automatically logs back in after restart
- Requires saved credentials (security consideration!)

### Auto-Logoff Configuration

**Days to stay logged in**: `7 days` (default)
- How long before forcing manual re-authentication
- Recommended: 7 days for development, 1 day for production

---

## Advanced Settings

### Market Data Lines

**Location**: API Settings → Market Data Lines

**Default**: `100` lines
- Maximum number of simultaneous market data subscriptions
- More lines = higher subscription fees
- Bot typically needs 10-50 lines depending on strategy

**Recommendation**: Keep default unless you need more

### Precautionary Settings

**Location**: Trading → Precautionary Settings

☑ **Enable Order Pre-cautions** (Recommended: ✅)
- Shows warning before submitting large orders
- Helps prevent accidental order placement
- Can be disabled for production bot (after testing!)

☑ **Show warning before cancelling orders** (Optional)
- Recommended for manual trading
- Can be disabled for bot automation

### Bypass Order Precautions (Advanced)

**Location**: API Settings

☐ **Bypass Order Precautions for API orders** (Use with caution!)
- If checked: No warnings for API orders
- Recommended: Leave unchecked during development
- Enable only after thorough testing

---

## Verification

### Verify API Settings

```powershell
# Check configuration file
$ConfigPath = "$env:USERPROFILE\Jts\jts.ini"

# View all API-related settings
Get-Content $ConfigPath | Select-String -Pattern "api|socket|port"

# Expected output includes:
# s.SocketPort=7497
# s.SocketPortSecurityLevel=0
# s.ApiEnabled=true
```

### Test API Connection

**Create Verification Script**:
```powershell
@"
from ib_insync import IB
import sys

print("IB API Configuration Test")
print("=" * 50)

ib = IB()

try:
    # Attempt connection
    print("Connecting to IB Gateway on 127.0.0.1:7497...")
    ib.connect('127.0.0.1', 7497, clientId=1)

    print("✅ Connection successful!")
    print(f"Server time: {ib.reqCurrentTime()}")
    print(f"Managed accounts: {ib.managedAccounts()}")

    # Test account summary request
    print("\nTesting account data request...")
    summary = ib.accountSummary()
    print(f"✅ Account summary received: {len(summary)} items")

    # Test position request
    print("\nTesting position data request...")
    positions = ib.positions()
    print(f"✅ Positions received: {len(positions)} items")

    ib.disconnect()
    print("\n✅ All API configuration tests passed!")
    sys.exit(0)

except ConnectionRefusedError:
    print("❌ Connection refused!")
    print("Solutions:")
    print("1. Ensure IB Gateway is running")
    print("2. Check API is enabled: Configure → Settings → API")
    print("3. Verify 'Enable ActiveX and Socket Clients' is checked")
    print("4. Verify port is 7497")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
"@ | Out-File -FilePath test_api_config.py -Encoding utf8

# Run test
poetry run python test_api_config.py
```

**Expected Output**:
```
IB API Configuration Test
==================================================
Connecting to IB Gateway on 127.0.0.1:7497...
✅ Connection successful!
Server time: 2025-11-15 20:30:45
Managed accounts: ['DU123456']

Testing account data request...
✅ Account summary received: 15 items

Testing position data request...
✅ Positions received: 0 items

✅ All API configuration tests passed!
```

### Verify Port is Listening

```powershell
# Check port 7497
netstat -an | findstr 7497

# Expected:
# TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING

# Or using PowerShell cmdlet
Get-NetTCPConnection -LocalPort 7497 -ErrorAction SilentlyContinue | Format-Table LocalPort, State, LocalAddress

# Expected: State = Listen
```

---

## Troubleshooting

### Problem: "API client not enabled"

**Error Message**: "API client not enabled. Please check Global Configuration."

**Solution**:
1. Open Global Configuration
2. API → Settings
3. ✅ Check "Enable ActiveX and Socket Clients"
4. Click "OK"
5. **Restart IB Gateway** (important!)

### Problem: Connection refused

**Error**: `ConnectionRefusedError: [Errno 10061]`

**Checklist**:
- [ ] IB Gateway is running
- [ ] API is enabled (checkbox checked)
- [ ] Port is 7497 (paper trading)
- [ ] 127.0.0.1 is in trusted IPs
- [ ] Firewall allows port 7497

**Solution**:
```powershell
# 1. Check if IB Gateway is running
Get-Process | Where-Object {$_.ProcessName -like "*java*"}

# 2. Check port
netstat -an | findstr 7497

# 3. Restart IB Gateway
# Close and reopen IB Gateway application
```

### Problem: "Client ID X is already in use"

**Error**: "Socket port 7497 is in use."

**Causes**:
1. Another bot/script is connected with same client ID
2. Previous connection didn't disconnect properly

**Solutions**:
```powershell
# Option 1: Use different client ID
# In Python: ib.connect('127.0.0.1', 7497, clientId=2)  # Changed from 1 to 2

# Option 2: Disconnect previous connection
# Close all Python scripts using IB API

# Option 3: Restart IB Gateway
# Close IB Gateway completely and relaunch
```

### Problem: "TLS required"

**Error**: "Transport Layer Security (TLS) is required."

**Solution**:
1. Global Configuration → API → Settings
2. Find "Bypass SSL" or "Use SSL" setting
3. Adjust based on your ib_insync version
4. Restart IB Gateway

### Problem: Settings not saving

**Symptoms**: Settings revert after closing IB Gateway

**Solutions**:
1. Ensure IB Gateway has write permissions:
   ```powershell
   # Check permissions on config directory
   Get-Acl "$env:USERPROFILE\Jts"

   # Grant full control if needed (run as admin)
   $Acl = Get-Acl "$env:USERPROFILE\Jts"
   $Rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME, "FullControl", "Allow")
   $Acl.SetAccessRule($Rule)
   Set-Acl "$env:USERPROFILE\Jts" $Acl
   ```

2. Close IB Gateway properly (don't force kill)
3. Check if antivirus is blocking file writes

---

## Configuration File Reference

### Location

```powershell
$env:USERPROFILE\Jts\jts.ini
```

### Key Settings

```ini
[IBGateway]
s.SocketPort=7497
s.ApiEnabled=true
s.ReadOnlyApi=false
s.TrustedIPs=127.0.0.1
s.MasterClientId=0

[Startup]
s.AutoRestartTime=23:55:00
s.AutoLogoffTime=23:50:00
```

### View Configuration

```powershell
# View entire config
Get-Content "$env:USERPROFILE\Jts\jts.ini"

# View API-specific settings
Get-Content "$env:USERPROFILE\Jts\jts.ini" | Select-String -Pattern "api|socket|port" -CaseSensitive:$false
```

---

## Quick Reference

### Essential Settings Checklist

- [x] ✅ Enable ActiveX and Socket Clients
- [x] Socket Port: 7497 (paper) or 7496 (live)
- [x] Trusted IP: 127.0.0.1
- [x] Master Client ID: 0 (or specific ID)
- [x] Allow connections from localhost
- [x] Download open orders on connection
- [x] Allow API account requests
- [x] Auto-restart: 11:55 PM EST (optional but recommended)

### PowerShell Verification Commands

```powershell
# Check IB Gateway running
Get-Process | Where-Object {$_.ProcessName -like "*java*"}

# Check API port listening
netstat -an | findstr 7497

# View config file
Get-Content "$env:USERPROFILE\Jts\jts.ini" | Select-String "api|port"

# Test connection with Python
poetry run python -c "from ib_insync import IB; ib = IB(); ib.connect('127.0.0.1', 7497, 1); print('✅ Connected'); ib.disconnect()"
```

---

## Next Steps

After completing API configuration:

1. ✅ API enabled and configured
2. ✅ Port 7497 verified
3. ✅ Connection tested

**Next**:
- Configure Windows Firewall: [WINDOWS_FIREWALL_SETUP.md](./WINDOWS_FIREWALL_SETUP.md)
- Run IB API tests: [../RUNNING_IB_TESTS.md](../RUNNING_IB_TESTS.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
**Tested On**: Windows 11 Pro, IB Gateway 10.25+
