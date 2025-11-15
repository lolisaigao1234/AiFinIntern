# ARCHITECTURE.md - Technical Architecture Specification

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Status**: Initial Design
**Related**: See CLAUDE.md for project overview and planning

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [System Components](#system-components)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Database Schema Design](#database-schema-design)
5. [API Specifications](#api-specifications)
6. [Class Diagrams](#class-diagrams)
7. [Technology Stack Details](#technology-stack-details)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### Design Principles

1. **Modularity**: Each component is independently deployable and testable
2. **Scalability**: Horizontal scaling capability for data processing and strategy execution
3. **Reliability**: Fault-tolerant design with graceful degradation
4. **Security**: Defense-in-depth approach with encryption and access controls
5. **Observability**: Comprehensive logging, metrics, and tracing
6. **Maintainability**: Clean code, clear interfaces, extensive documentation

### Architecture Patterns

- **Layered Architecture**: Separation of concerns across data, business logic, and presentation
- **Event-Driven**: Asynchronous processing for market data and trade signals
- **Repository Pattern**: Abstract data access layer
- **Strategy Pattern**: Pluggable trading strategies
- **Observer Pattern**: Real-time event notifications

---

## System Components

### 1. Data Layer

#### Purpose
Manage all data ingestion, storage, and retrieval operations for market data and historical records.

#### Sub-Components

```
data_layer/
├── api_client/           # Interactive Brokers API wrapper
│   ├── connection.py     # Connection management
│   ├── market_data.py    # Market data streaming
│   ├── historical.py     # Historical data retrieval
│   └── retry_handler.py  # Exponential backoff retry logic
├── data_store/           # Database abstraction
│   ├── models.py         # SQLAlchemy ORM models
│   ├── repositories.py   # Data access repositories
│   └── migrations/       # Database migrations
├── preprocessing/        # Data transformation
│   ├── normalizer.py     # Price normalization
│   ├── feature_eng.py    # Feature engineering
│   └── validators.py     # Data quality checks
└── cache/                # Redis caching layer
    ├── cache_manager.py
    └── cache_policies.py
```

#### Key Interfaces

```python
class IMarketDataProvider(ABC):
    """Abstract interface for market data providers"""

    @abstractmethod
    async def get_real_time_quote(self, symbol: str) -> Quote:
        pass

    @abstractmethod
    async def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    async def subscribe_market_data(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        pass
```

#### Data Models

```python
@dataclass
class Quote:
    symbol: str
    timestamp: datetime
    bid: Decimal
    ask: Decimal
    last: Decimal
    volume: int
    bid_size: int
    ask_size: int

@dataclass
class OHLCV:
    symbol: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
```

---

### 2. Strategy Layer

#### Purpose
Implement trading strategies, ML models, and signal generation logic.

#### Sub-Components

```
strategy_layer/
├── models/               # ML models
│   ├── base_model.py     # Abstract base model
│   ├── lstm_model.py     # LSTM price prediction
│   ├── random_forest.py  # Random Forest classifier
│   └── ensemble.py       # Ensemble model
├── backtesting/          # Backtesting framework
│   ├── backtester.py     # Main backtesting engine
│   ├── metrics.py        # Performance metrics
│   └── optimizer.py      # Parameter optimization
├── signals/              # Signal generation
│   ├── technical.py      # Technical indicators
│   ├── ml_signals.py     # ML-based signals
│   └── composite.py      # Combined signals
└── strategies/           # Trading strategies
    ├── base_strategy.py  # Strategy interface
    ├── mean_reversion.py # Mean reversion strategy
    ├── momentum.py       # Momentum strategy
    └── ml_strategy.py    # ML-driven strategy
```

#### Key Interfaces

```python
class IStrategy(ABC):
    """Abstract interface for trading strategies"""

    @abstractmethod
    def generate_signals(
        self,
        market_data: pd.DataFrame
    ) -> List[Signal]:
        """Generate trading signals from market data"""
        pass

    @abstractmethod
    def calculate_position_size(
        self,
        signal: Signal,
        portfolio: Portfolio
    ) -> int:
        """Calculate appropriate position size"""
        pass

    @abstractmethod
    def should_close_position(
        self,
        position: Position,
        current_data: MarketData
    ) -> bool:
        """Determine if position should be closed"""
        pass
```

#### Signal Types

```python
from enum import Enum

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE_LONG = "CLOSE_LONG"
    CLOSE_SHORT = "CLOSE_SHORT"

@dataclass
class Signal:
    symbol: str
    signal_type: SignalType
    timestamp: datetime
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]
    strategy_name: str
```

---

### 3. Execution Layer

#### Purpose
Handle order placement, position management, and risk controls.

#### Sub-Components

```
execution_layer/
├── order_manager/        # Order management
│   ├── order_router.py   # Route orders to broker
│   ├── order_tracker.py  # Track order status
│   └── order_types.py    # Order type definitions
├── position_manager/     # Position tracking
│   ├── portfolio.py      # Portfolio state
│   ├── position.py       # Position model
│   └── reconciler.py     # Position reconciliation
├── risk_manager/         # Risk controls
│   ├── pre_trade.py      # Pre-trade risk checks
│   ├── position_limits.py# Position size limits
│   └── exposure.py       # Portfolio exposure analysis
└── execution_algos/      # Smart order routing
    ├── twap.py           # Time-weighted average price
    ├── vwap.py           # Volume-weighted average price
    └── adaptive.py       # Adaptive execution
```

#### Key Interfaces

```python
class IOrderManager(ABC):
    """Abstract interface for order management"""

    @abstractmethod
    async def place_order(self, order: Order) -> OrderConfirmation:
        """Place an order with the broker"""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order"""
        pass

    @abstractmethod
    async def get_order_status(self, order_id: str) -> OrderStatus:
        """Get current status of an order"""
        pass

    @abstractmethod
    async def modify_order(
        self,
        order_id: str,
        modifications: OrderModification
    ) -> OrderConfirmation:
        """Modify an existing order"""
        pass
```

#### Order Models

```python
from enum import Enum

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

@dataclass
class Order:
    symbol: str
    order_type: OrderType
    side: OrderSide
    quantity: int
    price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
    time_in_force: str = "DAY"
    order_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
```

#### Risk Management

```python
class RiskManager:
    """Pre-trade and post-trade risk management"""

    def __init__(self, config: RiskConfig):
        self.max_position_size = config.max_position_size
        self.max_portfolio_exposure = config.max_portfolio_exposure
        self.max_sector_exposure = config.max_sector_exposure
        self.max_single_loss = config.max_single_loss
        self.max_daily_loss = config.max_daily_loss

    def check_order_risk(
        self,
        order: Order,
        portfolio: Portfolio
    ) -> RiskCheckResult:
        """Validate order against risk limits"""
        checks = [
            self._check_position_size(order, portfolio),
            self._check_portfolio_exposure(order, portfolio),
            self._check_concentration_risk(order, portfolio),
            self._check_loss_limits(portfolio)
        ]
        return RiskCheckResult(
            approved=all(c.passed for c in checks),
            checks=checks
        )
```

---

### 4. Tax & Reconciliation Engine

#### Purpose
Calculate tax liabilities, detect wash sales, and reconcile with broker statements.

#### Sub-Components

```
tax_recon/
├── tax_lots/             # Tax lot tracking
│   ├── lot_manager.py    # Tax lot management
│   ├── fifo.py           # FIFO accounting
│   ├── lifo.py           # LIFO accounting
│   └── specific_id.py    # Specific identification
├── wash_sale/            # Wash sale detection
│   ├── detector.py       # Wash sale detection logic
│   ├── rules.py          # IRS wash sale rules
│   └── adjustment.py     # Cost basis adjustments
├── capital_gains/        # Capital gains calculation
│   ├── calculator.py     # Gains/losses calculator
│   ├── short_term.py     # Short-term gains
│   └── long_term.py      # Long-term gains
└── reconciliation/       # Broker reconciliation
    ├── statement_parser.py # Parse broker statements
    ├── reconciler.py     # Match trades and positions
    └── discrepancy.py    # Handle discrepancies
```

#### Tax Models

```python
@dataclass
class TaxLot:
    """Represents a tax lot for a security purchase"""
    symbol: str
    purchase_date: datetime
    quantity: int
    cost_basis: Decimal
    lot_id: str
    acquisition_method: str  # "BUY", "TRANSFER", etc.
    is_wash_sale_adjusted: bool = False
    wash_sale_disallowed: Decimal = Decimal('0')

@dataclass
class CapitalGain:
    """Represents a realized capital gain/loss"""
    symbol: str
    open_date: datetime
    close_date: datetime
    quantity: int
    cost_basis: Decimal
    proceeds: Decimal
    gain_loss: Decimal
    is_short_term: bool
    is_wash_sale: bool
    disallowed_loss: Decimal = Decimal('0')

class WashSaleDetector:
    """Detect wash sales per IRS rules"""

    WASH_SALE_WINDOW = timedelta(days=30)

    def detect_wash_sales(
        self,
        realized_losses: List[Trade],
        purchases: List[Trade]
    ) -> List[WashSale]:
        """
        Detect wash sales according to IRS Publication 550

        A wash sale occurs when you sell or trade stock or securities
        at a loss and within 30 days before or after the sale you:
        1. Buy substantially identical stock or securities
        2. Acquire substantially identical stock or securities in a fully taxable trade
        3. Acquire a contract or option to buy substantially identical stock or securities
        """
        wash_sales = []

        for loss_trade in realized_losses:
            if loss_trade.gain_loss >= 0:
                continue

            # Check 61-day window (30 days before + day of sale + 30 days after)
            window_start = loss_trade.close_date - self.WASH_SALE_WINDOW
            window_end = loss_trade.close_date + self.WASH_SALE_WINDOW

            # Find purchases of same security in window
            replacement_purchases = [
                p for p in purchases
                if p.symbol == loss_trade.symbol
                and window_start <= p.trade_date <= window_end
                and p.trade_date != loss_trade.close_date
            ]

            if replacement_purchases:
                wash_sales.append(
                    self._calculate_wash_sale(loss_trade, replacement_purchases)
                )

        return wash_sales
```

---

### 5. Reporting Engine

#### Purpose
Generate performance reports, tax documents, and analytics dashboards.

#### Sub-Components

```
reporting/
├── pnl/                  # P&L reporting
│   ├── daily_pnl.py      # Daily P&L calculator
│   ├── realized.py       # Realized P&L
│   └── unrealized.py     # Unrealized P&L
├── performance/          # Performance metrics
│   ├── returns.py        # Return calculations
│   ├── risk_metrics.py   # Sharpe, Sortino, etc.
│   └── attribution.py    # Performance attribution
├── tax_reports/          # Tax reporting
│   ├── form_8949.py      # IRS Form 8949 generator
│   ├── schedule_d.py     # Schedule D generator
│   └── trade_history.py  # Trade history export
└── dashboards/           # Visualization
    ├── plotly_dash.py    # Interactive dashboard
    ├── charts.py         # Chart generators
    └── exports.py        # Export to Excel/PDF
```

#### Metrics Calculations

```python
class PerformanceMetrics:
    """Calculate portfolio performance metrics"""

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate annualized Sharpe ratio"""
        excess_returns = returns - (risk_free_rate / 252)
        return np.sqrt(252) * (excess_returns.mean() / excess_returns.std())

    @staticmethod
    def sortino_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate annualized Sortino ratio"""
        excess_returns = returns - (risk_free_rate / 252)
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = downside_returns.std()
        return np.sqrt(252) * (excess_returns.mean() / downside_std)

    @staticmethod
    def max_drawdown(returns: pd.Series) -> float:
        """Calculate maximum drawdown"""
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()

    @staticmethod
    def calmar_ratio(
        returns: pd.Series,
        periods_per_year: int = 252
    ) -> float:
        """Calculate Calmar ratio (annualized return / max drawdown)"""
        annual_return = (1 + returns.mean()) ** periods_per_year - 1
        max_dd = abs(PerformanceMetrics.max_drawdown(returns))
        return annual_return / max_dd if max_dd != 0 else 0
```

---

## Data Flow Architecture

### Real-Time Trading Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Market Data Stream                           │
│                  (Interactive Brokers API)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Data Layer           │
            │   - Normalization      │
            │   - Validation         │
            │   - Feature Engineering│
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Strategy Layer       │
            │   - ML Models          │
            │   - Signal Generation  │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Risk Manager         │
            │   - Pre-trade Checks   │
            │   - Position Limits    │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Execution Layer      │
            │   - Order Routing      │
            │   - Position Tracking  │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Broker Execution     │
            │   (Interactive Brokers)│
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Tax & Reconciliation │
            │   - Tax Lot Update     │
            │   - P&L Calculation    │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Reporting Engine     │
            │   - Dashboards         │
            │   - Alerts             │
            └────────────────────────┘
```

### Backtesting Flow

```
┌────────────────────┐
│ Historical Data DB │
└─────────┬──────────┘
          │
          ▼
┌────────────────────────┐
│ Backtesting Engine     │
│ - Walk-forward analysis│
│ - Strategy simulation  │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ Performance Metrics    │
│ - Returns              │
│ - Sharpe Ratio         │
│ - Drawdown             │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ Optimization Engine    │
│ - Parameter tuning     │
│ - Strategy selection   │
└────────────────────────┘
```

---

## Database Schema Design

### PostgreSQL Schema

```sql
-- Market Data Tables

CREATE TABLE symbols (
    symbol_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL UNIQUE,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    exchange VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE market_data (
    id BIGSERIAL PRIMARY KEY,
    symbol_id INTEGER REFERENCES symbols(symbol_id),
    timestamp TIMESTAMP NOT NULL,
    open NUMERIC(15, 4) NOT NULL,
    high NUMERIC(15, 4) NOT NULL,
    low NUMERIC(15, 4) NOT NULL,
    close NUMERIC(15, 4) NOT NULL,
    volume BIGINT NOT NULL,
    interval VARCHAR(10) NOT NULL, -- '1min', '5min', '1day', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol_id, timestamp, interval)
);

CREATE INDEX idx_market_data_symbol_time
ON market_data(symbol_id, timestamp DESC);

-- Trading Tables

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    symbol_id INTEGER REFERENCES symbols(symbol_id),
    order_type VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(15, 4),
    stop_price NUMERIC(15, 4),
    status VARCHAR(20) NOT NULL,
    submitted_at TIMESTAMP NOT NULL,
    filled_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    rejection_reason TEXT,
    strategy_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE executions (
    execution_id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES orders(order_id),
    executed_quantity INTEGER NOT NULL,
    executed_price NUMERIC(15, 4) NOT NULL,
    commission NUMERIC(10, 4) NOT NULL,
    executed_at TIMESTAMP NOT NULL,
    exchange VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE positions (
    position_id SERIAL PRIMARY KEY,
    symbol_id INTEGER REFERENCES symbols(symbol_id),
    quantity INTEGER NOT NULL,
    average_cost NUMERIC(15, 4) NOT NULL,
    current_price NUMERIC(15, 4),
    unrealized_pnl NUMERIC(15, 4),
    opened_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol_id, opened_at)
);

-- Tax Tracking Tables

CREATE TABLE tax_lots (
    lot_id VARCHAR(50) PRIMARY KEY,
    symbol_id INTEGER REFERENCES symbols(symbol_id),
    purchase_date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL,
    remaining_quantity INTEGER NOT NULL,
    cost_basis NUMERIC(15, 4) NOT NULL,
    wash_sale_adjusted_basis NUMERIC(15, 4),
    acquisition_method VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE capital_gains (
    gain_id SERIAL PRIMARY KEY,
    symbol_id INTEGER REFERENCES symbols(symbol_id),
    lot_id VARCHAR(50) REFERENCES tax_lots(lot_id),
    open_date TIMESTAMP NOT NULL,
    close_date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL,
    cost_basis NUMERIC(15, 4) NOT NULL,
    proceeds NUMERIC(15, 4) NOT NULL,
    gain_loss NUMERIC(15, 4) NOT NULL,
    is_short_term BOOLEAN NOT NULL,
    is_wash_sale BOOLEAN DEFAULT FALSE,
    disallowed_loss NUMERIC(15, 4) DEFAULT 0,
    tax_year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE wash_sales (
    wash_sale_id SERIAL PRIMARY KEY,
    loss_trade_id INTEGER REFERENCES capital_gains(gain_id),
    replacement_trade_id INTEGER REFERENCES capital_gains(gain_id),
    disallowed_loss NUMERIC(15, 4) NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Tracking Tables

CREATE TABLE daily_pnl (
    date DATE PRIMARY KEY,
    realized_pnl NUMERIC(15, 4) NOT NULL,
    unrealized_pnl NUMERIC(15, 4) NOT NULL,
    total_pnl NUMERIC(15, 4) NOT NULL,
    portfolio_value NUMERIC(15, 4) NOT NULL,
    cash_balance NUMERIC(15, 4) NOT NULL,
    num_trades INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE strategy_performance (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    num_signals INTEGER DEFAULT 0,
    num_trades INTEGER DEFAULT 0,
    pnl NUMERIC(15, 4) NOT NULL,
    win_rate NUMERIC(5, 4),
    sharpe_ratio NUMERIC(10, 6),
    max_drawdown NUMERIC(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(strategy_name, date)
);
```

### Redis Cache Structure

```
# Market Data Cache (5-minute TTL)
market:quote:{symbol} -> JSON {bid, ask, last, volume, timestamp}
market:ohlcv:{symbol}:{interval} -> JSON array of OHLCV data

# Position Cache (real-time updates)
position:current:{symbol} -> JSON {quantity, avg_cost, unrealized_pnl}
portfolio:summary -> JSON {total_value, cash, positions_value, pnl}

# Strategy Signals Cache (15-minute TTL)
signal:{strategy_name}:{symbol} -> JSON {signal_type, confidence, timestamp}

# Risk Limits Cache (1-hour TTL)
risk:limits:position -> JSON {max_position_size, max_exposure}
risk:exposure:current -> JSON {sector_exposure, total_exposure}
```

---

## API Specifications

### Internal REST API

```python
# FastAPI Application Structure

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Quant Trading Bot API", version="1.0.0")

# Request/Response Models

class OrderRequest(BaseModel):
    symbol: str
    order_type: str  # MARKET, LIMIT
    side: str  # BUY, SELL
    quantity: int
    price: Optional[Decimal] = None
    strategy_name: Optional[str] = None

class OrderResponse(BaseModel):
    order_id: str
    status: str
    submitted_at: datetime
    message: str

class PositionResponse(BaseModel):
    symbol: str
    quantity: int
    average_cost: Decimal
    current_price: Decimal
    unrealized_pnl: Decimal
    pnl_percentage: float

# API Endpoints

@app.post("/api/v1/orders", response_model=OrderResponse)
async def place_order(order: OrderRequest):
    """Place a new trading order"""
    # Risk checks
    # Order validation
    # Submit to broker
    pass

@app.get("/api/v1/positions", response_model=List[PositionResponse])
async def get_positions():
    """Get all current positions"""
    pass

@app.get("/api/v1/positions/{symbol}", response_model=PositionResponse)
async def get_position(symbol: str):
    """Get position for specific symbol"""
    pass

@app.get("/api/v1/pnl/daily")
async def get_daily_pnl(start_date: date, end_date: date):
    """Get daily P&L for date range"""
    pass

@app.get("/api/v1/tax/capital-gains/{year}")
async def get_capital_gains(year: int):
    """Get capital gains/losses for tax year"""
    pass

@app.post("/api/v1/strategies/{strategy_name}/backtest")
async def run_backtest(
    strategy_name: str,
    start_date: date,
    end_date: date,
    parameters: dict
):
    """Run strategy backtest"""
    pass
```

---

## Class Diagrams

### Core Trading System Classes

```python
# Domain Models

class Portfolio:
    """Portfolio state and management"""

    def __init__(self):
        self.cash: Decimal = Decimal('100000')
        self.positions: Dict[str, Position] = {}
        self.order_history: List[Order] = []
        self.transaction_history: List[Transaction] = []

    def calculate_total_value(self, current_prices: Dict[str, Decimal]) -> Decimal:
        """Calculate total portfolio value"""
        positions_value = sum(
            pos.quantity * current_prices.get(pos.symbol, pos.average_cost)
            for pos in self.positions.values()
        )
        return self.cash + positions_value

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for symbol"""
        return self.positions.get(symbol)

    def update_position(
        self,
        symbol: str,
        quantity_change: int,
        price: Decimal
    ):
        """Update position after trade execution"""
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol, 0, Decimal('0'))

        position = self.positions[symbol]
        position.update(quantity_change, price)

        if position.quantity == 0:
            del self.positions[symbol]

class Position:
    """Individual position in a security"""

    def __init__(self, symbol: str, quantity: int, average_cost: Decimal):
        self.symbol = symbol
        self.quantity = quantity
        self.average_cost = average_cost
        self.opened_at = datetime.utcnow()

    def update(self, quantity_change: int, price: Decimal):
        """Update position with new trade"""
        if quantity_change > 0:  # Adding to position
            total_cost = (self.quantity * self.average_cost) + \
                        (quantity_change * price)
            self.quantity += quantity_change
            self.average_cost = total_cost / self.quantity
        else:  # Reducing position
            self.quantity += quantity_change  # quantity_change is negative

    def calculate_unrealized_pnl(self, current_price: Decimal) -> Decimal:
        """Calculate unrealized P&L"""
        return (current_price - self.average_cost) * self.quantity

class TradingBot:
    """Main trading bot orchestrator"""

    def __init__(
        self,
        data_provider: IMarketDataProvider,
        strategy: IStrategy,
        order_manager: IOrderManager,
        risk_manager: RiskManager,
        portfolio: Portfolio
    ):
        self.data_provider = data_provider
        self.strategy = strategy
        self.order_manager = order_manager
        self.risk_manager = risk_manager
        self.portfolio = portfolio
        self.is_running = False

    async def start(self):
        """Start the trading bot"""
        self.is_running = True
        await self._trading_loop()

    async def _trading_loop(self):
        """Main trading loop"""
        while self.is_running:
            try:
                # Get market data
                market_data = await self.data_provider.get_market_snapshot()

                # Generate signals
                signals = self.strategy.generate_signals(market_data)

                # Process signals
                for signal in signals:
                    await self._process_signal(signal)

                # Wait for next iteration
                await asyncio.sleep(self.config.loop_interval)

            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                await self._handle_error(e)

    async def _process_signal(self, signal: Signal):
        """Process a trading signal"""
        # Calculate position size
        position_size = self.strategy.calculate_position_size(
            signal,
            self.portfolio
        )

        # Create order
        order = Order(
            symbol=signal.symbol,
            order_type=OrderType.MARKET,
            side=OrderSide.BUY if signal.signal_type == SignalType.BUY else OrderSide.SELL,
            quantity=position_size
        )

        # Risk checks
        risk_result = self.risk_manager.check_order_risk(order, self.portfolio)
        if not risk_result.approved:
            logger.warning(f"Order rejected by risk manager: {risk_result.reason}")
            return

        # Submit order
        confirmation = await self.order_manager.place_order(order)
        logger.info(f"Order placed: {confirmation}")
```

---

## Technology Stack Details

### Core Technologies

```yaml
Language:
  - Python: 3.14.0 (Required)
  - Type Hints: Full typing support with mypy

Hardware Environment (Local Development):
  - CPU: AMD Ryzen 7 7700X (8 cores, 16 threads)
  - GPU: NVIDIA RTX 5090 Founders Edition (24GB VRAM)
  - RAM: 32GB DDR5
  - CUDA: 12.x with cuDNN 8.9+

API & Broker Integration:
  - Interactive Brokers: ib_insync (async wrapper for ibapi)
  - Alternative: alpaca-trade-api (for Alpaca broker)

Data Processing:
  - pandas: 2.1+
  - numpy: 1.26+
  - polars: High-performance alternative to pandas
  - pyarrow: Columnar data format

Machine Learning:
  - PyTorch: 2.5.1+ (CUDA 12.1 enabled for RTX 5090)
  - TensorFlow: 2.18.0+ (GPU support with CUDA)
  - Hugging Face Transformers: 4.46+ (pre-trained model fine-tuning)
  - scikit-learn: 1.6+ (traditional ML models)
  - XGBoost: 2.1+ (gradient boosting)
  - LightGBM: 4.5+ (fast gradient boosting)

ML Model Fine-Tuning (Hugging Face):
  - Financial Sentiment: ProsusAI/finbert, yiyanghkust/finbert-tone
  - Time Series: AutonLab/MOMENT-1-large, google/timesfm-1.0-200m
  - General Transformers: distilbert, deberta-v3, flan-t5
  - Fine-tuning Libraries: transformers, datasets, accelerate, peft (LoRA)
  - Quantization: bitsandbytes (8-bit optimizers)

GPU Acceleration:
  - CUDA Toolkit: 12.6+
  - cuDNN: 8.9+
  - CuPy: 13.3+ (NumPy-compatible GPU arrays)
  - Mixed Precision: FP16 training for faster convergence
  - Optimization: TF32 for matrix operations on RTX 5090

Database:
  - PostgreSQL: 15+ (primary relational database)
  - TimescaleDB: Time-series extension for PostgreSQL
  - Redis: 7+ (caching and pub/sub)

Web Framework:
  - FastAPI: REST API endpoints
  - WebSockets: Real-time data streaming
  - Uvicorn: ASGI server

Testing:
  - pytest: Unit and integration tests
  - pytest-asyncio: Async test support
  - hypothesis: Property-based testing
  - pytest-cov: Code coverage

Monitoring & Logging:
  - structlog: Structured logging
  - Prometheus: Metrics collection
  - Grafana: Dashboards and visualization
  - Sentry: Error tracking

Development Tools:
  - Poetry: Dependency management
  - Black: Code formatting
  - Ruff: Fast linting
  - mypy: Static type checking
  - pre-commit: Git hooks
```

### Project Dependencies (pyproject.toml)

```toml
[tool.poetry]
name = "quant-trading-bot"
version = "0.1.0"
description = "AI-Driven Quantitative Trading Bot"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.14.0"
# Trading & Market Data
ib-insync = "^0.9.86"
pandas = "^2.1.0"
numpy = "^1.26.0"
polars = "^0.19.0"

# Machine Learning (GPU-enabled)
torch = "^2.5.1"  # Install with: --index-url https://download.pytorch.org/whl/cu121
tensorflow = {extras = ["and-cuda"], version = "^2.18.0"}
scikit-learn = "^1.6.0"
xgboost = "^2.1.0"
lightgbm = "^4.5.0"

# Hugging Face Ecosystem
transformers = "^4.46.0"
datasets = "^3.1.0"
accelerate = "^1.1.0"
peft = "^0.13.0"
bitsandbytes = "^0.44.0"

# Database
sqlalchemy = "^2.0.0"
asyncpg = "^0.28.0"
redis = "^4.6.0"
alembic = "^1.11.0"

# Web Framework
fastapi = "^0.100.0"
uvicorn = {extras = ["standard"], version = "^0.23.0"}
pydantic = "^2.0.0"

# Utilities
python-dotenv = "^1.0.0"
pyyaml = "^6.0"
structlog = "^23.1.0"
tenacity = "^8.2.0"

# Monitoring
prometheus-client = "^0.17.0"
sentry-sdk = "^1.28.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
hypothesis = "^6.82.0"
black = "^23.7.0"
ruff = "^0.0.280"
mypy = "^1.4.0"
pre-commit = "^3.3.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## ML Model Fine-Tuning Architecture

### Fine-Tuning Philosophy

**Core Principle**: Leverage pre-trained models from Hugging Face and other open-source platforms rather than training from scratch.

**Rationale**:
- **Transfer Learning**: Utilize knowledge from large-scale pre-training on massive datasets
- **Time Efficiency**: Reduce training time from weeks/months to hours/days
- **Cost Efficiency**: Lower computational costs (no need for extensive pre-training)
- **Better Performance**: State-of-the-art architectures from research community
- **Data Efficiency**: Achieve good results with limited financial data

### GPU Optimization Strategy

#### Hardware Utilization (RTX 5090)

```python
import torch
import tensorflow as tf

# PyTorch CUDA Configuration
def configure_pytorch_gpu():
    """Optimize PyTorch for RTX 5090"""
    assert torch.cuda.is_available(), "CUDA not available!"

    # Device info
    device = torch.device("cuda:0")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

    # Optimization settings
    torch.backends.cudnn.benchmark = True  # Auto-tune kernels
    torch.backends.cuda.matmul.allow_tf32 = True  # TF32 for matmul
    torch.set_float32_matmul_precision('high')  # Better performance

    # Memory management
    torch.cuda.empty_cache()  # Clear cache before training

    return device

# TensorFlow GPU Configuration
def configure_tensorflow_gpu():
    """Optimize TensorFlow for RTX 5090"""
    gpus = tf.config.list_physical_devices('GPU')

    if gpus:
        for gpu in gpus:
            # Enable memory growth (prevent OOM)
            tf.config.experimental.set_memory_growth(gpu, True)

        # Mixed precision for faster training
        tf.keras.mixed_precision.set_global_policy('mixed_float16')

        print(f"TensorFlow GPU: {tf.test.gpu_device_name()}")
```

#### Memory Optimization Techniques

**1. Mixed Precision Training (FP16)**
```python
from torch.cuda.amp import autocast, GradScaler

# PyTorch mixed precision
scaler = GradScaler()

for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()

        # Automatic mixed precision
        with autocast():
            outputs = model(batch['input_ids'], attention_mask=batch['attention_mask'])
            loss = outputs.loss

        # Scale loss and backprop
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
```

**2. Gradient Checkpointing**
```python
# Trade computation for memory (reduces VRAM usage by ~30%)
model.gradient_checkpointing_enable()
```

**3. Gradient Accumulation**
```python
# Simulate larger batch sizes
accumulation_steps = 4
for i, batch in enumerate(dataloader):
    outputs = model(**batch)
    loss = outputs.loss / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

**4. Dynamic Batching**
```python
# Adjust batch size based on available memory
def get_optimal_batch_size(model, device, sample_input):
    """Find largest batch size that fits in memory"""
    batch_size = 1
    while True:
        try:
            # Test batch
            batch = {k: v.repeat(batch_size, 1).to(device)
                    for k, v in sample_input.items()}
            _ = model(**batch)
            batch_size *= 2
        except RuntimeError:  # OOM
            return batch_size // 2
```

### Fine-Tuning Pipeline Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Fine-Tuning Pipeline Architecture              │
└─────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Model        │  │ Data         │  │ Training     │
│ Selection    │  │ Preparation  │  │ Pipeline     │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Download     │  │ Tokenization │  │ GPU          │
│ Pre-trained  │  │ & Feature    │  │ Training     │
│ Model        │  │ Engineering  │  │ (RTX 5090)   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        ▼                ▼                ▼
┌──────────────────────────────────────────────────┐
│            Evaluation & Validation                │
└──────────────────────────────────────────────────┘
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Model        │  │ Inference    │  │ Deployment   │
│ Export       │  │ Optimization │  │ to Trading   │
│ (ONNX)       │  │ (Quantize)   │  │ System       │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Recommended Models for Financial Trading

#### 1. Financial Sentiment Analysis

**Model**: `ProsusAI/finbert`
- **Purpose**: Analyze financial news sentiment
- **Architecture**: BERT-base fine-tuned on financial data
- **Use Case**: News-driven trading signals

**Fine-tuning Example**:
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments

# Load pre-trained FinBERT
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained(
    "ProsusAI/finbert",
    num_labels=3  # Positive, Negative, Neutral
)

# Training arguments optimized for RTX 5090
training_args = TrainingArguments(
    output_dir="./models/finbert_custom",
    num_train_epochs=3,
    per_device_train_batch_size=32,  # Large batch for 24GB VRAM
    per_device_eval_batch_size=64,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    fp16=True,  # Mixed precision
    dataloader_num_workers=8,  # Utilize all CPU cores
    optim="adamw_torch_fused",  # Faster optimizer
)
```

#### 2. Time Series Forecasting

**Model**: `AutonLab/MOMENT-1-large`
- **Purpose**: General-purpose time series foundation model
- **Architecture**: Transformer-based time series model
- **Use Case**: Price prediction, trend forecasting

**Alternative**: `google/timesfm-1.0-200m`
- **Purpose**: Time series forecasting at scale
- **Architecture**: Decoder-only transformer
- **Use Case**: Multi-horizon forecasting

#### 3. Parameter-Efficient Fine-Tuning (PEFT)

**Using LoRA for Memory Efficiency**:
```python
from peft import LoraConfig, get_peft_model, TaskType

# Configure LoRA (Low-Rank Adaptation)
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8,  # Rank
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["query", "value"]  # Only fine-tune attention
)

# Apply LoRA to model (reduces trainable params by 90%+)
model = get_peft_model(model, lora_config)
print(f"Trainable params: {model.num_parameters(only_trainable=True):,}")
```

### Training Performance Benchmarks

**Expected Performance on RTX 5090:**

| Model | Params | Batch Size | Throughput (samples/sec) | Training Time (1 epoch, 10k samples) |
|-------|--------|------------|-------------------------|-------------------------------------|
| FinBERT | 110M | 32 | ~180 | ~15 minutes |
| DistilBERT | 66M | 64 | ~320 | ~8 minutes |
| MOMENT-1-large | 385M | 16 | ~90 | ~30 minutes |
| Custom LSTM | 5M | 256 | ~2000 | ~2 minutes |

**Memory Usage**:
- FinBERT (batch 32, FP16): ~12GB VRAM
- FinBERT (batch 32, FP32): ~20GB VRAM
- MOMENT-1-large (batch 16, FP16): ~18GB VRAM

### Model Integration with Trading System

```python
# components/strategy_layer/models/ml_model_loader.py

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class FinancialMLModel:
    """Wrapper for fine-tuned financial ML models"""

    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()  # Inference mode

    @torch.no_grad()
    def predict_sentiment(self, text: str) -> dict:
        """Predict sentiment for financial text"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)

        return {
            "positive": probabilities[0][0].item(),
            "negative": probabilities[0][1].item(),
            "neutral": probabilities[0][2].item()
        }
```

### Monitoring and Optimization

**GPU Monitoring During Training**:
```python
import torch

def log_gpu_metrics():
    """Log GPU utilization and memory"""
    if torch.cuda.is_available():
        print(f"GPU Memory Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
        print(f"GPU Memory Reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
        print(f"GPU Utilization: {torch.cuda.utilization()}%")
```

**TensorBoard Integration**:
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('logs/finbert_training')

# Log metrics
writer.add_scalar('Loss/train', train_loss, epoch)
writer.add_scalar('Accuracy/val', val_accuracy, epoch)
writer.add_scalar('GPU/memory_allocated', torch.cuda.memory_allocated() / 1e9, epoch)
```

---

## Security Architecture

### Security Principles

1. **Secrets Management**: Never store credentials in code or config files
2. **API Key Rotation**: Regular rotation of API keys and tokens
3. **Least Privilege**: Minimal permissions for each component
4. **Encryption**: All sensitive data encrypted at rest and in transit
5. **Audit Logging**: Comprehensive logging of all trading activities
6. **Input Validation**: Strict validation of all external inputs

### Secrets Management

```python
# Using environment variables and secret management

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment"""

    # Interactive Brokers credentials
    IB_HOST: str = "127.0.0.1"
    IB_PORT: int = 7497
    IB_CLIENT_ID: int = 1
    IB_ACCOUNT: str

    # Database
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    SENTRY_DSN: Optional[str] = None

    # Trading parameters
    MAX_POSITION_SIZE: int = 1000
    MAX_DAILY_LOSS: float = 5000.0

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Authentication & Authorization

```python
# API authentication using JWT tokens

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.post("/api/v1/orders")
async def place_order(
    order: OrderRequest,
    user: dict = Depends(verify_token)
):
    """Protected endpoint requiring authentication"""
    pass
```

---

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────┐
│  Developer Machine                   │
│  ┌─────────────────────────────────┐│
│  │  Trading Bot (local)            ││
│  │  - Paper trading mode           ││
│  │  - Mock data provider           ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  PostgreSQL (Docker)            ││
│  │  Redis (Docker)                 ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Production Environment

```
┌──────────────────────────────────────────────────────────┐
│  Cloud Infrastructure (AWS/GCP/Azure)                     │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Application Layer                                  │  │
│  │  ┌──────────────┐  ┌──────────────┐               │  │
│  │  │ Trading Bot  │  │ Trading Bot  │  (redundancy) │  │
│  │  │  Instance 1  │  │  Instance 2  │               │  │
│  │  └──────────────┘  └──────────────┘               │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Data Layer                                         │  │
│  │  ┌──────────────────┐  ┌──────────────────┐       │  │
│  │  │  PostgreSQL      │  │  Redis Cluster   │       │  │
│  │  │  (RDS/CloudSQL)  │  │  (ElastiCache)   │       │  │
│  │  └──────────────────┘  └──────────────────┘       │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Monitoring & Logging                               │  │
│  │  ┌──────────────┐  ┌──────────────┐               │  │
│  │  │  Prometheus  │  │  Grafana     │               │  │
│  │  └──────────────┘  └──────────────┘               │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

# Copy application code
COPY . .

# Run the application
CMD ["python", "-m", "src.main"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: trading_bot
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  trading_bot:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/trading_bot
      REDIS_URL: redis://redis:6379
    volumes:
      - ./logs:/app/logs

volumes:
  postgres_data:
  redis_data:
```

---

## Performance Considerations

### Optimization Strategies

1. **Database Optimization**
   - Indexing on frequently queried columns (symbol, timestamp)
   - Partitioning large tables by date
   - Connection pooling
   - Materialized views for complex queries

2. **Caching Strategy**
   - Redis for real-time market data (5-minute TTL)
   - Application-level caching for static data
   - Cache warming on startup

3. **Async Processing**
   - Asyncio for I/O-bound operations
   - Concurrent order processing
   - Background tasks for reporting

4. **Data Pipeline**
   - Batch processing for historical data
   - Streaming for real-time updates
   - Efficient serialization (msgpack, protobuf)

### Performance Targets

```yaml
Latency:
  Market Data Ingestion: < 50ms p99
  Signal Generation: < 100ms p99
  Order Placement: < 200ms p99
  Risk Checks: < 10ms p99

Throughput:
  Market Data Updates: 10,000 msgs/sec
  Orders Per Second: 100 orders/sec
  Database Writes: 5,000 writes/sec

Resource Usage:
  Memory: < 2GB per instance
  CPU: < 50% average utilization
  Database Connections: < 100 connections
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-15 | Initial architecture design | System |

---

**Next Review Date**: 2025-11-22
**Document Owner**: Technical Lead
**Approval Status**: Draft - Pending Review
