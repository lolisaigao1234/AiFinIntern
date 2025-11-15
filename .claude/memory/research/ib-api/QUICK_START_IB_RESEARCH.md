# Quick Start: IB API Integration Research

**Quick Reference Guide for Local Testing and Research**

---

## 🚀 Quick Setup (5 Minutes)

### 1. Download and Install IB Gateway

```powershell
# Download IB Gateway for Windows 11 Pro
# Visit: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php
# Download: ibgateway-latest-windows-x64.exe

# Run the installer
# Double-click the downloaded .exe file and follow the setup wizard
```

### 2. Configure IB Gateway

**Enable API Access**:
1. Launch IB Gateway
2. Login with paper trading credentials
3. Go to: **File → Global Configuration → API → Settings**
4. Configure:
   - ✅ Enable ActiveX and Socket Clients
   - Socket Port: **7497** (paper trading)
   - Master API Client ID: **1**
   - Trusted IP: **127.0.0.1**

### 3. Test Connection

```powershell
# Navigate to project (Windows)
cd C:\path\to\AiFinIntern

# Install dependencies
poetry install
poetry add ib-insync

# Create simple test (PowerShell)
@"
from ib_insync import IB

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
print("✅ Connected to IB Gateway!")
print(f"Account: {ib.managedAccounts()}")
ib.disconnect()
"@ | Out-File -FilePath test_quick.py -Encoding utf8

# Run test
poetry run python test_quick.py
```

**Expected Output**:
```
✅ Connected to IB Gateway!
Account: ['DU123456']
```

---

## 📋 Research Workflow

### Step 1: Choose Research Area

Pick a research topic from:
- Market Data (real-time & historical)
- Order Management (order types & execution)
- Error Handling (error codes & recovery)
- Performance (latency & throughput)

### Step 2: Run Tests

```bash
# Example: Test market data
poetry run python tests/ib_api/test_historical_data.py

# Example: Test connection
poetry run python tests/ib_api/test_connection.py
```

### Step 3: Document Findings

Create markdown file in appropriate directory:
```bash
# Example: Document market data findings
nano research/ib_api/market_data/realtime_data.md
```

### Step 4: Update Research README

```bash
# Update status
nano research/ib_api/README.md
```

---

## 📚 Key Documentation Files

| Document | Purpose | Location |
|----------|---------|----------|
| **Main Research Guide** | Comprehensive IB API research instructions | `docs/IB_API_INTEGRATION_RESEARCH.md` |
| **Research README** | Research directory overview and status | `research/ib_api/README.md` |
| **Agent Specification** | API Client Research Agent definition | `components/data_layer/agents/api_client_research_agent.md` |
| **Quick Start** | This file - quick reference | `docs/QUICK_START_IB_RESEARCH.md` |

---

## 🧪 Test Scripts Reference

### Connection Tests
```bash
# Basic connection test
poetry run python tests/ib_api/test_connection.py

# Expected: ✅ Connected successfully
```

### Market Data Tests
```bash
# Historical data test
poetry run python tests/ib_api/test_historical_data.py

# Real-time streaming test
poetry run python tests/ib_api/test_realtime_data.py
```

### Order Tests
```bash
# Order placement test (SAFE - uses limit orders far from market)
poetry run python tests/ib_api/test_order_placement.py
```

---

## 🎯 Research Checklist

### Week 1 Focus
- [ ] Set up IB Gateway/TWS
- [ ] Test basic connection
- [ ] Research market data capabilities
- [ ] Test historical data retrieval
- [ ] Document rate limits
- [ ] Measure latency

### Week 2 Focus
- [ ] Test all order types
- [ ] Research error handling
- [ ] Benchmark performance
- [ ] Design production API client

---

## 🔍 Useful Commands

### Check if IB Gateway is Running
```powershell
# Check port 7497 (Windows)
netstat -an | findstr 7497
# Expected: TCP    127.0.0.1:7497         0.0.0.0:0              LISTENING

# Or using PowerShell cmdlet:
Get-NetTCPConnection -LocalPort 7497 -ErrorAction SilentlyContinue
```

### View Research Files
```powershell
# List all research documentation (PowerShell)
Get-ChildItem -Path research\ib_api -Filter *.md -Recurse

# View research status
Get-Content research\ib_api\README.md
```

### Run All Tests
```powershell
# Run all IB API tests (PowerShell)
poetry run pytest tests/ib_api/ -v

# Run specific test category
poetry run pytest tests/ib_api/performance/ -v
```

---

## ⚠️ Safety Reminders

1. **Always Use Paper Trading** (port 7497)
2. **Never Place Real Orders** without explicit review
3. **Use Small Quantities** (1 share) for order tests
4. **Cancel Test Orders** immediately after testing
5. **Verify IB Gateway Settings** before each session

---

## 🤖 Using the API Client Research Agent

### Invoke the Agent

```markdown
# In Claude Code, use this prompt:

I need the API Client Research Agent to investigate IB API market data streaming capabilities.

Tasks:
1. Test real-time market data for AAPL, MSFT, GOOGL
2. Measure update latency
3. Identify subscription limits
4. Document findings in research/ib_api/market_data/realtime_data.md

Context scope: Market data only (8K tokens max)
Environment: Paper trading (port 7497)
```

### Agent Deliverables

The agent will produce:
- Markdown documentation with findings
- Python test scripts
- Performance benchmark data
- Recommendations for production

---

## 🆘 Troubleshooting

### Connection Failed
```
Error: Connection refused
Solution: Ensure IB Gateway is running on port 7497
Check: netstat -tuln | grep 7497
```

### API Not Enabled
```
Error: API client not enabled
Solution: Enable API in IB Gateway settings
Path: File → Global Configuration → API → Settings
```

### Wrong Credentials
```
Error: Authentication failed
Solution: Verify using paper trading credentials
Check: IB account is paper trading account
```

---

## 📞 Support Resources

- **Main Documentation**: `/docs/IB_API_INTEGRATION_RESEARCH.md`
- **IB API Docs**: https://interactivebrokers.github.io/tws-api/
- **ib_insync Docs**: https://ib-insync.readthedocs.io/
- **Project Issues**: See `research/ib_api/README.md`

---

**Created**: 2025-11-15
**Status**: Active
**Next Steps**: Set up IB Gateway and run initial tests
