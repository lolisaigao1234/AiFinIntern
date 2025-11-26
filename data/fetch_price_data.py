"""
Price Data Fetcher Module - Task 2.1

Fetches historical OHLCV price data for the Magnificent Seven stocks
from Yahoo Finance, ensuring after-hours trading data is excluded.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Tuple, Optional
import pandas_market_calendars as mcal

# Valid tickers for the Magnificent Seven
VALID_TICKERS = ("AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META")

# Constraints for days parameter
MIN_DAYS = 1
MAX_DAYS = 10


def check_ticker_validity(ticker: str) -> bool:
    """
    Checks if the ticker symbol is valid by verifying it returns actual data.
    
    Args:
        ticker: Stock ticker symbol to validate.
        
    Returns:
        True if ticker is valid and has data, False otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        # yfinance doesn't raise exception for invalid tickers,
        # so we need to check if we can get actual data
        info = stock.info
        # Check if the ticker has meaningful data
        return info is not None and len(info) > 0 and info.get("regularMarketPrice") is not None
    except Exception:
        return False


def validate_inputs(ticker: str, days: int) -> None:
    """
    Validates the input parameters for fetch_price_data.
    
    Args:
        ticker: Stock ticker symbol.
        days: Number of trading days to fetch.
        
    Raises:
        ValueError: If ticker is invalid or days is out of range.
    """
    if ticker not in VALID_TICKERS:
        raise ValueError(
            f"Invalid ticker '{ticker}'. Must be one of: {', '.join(VALID_TICKERS)}"
        )
    
    # Check for bool first since bool is a subclass of int in Python
    if isinstance(days, bool) or not isinstance(days, int):
        raise ValueError(f"Days must be an integer, got {type(days).__name__}")
    
    if days < MIN_DAYS or days > MAX_DAYS:
        raise ValueError(
            f"Days must be between {MIN_DAYS} and {MAX_DAYS}, got {days}"
        )


def calculate_date_range(days: int) -> Tuple[str, str]:
    """
    Calculates the date range for fetching data.
    
    Uses a 1.5x multiplier to account for weekends and holidays,
    ensuring we fetch enough data to get the requested number of trading days.
    
    Args:
        days: Number of trading days requested.
        
    Returns:
        Tuple of (start_date, end_date) as strings in 'YYYY-MM-DD' format.
    """
    end_date = pd.Timestamp.today().normalize()
    # Use 1.5x multiplier to account for weekends and holidays
    start_date = end_date - pd.Timedelta(days=int(days * 1.5))
    return (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))


def fetch_raw_price_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches raw price data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol.
        start_date: Start date in 'YYYY-MM-DD' format.
        end_date: End date in 'YYYY-MM-DD' format.
        
    Returns:
        DataFrame with OHLCV data and Date column.
    """
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if data.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'")
    
    # Reset index to make Date a column
    df = pd.DataFrame(data).reset_index()
    
    # Handle multi-level columns from yfinance (when single ticker)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if col[1] == '' or col[1] == ticker else col[0] 
                      for col in df.columns]
    
    return df


def filter_to_market_data_only(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Filters the data to only include valid NYSE trading days.
    
    Args:
        df: DataFrame with 'Date' column.
        start_date: Start date for calendar lookup.
        end_date: End date for calendar lookup.
        
    Returns:
        DataFrame filtered to only valid trading days.
    """
    nyse = mcal.get_calendar("NYSE")
    valid_days = nyse.valid_days(start_date=start_date, end_date=end_date)
    
    # Convert valid_days to date only for comparison
    valid_dates = pd.to_datetime(valid_days.date)
    
    # Convert df Date column to date only for comparison
    df_dates = pd.to_datetime(df["Date"]).dt.normalize()
    
    # Filter using boolean indexing
    mask = df_dates.isin(valid_dates)
    return df[mask].reset_index(drop=True)


def trim_to_exact_num_of_days(df: pd.DataFrame, num_of_days: int) -> pd.DataFrame:
    """
    Trims the data to only include the exact number of most recent days.
    
    Args:
        df: DataFrame to trim.
        num_of_days: Number of rows to keep.
        
    Returns:
        DataFrame with exactly num_of_days rows (or fewer if not enough data).
    """
    return df.tail(num_of_days).reset_index(drop=True)


def clean_and_validate_output(df: pd.DataFrame, num_of_days: int) -> None:
    """
    Cleans and validates the output data.
    
    Args:
        df: DataFrame to validate.
        num_of_days: Expected number of rows.
        
    Raises:
        ValueError: If validation fails.
    """
    required_columns = ["Date", "Open", "Close", "Volume"]
    
    # Check required columns exist
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    opens = df["Open"]
    closes = df["Close"]
    volumes = df["Volume"]
    dates = df["Date"]
    
    # Check for null values in price columns
    if opens.isnull().any():
        raise ValueError("Output data contains null values in Open column.")
    if closes.isnull().any():
        raise ValueError("Output data contains null values in Close column.")
    if volumes.isnull().any():
        raise ValueError("Output data contains null values in Volume column.")
    if dates.isnull().any():
        raise ValueError("Output data contains null values in Date column.")
    
    # Check for negative values (use .any() for Series comparison)
    if (opens < 0).any():
        raise ValueError("Output data contains negative values in Open column.")
    if (closes < 0).any():
        raise ValueError("Output data contains negative values in Close column.")
    if (volumes < 0).any():
        raise ValueError("Output data contains negative values in Volume column.")
    
    # Check dates are sorted in ascending order
    if not dates.is_monotonic_increasing:
        raise ValueError("Output data is not sorted by date in ascending order.")
    
    # Check all dates are weekdays (Monday=0 to Friday=4)
    weekdays = pd.to_datetime(dates).dt.dayofweek
    if (weekdays > 4).any():
        raise ValueError("Output data contains weekend dates.")
    
    # Check length matches expected
    if len(df) != num_of_days:
        raise ValueError(
            f"Output data has {len(df)} rows, expected {num_of_days}."
        )


def fetch_price_data(ticker: str, days: int = 10) -> pd.DataFrame:
    """
    Fetches historical OHLCV price data for a given ticker symbol.
    
    This is the main entry point for Task 2.1. It fetches data from Yahoo Finance,
    filters to valid trading days, and validates the output.
    
    Args:
        ticker: Stock ticker symbol. Must be one of: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META
        days: Number of trading days to fetch (1-10, default 10).
        
    Returns:
        pandas DataFrame with columns: Date, Open, High, Low, Close, Volume, Adj Close
        
    Raises:
        ValueError: If ticker is invalid, days is out of range, or data validation fails.
    """
    # Step 2.1.2: Validate inputs
    validate_inputs(ticker, days)
    
    # Step 2.1.3: Calculate date range
    start_date, end_date = calculate_date_range(days)
    
    # Step 2.1.4: Fetch data from yfinance
    df = fetch_raw_price_data(ticker, start_date, end_date)
    
    # Step 2.1.5: Filter to market hours data only
    df = filter_to_market_data_only(df, start_date, end_date)
    
    # Step 2.1.6: Trim to exact number of days
    df = trim_to_exact_num_of_days(df, days)
    
    # Step 2.1.7: Clean and validate output
    clean_and_validate_output(df, days)
    
    return df


if __name__ == "__main__":
    # Test with all Magnificent Seven tickers
    ticker_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]
    
    for ticker in ticker_list:
        print(f"\n{'='*50}")
        print(f"Fetching data for {ticker}")
        print('='*50)
        try:
            data = fetch_price_data(ticker, days=5)
            print(data)
            print(f"\nColumns: {data.columns.tolist()}")
            print(f"Shape: {data.shape}")
        except Exception as e:
            print(f"Error: {e}")