import yfinance as yf
import pandas as pd
import os


def fetch_news_headlines(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    days = (end_date - start_date).days
    df = pd.DataFrame(columns=['Date', 'Ticker', 'Headline', 'Source'])

    
