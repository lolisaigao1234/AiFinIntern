# Windows Firewall Setup for IB Gateway - Windows 11 Pro

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Platform**: Windows 11 Pro
**Purpose**: Configure Windows Defender Firewall for IB Gateway/TWS API connectivity

---

## Table of Contents
1. [Overview](#overview)
2. [Required Ports](#required-ports)
3. [Automated Setup (Recommended)](#automated-setup-recommended)
4. [Manual Setup (Step-by-Step)](#manual-setup-step-by-step)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

---

## Overview

Windows Defender Firewall may block IB Gateway from establishing connections. This guide configures firewall rules to allow IB Gateway while maintaining security.

### Why Firewall Configuration is Needed

IB Gateway requires:
1. **Outbound access** to IB servers (ports 4000, 4001)
2. **Inbound access** for API connections (ports 7496, 7497)
3. **Java process** allowance (IB Gateway uses Java)

---

## Required Ports

| Port | Direction | Purpose | Required |
|------|-----------|---------|----------|
| **7497** | Inbound (localhost) | Paper Trading API | ✅ Yes |
| **7496** | Inbound (localhost) | Live Trading API | ⚠️ Production only |
| **4000** | Outbound | IB Server Connection | ✅ Yes |
| **4001** | Outbound | IB Server Connection | ✅ Yes |

---

## Automated Setup (Recommended)

### Quick Setup Script

**Run PowerShell as Administrator**:

```powershell
# Run PowerShell as Admin
Start-Process powershell -Verb RunAs

# In the Administrator PowerShell window:
```

```powershell
# ===================================
# IB Gateway Firewall Configuration
# Windows 11 Pro
# ===================================

Write-Host "Configuring Windows Firewall for IB Gateway..." -ForegroundColor Cyan

# Get IB Gateway version (adjust path if needed)
$IBPath = "C:\Jts\ibgateway"
$LatestVersion = Get-ChildItem $IBPath | Sort-Object Name -Descending | Select-Object -First 1 -ExpandProperty Name
$IBGatewayExe = "C:\Jts\ibgateway\$LatestVersion\ibgateway.exe"

Write-Host "IB Gateway path: $IBGatewayExe" -ForegroundColor Yellow

# ===================================
# 1. Allow IB Gateway Executable
# ===================================

Write-Host "`n1. Adding IB Gateway executable rules..." -ForegroundColor Green

# Inbound rule
New-NetFirewallRule -DisplayName "IB Gateway - Inbound" `
    -Description "Allow IB Gateway inbound connections" `
    -Direction Inbound `
    -Program $IBGatewayExe `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

# Outbound rule
New-NetFirewallRule -DisplayName "IB Gateway - Outbound" `
    -Description "Allow IB Gateway outbound connections to IB servers" `
    -Direction Outbound `
    -Program $IBGatewayExe `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

Write-Host "✅ IB Gateway executable rules added" -ForegroundColor Green

# ===================================
# 2. Allow Java (if needed)
# ===================================

Write-Host "`n2. Adding Java runtime rules..." -ForegroundColor Green

# Find Java executable used by IB Gateway
$JavaPath = "C:\Jts\ibgateway\$LatestVersion\jre\bin\javaw.exe"

if (Test-Path $JavaPath) {
    New-NetFirewallRule -DisplayName "IB Gateway Java - Inbound" `
        -Description "Allow IB Gateway Java runtime inbound" `
        -Direction Inbound `
        -Program $JavaPath `
        -Action Allow `
        -Profile Any `
        -Enabled True `
        -ErrorAction SilentlyContinue

    New-NetFirewallRule -DisplayName "IB Gateway Java - Outbound" `
        -Description "Allow IB Gateway Java runtime outbound" `
        -Direction Outbound `
        -Program $JavaPath `
        -Action Allow `
        -Profile Any `
        -Enabled True `
        -ErrorAction SilentlyContinue

    Write-Host "✅ Java runtime rules added" -ForegroundColor Green
} else {
    Write-Host "⚠️ Java path not found, skipping" -ForegroundColor Yellow
}

# ===================================
# 3. Allow IB Server Ports (4000, 4001)
# ===================================

Write-Host "`n3. Adding IB server port rules..." -ForegroundColor Green

# Port 4000 - Outbound to IB servers
New-NetFirewallRule -DisplayName "IB Servers - Port 4000" `
    -Description "Allow outbound connections to IB servers on port 4000" `
    -Direction Outbound `
    -LocalPort Any `
    -RemotePort 4000 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

# Port 4001 - Outbound to IB servers
New-NetFirewallRule -DisplayName "IB Servers - Port 4001" `
    -Description "Allow outbound connections to IB servers on port 4001" `
    -Direction Outbound `
    -LocalPort Any `
    -RemotePort 4001 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

Write-Host "✅ IB server port rules added" -ForegroundColor Green

# ===================================
# 4. Allow API Ports (7496, 7497) - Localhost Only
# ===================================

Write-Host "`n4. Adding API port rules (localhost only)..." -ForegroundColor Green

# Port 7497 - Paper Trading API (localhost only)
New-NetFirewallRule -DisplayName "IB API - Port 7497 (Paper Trading)" `
    -Description "Allow API connections on port 7497 (Paper Trading) - Localhost only" `
    -Direction Inbound `
    -LocalPort 7497 `
    -RemoteAddress 127.0.0.1 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

# Port 7496 - Live Trading API (localhost only)
New-NetFirewallRule -DisplayName "IB API - Port 7496 (Live Trading)" `
    -Description "Allow API connections on port 7496 (Live Trading) - Localhost only" `
    -Direction Inbound `
    -LocalPort 7496 `
    -RemoteAddress 127.0.0.1 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Enabled True `
    -ErrorAction SilentlyContinue

Write-Host "✅ API port rules added (localhost only)" -ForegroundColor Green

# ===================================
# 5. Verification
# ===================================

Write-Host "`n5. Verifying firewall rules..." -ForegroundColor Cyan

$Rules = Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"}
Write-Host "`nCreated firewall rules:" -ForegroundColor Yellow
$Rules | Format-Table DisplayName, Enabled, Direction, Action -AutoSize

Write-Host "`n✅ Firewall configuration complete!" -ForegroundColor Green
Write-Host "Total rules created: $($Rules.Count)" -ForegroundColor Cyan
```

**Save Script**:
```powershell
# Save the above script
$Script | Out-File -FilePath "C:\Temp\ib_firewall_setup.ps1" -Encoding UTF8

# Run it
Set-ExecutionPolicy Bypass -Scope Process -Force
C:\Temp\ib_firewall_setup.ps1
```

---

## Manual Setup (Step-by-Step)

### Prerequisites

Open PowerShell as Administrator:
```powershell
Start-Process powershell -Verb RunAs
```

### Step 1: Allow IB Gateway Executable

```powershell
# Replace <version> with your IB Gateway version (e.g., 10.25)
$IBGatewayExe = "C:\Jts\ibgateway\<version>\ibgateway.exe"

# Inbound rule
New-NetFirewallRule -DisplayName "IB Gateway - Inbound" `
    -Direction Inbound `
    -Program $IBGatewayExe `
    -Action Allow `
    -Profile Any

# Outbound rule
New-NetFirewallRule -DisplayName "IB Gateway - Outbound" `
    -Direction Outbound `
    -Program $IBGatewayExe `
    -Action Allow `
    -Profile Any
```

### Step 2: Allow IB Server Ports

```powershell
# Port 4000
New-NetFirewallRule -DisplayName "IB Servers - Port 4000" `
    -Direction Outbound `
    -RemotePort 4000 `
    -Protocol TCP `
    -Action Allow

# Port 4001
New-NetFirewallRule -DisplayName "IB Servers - Port 4001" `
    -Direction Outbound `
    -RemotePort 4001 `
    -Protocol TCP `
    -Action Allow
```

### Step 3: Allow API Ports (Localhost Only)

```powershell
# Paper Trading API - Port 7497
New-NetFirewallRule -DisplayName "IB API - Port 7497 (Paper)" `
    -Direction Inbound `
    -LocalPort 7497 `
    -RemoteAddress 127.0.0.1 `
    -Protocol TCP `
    -Action Allow

# Live Trading API - Port 7496
New-NetFirewallRule -DisplayName "IB API - Port 7496 (Live)" `
    -Direction Inbound `
    -LocalPort 7496 `
    -RemoteAddress 127.0.0.1 `
    -Protocol TCP `
    -Action Allow
```

---

## Verification

### Check Firewall Rules

```powershell
# List all IB-related firewall rules
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} | Format-Table DisplayName, Enabled, Direction, Action

# Expected output: 6+ rules (IB Gateway, Java, Ports)
```

### Test IB Gateway Connection

```powershell
# 1. Start IB Gateway
& "C:\Jts\ibgateway\<version>\ibgateway.exe"

# 2. Wait for login, then check listening port
netstat -an | findstr 7497

# Expected: TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING
```

### Test API Connection

```powershell
# Create test script
@"
from ib_insync import IB

ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)
    print('✅ Firewall configuration successful - API connected!')
    print(f'Server time: {ib.reqCurrentTime()}')
    ib.disconnect()
except Exception as e:
    print(f'❌ Connection failed: {e}')
    print('Check firewall rules and IB Gateway API settings')
"@ | Out-File -FilePath test_firewall.py -Encoding utf8

# Run test
poetry run python test_firewall.py
```

**Expected Output**:
```
✅ Firewall configuration successful - API connected!
Server time: 2025-11-15 20:30:45
```

---

## Troubleshooting

### Problem: Connection still blocked

**Check if firewall is active**:
```powershell
Get-NetFirewallProfile | Format-Table Name, Enabled
```

**Temporarily disable firewall (for testing only!)**:
```powershell
# Disable (run as admin)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Test connection now...

# Re-enable immediately after testing
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**DO NOT** leave firewall disabled!

### Problem: Rules not working

**Delete and recreate rules**:
```powershell
# Remove all IB rules
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} | Remove-NetFirewallRule

# Re-run automated setup script
```

### Problem: Third-party antivirus blocking

**Check for third-party firewall**:
- Norton, McAfee, Kaspersky, etc. may have additional firewalls
- Add IB Gateway to their exceptions manually
- Consult antivirus documentation

---

## Security Considerations

### Best Practices

1. **Localhost Only for API Ports**:
   ```powershell
   # Always restrict API ports to 127.0.0.1
   -RemoteAddress 127.0.0.1
   ```
   - Prevents remote connections
   - Reduces attack surface

2. **Specific Program Rules**:
   ```powershell
   # Better than open port rules
   -Program "C:\Jts\ibgateway\<version>\ibgateway.exe"
   ```
   - Only IB Gateway can use these ports
   - More secure than allowing any program

3. **Disable Unused Rules**:
   ```powershell
   # Disable live trading API if not needed
   Get-NetFirewallRule -DisplayName "IB API - Port 7496*" | Disable-NetFirewallRule
   ```

### Security Warnings

⚠️ **Never** allow remote connections to API ports (7496/7497)
⚠️ **Never** expose ports to public internet
⚠️ **Always** use localhost (127.0.0.1) for API connections
⚠️ **Regularly** review firewall rules for unauthorized changes

### Audit Firewall Rules

```powershell
# Review all IB-related rules quarterly
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} |
    Select-Object DisplayName, Enabled, Direction, Action, RemoteAddress |
    Format-Table -AutoSize

# Export to file for audit trail
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} |
    Export-Csv -Path "C:\Temp\ib_firewall_audit_$(Get-Date -Format 'yyyyMMdd').csv" -NoTypeInformation
```

---

## Cleanup / Removal

### Remove All IB Firewall Rules

```powershell
# Run as Administrator

# List rules to be removed
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} | Format-Table DisplayName

# Remove rules (confirm before running!)
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"} | Remove-NetFirewallRule

# Verify removal
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"}
# Expected: No output
```

---

## Quick Reference

### Essential PowerShell Commands

```powershell
# List IB rules
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "IB*"}

# Check port 7497
netstat -an | findstr 7497

# Test connection
Get-NetTCPConnection -LocalPort 7497

# Disable/Enable rule
Disable-NetFirewallRule -DisplayName "IB API - Port 7496*"
Enable-NetFirewallRule -DisplayName "IB API - Port 7497*"

# View rule details
Get-NetFirewallRule -DisplayName "IB Gateway - Inbound" | Get-NetFirewallPortFilter
```

---

## Next Steps

After firewall configuration:

1. ✅ Firewall rules created
2. ✅ Ports 7497, 4000, 4001 allowed
3. ✅ IB Gateway executable allowed

**Next**:
- Test connection: [../RUNNING_IB_TESTS.md](../RUNNING_IB_TESTS.md)
- Configure IB API: [IB_API_CONFIGURATION_WINDOWS.md](./IB_API_CONFIGURATION_WINDOWS.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Production Ready
**Tested On**: Windows 11 Pro (Build 22000+)
