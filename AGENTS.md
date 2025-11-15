# AGENTS.md - AI Agent Configuration & Management

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Related**: See CLAUDE.md for project overview, ARCHITECTURE.md for technical details

---

## Table of Contents
1. [Agent Overview](#agent-overview)
2. [Agent Architecture](#agent-architecture)
3. [Agent Specifications](#agent-specifications)
4. [Agent Communication Patterns](#agent-communication-patterns)
5. [Agent Deployment](#agent-deployment)
6. [Context Management](#context-management)

---

## Agent Overview

### Purpose
This document defines all AI agents (subagents) used in the Quant Trading Bot project. Each agent is designed to work autonomously within its domain while collaborating with other agents to achieve overall system goals.

### Design Philosophy
- **Single Responsibility**: Each agent has a clearly defined scope
- **Autonomous Operation**: Agents operate independently within their domain
- **Contextual Awareness**: Agents maintain focused context to avoid token limits
- **Collaboration**: Agents communicate via well-defined interfaces
- **Resilience**: Agents handle failures gracefully

---

## Agent Architecture

### Agent Hierarchy

```
Main Orchestrator (Human/System)
    │
    ├─── Data Layer Agent (Subagent 1)
    │    ├─── API Client Agent
    │    ├─── Data Store Agent
    │    └─── Preprocessing Agent
    │
    ├─── Strategy Layer Agent (Subagent 2)
    │    ├─── Model Training Agent
    │    ├─── Backtesting Agent
    │    └─── Signal Generation Agent
    │
    ├─── Execution Layer Agent (Subagent 3)
    │    ├─── Order Management Agent
    │    ├─── Position Tracking Agent
    │    └─── Risk Management Agent
    │
    ├─── Tax & Recon Agent (Subagent 4)
    │    ├─── Tax Lot Agent
    │    ├─── Wash Sale Agent
    │    └─── Capital Gains Agent
    │
    └─── Reporting Agent (Subagent 5)
         ├─── P&L Calculation Agent
         ├─── Performance Metrics Agent
         └─── Report Generation Agent
```

---

## Agent Specifications

### 1. Data Layer Agent (Subagent 1)

**Location**: `components/data_layer/agents/`

**Primary Responsibility**: Manage all data ingestion, storage, and retrieval operations

**Context Scope**:
- Market data schemas and formats
- Database connection configurations
- API rate limits and retry policies
- Data validation rules

**Sub-Agents**:

#### 1.1 API Client Agent
**File**: `components/data_layer/agents/api_client_agent.md`

**Responsibilities**:
- Connect to Interactive Brokers API
- Stream real-time market data
- Retrieve historical data
- Handle connection failures and retries
- Manage API rate limits

**Context Requirements**:
```yaml
Required Context:
  - IB API documentation
  - Connection parameters
  - Rate limit specifications
  - Error handling patterns

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/data_layer/api_client/connection.py
  - components/data_layer/api_client/market_data.py
  - components/data_layer/api_client/retry_handler.py
```

**Decision Boundaries**:
- Can adjust retry timing and backoff strategies
- Can cache frequently requested data
- Cannot modify API credentials without approval
- Cannot change data schema without coordination

---

#### 1.2 Data Store Agent
**File**: `components/data_layer/agents/data_store_agent.md`

**Responsibilities**:
- Manage database connections and queries
- Implement repository pattern for data access
- Handle database migrations
- Optimize query performance

**Context Requirements**:
```yaml
Required Context:
  - Database schema definitions
  - SQLAlchemy ORM models
  - Query optimization patterns
  - Migration scripts

Max Context Size: 10K tokens

Key Files to Monitor:
  - components/data_layer/data_store/models.py
  - components/data_layer/data_store/repositories.py
  - components/data_layer/data_store/migrations/
```

**Decision Boundaries**:
- Can optimize queries and add indexes
- Can create new repository methods
- Cannot modify core data models without coordination
- Cannot delete historical data without approval

---

#### 1.3 Preprocessing Agent
**File**: `components/data_layer/agents/preprocessing_agent.md`

**Responsibilities**:
- Normalize market data
- Engineer features for ML models
- Validate data quality
- Handle missing or anomalous data

**Context Requirements**:
```yaml
Required Context:
  - Feature engineering specifications
  - Data normalization techniques
  - Quality validation rules
  - Anomaly detection thresholds

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/data_layer/preprocessing/normalizer.py
  - components/data_layer/preprocessing/feature_eng.py
  - components/data_layer/preprocessing/validators.py
```

**Decision Boundaries**:
- Can add new features for ML models
- Can adjust normalization parameters
- Cannot remove existing features without impact analysis
- Cannot change validation rules that affect other components

---

### 2. Strategy Layer Agent (Subagent 2)

**Location**: `components/strategy_layer/agents/`

**Primary Responsibility**: Develop and optimize trading strategies and ML models

**Context Scope**:
- ML model architectures
- Backtesting methodologies
- Strategy parameters
- Performance metrics

**Sub-Agents**:

#### 2.1 Model Training Agent
**File**: `components/strategy_layer/agents/model_training_agent.md`

**Responsibilities**:
- Train ML models on historical data
- Perform hyperparameter tuning
- Implement cross-validation
- Monitor model performance

**Context Requirements**:
```yaml
Required Context:
  - Model architecture specifications
  - Training data format
  - Hyperparameter ranges
  - Evaluation metrics

Max Context Size: 12K tokens

Key Files to Monitor:
  - components/strategy_layer/models/base_model.py
  - components/strategy_layer/models/lstm_model.py
  - components/strategy_layer/models/ensemble.py
```

**Decision Boundaries**:
- Can experiment with model architectures
- Can adjust hyperparameters within defined ranges
- Cannot deploy models without validation metrics meeting thresholds
- Cannot change model input/output interfaces without coordination

---

#### 2.2 Backtesting Agent
**File**: `components/strategy_layer/agents/backtesting_agent.md`

**Responsibilities**:
- Run strategy backtests on historical data
- Calculate performance metrics
- Perform walk-forward optimization
- Generate backtest reports

**Context Requirements**:
```yaml
Required Context:
  - Backtesting framework design
  - Performance metric calculations
  - Transaction cost models
  - Slippage assumptions

Max Context Size: 10K tokens

Key Files to Monitor:
  - components/strategy_layer/backtesting/backtester.py
  - components/strategy_layer/backtesting/metrics.py
  - components/strategy_layer/backtesting/optimizer.py
```

**Decision Boundaries**:
- Can adjust backtesting parameters
- Can add new performance metrics
- Cannot modify historical data
- Cannot override risk constraints in backtests

---

#### 2.3 Signal Generation Agent
**File**: `components/strategy_layer/agents/signal_generation_agent.md`

**Responsibilities**:
- Generate trading signals from market data
- Combine signals from multiple sources
- Calculate signal confidence scores
- Filter low-quality signals

**Context Requirements**:
```yaml
Required Context:
  - Signal generation algorithms
  - Technical indicator calculations
  - ML model prediction interfaces
  - Signal filtering criteria

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/strategy_layer/signals/technical.py
  - components/strategy_layer/signals/ml_signals.py
  - components/strategy_layer/signals/composite.py
```

**Decision Boundaries**:
- Can adjust signal thresholds
- Can combine signals in new ways
- Cannot generate signals without minimum confidence level
- Cannot bypass signal validation checks

---

### 3. Execution Layer Agent (Subagent 3)

**Location**: `components/execution_layer/agents/`

**Primary Responsibility**: Execute trades and manage positions with risk controls

**Context Scope**:
- Order management workflows
- Risk limit configurations
- Position tracking logic
- Execution algorithms

**Sub-Agents**:

#### 3.1 Order Management Agent
**File**: `components/execution_layer/agents/order_management_agent.md`

**Responsibilities**:
- Route orders to broker
- Track order status
- Handle order modifications and cancellations
- Implement smart order routing

**Context Requirements**:
```yaml
Required Context:
  - Order lifecycle states
  - Broker API specifications
  - Order routing logic
  - Error handling procedures

Max Context Size: 10K tokens

Key Files to Monitor:
  - components/execution_layer/order_manager/order_router.py
  - components/execution_layer/order_manager/order_tracker.py
  - components/execution_layer/order_manager/order_types.py
```

**Decision Boundaries**:
- Can retry failed orders with exponential backoff
- Can route orders to best execution venue
- Cannot override pre-trade risk checks
- Cannot place orders outside market hours without approval

---

#### 3.2 Position Tracking Agent
**File**: `components/execution_layer/agents/position_tracking_agent.md`

**Responsibilities**:
- Track portfolio positions in real-time
- Calculate unrealized P&L
- Reconcile positions with broker
- Monitor position limits

**Context Requirements**:
```yaml
Required Context:
  - Position calculation methods
  - P&L formulas
  - Reconciliation procedures
  - Position limit definitions

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/execution_layer/position_manager/portfolio.py
  - components/execution_layer/position_manager/position.py
  - components/execution_layer/position_manager/reconciler.py
```

**Decision Boundaries**:
- Can update position calculations in real-time
- Can flag reconciliation discrepancies
- Cannot modify historical position data
- Cannot override position limits

---

#### 3.3 Risk Management Agent
**File**: `components/execution_layer/agents/risk_management_agent.md`

**Responsibilities**:
- Perform pre-trade risk checks
- Monitor portfolio exposure
- Enforce position limits
- Track daily loss limits

**Context Requirements**:
```yaml
Required Context:
  - Risk limit configurations
  - Exposure calculation methods
  - Pre-trade check procedures
  - Circuit breaker logic

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/execution_layer/risk_manager/pre_trade.py
  - components/execution_layer/risk_manager/position_limits.py
  - components/execution_layer/risk_manager/exposure.py
```

**Decision Boundaries**:
- Can reject orders that violate risk limits
- Can trigger circuit breakers
- Cannot relax risk limits without approval
- Cannot allow trades during market closures

---

### 4. Tax & Recon Agent (Subagent 4)

**Location**: `components/tax_recon/agents/`

**Primary Responsibility**: Calculate taxes and reconcile with broker statements

**Context Scope**:
- IRS tax regulations
- Wash sale rules
- Capital gains calculations
- Reconciliation procedures

**Sub-Agents**:

#### 4.1 Tax Lot Agent
**File**: `components/tax_recon/agents/tax_lot_agent.md`

**Responsibilities**:
- Track tax lots for all securities
- Implement FIFO, LIFO, specific ID methods
- Maintain cost basis records
- Update lots for corporate actions

**Context Requirements**:
```yaml
Required Context:
  - Tax lot accounting methods
  - Cost basis calculation rules
  - Corporate action handling
  - IRS Publication 550 guidelines

Max Context Size: 10K tokens

Key Files to Monitor:
  - components/tax_recon/tax_lots/lot_manager.py
  - components/tax_recon/tax_lots/fifo.py
  - components/tax_recon/tax_lots/specific_id.py
```

**Decision Boundaries**:
- Can create and close tax lots
- Can adjust cost basis for wash sales
- Cannot delete tax lot history
- Cannot change accounting method mid-year without approval

---

#### 4.2 Wash Sale Agent
**File**: `components/tax_recon/agents/wash_sale_agent.md`

**Responsibilities**:
- Detect wash sales per IRS rules
- Calculate disallowed losses
- Adjust cost basis for replacement shares
- Generate wash sale reports

**Context Requirements**:
```yaml
Required Context:
  - IRS wash sale rules (Publication 550)
  - 61-day window calculation
  - Substantially identical securities definition
  - Cost basis adjustment procedures

Max Context Size: 12K tokens

Key Files to Monitor:
  - components/tax_recon/wash_sale/detector.py
  - components/tax_recon/wash_sale/rules.py
  - components/tax_recon/wash_sale/adjustment.py
```

**Decision Boundaries**:
- Can detect and flag wash sales
- Can calculate disallowed losses
- Cannot override IRS wash sale determinations
- Cannot modify wash sale detection logic without tax advisor review

---

#### 4.3 Capital Gains Agent
**File**: `components/tax_recon/agents/capital_gains_agent.md`

**Responsibilities**:
- Calculate realized gains and losses
- Classify short-term vs long-term
- Generate IRS Form 8949 data
- Calculate tax liability estimates

**Context Requirements**:
```yaml
Required Context:
  - Capital gains tax rates
  - Short-term vs long-term classification (1-year rule)
  - Form 8949 requirements
  - Schedule D formatting

Max Context Size: 10K tokens

Key Files to Monitor:
  - components/tax_recon/capital_gains/calculator.py
  - components/tax_recon/capital_gains/short_term.py
  - components/tax_recon/capital_gains/long_term.py
```

**Decision Boundaries**:
- Can calculate gains/losses using specified method
- Can generate tax forms
- Cannot modify tax rate tables without approval
- Cannot change gain/loss calculations without validation

---

### 5. Reporting Agent (Subagent 5)

**Location**: `components/reporting/agents/`

**Primary Responsibility**: Generate reports, dashboards, and analytics

**Context Scope**:
- Report templates and formats
- Performance metric calculations
- Dashboard layouts
- Export formats

**Sub-Agents**:

#### 5.1 P&L Calculation Agent
**File**: `components/reporting/agents/pnl_calculation_agent.md`

**Responsibilities**:
- Calculate daily realized P&L
- Calculate unrealized P&L
- Generate P&L statements
- Track P&L by strategy

**Context Requirements**:
```yaml
Required Context:
  - P&L calculation formulas
  - Commission and fee structures
  - Reporting periods and formats
  - Strategy attribution methods

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/reporting/pnl/daily_pnl.py
  - components/reporting/pnl/realized.py
  - components/reporting/pnl/unrealized.py
```

**Decision Boundaries**:
- Can generate P&L reports
- Can attribute P&L to strategies
- Cannot modify P&L calculation formulas without validation
- Cannot backdate P&L calculations

---

#### 5.2 Performance Metrics Agent
**File**: `components/reporting/agents/performance_metrics_agent.md`

**Responsibilities**:
- Calculate Sharpe ratio, Sortino ratio
- Calculate maximum drawdown
- Generate risk-adjusted return metrics
- Perform performance attribution

**Context Requirements**:
```yaml
Required Context:
  - Performance metric formulas
  - Risk-free rate assumptions
  - Benchmark indices
  - Attribution methodologies

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/reporting/performance/returns.py
  - components/reporting/performance/risk_metrics.py
  - components/reporting/performance/attribution.py
```

**Decision Boundaries**:
- Can calculate standard performance metrics
- Can add new metrics
- Cannot change industry-standard metric calculations
- Cannot modify historical performance data

---

#### 5.3 Report Generation Agent
**File**: `components/reporting/agents/report_generation_agent.md`

**Responsibilities**:
- Generate PDF and Excel reports
- Create interactive dashboards
- Export tax reports (Form 8949, Schedule D)
- Send email alerts and notifications

**Context Requirements**:
```yaml
Required Context:
  - Report templates
  - Dashboard layouts
  - Export formats
  - Email notification rules

Max Context Size: 8K tokens

Key Files to Monitor:
  - components/reporting/tax_reports/form_8949.py
  - components/reporting/dashboards/plotly_dash.py
  - components/reporting/dashboards/exports.py
```

**Decision Boundaries**:
- Can generate reports in specified formats
- Can customize report layouts
- Cannot modify tax form formats (must match IRS requirements)
- Cannot send reports to unauthorized recipients

---

## Agent Communication Patterns

### Message Passing

Agents communicate via well-defined message interfaces:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

class MessageType(Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    NOTIFICATION = "NOTIFICATION"
    ERROR = "ERROR"

@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication"""
    message_type: MessageType
    sender_agent: str
    recipient_agent: str
    payload: Dict[str, Any]
    correlation_id: str
    timestamp: datetime
    priority: int = 5  # 1-10, higher is more urgent

# Example: Data Layer Agent requests signal from Strategy Layer Agent
message = AgentMessage(
    message_type=MessageType.REQUEST,
    sender_agent="data_layer.preprocessing_agent",
    recipient_agent="strategy_layer.signal_generation_agent",
    payload={
        "action": "generate_signal",
        "symbol": "AAPL",
        "market_data": {...}
    },
    correlation_id="req-12345",
    timestamp=datetime.utcnow(),
    priority=8
)
```

### Event Bus

Agents subscribe to events they care about:

```python
from typing import Callable

class EventBus:
    """Publish-subscribe event bus for agent communication"""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, event_data: Any):
        """Publish an event to all subscribers"""
        for handler in self.subscribers.get(event_type, []):
            handler(event_data)

# Example: Order execution events
event_bus = EventBus()

# Position Tracking Agent subscribes to order fills
event_bus.subscribe(
    "order.filled",
    position_tracking_agent.handle_order_fill
)

# Order Management Agent publishes fill event
event_bus.publish(
    "order.filled",
    {"order_id": "12345", "symbol": "AAPL", "quantity": 100}
)
```

---

## Agent Deployment

### Development Mode

Each agent runs in the same process during development:

```python
# main.py
from components.data_layer.agents import DataLayerAgent
from components.strategy_layer.agents import StrategyLayerAgent
from components.execution_layer.agents import ExecutionLayerAgent

async def main():
    # Initialize all agents
    data_agent = DataLayerAgent()
    strategy_agent = StrategyLayerAgent()
    execution_agent = ExecutionLayerAgent()

    # Start agent coordination
    await asyncio.gather(
        data_agent.run(),
        strategy_agent.run(),
        execution_agent.run()
    )
```

### Production Mode

Agents can be deployed as separate microservices:

```yaml
# docker-compose-agents.yml
version: '3.8'

services:
  data_layer_agent:
    build: ./components/data_layer
    environment:
      AGENT_NAME: data_layer_agent
      RABBITMQ_URL: amqp://rabbitmq:5672

  strategy_layer_agent:
    build: ./components/strategy_layer
    environment:
      AGENT_NAME: strategy_layer_agent
      RABBITMQ_URL: amqp://rabbitmq:5672

  execution_layer_agent:
    build: ./components/execution_layer
    environment:
      AGENT_NAME: execution_layer_agent
      RABBITMQ_URL: amqp://rabbitmq:5672
```

---

## Context Management

### Context Size Limits

Each agent maintains focused context to avoid token limit issues:

| Agent Type | Max Context Size | Priority Context |
|-----------|------------------|------------------|
| API Client Agent | 8K tokens | API specs, retry logic |
| Data Store Agent | 10K tokens | Schema, queries |
| Preprocessing Agent | 8K tokens | Features, validation |
| Model Training Agent | 12K tokens | Model arch, training |
| Backtesting Agent | 10K tokens | Metrics, optimization |
| Signal Generation Agent | 8K tokens | Signal logic |
| Order Management Agent | 10K tokens | Order workflow |
| Position Tracking Agent | 8K tokens | Position calc |
| Risk Management Agent | 8K tokens | Risk limits |
| Tax Lot Agent | 10K tokens | Tax rules |
| Wash Sale Agent | 12K tokens | IRS regulations |
| Capital Gains Agent | 10K tokens | Tax calculations |
| P&L Agent | 8K tokens | P&L formulas |
| Performance Agent | 8K tokens | Metrics |
| Report Generation Agent | 8K tokens | Templates |

### Context Refresh Strategy

Agents periodically refresh their context to stay current:

```python
class AgentContext:
    """Manage agent context and prevent token overflow"""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.current_context = []
        self.context_version = 0

    def add_to_context(self, item: str, priority: int = 5):
        """Add item to context with priority"""
        self.current_context.append({
            "content": item,
            "priority": priority,
            "added_at": datetime.utcnow()
        })
        self._prune_if_needed()

    def _prune_if_needed(self):
        """Remove low-priority items if context is too large"""
        total_tokens = self._estimate_tokens()
        if total_tokens > self.max_tokens:
            # Sort by priority (descending) and recency
            self.current_context.sort(
                key=lambda x: (x["priority"], x["added_at"]),
                reverse=True
            )
            # Keep only high-priority recent items
            self.current_context = self.current_context[:int(self.max_tokens * 0.8)]
            self.context_version += 1

    def _estimate_tokens(self) -> int:
        """Estimate total tokens in context"""
        # Rough estimate: 1 token ≈ 4 characters
        total_chars = sum(len(item["content"]) for item in self.current_context)
        return total_chars // 4
```

---

## Agent Monitoring & Debugging

### Agent Health Checks

```python
@dataclass
class AgentHealth:
    agent_name: str
    status: str  # "healthy", "degraded", "unhealthy"
    last_activity: datetime
    messages_processed: int
    errors_count: int
    context_size: int
    memory_usage_mb: float

class AgentMonitor:
    """Monitor agent health and performance"""

    async def check_health(self, agent_name: str) -> AgentHealth:
        """Check health of specific agent"""
        pass

    async def get_all_agents_health(self) -> List[AgentHealth]:
        """Get health status of all agents"""
        pass
```

### Logging Standards

All agents follow consistent logging:

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "signal_generated",
    agent="strategy_layer.signal_generation_agent",
    symbol="AAPL",
    signal_type="BUY",
    confidence=0.85,
    timestamp=datetime.utcnow().isoformat()
)
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-15 | Initial agent architecture | System |

---

**Next Review Date**: 2025-11-22
**Document Owner**: Technical Lead
**Approval Status**: Draft - Pending Review
