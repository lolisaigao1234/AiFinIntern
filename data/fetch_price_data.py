import torch
import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import pandas_market_calendars as mcal 

def check_ticker_validity(ticker: str) -> bool:
    """Checks if the ticker symbol is valid."""
    try:
        yf.Ticker(ticker)
        return True
    except Exception:
        return False

def calculate_date_range(days: int) -> tuple:
    """Calculates the date range for the given start and end dates."""
    end_date = pd.to_datetime(pd.Timestamp.today().strftime("%Y-%m-%d"))
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=days) * 1.5
    return (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

def fetch_price_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches price data for a given ticker symbol from Yahoo Finance."""
    
    # Download the data
    data = yf.download(ticker, start=start_date, end=end_date)

    df = pd.DataFrame(data).reset_index()
    print(df.head())
    print(df.columns)
    print(df.index)
    print(df.dtypes)
    return df

def filter_to_market_data_only(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the data to only include market data."""
    days = df["Date"]
    valid_days = mcal.get_calendar("NYSE").valid_days(start_date, end_date)
    for day in days:
        if day not in valid_days:
            df = df.drop(day)

    return df

def trim_to_exact_num_of_days(df: pd.DataFrame, num_of_days: int) -> pd.DataFrame:
    """Trims the data to only include the exact number of days."""
    return df.tail(num_of_days)


def clean_and_validate_output(df: pd.DataFrame):
    """Cleans and validates the output data."""
    opens = df["Open"]
    closes = df["Close"]
    volumes = df["Volume"]
    date = df["Date"]
    
    if opens.isnull().values.any() or closes.isnull().values.any() or volumes.isnull().values.any():
        raise ValueError("Output data contains null values.")

    if opens < 0 or closes < 0 or volumes < 0:
        raise ValueError("Output data contains negative values.")
    
    if date.isnull().values.any():
        raise ValueError("Output data contains null values.")

    if date != sorted(date):
        raise ValueError("Output data is not sorted by date in ascending order.")

    if len(opens) != len(closes) or len(opens) != len(volumes) or len(opens) != len(date):
        raise ValueError("Output data has different lengths.")

    if len(opens) != num_of_days:
        raise ValueError("Output data has different lengths.")

    if len(closes) != num_of_days:
        raise ValueError("Output data has different lengths.")

    if len(volumes) != num_of_days:
        raise ValueError("Output data has different lengths.")

    if len(date) != num_of_days:
        raise ValueError("Output data has different lengths.")

    if volumes < 0:
        raise ValueError("Output data contains negative values.")

    print("Output data is valid.")

if __name__ == "__main__":
    ticker_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]


    for ticker in ticker_list:
        if check_ticker_validity(ticker):
            data = fetch_price_data(ticker, "2025-11-17", "2025-11-21")
            print(data)