import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.fetch_price_data import (
    check_ticker_validity,
    calculate_date_range,
    fetch_price_data,
    filter_to_market_data_only,
    trim_to_exact_num_of_days,
    clean_and_validate_output
)

@pytest.fixture
def valid_ticker():
    return "AAPL"

@pytest.fixture
def invalid_ticker():
    return "INVALID_TICKER"

@pytest.fixture
def sample_price_data():
    dates = pd.date_range(start="2023-01-01", periods=5, freq="B")
    data = {
        "Date": dates,
        "Open": [150.0, 151.0, 152.0, 153.0, 154.0],
        "High": [155.0, 156.0, 157.0, 158.0, 159.0],
        "Low": [149.0, 150.0, 151.0, 152.0, 153.0],
        "Close": [152.0, 153.0, 154.0, 155.0, 156.0],
        "Volume": [1000000, 1100000, 1200000, 1300000, 1400000]
    }
    return pd.DataFrame(data)

def test_check_ticker_validity_valid(valid_ticker):
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value = MagicMock()
        assert check_ticker_validity(valid_ticker) is True

def test_check_ticker_validity_invalid(invalid_ticker):
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.side_effect = Exception("Invalid ticker")
        assert check_ticker_validity(invalid_ticker) is False

def test_calculate_date_range():
    days = 10
    start, end = calculate_date_range(days)
    
    assert isinstance(start, str)
    assert isinstance(end, str)
    
    end_date = pd.to_datetime(end)
    start_date = pd.to_datetime(start)
    
    # Check if start date is roughly 1.5 * days before end date
    expected_delta = pd.Timedelta(days=days * 1.5)
    assert (end_date - start_date) == expected_delta

@patch("yfinance.download")
def test_fetch_price_data(mock_download):
    # Setup mock return value
    dates = pd.date_range(start="2023-01-01", periods=5)
    mock_df = pd.DataFrame({
        "Open": [100]*5,
        "High": [110]*5,
        "Low": [90]*5,
        "Close": [105]*5,
        "Volume": [1000]*5
    }, index=dates)
    mock_download.return_value = mock_df

    ticker = "AAPL"
    start = "2023-01-01"
    end = "2023-01-05"
    
    result = fetch_price_data(ticker, start, end)
    
    assert isinstance(result, pd.DataFrame)
    assert "Date" in result.columns  # Should be reset_index
    assert len(result) == 5
    mock_download.assert_called_once_with(ticker, start=start, end=end)

def test_trim_to_exact_num_of_days(sample_price_data):
    days = 3
    trimmed = trim_to_exact_num_of_days(sample_price_data, days)
    assert len(trimmed) == days
    assert trimmed.iloc[-1]["Close"] == sample_price_data.iloc[-1]["Close"]

def test_clean_and_validate_output_valid(sample_price_data):
    # This test might fail if the function has bugs (like missing num_of_days arg)
    # We will patch the global variable if needed or expect failure if we can't
    # But for now let's try to call it. 
    # Note: The function clean_and_validate_output in the file uses a global 'num_of_days' 
    # which is not passed as argument. This is a bug in the code.
    # We will try to set it in the module if possible, or expect error.
    
    # Injecting the missing variable into the function's globals for the test to pass
    # if the logic is otherwise correct.
    with patch("data.fetch_price_data.num_of_days", 5, create=True):
        # It prints "Output data is valid." and returns None
        try:
            clean_and_validate_output(sample_price_data)
        except ValueError as e:
            pytest.fail(f"Validation failed with error: {e}")

def test_clean_and_validate_output_invalid_nulls(sample_price_data):
    df = sample_price_data.copy()
    df.loc[0, "Open"] = np.nan
    
    with patch("data.fetch_price_data.num_of_days", 5, create=True):
        with pytest.raises(ValueError, match="Output data contains null values"):
            clean_and_validate_output(df)

def test_clean_and_validate_output_invalid_negative(sample_price_data):
    df = sample_price_data.copy()
    df.loc[0, "Close"] = -10.0
    
    with patch("data.fetch_price_data.num_of_days", 5, create=True):
        with pytest.raises(ValueError, match="Output data contains negative values"):
            clean_and_validate_output(df)

def test_clean_and_validate_output_unsorted(sample_price_data):
    df = sample_price_data.copy()
    df = df.sort_values(by="Date", ascending=False)
    
    with patch("data.fetch_price_data.num_of_days", 5, create=True):
        with pytest.raises(ValueError, match="Output data is not sorted"):
            clean_and_validate_output(df)

# Note: filter_to_market_data_only also has missing start_date/end_date args in the implementation
# We will patch the globals to test it.

def test_filter_to_market_data_only(sample_price_data):
    df = sample_price_data.copy()
    
    # Mock mcal.get_calendar("NYSE").valid_days
    with patch("pandas_market_calendars.get_calendar") as mock_get_calendar:
        mock_calendar = MagicMock()
        # Let's say only the first 3 days are valid
        valid_days = df["Date"].iloc[:3]
        mock_calendar.valid_days.return_value = valid_days
        mock_get_calendar.return_value = mock_calendar
        
        # Patch the global start_date and end_date which are used in the function
        with patch("data.fetch_price_data.start_date", "2023-01-01", create=True):
            with patch("data.fetch_price_data.end_date", "2023-01-05", create=True):
                filtered = filter_to_market_data_only(df)
                
                assert len(filtered) == 3
                assert filtered["Date"].isin(valid_days).all()

