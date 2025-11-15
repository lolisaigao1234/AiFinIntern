# CLAUDE.md - AI-Driven Quant Trading Bot Memory File

**Project Name**: AI-Driven Tax and Portfolio Reconciliation System
**Status**: Planning Phase
**Last Updated**: 2025-11-15
**Current Branch**: claude/init-claude-md-01U7Gzme2rYKkN2M3dEyFUAj

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Project Phases](#project-phases)
4. [Component Structure](#component-structure)
5. [Testing & Validation Strategy](#testing--validation-strategy)
6. [Decision Log](#decision-log)
7. [Change Log](#change-log)
8. [Risk Register](#risk-register)
9. [Related Documentation](#related-documentation)

---

## Project Overview

### Objective
Build an AI-driven quantitative trading bot that:
- **Analyzes market data** from Interactive Brokers API
- **Makes predictions** using machine learning models
- **Executes trades automatically** with risk management
- **Simulates broker operations** for tax and portfolio reconciliation
- **Calculates tax liabilities**, capital gains, and wash-sale implications
- **Generates daily statements** for trade P&L and tax entries
- **Learns and adapts** strategies from historical data

### Key Features
1. Real-time market data retrieval via Interactive Brokers API
2. ML-based prediction engine for trade signals
3. Automated trade execution with risk controls
4. Tax reconciliation system (US tax guidelines)
5. Portfolio performance tracking and reporting
6. Wash-sale detection and capital gains calculation
7. Daily P&L statements with tax implications

### Technology Stack
- **Language**: Python 3.14.0
- **Dependency Management**: Poetry (with pyproject.toml)
- **Trading API**: Interactive Brokers (TWS API / ibapi)
- **Data Processing**: Pandas, NumPy, Polars
- **Machine Learning**: PyTorch (CUDA), TensorFlow (GPU), scikit-learn, XGBoost
- **ML Models**: Hugging Face Transformers (FinBERT, TimesNet, etc.)
- **GPU Acceleration**: CUDA 12.x, cuDNN 8.9+, NVIDIA RTX 5090 (24GB VRAM)
- **Database**: PostgreSQL 15+ with TimescaleDB extension
- **Caching**: Redis 7+
- **Web Framework**: FastAPI with Uvicorn
- **AI Assistance**: ChatGPT/Claude for tax interpretation
- **Testing**: pytest, unittest, pytest-asyncio

### Hardware Environment (Local Development)
- **CPU**: AMD Ryzen 7 7700X (8 cores, 16 threads)
- **GPU**: NVIDIA RTX 5090 Founders Edition (24GB VRAM)
- **RAM**: 32GB DDR5
- **OS**: Linux (Ubuntu 22.04+)
- **CUDA**: 12.x with cuDNN 8.9+

### ML Development Strategy
- **Approach**: Fine-tuning pre-trained models (NOT training from scratch)
- **Model Source**: Hugging Face Model Hub and other open-source platforms
- **Fine-tuning Focus**: Financial sentiment, time series forecasting, pattern recognition
- **GPU Utilization**: Maximum leverage of CUDA, PyTorch, and TensorFlow capabilities

### Existing Files
- `Code/order.py` - Interactive Brokers API trading logic tests
- `Code/test.py` - Trading logic validation
- `Code/main.py` - Core trading bot logic (to be developed)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AI Trading Bot System                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Data Layer   │    │ Strategy     │    │ Execution    │
│ (Subagent 1) │    │ Layer        │    │ Layer        │
│              │    │ (Subagent 2) │    │ (Subagent 3) │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│         Interactive Brokers API Interface            │
└──────────────────────────────────────────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Tax & Recon  │    │ Reporting    │    │ Monitoring   │
│ Engine       │    │ Engine       │    │ & Logging    │
│ (Subagent 4) │    │ (Subagent 5) │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Component Breakdown

#### 1. Data Layer (Subagent 1)
**Responsibility**: Data retrieval, preprocessing, and storage
- Market data ingestion from IB API
- Historical data management
- Data normalization and feature engineering
- Database management

#### 2. Strategy Layer (Subagent 2)
**Responsibility**: Trading strategy and ML model development
- ML model training and prediction
- Signal generation
- Strategy backtesting
- Model performance evaluation

#### 3. Execution Layer (Subagent 3)
**Responsibility**: Trade execution and order management
- Order placement via IB API
- Position management
- Risk management and position sizing
- Order status tracking

#### 4. Tax & Reconciliation Engine (Subagent 4)
**Responsibility**: Tax calculation and compliance
- Wash-sale detection algorithm
- Capital gains/losses calculation
- Tax lot tracking (FIFO, LIFO, specific identification)
- Reconciliation with broker statements

#### 5. Reporting Engine (Subagent 5)
**Responsibility**: Performance tracking and reporting
- Daily P&L generation
- Tax liability reports
- Portfolio analytics
- Performance metrics (Sharpe, max drawdown, etc.)

---

## Project Phases

### Phase 1: Research & Planning (Week 1-2)
**Status**: In Progress

#### Objectives
- [ ] Finalize architecture design
- [ ] Research Interactive Brokers API capabilities
- [ ] Research US tax regulations (wash sales, capital gains)
- [ ] Define data requirements and sources
- [ ] Select ML models for strategy development
- [ ] Set up development environment

#### Deliverables
- Architecture documentation (this file)
- API research findings
- Tax regulation compliance checklist
- Development environment setup guide

---

### Phase 2: Core Development (Week 3-6)

#### Stage 2.1: Data Infrastructure
**Directory**: `components/data_layer/`

**Tasks**:
- [ ] Implement IB API connection wrapper
- [ ] Build data retrieval module
- [ ] Create database schema
- [ ] Develop data preprocessing pipeline
- [ ] Implement data validation

**Expected Outcome**: Reliable data pipeline from IB API to database

**Risks**:
- API rate limits
- Data quality issues
- Connection stability

---

#### Stage 2.2: Strategy Development
**Directory**: `components/strategy_layer/`

**Tasks**:
- [ ] Implement backtesting framework
- [ ] Develop baseline trading strategies
- [ ] Build ML prediction models
- [ ] Create signal generation logic
- [ ] Implement strategy evaluation metrics

**Expected Outcome**: Validated trading strategies with positive backtest results

**Risks**:
- Overfitting to historical data
- Market regime changes
- Transaction cost impact

---

#### Stage 2.3: Execution Engine
**Directory**: `components/execution_layer/`

**Tasks**:
- [ ] Build order management system
- [ ] Implement risk management rules
- [ ] Create position tracking
- [ ] Develop order execution logic
- [ ] Add error handling and retry mechanisms

**Expected Outcome**: Robust execution system with risk controls

**Risks**:
- Order rejection
- Slippage
- Execution delays

---

#### Stage 2.4: Tax & Reconciliation
**Directory**: `components/tax_recon/`

**Tasks**:
- [ ] Implement wash-sale detection
- [ ] Build capital gains calculator
- [ ] Create tax lot tracking system
- [ ] Develop reconciliation engine
- [ ] Integrate with US tax guidelines

**Expected Outcome**: Automated tax calculation and compliance reporting

**Risks**:
- Complex tax rule interpretation
- Regulatory changes
- Calculation errors

---

#### Stage 2.5: Reporting System
**Directory**: `components/reporting/`

**Tasks**:
- [ ] Build daily P&L calculator
- [ ] Create portfolio analytics dashboard
- [ ] Implement performance metrics
- [ ] Develop tax report generation
- [ ] Add alerting system

**Expected Outcome**: Comprehensive reporting and monitoring system

**Risks**:
- Performance bottlenecks
- Report accuracy

---

### Phase 3: Testing & Validation (Week 7-8)

#### Unit Testing
**Directory**: `tests/unit/`

**Coverage Areas**:
- Data retrieval and preprocessing
- Strategy logic and ML models
- Order execution logic
- Tax calculations
- Reporting functions

**Target**: 80%+ code coverage

---

#### Integration Testing
**Directory**: `tests/integration/`

**Test Scenarios**:
- End-to-end trade flow
- Data pipeline integration
- Tax reconciliation workflow
- Error handling and recovery
- API connection resilience

---

#### Paper Trading Validation
**Directory**: `tests/paper_trading/`

**Validation Steps**:
- [ ] Run bot in paper trading mode
- [ ] Monitor for 2+ weeks
- [ ] Compare predictions vs. actuals
- [ ] Validate tax calculations
- [ ] Assess risk management effectiveness

**Success Criteria**:
- No critical errors
- Positive risk-adjusted returns
- Accurate tax reporting
- Proper risk controls

---

### Phase 4: Deployment & Monitoring (Week 9-10)

#### Deployment Preparation
- [ ] Set up production environment
- [ ] Configure monitoring and alerting
- [ ] Implement backup and recovery
- [ ] Create runbooks and documentation
- [ ] Conduct security audit

#### Go-Live Strategy
- [ ] Start with minimal capital allocation
- [ ] Gradual position size increase
- [ ] Daily performance review
- [ ] Weekly strategy adjustment
- [ ] Monthly comprehensive audit

---

## Component Structure

Each component follows this standard structure:

```
components/
├── [component_name]/
│   ├── README.md              # Component overview and purpose
│   ├── DESIGN.md              # Detailed design decisions
│   ├── src/                   # Source code
│   │   ├── __init__.py
│   │   ├── [module].py
│   │   └── utils/
│   ├── tests/                 # Component-specific tests
│   │   ├── test_[module].py
│   │   └── fixtures/
│   ├── docs/                  # Additional documentation
│   │   └── api_reference.md
│   └── config/                # Configuration files
│       └── config.yaml
```

---

## Testing & Validation Strategy

### Testing Pyramid

```
                    ┌─────────────┐
                    │   Manual    │
                    │   Testing   │
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

### Unit Test Requirements
- **Coverage Target**: 80%+
- **Tools**: pytest, unittest, mock
- **Run Frequency**: On every commit
- **Test Cases**:
  - Happy path scenarios
  - Edge cases
  - Error conditions
  - Boundary values

### Integration Test Requirements
- **Scope**: Component interactions
- **Environment**: Staging with paper trading
- **Run Frequency**: Daily
- **Test Scenarios**:
  - Complete trade lifecycle
  - Data pipeline end-to-end
  - Tax calculation workflow
  - Report generation

### Validation Metrics
1. **Trading Performance**:
   - Sharpe Ratio > 1.5
   - Max Drawdown < 15%
   - Win Rate > 55%
   - Profit Factor > 1.3

2. **System Performance**:
   - API response time < 500ms
   - Order execution latency < 2s
   - Data refresh rate: real-time
   - System uptime > 99%

3. **Tax Accuracy**:
   - 100% wash-sale detection
   - Capital gains calculation accuracy: 99.9%+
   - Reconciliation match rate: 100%

---

## Decision Log

### Decision Template
```markdown
### [DECISION-XXX] - Decision Title
**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Rejected | Superseded
**Decider**: [Name/Role]

#### Context
[What is the situation and problem statement?]

#### Options Considered
1. Option A - [brief description]
2. Option B - [brief description]
3. Option C - [brief description]

#### Decision
[What option was chosen and why?]

#### Consequences
**Positive**:
- [Benefit 1]
- [Benefit 2]

**Negative**:
- [Risk/Trade-off 1]
- [Risk/Trade-off 2]

#### Implementation Notes
[Any specific guidance for implementing this decision]
```

---

### [DECISION-001] - CLAUDE.md as Main Memory File
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need a centralized documentation system to track all decisions, changes, and project evolution for the AI trading bot.

#### Options Considered
1. Multiple separate documentation files
2. Wiki-based documentation
3. Single CLAUDE.md memory file

#### Decision
Use CLAUDE.md as the single source of truth for project memory, decisions, and architecture.

#### Consequences
**Positive**:
- Single file for quick reference
- Easy to track project evolution
- Clear audit trail
- Better version control

**Negative**:
- File may become large over time
- Need discipline to keep updated
- May need to split later if too large

#### Implementation Notes
- Update CLAUDE.md for every significant change
- Include reasoning, expected outcomes, and risks
- Review and refactor structure as needed

---

### [DECISION-002] - ML Fine-Tuning Over Training From Scratch
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need to decide whether to train ML models from scratch or fine-tune existing pre-trained models for trading signal generation and financial analysis.

#### Options Considered
1. Train models from scratch - Full control but resource intensive
2. Fine-tune pre-trained models - Leverage existing research, faster development
3. Hybrid approach - Mix of both strategies

#### Decision
Focus on **fine-tuning pre-trained models** from Hugging Face and other open-source platforms rather than training from scratch.

#### Consequences
**Positive**:
- Significantly reduced training time and computational costs
- Leverage state-of-the-art architectures from research community
- Better performance with limited financial data (transfer learning)
- Access to specialized financial models (FinBERT, etc.)
- Faster iteration and experimentation
- Lower barrier to entry for ML development

**Negative**:
- Less flexibility in model architecture design
- Dependency on external model repositories
- May need to adapt models that weren't designed for trading
- Potential licensing considerations for commercial use

#### Implementation Notes
- Prioritize financial-specific models (FinBERT, financial sentiment analyzers)
- Use Hugging Face Transformers library as primary framework
- Implement fine-tuning pipeline with PyTorch/TensorFlow
- Leverage local GPU (RTX 5090) for efficient fine-tuning
- Document all pre-trained models used and their licenses

---

### [DECISION-003] - Local Development with NVIDIA RTX 5090
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need to optimize development environment for ML model fine-tuning and training with available hardware: AMD R7-7700X CPU, NVIDIA RTX 5090 FE GPU (24GB VRAM), 32GB RAM.

#### Options Considered
1. Cloud-based GPU training (AWS, GCP, Azure)
2. Local GPU development with RTX 5090
3. Hybrid approach (local dev, cloud for large-scale training)

#### Decision
Optimize for **local development using NVIDIA RTX 5090** with full CUDA, PyTorch, and TensorFlow GPU acceleration.

#### Consequences
**Positive**:
- Zero cloud compute costs during development
- Full control over environment and dependencies
- 24GB VRAM sufficient for fine-tuning large models
- Low latency for iterative development
- No data transfer costs or privacy concerns
- Can utilize all 8 CPU cores for data preprocessing

**Negative**:
- Limited to single GPU (no multi-GPU training)
- 32GB system RAM may limit very large dataset operations
- Electricity costs for GPU usage
- Cannot scale beyond local hardware limits
- Need to maintain CUDA/driver compatibility

#### Implementation Notes
- Install CUDA 12.x with cuDNN 8.9+ for optimal RTX 5090 performance
- Configure PyTorch with CUDA backend (cu121)
- Enable mixed precision training (FP16) for faster training
- Use gradient checkpointing for memory-intensive models
- Monitor GPU temperature and utilization
- Consider cloud deployment for production inference at scale

---

### [DECISION-004] - Poetry for Dependency Management
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need a robust, modern dependency management solution for Python 3.14.0 project with complex dependencies including CUDA-enabled ML frameworks, multiple package sources (PyPI, PyTorch repos), and development/production separation.

#### Options Considered
1. pip with requirements.txt - Traditional approach, simple but limited
2. Poetry - Modern dependency management with lock files
3. Pipenv - Alternative to Poetry, less actively maintained
4. Conda - Heavy, primarily for data science, complex with pip packages

#### Decision
Use **Poetry** as the primary dependency management tool with pyproject.toml configuration.

#### Consequences
**Positive**:
- Deterministic builds with poetry.lock file
- Clear separation of development and production dependencies
- Better dependency resolution and conflict detection
- Modern pyproject.toml standard (PEP 518)
- Built-in virtual environment management
- Support for private package repositories
- Easier version management and updates
- Optional dependency groups (jupyter, cuda extras)
- Integration with modern Python tooling (black, ruff, mypy)

**Negative**:
- Additional tool to learn for team members
- Slightly slower than pure pip installations
- Some edge cases with CUDA packages require pip fallback
- Poetry lock file adds repository size
- May need pip for some specialized packages (PyTorch CUDA wheels)

#### Implementation Notes
- Create comprehensive pyproject.toml with all dependencies
- Use poetry extras for optional dependencies (cuda, jupyter)
- Configure PyTorch CUDA installation as separate pip step
- Set up dependency groups: main, dev, jupyter
- Configure all tooling (black, ruff, mypy, pytest) in pyproject.toml
- Keep requirements.txt as fallback for pip-only environments
- Document Poetry installation and usage in README.md
- Use poetry.lock for reproducible builds (commit to repository)

---

## Change Log

### Change Template
```markdown
### [CHANGE-XXX] - Change Title
**Date**: YYYY-MM-DD
**Component**: [Component Name]
**Type**: Feature | Bugfix | Refactor | Documentation | Performance

#### Reasoning
[Why was this change needed?]

#### Expected Outcome
[What should happen after this change?]

#### Implementation Details
- [Detail 1]
- [Detail 2]

#### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

#### Risks & Challenges
[Any potential issues or challenges encountered]

#### Rollback Plan
[How to revert this change if needed]
```

---

### [CHANGE-001] - Initial Project Setup
**Date**: 2025-11-15
**Component**: Project Root
**Type**: Documentation

#### Reasoning
Initialize CLAUDE.md to establish project structure, architecture, and planning framework.

#### Expected Outcome
- Clear project roadmap
- Documented architecture
- Testing strategy defined
- Component structure established

#### Implementation Details
- Created CLAUDE.md with comprehensive sections
- Defined 5 main subagents for work delegation
- Outlined 4-phase development approach
- Established testing and validation framework

#### Testing
- [x] Documentation review
- [ ] Stakeholder approval pending

#### Risks & Challenges
- Architecture may need refinement as development progresses
- Subagent delegation boundaries may need adjustment
- Phase timelines are estimates

#### Rollback Plan
N/A - Initial setup

---

### [CHANGE-002] - Architecture and Agent Documentation
**Date**: 2025-11-15
**Component**: Project Root / All Components
**Type**: Documentation

#### Reasoning
Comprehensive technical architecture and agent specifications needed to guide development and avoid context overflow during AI-assisted development.

#### Expected Outcome
- Complete technical blueprint for implementation
- Clear agent responsibilities and boundaries
- Structured directory layout matching architecture
- Prevention of context overflow issues during development

#### Implementation Details
- Created ARCHITECTURE.md with detailed technical specifications
  - Database schema design (PostgreSQL + TimescaleDB)
  - API specifications using FastAPI
  - Class diagrams and data models
  - Security and deployment architecture
  - Performance targets and optimization strategies
- Created AGENTS.md with agent hierarchy
  - 5 main agents with 15 sub-agents total
  - Context size limits for each agent (8K-12K tokens)
  - Agent communication patterns (message passing, event bus)
  - Decision boundaries for autonomous operation
- Created full directory structure:
  - `components/` with 5 main layers (data, strategy, execution, tax_recon, reporting)
  - `agents/` subdirectories in each component
  - `tests/` structure (unit, integration, paper_trading)
  - `config/`, `docs/`, `logs/`, `data/` directories
- Created README.md for each component documenting purpose and responsibilities
- Added __init__.py files to create proper Python package structure
- Updated CLAUDE.md with cross-references to new documentation

#### Testing
- [x] Documentation structure review
- [x] Directory structure validation
- [ ] Stakeholder review of architecture
- [ ] Agent specification validation

#### Risks & Challenges
- Architecture may need refinement during implementation
- Agent context limits may need adjustment based on real usage
- Directory structure may evolve as implementation progresses
- Need to keep all documentation synchronized

#### Rollback Plan
Can revert to simpler structure if needed, but architecture provides valuable blueprint for implementation.

---

### [CHANGE-003] - Local Development Setup and ML Fine-Tuning Specifications
**Date**: 2025-11-15
**Component**: Project Root / All Documentation
**Type**: Documentation

#### Reasoning
Need to document local development hardware specifications, ML fine-tuning approach (vs training from scratch), and GPU optimization strategies to guide efficient development and ensure proper environment setup.

#### Expected Outcome
- Clear hardware requirements documented (AMD R7-7700X, RTX 5090, 32GB RAM)
- ML development approach defined (fine-tuning pre-trained models)
- CUDA/PyTorch/TensorFlow GPU optimization strategies specified
- Comprehensive local setup guide for developers
- Updated Python version to 3.14.0 across all documentation

#### Implementation Details
- Updated README.md with:
  - New "Local Development Setup" section
  - Hardware specifications table
  - ML fine-tuning philosophy and approach
  - Recommended pre-trained models from Hugging Face
  - GPU optimization strategies for PyTorch and TensorFlow
  - CUDA/cuDNN installation instructions
  - Fine-tuning workflow examples
  - Performance benchmarks for RTX 5090
  - Memory management tips
  - Troubleshooting guide
- Updated CLAUDE.md with:
  - Technology stack including GPU specifications
  - Hardware environment section
  - ML development strategy
  - Two new decisions (DECISION-002, DECISION-003)
  - This change log entry
- Updated Python version from 3.11+ to 3.14.0 throughout documentation
- Added CUDA badge to README.md
- Updated Machine Learning section with fine-tuning focus

#### Testing
- [x] Documentation review
- [ ] Hardware specifications validation
- [ ] GPU setup testing
- [ ] Fine-tuning workflow validation
- [ ] Requirements file updates pending

#### Risks & Challenges
- RTX 5090 may have evolving driver/CUDA support requirements
- Python 3.14.0 is very recent, may have limited library support initially
- Some Hugging Face models may require modifications for financial data
- 24GB VRAM may limit certain very large model fine-tuning
- Need to maintain CUDA version compatibility across PyTorch/TensorFlow

#### Rollback Plan
Can revert to cloud-based GPU training if local setup proves problematic. Documentation changes can be reverted via git.

---

### [CHANGE-004] - Poetry Configuration and Dependency Management
**Date**: 2025-11-15
**Component**: Project Root / Configuration
**Type**: Feature

#### Reasoning
Need modern dependency management with deterministic builds, better dependency resolution, and clear separation between development and production dependencies. Traditional requirements.txt approach lacks lock file support and proper dependency group management.

#### Expected Outcome
- Reproducible builds across all development environments
- Simplified dependency installation and management
- Better tooling integration (black, ruff, mypy, pytest)
- Clear documentation for new developers
- Optional dependency groups for CUDA and Jupyter

#### Implementation Details
- Created comprehensive `pyproject.toml` with:
  - All production dependencies from requirements.txt
  - Separated development dependencies (testing, linting, profiling)
  - Optional dependency groups (cuda, jupyter)
  - Complete tool configuration (black, ruff, mypy, pytest, isort, coverage)
  - PyTorch CUDA repository configuration
  - Project metadata and entry points
- Updated README.md with:
  - Poetry installation instructions
  - Step-by-step dependency installation guide
  - Poetry command examples for testing, formatting, linting
  - GPU verification commands
  - Dependency management workflows
  - Added Poetry badge to README
- Updated CLAUDE.md with:
  - New decision (DECISION-004) documenting Poetry adoption
  - This change log entry (CHANGE-004)
- Preserved requirements.txt as fallback for pip-only environments
- Configured Poetry extras:
  - `cuda` - PyTorch with CUDA support
  - `jupyter` - Jupyter notebook environment
  - `all` - All optional dependencies

#### Testing
- [ ] Poetry install verification
- [ ] Dependency resolution testing
- [ ] CUDA package installation testing
- [ ] Tool configuration validation (black, ruff, mypy)
- [ ] Virtual environment creation
- [ ] Lock file generation

#### Risks & Challenges
- Poetry may have issues with PyTorch CUDA wheels (requires pip fallback)
- Team members need to learn Poetry commands
- Some CI/CD pipelines may need updating
- poetry.lock file increases repository size
- Python 3.14.0 is very new, may have limited Poetry compatibility testing

#### Rollback Plan
Can revert to pure requirements.txt approach by:
1. Remove pyproject.toml
2. Revert README.md changes
3. Use traditional venv + pip install -r requirements.txt

---

## Risk Register

### Risk Template
```markdown
### [RISK-XXX] - Risk Title
**Identified**: YYYY-MM-DD
**Category**: Technical | Regulatory | Market | Operational
**Probability**: Low | Medium | High
**Impact**: Low | Medium | High | Critical
**Status**: Open | Mitigated | Closed

#### Description
[What is the risk?]

#### Mitigation Strategy
[How are we addressing this risk?]

#### Contingency Plan
[What's the backup plan if mitigation fails?]

#### Owner
[Who is responsible for monitoring this risk?]
```

---

### [RISK-001] - Interactive Brokers API Rate Limits
**Identified**: 2025-11-15
**Category**: Technical
**Probability**: High
**Impact**: Medium
**Status**: Open

#### Description
IB API has rate limits that could throttle data retrieval and order execution, impacting bot performance.

#### Mitigation Strategy
- Implement request queuing system
- Cache frequently accessed data
- Use market data subscriptions efficiently
- Monitor API usage metrics

#### Contingency Plan
- Reduce data polling frequency
- Implement circuit breakers
- Fall back to delayed data if needed

#### Owner
Data Layer Subagent Team

---

### [RISK-002] - US Tax Regulation Complexity
**Identified**: 2025-11-15
**Category**: Regulatory
**Probability**: Medium
**Impact**: High
**Status**: Open

#### Description
US tax regulations (wash sales, capital gains) are complex and may be misinterpreted, leading to incorrect calculations.

#### Mitigation Strategy
- Use AI (ChatGPT/Claude) to interpret regulations
- Cross-reference with official IRS publications
- Implement comprehensive test cases
- Consider tax professional consultation
- Build audit trail for all calculations

#### Contingency Plan
- Manual review of tax calculations
- Professional tax audit before filing
- Conservative interpretation of ambiguous rules

#### Owner
Tax & Reconciliation Subagent Team

---

### [RISK-003] - Model Overfitting
**Identified**: 2025-11-15
**Category**: Technical
**Probability**: High
**Impact**: Critical
**Status**: Open

#### Description
ML models may overfit to historical data and perform poorly in live trading, leading to losses.

#### Mitigation Strategy
- Use robust cross-validation
- Implement walk-forward optimization
- Monitor out-of-sample performance
- Regular model retraining
- Ensemble methods
- Conservative position sizing initially

#### Contingency Plan
- Immediately halt trading if metrics degrade
- Fall back to simpler rule-based strategies
- Manual intervention protocols
- Reduce position sizes

#### Owner
Strategy Layer Subagent Team

---

### [RISK-004] - Order Execution Failures
**Identified**: 2025-11-15
**Category**: Operational
**Probability**: Medium
**Impact**: High
**Status**: Open

#### Description
Orders may be rejected, experience slippage, or fail to execute, impacting strategy performance.

#### Mitigation Strategy
- Implement robust error handling
- Retry mechanisms with exponential backoff
- Order status monitoring
- Pre-trade validation checks
- Market hours verification

#### Contingency Plan
- Manual order placement procedures
- Alert system for failed orders
- Position reconciliation checks
- Emergency stop-loss orders

#### Owner
Execution Layer Subagent Team

---

## Related Documentation

### Core Documentation Files

This project maintains several interconnected documentation files:

#### 1. CLAUDE.md (This File)
**Purpose**: Main project memory file tracking decisions, changes, and progress
- Project overview and objectives
- Development phases and milestones
- Decision log with rationale
- Change log with implementation details
- Risk register and mitigation strategies

#### 2. ARCHITECTURE.md
**Purpose**: Technical architecture specification
- Detailed system architecture and component design
- Database schema definitions
- API specifications and interfaces
- Class diagrams and data models
- Technology stack details
- Security and deployment architecture

**Link**: See [ARCHITECTURE.md](./ARCHITECTURE.md)

#### 3. AGENTS.md
**Purpose**: AI agent configuration and management
- Agent hierarchy and responsibilities
- Sub-agent specifications for each component
- Context management strategies (to avoid token limits)
- Agent communication patterns
- Deployment and monitoring guidelines

**Link**: See [AGENTS.md](./AGENTS.md)

#### 4. README.md
**Purpose**: Project introduction and quick start guide
- Project overview for new developers
- Installation and setup instructions
- Quick start guide
- Contributing guidelines

**Link**: See [README.md](./README.md)

### Component Documentation

Each component has its own README.md:
- `components/data_layer/README.md` - Data layer overview
- `components/strategy_layer/README.md` - Strategy layer overview
- `components/execution_layer/README.md` - Execution layer overview
- `components/tax_recon/README.md` - Tax & reconciliation overview
- `components/reporting/README.md` - Reporting engine overview

### Agent-Specific Documentation

Each agent subdirectory contains focused documentation:
- `components/*/agents/*.md` - Individual agent specifications
- Context limits and scope definitions
- Decision boundaries and responsibilities

### Documentation Update Guidelines

**When to Update Each File**:

| File | Update When |
|------|-------------|
| CLAUDE.md | Major decisions, phase completion, risks identified |
| ARCHITECTURE.md | Technical design changes, new components, API changes |
| AGENTS.md | New agents added, context limits adjusted, communication patterns changed |
| README.md | Setup process changes, new features added |
| Component READMEs | Component responsibilities change, new sub-components added |

**Documentation Sync**:
- All documentation files reference the same project version
- Cross-reference related sections between files
- Update Last Modified dates when making changes
- Review all documentation monthly for accuracy

---

## Next Steps

### Immediate Actions (Next 48 Hours)
1. [x] Review and approve CLAUDE.md structure
2. [x] Set up project directory structure
3. [x] Create component subdirectories with README templates
4. [x] Create ARCHITECTURE.md with technical specifications
5. [x] Create AGENTS.md with agent hierarchy and specifications
6. [x] Configure Poetry for dependency management
7. [x] Review existing Code/order.py and Code/test.py
8. [x] Document current IB API integration status
9. [x] Create IB API Integration Research Guide
10. [x] Create IB API research directory structure
11. [x] Define API Client Research Agent specification
12. [ ] Set up IB Gateway/TWS for testing
13. [ ] Run initial IB API connection tests

### Week 1 Goals
1. [ ] Complete Interactive Brokers API research
2. [ ] Finalize technology stack decisions
3. [ ] Set up development environment
4. [ ] Begin Data Layer component design
5. [ ] Create detailed tax regulation compliance checklist

### Success Criteria for Phase 1
- [ ] All architecture decisions documented
- [ ] Development environment operational
- [ ] IB API connection tested and validated
- [ ] Team aligned on approach and timeline
- [ ] Risk mitigation strategies in place

---

## Appendix

### References
- Interactive Brokers API Documentation: https://interactivebrokers.github.io/
- IRS Tax Guidelines: https://www.irs.gov/
- Python Trading Libraries: pandas, numpy, scikit-learn
- Testing Frameworks: pytest documentation

### Glossary
- **Wash Sale**: IRS rule preventing tax deduction on securities sold at a loss and repurchased within 30 days
- **Capital Gains**: Profit from sale of securities
- **Tax Lot**: Specific purchase of securities for tax tracking
- **FIFO**: First In First Out (tax lot accounting method)
- **Sharpe Ratio**: Risk-adjusted return metric
- **Drawdown**: Peak-to-trough decline in portfolio value
- **Slippage**: Difference between expected and actual execution price

### Contact & Support
- **Project Lead**: [TBD]
- **Technical Lead**: [TBD]
- **Tax Advisor**: [TBD]

---

**Document Version**: 1.0
**Last Review**: 2025-11-15
**Next Review**: 2025-11-22
