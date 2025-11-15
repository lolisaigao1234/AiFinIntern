# Interactive Brokers API Integration Research Guide

**Document Version**: 1.0
**Created**: 2025-11-15
**Phase**: Phase 1 - Research & Planning
**Status**: Active Research
**Related**: [CLAUDE.md](../CLAUDE.md) | [ARCHITECTURE.md](../ARCHITECTURE.md) | [AGENTS.md](../AGENTS.md)

---

## Table of Contents
1. [Overview](#overview)
2. [Local Testing Setup](#local-testing-setup)
3. [Research Areas](#research-areas)
4. [Directory Structure](#directory-structure)
5. [Subagent Definitions](#subagent-definitions)
6. [Testing Checklist](#testing-checklist)
7. [Research Deliverables](#research-deliverables)
8. [References](#references)

---

## Overview

### Purpose
This document provides a comprehensive guide for researching and testing the Interactive Brokers (IB) API integration. It covers local machine setup, research objectives, directory organization, and subagent configuration for Claude Code.

### Current Status
**Existing IB API Code**:
- `Code/test.py` - Basic IB API connection test with historical and real-time data
- `Code/order.py` - Trading strategy implementation with Black-Scholes model and Backtrader integration

**Next Steps**:
1. Set up local IB API testing environment (TWS/IB Gateway)
2. Conduct comprehensive API research
3. Document findings and capabilities
4. Design robust API client architecture

---

## Local Testing Setup

### Prerequisites

#### 1. Interactive Brokers Account
- **Paper Trading Account** (recommended for testing)
  - Sign up at: https://www.interactivebrokers.com/en/home.php
  - Request Paper Trading access
  - Note: Paper trading replicates live trading without real money

#### 2. Software Installation

**Option A: Trader Workstation (TWS)**
```bash
# Download TWS from IB website
# https://www.interactivebrokers.com/en/trading/tws.php

# Install on Linux
chmod +x tws-latest-standalone-linux-x64.sh
./tws-latest-standalone-linux-x64.sh

# Default ports:
# Paper Trading: 7497
# Live Trading: 7496
```

**Option B: IB Gateway** (Recommended for automated trading)
```bash
# Download IB Gateway (lightweight, no GUI)
# https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

# Install on Linux
chmod +x ibgateway-latest-standalone-linux-x64.sh
./ibgateway-latest-standalone-linux-x64.sh

# Benefits:
# - Lower resource usage
# - No GUI distractions
# - Optimized for automation
# - Stable connection
```

#### 3. Enable API Access

**In TWS/IB Gateway**:
1. Navigate to: **File → Global Configuration → API → Settings**
2. Configure:
   - ✅ Enable ActiveX and Socket Clients
   - ✅ Read-Only API
   - ✅ Download open orders on connection
   - ✅ Enable API auto-restart
   - Socket Port: **7497** (paper) or **7496** (live)
   - Master API Client ID: **1** (or your preferred ID)
   - Trusted IP Addresses: **127.0.0.1** (localhost)

3. **Important Settings**:
   - Auto-restart Time: 00:00:00 - 23:59:59
   - Allow connections from localhost
   - Socket Port: 7497 (paper trading)

#### 4. Python Environment Setup

```bash
# Navigate to project directory
cd /home/user/AiFinIntern

# Install dependencies using Poetry
poetry install

# Install IB API package
poetry add ib-insync

# Or using pip
pip install ib-insync

# Verify installation
poetry run python -c "from ib_insync import *; print('IB API installed successfully')"
```

---

### Local Testing Workflow

#### Step 1: Start IB Gateway/TWS

```bash
# Start IB Gateway (paper trading)
# Use the GUI or configure for headless operation

# Verify it's running on port 7497
netstat -tuln | grep 7497

# Expected output:
# tcp        0      0 127.0.0.1:7497          0.0.0.0:*               LISTEN
```

#### Step 2: Test Basic Connection

**Create**: `tests/ib_api/test_connection.py`

```python
#!/usr/bin/env python3
"""Test IB API connection and basic functionality"""

from ib_insync import IB
import asyncio
from datetime import datetime

def test_connection():
    """Test basic IB API connection"""
    ib = IB()

    try:
        # Connect to IB Gateway (paper trading)
        ib.connect('127.0.0.1', 7497, clientId=1)
        print("✅ Connected to IB API successfully")

        # Get account information
        account_values = ib.accountValues()
        print(f"\n📊 Account Values:")
        for av in account_values[:5]:  # Print first 5
            print(f"  {av.tag}: {av.value} {av.currency}")

        # Test contract creation
        contract = Stock('AAPL', 'SMART', 'USD')
        ib.qualifyContracts(contract)
        print(f"\n✅ Contract qualified: {contract}")

        # Request current market data
        ticker = ib.reqMktData(contract)
        ib.sleep(2)  # Wait for data

        print(f"\n📈 Market Data for {contract.symbol}:")
        print(f"  Bid: {ticker.bid}")
        print(f"  Ask: {ticker.ask}")
        print(f"  Last: {ticker.last}")
        print(f"  Close: {ticker.close}")

        # Disconnect
        ib.disconnect()
        print("\n✅ Disconnected successfully")
        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
```

**Run the test**:
```bash
# Make executable
chmod +x tests/ib_api/test_connection.py

# Run test
poetry run python tests/ib_api/test_connection.py

# Expected output:
# ✅ Connected to IB API successfully
# 📊 Account Values:
#   NetLiquidation: 1000000 USD
#   ...
# ✅ Contract qualified: Stock(conId=265598, symbol='AAPL', ...)
# 📈 Market Data for AAPL:
#   Bid: 185.50
#   Ask: 185.52
# ✅ Disconnected successfully
```

#### Step 3: Test Historical Data Retrieval

**Create**: `tests/ib_api/test_historical_data.py`

```python
#!/usr/bin/env python3
"""Test historical data retrieval from IB API"""

from ib_insync import IB, Stock, util
import pandas as pd
from datetime import datetime

def test_historical_data():
    """Test retrieving historical market data"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    try:
        # Define contract
        contract = Stock('AMD', 'SMART', 'USD')
        ib.qualifyContracts(contract)

        # Request historical data
        print("📊 Requesting historical data for AMD...")
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='30 D',
            barSizeSetting='1 hour',
            whatToShow='MIDPOINT',
            useRTH=True,
            formatDate=1
        )

        # Convert to DataFrame
        df = util.df(bars)
        print(f"\n✅ Retrieved {len(df)} bars")
        print(f"\nFirst 5 bars:")
        print(df.head())

        print(f"\nData summary:")
        print(df.describe())

        # Save to CSV for analysis
        output_file = 'data/historical/amd_30d_1h.csv'
        df.to_csv(output_file)
        print(f"\n✅ Saved to {output_file}")

        ib.disconnect()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        ib.disconnect()
        return False

if __name__ == "__main__":
    success = test_historical_data()
    exit(0 if success else 1)
```

#### Step 4: Test Order Placement (Paper Trading)

**Create**: `tests/ib_api/test_order_placement.py`

```python
#!/usr/bin/env python3
"""Test order placement in paper trading"""

from ib_insync import IB, Stock, MarketOrder, LimitOrder
from datetime import datetime

def test_order_placement():
    """Test placing orders in paper trading account"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    try:
        # Define contract
        contract = Stock('AAPL', 'SMART', 'USD')
        ib.qualifyContracts(contract)

        # Get current market price
        ticker = ib.reqMktData(contract)
        ib.sleep(2)
        current_price = ticker.last or ticker.close

        print(f"📈 Current price for {contract.symbol}: ${current_price}")

        # Test 1: Market Order (CAUTION: Will execute immediately in paper trading)
        print("\n🔵 Testing Market Order (commented out for safety)...")
        # market_order = MarketOrder('BUY', 1)
        # trade = ib.placeOrder(contract, market_order)
        # print(f"Market order placed: {trade}")

        # Test 2: Limit Order (safer for testing)
        print("\n🟢 Testing Limit Order...")
        limit_price = round(current_price * 0.95, 2)  # 5% below market
        limit_order = LimitOrder('BUY', 1, limit_price)

        trade = ib.placeOrder(contract, limit_order)
        print(f"✅ Limit order placed:")
        print(f"  Order ID: {trade.order.orderId}")
        print(f"  Action: BUY")
        print(f"  Quantity: 1")
        print(f"  Limit Price: ${limit_price}")
        print(f"  Status: {trade.orderStatus.status}")

        # Wait for order to be acknowledged
        ib.sleep(2)

        # Cancel the order (cleanup)
        print("\n🔴 Cancelling order...")
        ib.cancelOrder(trade.order)
        ib.sleep(1)

        print(f"✅ Order cancelled: {trade.orderStatus.status}")

        ib.disconnect()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        ib.disconnect()
        return False

if __name__ == "__main__":
    success = test_order_placement()
    exit(0 if success else 1)
```

⚠️ **WARNING**: Be extremely careful with order placement even in paper trading. Always:
- Test with small quantities (1 share)
- Use limit orders far from market price
- Cancel test orders immediately
- Never run in live trading without thorough testing

#### Step 5: Test Real-Time Data Streaming

**Create**: `tests/ib_api/test_realtime_data.py`

```python
#!/usr/bin/env python3
"""Test real-time data streaming"""

from ib_insync import IB, Stock
import time

def test_realtime_streaming():
    """Test real-time market data streaming"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    try:
        contracts = [
            Stock('AAPL', 'SMART', 'USD'),
            Stock('MSFT', 'SMART', 'USD'),
            Stock('GOOGL', 'SMART', 'USD')
        ]

        # Qualify all contracts
        ib.qualifyContracts(*contracts)

        # Subscribe to market data
        tickers = [ib.reqMktData(contract) for contract in contracts]

        print("📡 Streaming real-time market data...")
        print("Press Ctrl+C to stop\n")

        # Stream for 30 seconds
        start_time = time.time()
        update_count = 0

        def on_ticker_update(ticker):
            nonlocal update_count
            update_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] {ticker.contract.symbol}: "
                  f"Bid={ticker.bid} Ask={ticker.ask} Last={ticker.last}")

        # Attach event handler
        for ticker in tickers:
            ticker.updateEvent += on_ticker_update

        # Run for 30 seconds
        try:
            while time.time() - start_time < 30:
                ib.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopped by user")

        print(f"\n✅ Received {update_count} updates in {time.time() - start_time:.1f} seconds")

        ib.disconnect()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        ib.disconnect()
        return False

if __name__ == "__main__":
    success = test_realtime_streaming()
    exit(0 if success else 1)
```

---

## Research Areas

### 1. API Capabilities Research

**Objective**: Understand all capabilities of the IB API for trading bot integration

#### 1.1 Market Data Research

**Directory**: `research/ib_api/market_data/`

**Research Topics**:

| Topic | Questions to Answer | Documentation Reference |
|-------|---------------------|-------------------------|
| **Real-time Data** | - What data types are available? (tick, bars, depth)<br>- Update frequency?<br>- Subscription limits? | `research/ib_api/market_data/realtime_data.md` |
| **Historical Data** | - Max duration per request?<br>- Available bar sizes?<br>- Rate limits?<br>- Data quality/gaps? | `research/ib_api/market_data/historical_data.md` |
| **Market Depth** | - Level II data availability?<br>- Order book depth?<br>- Cost/permissions? | `research/ib_api/market_data/market_depth.md` |
| **Fundamentals** | - Financial statement data?<br>- News/calendar events?<br>- Company info? | `research/ib_api/market_data/fundamentals.md` |

**Research Template**: `research/ib_api/market_data/realtime_data.md`

```markdown
# Real-Time Market Data Research

## Overview
Document findings on IB API real-time market data capabilities.

## Data Types

### 1. Tick Data
- **Fields Available**: bid, ask, last, volume, etc.
- **Update Frequency**: [Test and document]
- **Latency**: [Measure average latency]

### 2. Bar Data
- **Supported Intervals**: 1 sec, 5 sec, 15 sec, 30 sec, 1 min, 2 min, 3 min, 5 min, 15 min, 30 min, 1 hour, 1 day
- **Real-time Updates**: [Test if bars update in real-time]

## Rate Limits
- **Max Concurrent Subscriptions**: [Document limit]
- **Pacing Rules**: [Document pacing violations]
- **Workarounds**: [Document strategies to avoid limits]

## Code Examples
```python
# Working example from testing
```

## Issues Encountered
- [List any issues, bugs, or limitations]

## Recommendations
- [Best practices for production use]
```

#### 1.2 Order Management Research

**Directory**: `research/ib_api/order_management/`

**Research Topics**:

| Topic | Questions to Answer | Documentation |
|-------|---------------------|---------------|
| **Order Types** | - All supported order types?<br>- Smart routing capabilities?<br>- Time-in-force options? | `research/ib_api/order_management/order_types.md` |
| **Order Lifecycle** | - Order states and transitions?<br>- Cancellation/modification rules?<br>- Fill notifications? | `research/ib_api/order_management/order_lifecycle.md` |
| **Execution Algorithms** | - TWAP, VWAP support?<br>- Adaptive algos?<br>- Custom algo capabilities? | `research/ib_api/order_management/execution_algos.md` |

**Order Types to Test**:
- ✅ Market Order
- ✅ Limit Order
- ⬜ Stop Order
- ⬜ Stop-Limit Order
- ⬜ Trailing Stop
- ⬜ Bracket Order
- ⬜ Adaptive Order
- ⬜ TWAP
- ⬜ VWAP

**Test Script Template**:
```python
# tests/ib_api/order_types/test_limit_order.py

from ib_insync import IB, Stock, LimitOrder

def test_limit_order():
    """Test limit order placement and lifecycle"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    # Test limit order
    contract = Stock('AAPL', 'SMART', 'USD')
    order = LimitOrder('BUY', 1, 150.00)

    trade = ib.placeOrder(contract, order)

    # Document findings
    findings = {
        "order_id": trade.order.orderId,
        "initial_status": trade.orderStatus.status,
        "acknowledgement_time": "measure in ms",
        "modification_allowed": True,  # Test modification
        "cancellation_allowed": True   # Test cancellation
    }

    # Cleanup
    ib.cancelOrder(order)
    ib.disconnect()

    return findings
```

#### 1.3 Account Management Research

**Directory**: `research/ib_api/account_management/`

**Research Topics**:
- Portfolio positions retrieval
- Account values and balances
- P&L calculations (realized/unrealized)
- Margin requirements
- Position reconciliation methods

#### 1.4 Error Handling Research

**Directory**: `research/ib_api/error_handling/`

**Critical Research**:
- All error codes and meanings
- Connection failure scenarios
- Reconnection strategies
- Order rejection reasons
- Rate limit violations and recovery

**Error Testing Script**:
```python
# tests/ib_api/error_handling/test_error_scenarios.py

def test_connection_errors():
    """Test various connection error scenarios"""
    test_cases = [
        {
            "name": "Wrong port",
            "host": "127.0.0.1",
            "port": 9999,
            "expected_error": "Connection refused"
        },
        {
            "name": "Wrong client ID",
            "host": "127.0.0.1",
            "port": 7497,
            "client_id": -1,
            "expected_error": "Invalid client ID"
        },
        # Add more scenarios
    ]

    for test in test_cases:
        # Run test and document error behavior
        pass
```

---

### 2. Rate Limits and Quotas Research

**Objective**: Document all rate limits to avoid violations

**Research Areas**:

| Limit Type | Research Questions | Documentation |
|------------|-------------------|---------------|
| **Market Data** | - Messages per second?<br>- Concurrent subscriptions?<br>- Historical data requests per minute? | `research/ib_api/rate_limits/market_data_limits.md` |
| **Order Placement** | - Orders per second?<br>- Modifications per second?<br>- Daily order limits? | `research/ib_api/rate_limits/order_limits.md` |
| **Account Requests** | - Position requests per minute?<br>- Account value update frequency? | `research/ib_api/rate_limits/account_limits.md` |

**Rate Limit Testing Framework**:
```python
# tests/ib_api/rate_limits/test_rate_limits.py

import time
from ib_insync import IB, Stock

def test_market_data_rate_limit():
    """Test market data subscription rate limits"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    symbols = [f"SYM{i}" for i in range(200)]  # Try 200 subscriptions
    subscriptions = []
    errors = []

    for symbol in symbols:
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            ticker = ib.reqMktData(contract)
            subscriptions.append(ticker)
            print(f"✅ Subscribed to {symbol}")
        except Exception as e:
            errors.append({"symbol": symbol, "error": str(e)})
            print(f"❌ Failed to subscribe to {symbol}: {e}")
            break

    print(f"\nMax subscriptions before error: {len(subscriptions)}")
    print(f"Errors encountered: {len(errors)}")

    # Document findings
    findings = {
        "max_concurrent_subscriptions": len(subscriptions),
        "error_message": errors[0] if errors else None,
        "recommended_limit": len(subscriptions) * 0.8  # 80% of max
    }

    return findings
```

---

### 3. Performance and Latency Research

**Objective**: Measure performance characteristics for production planning

**Benchmarks to Establish**:

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Connection Time | < 1s | Time from connect() to successful handshake |
| Market Data Latency | < 50ms | Time from market event to API callback |
| Order Placement Latency | < 100ms | Time from placeOrder() to acknowledgement |
| Historical Data Retrieval | < 2s | Time to retrieve 30 days of 1-hour bars |

**Performance Testing Script**:
```python
# tests/ib_api/performance/test_latency.py

import time
from ib_insync import IB, Stock
import statistics

def measure_connection_latency(iterations=10):
    """Measure IB API connection latency"""
    latencies = []

    for i in range(iterations):
        ib = IB()
        start = time.time()
        ib.connect('127.0.0.1', 7497, clientId=1)
        latency = (time.time() - start) * 1000  # ms
        latencies.append(latency)
        ib.disconnect()
        time.sleep(1)

    return {
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "p95": statistics.quantiles(latencies, n=20)[18],
        "p99": statistics.quantiles(latencies, n=100)[98]
    }

def measure_market_data_latency():
    """Measure market data update latency"""
    # Requires exchange timestamp comparison
    # Document methodology
    pass
```

---

### 4. Data Quality Research

**Objective**: Assess data quality for ML model training

**Research Questions**:
- What is the percentage of missing bars in historical data?
- How frequent are data gaps during market hours?
- How accurate are MIDPOINT vs TRADES vs BID_ASK data?
- Are there any data correction/adjustment issues?

**Data Quality Test**:
```python
# research/ib_api/data_quality/test_data_completeness.py

def analyze_historical_data_quality():
    """Analyze quality of historical data from IB"""
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    contract = Stock('AAPL', 'SMART', 'USD')

    # Request 1 year of daily bars
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 Y',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True
    )

    df = util.df(bars)

    # Analyze completeness
    expected_trading_days = 252  # Approximate
    actual_bars = len(df)
    completeness = actual_bars / expected_trading_days

    # Check for gaps
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['date_diff'] = df['date'].diff().dt.days

    gaps = df[df['date_diff'] > 3]  # More than weekend

    findings = {
        "total_bars": actual_bars,
        "expected_bars": expected_trading_days,
        "completeness_pct": completeness * 100,
        "gaps_found": len(gaps),
        "gap_dates": gaps['date'].tolist()
    }

    print(f"Data Quality Report for {contract.symbol}:")
    print(f"  Completeness: {findings['completeness_pct']:.1f}%")
    print(f"  Gaps found: {findings['gaps_found']}")

    return findings
```

---

## Directory Structure

### Recommended Research Directory Layout

```
AiFinIntern/
├── components/
│   └── data_layer/
│       ├── api_client/              # Production IB API client code
│       │   ├── __init__.py
│       │   ├── connection.py        # Connection management
│       │   ├── market_data.py       # Market data retrieval
│       │   ├── historical.py        # Historical data
│       │   ├── orders.py            # Order management
│       │   ├── retry_handler.py     # Exponential backoff
│       │   └── error_handler.py     # Error handling
│       └── agents/                  # AI agents for data layer
│           └── api_client_agent.md  # Agent specification
├── research/
│   └── ib_api/                      # ⭐ IB API research directory
│       ├── README.md                # Research overview
│       ├── market_data/
│       │   ├── realtime_data.md
│       │   ├── historical_data.md
│       │   ├── market_depth.md
│       │   └── fundamentals.md
│       ├── order_management/
│       │   ├── order_types.md
│       │   ├── order_lifecycle.md
│       │   └── execution_algos.md
│       ├── account_management/
│       │   ├── positions.md
│       │   ├── balances.md
│       │   └── pnl_calculations.md
│       ├── error_handling/
│       │   ├── error_codes.md
│       │   ├── connection_failures.md
│       │   └── recovery_strategies.md
│       ├── rate_limits/
│       │   ├── market_data_limits.md
│       │   ├── order_limits.md
│       │   └── account_limits.md
│       ├── performance/
│       │   ├── latency_benchmarks.md
│       │   ├── throughput_tests.md
│       │   └── optimization_notes.md
│       └── data_quality/
│           ├── completeness_analysis.md
│           ├── accuracy_tests.md
│           └── gap_analysis.md
├── tests/
│   └── ib_api/                      # IB API test scripts
│       ├── test_connection.py
│       ├── test_historical_data.py
│       ├── test_realtime_data.py
│       ├── test_order_placement.py
│       ├── order_types/             # Test each order type
│       │   ├── test_market_order.py
│       │   ├── test_limit_order.py
│       │   ├── test_stop_order.py
│       │   └── test_bracket_order.py
│       ├── error_handling/
│       │   ├── test_connection_errors.py
│       │   ├── test_order_rejections.py
│       │   └── test_rate_limits.py
│       ├── performance/
│       │   ├── test_latency.py
│       │   ├── test_throughput.py
│       │   └── benchmark_suite.py
│       └── integration/
│           ├── test_full_workflow.py
│           └── test_error_recovery.py
├── data/
│   └── ib_api_research/             # Research data output
│       ├── historical/              # Historical data samples
│       ├── benchmarks/              # Performance benchmarks
│       └── logs/                    # Test logs
└── Code/                            # Legacy code (to be migrated)
    ├── test.py                      # Existing test script
    └── order.py                     # Existing trading script
```

---

## Subagent Definitions

### How to Define Subagents for IB API Research in Claude Code

Based on the [AGENTS.md](../AGENTS.md) architecture, we define specialized subagents for IB API integration research.

#### Agent Hierarchy for IB API Research

```
Main Orchestrator (You / Claude)
│
└─── Data Layer Agent
     │
     └─── API Client Agent (Sub-agent 1.1)
          │
          ├─── Connection Research Agent
          ├─── Market Data Research Agent
          ├─── Order Management Research Agent
          └─── Error Handling Research Agent
```

---

### Agent Specification: API Client Research Agent

**File**: `components/data_layer/agents/api_client_research_agent.md`

```markdown
# API Client Research Agent

**Agent Type**: Research & Documentation
**Parent Agent**: Data Layer Agent
**Context Limit**: 10K tokens
**Status**: Active (Phase 1 - Research)

## Responsibilities

1. **Connection Management Research**
   - Test IB Gateway/TWS connectivity
   - Document connection parameters and configurations
   - Research reconnection strategies
   - Test connection stability under various conditions

2. **Market Data Research**
   - Document all market data types and formats
   - Test real-time streaming capabilities
   - Measure historical data retrieval performance
   - Identify rate limits and quotas

3. **Order Management Research**
   - Test all order types (market, limit, stop, etc.)
   - Document order lifecycle and state transitions
   - Test order modification and cancellation
   - Research smart order routing capabilities

4. **Error Handling Research**
   - Catalog all error codes and meanings
   - Test error scenarios and recovery
   - Document retry strategies
   - Research graceful degradation patterns

## Required Context

```yaml
Priority Context (Always Include):
  - IB API documentation (ib_insync)
  - Connection parameters (host, port, client ID)
  - Test environment setup (TWS/Gateway config)
  - Error code reference

Secondary Context (Include as Needed):
  - Historical test results
  - Performance benchmarks
  - Rate limit findings
  - Data quality analysis

Max Context Size: 10K tokens
```

## Decision Boundaries

### Can Do (Autonomous):
- Run test scripts against paper trading account
- Document API capabilities and limitations
- Create code examples and snippets
- Measure performance and latency
- Identify and document errors
- Suggest retry strategies and optimizations

### Cannot Do (Requires Approval):
- Connect to live trading account
- Place real orders (even in paper trading without review)
- Modify production code
- Change API credentials or configurations
- Make architectural decisions affecting other components

## Communication Interfaces

### Input Messages:
- `RESEARCH_REQUEST`: Request to research specific API capability
  ```python
  {
    "action": "research",
    "topic": "market_data_rate_limits",
    "priority": "high",
    "deadline": "2025-11-18"
  }
  ```

### Output Messages:
- `RESEARCH_FINDINGS`: Report research findings
  ```python
  {
    "topic": "market_data_rate_limits",
    "findings": {
      "max_concurrent_subscriptions": 100,
      "recommended_limit": 80,
      "error_behavior": "..."
    },
    "documentation": "research/ib_api/rate_limits/market_data_limits.md"
  }
  ```

## Key Files to Monitor

```yaml
Research Documentation:
  - research/ib_api/market_data/*.md
  - research/ib_api/order_management/*.md
  - research/ib_api/error_handling/*.md

Test Scripts:
  - tests/ib_api/test_*.py
  - tests/ib_api/*/test_*.py

Legacy Code (for migration reference):
  - Code/test.py
  - Code/order.py

Output:
  - data/ib_api_research/
  - logs/ib_api_tests/
```

## Success Criteria

### Research Phase Complete When:
- ✅ All market data capabilities documented
- ✅ All order types tested and documented
- ✅ Rate limits identified and documented
- ✅ Error handling strategies defined
- ✅ Performance benchmarks established
- ✅ Data quality analysis completed
- ✅ Production-ready API client design finalized

## Tools and Resources

- **IB API Library**: `ib-insync`
- **Testing Framework**: `pytest`
- **Documentation**: Markdown files in `research/ib_api/`
- **Data Storage**: CSV/Parquet files in `data/ib_api_research/`
- **Logging**: structlog for structured logging

## Escalation Criteria

Escalate to Data Layer Agent when:
- Architectural decisions needed (e.g., caching strategy)
- Integration with other components required
- Production deployment planning
- Resource allocation decisions
```

---

### How to Use This Agent in Claude Code

#### 1. Agent Invocation Pattern

When working on IB API research tasks, invoke the agent with specific research requests:

```markdown
# Example prompt to Claude Code:

I need the API Client Research Agent to investigate IB API market data capabilities. Specifically:

1. Test real-time market data streaming for AAPL, MSFT, GOOGL
2. Measure latency from market event to callback
3. Identify max concurrent subscriptions before rate limit
4. Document findings in research/ib_api/market_data/realtime_data.md

Context scope:
- Focus only on real-time market data (not historical)
- Use paper trading account (port 7497)
- Maximum 8K token context

Expected deliverables:
- Markdown documentation with findings
- Python test script demonstrating capabilities
- Performance benchmark data
```

#### 2. Context Management

The agent maintains focused context by:
- **Loading only relevant files** (not entire codebase)
- **Prioritizing current research topic** (e.g., only market data files)
- **Pruning old context** (removing completed research from memory)
- **Documenting findings immediately** (offload to markdown files)

#### 3. Parallel Research Execution

Multiple research tasks can run in parallel by invoking multiple agent instances:

```markdown
# Parallel research request:

Launch 3 API Client Research Agents in parallel:

Agent 1: Research market data capabilities
- Files: research/ib_api/market_data/
- Tests: tests/ib_api/test_realtime_data.py

Agent 2: Research order management
- Files: research/ib_api/order_management/
- Tests: tests/ib_api/order_types/

Agent 3: Research error handling
- Files: research/ib_api/error_handling/
- Tests: tests/ib_api/error_handling/

Each agent reports findings independently.
```

---

## Testing Checklist

### Phase 1: Basic Connectivity (Week 1)

- [ ] **Environment Setup**
  - [ ] Install IB Gateway/TWS
  - [ ] Configure paper trading account
  - [ ] Enable API access (port 7497)
  - [ ] Install ib-insync package
  - [ ] Create test directory structure

- [ ] **Connection Tests**
  - [ ] Test basic connection to IB Gateway
  - [ ] Test connection failure scenarios
  - [ ] Test reconnection logic
  - [ ] Test multiple concurrent connections
  - [ ] Measure connection latency

- [ ] **Account Information**
  - [ ] Retrieve account values
  - [ ] Retrieve portfolio positions
  - [ ] Retrieve order history
  - [ ] Test position reconciliation

### Phase 2: Market Data Research (Week 1)

- [ ] **Real-Time Data**
  - [ ] Test real-time tick data streaming
  - [ ] Test real-time bar updates
  - [ ] Test multiple symbol subscriptions
  - [ ] Identify subscription limits
  - [ ] Measure market data latency

- [ ] **Historical Data**
  - [ ] Test various bar sizes (1min, 5min, 1hour, 1day)
  - [ ] Test different durations (1D, 1W, 1M, 1Y)
  - [ ] Test different data types (TRADES, MIDPOINT, BID_ASK)
  - [ ] Identify rate limits for historical requests
  - [ ] Analyze data completeness and quality

- [ ] **Market Depth**
  - [ ] Test Level II data (if available)
  - [ ] Test order book depth
  - [ ] Document costs and requirements

### Phase 3: Order Management Research (Week 2)

- [ ] **Order Types**
  - [ ] Market orders
  - [ ] Limit orders
  - [ ] Stop orders
  - [ ] Stop-limit orders
  - [ ] Trailing stop orders
  - [ ] Bracket orders
  - [ ] Adaptive orders

- [ ] **Order Lifecycle**
  - [ ] Test order submission
  - [ ] Test order acknowledgement
  - [ ] Test order fills (partial and complete)
  - [ ] Test order modifications
  - [ ] Test order cancellations
  - [ ] Test order rejections

- [ ] **Execution Algorithms**
  - [ ] Test TWAP execution
  - [ ] Test VWAP execution
  - [ ] Test adaptive algorithms
  - [ ] Document configuration options

### Phase 4: Error Handling & Edge Cases (Week 2)

- [ ] **Connection Errors**
  - [ ] Wrong port
  - [ ] Wrong credentials
  - [ ] Network interruption
  - [ ] Gateway restart during connection

- [ ] **Order Errors**
  - [ ] Invalid contract
  - [ ] Insufficient funds
  - [ ] Outside market hours
  - [ ] Invalid order parameters

- [ ] **Rate Limiting**
  - [ ] Market data pacing violations
  - [ ] Historical data request limits
  - [ ] Order rate limits
  - [ ] Recovery strategies

### Phase 5: Performance & Optimization (Week 2)

- [ ] **Latency Benchmarks**
  - [ ] Connection latency (p50, p95, p99)
  - [ ] Market data latency
  - [ ] Order placement latency
  - [ ] Historical data retrieval time

- [ ] **Throughput Tests**
  - [ ] Max market data updates per second
  - [ ] Max orders per second
  - [ ] Max historical data requests per minute

- [ ] **Optimization**
  - [ ] Caching strategies
  - [ ] Connection pooling
  - [ ] Batch request optimization
  - [ ] Async/await patterns

---

## Research Deliverables

### Week 1 Deliverables

1. **Connection Research Report**
   - File: `research/ib_api/connection_research_report.md`
   - Contents: Connection parameters, retry strategies, stability findings

2. **Market Data Capabilities Report**
   - File: `research/ib_api/market_data_capabilities.md`
   - Contents: Data types, rate limits, latency benchmarks, quality analysis

3. **Test Scripts Collection**
   - Files: `tests/ib_api/test_*.py`
   - Contents: All working test scripts with documentation

### Week 2 Deliverables

4. **Order Management Research Report**
   - File: `research/ib_api/order_management_research.md`
   - Contents: Order types, lifecycle, execution algos, limitations

5. **Error Handling Playbook**
   - File: `research/ib_api/error_handling_playbook.md`
   - Contents: All error codes, recovery strategies, retry logic

6. **Performance Benchmark Report**
   - File: `research/ib_api/performance_benchmarks.md`
   - Contents: Latency metrics, throughput limits, optimization recommendations

7. **Production-Ready API Client Design**
   - File: `components/data_layer/api_client/DESIGN.md`
   - Contents: Architecture design for production IB API client

### Final Deliverable: IB API Integration Summary

**File**: `research/ib_api/IB_API_INTEGRATION_SUMMARY.md`

**Contents**:
- Executive summary of research findings
- Go/no-go recommendation for IB API
- Identified risks and mitigation strategies
- Production implementation roadmap
- Resource requirements
- Timeline estimates

---

## References

### Official Documentation
- **IB API Documentation**: https://interactivebrokers.github.io/tws-api/
- **ib_insync Documentation**: https://ib-insync.readthedocs.io/
- **IB Trader Workstation**: https://www.interactivebrokers.com/en/trading/tws.php

### Research Resources
- **IB API Error Codes**: https://interactivebrokers.github.io/tws-api/message_codes.html
- **Rate Limiting**: https://interactivebrokers.github.io/tws-api/pacing_violations.html
- **Market Data Types**: https://interactivebrokers.github.io/tws-api/market_data_type.html

### Community Resources
- **ib_insync GitHub**: https://github.com/erdewit/ib_insync
- **IB API Forum**: https://groups.io/g/insync

---

## Next Steps

### Immediate Actions (Next 48 Hours)

1. **Set up IB Gateway/TWS**
   - Install software
   - Configure paper trading account
   - Enable API access

2. **Run Initial Tests**
   - Execute `tests/ib_api/test_connection.py`
   - Execute `tests/ib_api/test_historical_data.py`
   - Document initial findings

3. **Create Research Directory Structure**
   ```bash
   mkdir -p research/ib_api/{market_data,order_management,account_management,error_handling,rate_limits,performance,data_quality}
   mkdir -p tests/ib_api/{order_types,error_handling,performance,integration}
   mkdir -p data/ib_api_research/{historical,benchmarks,logs}
   ```

4. **Begin Market Data Research**
   - Focus on real-time data streaming
   - Document rate limits
   - Measure latency

### Week 1 Focus Areas

- Connection stability and retry logic
- Market data capabilities and limitations
- Historical data quality analysis
- Rate limit identification

### Week 2 Focus Areas

- Order management comprehensive testing
- Error handling and recovery strategies
- Performance optimization
- Production API client design

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Next Review**: 2025-11-18
**Status**: Active Research - Phase 1
