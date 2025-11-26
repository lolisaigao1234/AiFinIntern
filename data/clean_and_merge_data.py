"""
Data Cleaner and Merger Module for Financial News and Price Data

This module provides functionality to preprocess news headlines (removing noise)
and align them with corresponding trading day price data for FinBERT-based
sentiment analysis.

Author: Financial Data Pipeline
Version: 1.0.0
"""

import re
import html
import unicodedata
from typing import List, Optional, Union
import pandas as pd
import numpy as np


# Compile regex patterns once for performance
URL_PATTERN = re.compile(
    r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*|'
    r'www\.(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*',
    re.IGNORECASE
)

# Ticker pattern: $AAPL, $MSFT, etc.
TICKER_PATTERN = re.compile(r'\$[A-Za-z]{1,5}\b')

# Emoji and special character pattern (keeps alphanumeric, basic punctuation, spaces)
# Basic punctuation includes: . , ! ? ' " - : ; ( ) [ ] { } / \ @ # % & * + = < > | ~ `
SPECIAL_CHAR_PATTERN = re.compile(
    r'[^\w\s\.\,\!\?\'\"\-\:\;\(\)\[\]\{\}\/\\\@\#\%\&\*\+\=\<\>\|\~\`]',
    re.UNICODE
)

# Whitespace normalization pattern
WHITESPACE_PATTERN = re.compile(r'\s+')

# HTML tag pattern
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')


def clean_headline(
    text: str,
    remove_urls: bool = True,
    remove_html_entities: bool = True,
    remove_emojis: bool = True,
    remove_special_chars: bool = True,
    normalize_whitespace: bool = True,
    strip_whitespace: bool = True,
    remove_tickers: bool = True,
    lowercase: bool = False,
    remove_html_tags: bool = True
) -> str:
    """
    Clean a single headline by applying various text preprocessing operations.
    
    Parameters
    ----------
    text : str
        The headline text to clean.
    remove_urls : bool, default=True
        Remove HTTP/HTTPS URLs from the text.
    remove_html_entities : bool, default=True
        Convert HTML entities (e.g., &amp;) to their character equivalents.
    remove_emojis : bool, default=True
        Remove emoji characters from the text.
    remove_special_chars : bool, default=True
        Remove special characters, keeping only alphanumeric and basic punctuation.
    normalize_whitespace : bool, default=True
        Collapse multiple whitespace characters to a single space.
    strip_whitespace : bool, default=True
        Remove leading and trailing whitespace.
    remove_tickers : bool, default=True
        Remove stock ticker symbols (e.g., $AAPL).
    lowercase : bool, default=False
        Convert text to lowercase (optional for FinBERT as it handles case).
    remove_html_tags : bool, default=True
        Remove HTML tags from the text.
    
    Returns
    -------
    str
        The cleaned headline text.
    
    Raises
    ------
    TypeError
        If text is not a string.
    """
    # Type validation
    if text is None:
        return ""
    
    # Handle pandas/numpy NaN values
    try:
        if pd.isna(text):
            return ""
    except (TypeError, ValueError):
        pass  # Not a type that pd.isna can check
    
    if not isinstance(text, str):
        # Attempt to convert to string
        try:
            text = str(text)
            # Check if conversion resulted in 'nan' string
            if text.lower() == 'nan':
                return ""
        except Exception:
            return ""
    
    # Handle empty or whitespace-only strings
    if not text or not text.strip():
        return ""
    
    result = text
    
    # Step 1: Remove HTML tags first (before entity conversion)
    if remove_html_tags:
        result = HTML_TAG_PATTERN.sub(' ', result)
    
    # Step 2: Convert HTML entities (e.g., &amp; -> &)
    if remove_html_entities:
        result = html.unescape(result)
    
    # Step 3: Remove URLs
    if remove_urls:
        result = URL_PATTERN.sub('', result)
    
    # Step 4: Remove ticker symbols
    if remove_tickers:
        result = TICKER_PATTERN.sub('', result)
    
    # Step 5: Remove emojis and special characters
    if remove_emojis or remove_special_chars:
        # First, normalize unicode to decomposed form for consistent handling
        result = unicodedata.normalize('NFKD', result)
        
        # Remove emojis by filtering out characters in emoji ranges
        if remove_emojis:
            cleaned_chars = []
            for char in result:
                # Check if character is an emoji
                if not _is_emoji(char):
                    cleaned_chars.append(char)
            result = ''.join(cleaned_chars)
        
        # Remove remaining special characters
        if remove_special_chars:
            result = SPECIAL_CHAR_PATTERN.sub('', result)
    
    # Step 6: Normalize whitespace (collapse multiple spaces to single)
    if normalize_whitespace:
        result = WHITESPACE_PATTERN.sub(' ', result)
    
    # Step 7: Strip leading/trailing whitespace
    if strip_whitespace:
        result = result.strip()
    
    # Step 8: Lowercase conversion (optional)
    if lowercase:
        result = result.lower()
    
    return result


def _is_emoji(char: str) -> bool:
    """
    Check if a character is an emoji.
    
    Parameters
    ----------
    char : str
        A single character to check.
    
    Returns
    -------
    bool
        True if the character is an emoji, False otherwise.
    """
    if len(char) != 1:
        return False
    
    code_point = ord(char)
    
    # Common emoji ranges
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map
        (0x1F1E0, 0x1F1FF),  # Flags
        (0x2600, 0x26FF),    # Misc symbols
        (0x2700, 0x27BF),    # Dingbats
        (0xFE00, 0xFE0F),    # Variation Selectors
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1FA00, 0x1FA6F),  # Chess Symbols
        (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
        (0x231A, 0x231B),    # Watch, Hourglass
        (0x23E9, 0x23F3),    # Various symbols
        (0x23F8, 0x23FA),    # Various symbols
        (0x25AA, 0x25AB),    # Squares
        (0x25B6, 0x25B6),    # Play button
        (0x25C0, 0x25C0),    # Reverse button
        (0x25FB, 0x25FE),    # Squares
        (0x2614, 0x2615),    # Umbrella, Hot beverage
        (0x2648, 0x2653),    # Zodiac
        (0x267F, 0x267F),    # Wheelchair
        (0x2693, 0x2693),    # Anchor
        (0x26A1, 0x26A1),    # High voltage
        (0x26AA, 0x26AB),    # Circles
        (0x26BD, 0x26BE),    # Sports
        (0x26C4, 0x26C5),    # Snowman, Sun
        (0x26CE, 0x26CE),    # Ophiuchus
        (0x26D4, 0x26D4),    # No entry
        (0x26EA, 0x26EA),    # Church
        (0x26F2, 0x26F3),    # Fountain, Golf
        (0x26F5, 0x26F5),    # Sailboat
        (0x26FA, 0x26FA),    # Tent
        (0x26FD, 0x26FD),    # Fuel pump
        (0x2702, 0x2702),    # Scissors
        (0x2705, 0x2705),    # Check mark
        (0x2708, 0x270D),    # Various
        (0x270F, 0x270F),    # Pencil
        (0x2712, 0x2712),    # Black nib
        (0x2714, 0x2714),    # Check mark
        (0x2716, 0x2716),    # X mark
        (0x271D, 0x271D),    # Latin cross
        (0x2721, 0x2721),    # Star of David
        (0x2728, 0x2728),    # Sparkles
        (0x2733, 0x2734),    # Various
        (0x2744, 0x2744),    # Snowflake
        (0x2747, 0x2747),    # Sparkle
        (0x274C, 0x274C),    # Cross mark
        (0x274E, 0x274E),    # Cross mark
        (0x2753, 0x2755),    # Question marks
        (0x2757, 0x2757),    # Exclamation
        (0x2763, 0x2764),    # Heart
        (0x2795, 0x2797),    # Math symbols
        (0x27A1, 0x27A1),    # Arrow
        (0x27B0, 0x27B0),    # Curly loop
        (0x27BF, 0x27BF),    # Double curly loop
        (0x2934, 0x2935),    # Arrows
        (0x2B05, 0x2B07),    # Arrows
        (0x2B1B, 0x2B1C),    # Squares
        (0x2B50, 0x2B50),    # Star
        (0x2B55, 0x2B55),    # Circle
        (0x3030, 0x3030),    # Wavy dash
        (0x303D, 0x303D),    # Part alternation mark
        (0x3297, 0x3297),    # Circled Ideograph Congratulation
        (0x3299, 0x3299),    # Circled Ideograph Secret
    ]
    
    for start, end in emoji_ranges:
        if start <= code_point <= end:
            return True
    
    return False


def validate_price_dataframe(df: pd.DataFrame) -> tuple:
    """
    Validate the structure and content of a price DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        The price DataFrame to validate.
    
    Returns
    -------
    tuple
        (is_valid: bool, error_message: str or None)
    """
    if df is None:
        return False, "Price DataFrame is None"
    
    if not isinstance(df, pd.DataFrame):
        return False, f"Expected DataFrame, got {type(df).__name__}"
    
    if df.empty:
        return True, None  # Empty DataFrame is valid
    
    required_columns = ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing required columns: {missing_cols}"
    
    # Validate no NaN in critical columns
    for col in ['date', 'ticker']:
        if df[col].isna().any():
            return False, f"NaN values found in column '{col}'"
    
    return True, None


def validate_news_dataframe(df: pd.DataFrame) -> tuple:
    """
    Validate the structure and content of a news DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        The news DataFrame to validate.
    
    Returns
    -------
    tuple
        (is_valid: bool, error_message: str or None)
    """
    if df is None:
        return False, "News DataFrame is None"
    
    if not isinstance(df, pd.DataFrame):
        return False, f"Expected DataFrame, got {type(df).__name__}"
    
    if df.empty:
        return True, None  # Empty DataFrame is valid
    
    required_columns = ['date', 'headline']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing required columns: {missing_cols}"
    
    return True, None


def normalize_date(
    date_value: Union[str, pd.Timestamp, np.datetime64],
    errors: str = 'coerce'
) -> Optional[pd.Timestamp]:
    """
    Normalize a date value to a pandas Timestamp without time component.
    
    Parameters
    ----------
    date_value : Union[str, pd.Timestamp, np.datetime64]
        The date value to normalize.
    errors : str, default='coerce'
        How to handle errors: 'coerce' returns NaT, 'raise' raises exception.
    
    Returns
    -------
    Optional[pd.Timestamp]
        Normalized date or NaT if invalid and errors='coerce'.
    """
    try:
        if pd.isna(date_value):
            return pd.NaT
        
        # Convert to Timestamp
        ts = pd.to_datetime(date_value, errors=errors)
        
        if pd.isna(ts):
            return pd.NaT
        
        # Remove time component and timezone
        if hasattr(ts, 'tz') and ts.tz is not None:
            ts = ts.tz_localize(None)
        
        return ts.normalize()
    
    except Exception as e:
        if errors == 'raise':
            raise ValueError(f"Cannot normalize date: {date_value}") from e
        return pd.NaT


def clean_and_merge_data(
    price_data: pd.DataFrame,
    news_data: pd.DataFrame,
    date_column: str = 'date',
    headline_column: str = 'headline',
    ticker_column: str = 'ticker',
    clean_options: Optional[dict] = None,
    validate_inputs: bool = True,
    validate_outputs: bool = True
) -> pd.DataFrame:
    """
    Preprocess news headlines and align them with corresponding trading day price data.
    
    This function performs the following operations:
    1. Validates input DataFrames
    2. Cleans all headlines using text preprocessing
    3. Normalizes date formats in both DataFrames
    4. Aggregates headlines by date into lists
    5. Performs a left join of price data with news data
    6. Handles missing news days with empty lists
    7. Validates output DataFrame
    
    Parameters
    ----------
    price_data : pd.DataFrame
        Output from fetch_price_data() containing OHLCV data.
        Required columns: date, ticker, open, high, low, close, volume
    news_data : pd.DataFrame
        Output from fetch_news_headlines() containing headlines.
        Required columns: date, headline
    date_column : str, default='date'
        Name of the date column in both DataFrames.
    headline_column : str, default='headline'
        Name of the headline column in news_data.
    ticker_column : str, default='ticker'
        Name of the ticker column in price_data.
    clean_options : dict, optional
        Options to pass to clean_headline function.
    validate_inputs : bool, default=True
        Whether to validate input DataFrames.
    validate_outputs : bool, default=True
        Whether to validate output DataFrame.
    
    Returns
    -------
    pd.DataFrame
        Merged DataFrame with columns:
        - date: Trading date (datetime64)
        - ticker: Stock ticker (str)
        - open: Opening price (float64)
        - high: High price (float64)
        - low: Low price (float64)
        - close: Closing price (float64)
        - volume: Trading volume (int64)
        - headlines: List of cleaned headlines (list[str])
        - headline_count: Number of headlines (int)
    
    Raises
    ------
    TypeError
        If inputs are not DataFrames.
    ValueError
        If required columns are missing or data is invalid.
    
    Examples
    --------
    >>> price_df = pd.DataFrame({
    ...     'date': ['2024-01-02'],
    ...     'ticker': ['AAPL'],
    ...     'open': [185.0],
    ...     'high': [186.0],
    ...     'low': [184.0],
    ...     'close': [185.5],
    ...     'volume': [1000000]
    ... })
    >>> news_df = pd.DataFrame({
    ...     'date': ['2024-01-02'],
    ...     'headline': ['Apple stock rises on strong earnings']
    ... })
    >>> result = clean_and_merge_data(price_df, news_df)
    >>> result['headline_count'].iloc[0]
    1
    """
    # Default clean options
    if clean_options is None:
        clean_options = {}
    
    # Step 1: Input validation
    if validate_inputs:
        # Validate price data
        is_valid, error_msg = validate_price_dataframe(price_data)
        if not is_valid:
            raise ValueError(f"Invalid price_data: {error_msg}")
        
        # Validate news data
        is_valid, error_msg = validate_news_dataframe(news_data)
        if not is_valid:
            raise ValueError(f"Invalid news_data: {error_msg}")
    
    # Handle empty price data
    if price_data is None or price_data.empty:
        # Return empty DataFrame with correct schema
        return pd.DataFrame({
            'date': pd.Series(dtype='datetime64[ns]'),
            'ticker': pd.Series(dtype='str'),
            'open': pd.Series(dtype='float64'),
            'high': pd.Series(dtype='float64'),
            'low': pd.Series(dtype='float64'),
            'close': pd.Series(dtype='float64'),
            'volume': pd.Series(dtype='int64'),
            'headlines': pd.Series(dtype='object'),
            'headline_count': pd.Series(dtype='int64')
        })
    
    # Step 2: Create copies to avoid modifying originals
    price_df = price_data.copy()
    news_df = news_data.copy() if news_data is not None and not news_data.empty else pd.DataFrame()
    
    # Step 3: Normalize date formats in price data
    price_df[date_column] = price_df[date_column].apply(
        lambda x: normalize_date(x, errors='coerce')
    )
    
    # Remove rows with invalid dates in price data
    invalid_dates = price_df[date_column].isna()
    if invalid_dates.any():
        price_df = price_df[~invalid_dates].copy()
    
    # Step 4: Clean and process news data
    if news_df.empty:
        # No news data - create empty aggregation
        aggregated_news = pd.DataFrame({
            date_column: pd.Series(dtype='datetime64[ns]'),
            'headlines': pd.Series(dtype='object'),
            'headline_count': pd.Series(dtype='int64')
        })
    else:
        # Normalize date formats in news data
        news_df[date_column] = news_df[date_column].apply(
            lambda x: normalize_date(x, errors='coerce')
        )
        
        # Remove rows with invalid dates in news data
        invalid_dates = news_df[date_column].isna()
        if invalid_dates.any():
            news_df = news_df[~invalid_dates].copy()
        
        # Clean headlines
        news_df['cleaned_headline'] = news_df[headline_column].apply(
            lambda x: clean_headline(x, **clean_options)
        )
        
        # Filter out empty headlines after cleaning
        news_df = news_df[news_df['cleaned_headline'].str.len() > 0].copy()
        
        # Aggregate headlines by date
        if news_df.empty:
            aggregated_news = pd.DataFrame({
                date_column: pd.Series(dtype='datetime64[ns]'),
                'headlines': pd.Series(dtype='object'),
                'headline_count': pd.Series(dtype='int64')
            })
        else:
            aggregated_news = news_df.groupby(date_column).agg(
                headlines=('cleaned_headline', list),
                headline_count=('cleaned_headline', 'count')
            ).reset_index()
    
    # Step 5: Merge price data with aggregated news (left join)
    merged_df = price_df.merge(
        aggregated_news,
        on=date_column,
        how='left'
    )
    
    # Step 6: Handle missing news days
    # Replace NaN headlines with empty lists
    merged_df['headlines'] = merged_df['headlines'].apply(
        lambda x: x if isinstance(x, list) else []
    )
    
    # Replace NaN headline_count with 0
    merged_df['headline_count'] = merged_df['headline_count'].fillna(0).astype('int64')
    
    # Step 7: Ensure correct column order and types
    output_columns = [
        'date', 'ticker', 'open', 'high', 'low', 'close', 'volume',
        'headlines', 'headline_count'
    ]
    
    # Ensure all required columns exist
    for col in output_columns:
        if col not in merged_df.columns:
            if col == 'headlines':
                merged_df[col] = [[] for _ in range(len(merged_df))]
            elif col == 'headline_count':
                merged_df[col] = 0
            else:
                merged_df[col] = None
    
    # Select and order columns
    merged_df = merged_df[output_columns].copy()
    
    # Ensure correct data types
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    merged_df['ticker'] = merged_df['ticker'].astype(str)
    merged_df['open'] = merged_df['open'].astype('float64')
    merged_df['high'] = merged_df['high'].astype('float64')
    merged_df['low'] = merged_df['low'].astype('float64')
    merged_df['close'] = merged_df['close'].astype('float64')
    merged_df['volume'] = merged_df['volume'].astype('int64')
    merged_df['headline_count'] = merged_df['headline_count'].astype('int64')
    
    # Step 8: Final validation
    if validate_outputs:
        # Check no NaN in price columns
        price_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in price_cols:
            if merged_df[col].isna().any():
                raise ValueError(f"NaN values found in output column '{col}'")
        
        # Check all headline_counts are >= 0
        if (merged_df['headline_count'] < 0).any():
            raise ValueError("Negative headline_count values found")
        
        # Verify headlines column contains lists
        if not merged_df['headlines'].apply(lambda x: isinstance(x, list)).all():
            raise ValueError("headlines column must contain lists")
    
    return merged_df


def clean_headlines_batch(
    headlines: List[str],
    clean_options: Optional[dict] = None
) -> List[str]:
    """
    Clean a batch of headlines.
    
    Parameters
    ----------
    headlines : List[str]
        List of headlines to clean.
    clean_options : dict, optional
        Options to pass to clean_headline function.
    
    Returns
    -------
    List[str]
        List of cleaned headlines (empty strings filtered out).
    """
    if clean_options is None:
        clean_options = {}
    
    cleaned = []
    for headline in headlines:
        result = clean_headline(headline, **clean_options)
        if result:  # Only include non-empty results
            cleaned.append(result)
    
    return cleaned


# Convenience function for testing
def create_sample_data() -> tuple:
    """
    Create sample price and news DataFrames for testing.
    
    Returns
    -------
    tuple
        (price_df, news_df)
    """
    price_df = pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02', '2024-01-03', '2024-01-04']),
        'ticker': ['AAPL', 'AAPL', 'AAPL'],
        'open': [185.0, 186.0, 184.0],
        'high': [186.5, 187.0, 185.5],
        'low': [184.5, 185.0, 183.0],
        'close': [186.0, 184.5, 185.0],
        'volume': [1000000, 1200000, 900000]
    })
    
    news_df = pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02', '2024-01-02', '2024-01-04']),
        'headline': [
            'Apple announces new product line',
            'Tech stocks rally on strong earnings',
            'Market volatility increases amid uncertainty'
        ]
    })
    
    return price_df, news_df


if __name__ == '__main__':
    # Demo usage
    price_df, news_df = create_sample_data()
    result = clean_and_merge_data(price_df, news_df)
    print("Sample merged data:")
    print(result)
    print("\nColumns:", result.columns.tolist())
    print("Dtypes:")
    print(result.dtypes)