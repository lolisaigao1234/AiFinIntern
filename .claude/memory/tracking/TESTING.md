# Testing & Validation Strategy

**Project**: AI-Driven Tax and Portfolio Reconciliation System
**Last Updated**: 2025-11-15
**Documentation Home**: [CLAUDE.md](../../../CLAUDE.md)
**Location**: `.claude/memory/tracking/TESTING.md`

---

## Overview

This document defines the comprehensive testing and validation strategy for the AI trading bot. The strategy follows the testing pyramid approach with unit tests at the base, integration tests in the middle, and manual/paper trading tests at the top.

**Related Documentation**:
- [CLAUDE.md](../../../CLAUDE.md) - Main project overview and index
- [ROADMAP.md](../planning/ROADMAP.md) - Project phases and milestones
- [DECISIONS.md](../planning/DECISIONS.md) - Decision log
- [RISKS.md](../planning/RISKS.md) - Risk register

---

## Testing Pyramid

```
                    ┌─────────────┐
                    │   Manual    │
                    │   Testing   │
                    │ Paper Trade │
                    └─────────────┘
                ┌─────────────────────┐
                │  Integration Tests  │
                │  (End-to-end flows) │
                └─────────────────────┘
        ┌───────────────────────────────────┐
        │          Unit Tests               │
        │  (Individual functions/classes)   │
        └───────────────────────────────────┘
```

**Philosophy**:
- Most tests should be unit tests (fast, isolated, specific)
- Integration tests validate component interactions
- Manual/paper trading validates real-world behavior

---

## Unit Testing

### Overview
Unit tests validate individual functions, classes, and modules in isolation using mocks and fixtures.

**Directory**: `tests/unit/`

### Requirements

#### Coverage Target
- **Minimum**: 80% code coverage
- **Target**: 85%+ code coverage
- **Critical Components**: 95%+ coverage (tax calculations, order execution)

#### Tools & Frameworks
- **Test Runner**: pytest
- **Mocking**: unittest.mock, pytest-mock
- **Coverage**: pytest-cov
- **Fixtures**: pytest fixtures
- **Async Testing**: pytest-asyncio

#### Run Frequency
- On every commit (pre-commit hook)
- Before pull request merge
- Nightly full test suite

### Coverage Areas

#### 1. Data Layer (`tests/unit/data_layer/`)
**Files to Test**:
- `test_ib_api_client.py` - IB API connection wrapper
- `test_data_retriever.py` - Market data fetching logic
- `test_data_preprocessor.py` - Data cleaning and normalization
- `test_database_manager.py` - Database operations

**Test Cases**:
- API connection success/failure handling
- Data retrieval with various parameters
- Data preprocessing edge cases
- Database CRUD operations
- Error handling and retries

---

#### 2. Strategy Layer (`tests/unit/strategy_layer/`)
**Files to Test**:
- `test_ml_model_manager.py` - Model fine-tuning and inference
- `test_signal_generator.py` - Trading signal creation
- `test_backtester.py` - Strategy validation
- `test_performance_evaluator.py` - Metrics calculation

**Test Cases**:
- Model loading and inference
- Signal generation logic
- Backtesting calculations
- Performance metric accuracy
- Edge cases (missing data, extreme values)

---

#### 3. Execution Layer (`tests/unit/execution_layer/`)
**Files to Test**:
- `test_order_manager.py` - Order lifecycle management
- `test_position_tracker.py` - Position monitoring
- `test_risk_manager.py` - Risk controls
- `test_execution_engine.py` - Trade execution

**Test Cases**:
- Order creation and validation
- Position tracking accuracy
- Risk limit enforcement
- Order execution logic
- Error handling (rejections, timeouts)

---

#### 4. Tax & Reconciliation (`tests/unit/tax_recon/`)
**Files to Test**:
- `test_wash_sale_detector.py` - Wash sale detection
- `test_capital_gains_calculator.py` - Gain/loss computation
- `test_tax_lot_tracker.py` - Tax lot management
- `test_reconciliation_engine.py` - Broker reconciliation

**Test Cases**:
- Wash sale detection (30-day rule)
- Capital gains calculations (short-term, long-term)
- Tax lot tracking (FIFO, LIFO, specific ID)
- Reconciliation accuracy
- Edge cases (splits, dividends, corporate actions)

---

#### 5. Reporting (`tests/unit/reporting/`)
**Files to Test**:
- `test_pl_calculator.py` - P&L computation
- `test_tax_reporter.py` - Tax reports
- `test_portfolio_analytics.py` - Performance metrics
- `test_alert_manager.py` - Notifications

**Test Cases**:
- P&L calculation accuracy
- Tax report generation
- Performance metric calculations (Sharpe, Drawdown)
- Alert triggering logic

---

### Test Case Requirements

For each test, ensure:
- **Happy path scenarios** - Normal, expected behavior
- **Edge cases** - Boundary values, empty inputs, null values
- **Error conditions** - Invalid inputs, API failures, database errors
- **Boundary values** - Min/max values, limits

### Example Unit Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from components.data_layer.src.ib_api_client import IBAPIClient

class TestIBAPIClient:
    @pytest.fixture
    def api_client(self):
        """Fixture for IBAPIClient instance"""
        return IBAPIClient(host="127.0.0.1", port=7497, client_id=1)

    def test_connect_success(self, api_client):
        """Test successful connection to IB API"""
        with patch.object(api_client, 'connect') as mock_connect:
            mock_connect.return_value = True
            result = api_client.connect()
            assert result is True
            mock_connect.assert_called_once()

    def test_connect_failure(self, api_client):
        """Test connection failure handling"""
        with patch.object(api_client, 'connect') as mock_connect:
            mock_connect.side_effect = ConnectionError("Connection refused")
            with pytest.raises(ConnectionError):
                api_client.connect()

    def test_get_market_data_valid_symbol(self, api_client):
        """Test market data retrieval for valid symbol"""
        # Test implementation
        pass

    def test_get_market_data_invalid_symbol(self, api_client):
        """Test market data retrieval for invalid symbol"""
        # Test implementation
        pass
```

---

## Integration Testing

### Overview
Integration tests validate interactions between components and end-to-end workflows.

**Directory**: `tests/integration/`

### Requirements

#### Environment
- **Test Environment**: Staging with IB paper trading account
- **Database**: Separate test database (PostgreSQL)
- **External Services**: Mock or sandboxed versions

#### Tools & Frameworks
- **Test Runner**: pytest
- **Test Data**: pytest fixtures, factory_boy
- **API Mocking**: responses, vcrpy (for recording/replaying API calls)

#### Run Frequency
- Daily (automated)
- Before major releases
- After significant component changes

### Test Scenarios

#### 1. End-to-End Trade Flow (`test_e2e_trade_flow.py`)
**Scenario**: Complete trade lifecycle from signal generation to execution to tax reporting

**Steps**:
1. Generate trading signal from strategy layer
2. Pass signal to execution layer
3. Place order via IB API (paper trading)
4. Track order status until filled
5. Update position tracker
6. Calculate tax implications
7. Generate P&L report

**Validation**:
- Signal correctly triggers order
- Order successfully placed and filled
- Position accurately tracked
- Tax calculations correct
- Reports generated without errors

---

#### 2. Data Pipeline Integration (`test_data_pipeline.py`)
**Scenario**: Data flows from IB API through preprocessing to database

**Steps**:
1. Fetch market data via IB API
2. Preprocess and normalize data
3. Store in PostgreSQL/TimescaleDB
4. Retrieve and validate stored data

**Validation**:
- Data retrieved successfully
- Preprocessing applied correctly
- Database storage successful
- Retrieved data matches expected format

---

#### 3. Tax Reconciliation Workflow (`test_tax_reconciliation.py`)
**Scenario**: Complete tax calculation and reconciliation process

**Steps**:
1. Simulate multiple trades (buy/sell)
2. Detect wash sales
3. Calculate capital gains/losses
4. Track tax lots
5. Reconcile with broker statements
6. Generate tax reports

**Validation**:
- Wash sales correctly identified
- Capital gains calculated accurately
- Tax lots properly tracked
- Reconciliation successful
- Reports match expected values

---

#### 4. Error Handling and Recovery (`test_error_recovery.py`)
**Scenario**: System handles errors gracefully and recovers

**Steps**:
1. Simulate API connection failure
2. Verify retry mechanisms
3. Simulate database failure
4. Verify fallback mechanisms
5. Simulate order rejection
6. Verify error handling and logging

**Validation**:
- Errors caught and logged
- Retry mechanisms work
- Fallback strategies activated
- System remains stable

---

#### 5. API Connection Resilience (`test_api_resilience.py`)
**Scenario**: System maintains connection to IB API under various conditions

**Steps**:
1. Test connection stability over extended period
2. Simulate network interruptions
3. Verify reconnection logic
4. Test rate limit handling
5. Verify data continuity

**Validation**:
- Connection maintained or reconnected
- Rate limits respected
- Data stream uninterrupted
- No data loss

---

### Example Integration Test Structure

```python
import pytest
from components.data_layer.src.ib_api_client import IBAPIClient
from components.data_layer.src.data_retriever import DataRetriever
from components.data_layer.src.database_manager import DatabaseManager

@pytest.mark.integration
class TestDataPipeline:
    @pytest.fixture(scope="module")
    def test_db(self):
        """Setup test database"""
        db = DatabaseManager(database="test_db")
        db.create_schema()
        yield db
        db.drop_schema()

    def test_e2e_data_flow(self, test_db):
        """Test complete data flow from API to database"""
        # Setup
        api_client = IBAPIClient()
        retriever = DataRetriever(api_client)

        # Execute
        data = retriever.get_market_data("AAPL", "1d", "1m")
        test_db.insert_market_data(data)
        stored_data = test_db.query_market_data("AAPL")

        # Validate
        assert len(stored_data) > 0
        assert stored_data[0]["symbol"] == "AAPL"
        # Additional validations...
```

---

## Paper Trading Validation

### Overview
Paper trading validates system behavior in a real-world environment using IB paper trading account.

**Directory**: `tests/paper_trading/`

### Requirements

#### Duration
- **Minimum**: 2 weeks continuous operation
- **Target**: 4 weeks for comprehensive validation

#### Monitoring
- **Frequency**: Daily review
- **Metrics**: Performance, errors, tax accuracy
- **Logging**: Comprehensive logging of all operations

### Validation Steps

#### 1. Setup Paper Trading Environment
- [ ] Configure IB paper trading account
- [ ] Set up bot with paper trading credentials
- [ ] Configure initial capital allocation
- [ ] Enable comprehensive logging
- [ ] Set up monitoring dashboard

#### 2. Run Bot in Paper Trading Mode
- [ ] Start bot with paper trading configuration
- [ ] Monitor for minimum 2 weeks
- [ ] Log all trades, signals, and errors
- [ ] Collect performance metrics daily

#### 3. Compare Predictions vs. Actuals
- [ ] Track predicted vs. actual returns
- [ ] Analyze signal accuracy
- [ ] Evaluate model performance
- [ ] Identify overfitting or bias

#### 4. Validate Tax Calculations
- [ ] Compare bot tax calculations with manual calculations
- [ ] Verify wash sale detection accuracy
- [ ] Validate capital gains computations
- [ ] Check tax lot tracking correctness

#### 5. Assess Risk Management Effectiveness
- [ ] Verify position sizing limits
- [ ] Check drawdown controls
- [ ] Validate stop-loss execution
- [ ] Assess portfolio risk metrics

### Success Criteria

**System Stability**:
- No critical errors during testing period
- Uptime > 99%
- All trades executed successfully

**Performance**:
- Positive risk-adjusted returns (Sharpe > 0.5)
- Max drawdown < 15%
- Win rate > 50%

**Tax Accuracy**:
- 100% wash sale detection accuracy
- Capital gains calculations within 0.1% of manual verification
- Tax lot tracking 100% accurate

**Risk Controls**:
- No position limit breaches
- All risk rules enforced
- Emergency stops function correctly

---

## Validation Metrics

### 1. Trading Performance Metrics

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Sharpe Ratio | > 1.5 | > 0.5 |
| Max Drawdown | < 15% | < 25% |
| Win Rate | > 55% | > 45% |
| Profit Factor | > 1.3 | > 1.0 |
| Average Trade Duration | - | - |
| Total Return | > 0% | - |

### 2. System Performance Metrics

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| API Response Time | < 500ms | < 1000ms |
| Order Execution Latency | < 2s | < 5s |
| Data Refresh Rate | Real-time | < 5s delay |
| System Uptime | > 99.5% | > 99% |
| Error Rate | < 0.1% | < 1% |

### 3. Tax Accuracy Metrics

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Wash Sale Detection | 100% | 100% |
| Capital Gains Accuracy | 99.9%+ | 99% |
| Reconciliation Match Rate | 100% | 99.5% |
| Tax Report Generation Time | < 5s | < 30s |

---

## Test Execution Guidelines

### Pre-Commit Testing
```bash
# Run unit tests before every commit
poetry run pytest tests/unit/ -v --cov=components --cov-report=term-missing

# Run linting
poetry run ruff check components/
poetry run black --check components/

# Run type checking
poetry run mypy components/
```

### Daily Testing
```bash
# Run all tests (unit + integration)
poetry run pytest tests/ -v --cov=components --cov-report=html

# Check coverage report
open htmlcov/index.html
```

### Pre-Release Testing
```bash
# Run full test suite with strict settings
poetry run pytest tests/ -v --strict-markers --cov=components --cov-fail-under=80

# Run integration tests only
poetry run pytest tests/integration/ -v -m integration

# Generate coverage report
poetry run coverage html
```

---

## Continuous Integration

### CI Pipeline
1. **Trigger**: Every push to feature branches
2. **Steps**:
   - Install dependencies
   - Run linting (ruff, black)
   - Run type checking (mypy)
   - Run unit tests
   - Generate coverage report
   - Upload coverage to codecov (optional)
3. **Pass Criteria**:
   - All tests pass
   - Coverage > 80%
   - No linting errors

### CD Pipeline (Future)
1. **Trigger**: Merge to main branch
2. **Steps**:
   - Run full test suite
   - Run integration tests
   - Build Docker image
   - Deploy to staging
   - Run smoke tests
3. **Pass Criteria**:
   - All tests pass
   - Smoke tests successful

---

## Test Data Management

### Test Fixtures
- Store in `tests/fixtures/`
- Use factory_boy for dynamic test data
- Mock external API responses

### Test Database
- Use separate test database
- Reset between test runs
- Use transactions for rollback

### Test Secrets
- Never commit secrets to repository
- Use environment variables
- Use `.env.test` for test credentials

---

**Last Updated**: 2025-11-15
**Next Review**: 2025-11-22
