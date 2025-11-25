# FinBERT Sentiment-Based Quantitative Trading Strategy

## A Step-by-Step Walkthrough for Novice Developers

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Section 1.0: Environment Setup (Leveraging GPU Power)](#section-10-environment-setup-leveraging-gpu-power)
3. [Section 2.0: Data Acquisition and Cleaning](#section-20-data-acquisition-and-cleaning-price--news)
4. [Section 3.0: FinBERT Model Pipeline Development](#section-30-finbert-model-pipeline-development-the-ai-core)
5. [Section 4.0: Feature Engineering: Sentiment to Signal](#section-40-feature-engineering-sentiment-to-signal)
6. [Section 5.0: Strategy Logic and Signal Generation](#section-50-strategy-logic-and-signal-generation)
7. [Section 6.0: Bonus - Backtesting Framework](#section-60-bonus-backtesting-framework)
8. [Appendix: Project File Structure](#appendix-project-file-structure)

---

## 1. Introduction

### 1.1 Project Overview

This walkthrough guides you through building a **sentiment-based quantitative trading strategy** using **FinBERT**, a state-of-the-art financial sentiment analysis model. You will learn to:

- Set up a high-performance GPU computing environment
- Acquire and clean financial news and price data
- Use deep learning to extract sentiment signals from text
- Convert sentiment into actionable trading signals
- Backtest your strategy on historical data

### 1.2 Target Assets: The Magnificent Seven

This project focuses exclusively on seven major technology stocks:

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| MSFT | Microsoft Corporation | Technology |
| GOOGL | Alphabet Inc. (Class A) | Technology |
| AMZN | Amazon.com Inc. | Consumer Cyclical |
| NVDA | NVIDIA Corporation | Technology |
| TSLA | Tesla Inc. | Consumer Cyclical |
| META | Meta Platforms Inc. | Technology |

### 1.3 Hardware Requirements

This project is optimized for:

- **GPU**: NVIDIA GeForce RTX 5090 (Blackwell Architecture, sm_120)
- **RAM**: 32GB DDR5
- **CUDA**: Version 12.8+ (or CUDA 13.0)
- **Storage**: ~10GB free space for models and data

### 1.4 Data Constraints

- **Price Data**: Maximum 10 trading days (approximately two weeks)
- **Trading Hours**: Standard market hours only (9:30 AM - 4:00 PM EST)
- **After-Hours Data**: Excluded from analysis

---

## Section 1.0: Environment Setup (Leveraging GPU Power)

### Task 1.1: CUDA and PyTorch Installation

#### Objective
Verify NVIDIA driver compatibility with the RTX 5090 and install PyTorch with CUDA 12.8+ support to leverage Blackwell architecture's sm_120 compute capability.

#### Background Knowledge
The NVIDIA RTX 5090 uses the Blackwell architecture with compute capability sm_120. This requires:
- NVIDIA Driver R570 or higher
- CUDA Toolkit 12.8 or higher
- PyTorch 2.7.0+ compiled with CUDA 12.8 support

#### Step-by-Step Instructions

**Step 1.1.1: Verify NVIDIA Driver Version**

Open a terminal and run the NVIDIA System Management Interface utility. The output should display:
- Driver Version: 570.xx or higher
- CUDA Version: 12.8 or higher (shown as maximum supported version)

Document the exact driver version for troubleshooting purposes.

**Step 1.1.2: Create a Dedicated Conda Environment**

Create a new isolated Python environment specifically for this project. Use Python 3.12 or 3.13, as these versions have the best compatibility with Blackwell GPUs. Name the environment something descriptive like `finbert-trading`.

**Step 1.1.3: Install PyTorch with CUDA 12.8 Support**

Visit the official PyTorch website (pytorch.org) and use the installation selector to generate the correct installation command. Select:
- PyTorch Build: Stable (2.7.0 or higher)
- Operating System: Your OS
- Package: Conda or Pip
- Compute Platform: CUDA 12.8

**Important**: Do NOT install a CPU-only or older CUDA version, as the RTX 5090 will not be recognized.

**Step 1.1.4: Verify GPU Detection**

After installation, launch Python and import the torch library. Execute the CUDA availability check function. The function should return `True`. Additionally, query the device name to confirm it shows "NVIDIA GeForce RTX 5090".

#### Unit Test Specification: `test_cuda_setup()`

| Test Case | Input | Expected Output | Pass Criteria |
|-----------|-------|-----------------|---------------|
| CUDA Available | None | Boolean | Returns `True` |
| Device Count | None | Integer | Returns ≥ 1 |
| Device Name | device_index=0 | String | Contains "RTX 5090" or "Blackwell" |
| CUDA Version | None | String | Version ≥ "12.8" |
| Memory Available | device_index=0 | Integer | > 20GB (20,000 MB) |

**Test Implementation Notes**:
- Create a function that runs all five checks
- Each check should print a PASS/FAIL status
- The function should return a boolean indicating overall success
- Include a try-except block to catch import errors gracefully

---

### Task 1.2: Core Library Installation

#### Objective
Install all required Python libraries for data acquisition, NLP processing, and numerical computation.

#### Required Libraries

| Library | Purpose | Minimum Version |
|---------|---------|-----------------|
| transformers | Hugging Face model loading (FinBERT) | 4.40.0 |
| pandas | Data manipulation and analysis | 2.2.0 |
| numpy | Numerical computations | 1.26.0 |
| yfinance | Yahoo Finance price data API | 0.2.40 |
| requests | HTTP requests for news APIs | 2.31.0 |
| beautifulsoup4 | HTML parsing for web scraping | 4.12.0 |
| feedparser | RSS feed parsing for news | 6.0.0 |
| pytest | Unit testing framework | 8.0.0 |
| matplotlib | Visualization (for backtesting) | 3.8.0 |

#### Step-by-Step Instructions

**Step 1.2.1: Install Hugging Face Transformers**

Install the transformers library from Hugging Face. This library provides the interface to load and run the FinBERT model. Ensure you install with PyTorch support by verifying torch is already installed.

**Step 1.2.2: Install Data Acquisition Libraries**

Install yfinance for fetching historical stock prices. Install beautifulsoup4 and feedparser for scraping and parsing financial news headlines.

**Step 1.2.3: Install Scientific Computing Libraries**

Install pandas for data manipulation, numpy for numerical operations, and scipy for statistical functions (needed for softmax in some configurations).

**Step 1.2.4: Install Development Tools**

Install pytest for running unit tests and matplotlib for visualizing backtest results.

**Step 1.2.5: Verify All Imports**

Create a test script that attempts to import every required library. Run this script to ensure there are no import errors or version conflicts.

#### Unit Test Specification: `test_library_imports()`

| Test Case | Action | Expected Result |
|-----------|--------|-----------------|
| Import torch | `import torch` | No ImportError |
| Import transformers | `import transformers` | No ImportError |
| Import pandas | `import pandas` | No ImportError |
| Import yfinance | `import yfinance` | No ImportError |
| Import beautifulsoup4 | `from bs4 import BeautifulSoup` | No ImportError |
| Version Check - transformers | Check version string | ≥ 4.40.0 |
| Version Check - pandas | Check version string | ≥ 2.2.0 |

**Test Implementation Notes**:
- Use a dictionary to map library names to their import statements
- Loop through and attempt each import in a try-except block
- Record successes and failures
- Print a summary table at the end

---

## Section 2.0: Data Acquisition and Cleaning (Price & News)

### Task 2.1: Price Data Fetcher Function

#### Objective
Implement a function that retrieves historical OHLCV (Open, High, Low, Close, Volume) price data for any of the Magnificent Seven stocks, ensuring after-hours trading data is excluded.

#### Function Signature
```
fetch_price_data(ticker: str, days: int = 10) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| ticker | str | Stock ticker symbol | Must be one of: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META |
| days | int | Number of trading days to fetch | 1 ≤ days ≤ 10 |

#### Output Specification

The function should return a pandas DataFrame with the following columns:

| Column | Data Type | Description |
|--------|-----------|-------------|
| Date | datetime64 | Trading date (index) |
| Open | float64 | Opening price |
| High | float64 | Highest price during session |
| Low | float64 | Lowest price during session |
| Close | float64 | Closing price |
| Volume | int64 | Number of shares traded |
| Adj Close | float64 | Adjusted closing price |

#### Step-by-Step Instructions

**Step 2.1.1: Define the Valid Tickers List**

Create a constant list or tuple containing the seven valid ticker symbols. This will be used for input validation.

**Step 2.1.2: Implement Input Validation**

At the start of the function:
1. Check if the provided ticker is in the valid tickers list
2. Check if days is within the valid range (1-10)
3. Raise a ValueError with a descriptive message if validation fails

**Step 2.1.3: Calculate Date Range**

Calculate the start and end dates for data fetching:
- End date: Today's date (or most recent trading day if weekend)
- Start date: End date minus (days × 1.5) calendar days

The 1.5 multiplier accounts for weekends and holidays. You will filter to exactly `days` trading days later.

**Step 2.1.4: Fetch Data Using yfinance**

Use the yfinance library's download function or Ticker object to fetch historical data. Specify:
- The ticker symbol
- Start and end dates
- Interval as "1d" (daily)

**Step 2.1.5: Filter to Market Hours Data Only**

yfinance daily data already excludes after-hours by default, but verify by checking:
- All timestamps fall on weekdays (Monday-Friday)
- No holiday dates are included (optional: use pandas market calendar)

**Step 2.1.6: Trim to Exact Number of Days**

After fetching, the DataFrame may contain more than `days` rows. Use tail() to select only the most recent `days` trading days.

**Step 2.1.7: Clean and Validate Output**

- Ensure no NaN values exist in critical columns (Open, Close)
- Ensure all prices are positive
- Ensure the DataFrame is sorted by date in ascending order

#### Unit Test Specification: `test_fetch_price_data()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 2.1.1 | Valid ticker returns data | ticker="AAPL", days=5 | DataFrame with 5 rows |
| 2.1.2 | Invalid ticker raises error | ticker="INVALID", days=5 | Raises ValueError |
| 2.1.3 | Days out of range (high) | ticker="AAPL", days=15 | Raises ValueError |
| 2.1.4 | Days out of range (low) | ticker="AAPL", days=0 | Raises ValueError |
| 2.1.5 | No NaN in Close column | ticker="MSFT", days=10 | All Close values non-null |
| 2.1.6 | All prices positive | ticker="GOOGL", days=10 | All OHLC > 0 |
| 2.1.7 | Dates are weekdays | ticker="NVDA", days=10 | All dates Mon-Fri |
| 2.1.8 | Data is sorted ascending | ticker="TSLA", days=5 | Dates strictly increasing |

**Test Implementation Notes**:
- Use pytest fixtures to avoid repeated API calls
- Cache the API response for multiple test cases
- Include a timeout decorator for network-dependent tests
- Mock the yfinance response for offline testing capability

---

### Task 2.2: News Data Fetcher Function

#### Objective
Implement a function that retrieves financial news headlines for a specific stock ticker over a defined time period. These headlines will serve as input text for the FinBERT sentiment model.

#### Function Signature
```
fetch_news_headlines(ticker: str, days: int = 10) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| ticker | str | Stock ticker symbol | Must be one of the Magnificent Seven |
| days | int | Number of days of news to fetch | 1 ≤ days ≤ 10 |

#### Output Specification

| Column | Data Type | Description |
|--------|-----------|-------------|
| date | datetime64 | Publication date |
| ticker | str | Associated stock ticker |
| headline | str | News headline text |
| source | str | News source name |

#### Data Sources (Choose One or Combine)

**Option A: Yahoo Finance RSS Feeds**
- URL pattern: `https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}`
- Free, no API key required
- Limited historical depth

**Option B: NewsAPI.org**
- Requires free API key registration
- Better historical coverage
- Rate limits apply

**Option C: Financial News Websites (Scraping)**
- Seeking Alpha, MarketWatch, Reuters
- Requires BeautifulSoup parsing
- May require handling of anti-scraping measures

#### Step-by-Step Instructions

**Step 2.2.1: Select and Configure Data Source**

Choose your news data source from the options above. If using an API, store the API key in an environment variable (never hardcode).

**Step 2.2.2: Implement Input Validation**

Validate ticker and days parameters using the same logic as Task 2.1.

**Step 2.2.3: Construct the Request**

Build the appropriate URL or API request:
- For RSS: Construct the feed URL with the ticker symbol
- For NewsAPI: Build query parameters including date range and stock symbol/company name
- For scraping: Construct the search URL

**Step 2.2.4: Fetch and Parse Response**

Execute the HTTP request and parse the response:
- For RSS: Use feedparser to extract entries
- For JSON APIs: Parse the JSON response
- For HTML: Use BeautifulSoup to extract headline elements

**Step 2.2.5: Extract Relevant Fields**

From each news item, extract:
- Publication date/time (convert to date only)
- Headline text
- Source name (if available)

**Step 2.2.6: Filter by Date Range**

Filter the collected headlines to include only those within the specified `days` range from today.

**Step 2.2.7: Handle Empty Results**

If no headlines are found for a ticker/date combination:
- Return an empty DataFrame with the correct schema
- Log a warning message (do not raise an exception)

**Step 2.2.8: Deduplicate Headlines**

Remove duplicate headlines (same headline text on same date) that may appear from multiple sources.

#### Unit Test Specification: `test_fetch_news_headlines()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 2.2.1 | Valid ticker returns DataFrame | ticker="AAPL", days=5 | DataFrame (may be empty) |
| 2.2.2 | DataFrame has correct columns | ticker="MSFT", days=5 | Columns: date, ticker, headline, source |
| 2.2.3 | Invalid ticker raises error | ticker="INVALID" | Raises ValueError |
| 2.2.4 | Headlines are strings | ticker="GOOGL", days=5 | All headlines are str type |
| 2.2.5 | Dates within range | ticker="NVDA", days=5 | All dates ≤ 5 days ago |
| 2.2.6 | No duplicate headlines | ticker="TSLA", days=10 | len(df) == len(df.drop_duplicates()) |
| 2.2.7 | Empty result handling | ticker="META", days=1 | Returns empty DataFrame, no error |

**Test Implementation Notes**:
- Mock HTTP responses to avoid network dependency
- Create sample RSS/JSON fixtures for testing
- Test with intentionally malformed data to verify error handling

---

### Task 2.3: Data Cleaner and Merger Function

#### Objective
Implement a function that preprocesses news headlines (removing noise) and aligns them with corresponding trading day price data.

#### Function Signature
```
clean_and_merge_data(
    price_data: pandas.DataFrame,
    news_data: pandas.DataFrame
) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| price_data | DataFrame | Output from `fetch_price_data()` |
| news_data | DataFrame | Output from `fetch_news_headlines()` |

#### Output Specification

| Column | Data Type | Description |
|--------|-----------|-------------|
| date | datetime64 | Trading date |
| ticker | str | Stock ticker |
| open | float64 | Opening price |
| high | float64 | High price |
| low | float64 | Low price |
| close | float64 | Closing price |
| volume | int64 | Trading volume |
| headlines | list[str] | List of cleaned headlines for that day |
| headline_count | int | Number of headlines for the day |

#### Text Cleaning Operations

The following cleaning operations should be applied to each headline:

1. **Remove URLs**: Strip any http/https links
2. **Remove HTML entities**: Convert &amp; to &, etc.
3. **Remove emojis and special characters**: Keep only alphanumeric and basic punctuation
4. **Remove excessive whitespace**: Collapse multiple spaces to single space
5. **Strip leading/trailing whitespace**: Trim the string
6. **Remove ticker symbols**: Remove $AAPL style mentions (optional)
7. **Lowercase conversion**: Convert to lowercase for consistency (optional, FinBERT handles case)

#### Step-by-Step Instructions

**Step 2.3.1: Implement Text Cleaning Helper Function**

Create a helper function `clean_headline(text: str) -> str` that applies all the cleaning operations listed above. This function will be applied to each headline.

**Step 2.3.2: Apply Cleaning to News Data**

Use pandas apply() or a list comprehension to clean all headlines in the news DataFrame.

**Step 2.3.3: Normalize Date Formats**

Ensure both DataFrames have their date columns in the same format:
- Convert both to datetime64 without time component
- Remove timezone information if present

**Step 2.3.4: Aggregate Headlines by Date**

Group the news DataFrame by date and aggregate headlines into a list. Count the number of headlines per day.

**Step 2.3.5: Merge DataFrames**

Perform a left join of price_data with aggregated news data on the date column. This ensures all trading days are included, even if no news exists for that day.

**Step 2.3.6: Handle Missing News Days**

For trading days with no news:
- Set headlines to an empty list []
- Set headline_count to 0
- Do NOT drop these rows

**Step 2.3.7: Final Validation**

Verify the output DataFrame:
- No NaN values in price columns
- All headline_counts are ≥ 0
- Date column is properly aligned

#### Unit Test Specification: `test_clean_and_merge_data()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 2.3.1 | URL removal works | "Check https://example.com news" | "Check news" |
| 2.3.2 | Emoji removal works | "Stocks up 📈🚀" | "Stocks up" |
| 2.3.3 | HTML entity conversion | "Q1 &amp; Q2 results" | "Q1 & Q2 results" |
| 2.3.4 | Whitespace normalization | "Too   many   spaces" | "Too many spaces" |
| 2.3.5 | Empty news handling | price_data + empty news_data | All headline_count = 0 |
| 2.3.6 | No NaN in output | Valid inputs | No NaN in any column |
| 2.3.7 | Date alignment correct | Mismatched dates | Only matching dates merged |
| 2.3.8 | Headlines aggregated | Multiple headlines same day | List contains all headlines |
| 2.3.9 | Row count preserved | 10 trading days | Output has 10 rows |

**Test Implementation Notes**:
- Create fixture DataFrames for consistent testing
- Test each cleaning operation individually
- Test the full merge operation with known data
- Include edge cases: empty inputs, single row inputs

---

## Section 3.0: FinBERT Model Pipeline Development (The AI Core)

### Task 3.1: Model Loader Function

#### Objective
Implement a function that loads the pre-trained FinBERT model and tokenizer from Hugging Face, transfers them to GPU memory, and prepares them for inference.

#### Function Signature
```
load_finbert_model(device: str = "cuda") -> Tuple[model, tokenizer]
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| device | str | Target device ("cuda" or "cpu") | "cuda" |

#### Output Specification

Returns a tuple containing:
1. **model**: A `BertForSequenceClassification` or `AutoModelForSequenceClassification` object loaded on the specified device
2. **tokenizer**: A `BertTokenizer` or `AutoTokenizer` object for preprocessing text

#### Model Details

- **Model Name**: `ProsusAI/finbert`
- **Model Type**: BERT for Sequence Classification
- **Output Classes**: 3 (positive, negative, neutral)
- **Maximum Input Length**: 512 tokens
- **Model Size**: ~440MB

#### Step-by-Step Instructions

**Step 3.1.1: Import Required Classes**

Import the necessary classes from the transformers library:
- For automatic model/tokenizer selection: `AutoModelForSequenceClassification`, `AutoTokenizer`
- Or specifically for BERT: `BertForSequenceClassification`, `BertTokenizer`

**Step 3.1.2: Check Device Availability**

Before attempting to load to GPU:
1. If device is "cuda", verify CUDA is available
2. If CUDA is not available and device is "cuda", either raise an error or fall back to CPU with a warning

**Step 3.1.3: Load the Tokenizer**

Load the FinBERT tokenizer from Hugging Face:
- Model identifier: "ProsusAI/finbert"
- The tokenizer will be downloaded and cached on first run (~2MB)

**Step 3.1.4: Load the Model**

Load the FinBERT model from Hugging Face:
- Model identifier: "ProsusAI/finbert"
- The model will be downloaded and cached on first run (~440MB)

**Step 3.1.5: Transfer Model to Device**

Move the model to the specified device:
- Use the `.to(device)` method
- For GPU: `.to('cuda')` or `.to('cuda:0')` for specific GPU

**Step 3.1.6: Set Model to Evaluation Mode**

Call `.eval()` on the model to:
- Disable dropout layers
- Disable batch normalization updates
- Prepare for inference (not training)

**Step 3.1.7: Verify Model Loading**

Perform a quick validation:
- Check model is on correct device
- Check model config shows 3 labels
- Optionally, run a dummy inference to verify functionality

#### Unit Test Specification: `test_load_finbert_model()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 3.1.1 | Model loads successfully | device="cuda" | Returns (model, tokenizer) tuple |
| 3.1.2 | Model on correct device | device="cuda" | model.device == cuda:0 |
| 3.1.3 | Model in eval mode | default | model.training == False |
| 3.1.4 | Correct number of labels | default | model.config.num_labels == 3 |
| 3.1.5 | Tokenizer loads correctly | default | tokenizer is not None |
| 3.1.6 | CPU fallback works | device="cpu" | Model loads on CPU |
| 3.1.7 | Invalid device handling | device="invalid" | Raises ValueError |
| 3.1.8 | GPU memory allocated | device="cuda" | torch.cuda.memory_allocated() > 0 |

**Test Implementation Notes**:
- Use pytest fixtures to load model once and reuse
- The first test run will be slow (model download)
- Mock the download for CI/CD environments
- Test both CUDA and CPU modes

---

### Task 3.2: Sentiment Scorer Function

#### Objective
Implement a function that takes a list of text headlines, processes them through the FinBERT model on GPU, and returns sentiment scores.

#### Function Signature
```
get_sentiment_score(
    text_list: List[str],
    model: BertModel,
    tokenizer: BertTokenizer,
    batch_size: int = 16
) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| text_list | List[str] | List of headline strings to analyze | Required |
| model | BertModel | Loaded FinBERT model from Task 3.1 | Required |
| tokenizer | BertTokenizer | Loaded tokenizer from Task 3.1 | Required |
| batch_size | int | Number of texts to process simultaneously | 16 |

#### Output Specification

| Column | Data Type | Description | Value Range |
|--------|-----------|-------------|-------------|
| text | str | Original input text | - |
| positive | float64 | Probability of positive sentiment | [0.0, 1.0] |
| negative | float64 | Probability of negative sentiment | [0.0, 1.0] |
| neutral | float64 | Probability of neutral sentiment | [0.0, 1.0] |
| prediction | str | Highest probability label | "positive", "negative", "neutral" |
| sentiment_score | float64 | Composite score (positive - negative) | [-1.0, 1.0] |

#### Step-by-Step Instructions

**Step 3.2.1: Handle Empty Input**

If text_list is empty or None:
- Return an empty DataFrame with the correct schema
- Do not raise an error

**Step 3.2.2: Preprocess Text for Tokenization**

For each text in the list:
- Ensure it is a string (convert if necessary)
- Handle None values by replacing with empty string
- Truncate very long texts if needed (FinBERT max is 512 tokens)

**Step 3.2.3: Create Batches**

Divide the text list into batches of size `batch_size`:
- This prevents GPU memory overflow with large inputs
- Smaller batches = less memory, slower processing
- Larger batches = more memory, faster processing
- For RTX 5090 with 32GB, batch_size of 16-32 is reasonable

**Step 3.2.4: Tokenize Each Batch**

For each batch, use the tokenizer to convert text to model inputs:
- Set `padding=True` to pad shorter sequences
- Set `truncation=True` to truncate long sequences
- Set `max_length=512` to enforce the model's limit
- Set `return_tensors="pt"` for PyTorch tensors

**Step 3.2.5: Move Tensors to GPU**

Transfer the tokenized inputs to the same device as the model:
- Move input_ids to GPU
- Move attention_mask to GPU
- Move token_type_ids to GPU (if present)

**Step 3.2.6: Run Inference (No Gradient Computation)**

Execute the model within a `torch.no_grad()` context:
- This disables gradient computation
- Reduces memory usage
- Speeds up inference

Pass the tokenized inputs to the model and capture the logits output.

**Step 3.2.7: Apply Softmax to Get Probabilities**

Convert raw logits to probabilities:
- Apply softmax function along the class dimension (dim=1)
- The output will sum to 1.0 for each text
- Move results back to CPU for pandas compatibility

**Step 3.2.8: Extract Label Probabilities**

The FinBERT model outputs probabilities in this order:
- Index 0: positive
- Index 1: negative  
- Index 2: neutral

Extract each probability into separate columns.

**Step 3.2.9: Calculate Composite Sentiment Score**

Compute the sentiment score using the formula:
```
sentiment_score = positive_probability - negative_probability
```

This yields a score from -1.0 (very negative) to +1.0 (very positive).

**Step 3.2.10: Determine Prediction Label**

For each text, identify the label with the highest probability. Assign the corresponding string label ("positive", "negative", "neutral").

**Step 3.2.11: Compile Results DataFrame**

Combine all results into a pandas DataFrame with the specified columns.

#### Unit Test Specification: `test_get_sentiment_score()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 3.2.1 | Positive text detection | ["Revenue surged 50%"] | prediction == "positive" |
| 3.2.2 | Negative text detection | ["Company reports massive losses"] | prediction == "negative" |
| 3.2.3 | Neutral text detection | ["The company held a meeting"] | prediction == "neutral" |
| 3.2.4 | Probabilities sum to 1 | Any valid text | pos + neg + neu ≈ 1.0 |
| 3.2.5 | Score range valid | Any valid text | -1.0 ≤ score ≤ 1.0 |
| 3.2.6 | Empty list handling | [] | Empty DataFrame returned |
| 3.2.7 | Batch processing works | 50 headlines | 50 rows returned |
| 3.2.8 | GPU memory released | Large batch | Memory freed after call |
| 3.2.9 | Long text handling | 1000-word text | No error, truncated correctly |
| 3.2.10 | Special characters | "Apple's Q1 #results @2024!" | Processes without error |

**Test Implementation Notes**:
- Use known financial phrases with clear sentiment
- Test with actual FinBERT model for accuracy tests
- Use mocked model for unit tests (speed)
- Verify GPU memory is properly managed

---

## Section 4.0: Feature Engineering: Sentiment to Signal

### Task 4.1: Signal Aggregator Function

#### Objective
Implement a function that converts the per-headline sentiment probabilities into a single daily sentiment alpha feature for each stock.

#### Function Signature
```
calculate_daily_signal(daily_sentiment_scores: pandas.DataFrame) -> float
```

#### Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| daily_sentiment_scores | DataFrame | Output from `get_sentiment_score()` for one day's headlines |

#### Output Specification

Returns a single float value representing the aggregated daily sentiment alpha, in the range [-1.0, 1.0].

#### Aggregation Methods

You should implement one or more of these methods:

**Method A: Simple Mean**
```
alpha = mean(sentiment_scores)
```

**Method B: Weighted by Confidence**
```
confidence = max(positive, negative, neutral) for each headline
alpha = weighted_mean(sentiment_scores, weights=confidence)
```

**Method C: Positive-Negative Ratio**
```
alpha = (sum(positive) - sum(negative)) / (sum(positive) + sum(negative) + sum(neutral))
```

**Method D: Count-Based**
```
alpha = (count_positive - count_negative) / total_count
```

#### Step-by-Step Instructions

**Step 4.1.1: Handle Empty Input**

If the input DataFrame is empty (no headlines for the day):
- Return 0.0 (neutral signal)
- This represents "no information" rather than positive or negative

**Step 4.1.2: Extract Sentiment Scores**

Extract the sentiment_score column (or positive/negative/neutral columns) from the input DataFrame.

**Step 4.1.3: Apply Aggregation Method**

Apply your chosen aggregation method to compute a single daily value.

**Step 4.1.4: Clip to Valid Range**

Ensure the output is within [-1.0, 1.0]:
- Clip values below -1.0 to -1.0
- Clip values above 1.0 to 1.0

**Step 4.1.5: Round for Numerical Stability**

Round the result to 4-6 decimal places to avoid floating-point precision issues.

#### Unit Test Specification: `test_calculate_daily_signal()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 4.1.1 | All positive headlines | scores all > 0.5 | Output > 0.0 |
| 4.1.2 | All negative headlines | scores all < -0.5 | Output < 0.0 |
| 4.1.3 | Mixed headlines | half positive, half negative | Output ≈ 0.0 |
| 4.1.4 | Empty input | Empty DataFrame | Output == 0.0 |
| 4.1.5 | Single headline | One row | Output == that score |
| 4.1.6 | Output in range | Any input | -1.0 ≤ output ≤ 1.0 |
| 4.1.7 | Output is float | Any input | isinstance(output, float) |

---

### Task 4.2: Feature Lagging Function

#### Objective
Implement a function that time-shifts sentiment features to ensure proper temporal alignment and prevent lookahead bias.

#### Critical Concept: Lookahead Bias

**Lookahead bias** occurs when future information is used to make past predictions. In trading:
- News published on Day T should only influence trades on Day T+1 or later
- Using Day T news to predict Day T prices creates unrealistic backtests
- This is the most common mistake in quantitative finance

#### Function Signature
```
lag_feature(
    merged_data: pandas.DataFrame,
    lag_days: int = 1
) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| merged_data | DataFrame | Output from clean_and_merge_data() with daily_signal added | Required |
| lag_days | int | Number of days to shift signals | 1 |

#### Output Specification

Returns a DataFrame with an additional column:
- `signal_lagged`: The sentiment signal shifted forward by `lag_days`

The relationship should be:
- `signal_lagged[T]` contains the sentiment computed from Day T-1 news
- This signal is then used to make trading decisions for Day T

#### Step-by-Step Instructions

**Step 4.2.1: Create Copy of Input**

Create a copy of the input DataFrame to avoid modifying the original data.

**Step 4.2.2: Apply Temporal Shift**

Use pandas shift() function to move the sentiment signal forward:
- `df['signal_lagged'] = df['daily_signal'].shift(lag_days)`
- With lag_days=1: Day T gets Day T-1's signal

**Step 4.2.3: Handle NaN Values**

The shift operation creates NaN values at the beginning:
- First `lag_days` rows will have NaN in signal_lagged
- Option A: Drop these rows (reduces data size)
- Option B: Fill with 0.0 (neutral signal for no prior info)
- Option C: Keep NaN and handle in strategy logic

**Step 4.2.4: Verify Alignment**

Add assertions or checks to verify:
- signal_lagged[i] == daily_signal[i - lag_days] for all valid i
- No future data is accessible in signal_lagged

**Step 4.2.5: Document the Lag**

Add a note or column indicating the lag applied for traceability.

#### Unit Test Specification: `test_lag_feature()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 4.2.1 | Basic lag works | 10-day data, lag=1 | signal_lagged[1] == daily_signal[0] |
| 4.2.2 | First row is NaN | lag=1 | signal_lagged[0] is NaN |
| 4.2.3 | Lag=2 shifts correctly | lag=2 | signal_lagged[2] == daily_signal[0] |
| 4.2.4 | No lookahead | All rows | signal_lagged[i] uses only data from < Day i |
| 4.2.5 | Data integrity | Original data | Original columns unchanged |
| 4.2.6 | Edge case: lag=0 | lag=0 | signal_lagged == daily_signal |

**Test Implementation Notes**:
- This test is CRITICAL for strategy validity
- Manually verify with known data
- Create test case with obvious pattern to detect errors
- Example: daily_signal = [1, 2, 3, 4, 5], lag=1 → signal_lagged = [NaN, 1, 2, 3, 4]

---

## Section 5.0: Strategy Logic and Signal Generation

### Task 5.1: Strategy Generator Function

#### Objective
Implement a function that converts the lagged sentiment alpha feature into actionable trading signals (BUY, SELL, HOLD).

#### Function Signature
```
generate_trading_signal(
    alpha_feature: float,
    buy_threshold: float = 0.3,
    sell_threshold: float = -0.3
) -> str
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| alpha_feature | float | The lagged daily sentiment score | Required |
| buy_threshold | float | Minimum score to generate BUY | 0.3 |
| sell_threshold | float | Maximum score to generate SELL | -0.3 |

#### Output Specification

Returns one of three string values:
- `"BUY"`: Alpha exceeds buy_threshold
- `"SELL"`: Alpha is below sell_threshold
- `"HOLD"`: Alpha is between thresholds

#### Signal Logic

```
IF alpha_feature > buy_threshold:
    RETURN "BUY"
ELIF alpha_feature < sell_threshold:
    RETURN "SELL"
ELSE:
    RETURN "HOLD"
```

#### Step-by-Step Instructions

**Step 5.1.1: Validate Thresholds**

Ensure the thresholds make sense:
- buy_threshold > sell_threshold
- Both thresholds are within [-1.0, 1.0]
- Raise ValueError if invalid

**Step 5.1.2: Handle NaN/None Input**

If alpha_feature is NaN or None:
- Return "HOLD" (conservative approach)
- Alternatively, raise an error

**Step 5.1.3: Apply Signal Logic**

Compare alpha_feature against thresholds and return the appropriate signal string.

**Step 5.1.4: Vectorized Version (Optional)**

For processing entire DataFrames, implement a vectorized version using numpy.where() or pandas.cut() for efficiency.

#### Unit Test Specification: `test_generate_trading_signal()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 5.1.1 | Strong positive signal | alpha=0.8, thresholds=±0.3 | "BUY" |
| 5.1.2 | Strong negative signal | alpha=-0.8, thresholds=±0.3 | "SELL" |
| 5.1.3 | Neutral signal | alpha=0.0, thresholds=±0.3 | "HOLD" |
| 5.1.4 | Edge case: exactly at buy | alpha=0.3 | "HOLD" (not strictly greater) |
| 5.1.5 | Edge case: exactly at sell | alpha=-0.3 | "HOLD" (not strictly less) |
| 5.1.6 | Custom thresholds | alpha=0.2, buy=0.1, sell=-0.1 | "BUY" |
| 5.1.7 | NaN handling | alpha=NaN | "HOLD" |
| 5.1.8 | Invalid thresholds | buy=-0.5, sell=0.5 | Raises ValueError |

---

### Task 5.2: Portfolio Logic Function

#### Objective
Implement a function that takes trading signals for all Magnificent Seven stocks and determines the portfolio allocation for the day.

#### Function Signature
```
allocate_portfolio(
    signals: Dict[str, str],
    capital: float = 100000.0,
    max_positions: int = 7
) -> Dict[str, float]
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| signals | Dict[str, str] | Mapping of ticker → signal (BUY/SELL/HOLD) | Required |
| capital | float | Total capital available | 100000.0 |
| max_positions | int | Maximum number of positions to hold | 7 |

#### Output Specification

Returns a dictionary mapping ticker → dollar allocation:
- Positive values: Long position (buy)
- Negative values: Short position (sell)
- Zero: No position

#### Allocation Methods

**Method A: Equal Weight Long-Only**
- Allocate equally among all BUY signals
- Ignore SELL signals (no shorting)
- Hold cash for HOLD signals

**Method B: Long-Short Equal Weight**
- Allocate equally among BUY signals (positive allocation)
- Allocate equally among SELL signals (negative allocation)
- Total absolute allocation = capital

**Method C: Signal-Strength Weighted**
- Weight by the magnitude of the alpha feature
- Stronger signals get larger allocations

#### Step-by-Step Instructions

**Step 5.2.1: Count Signals by Type**

Count how many tickers have each signal type:
- num_buy = count of "BUY" signals
- num_sell = count of "SELL" signals
- num_hold = count of "HOLD" signals

**Step 5.2.2: Calculate Per-Position Allocation**

For equal-weight long-only:
```
if num_buy > 0:
    allocation_per_stock = capital / num_buy
else:
    allocation_per_stock = 0
```

**Step 5.2.3: Build Allocation Dictionary**

Create the output dictionary:
- For BUY tickers: allocation = +allocation_per_stock
- For SELL tickers: allocation = 0 (or -allocation for long-short)
- For HOLD tickers: allocation = 0

**Step 5.2.4: Verify Total Allocation**

Ensure total allocation does not exceed available capital:
```
assert sum(abs(allocations.values())) <= capital
```

**Step 5.2.5: Handle Edge Cases**

- All HOLD signals: Return all zero allocations
- All BUY signals: Allocate capital / 7 to each
- All SELL signals (long-short): Allocate short positions

#### Unit Test Specification: `test_allocate_portfolio()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 5.2.1 | Single BUY signal | AAPL=BUY, rest=HOLD | AAPL gets 100% capital |
| 5.2.2 | Two BUY signals | AAPL=BUY, MSFT=BUY | Each gets 50% capital |
| 5.2.3 | All HOLD signals | All tickers=HOLD | All allocations = 0 |
| 5.2.4 | All BUY signals | All tickers=BUY | Each gets ~14.3% capital |
| 5.2.5 | No over-allocation | Any signals | sum(allocations) ≤ capital |
| 5.2.6 | Correct tickers | Any signals | Output keys match input keys |
| 5.2.7 | Long-short mode | BUY and SELL present | Positive and negative allocations |

---

## Section 6.0: Bonus Backtesting Framework

### Task 6.1: PnL Calculation Function

#### Objective
Implement a function that simulates trading based on generated signals and calculates profit and loss over the historical period.

#### Function Signature
```
calculate_pnl(
    trade_signals: pandas.DataFrame,
    price_data: pandas.DataFrame,
    initial_capital: float = 100000.0,
    transaction_cost_pct: float = 0.001
) -> pandas.DataFrame
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| trade_signals | DataFrame | Contains date, ticker, signal, allocation | Required |
| price_data | DataFrame | Contains date, ticker, open, close prices | Required |
| initial_capital | float | Starting capital | 100000.0 |
| transaction_cost_pct | float | Transaction cost as percentage | 0.001 (0.1%) |

#### Output Specification

| Column | Data Type | Description |
|--------|-----------|-------------|
| date | datetime64 | Trading date |
| ticker | str | Stock ticker |
| signal | str | BUY/SELL/HOLD |
| entry_price | float64 | Price at entry (open) |
| exit_price | float64 | Price at exit (close) |
| position_value | float64 | Dollar value of position |
| daily_return_pct | float64 | Percentage return for the day |
| daily_pnl | float64 | Dollar profit/loss for the day |
| transaction_cost | float64 | Cost of transaction |
| net_pnl | float64 | PnL after costs |
| cumulative_pnl | float64 | Running total PnL |
| portfolio_value | float64 | Total portfolio value |

#### Assumptions

1. **Entry at Open**: Positions are entered at the opening price
2. **Exit at Close**: Positions are exited at the closing price (same day)
3. **No Overnight Holding**: All positions closed by end of day
4. **Transaction Costs**: Applied on both entry and exit (round trip)

#### Step-by-Step Instructions

**Step 6.1.1: Merge Signal and Price Data**

Join the trade signals with price data on date and ticker to get entry (open) and exit (close) prices.

**Step 6.1.2: Calculate Position Returns**

For each position:
```
daily_return_pct = (exit_price - entry_price) / entry_price
```

For SELL signals (short positions), invert:
```
daily_return_pct = (entry_price - exit_price) / entry_price
```

**Step 6.1.3: Calculate Dollar PnL**

```
daily_pnl = position_value * daily_return_pct
```

**Step 6.1.4: Calculate Transaction Costs**

```
transaction_cost = position_value * transaction_cost_pct * 2  # Round trip
```

**Step 6.1.5: Calculate Net PnL**

```
net_pnl = daily_pnl - transaction_cost
```

**Step 6.1.6: Calculate Cumulative Values**

Iterate through each day and calculate:
- Cumulative PnL (running sum of net_pnl)
- Portfolio value (initial_capital + cumulative_pnl)

**Step 6.1.7: Handle HOLD Signals**

For HOLD signals:
- daily_pnl = 0
- transaction_cost = 0
- Position value remains unchanged

#### Unit Test Specification: `test_calculate_pnl()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 6.1.1 | Profitable long trade | BUY, price up 5% | Positive net_pnl |
| 6.1.2 | Losing long trade | BUY, price down 5% | Negative net_pnl |
| 6.1.3 | Profitable short trade | SELL, price down 5% | Positive net_pnl |
| 6.1.4 | Transaction cost applied | Any trade | transaction_cost > 0 |
| 6.1.5 | HOLD has zero PnL | HOLD signal | daily_pnl == 0 |
| 6.1.6 | Cumulative is cumulative | Multiple days | cumulative[-1] == sum(net_pnl) |
| 6.1.7 | Portfolio value correct | After trades | portfolio_value == initial + cumulative |
| 6.1.8 | No negative portfolio | Losing streak | portfolio_value remains valid |

---

### Task 6.2: Metric Reporter Function

#### Objective
Implement a function that calculates and displays key performance metrics for the backtested strategy.

#### Function Signature
```
report_backtest_metrics(
    pnl_data: pandas.DataFrame,
    risk_free_rate: float = 0.05
) -> Dict[str, float]
```

#### Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| pnl_data | DataFrame | Output from calculate_pnl() | Required |
| risk_free_rate | float | Annual risk-free rate for Sharpe calculation | 0.05 (5%) |

#### Output Specification

Returns a dictionary containing these metrics:

| Metric | Description | Formula |
|--------|-------------|---------|
| total_return | Total percentage return | (final_value - initial) / initial |
| total_pnl | Total dollar profit/loss | sum(net_pnl) |
| win_rate | Percentage of profitable trades | profitable_trades / total_trades |
| avg_win | Average profit on winning trades | mean(pnl where pnl > 0) |
| avg_loss | Average loss on losing trades | mean(pnl where pnl < 0) |
| profit_factor | Gross profit / Gross loss | sum(wins) / abs(sum(losses)) |
| sharpe_ratio | Risk-adjusted return | (mean_return - rf) / std_return |
| sortino_ratio | Downside risk-adjusted return | (mean_return - rf) / downside_std |
| max_drawdown | Largest peak-to-trough decline | max(peak - trough) / peak |
| calmar_ratio | Return / Max Drawdown | annual_return / max_drawdown |

#### Step-by-Step Instructions

**Step 6.2.1: Calculate Basic Return Metrics**

From the PnL data:
- Total PnL = sum of all net_pnl
- Total Return = Total PnL / Initial Capital

**Step 6.2.2: Calculate Win/Loss Metrics**

- Count winning trades (net_pnl > 0)
- Count losing trades (net_pnl < 0)
- Calculate win rate, average win, average loss

**Step 6.2.3: Calculate Sharpe Ratio**

```
daily_rf = risk_free_rate / 252  # 252 trading days
excess_returns = daily_returns - daily_rf
sharpe_ratio = mean(excess_returns) / std(excess_returns) * sqrt(252)
```

**Step 6.2.4: Calculate Sortino Ratio**

Similar to Sharpe, but using only downside deviation:
```
downside_returns = returns[returns < 0]
downside_std = std(downside_returns)
sortino_ratio = mean(excess_returns) / downside_std * sqrt(252)
```

**Step 6.2.5: Calculate Maximum Drawdown**

```
cumulative_max = cummax(portfolio_value)
drawdown = (cumulative_max - portfolio_value) / cumulative_max
max_drawdown = max(drawdown)
```

**Step 6.2.6: Format and Print Report**

Create a formatted string report displaying all metrics in a readable format. Include:
- Strategy name and test period
- Summary statistics table
- Risk metrics table
- Interpretation notes

#### Unit Test Specification: `test_report_backtest_metrics()`

| Test ID | Test Description | Input | Expected Outcome |
|---------|------------------|-------|------------------|
| 6.2.1 | All metrics calculated | Valid PnL data | All keys present in output |
| 6.2.2 | Win rate in valid range | Any data | 0.0 ≤ win_rate ≤ 1.0 |
| 6.2.3 | Max drawdown in valid range | Any data | 0.0 ≤ max_drawdown ≤ 1.0 |
| 6.2.4 | Sharpe handles zero std | All same returns | Returns NaN or Inf, no error |
| 6.2.5 | Total return matches PnL | Computed data | total_return == total_pnl / initial |
| 6.2.6 | All wins scenario | All positive PnL | win_rate == 1.0, profit_factor = inf |
| 6.2.7 | All losses scenario | All negative PnL | win_rate == 0.0 |

---

## Appendix: Project File Structure

### Recommended Directory Layout

```
finbert-trading/
│
├── README.md                    # Project overview and setup instructions
├── requirements.txt             # Python dependencies
├── environment.yml              # Conda environment file
│
├── config/
│   └── settings.py              # Configuration constants (tickers, thresholds)
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── price_fetcher.py     # Task 2.1
│   │   ├── news_fetcher.py      # Task 2.2
│   │   └── data_cleaner.py      # Task 2.3
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   ├── model_loader.py      # Task 3.1
│   │   └── sentiment_scorer.py  # Task 3.2
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── signal_aggregator.py # Task 4.1
│   │   └── feature_lagging.py   # Task 4.2
│   │
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── signal_generator.py  # Task 5.1
│   │   └── portfolio.py         # Task 5.2
│   │
│   └── backtest/
│       ├── __init__.py
│       ├── pnl_calculator.py    # Task 6.1
│       └── metrics_reporter.py  # Task 6.2
│
├── tests/
│   ├── __init__.py
│   ├── test_data/               # Test fixtures and sample data
│   ├── test_price_fetcher.py
│   ├── test_news_fetcher.py
│   ├── test_data_cleaner.py
│   ├── test_model_loader.py
│   ├── test_sentiment_scorer.py
│   ├── test_signal_aggregator.py
│   ├── test_feature_lagging.py
│   ├── test_signal_generator.py
│   ├── test_portfolio.py
│   ├── test_pnl_calculator.py
│   └── test_metrics_reporter.py
│
├── notebooks/
│   ├── 01_exploration.ipynb     # Data exploration
│   ├── 02_model_testing.ipynb   # FinBERT testing
│   └── 03_backtest_analysis.ipynb # Results visualization
│
└── output/
    ├── data/                    # Downloaded and processed data
    ├── models/                  # Cached model files
    └── reports/                 # Backtest results and metrics
```

### Running the Complete Pipeline

After implementing all tasks:

1. **Run all unit tests**:
   ```
   pytest tests/ -v
   ```

2. **Execute the full pipeline**:
   ```
   python -m src.main
   ```

3. **View backtest results**:
   Check `output/reports/` for generated metrics and visualizations.

---

## Summary

This walkthrough has guided you through building a complete sentiment-based trading strategy:

| Section | Tasks | Key Deliverable |
|---------|-------|-----------------|
| 1.0 | 2 | GPU-enabled Python environment |
| 2.0 | 3 | Clean, aligned price + news data |
| 3.0 | 2 | FinBERT sentiment scoring pipeline |
| 4.0 | 2 | Lag-adjusted sentiment alpha features |
| 5.0 | 2 | Trading signals and portfolio allocation |
| 6.0 | 2 | Backtest results with performance metrics |

**Total**: 13 atomic tasks, each with corresponding unit tests.

### Next Steps

After completing this project, consider:

1. **Extending the time period**: Test with 30, 60, or 90 days of data
2. **Adding more stocks**: Expand beyond the Magnificent Seven
3. **Trying different models**: Compare FinBERT with other sentiment models
4. **Implementing position sizing**: Use Kelly Criterion or volatility targeting
5. **Adding risk management**: Implement stop-losses and position limits

---

*Document Version: 1.0*  
*Created: November 2025*  
*Target Hardware: NVIDIA RTX 5090, CUDA 12.8+, PyTorch 2.7+*
