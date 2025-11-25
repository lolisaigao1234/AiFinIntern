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



if __name__ == "__main__":
    ticker_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]


    for ticker in ticker_list:
        if check_ticker_validity(ticker):
            data = fetch_price_data(ticker, "2025-11-17", "2025-11-21")
            print(data)