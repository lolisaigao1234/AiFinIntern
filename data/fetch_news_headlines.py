"""
Task 2.2: News Data Fetcher Function

Fetches financial news headlines for Magnificent Seven stocks using Yahoo Finance RSS feeds.
"""

import feedparser
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Magnificent Seven tickers
MAGNIFICENT_SEVEN = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META'}


def fetch_news_headlines(ticker: str, days: int = 10) -> pd.DataFrame:
    """
    Fetch financial news headlines for a specific stock ticker.
    
    Retrieves news headlines from Yahoo Finance RSS feeds for use as input
    to the FinBERT sentiment model.
    
    Parameters
    ----------
    ticker : str
        Stock ticker symbol. Must be one of the Magnificent Seven:
        AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META
    days : int, optional
        Number of days of news to fetch. Must be between 1 and 10.
        Default is 10.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - date (datetime64): Publication date
        - ticker (str): Associated stock ticker
        - headline (str): News headline text
        - source (str): News source name
        
    Raises
    ------
    ValueError
        If ticker is not in Magnificent Seven or days is out of range (1-10).
        
    Examples
    --------
    >>> df = fetch_news_headlines("AAPL", days=5)
    >>> df.columns.tolist()
    ['date', 'ticker', 'headline', 'source']
    """
    # Step 2.2.2: Input Validation
    if not isinstance(ticker, str):
        raise ValueError(f"ticker must be a string, got {type(ticker).__name__}")
    
    ticker_upper = ticker.upper().strip()
    if ticker_upper not in MAGNIFICENT_SEVEN:
        raise ValueError(
            f"Invalid ticker '{ticker}'. Must be one of: {', '.join(sorted(MAGNIFICENT_SEVEN))}"
        )
    
    if not isinstance(days, int):
        raise ValueError(f"days must be an integer, got {type(days).__name__}")
    
    if not (1 <= days <= 10):
        raise ValueError(f"days must be between 1 and 10, got {days}")
    
    # Step 2.2.3: Construct the RSS URL
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker_upper}"
    
    # Step 2.2.4: Fetch and Parse Response
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        logger.error(f"Failed to fetch RSS feed for {ticker_upper}: {e}")
        return _empty_dataframe()
    
    # Check for feed errors
    if feed.bozo and not feed.entries:
        logger.warning(f"RSS feed parsing error for {ticker_upper}: {feed.bozo_exception}")
        return _empty_dataframe()
    
    # Step 2.2.5 & 2.2.6: Extract fields and filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    headlines_data = []
    
    for entry in feed.entries:
        # Parse publication date
        pub_date = _parse_entry_date(entry)
        if pub_date is None:
            continue
        
        # Filter by date range (only include headlines within the specified days)
        if pub_date < cutoff_date:
            continue
        
        # Extract headline text
        headline = entry.get('title', '').strip()
        if not headline:
            continue
        
        # Extract source if available
        source = _extract_source(entry)
        
        headlines_data.append({
            'date': pub_date,
            'ticker': ticker_upper,
            'headline': headline,
            'source': source
        })
    
    # Step 2.2.7: Handle Empty Results
    if not headlines_data:
        logger.warning(f"No headlines found for {ticker_upper} in the last {days} days")
        return _empty_dataframe()
    
    # Create DataFrame
    df = pd.DataFrame(headlines_data)
    
    # Ensure date column is datetime64
    df['date'] = pd.to_datetime(df['date'])
    
    # Step 2.2.8: Deduplicate Headlines (same headline text on same date)
    df = df.drop_duplicates(subset=['headline', 'date'])
    
    # Sort by date descending (most recent first)
    df = df.sort_values('date', ascending=False).reset_index(drop=True)
    
    logger.info(f"Fetched {len(df)} headlines for {ticker_upper}")
    
    return df


def _empty_dataframe() -> pd.DataFrame:
    """Return an empty DataFrame with the correct schema."""
    return pd.DataFrame(columns=['date', 'ticker', 'headline', 'source']).astype({
        'date': 'datetime64[ns]',
        'ticker': 'str',
        'headline': 'str',
        'source': 'str'
    })


def _parse_entry_date(entry) -> datetime | None:
    """
    Parse the publication date from an RSS feed entry.
    
    Parameters
    ----------
    entry : feedparser.FeedParserDict
        A single entry from the RSS feed.
        
    Returns
    -------
    datetime or None
        The parsed datetime, or None if parsing failed.
    """
    # Try published_parsed first
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6])
        except (TypeError, ValueError):
            pass
    
    # Fall back to updated_parsed
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6])
        except (TypeError, ValueError):
            pass
    
    # Try parsing from string fields
    for date_field in ['published', 'updated']:
        date_str = entry.get(date_field)
        if date_str:
            try:
                return pd.to_datetime(date_str).to_pydatetime()
            except (ValueError, TypeError):
                pass
    
    return None


def _extract_source(entry) -> str:
    """
    Extract the source name from an RSS feed entry.
    
    Parameters
    ----------
    entry : feedparser.FeedParserDict
        A single entry from the RSS feed.
        
    Returns
    -------
    str
        The source name, defaults to 'Yahoo Finance' if not found.
    """
    # Try to get source from the entry
    if hasattr(entry, 'source') and entry.source:
        source_title = entry.source.get('title', '')
        if source_title:
            return source_title
    
    # Check for publisher field
    publisher = entry.get('publisher', '')
    if publisher:
        return publisher
    
    # Default to Yahoo Finance
    return 'Yahoo Finance'


if __name__ == "__main__":
    # Quick test
    for ticker in ['AAPL', 'NVDA']:
        print(f"\n--- Headlines for {ticker} ---")
        df = fetch_news_headlines(ticker, days=5)
        print(f"Found {len(df)} headlines")
        if not df.empty:
            print(df.head())