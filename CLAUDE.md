# CLAUDE.md - AI Trading Bot Project Documentation Index

**Project Name**: AI-Driven Tax and Portfolio Reconciliation System
**Status**: Phase 1 - Research & Planning
**Last Updated**: 2025-11-15
**Current Branch**: claude/split-claude-documentation-01ULcqLsykmmhEkRMCeH4kzC

---

## 📋 Documentation Navigation

This is the main documentation index for the AI Trading Bot project. All project documentation has been organized into focused, purpose-specific files for easier navigation and maintenance.

### Core Documentation

| Document | Purpose | Quick Link |
|----------|---------|------------|
| **[ROADMAP.md](./ROADMAP.md)** | Project phases, milestones, and component structure | [View →](./ROADMAP.md) |
| **[DECISIONS.md](./DECISIONS.md)** | All architectural and technical decisions with rationale | [View →](./DECISIONS.md) |
| **[CHANGES.md](./CHANGES.md)** | Implementation change log with details and testing | [View →](./CHANGES.md) |
| **[RISKS.md](./RISKS.md)** | Risk register with mitigation strategies | [View →](./RISKS.md) |
| **[TESTING.md](./TESTING.md)** | Testing strategy and validation metrics | [View →](./TESTING.md) |

### Technical Documentation

| Document | Purpose | Quick Link |
|----------|---------|------------|
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | System architecture and technical specifications | [View →](./ARCHITECTURE.md) |
| **[AGENTS.md](./AGENTS.md)** | AI agent hierarchy and specifications | [View →](./AGENTS.md) |
| **[README.md](./README.md)** | Project overview and quick start guide | [View →](./README.md) |

---

## 🎯 Project Quick Reference

### Objective
Build an AI-driven quantitative trading bot that:
- Analyzes market data from Interactive Brokers API
- Makes predictions using fine-tuned ML models
- Executes trades automatically with risk management
- Calculates tax liabilities and capital gains
- Generates daily P&L statements with tax implications

### Current Status
**Phase 1: Research & Planning** (60% complete)
- ✅ Architecture documentation completed
- ✅ Agent specifications defined
- ✅ Technology stack finalized
- ✅ Development environment setup guide created
- ⏳ IB API integration testing in progress

**Next Milestone**: Complete IB API connection tests → Begin Phase 2 (Core Development)

---

## 🛠️ Technology Stack

### Core Technologies
- **Language**: Python 3.14.0
- **Dependency Management**: Poetry (pyproject.toml)
- **Trading API**: Interactive Brokers (TWS API / ibapi)
- **Database**: PostgreSQL 15+ with TimescaleDB extension
- **Caching**: Redis 7+
- **Web Framework**: FastAPI with Uvicorn

### Machine Learning
- **Frameworks**: PyTorch (CUDA), TensorFlow (GPU), scikit-learn
- **Models**: Hugging Face Transformers (FinBERT, TimesNet)
- **Strategy**: Fine-tuning pre-trained models (NOT training from scratch)
- **GPU**: NVIDIA RTX 5090 (24GB VRAM) with CUDA 12.x

### Data Processing
- **Libraries**: Pandas, NumPy, Polars
- **Acceleration**: CUDA, cuDNN 8.9+

### Testing & Quality
- **Testing**: pytest, unittest, pytest-asyncio
- **Coverage Target**: 80%+ (95%+ for critical components)
- **Linting**: ruff, black
- **Type Checking**: mypy

---

## 💻 Hardware Environment

Local development machine specifications:

| Component | Specification |
|-----------|--------------|
| **CPU** | AMD Ryzen 7 7700X (8 cores, 16 threads) |
| **GPU** | NVIDIA RTX 5090 Founders Edition (24GB VRAM) |
| **RAM** | 32GB DDR5 |
| **OS** | Windows 11 Pro |
| **CUDA** | 12.x with cuDNN 8.9+ |

---

## 🏗️ System Architecture

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
│              │    │ Layer        │    │ Layer        │
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
└──────────────┘    └──────────────┘    └──────────────┘
```

**For detailed architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 📊 Project Phases

### Phase 1: Research & Planning (Week 1-2) - **IN PROGRESS**
- Finalize architecture design
- Research Interactive Brokers API
- Research US tax regulations
- Set up development environment

### Phase 2: Core Development (Week 3-6)
- Data Infrastructure
- Strategy Development
- Execution Engine
- Tax & Reconciliation
- Reporting System

### Phase 3: Testing & Validation (Week 7-8)
- Unit Testing (80%+ coverage)
- Integration Testing
- Paper Trading Validation (2+ weeks)

### Phase 4: Deployment & Monitoring (Week 9-10)
- Production environment setup
- Go-live strategy
- Monitoring and alerting

**For detailed roadmap**: See [ROADMAP.md](./ROADMAP.md)

---

## 🔑 Key Decisions

Recent architectural and technical decisions:

1. **[DECISION-006]** - Split CLAUDE.md into focused documentation files ✅
2. **[DECISION-005]** - Remove pickle5 dependency (Python 3.14 compatibility) ✅
3. **[DECISION-004]** - Use Poetry for dependency management ✅
4. **[DECISION-003]** - Local development with NVIDIA RTX 5090 ✅
5. **[DECISION-002]** - ML fine-tuning over training from scratch ✅

**For complete decision log**: See [DECISIONS.md](./DECISIONS.md)

---

## 📝 Recent Changes

Latest implementation changes:

1. **[CHANGE-007]** - Split CLAUDE.md into focused documentation files (2025-11-15)
2. **[CHANGE-006]** - Migrate development OS to Windows 11 Pro (2025-11-15)
3. **[CHANGE-005]** - Remove pickle5 dependency (2025-11-15)
4. **[CHANGE-004]** - Poetry configuration and dependency management (2025-11-15)

**For complete change log**: See [CHANGES.md](./CHANGES.md)

---

## ⚠️ Active Risks

High-priority risks currently being monitored:

| Risk | Category | Probability | Impact | Status |
|------|----------|-------------|---------|--------|
| **[RISK-003]** Model Overfitting | Technical | High | Critical | Open |
| **[RISK-001]** IB API Rate Limits | Technical | High | Medium | Open |
| **[RISK-002]** Tax Regulation Complexity | Regulatory | Medium | High | Open |
| **[RISK-004]** Order Execution Failures | Operational | Medium | High | Open |

**For complete risk register**: See [RISKS.md](./RISKS.md)

---

## 🎯 Next Steps

### Immediate Actions (Next 48 Hours)
- [ ] Set up IB Gateway/TWS for testing
- [ ] Run initial IB API connection tests
- [ ] Verify Poetry dependency installation
- [ ] Test GPU/CUDA environment setup

### Week 1 Goals
- [ ] Complete Interactive Brokers API research
- [ ] Finalize technology stack decisions
- [ ] Set up development environment
- [ ] Begin Data Layer component design
- [ ] Create detailed tax regulation compliance checklist

**For detailed roadmap**: See [ROADMAP.md](./ROADMAP.md)

---

## 📚 Component Structure

### Main Components

Each component follows standardized structure:

1. **Data Layer** (`components/data_layer/`)
   - IB API connection wrapper
   - Market data retrieval
   - Data preprocessing
   - Database management

2. **Strategy Layer** (`components/strategy_layer/`)
   - ML model fine-tuning and inference
   - Trading signal generation
   - Backtesting framework
   - Performance evaluation

3. **Execution Layer** (`components/execution_layer/`)
   - Order management system
   - Position tracking
   - Risk management
   - Trade execution logic

4. **Tax & Reconciliation** (`components/tax_recon/`)
   - Wash-sale detection
   - Capital gains calculation
   - Tax lot tracking
   - Broker reconciliation

5. **Reporting Engine** (`components/reporting/`)
   - Daily P&L calculation
   - Tax liability reports
   - Portfolio analytics
   - Performance metrics

**For detailed component specifications**: See [ROADMAP.md](./ROADMAP.md)

---

## 🧪 Testing Strategy

### Testing Pyramid
- **Unit Tests**: 80%+ coverage, run on every commit
- **Integration Tests**: End-to-end workflows, run daily
- **Paper Trading**: 2+ weeks validation in IB paper trading environment

### Key Validation Metrics
- **Trading Performance**: Sharpe Ratio > 1.5, Max Drawdown < 15%
- **System Performance**: API response < 500ms, Uptime > 99%
- **Tax Accuracy**: 100% wash-sale detection, 99.9%+ capital gains accuracy

**For complete testing strategy**: See [TESTING.md](./TESTING.md)

---

## 📖 Related Documentation

### Component Documentation
Each component has its own README.md:
- `components/data_layer/README.md`
- `components/strategy_layer/README.md`
- `components/execution_layer/README.md`
- `components/tax_recon/README.md`
- `components/reporting/README.md`

### Research Documentation
- `docs/IB_API_INTEGRATION_RESEARCH.md` - IB API integration guide
- `docs/QUICK_START_IB_RESEARCH.md` - Quick start guide for IB API testing

### Configuration Files
- `pyproject.toml` - Poetry dependency configuration
- `requirements.txt` - Fallback pip dependencies
- `.env.example` - Environment variable template

---

## 📚 Appendix

### Quick Links

**External Resources**:
- [Interactive Brokers API Documentation](https://interactivebrokers.github.io/)
- [IRS Tax Guidelines](https://www.irs.gov/)
- [Hugging Face Model Hub](https://huggingface.co/models)
- [PyTorch Documentation](https://pytorch.org/docs/)

**Internal Documentation**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture
- [AGENTS.md](./AGENTS.md) - AI agent specifications
- [README.md](./README.md) - Project overview and quick start

### Glossary

| Term | Definition |
|------|------------|
| **Wash Sale** | IRS rule preventing tax deduction on securities sold at a loss and repurchased within 30 days |
| **Capital Gains** | Profit from sale of securities (short-term < 1 year, long-term ≥ 1 year) |
| **Tax Lot** | Specific purchase of securities for tax tracking purposes |
| **FIFO** | First In First Out - tax lot accounting method |
| **Sharpe Ratio** | Risk-adjusted return metric (return / volatility) |
| **Drawdown** | Peak-to-trough decline in portfolio value |
| **Slippage** | Difference between expected and actual execution price |

---

## 📞 Contact & Support

### Project Team
- **Project Lead**: [TBD]
- **Technical Lead**: [TBD]
- **Tax Advisor**: [TBD]

### Documentation Guidelines

**When to Update Each Document**:

| Document | Update When |
|----------|-------------|
| CLAUDE.md | Project status changes, quick reference updates |
| ROADMAP.md | Phase completion, milestone changes, timeline updates |
| DECISIONS.md | Major architectural or technical decisions |
| CHANGES.md | Implementation changes, features, bugfixes |
| RISKS.md | New risks identified, risk status changes |
| TESTING.md | Testing strategy changes, new test requirements |

**Documentation Sync**:
- Update "Last Updated" dates when making changes
- Maintain cross-references between related sections
- Review all documentation monthly for accuracy
- Update README.md for project-wide changes

---

**Document Version**: 2.0 (Restructured)
**Last Updated**: 2025-11-15
**Next Review**: 2025-11-22

---

## 🗂️ Documentation History

### Version 2.0 (2025-11-15)
- Restructured CLAUDE.md as documentation index
- Split into focused files: DECISIONS.md, CHANGES.md, RISKS.md, ROADMAP.md, TESTING.md
- Added navigation table and quick reference sections
- Improved documentation organization and maintainability

### Version 1.0 (2025-11-15)
- Initial CLAUDE.md with all sections in single file
- Comprehensive project memory and planning
- Architecture, decisions, changes, and risks combined
