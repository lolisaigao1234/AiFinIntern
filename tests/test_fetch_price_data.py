"""
Unit Tests for Price Data Fetcher Module - Task 2.1

Comprehensive test suite covering all functions in fetch_price_data.py
with edge cases and thorough validation per the walkthrough specification.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, PropertyMock
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.fetch_price_data import (
    check_ticker_validity,
    validate_inputs,
    calculate_date_range,
    fetch_raw_price_data,
    filter_to_market_data_only,
    trim_to_exact_num_of_days,
    clean_and_validate_output,
    fetch_price_data,
    VALID_TICKERS,
    MIN_DAYS,
    MAX_DAYS,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def valid_ticker():
    """A valid ticker from the Magnificent Seven."""
    return "AAPL"


@pytest.fixture
def invalid_ticker():
    """An invalid ticker symbol."""
    return "INVALID_TICKER_XYZ"


@pytest.fixture
def sample_price_data():
    """Sample price DataFrame with valid business day data."""
    dates = pd.date_range(start="2023-01-02", periods=5, freq="B")
    data = {
        "Date": dates,
        "Open": [150.0, 151.0, 152.0, 153.0, 154.0],
        "High": [155.0, 156.0, 157.0, 158.0, 159.0],
        "Low": [149.0, 150.0, 151.0, 152.0, 153.0],
        "Close": [152.0, 153.0, 154.0, 155.0, 156.0],
        "Adj Close": [152.0, 153.0, 154.0, 155.0, 156.0],
        "Volume": [1000000, 1100000, 1200000, 1300000, 1400000]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_price_data_10_days():
    """Sample price DataFrame with 10 business days."""
    dates = pd.date_range(start="2023-01-02", periods=10, freq="B")
    data = {
        "Date": dates,
        "Open": [150.0 + i for i in range(10)],
        "High": [155.0 + i for i in range(10)],
        "Low": [149.0 + i for i in range(10)],
        "Close": [152.0 + i for i in range(10)],
        "Adj Close": [152.0 + i for i in range(10)],
        "Volume": [1000000 + i * 100000 for i in range(10)]
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_yf_download_response():
    """Mock response from yfinance download with named Date index."""
    dates = pd.date_range(start="2023-01-02", periods=5, freq="B", name="Date")
    return pd.DataFrame({
        "Open": [150.0, 151.0, 152.0, 153.0, 154.0],
        "High": [155.0, 156.0, 157.0, 158.0, 159.0],
        "Low": [149.0, 150.0, 151.0, 152.0, 153.0],
        "Close": [152.0, 153.0, 154.0, 155.0, 156.0],
        "Adj Close": [152.0, 153.0, 154.0, 155.0, 156.0],
        "Volume": [1000000, 1100000, 1200000, 1300000, 1400000]
    }, index=dates)


# =============================================================================
# Tests for VALID_TICKERS constant
# =============================================================================

class TestValidTickersConstant:
    """Tests for the VALID_TICKERS constant."""
    
    def test_valid_tickers_contains_magnificent_seven(self):
        """Verify all Magnificent Seven tickers are in VALID_TICKERS."""
        expected = {"AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"}
        assert set(VALID_TICKERS) == expected
    
    def test_valid_tickers_count(self):
        """Verify exactly 7 valid tickers."""
        assert len(VALID_TICKERS) == 7
    
    def test_valid_tickers_is_immutable(self):
        """Verify VALID_TICKERS is a tuple (immutable)."""
        assert isinstance(VALID_TICKERS, tuple)


# =============================================================================
# Tests for check_ticker_validity
# =============================================================================

class TestCheckTickerValidity:
    """Tests for the check_ticker_validity function."""
    
    def test_valid_ticker_returns_true(self, valid_ticker):
        """Test that a valid ticker returns True."""
        with patch("yfinance.Ticker") as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {"regularMarketPrice": 150.0, "symbol": "AAPL"}
            mock_ticker.return_value = mock_instance
            assert check_ticker_validity(valid_ticker) is True
    
    def test_invalid_ticker_returns_false(self, invalid_ticker):
        """Test that an invalid ticker returns False."""
        with patch("yfinance.Ticker") as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {"regularMarketPrice": None}
            mock_ticker.return_value = mock_instance
            assert check_ticker_validity(invalid_ticker) is False
    
    def test_ticker_raises_exception_returns_false(self):
        """Test that an exception during lookup returns False."""
        with patch("yfinance.Ticker") as mock_ticker:
            mock_ticker.side_effect = Exception("Network error")
            assert check_ticker_validity("ANY") is False
    
    def test_ticker_with_empty_info_returns_false(self):
        """Test that a ticker with empty info returns False."""
        with patch("yfinance.Ticker") as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {}
            mock_ticker.return_value = mock_instance
            assert check_ticker_validity("EMPTY") is False
    
    def test_ticker_with_none_info_returns_false(self):
        """Test that a ticker with None info returns False."""
        with patch("yfinance.Ticker") as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = None
            mock_ticker.return_value = mock_instance
            assert check_ticker_validity("NONE") is False


# =============================================================================
# Tests for validate_inputs
# =============================================================================

class TestValidateInputs:
    """Tests for the validate_inputs function."""
    
    def test_valid_inputs_no_exception(self, valid_ticker):
        """Test that valid inputs don't raise an exception."""
        validate_inputs(valid_ticker, 5)  # Should not raise
    
    def test_all_valid_tickers_accepted(self):
        """Test that all Magnificent Seven tickers are accepted."""
        for ticker in VALID_TICKERS:
            validate_inputs(ticker, 5)  # Should not raise
    
    def test_invalid_ticker_raises_valueerror(self, invalid_ticker):
        """Test that invalid ticker raises ValueError."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            validate_inputs(invalid_ticker, 5)
    
    def test_lowercase_ticker_raises_valueerror(self):
        """Test that lowercase ticker raises ValueError (case sensitive)."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            validate_inputs("aapl", 5)
    
    def test_days_below_minimum_raises_valueerror(self, valid_ticker):
        """Test that days=0 raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            validate_inputs(valid_ticker, 0)
    
    def test_days_negative_raises_valueerror(self, valid_ticker):
        """Test that negative days raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            validate_inputs(valid_ticker, -1)
    
    def test_days_above_maximum_raises_valueerror(self, valid_ticker):
        """Test that days > 10 raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            validate_inputs(valid_ticker, 11)
    
    def test_days_way_above_maximum_raises_valueerror(self, valid_ticker):
        """Test that days=100 raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            validate_inputs(valid_ticker, 100)
    
    def test_days_at_minimum_boundary_valid(self, valid_ticker):
        """Test that days=1 (minimum) is valid."""
        validate_inputs(valid_ticker, 1)  # Should not raise
    
    def test_days_at_maximum_boundary_valid(self, valid_ticker):
        """Test that days=10 (maximum) is valid."""
        validate_inputs(valid_ticker, 10)  # Should not raise
    
    def test_days_as_float_raises_valueerror(self, valid_ticker):
        """Test that float days raises ValueError."""
        with pytest.raises(ValueError, match="Days must be an integer"):
            validate_inputs(valid_ticker, 5.5)
    
    def test_days_as_string_raises_valueerror(self, valid_ticker):
        """Test that string days raises ValueError."""
        with pytest.raises(ValueError, match="Days must be an integer"):
            validate_inputs(valid_ticker, "5")


# =============================================================================
# Tests for calculate_date_range
# =============================================================================

class TestCalculateDateRange:
    """Tests for the calculate_date_range function."""
    
    def test_returns_tuple_of_strings(self):
        """Test that function returns tuple of two strings."""
        start, end = calculate_date_range(10)
        assert isinstance(start, str)
        assert isinstance(end, str)
    
    def test_date_format_is_correct(self):
        """Test that dates are in YYYY-MM-DD format."""
        start, end = calculate_date_range(10)
        # Verify format by parsing
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    
    def test_start_date_before_end_date(self):
        """Test that start date is before end date."""
        start, end = calculate_date_range(10)
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        assert start_dt < end_dt
    
    def test_date_range_uses_1_5_multiplier(self):
        """Test that date range uses 1.5x multiplier for days."""
        days = 10
        start, end = calculate_date_range(days)
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        expected_delta = pd.Timedelta(days=int(days * 1.5))
        assert (end_dt - start_dt) == expected_delta
    
    def test_end_date_is_today(self):
        """Test that end date is today."""
        _, end = calculate_date_range(10)
        today = pd.Timestamp.today().strftime("%Y-%m-%d")
        assert end == today
    
    def test_different_days_produce_different_ranges(self):
        """Test that different days values produce different start dates."""
        start_5, _ = calculate_date_range(5)
        start_10, _ = calculate_date_range(10)
        assert start_5 != start_10
    
    def test_minimum_days_range(self):
        """Test date range calculation with days=1."""
        start, end = calculate_date_range(1)
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        expected_delta = pd.Timedelta(days=1)  # 1 * 1.5 = 1.5, int() = 1
        assert (end_dt - start_dt) == expected_delta


# =============================================================================
# Tests for fetch_raw_price_data
# =============================================================================

class TestFetchRawPriceData:
    """Tests for the fetch_raw_price_data function."""
    
    @patch("yfinance.download")
    def test_returns_dataframe(self, mock_download, mock_yf_download_response):
        """Test that function returns a DataFrame."""
        mock_download.return_value = mock_yf_download_response
        result = fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
        assert isinstance(result, pd.DataFrame)
    
    @patch("yfinance.download")
    def test_date_column_exists(self, mock_download, mock_yf_download_response):
        """Test that Date column exists after reset_index."""
        mock_download.return_value = mock_yf_download_response
        result = fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
        assert "Date" in result.columns
    
    @patch("yfinance.download")
    def test_ohlcv_columns_exist(self, mock_download, mock_yf_download_response):
        """Test that all OHLCV columns exist."""
        mock_download.return_value = mock_yf_download_response
        result = fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
        expected_cols = ["Open", "High", "Low", "Close", "Volume"]
        for col in expected_cols:
            assert col in result.columns
    
    @patch("yfinance.download")
    def test_empty_response_raises_valueerror(self, mock_download):
        """Test that empty response raises ValueError."""
        mock_download.return_value = pd.DataFrame()
        with pytest.raises(ValueError, match="No data returned"):
            fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
    
    @patch("yfinance.download")
    def test_correct_row_count(self, mock_download, mock_yf_download_response):
        """Test that row count matches mock data."""
        mock_download.return_value = mock_yf_download_response
        result = fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
        assert len(result) == 5
    
    @patch("yfinance.download")
    def test_download_called_with_correct_args(self, mock_download, mock_yf_download_response):
        """Test that yfinance.download is called with correct arguments."""
        mock_download.return_value = mock_yf_download_response
        fetch_raw_price_data("AAPL", "2023-01-01", "2023-01-10")
        mock_download.assert_called_once_with(
            "AAPL", start="2023-01-01", end="2023-01-10", progress=False
        )


# =============================================================================
# Tests for filter_to_market_data_only
# =============================================================================

class TestFilterToMarketDataOnly:
    """Tests for the filter_to_market_data_only function."""
    
    def test_filters_to_valid_trading_days(self, sample_price_data):
        """Test that function filters to valid NYSE trading days."""
        with patch("pandas_market_calendars.get_calendar") as mock_get_cal:
            mock_calendar = MagicMock()
            # Return only the first 3 dates as valid
            valid_days = sample_price_data["Date"].iloc[:3]
            mock_calendar.valid_days.return_value = pd.DatetimeIndex(valid_days)
            mock_get_cal.return_value = mock_calendar
            
            result = filter_to_market_data_only(
                sample_price_data, "2023-01-01", "2023-01-10"
            )
            assert len(result) == 3
    
    def test_preserves_all_columns(self, sample_price_data):
        """Test that all columns are preserved after filtering."""
        with patch("pandas_market_calendars.get_calendar") as mock_get_cal:
            mock_calendar = MagicMock()
            mock_calendar.valid_days.return_value = pd.DatetimeIndex(
                sample_price_data["Date"]
            )
            mock_get_cal.return_value = mock_calendar
            
            result = filter_to_market_data_only(
                sample_price_data, "2023-01-01", "2023-01-10"
            )
            assert set(result.columns) == set(sample_price_data.columns)
    
    def test_resets_index_after_filtering(self, sample_price_data):
        """Test that index is reset after filtering."""
        with patch("pandas_market_calendars.get_calendar") as mock_get_cal:
            mock_calendar = MagicMock()
            # Return only middle dates
            valid_days = sample_price_data["Date"].iloc[1:4]
            mock_calendar.valid_days.return_value = pd.DatetimeIndex(valid_days)
            mock_get_cal.return_value = mock_calendar
            
            result = filter_to_market_data_only(
                sample_price_data, "2023-01-01", "2023-01-10"
            )
            assert list(result.index) == [0, 1, 2]
    
    def test_empty_valid_days_returns_empty_df(self, sample_price_data):
        """Test that no valid days returns empty DataFrame."""
        with patch("pandas_market_calendars.get_calendar") as mock_get_cal:
            mock_calendar = MagicMock()
            mock_calendar.valid_days.return_value = pd.DatetimeIndex([])
            mock_get_cal.return_value = mock_calendar
            
            result = filter_to_market_data_only(
                sample_price_data, "2023-01-01", "2023-01-10"
            )
            assert len(result) == 0


# =============================================================================
# Tests for trim_to_exact_num_of_days
# =============================================================================

class TestTrimToExactNumOfDays:
    """Tests for the trim_to_exact_num_of_days function."""
    
    def test_trims_to_exact_count(self, sample_price_data):
        """Test that DataFrame is trimmed to exact count."""
        result = trim_to_exact_num_of_days(sample_price_data, 3)
        assert len(result) == 3
    
    def test_keeps_most_recent_data(self, sample_price_data):
        """Test that most recent (tail) data is kept."""
        result = trim_to_exact_num_of_days(sample_price_data, 3)
        # Last row should match
        assert result.iloc[-1]["Close"] == sample_price_data.iloc[-1]["Close"]
    
    def test_resets_index(self, sample_price_data):
        """Test that index is reset after trimming."""
        result = trim_to_exact_num_of_days(sample_price_data, 3)
        assert list(result.index) == [0, 1, 2]
    
    def test_trim_to_one_day(self, sample_price_data):
        """Test trimming to single day."""
        result = trim_to_exact_num_of_days(sample_price_data, 1)
        assert len(result) == 1
        assert result.iloc[0]["Close"] == sample_price_data.iloc[-1]["Close"]
    
    def test_trim_to_same_length(self, sample_price_data):
        """Test trimming to same length returns same data."""
        result = trim_to_exact_num_of_days(sample_price_data, len(sample_price_data))
        assert len(result) == len(sample_price_data)
    
    def test_trim_to_more_than_available(self, sample_price_data):
        """Test trimming to more than available returns all data."""
        result = trim_to_exact_num_of_days(sample_price_data, 100)
        assert len(result) == len(sample_price_data)


# =============================================================================
# Tests for clean_and_validate_output
# =============================================================================

class TestCleanAndValidateOutput:
    """Tests for the clean_and_validate_output function."""
    
    def test_valid_data_passes(self, sample_price_data):
        """Test that valid data passes validation."""
        clean_and_validate_output(sample_price_data, 5)  # Should not raise
    
    def test_null_open_raises_valueerror(self, sample_price_data):
        """Test that null in Open column raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Open"] = np.nan
        with pytest.raises(ValueError, match="null values in Open"):
            clean_and_validate_output(df, 5)
    
    def test_null_close_raises_valueerror(self, sample_price_data):
        """Test that null in Close column raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Close"] = np.nan
        with pytest.raises(ValueError, match="null values in Close"):
            clean_and_validate_output(df, 5)
    
    def test_null_volume_raises_valueerror(self, sample_price_data):
        """Test that null in Volume column raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Volume"] = np.nan
        with pytest.raises(ValueError, match="null values in Volume"):
            clean_and_validate_output(df, 5)
    
    def test_null_date_raises_valueerror(self, sample_price_data):
        """Test that null in Date column raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Date"] = pd.NaT
        with pytest.raises(ValueError, match="null values in Date"):
            clean_and_validate_output(df, 5)
    
    def test_negative_open_raises_valueerror(self, sample_price_data):
        """Test that negative Open value raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Open"] = -10.0
        with pytest.raises(ValueError, match="negative values in Open"):
            clean_and_validate_output(df, 5)
    
    def test_negative_close_raises_valueerror(self, sample_price_data):
        """Test that negative Close value raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Close"] = -10.0
        with pytest.raises(ValueError, match="negative values in Close"):
            clean_and_validate_output(df, 5)
    
    def test_negative_volume_raises_valueerror(self, sample_price_data):
        """Test that negative Volume value raises ValueError."""
        df = sample_price_data.copy()
        df.loc[0, "Volume"] = -1000
        with pytest.raises(ValueError, match="negative values in Volume"):
            clean_and_validate_output(df, 5)
    
    def test_unsorted_dates_raises_valueerror(self, sample_price_data):
        """Test that unsorted dates raise ValueError."""
        df = sample_price_data.copy()
        df = df.sort_values("Date", ascending=False).reset_index(drop=True)
        with pytest.raises(ValueError, match="not sorted by date"):
            clean_and_validate_output(df, 5)
    
    def test_wrong_row_count_raises_valueerror(self, sample_price_data):
        """Test that wrong row count raises ValueError."""
        with pytest.raises(ValueError, match="has 5 rows, expected 10"):
            clean_and_validate_output(sample_price_data, 10)
    
    def test_weekend_dates_raises_valueerror(self):
        """Test that weekend dates raise ValueError."""
        # Create data with a Saturday
        dates = pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04", 
                                "2023-01-05", "2023-01-07"])  # Jan 7 is Saturday
        df = pd.DataFrame({
            "Date": dates,
            "Open": [150.0] * 5,
            "High": [155.0] * 5,
            "Low": [149.0] * 5,
            "Close": [152.0] * 5,
            "Volume": [1000000] * 5
        })
        with pytest.raises(ValueError, match="weekend dates"):
            clean_and_validate_output(df, 5)
    
    def test_missing_date_column_raises_valueerror(self, sample_price_data):
        """Test that missing Date column raises ValueError."""
        df = sample_price_data.drop(columns=["Date"])
        with pytest.raises(ValueError, match="Missing required column: Date"):
            clean_and_validate_output(df, 5)
    
    def test_missing_open_column_raises_valueerror(self, sample_price_data):
        """Test that missing Open column raises ValueError."""
        df = sample_price_data.drop(columns=["Open"])
        with pytest.raises(ValueError, match="Missing required column: Open"):
            clean_and_validate_output(df, 5)
    
    def test_missing_close_column_raises_valueerror(self, sample_price_data):
        """Test that missing Close column raises ValueError."""
        df = sample_price_data.drop(columns=["Close"])
        with pytest.raises(ValueError, match="Missing required column: Close"):
            clean_and_validate_output(df, 5)
    
    def test_missing_volume_column_raises_valueerror(self, sample_price_data):
        """Test that missing Volume column raises ValueError."""
        df = sample_price_data.drop(columns=["Volume"])
        with pytest.raises(ValueError, match="Missing required column: Volume"):
            clean_and_validate_output(df, 5)
    
    def test_zero_values_are_valid(self, sample_price_data):
        """Test that zero values are valid (not negative)."""
        df = sample_price_data.copy()
        df.loc[0, "Volume"] = 0  # Zero volume is valid
        clean_and_validate_output(df, 5)  # Should not raise
    
    def test_all_null_raises_valueerror(self):
        """Test that all null values raise ValueError."""
        df = pd.DataFrame({
            "Date": [pd.NaT] * 5,
            "Open": [np.nan] * 5,
            "Close": [np.nan] * 5,
            "Volume": [np.nan] * 5
        })
        with pytest.raises(ValueError):
            clean_and_validate_output(df, 5)


# =============================================================================
# Tests for fetch_price_data (Main Integration Function)
# =============================================================================

class TestFetchPriceData:
    """Integration tests for the main fetch_price_data function."""
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_returns_dataframe(self, mock_filter, mock_fetch, sample_price_data):
        """Test that function returns a DataFrame."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("AAPL", 5)
        assert isinstance(result, pd.DataFrame)
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_correct_row_count(self, mock_filter, mock_fetch, sample_price_data):
        """Test that function returns correct number of rows."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("AAPL", 5)
        assert len(result) == 5
    
    def test_invalid_ticker_raises_valueerror(self, invalid_ticker):
        """Test ID 2.1.2: Invalid ticker raises ValueError."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data(invalid_ticker, 5)
    
    def test_days_above_max_raises_valueerror(self, valid_ticker):
        """Test ID 2.1.3: Days out of range (high) raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            fetch_price_data(valid_ticker, 15)
    
    def test_days_below_min_raises_valueerror(self, valid_ticker):
        """Test ID 2.1.4: Days out of range (low) raises ValueError."""
        with pytest.raises(ValueError, match="Days must be between"):
            fetch_price_data(valid_ticker, 0)
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_no_nan_in_close_column(self, mock_filter, mock_fetch, sample_price_data):
        """Test ID 2.1.5: No NaN values in Close column."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("MSFT", 5)
        assert result["Close"].notna().all()
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_all_prices_positive(self, mock_filter, mock_fetch, sample_price_data):
        """Test ID 2.1.6: All OHLC prices are positive."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("GOOGL", 5)
        assert (result["Open"] > 0).all()
        assert (result["High"] > 0).all()
        assert (result["Low"] > 0).all()
        assert (result["Close"] > 0).all()
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_dates_are_weekdays(self, mock_filter, mock_fetch, sample_price_data):
        """Test ID 2.1.7: All dates are weekdays (Mon-Fri)."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("NVDA", 5)
        weekdays = result["Date"].dt.dayofweek
        assert (weekdays <= 4).all()
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_data_sorted_ascending(self, mock_filter, mock_fetch, sample_price_data):
        """Test ID 2.1.8: Data is sorted by date in ascending order."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        result = fetch_price_data("TSLA", 5)
        assert result["Date"].is_monotonic_increasing
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_all_magnificent_seven_tickers(self, mock_filter, mock_fetch, sample_price_data):
        """Test that all Magnificent Seven tickers work."""
        mock_fetch.return_value = sample_price_data
        mock_filter.return_value = sample_price_data
        
        for ticker in VALID_TICKERS:
            result = fetch_price_data(ticker, 5)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 5
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_default_days_is_10(self, mock_filter, mock_fetch, sample_price_data_10_days):
        """Test that default days parameter is 10."""
        mock_fetch.return_value = sample_price_data_10_days
        mock_filter.return_value = sample_price_data_10_days
        
        result = fetch_price_data("AAPL")  # No days argument
        assert len(result) == 10
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_minimum_days_boundary(self, mock_filter, mock_fetch):
        """Test with days=1 (minimum boundary)."""
        single_day = pd.DataFrame({
            "Date": pd.date_range("2023-01-02", periods=1, freq="B"),
            "Open": [150.0],
            "High": [155.0],
            "Low": [149.0],
            "Close": [152.0],
            "Volume": [1000000]
        })
        mock_fetch.return_value = single_day
        mock_filter.return_value = single_day
        
        result = fetch_price_data("AAPL", 1)
        assert len(result) == 1
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_maximum_days_boundary(self, mock_filter, mock_fetch, sample_price_data_10_days):
        """Test with days=10 (maximum boundary)."""
        mock_fetch.return_value = sample_price_data_10_days
        mock_filter.return_value = sample_price_data_10_days
        
        result = fetch_price_data("AAPL", 10)
        assert len(result) == 10


# =============================================================================
# Edge Case Tests
# =============================================================================

class TestEdgeCases:
    """Edge case tests for robustness."""
    
    def test_ticker_with_whitespace_invalid(self):
        """Test that ticker with whitespace is invalid."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data(" AAPL ", 5)
    
    def test_empty_ticker_invalid(self):
        """Test that empty ticker is invalid."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data("", 5)
    
    def test_none_ticker_raises_error(self):
        """Test that None ticker raises error."""
        with pytest.raises((ValueError, TypeError)):
            fetch_price_data(None, 5)
    
    def test_days_as_boolean_raises_error(self, valid_ticker):
        """Test that boolean days raises error."""
        with pytest.raises(ValueError):
            fetch_price_data(valid_ticker, True)  # True == 1 but is bool
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_volume_with_large_numbers(self, mock_filter, mock_fetch):
        """Test handling of large volume numbers."""
        df = pd.DataFrame({
            "Date": pd.date_range("2023-01-02", periods=5, freq="B"),
            "Open": [150.0] * 5,
            "High": [155.0] * 5,
            "Low": [149.0] * 5,
            "Close": [152.0] * 5,
            "Volume": [10**12] * 5  # 1 trillion volume
        })
        mock_fetch.return_value = df
        mock_filter.return_value = df
        
        result = fetch_price_data("AAPL", 5)
        assert (result["Volume"] == 10**12).all()
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_very_small_prices(self, mock_filter, mock_fetch):
        """Test handling of very small (penny stock) prices."""
        df = pd.DataFrame({
            "Date": pd.date_range("2023-01-02", periods=5, freq="B"),
            "Open": [0.001] * 5,
            "High": [0.002] * 5,
            "Low": [0.0005] * 5,
            "Close": [0.0015] * 5,
            "Volume": [1000000] * 5
        })
        mock_fetch.return_value = df
        mock_filter.return_value = df
        
        result = fetch_price_data("AAPL", 5)
        assert (result["Close"] > 0).all()
    
    @patch("data.fetch_price_data.fetch_raw_price_data")
    @patch("data.fetch_price_data.filter_to_market_data_only")
    def test_very_large_prices(self, mock_filter, mock_fetch):
        """Test handling of very large prices."""
        df = pd.DataFrame({
            "Date": pd.date_range("2023-01-02", periods=5, freq="B"),
            "Open": [500000.0] * 5,  # Like BRK.A
            "High": [510000.0] * 5,
            "Low": [495000.0] * 5,
            "Close": [505000.0] * 5,
            "Volume": [100] * 5
        })
        mock_fetch.return_value = df
        mock_filter.return_value = df
        
        result = fetch_price_data("AAPL", 5)
        assert (result["Close"] > 0).all()
    
    def test_special_characters_in_ticker_invalid(self):
        """Test that special characters in ticker are invalid."""
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data("AAPL!", 5)
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data("AA$PL", 5)
        with pytest.raises(ValueError, match="Invalid ticker"):
            fetch_price_data("AAPL\n", 5)


# =============================================================================
# Constant Boundary Tests
# =============================================================================

class TestConstantBoundaries:
    """Tests for MIN_DAYS and MAX_DAYS constants."""
    
    def test_min_days_is_one(self):
        """Verify MIN_DAYS constant is 1."""
        assert MIN_DAYS == 1
    
    def test_max_days_is_ten(self):
        """Verify MAX_DAYS constant is 10."""
        assert MAX_DAYS == 10
    
    def test_boundary_constants_are_integers(self):
        """Verify boundary constants are integers."""
        assert isinstance(MIN_DAYS, int)
        assert isinstance(MAX_DAYS, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])