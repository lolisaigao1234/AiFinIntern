# Interactive Brokers API Tests

**Purpose**: Comprehensive test suite for IB API integration
**Status**: Setup Complete
**Last Updated**: 2025-11-15

---

## Overview

This directory contains all tests for Interactive Brokers API integration. Tests are organized by functionality to ensure comprehensive coverage of all API capabilities.

## Directory Structure

```
tests/ib_api/
├── basic/              - Basic connection and authentication tests
├── account/            - Account information and portfolio tests
├── market_data/        - Market data streaming and historical data tests
├── contracts/          - Contract definition and qualification tests
├── order_management/   - Order placement and management tests
├── execution/          - Execution algorithm tests (TWAP, VWAP, etc.)
├── error_handling/     - Error scenarios and recovery tests
├── integration/        - End-to-end integration tests
├── helpers/            - Helper functions and utilities
├── fixtures/           - Test data and mock objects
├── config/             - Test configuration files
└── results/            - Test execution results and reports
```

## Test Categories

### 1. Basic Tests (`basic/`)
- Connection tests
- Authentication tests
- Connection retry logic
- Multiple client connections
- Connection timeouts

### 2. Account Tests (`account/`)
- Account summary retrieval
- Account values
- Portfolio positions
- P&L tracking (realized and unrealized)

### 3. Market Data Tests (`market_data/`)
- Real-time quote streaming
- Historical data retrieval
- Market depth (Level II)
- Tick-by-tick data
- Real-time bars

### 4. Contract Tests (`contracts/`)
- Stock contracts
- Option contracts
- Futures contracts
- Forex contracts
- Contract search and qualification

### 5. Order Management Tests (`order_management/`)
- Market orders
- Limit orders
- Stop orders
- Stop-limit orders
- Bracket orders
- Order modifications
- Order cancellations
- Order status tracking

### 6. Execution Algorithm Tests (`execution/`)
- TWAP (Time-Weighted Average Price)
- VWAP (Volume-Weighted Average Price)
- Adaptive algorithms

### 7. Error Handling Tests (`error_handling/`)
- Connection errors
- Order rejections
- Rate limiting
- Error code catalog

### 8. Integration Tests (`integration/`)
- End-to-end trading workflows
- Position reconciliation
- P&L calculation

## Running Tests

### Run All Tests
```powershell
poetry run pytest tests/ib_api/ -v
```

### Run Specific Category
```powershell
# Basic tests
poetry run pytest tests/ib_api/basic/ -v

# Market data tests
poetry run pytest tests/ib_api/market_data/ -v

# Order management tests
poetry run pytest tests/ib_api/order_management/ -v
```

### Run Single Test File
```powershell
poetry run pytest tests/ib_api/basic/test_01_connection.py -v
```

### Generate Coverage Report
```powershell
poetry run pytest tests/ib_api/ --cov=tests/ib_api --cov-report=html
```

## Test Configuration

### Prerequisites
1. **IB Gateway or TWS** must be running
2. **Paper trading account** configured
3. **API enabled** on port 7497
4. **Localhost** (127.0.0.1) in trusted IPs

### Configuration Files
- `config/test_config.py` - Centralized test configuration
- `config/logging_config.py` - Logging configuration
- `pytest.ini` - pytest configuration

### Environment Variables
```powershell
# Set IB connection parameters (optional)
$env:IB_HOST = "127.0.0.1"
$env:IB_PORT = "7497"
$env:IB_CLIENT_ID = "1"
```

## Safety Guidelines

**IMPORTANT**: All order tests use paper trading only!

1. **Always use paper trading** (port 7497, NOT 7496)
2. **Auto-cancel all test orders** immediately after execution
3. **Use limit orders far from market** (50%+ away) for safety
4. **Test with quantity of 1** for all order tests
5. **Never run tests with real money**

## Test Fixtures

Common test fixtures are located in `fixtures/`:
- `test_data.py` - Sample market data, quotes, bars
- Mock IB API responses
- Sample contract definitions
- Sample order objects

## Helper Functions

Common helper functions in `helpers/`:
- `ib_wrapper.py` - Simplified IB API wrapper
- `contracts.py` - Contract creation helpers
- `orders.py` - Order creation helpers

## Test Data Output

Test results and data are stored in `results/`:
- Test execution reports
- Historical data samples
- Performance benchmarks
- Error logs

## Contributing

When adding new tests:
1. Follow the naming convention: `test_##_description.py`
2. Include docstrings for all test functions
3. Use appropriate fixtures for setup/teardown
4. Add safety checks for order tests
5. Update this README with new test categories

## Troubleshooting

### Connection Failed
```
Error: Connection refused
Solution: Ensure IB Gateway is running on port 7497
```

### API Not Enabled
```
Error: API client not enabled
Solution: Enable API in IB Gateway settings
```

### Rate Limiting
```
Error: Pacing violation
Solution: Reduce request frequency, add delays between calls
```

## Reference Documentation

- **Main TODO Tracker**: `/docs/IB_API_TESTING_SETUP_TODOS.md`
- **IB API Integration Research**: `/docs/IB_API_INTEGRATION_RESEARCH.md`
- **Quick Start Guide**: `/docs/QUICK_START_IB_RESEARCH.md`
- **IB API Docs**: https://interactivebrokers.github.io/tws-api/
- **ib_insync Docs**: https://ib-insync.readthedocs.io/

---

**Version**: 1.0
**Status**: Ready for test implementation
**Next Steps**: Begin implementing test files per TODO tracker
