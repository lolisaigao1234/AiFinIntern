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
