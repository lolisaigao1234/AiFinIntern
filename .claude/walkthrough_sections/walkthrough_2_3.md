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