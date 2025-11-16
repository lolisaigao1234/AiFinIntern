# AI-Driven Quantitative Trading Bot

An intelligent, automated trading system that combines machine learning, algorithmic trading, and comprehensive tax reconciliation for the US market.

[![Python Version](https://img.shields.io/badge/python-3.14.0-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CUDA](https://img.shields.io/badge/CUDA-Enabled-green.svg)](https://developer.nvidia.com/cuda-toolkit)

---

## Overview

This project implements a sophisticated quantitative trading bot that:

- **Analyzes Markets**: Real-time data ingestion from Interactive Brokers API
- **Predicts Movements**: ML-based prediction engine using LSTM, Random Forest, and ensemble methods
- **Executes Trades**: Automated order execution with comprehensive risk management
- **Calculates Taxes**: US tax compliance with wash-sale detection and capital gains tracking
- **Reports Performance**: Daily P&L, performance metrics, and tax liability reports
- **Learns & Adapts**: Continuous strategy optimization based on historical performance

---

## Key Features

### Trading Capabilities
- Real-time market data streaming via Interactive Brokers
- Multiple trading strategies (mean reversion, momentum, ML-driven)
- Smart order routing with TWAP/VWAP execution algorithms
- Comprehensive risk management with position limits and circuit breakers

### Machine Learning
- **Fine-tuned transformer models** from Hugging Face for price prediction and sentiment analysis
- **Pre-trained models** adapted for financial time series (FinBERT, TimesNet, etc.)
- LSTM neural networks for sequential pattern recognition
- Random Forest and XGBoost for feature-based predictions
- Ensemble methods combining multiple fine-tuned models
- Walk-forward optimization for robust backtesting
- **GPU-accelerated training** using CUDA, PyTorch, and TensorFlow

### Tax & Compliance
- Automated wash-sale detection per IRS Publication 550
- Capital gains/losses calculation (short-term and long-term)
- Tax lot tracking with FIFO, LIFO, and specific identification
- IRS Form 8949 and Schedule D generation

### Performance Analytics
- Real-time P&L tracking (realized and unrealized)
- Risk-adjusted metrics (Sharpe ratio, Sortino ratio, Calmar ratio)
- Maximum drawdown analysis
- Strategy performance attribution

---

## Architecture

The system is built using a modular, layered architecture with 5 main components:

```
┌─────────────────────────────────────┐
│      Trading Bot System             │
└─────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
     ▼           ▼           ▼
┌──────────┬──────────┬──────────────┐
│   Data   │ Strategy │  Execution   │
│  Layer   │  Layer   │    Layer     │
└──────────┴──────────┴──────────────┘
     │           │           │
     ▼           ▼           ▼
┌──────────────────────────────────────┐
│  Tax & Recon  │  Reporting Engine    │
└──────────────────────────────────────┘
```

**Components:**
- **Data Layer**: Market data ingestion & storage
- **Strategy Layer**: ML models & signal generation
- **Execution Layer**: Order management & risk controls
- **Tax & Recon Engine**: Tax calculations & compliance
- **Reporting Engine**: Analytics & dashboards

For detailed architecture information, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.14.0 |
| **Trading API** | Interactive Brokers (ib_insync) |
| **Data Processing** | Pandas, NumPy, Polars |
| **Machine Learning** | PyTorch (CUDA), TensorFlow (GPU), scikit-learn, XGBoost |
| **ML Models** | Hugging Face Transformers, FinBERT, TimesNet, LightGBM |
| **GPU Acceleration** | CUDA 12.x, cuDNN, NVIDIA RTX 5090 optimized |
| **Database** | PostgreSQL 15+ with TimescaleDB extension |
| **Caching** | Redis 7+ |
| **Web Framework** | FastAPI with Uvicorn |
| **Testing** | pytest, pytest-asyncio, hypothesis |
| **Monitoring** | Prometheus, Grafana, Sentry |
| **Development** | Poetry, Black, Ruff, mypy |

---

## Project Structure

```
AiFinIntern/
├── components/              # Main application components
│   ├── data_layer/          # Data ingestion and storage
│   │   ├── api_client/      # IB API wrapper
│   │   ├── data_store/      # Database models & repositories
│   │   ├── preprocessing/   # Data normalization & features
│   │   └── agents/          # Data layer AI agents
│   ├── strategy_layer/      # Trading strategies & ML
│   │   ├── models/          # ML model implementations
│   │   ├── backtesting/     # Backtesting framework
│   │   ├── signals/         # Signal generation
│   │   ├── strategies/      # Trading strategies
│   │   └── agents/          # Strategy layer AI agents
│   ├── execution_layer/     # Order execution & positions
│   │   ├── order_manager/   # Order management system
│   │   ├── position_manager/# Position tracking
│   │   ├── risk_manager/    # Risk controls
│   │   └── agents/          # Execution layer AI agents
│   ├── tax_recon/           # Tax calculations
│   │   ├── tax_lots/        # Tax lot tracking
│   │   ├── wash_sale/       # Wash sale detection
│   │   ├── capital_gains/   # Capital gains calculator
│   │   └── agents/          # Tax & recon AI agents
│   └── reporting/           # Reports & analytics
│       ├── pnl/             # P&L calculations
│       ├── performance/     # Performance metrics
│       ├── tax_reports/     # Tax report generation
│       └── agents/          # Reporting AI agents
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── paper_trading/       # Paper trading validation
├── config/                  # Configuration files
├── docs/                    # Additional documentation
├── logs/                    # Application logs
├── data/                    # Data storage
│   ├── historical/          # Historical market data
│   └── cache/               # Cached data
├── Code/                    # Legacy code (to be migrated)
├── CLAUDE.md                # Project documentation index
├── DECISIONS.md             # Decision log with rationale
├── CHANGES.md               # Implementation change log
├── RISKS.md                 # Risk register
├── ROADMAP.md               # Project phases and milestones
├── TESTING.md               # Testing strategy
├── ARCHITECTURE.md          # Technical architecture spec
├── AGENTS.md                # AI agent specifications
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Poetry configuration
└── docker-compose.yml       # Docker services
```

---

## Installation

### Prerequisites

- **Python 3.14.0** (required)
- PostgreSQL 15+ with TimescaleDB extension
- Redis 7+
- Interactive Brokers TWS or IB Gateway (for live/paper trading)
- Docker & Docker Compose (optional, for containerized deployment)
- **NVIDIA GPU with CUDA 12.x** (recommended for ML training)
- CUDA Toolkit and cuDNN libraries (for GPU acceleration)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/lolisaigao1234/AiFinIntern.git
   cd AiFinIntern
   ```

2. **Install Poetry** (recommended for dependency management)
   ```bash
   # Using pip
   pip install poetry

   # Or using the official installer (recommended)
   curl -sSL https://install.python-poetry.org | python3 -

   # Verify installation
   poetry --version
   ```

3. **Install dependencies**

   **Option A: Using Poetry (Recommended)**
   ```bash
   # Install all dependencies
   poetry install

   # Install with CUDA support for GPU acceleration
   poetry install --extras cuda

   # Install with Jupyter notebook support
   poetry install --extras jupyter

   # Install all optional dependencies
   poetry install --extras all

   # Activate the virtual environment
   poetry shell

   # IMPORTANT: Install PyTorch with CUDA separately
   poetry run pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130
   ```

4. **Verify GPU Installation**
   ```bash
   # Check CUDA availability in PyTorch
   poetry run python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

   # Check TensorFlow GPU
   poetry run python -c "import tensorflow as tf; print('GPUs available:', len(tf.config.list_physical_devices('GPU')))"
   ```asd

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

   Required environment variables:
   ```env
   # Interactive Brokers
   IB_HOST=127.0.0.1
   IB_PORT=7497          # 7497 for paper, 7496 for live
   IB_CLIENT_ID=1
   IB_ACCOUNT=YOUR_ACCOUNT_ID

   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/trading_bot
   REDIS_URL=redis://localhost:6379

   # Trading Parameters
   MAX_POSITION_SIZE=1000
   MAX_DAILY_LOSS=5000.0
   ENVIRONMENT=development
   ```

6. **Set up database**
   ```bash
   # Using Docker Compose
   docker-compose up -d postgres redis

   # Or install PostgreSQL locally and run migrations
   poetry run alembic upgrade head
   ```

7. **Run tests**
   ```bash
   # Using Poetry
   poetry run pytest tests/

   # Or with coverage
   poetry run pytest --cov=components --cov-report=html

   # Run specific test types
   poetry run pytest -m unit           # Unit tests only
   poetry run pytest -m integration    # Integration tests only
   poetry run pytest -m "not slow"     # Skip slow tests
   ```

8. **Start the application**
   ```bash
   # Using Poetry (recommended)
   poetry run python -m components.main

   # Or activate shell first
   poetry shell
   python -m components.main

   # Using Docker
   docker-compose up
   ```

---

## Local Development Setup

### Hardware Specifications

This project is optimized for the following local development environment:

| Component | Specification |
|-----------|--------------|
| **CPU** | AMD Ryzen 7 7700X (8 cores, 16 threads) |
| **GPU** | NVIDIA RTX 5090 Founders Edition (24GB VRAM) |
| **RAM** | 32GB DDR5 |
| **OS** | Windows 11 Pro |
| **CUDA** | 12.x with cuDNN 8.9+ |

### ML Model Fine-Tuning Approach

**Philosophy**: We focus on **fine-tuning pre-trained models** rather than training from scratch to:
- Leverage state-of-the-art architectures from the research community
- Reduce training time and computational costs
- Achieve better performance with limited data
- Utilize transfer learning from large-scale datasets

#### Recommended Pre-trained Models

**From Hugging Face:**

1. **Financial Sentiment & Text Analysis**
   - `ProsusAI/finbert` - Financial sentiment analysis
   - `yiyanghkust/finbert-tone` - Financial tone detection
   - `mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis`

2. **Time Series Forecasting**
   - `AutonLab/MOMENT-1-large` - Pre-trained time series foundation model
   - `google/timesfm-1.0-200m` - Time series forecasting
   - `ibm/chronos-t5-base` - Time series transformer

3. **General Purpose Transformers** (for fine-tuning)
   - `distilbert-base-uncased` - Lighter BERT variant
   - `microsoft/deberta-v3-base` - High-performance transformer
   - `google/flan-t5-base` - Versatile encoder-decoder

#### GPU Optimization Strategy

**PyTorch CUDA Configuration:**

```python
import torch

# Verify CUDA availability
assert torch.cuda.is_available(), "CUDA not available!"
print(f"CUDA Version: {torch.version.cuda}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Optimization settings for RTX 5090
torch.backends.cudnn.benchmark = True  # Auto-tune kernels
torch.backends.cuda.matmul.allow_tf32 = True  # Use TF32 for matmul
torch.set_float32_matmul_precision('high')  # Better performance
```

**TensorFlow GPU Configuration:**

```python
import tensorflow as tf

# GPU memory growth (prevents OOM)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    # Enable mixed precision for RTX 5090
    tf.keras.mixed_precision.set_global_policy('mixed_float16')

    print(f"TensorFlow GPU: {tf.test.gpu_device_name()}")
    print(f"CUDA: {tf.test.is_built_with_cuda()}")
```

### Setting Up GPU Environment

1. **Install NVIDIA Drivers**
   ```powershell
   # Windows 11 Pro
   # Download latest Game Ready or Studio Driver from:
   # https://www.nvidia.com/Download/index.aspx

   # After installation, verify in PowerShell:
   nvidia-smi  # Verify installation
   ```

2. **Install CUDA Toolkit 12.x**
   ```powershell
   # Download CUDA Toolkit 12.x for Windows from:
   # https://developer.nvidia.com/cuda-downloads
   # Select: Windows > x86_64 > 11 > exe (local)

   # Run the installer (cuda_12.x.x_windows.exe)
   # Installation will automatically add CUDA to PATH

   # Verify installation in PowerShell:
   nvcc --version
   ```

3. **Install cuDNN**
   ```powershell
   # Download from NVIDIA (requires account)
   # https://developer.nvidia.com/cudnn
   # Download cuDNN for CUDA 12.x (Windows)

   # Extract ZIP and copy files to CUDA installation directory:
   # Copy cudnn-*-archive\bin\*.dll to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\bin
   # Copy cudnn-*-archive\include\*.h to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\include
   # Copy cudnn-*-archive\lib\*.lib to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\lib\x64
   ```

4. **Install PyTorch with CUDA**
   ```powershell
   # Using pip (for CUDA 12.x)
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

   # Verify installation
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

5. **Install TensorFlow with GPU support**
   ```bash
   pip install tensorflow[and-cuda]

   # Verify GPU detection
   python -c "import tensorflow as tf; print(f'GPUs: {tf.config.list_physical_devices(\"GPU\")}')"
   ```

6. **Install Hugging Face Libraries**
   ```bash
   pip install transformers datasets accelerate evaluate
   pip install sentencepiece protobuf  # For certain models
   pip install bitsandbytes  # For quantization (optional)
   ```

### Fine-Tuning Workflow

**Example: Fine-tuning FinBERT for Custom Financial Sentiment**

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch

# Load pre-trained FinBERT
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3  # Positive, Negative, Neutral
)

# Move to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Training arguments optimized for RTX 5090
training_args = TrainingArguments(
    output_dir="./models/finbert_finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=32,  # Large batch size for 24GB VRAM
    per_device_eval_batch_size=64,
    gradient_accumulation_steps=2,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    fp16=True,  # Mixed precision for faster training
    dataloader_num_workers=8,  # Utilize all CPU cores
    optim="adamw_torch_fused",  # Faster optimizer for CUDA
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  # Your custom dataset
    eval_dataset=eval_dataset,
)

# Fine-tune the model
trainer.train()

# Save fine-tuned model
model.save_pretrained("./models/finbert_custom")
tokenizer.save_pretrained("./models/finbert_custom")
```

### Performance Benchmarks

**Expected Training Performance (RTX 5090):**

| Model | Parameters | Batch Size | Training Time (1 epoch) |
|-------|-----------|------------|------------------------|
| FinBERT | 110M | 32 | ~15 minutes (10k samples) |
| DistilBERT | 66M | 64 | ~8 minutes (10k samples) |
| LSTM (custom) | 5M | 256 | ~2 minutes (10k samples) |
| Random Forest | N/A | N/A | ~30 seconds (10k samples) |

### Memory Management Tips

**For 24GB VRAM on RTX 5090:**

1. **Gradient Checkpointing** (reduce memory, slight speed trade-off)
   ```python
   model.gradient_checkpointing_enable()
   ```

2. **Batch Size Optimization**
   - Start with batch size 32, increase if memory allows
   - Use gradient accumulation for effective larger batches

3. **Mixed Precision Training**
   ```python
   from torch.cuda.amp import autocast, GradScaler

   scaler = GradScaler()
   with autocast():
       outputs = model(**inputs)
       loss = outputs.loss
   ```

4. **Model Quantization** (for inference)
   ```python
   from transformers import BitsAndBytesConfig

   quantization_config = BitsAndBytesConfig(
       load_in_8bit=True,  # 8-bit quantization
       llm_int8_threshold=6.0
   )
   ```

### Development Workflow

1. **Data Preparation**
   - Collect and preprocess financial data
   - Create train/validation/test splits
   - Store in efficient formats (Parquet, HDF5)

2. **Model Selection**
   - Browse Hugging Face Model Hub
   - Download pre-trained model
   - Test baseline performance

3. **Fine-tuning**
   - Configure training parameters
   - Monitor GPU utilization (`nvidia-smi`)
   - Track metrics with TensorBoard

4. **Evaluation**
   - Test on held-out dataset
   - Compare with baseline
   - Analyze errors

5. **Deployment**
   - Export optimized model
   - Implement inference pipeline
   - Integrate with trading system

### Monitoring GPU Usage

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Log GPU usage to file
nvidia-smi --query-gpu=timestamp,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv -l 5 > gpu_usage.csv

# Install and use nvtop for interactive monitoring
sudo apt install nvtop
nvtop
```

### Troubleshooting

**CUDA Out of Memory:**
- Reduce batch size
- Enable gradient checkpointing
- Use gradient accumulation
- Clear cache: `torch.cuda.empty_cache()`

**Slow Training:**
- Verify CUDA is being used: `model.device`
- Enable cudNN benchmarking
- Use mixed precision (FP16)
- Increase dataloader workers

**Model Not Converging:**
- Adjust learning rate
- Increase warmup steps
- Try different optimizer (AdamW, SGD)
- Check data preprocessing

---

## Quick Start

### Paper Trading Mode

```python
from components.data_layer.api_client import IBClient
from components.strategy_layer.strategies import MomentumStrategy
from components.execution_layer.order_manager import OrderManager
from components.execution_layer.risk_manager import RiskManager

# Initialize components
ib_client = IBClient(host='127.0.0.1', port=7497, client_id=1)
strategy = MomentumStrategy()
risk_manager = RiskManager()
order_manager = OrderManager(ib_client)

# Create trading bot
bot = TradingBot(
    data_provider=ib_client,
    strategy=strategy,
    order_manager=order_manager,
    risk_manager=risk_manager
)

# Start paper trading
await bot.start(mode='paper')
```

### Running Backtests

```python
from components.strategy_layer.backtesting import Backtester
from components.strategy_layer.strategies import MeanReversionStrategy

# Load historical data
data = load_historical_data('AAPL', start_date='2023-01-01', end_date='2024-01-01')

# Configure strategy
strategy = MeanReversionStrategy(
    lookback_period=20,
    entry_threshold=2.0,
    exit_threshold=0.5
)

# Run backtest
backtester = Backtester(strategy, data)
results = backtester.run()

# Analyze results
print(f"Total Return: {results.total_return:.2%}")
print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
print(f"Max Drawdown: {results.max_drawdown:.2%}")
```

### Generating Tax Reports

```python
from components.tax_recon.capital_gains import CapitalGainsCalculator
from components.reporting.tax_reports import Form8949Generator

# Calculate capital gains for tax year
calculator = CapitalGainsCalculator()
gains = calculator.calculate_for_year(2024, method='FIFO')

# Generate IRS Form 8949
form_generator = Form8949Generator()
form_8949 = form_generator.generate(gains)
form_8949.export_pdf('tax_reports/form_8949_2024.pdf')
```

---

## Configuration

### Trading Parameters

Edit `config/trading_config.yaml`:

```yaml
trading:
  max_position_size: 1000
  max_portfolio_exposure: 0.8  # 80% of capital
  max_daily_loss: 5000.0
  position_sizing_method: "kelly"  # or "fixed", "percent"

risk_management:
  enable_circuit_breaker: true
  circuit_breaker_loss_threshold: 0.05  # 5% daily loss
  max_drawdown_threshold: 0.15  # 15% max drawdown
```

### Strategy Configuration

Edit `config/strategy_config.yaml`:

```yaml
strategies:
  momentum:
    enabled: true
    lookback_period: 20
    min_signal_strength: 0.6

  mean_reversion:
    enabled: true
    lookback_period: 30
    entry_threshold: 2.0
    exit_threshold: 0.5

  ml_strategy:
    enabled: true
    model_path: "models/lstm_predictor.h5"
    confidence_threshold: 0.7
```

---

## Development

### Running Tests

```bash
# All tests
poetry run pytest

# Unit tests only
poetry run pytest tests/unit/

# Integration tests
poetry run pytest tests/integration/

# With coverage
poetry run pytest --cov=components --cov-report=html

# Specific markers
poetry run pytest -m unit
poetry run pytest -m integration
poetry run pytest -m "not slow"
poetry run pytest -m gpu  # GPU-required tests
```

### Code Quality

```bash
# Format code
poetry run black components/ tests/

# Lint code
poetry run ruff check components/ tests/

# Fix linting issues automatically
poetry run ruff check --fix components/ tests/

# Type checking
poetry run mypy components/

# Sort imports
poetry run isort components/ tests/

# Run all formatters at once
poetry run black . && poetry run isort . && poetry run ruff check --fix .
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run manually
poetry run pre-commit run --all-files

# Update hooks to latest versions
poetry run pre-commit autoupdate
```

### Adding New Dependencies

```bash
# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Add an optional dependency
poetry add --optional package-name

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree
```

---

## Documentation

The project documentation is organized into focused, purpose-specific files:

### Core Documentation
- **[CLAUDE.md](./CLAUDE.md)** - 📋 Main documentation index and project overview
- **[ROADMAP.md](./ROADMAP.md)** - 🗺️ Project phases, milestones, and component structure
- **[DECISIONS.md](./DECISIONS.md)** - 🔑 All architectural and technical decisions with rationale
- **[CHANGES.md](./CHANGES.md)** - 📝 Implementation change log with details and testing
- **[RISKS.md](./RISKS.md)** - ⚠️ Risk register with mitigation strategies
- **[TESTING.md](./TESTING.md)** - 🧪 Testing strategy and validation metrics

### Technical Documentation
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - 🏗️ System architecture and technical specifications
- **[AGENTS.md](./AGENTS.md)** - 🤖 AI agent hierarchy and specifications

### Component Documentation
Each component has its own README.md with detailed information:
- `components/data_layer/README.md`
- `components/strategy_layer/README.md`
- `components/execution_layer/README.md`
- `components/tax_recon/README.md`
- `components/reporting/README.md`

**Start here**: [CLAUDE.md](./CLAUDE.md) for a complete overview of all documentation.

---

## Roadmap

### Phase 1: Research & Planning (Weeks 1-2)
- [x] Architecture design
- [x] Project structure setup
- [x] Documentation framework
- [ ] IB API integration research
- [ ] Tax regulation compliance checklist

### Phase 2: Core Development (Weeks 3-6)
- [ ] Data layer implementation
- [ ] Strategy development and ML models
- [ ] Execution engine with risk management
- [ ] Tax reconciliation engine
- [ ] Reporting system

### Phase 3: Testing & Validation (Weeks 7-8)
- [ ] Unit and integration testing
- [ ] Paper trading validation
- [ ] Performance optimization
- [ ] Security audit

### Phase 4: Deployment (Weeks 9-10)
- [ ] Production environment setup
- [ ] Monitoring and alerting
- [ ] Go-live with minimal capital
- [ ] Gradual scaling

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public APIs
- Maintain test coverage above 80%
- Update documentation for any changes

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

**IMPORTANT**: This software is for educational and research purposes only.

- **Not Financial Advice**: This bot does not provide financial, investment, or trading advice
- **Use at Your Own Risk**: Trading involves substantial risk of loss
- **No Warranty**: The software is provided "as is" without warranty of any kind
- **Compliance**: Ensure you comply with all applicable laws and regulations
- **Tax Advice**: Consult a qualified tax professional for tax matters

By using this software, you acknowledge that you understand and accept these risks.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/lolisaigao1234/AiFinIntern/issues)
- **Documentation**: See [docs/](./docs) directory
- **Email**: Contact the project maintainers

---

## Acknowledgments

- Interactive Brokers for providing robust trading API
- Open-source community for excellent libraries (pandas, scikit-learn, etc.)
- IRS for clear tax guidelines and documentation

---

**Last Updated**: 2025-11-15
**Version**: 0.1.0 (Development)
**Status**: Planning Phase
