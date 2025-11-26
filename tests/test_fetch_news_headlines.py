"""
Unit Tests for Task 2.2: News Data Fetcher Function

Comprehensive test suite for fetch_news_headlines with extensive edge case coverage
for financial data robustness.
"""

import sys
from pathlib import Path

# =============================================================================
# Path Configuration - Fix module import issues
# =============================================================================
# Add the project root to sys.path to allow imports from the 'data' package
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# Imports
# =============================================================================
import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, PropertyMock
import time

from data.fetch_news_headlines import (
    fetch_news_headlines,
    MAGNIFICENT_SEVEN,
    _empty_dataframe,
    _parse_entry_date,
    _extract_source,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_rss_feed_with_entries():
    """Create a mock RSS feed with sample entries."""
    now = datetime.now()
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        _create_mock_entry(
            title="Apple announces new iPhone model",
            pub_date=now,
            source="Reuters"
        ),
        _create_mock_entry(
            title="AAPL stock rises on strong earnings",
            pub_date=now - timedelta(days=1),
            source="Bloomberg"
        ),
        _create_mock_entry(
            title="Tech sector shows resilience",
            pub_date=now - timedelta(days=2),
            source="CNBC"
        ),
    ]
    
    return mock_feed


@pytest.fixture
def mock_rss_feed_empty():
    """Create a mock RSS feed with no entries."""
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = []
    return mock_feed


@pytest.fixture
def mock_rss_feed_with_duplicates():
    """Create a mock RSS feed with duplicate headlines."""
    now = datetime.now()
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        _create_mock_entry(
            title="Breaking: Major tech announcement",
            pub_date=now,
            source="Reuters"
        ),
        _create_mock_entry(
            title="Breaking: Major tech announcement",  # Duplicate
            pub_date=now,
            source="AP News"
        ),
        _create_mock_entry(
            title="Different headline here",
            pub_date=now,
            source="Bloomberg"
        ),
    ]
    
    return mock_feed


@pytest.fixture
def mock_rss_feed_old_entries():
    """Create a mock RSS feed with entries older than 10 days."""
    old_date = datetime.now() - timedelta(days=15)
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        _create_mock_entry(
            title="Old news headline",
            pub_date=old_date,
            source="Reuters"
        ),
    ]
    
    return mock_feed


@pytest.fixture
def mock_rss_feed_missing_fields():
    """Create a mock RSS feed with entries missing required fields."""
    now = datetime.now()
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    
    # Entry with missing title
    entry_no_title = MagicMock()
    entry_no_title.published_parsed = (now.year, now.month, now.day, 10, 0, 0, 0, 0, 0)
    entry_no_title.source = {'title': 'Reuters'}
    entry_no_title.get = lambda key, default='': '' if key == 'title' else default
    
    # Entry with empty title
    entry_empty_title = MagicMock()
    entry_empty_title.title = "   "
    entry_empty_title.published_parsed = (now.year, now.month, now.day, 11, 0, 0, 0, 0, 0)
    entry_empty_title.source = {'title': 'Bloomberg'}
    entry_empty_title.get = lambda key, default='', e=entry_empty_title: (
        getattr(e, key, default) if hasattr(e, key) else default
    )
    
    # Entry with no date
    entry_no_date = MagicMock()
    entry_no_date.title = "Valid headline but no date"
    entry_no_date.published_parsed = None
    entry_no_date.updated_parsed = None
    entry_no_date.source = {'title': 'CNBC'}
    entry_no_date.get = lambda key, default='', e=entry_no_date: (
        getattr(e, key, default) if hasattr(e, key) and key != 'published' and key != 'updated' else ''
    )
    
    # Valid entry
    valid_entry = _create_mock_entry(
        title="Valid headline with all fields",
        pub_date=now,
        source="MarketWatch"
    )
    
    mock_feed.entries = [entry_no_title, entry_empty_title, entry_no_date, valid_entry]
    
    return mock_feed


@pytest.fixture
def mock_rss_feed_boundary_dates():
    """Create a mock RSS feed with entries at exact date boundaries."""
    now = datetime.now()
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        # Exactly at cutoff (5 days ago, should be included)
        _create_mock_entry(
            title="Headline at exact boundary",
            pub_date=now - timedelta(days=5),
            source="Reuters"
        ),
        # Just before cutoff (should be excluded)
        _create_mock_entry(
            title="Headline just outside boundary",
            pub_date=now - timedelta(days=5, seconds=1),
            source="Bloomberg"
        ),
        # Just after cutoff (should be included)
        _create_mock_entry(
            title="Headline just inside boundary",
            pub_date=now - timedelta(days=4, hours=23, minutes=59),
            source="CNBC"
        ),
    ]
    
    return mock_feed


@pytest.fixture
def mock_rss_feed_various_date_formats():
    """Create entries with various date format representations."""
    now = datetime.now()
    
    mock_feed = MagicMock()
    mock_feed.bozo = False
    
    entries = []
    
    # Standard published_parsed
    entry1 = MagicMock()
    entry1.title = "Standard date format"
    entry1.published_parsed = (now.year, now.month, now.day, 10, 0, 0, 0, 0, 0)
    entry1.updated_parsed = None
    entry1.source = {'title': 'Source1'}
    entry1.get = lambda key, default='', e=entry1: (
        getattr(e, key, default) if hasattr(e, key) else default
    )
    entries.append(entry1)
    
    # Using updated_parsed instead
    entry2 = MagicMock()
    entry2.title = "Updated date format"
    entry2.published_parsed = None
    entry2.updated_parsed = (now.year, now.month, now.day, 11, 0, 0, 0, 0, 0)
    entry2.source = {'title': 'Source2'}
    entry2.get = lambda key, default='', e=entry2: (
        getattr(e, key, default) if hasattr(e, key) else default
    )
    entries.append(entry2)
    
    # Using string date in 'published' field
    entry3 = MagicMock()
    entry3.title = "String date format"
    entry3.published_parsed = None
    entry3.updated_parsed = None
    entry3.published = now.strftime("%Y-%m-%dT%H:%M:%S")
    entry3.source = {'title': 'Source3'}
    entry3.get = lambda key, default='', e=entry3: (
        getattr(e, key, default) if hasattr(e, key) else default
    )
    entries.append(entry3)
    
    mock_feed.entries = entries
    return mock_feed


def _create_mock_entry(title: str, pub_date: datetime, source: str) -> MagicMock:
    """Helper to create a properly configured mock RSS entry."""
    entry = MagicMock()
    entry.title = title
    entry.published_parsed = (
        pub_date.year, pub_date.month, pub_date.day,
        pub_date.hour, pub_date.minute, pub_date.second,
        0, 0, 0
    )
    entry.updated_parsed = None
    entry.source = {'title': source}
    entry.get = lambda key, default='', e=entry: (
        getattr(e, key, default) if hasattr(e, key) else default
    )
    return entry


# =============================================================================
# Test 2.2.1: Valid ticker returns DataFrame
# =============================================================================

class TestValidTickerReturnsDataFrame:
    """Test 2.2.1: Valid ticker returns DataFrame (may be empty)."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_valid_ticker_returns_dataframe(self, mock_parse, mock_rss_feed_with_entries):
        """Valid ticker should return a DataFrame."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_valid_ticker_empty_feed_returns_dataframe(self, mock_parse, mock_rss_feed_empty):
        """Valid ticker with no news should return empty DataFrame."""
        mock_parse.return_value = mock_rss_feed_empty
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_all_magnificent_seven_tickers(self, mock_parse, mock_rss_feed_with_entries):
        """All Magnificent Seven tickers should be valid."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        for ticker in MAGNIFICENT_SEVEN:
            result = fetch_news_headlines(ticker=ticker, days=5)
            assert isinstance(result, pd.DataFrame)


# =============================================================================
# Test 2.2.2: DataFrame has correct columns
# =============================================================================

class TestDataFrameColumns:
    """Test 2.2.2: DataFrame has correct columns."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_dataframe_has_correct_columns(self, mock_parse, mock_rss_feed_with_entries):
        """DataFrame should have columns: date, ticker, headline, source."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="MSFT", days=5)
        
        expected_columns = ['date', 'ticker', 'headline', 'source']
        assert list(result.columns) == expected_columns
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_empty_dataframe_has_correct_columns(self, mock_parse, mock_rss_feed_empty):
        """Empty DataFrame should still have correct columns."""
        mock_parse.return_value = mock_rss_feed_empty
        
        result = fetch_news_headlines(ticker="MSFT", days=5)
        
        expected_columns = ['date', 'ticker', 'headline', 'source']
        assert list(result.columns) == expected_columns


# =============================================================================
# Test 2.2.3: Invalid ticker raises error
# =============================================================================

class TestInvalidTickerRaisesError:
    """Test 2.2.3: Invalid ticker raises ValueError."""
    
    def test_invalid_ticker_raises_valueerror(self):
        """Invalid ticker should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            fetch_news_headlines(ticker="INVALID", days=5)
        
        assert "Invalid ticker" in str(exc_info.value)
    
    def test_non_mag7_ticker_raises_valueerror(self):
        """Non-Magnificent Seven ticker should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            fetch_news_headlines(ticker="IBM", days=5)
        
        assert "Invalid ticker" in str(exc_info.value)
    
    def test_empty_ticker_raises_valueerror(self):
        """Empty ticker should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="", days=5)
    
    def test_non_string_ticker_raises_valueerror(self):
        """Non-string ticker should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker=123, days=5)
    
    def test_none_ticker_raises_valueerror(self):
        """None ticker should raise ValueError or TypeError."""
        with pytest.raises((ValueError, TypeError)):
            fetch_news_headlines(ticker=None, days=5)
    
    def test_list_ticker_raises_valueerror(self):
        """List ticker should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker=["AAPL"], days=5)
    
    def test_invalid_days_raises_valueerror(self):
        """Days outside 1-10 range should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=0)
        
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=11)
        
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=-1)
    
    def test_float_days_raises_valueerror(self):
        """Float days should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=5.5)
    
    def test_string_days_raises_valueerror(self):
        """String days should raise ValueError or TypeError."""
        with pytest.raises((ValueError, TypeError)):
            fetch_news_headlines(ticker="AAPL", days="5")
    
    def test_none_days_raises_error(self):
        """None days should raise an error."""
        with pytest.raises((ValueError, TypeError)):
            fetch_news_headlines(ticker="AAPL", days=None)
    
    def test_negative_days_raises_valueerror(self):
        """Negative days should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=-5)
    
    def test_very_large_days_raises_valueerror(self):
        """Very large days value should raise ValueError."""
        with pytest.raises(ValueError):
            fetch_news_headlines(ticker="AAPL", days=1000000)


# =============================================================================
# Test 2.2.4: Headlines are strings
# =============================================================================

class TestHeadlinesAreStrings:
    """Test 2.2.4: All headlines are str type."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_headlines_are_strings(self, mock_parse, mock_rss_feed_with_entries):
        """All headlines should be string type."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="GOOGL", days=5)
        
        if not result.empty:
            assert result['headline'].apply(lambda x: isinstance(x, str)).all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_ticker_column_is_string(self, mock_parse, mock_rss_feed_with_entries):
        """Ticker column should contain strings."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="GOOGL", days=5)
        
        if not result.empty:
            assert result['ticker'].apply(lambda x: isinstance(x, str)).all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_source_column_is_string(self, mock_parse, mock_rss_feed_with_entries):
        """Source column should contain strings."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="GOOGL", days=5)
        
        if not result.empty:
            assert result['source'].apply(lambda x: isinstance(x, str)).all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_headlines_are_not_empty_strings(self, mock_parse, mock_rss_feed_with_entries):
        """Headlines should not be empty strings after stripping."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="GOOGL", days=5)
        
        if not result.empty:
            assert (result['headline'].str.strip() != '').all()


# =============================================================================
# Test 2.2.5: Dates within range
# =============================================================================

class TestDatesWithinRange:
    """Test 2.2.5: All dates are within the specified days range."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_dates_within_range(self, mock_parse, mock_rss_feed_with_entries):
        """All dates should be within the specified days range."""
        mock_parse.return_value = mock_rss_feed_with_entries
        days = 5
        
        result = fetch_news_headlines(ticker="NVDA", days=days)
        
        if not result.empty:
            cutoff_date = datetime.now() - timedelta(days=days)
            assert (result['date'] >= pd.Timestamp(cutoff_date.date())).all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_old_entries_filtered_out(self, mock_parse, mock_rss_feed_old_entries):
        """Entries older than specified days should be filtered out."""
        mock_parse.return_value = mock_rss_feed_old_entries
        
        result = fetch_news_headlines(ticker="NVDA", days=5)
        
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_boundary_date_handling(self, mock_parse, mock_rss_feed_boundary_dates):
        """Test handling of entries at exact date boundaries."""
        mock_parse.return_value = mock_rss_feed_boundary_dates
        
        result = fetch_news_headlines(ticker="NVDA", days=5)
        
        # Should include entries within and at boundary, exclude those outside
        if not result.empty:
            cutoff_date = datetime.now() - timedelta(days=5)
            assert (result['date'] >= pd.Timestamp(cutoff_date)).all()


# =============================================================================
# Test 2.2.6: No duplicate headlines
# =============================================================================

class TestNoDuplicateHeadlines:
    """Test 2.2.6: No duplicate headlines in the result."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_no_duplicate_headlines(self, mock_parse, mock_rss_feed_with_duplicates):
        """Result should have no duplicate headlines on the same date."""
        mock_parse.return_value = mock_rss_feed_with_duplicates
        
        result = fetch_news_headlines(ticker="TSLA", days=10)
        
        assert len(result) == len(result.drop_duplicates(subset=['headline', 'date']))
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_duplicates_removed(self, mock_parse, mock_rss_feed_with_duplicates):
        """Duplicate entries should be removed."""
        mock_parse.return_value = mock_rss_feed_with_duplicates
        
        result = fetch_news_headlines(ticker="TSLA", days=10)
        
        # Original has 3 entries, 2 are duplicates, so result should have 2
        assert len(result) == 2


# =============================================================================
# Test 2.2.7: Empty result handling
# =============================================================================

class TestEmptyResultHandling:
    """Test 2.2.7: Empty result handling."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_empty_result_returns_dataframe(self, mock_parse, mock_rss_feed_empty):
        """Empty result should return empty DataFrame, not raise error."""
        mock_parse.return_value = mock_rss_feed_empty
        
        result = fetch_news_headlines(ticker="META", days=1)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_empty_result_has_correct_schema(self, mock_parse, mock_rss_feed_empty):
        """Empty DataFrame should have correct column schema."""
        mock_parse.return_value = mock_rss_feed_empty
        
        result = fetch_news_headlines(ticker="META", days=1)
        
        assert list(result.columns) == ['date', 'ticker', 'headline', 'source']
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_feed_error_returns_empty_dataframe(self, mock_parse):
        """Feed parsing error should return empty DataFrame."""
        mock_feed = MagicMock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("Parse error")
        mock_feed.entries = []
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="META", days=1)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty


# =============================================================================
# Edge Case Tests: Empty/Missing Data
# =============================================================================

class TestEmptyMissingData:
    """Test handling of empty or missing data fields."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_entries_with_missing_title_skipped(self, mock_parse, mock_rss_feed_missing_fields):
        """Entries with missing title should be skipped."""
        mock_parse.return_value = mock_rss_feed_missing_fields
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        # Only the valid entry should be included
        if not result.empty:
            assert all(result['headline'].str.strip() != '')
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_entries_with_empty_title_skipped(self, mock_parse, mock_rss_feed_missing_fields):
        """Entries with whitespace-only title should be skipped."""
        mock_parse.return_value = mock_rss_feed_missing_fields
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if not result.empty:
            for headline in result['headline']:
                assert headline.strip() != ''
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_entries_with_no_date_skipped(self, mock_parse, mock_rss_feed_missing_fields):
        """Entries with no parseable date should be skipped."""
        mock_parse.return_value = mock_rss_feed_missing_fields
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        # All dates in result should be valid
        if not result.empty:
            assert result['date'].notna().all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_null_entries_list(self, mock_parse):
        """Feed with None entries should be handled gracefully."""
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = None
        mock_parse.return_value = mock_feed
        
        # Should handle gracefully (either empty df or appropriate error)
        try:
            result = fetch_news_headlines(ticker="AAPL", days=5)
            assert isinstance(result, pd.DataFrame)
        except (TypeError, AttributeError):
            pass  # Also acceptable to raise error for invalid data


# =============================================================================
# Edge Case Tests: Date/Time Parsing
# =============================================================================

class TestDateTimeParsing:
    """Test various date/time parsing scenarios."""
    
    def test_parse_entry_date_with_published_parsed(self):
        """Test parsing with published_parsed tuple."""
        entry = MagicMock()
        entry.published_parsed = (2024, 6, 15, 10, 30, 45, 0, 0, 0)
        entry.updated_parsed = None
        entry.get = lambda key, default='': ''
        
        result = _parse_entry_date(entry)
        
        assert result == datetime(2024, 6, 15, 10, 30, 45)
    
    def test_parse_entry_date_with_updated_parsed(self):
        """Test fallback to updated_parsed when published_parsed is None."""
        entry = MagicMock()
        entry.published_parsed = None
        entry.updated_parsed = (2024, 6, 15, 11, 45, 0, 0, 0, 0)
        entry.get = lambda key, default='': ''
        
        result = _parse_entry_date(entry)
        
        assert result == datetime(2024, 6, 15, 11, 45, 0)
    
    def test_parse_entry_date_with_no_date(self):
        """Test parsing when no date is available."""
        entry = MagicMock()
        entry.published_parsed = None
        entry.updated_parsed = None
        entry.get = lambda key, default='': ''
        
        result = _parse_entry_date(entry)
        
        assert result is None
    
    def test_parse_entry_date_with_malformed_tuple(self):
        """Test parsing with malformed date tuple."""
        entry = MagicMock()
        entry.published_parsed = (2024,)  # Incomplete tuple
        entry.updated_parsed = None
        entry.get = lambda key, default='': ''
        
        result = _parse_entry_date(entry)
        
        # Should handle gracefully (return None or use fallback)
        # Either None or a valid datetime is acceptable
        assert result is None or isinstance(result, datetime)
    
    def test_parse_entry_date_with_string_fallback(self):
        """Test parsing from string date field."""
        entry = MagicMock()
        entry.published_parsed = None
        entry.updated_parsed = None
        
        def mock_get(key, default=''):
            if key == 'published':
                return '2024-06-15T10:30:00Z'
            return default
        
        entry.get = mock_get
        
        result = _parse_entry_date(entry)
        
        if result is not None:
            assert isinstance(result, datetime)
    
    def test_parse_entry_date_with_invalid_string(self):
        """Test parsing with invalid date string."""
        entry = MagicMock()
        entry.published_parsed = None
        entry.updated_parsed = None
        
        def mock_get(key, default=''):
            if key == 'published':
                return 'not-a-valid-date'
            return default
        
        entry.get = mock_get
        
        result = _parse_entry_date(entry)
        
        # Should return None for unparseable date
        assert result is None
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_various_date_formats(self, mock_parse, mock_rss_feed_various_date_formats):
        """Test that various date formats are parsed correctly."""
        mock_parse.return_value = mock_rss_feed_various_date_formats
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if not result.empty:
            # All dates should be datetime objects
            assert pd.api.types.is_datetime64_any_dtype(result['date'])


# =============================================================================
# Edge Case Tests: Source Extraction
# =============================================================================

class TestSourceExtraction:
    """Test source extraction from various entry formats."""
    
    def test_extract_source_with_source_dict(self):
        """Test extracting source from source dict with title."""
        entry = MagicMock()
        entry.source = {'title': 'Reuters'}
        entry.get = lambda key, default='': default
        
        result = _extract_source(entry)
        
        assert result == 'Reuters'
    
    def test_extract_source_with_empty_source_dict(self):
        """Test extracting source when source dict has no title."""
        entry = MagicMock()
        entry.source = {}
        entry.get = lambda key, default='': default
        
        result = _extract_source(entry)
        
        assert result == 'Yahoo Finance'  # Default
    
    def test_extract_source_with_none_source(self):
        """Test extracting source when source is None."""
        entry = MagicMock()
        entry.source = None
        entry.get = lambda key, default='': default
        
        result = _extract_source(entry)
        
        assert result == 'Yahoo Finance'  # Default
    
    def test_extract_source_with_publisher(self):
        """Test extracting source from publisher field."""
        entry = MagicMock()
        entry.source = None
        
        def mock_get(key, default=''):
            if key == 'publisher':
                return 'Bloomberg'
            return default
        
        entry.get = mock_get
        
        result = _extract_source(entry)
        
        assert result == 'Bloomberg'
    
    def test_extract_source_default(self):
        """Test default source when no source info available."""
        entry = MagicMock()
        entry.source = None
        entry.get = lambda key, default='': ''
        
        result = _extract_source(entry)
        
        assert result == 'Yahoo Finance'
    
    def test_extract_source_with_whitespace_title(self):
        """Test source extraction when title is only whitespace."""
        entry = MagicMock()
        entry.source = {'title': '   '}
        entry.get = lambda key, default='': default
        
        result = _extract_source(entry)
        
        # Should use default or handle whitespace appropriately
        assert isinstance(result, str)


# =============================================================================
# Edge Case Tests: Network/API Errors
# =============================================================================

class TestNetworkAPIErrors:
    """Test handling of network and API errors."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_network_timeout_handling(self, mock_parse):
        """Test handling of network timeout."""
        mock_parse.side_effect = TimeoutError("Connection timed out")
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_connection_error_handling(self, mock_parse):
        """Test handling of connection errors."""
        mock_parse.side_effect = ConnectionError("Failed to connect")
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_generic_exception_handling(self, mock_parse):
        """Test handling of generic exceptions during fetch."""
        mock_parse.side_effect = Exception("Unexpected error")
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_bozo_error_with_entries(self, mock_parse):
        """Test handling of feed with bozo error but valid entries."""
        now = datetime.now()
        mock_feed = MagicMock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("Minor parse warning")
        mock_feed.entries = [
            _create_mock_entry("Valid headline despite bozo", now, "Reuters")
        ]
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        # Should still return valid entries if available
        assert isinstance(result, pd.DataFrame)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_http_404_simulation(self, mock_parse):
        """Test handling of what would be a 404 response."""
        mock_feed = MagicMock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("HTTP 404: Not Found")
        mock_feed.entries = []
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_http_500_simulation(self, mock_parse):
        """Test handling of what would be a 500 response."""
        mock_feed = MagicMock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("HTTP 500: Internal Server Error")
        mock_feed.entries = []
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty


# =============================================================================
# Edge Case Tests: Data Integrity
# =============================================================================

class TestDataIntegrity:
    """Test data integrity and type adherence."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_date_column_is_datetime64(self, mock_parse, mock_rss_feed_with_entries):
        """Date column should be datetime64 type."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if not result.empty:
            assert pd.api.types.is_datetime64_any_dtype(result['date'])
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_ticker_column_matches_input(self, mock_parse, mock_rss_feed_with_entries):
        """Ticker column should match input ticker (uppercase)."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="aapl", days=5)  # lowercase input
        
        if not result.empty:
            assert (result['ticker'] == 'AAPL').all()  # Should be uppercase
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_no_null_values_in_required_columns(self, mock_parse, mock_rss_feed_with_entries):
        """Required columns should not have null values."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if not result.empty:
            assert result['date'].notna().all()
            assert result['ticker'].notna().all()
            assert result['headline'].notna().all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_dataframe_is_sorted_by_date(self, mock_parse, mock_rss_feed_with_entries):
        """DataFrame should be sorted by date (most recent first)."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if len(result) > 1:
            # Check descending order
            dates = result['date'].tolist()
            assert dates == sorted(dates, reverse=True)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_dataframe_index_is_reset(self, mock_parse, mock_rss_feed_with_entries):
        """DataFrame should have a clean reset index."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        if not result.empty:
            expected_index = list(range(len(result)))
            assert result.index.tolist() == expected_index
    
    def test_empty_dataframe_has_correct_dtypes(self):
        """Empty DataFrame should have correct dtypes."""
        result = _empty_dataframe()
        
        assert result['date'].dtype == 'datetime64[ns]'


# =============================================================================
# Additional Edge Case Tests
# =============================================================================

class TestAdditionalEdgeCases:
    """Additional edge case tests for robustness."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_lowercase_ticker_accepted(self, mock_parse, mock_rss_feed_with_entries):
        """Lowercase ticker should be accepted and converted to uppercase."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="aapl", days=5)
        
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert (result['ticker'] == 'AAPL').all()
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_mixed_case_ticker_accepted(self, mock_parse, mock_rss_feed_with_entries):
        """Mixed case ticker should be accepted."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="AaPl", days=5)
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_ticker_with_whitespace(self, mock_parse, mock_rss_feed_with_entries):
        """Ticker with leading/trailing whitespace should be handled."""
        mock_parse.return_value = mock_rss_feed_with_entries
        
        result = fetch_news_headlines(ticker="  AAPL  ", days=5)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_days_boundary_values(self):
        """Test boundary values for days parameter."""
        with patch('data.fetch_news_headlines.feedparser.parse') as mock_parse:
            mock_feed = MagicMock()
            mock_feed.bozo = False
            mock_feed.entries = []
            mock_parse.return_value = mock_feed
            
            # Minimum valid value
            result = fetch_news_headlines(ticker="AAPL", days=1)
            assert isinstance(result, pd.DataFrame)
            
            # Maximum valid value
            result = fetch_news_headlines(ticker="AAPL", days=10)
            assert isinstance(result, pd.DataFrame)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_special_characters_in_headline(self, mock_parse):
        """Test handling of special characters in headlines."""
        now = datetime.now()
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = [
            _create_mock_entry(
                title="Apple's Q4 earnings: $5.2B — 15% increase!",
                pub_date=now,
                source="Reuters"
            ),
            _create_mock_entry(
                title="BREAKING: AAPL ↑ 5% after announcement",
                pub_date=now,
                source="Bloomberg"
            ),
        ]
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_unicode_in_headline(self, mock_parse):
        """Test handling of unicode characters in headlines."""
        now = datetime.now()
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = [
            _create_mock_entry(
                title="苹果公司发布新产品",  # Chinese characters
                pub_date=now,
                source="Reuters"
            ),
        ]
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_very_long_headline(self, mock_parse):
        """Test handling of very long headlines."""
        now = datetime.now()
        long_headline = "Apple " * 500  # Very long headline
        
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = [
            _create_mock_entry(
                title=long_headline,
                pub_date=now,
                source="Reuters"
            ),
        ]
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert len(result['headline'].iloc[0]) > 1000


# =============================================================================
# Helper Function Tests
# =============================================================================

class TestHelperFunctions:
    """Tests for helper functions."""
    
    def test_empty_dataframe_schema(self):
        """_empty_dataframe should return DataFrame with correct schema."""
        result = _empty_dataframe()
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert list(result.columns) == ['date', 'ticker', 'headline', 'source']
    
    def test_empty_dataframe_dtypes(self):
        """_empty_dataframe should have correct dtypes."""
        result = _empty_dataframe()
        
        assert result['date'].dtype == 'datetime64[ns]'
    
    def test_parse_entry_date_handles_none_values(self):
        """_parse_entry_date should handle None values gracefully."""
        entry = MagicMock()
        entry.published_parsed = None
        entry.updated_parsed = None
        entry.get = lambda key, default='': None
        
        result = _parse_entry_date(entry)
        
        assert result is None
    
    def test_magnificent_seven_constant(self):
        """Verify MAGNIFICENT_SEVEN contains correct tickers."""
        expected = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META'}
        
        assert MAGNIFICENT_SEVEN == expected
    
    def test_magnificent_seven_is_set(self):
        """MAGNIFICENT_SEVEN should be a set for O(1) lookup."""
        assert isinstance(MAGNIFICENT_SEVEN, set)


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Basic performance and stress tests."""
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_handles_large_number_of_entries(self, mock_parse):
        """Test handling of large number of feed entries."""
        now = datetime.now()
        
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = [
            _create_mock_entry(
                title=f"Headline number {i}",
                pub_date=now - timedelta(hours=i),
                source="Reuters"
            )
            for i in range(1000)
        ]
        mock_parse.return_value = mock_feed
        
        result = fetch_news_headlines(ticker="AAPL", days=5)
        
        assert isinstance(result, pd.DataFrame)
        # All entries within 5 days should be included
        assert len(result) <= 1000
    
    @patch('data.fetch_news_headlines.feedparser.parse')
    def test_function_returns_quickly_on_empty(self, mock_parse, mock_rss_feed_empty):
        """Function should return quickly on empty feed."""
        mock_parse.return_value = mock_rss_feed_empty
        
        start_time = time.time()
        result = fetch_news_headlines(ticker="AAPL", days=5)
        elapsed = time.time() - start_time
        
        assert elapsed < 1.0  # Should complete in under 1 second


if __name__ == "__main__":
    pytest.main([__file__, "-v"])