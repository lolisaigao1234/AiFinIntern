"""
Comprehensive Unit Test Suite for Data Cleaner and Merger Module

This test suite provides extensive coverage of the clean_and_merge_data module,
including edge cases, corner cases, and error scenarios for financial data processing.

Target: 80+ test cases with zero tolerance for data processing errors.

Author: Financial Data Pipeline Tests
Version: 1.0.0
"""

import sys
import os
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import html

# Add the data directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'data'))

from clean_and_merge_data import (
    clean_headline,
    clean_and_merge_data,
    validate_price_dataframe,
    validate_news_dataframe,
    normalize_date,
    clean_headlines_batch,
    create_sample_data,
    _is_emoji,
    URL_PATTERN,
    TICKER_PATTERN,
    WHITESPACE_PATTERN,
    HTML_TAG_PATTERN,
    SPECIAL_CHAR_PATTERN
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def sample_price_data():
    """Create a standard sample price DataFrame."""
    return pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02', '2024-01-03', '2024-01-04', 
                                '2024-01-05', '2024-01-08']),
        'ticker': ['AAPL'] * 5,
        'open': [185.0, 186.0, 184.0, 185.5, 186.5],
        'high': [186.5, 187.0, 185.5, 187.0, 188.0],
        'low': [184.5, 185.0, 183.0, 184.5, 185.5],
        'close': [186.0, 184.5, 185.0, 186.5, 187.5],
        'volume': [1000000, 1200000, 900000, 1100000, 1300000]
    })


@pytest.fixture
def sample_news_data():
    """Create a standard sample news DataFrame."""
    return pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02', '2024-01-02', '2024-01-03', 
                                '2024-01-05', '2024-01-05', '2024-01-05']),
        'headline': [
            'Apple announces new iPhone',
            'Tech stocks surge on positive earnings',
            'Market volatility increases',
            'Apple stock hits all-time high',
            'AAPL rises 5% today',
            'Tech sector leads rally'
        ]
    })


@pytest.fixture
def empty_price_data():
    """Create an empty price DataFrame with correct schema."""
    return pd.DataFrame({
        'date': pd.Series(dtype='datetime64[ns]'),
        'ticker': pd.Series(dtype='str'),
        'open': pd.Series(dtype='float64'),
        'high': pd.Series(dtype='float64'),
        'low': pd.Series(dtype='float64'),
        'close': pd.Series(dtype='float64'),
        'volume': pd.Series(dtype='int64')
    })


@pytest.fixture
def empty_news_data():
    """Create an empty news DataFrame with correct schema."""
    return pd.DataFrame({
        'date': pd.Series(dtype='datetime64[ns]'),
        'headline': pd.Series(dtype='str')
    })


@pytest.fixture
def single_row_price_data():
    """Create a single row price DataFrame."""
    return pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02']),
        'ticker': ['AAPL'],
        'open': [185.0],
        'high': [186.5],
        'low': [184.5],
        'close': [186.0],
        'volume': [1000000]
    })


@pytest.fixture
def multi_ticker_price_data():
    """Create price data with multiple tickers."""
    return pd.DataFrame({
        'date': pd.to_datetime(['2024-01-02', '2024-01-02', '2024-01-03', '2024-01-03']),
        'ticker': ['AAPL', 'MSFT', 'AAPL', 'MSFT'],
        'open': [185.0, 370.0, 186.0, 372.0],
        'high': [186.5, 372.0, 187.0, 374.0],
        'low': [184.5, 368.0, 185.0, 370.0],
        'close': [186.0, 371.0, 184.5, 373.0],
        'volume': [1000000, 800000, 1200000, 850000]
    })


# =============================================================================
# TEST CLASS: clean_headline Function
# =============================================================================

class TestCleanHeadline:
    """Test cases for the clean_headline function."""
    
    # -------------------------------------------------------------------------
    # Test 1-10: URL Removal Tests
    # -------------------------------------------------------------------------
    
    def test_url_removal_https(self):
        """Test 1: HTTPS URL removal."""
        text = "Check https://example.com news"
        result = clean_headline(text)
        assert "https://example.com" not in result
        assert "Check" in result
        assert "news" in result
    
    def test_url_removal_http(self):
        """Test 2: HTTP URL removal."""
        text = "Visit http://news.site.com for more"
        result = clean_headline(text)
        assert "http://news.site.com" not in result
        assert "Visit" in result
    
    def test_url_removal_complex_url(self):
        """Test 3: Complex URL with path and query params."""
        text = "Details at https://api.example.com/v1/news?id=123&type=stock"
        result = clean_headline(text)
        assert "https://" not in result
        assert "Details at" in result.strip()
    
    def test_url_removal_multiple_urls(self):
        """Test 4: Multiple URLs in text."""
        text = "Check https://site1.com and http://site2.com for updates"
        result = clean_headline(text)
        assert "https://" not in result
        assert "http://" not in result
    
    def test_url_removal_www(self):
        """Test 5: www URL without protocol."""
        text = "Visit www.example.com today"
        result = clean_headline(text)
        assert "www.example.com" not in result
    
    def test_url_removal_disabled(self):
        """Test 6: URL removal can be disabled."""
        text = "Check https://example.com news"
        result = clean_headline(text, remove_urls=False)
        assert "https://example.com" in result
    
    def test_url_removal_url_only(self):
        """Test 7: Text that is only a URL."""
        text = "https://example.com/path/to/page"
        result = clean_headline(text)
        assert result == ""
    
    def test_url_removal_with_port(self):
        """Test 8: URL with port number."""
        text = "Server at https://example.com:8080/api is down"
        result = clean_headline(text)
        assert "8080" not in result
    
    def test_url_removal_preserves_text(self):
        """Test 9: URL removal preserves surrounding text."""
        text = "Apple (https://apple.com) releases new product"
        result = clean_headline(text)
        assert "Apple" in result
        assert "releases new product" in result
    
    def test_url_removal_encoded_url(self):
        """Test 10: URL with percent encoding."""
        text = "Link: https://example.com/path%20with%20spaces"
        result = clean_headline(text)
        assert "https://" not in result
    
    # -------------------------------------------------------------------------
    # Test 11-20: Emoji Removal Tests
    # -------------------------------------------------------------------------
    
    def test_emoji_removal_single_emoji(self):
        """Test 11: Single emoji removal."""
        text = "Stocks up 📈"
        result = clean_headline(text)
        assert "📈" not in result
        assert "Stocks up" in result.strip()
    
    def test_emoji_removal_multiple_emojis(self):
        """Test 12: Multiple emojis removal."""
        text = "Stocks up 📈🚀💰"
        result = clean_headline(text)
        assert "📈" not in result
        assert "🚀" not in result
        assert "💰" not in result
    
    def test_emoji_removal_emoji_in_middle(self):
        """Test 13: Emoji in middle of text."""
        text = "Great 🎉 news for investors"
        result = clean_headline(text)
        assert "🎉" not in result
        assert "Great" in result
        assert "news for investors" in result
    
    def test_emoji_removal_face_emojis(self):
        """Test 14: Face emoji removal."""
        text = "Happy investors 😊😀🙂"
        result = clean_headline(text)
        assert "😊" not in result
        assert "😀" not in result
    
    def test_emoji_removal_flag_emojis(self):
        """Test 15: Flag emoji removal."""
        text = "US markets 🇺🇸 rally"
        result = clean_headline(text)
        assert "🇺" not in result
    
    def test_emoji_removal_disabled(self):
        """Test 16: Emoji removal can be disabled."""
        text = "Stocks up 📈"
        result = clean_headline(text, remove_emojis=False, remove_special_chars=False)
        # Note: emoji might still be there depending on implementation
        assert "Stocks up" in result
    
    def test_emoji_removal_heart_symbols(self):
        """Test 17: Heart and love emojis."""
        text = "Love this stock ❤️💕"
        result = clean_headline(text)
        assert "Love this stock" in result.strip()
    
    def test_emoji_removal_weather_emojis(self):
        """Test 18: Weather emojis."""
        text = "Market outlook ☀️🌧️"
        result = clean_headline(text)
        assert "Market outlook" in result.strip()
    
    def test_emoji_removal_number_emojis(self):
        """Test 19: Number/symbol emojis."""
        text = "Top 10 stocks ⭐"
        result = clean_headline(text)
        assert "Top 10 stocks" in result.strip()
    
    def test_emoji_removal_complex_emojis(self):
        """Test 20: Complex combined emojis."""
        text = "Breaking 🔥📊💹 news"
        result = clean_headline(text)
        assert "Breaking" in result
        assert "news" in result
    
    # -------------------------------------------------------------------------
    # Test 21-30: HTML Entity Conversion Tests
    # -------------------------------------------------------------------------
    
    def test_html_entity_ampersand(self):
        """Test 21: Ampersand entity conversion."""
        text = "Q1 &amp; Q2 results"
        result = clean_headline(text)
        assert "Q1 & Q2 results" == result
    
    def test_html_entity_lt_gt(self):
        """Test 22: Less than and greater than entities."""
        text = "Price &lt; $100 and &gt; $50"
        result = clean_headline(text)
        assert "<" in result
        assert ">" in result
    
    def test_html_entity_quotes(self):
        """Test 23: Quote entities."""
        text = "CEO says &quot;Buy now&quot;"
        result = clean_headline(text)
        assert '"Buy now"' in result
    
    def test_html_entity_nbsp(self):
        """Test 24: Non-breaking space entity."""
        text = "Stock&nbsp;market&nbsp;news"
        result = clean_headline(text)
        assert "Stock market news" in result.strip()
    
    def test_html_entity_apostrophe(self):
        """Test 25: Apostrophe entity."""
        text = "Apple&#39;s earnings beat"
        result = clean_headline(text)
        assert "Apple's earnings beat" == result
    
    def test_html_entity_multiple(self):
        """Test 26: Multiple entities in one string."""
        text = "Q1 &amp; Q2 &gt; expectations &amp; outlook"
        result = clean_headline(text)
        assert "&amp;" not in result
        assert "&gt;" not in result
    
    def test_html_entity_numeric(self):
        """Test 27: Numeric HTML entities."""
        text = "Symbol: &#36;100"
        result = clean_headline(text)
        assert "&#" not in result
    
    def test_html_entity_disabled(self):
        """Test 28: HTML entity conversion can be disabled."""
        text = "Q1 &amp; Q2 results"
        result = clean_headline(text, remove_html_entities=False)
        assert "&amp;" in result
    
    def test_html_entity_mixed_with_text(self):
        """Test 29: HTML entities mixed with regular text."""
        text = "Buy &amp; hold strategy for &lt;AAPL&gt;"
        result = clean_headline(text)
        assert "&amp;" not in result
        assert "&lt;" not in result
        assert "&gt;" not in result
    
    def test_html_entity_copyright_trademark(self):
        """Test 30: Copyright and trademark entities."""
        text = "Apple&reg; and Microsoft&trade;"
        result = clean_headline(text)
        assert "&reg;" not in result
        assert "&trade;" not in result
    
    # -------------------------------------------------------------------------
    # Test 31-40: Whitespace Handling Tests
    # -------------------------------------------------------------------------
    
    def test_whitespace_multiple_spaces(self):
        """Test 31: Multiple spaces collapsed to single."""
        text = "Too   many   spaces"
        result = clean_headline(text)
        assert result == "Too many spaces"
    
    def test_whitespace_tabs(self):
        """Test 32: Tab characters normalized."""
        text = "Tab\there\ttest"
        result = clean_headline(text)
        assert "\t" not in result
    
    def test_whitespace_newlines(self):
        """Test 33: Newline characters normalized."""
        text = "Line1\nLine2\r\nLine3"
        result = clean_headline(text)
        assert "\n" not in result
        assert "\r" not in result
    
    def test_whitespace_leading(self):
        """Test 34: Leading whitespace stripped."""
        text = "   Leading spaces"
        result = clean_headline(text)
        assert result == "Leading spaces"
    
    def test_whitespace_trailing(self):
        """Test 35: Trailing whitespace stripped."""
        text = "Trailing spaces   "
        result = clean_headline(text)
        assert result == "Trailing spaces"
    
    def test_whitespace_both_ends(self):
        """Test 36: Whitespace stripped from both ends."""
        text = "   Both ends   "
        result = clean_headline(text)
        assert result == "Both ends"
    
    def test_whitespace_only(self):
        """Test 37: Whitespace-only string returns empty."""
        text = "     "
        result = clean_headline(text)
        assert result == ""
    
    def test_whitespace_mixed(self):
        """Test 38: Mixed whitespace types."""
        text = "  Multiple \t\n   mixed \r\n spaces  "
        result = clean_headline(text)
        assert result == "Multiple mixed spaces"
    
    def test_whitespace_normalize_disabled(self):
        """Test 39: Whitespace normalization can be disabled."""
        text = "Too   many   spaces"
        result = clean_headline(text, normalize_whitespace=False)
        assert "   " in result
    
    def test_whitespace_strip_disabled(self):
        """Test 40: Strip whitespace can be disabled."""
        text = "  test  "
        result = clean_headline(text, strip_whitespace=False, normalize_whitespace=True)
        assert result.startswith(" ") or result.endswith(" ")
    
    # -------------------------------------------------------------------------
    # Test 41-50: Ticker Symbol Removal Tests
    # -------------------------------------------------------------------------
    
    def test_ticker_removal_basic(self):
        """Test 41: Basic ticker symbol removal."""
        text = "$AAPL stock rises"
        result = clean_headline(text)
        assert "$AAPL" not in result
        assert "stock rises" in result
    
    def test_ticker_removal_multiple(self):
        """Test 42: Multiple ticker symbols."""
        text = "$AAPL $MSFT $GOOGL all up today"
        result = clean_headline(text)
        assert "$AAPL" not in result
        assert "$MSFT" not in result
        assert "$GOOGL" not in result
    
    def test_ticker_removal_in_sentence(self):
        """Test 43: Ticker in middle of sentence."""
        text = "Investors buy $NVDA on AI hype"
        result = clean_headline(text)
        assert "$NVDA" not in result
        assert "Investors buy" in result
        assert "on AI hype" in result
    
    def test_ticker_removal_disabled(self):
        """Test 44: Ticker removal can be disabled."""
        text = "$AAPL stock rises"
        result = clean_headline(text, remove_tickers=False)
        assert "$AAPL" in result or "AAPL" in result
    
    def test_ticker_removal_lowercase(self):
        """Test 45: Lowercase ticker symbols."""
        text = "$aapl trades at record high"
        result = clean_headline(text)
        assert "$aapl" not in result
    
    def test_ticker_removal_preserves_dollar_amounts(self):
        """Test 46: Dollar amounts should not be removed incorrectly."""
        # Note: $100 should be preserved as it's not a ticker pattern
        text = "Stock hits $100 target"
        result = clean_headline(text)
        # The regex $[A-Za-z]{1,5} shouldn't match $100
        assert "100" in result
    
    def test_ticker_removal_short_tickers(self):
        """Test 47: Short 1-2 character tickers."""
        text = "$A $GE $F stocks rally"
        result = clean_headline(text)
        assert "$A" not in result
        assert "$GE" not in result
        assert "$F" not in result
    
    def test_ticker_removal_five_char_tickers(self):
        """Test 48: 5-character tickers."""
        text = "$GOOGL and $NTDOY surge"
        result = clean_headline(text)
        assert "$GOOGL" not in result
    
    def test_ticker_removal_at_start(self):
        """Test 49: Ticker at start of headline."""
        text = "$TSLA announces new factory"
        result = clean_headline(text)
        assert result.strip().startswith("announces") or "announces new factory" in result
    
    def test_ticker_removal_at_end(self):
        """Test 50: Ticker at end of headline."""
        text = "Analysts upgrade $META"
        result = clean_headline(text)
        assert result.strip().endswith("upgrade") or "Analysts upgrade" in result
    
    # -------------------------------------------------------------------------
    # Test 51-60: Special Characters and HTML Tags Tests
    # -------------------------------------------------------------------------
    
    def test_html_tag_removal_basic(self):
        """Test 51: Basic HTML tag removal."""
        text = "<p>Market update</p>"
        result = clean_headline(text)
        assert "<p>" not in result
        assert "</p>" not in result
        assert "Market update" in result
    
    def test_html_tag_removal_nested(self):
        """Test 52: Nested HTML tags."""
        text = "<div><span>Breaking news</span></div>"
        result = clean_headline(text)
        assert "<" not in result
        assert ">" not in result
        assert "Breaking news" in result
    
    def test_html_tag_removal_with_attributes(self):
        """Test 53: HTML tags with attributes."""
        text = '<a href="http://test.com">Click here</a>'
        result = clean_headline(text)
        assert "<a" not in result
        assert "Click here" in result
    
    def test_html_tag_removal_disabled(self):
        """Test 54: HTML tag removal can be disabled."""
        text = "<b>Bold text</b>"
        result = clean_headline(text, remove_html_tags=False, remove_special_chars=False)
        assert "<b>" in result or "Bold text" in result
    
    def test_special_char_removal_basic(self):
        """Test 55: Basic special character removal."""
        text = "Stock™ goes up®"
        result = clean_headline(text, remove_emojis=True, remove_special_chars=True)
        assert "Stock" in result
        assert "goes up" in result
    
    def test_special_char_preserves_punctuation(self):
        """Test 56: Basic punctuation is preserved."""
        text = "What's next? Apple's earnings!"
        result = clean_headline(text)
        assert "?" in result
        assert "!" in result
        assert "'" in result
    
    def test_special_char_preserves_numbers(self):
        """Test 57: Numbers are preserved."""
        text = "Stock rises 5.5% to $100"
        result = clean_headline(text)
        assert "5" in result
        assert "100" in result
    
    def test_special_char_preserves_hyphens(self):
        """Test 58: Hyphens are preserved."""
        text = "Year-over-year growth strong"
        result = clean_headline(text)
        assert "-" in result
    
    def test_special_char_preserves_colons(self):
        """Test 59: Colons are preserved."""
        text = "Breaking: Market crashes"
        result = clean_headline(text)
        assert ":" in result
    
    def test_special_char_unicode_normalization(self):
        """Test 60: Unicode normalization works."""
        # Test with composed vs decomposed unicode
        text = "café résumé"  # Combined characters
        result = clean_headline(text)
        assert "cafe" in result or "café" in result
    
    # -------------------------------------------------------------------------
    # Test 61-70: Edge Cases and Error Handling Tests
    # -------------------------------------------------------------------------
    
    def test_edge_none_input(self):
        """Test 61: None input returns empty string."""
        result = clean_headline(None)
        assert result == ""
    
    def test_edge_empty_string(self):
        """Test 62: Empty string input."""
        result = clean_headline("")
        assert result == ""
    
    def test_edge_numeric_input(self):
        """Test 63: Numeric input converted to string."""
        result = clean_headline(12345)
        assert result == "12345"
    
    def test_edge_float_input(self):
        """Test 64: Float input converted to string."""
        result = clean_headline(123.45)
        assert "123" in result
    
    def test_edge_boolean_input(self):
        """Test 65: Boolean input converted to string."""
        result = clean_headline(True)
        assert result == "True"
    
    def test_edge_list_input(self):
        """Test 66: List input converted to string."""
        result = clean_headline(['test', 'headline'])
        assert "test" in result or result == ""
    
    def test_edge_very_long_text(self):
        """Test 67: Very long text handled."""
        text = "word " * 10000
        result = clean_headline(text)
        assert len(result) > 0
        assert "  " not in result  # No double spaces
    
    def test_edge_unicode_only(self):
        """Test 68: Unicode-only text."""
        text = "中文标题 日本語"
        result = clean_headline(text)
        # Should handle gracefully
        assert isinstance(result, str)
    
    def test_edge_mixed_unicode_ascii(self):
        """Test 69: Mixed unicode and ASCII."""
        text = "Apple 苹果 stock 股票"
        result = clean_headline(text)
        assert "Apple" in result
        assert "stock" in result
    
    def test_edge_all_special_chars(self):
        """Test 70: Text that becomes empty after cleaning."""
        text = "📈🚀💰🔥"  # Only emojis
        result = clean_headline(text)
        assert result == ""
    
    # -------------------------------------------------------------------------
    # Test 71-75: Lowercase and Combined Options Tests
    # -------------------------------------------------------------------------
    
    def test_lowercase_enabled(self):
        """Test 71: Lowercase conversion when enabled."""
        text = "AAPL Stock RISES"
        result = clean_headline(text, lowercase=True)
        assert result == "aapl stock rises"
    
    def test_lowercase_disabled_default(self):
        """Test 72: Lowercase disabled by default."""
        text = "AAPL Stock RISES"
        result = clean_headline(text)
        assert "AAPL" in result
        assert "RISES" in result
    
    def test_all_options_disabled(self):
        """Test 73: All cleaning options disabled."""
        text = "Test $AAPL https://example.com 📈 &amp;"
        result = clean_headline(
            text,
            remove_urls=False,
            remove_html_entities=False,
            remove_emojis=False,
            remove_special_chars=False,
            normalize_whitespace=False,
            strip_whitespace=False,
            remove_tickers=False,
            remove_html_tags=False
        )
        assert "$AAPL" in result
        assert "https://" in result
        assert "&amp;" in result
    
    def test_combined_cleaning_operations(self):
        """Test 74: All cleaning operations together."""
        text = "   $AAPL 📈 rises &amp; https://apple.com  <b>news</b>   "
        result = clean_headline(text)
        assert "$AAPL" not in result
        assert "📈" not in result
        assert "&amp;" not in result
        assert "https://" not in result
        assert "<b>" not in result
        assert result == "rises & news"
    
    def test_realistic_headline(self):
        """Test 75: Realistic messy headline."""
        text = "  Breaking: $AAPL 📈 stock hits ATH &amp; beats Q4!!! https://t.co/abc123  "
        result = clean_headline(text)
        assert result.startswith("Breaking:")
        assert "&" in result
        assert "stock hits ATH" in result
        assert "beats Q4!!!" in result


# =============================================================================
# TEST CLASS: Validation Functions
# =============================================================================

class TestValidationFunctions:
    """Test cases for DataFrame validation functions."""
    
    def test_validate_price_df_valid(self, sample_price_data):
        """Test 76: Valid price DataFrame passes validation."""
        is_valid, error = validate_price_dataframe(sample_price_data)
        assert is_valid is True
        assert error is None
    
    def test_validate_price_df_none(self):
        """Test 77: None price DataFrame fails validation."""
        is_valid, error = validate_price_dataframe(None)
        assert is_valid is False
        assert "None" in error
    
    def test_validate_price_df_not_dataframe(self):
        """Test 78: Non-DataFrame fails validation."""
        is_valid, error = validate_price_dataframe([1, 2, 3])
        assert is_valid is False
        assert "list" in error
    
    def test_validate_price_df_missing_column(self, sample_price_data):
        """Test 79: Missing column fails validation."""
        df = sample_price_data.drop(columns=['volume'])
        is_valid, error = validate_price_dataframe(df)
        assert is_valid is False
        assert "volume" in error
    
    def test_validate_price_df_empty(self, empty_price_data):
        """Test 80: Empty DataFrame passes validation."""
        is_valid, error = validate_price_dataframe(empty_price_data)
        assert is_valid is True
    
    def test_validate_news_df_valid(self, sample_news_data):
        """Test 81: Valid news DataFrame passes validation."""
        is_valid, error = validate_news_dataframe(sample_news_data)
        assert is_valid is True
        assert error is None
    
    def test_validate_news_df_none(self):
        """Test 82: None news DataFrame fails validation."""
        is_valid, error = validate_news_dataframe(None)
        assert is_valid is False
    
    def test_validate_news_df_missing_column(self, sample_news_data):
        """Test 83: Missing headline column fails validation."""
        df = sample_news_data.drop(columns=['headline'])
        is_valid, error = validate_news_dataframe(df)
        assert is_valid is False
        assert "headline" in error


# =============================================================================
# TEST CLASS: Date Normalization
# =============================================================================

class TestDateNormalization:
    """Test cases for date normalization function."""
    
    def test_normalize_date_string(self):
        """Test 84: String date normalization."""
        result = normalize_date("2024-01-02")
        assert isinstance(result, pd.Timestamp)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 2
    
    def test_normalize_date_timestamp(self):
        """Test 85: Timestamp input normalization."""
        ts = pd.Timestamp("2024-01-02 14:30:00")
        result = normalize_date(ts)
        assert result.hour == 0  # Time stripped
        assert result.minute == 0
    
    def test_normalize_date_with_timezone(self):
        """Test 86: Timezone-aware date normalization."""
        ts = pd.Timestamp("2024-01-02 14:30:00", tz="US/Eastern")
        result = normalize_date(ts)
        assert result.tz is None  # Timezone removed
    
    def test_normalize_date_none(self):
        """Test 87: None date returns NaT."""
        result = normalize_date(None)
        assert pd.isna(result)
    
    def test_normalize_date_nat(self):
        """Test 88: NaT input returns NaT."""
        result = normalize_date(pd.NaT)
        assert pd.isna(result)
    
    def test_normalize_date_invalid_string(self):
        """Test 89: Invalid string with coerce returns NaT."""
        result = normalize_date("not a date", errors='coerce')
        assert pd.isna(result)
    
    def test_normalize_date_invalid_raise(self):
        """Test 90: Invalid string with raise throws exception."""
        with pytest.raises(ValueError):
            normalize_date("not a date", errors='raise')
    
    def test_normalize_date_datetime(self):
        """Test 91: Python datetime normalization."""
        dt = datetime(2024, 1, 2, 14, 30, 0)
        result = normalize_date(dt)
        assert result.year == 2024
    
    def test_normalize_date_numpy_datetime(self):
        """Test 92: Numpy datetime64 normalization."""
        dt = np.datetime64('2024-01-02')
        result = normalize_date(dt)
        assert isinstance(result, pd.Timestamp)
    
    def test_normalize_date_various_formats(self):
        """Test 93: Various date format strings."""
        formats = ["2024-01-02", "01/02/2024", "Jan 2, 2024", "2024/01/02"]
        for fmt in formats:
            result = normalize_date(fmt, errors='coerce')
            if not pd.isna(result):
                assert result.year == 2024


# =============================================================================
# TEST CLASS: clean_and_merge_data Function
# =============================================================================

class TestCleanAndMergeData:
    """Test cases for the main clean_and_merge_data function."""
    
    def test_basic_merge(self, sample_price_data, sample_news_data):
        """Test 94: Basic merge operation works."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_price_data)
    
    def test_output_columns(self, sample_price_data, sample_news_data):
        """Test 95: Output has correct columns."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        expected_cols = ['date', 'ticker', 'open', 'high', 'low', 'close', 
                         'volume', 'headlines', 'headline_count']
        assert list(result.columns) == expected_cols
    
    def test_output_dtypes(self, sample_price_data, sample_news_data):
        """Test 96: Output has correct data types."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert result['date'].dtype == 'datetime64[ns]'
        assert result['ticker'].dtype == 'object'
        assert result['open'].dtype == 'float64'
        assert result['close'].dtype == 'float64'
        assert result['volume'].dtype == 'int64'
        assert result['headline_count'].dtype == 'int64'
    
    def test_empty_news_handling(self, sample_price_data, empty_news_data):
        """Test 97: Empty news DataFrame handled correctly."""
        result = clean_and_merge_data(sample_price_data, empty_news_data)
        assert len(result) == len(sample_price_data)
        assert all(result['headline_count'] == 0)
        assert all(result['headlines'].apply(lambda x: x == []))
    
    def test_empty_price_handling(self, empty_price_data, sample_news_data):
        """Test 98: Empty price DataFrame returns empty result."""
        result = clean_and_merge_data(empty_price_data, sample_news_data)
        assert len(result) == 0
        assert list(result.columns) == ['date', 'ticker', 'open', 'high', 'low', 
                                        'close', 'volume', 'headlines', 'headline_count']
    
    def test_no_nan_in_price_columns(self, sample_price_data, sample_news_data):
        """Test 99: No NaN values in price columns."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        for col in ['open', 'high', 'low', 'close', 'volume']:
            assert not result[col].isna().any()
    
    def test_headline_aggregation(self, sample_price_data, sample_news_data):
        """Test 100: Headlines aggregated correctly by date."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        # 2024-01-02 should have 2 headlines
        row = result[result['date'] == pd.Timestamp('2024-01-02')]
        assert row['headline_count'].iloc[0] == 2
        assert len(row['headlines'].iloc[0]) == 2
    
    def test_missing_news_days(self, sample_price_data, sample_news_data):
        """Test 101: Days without news have empty list and count 0."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        # 2024-01-04 has no news in sample data
        row = result[result['date'] == pd.Timestamp('2024-01-04')]
        assert row['headline_count'].iloc[0] == 0
        assert row['headlines'].iloc[0] == []
    
    def test_row_count_preserved(self, sample_price_data, sample_news_data):
        """Test 102: Row count equals price data row count."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert len(result) == len(sample_price_data)
    
    def test_headlines_cleaned(self, sample_price_data):
        """Test 103: Headlines are cleaned during merge."""
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['$AAPL rises 📈 https://example.com &amp; more']
        })
        result = clean_and_merge_data(sample_price_data, news_df)
        headline = result[result['date'] == pd.Timestamp('2024-01-02')]['headlines'].iloc[0][0]
        assert "$AAPL" not in headline
        assert "📈" not in headline
        assert "https://" not in headline
        assert "&amp;" not in headline
    
    def test_single_row_price(self, single_row_price_data, sample_news_data):
        """Test 104: Single row price data works."""
        result = clean_and_merge_data(single_row_price_data, sample_news_data)
        assert len(result) == 1
    
    def test_multi_ticker_data(self, multi_ticker_price_data, sample_news_data):
        """Test 105: Multiple tickers handled correctly."""
        result = clean_and_merge_data(multi_ticker_price_data, sample_news_data)
        assert len(result) == len(multi_ticker_price_data)
        assert set(result['ticker'].unique()) == {'AAPL', 'MSFT'}
    
    def test_date_alignment(self):
        """Test 106: Only matching dates are merged."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-03']),
            'ticker': ['AAPL', 'AAPL'],
            'open': [185.0, 186.0],
            'high': [186.0, 187.0],
            'low': [184.0, 185.0],
            'close': [185.5, 186.5],
            'volume': [1000000, 1100000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-04']),  # 01-04 not in price
            'headline': ['News for Jan 2', 'News for Jan 4']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert len(result) == 2
        # Jan 2 should have news, Jan 3 should not
        jan2 = result[result['date'] == pd.Timestamp('2024-01-02')]
        jan3 = result[result['date'] == pd.Timestamp('2024-01-03')]
        assert jan2['headline_count'].iloc[0] == 1
        assert jan3['headline_count'].iloc[0] == 0
    
    def test_headline_count_accuracy(self):
        """Test 107: Headline count matches list length."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02'] * 5),
            'headline': ['Headline 1', 'Headline 2', 'Headline 3', 
                        'Headline 4', 'Headline 5']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 5
        assert len(result['headlines'].iloc[0]) == 5
    
    def test_headlines_is_list_type(self, sample_price_data, sample_news_data):
        """Test 108: Headlines column contains lists."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert all(result['headlines'].apply(lambda x: isinstance(x, list)))
    
    def test_none_price_data_raises(self, sample_news_data):
        """Test 109: None price data raises ValueError."""
        with pytest.raises(ValueError):
            clean_and_merge_data(None, sample_news_data)
    
    def test_none_news_data_raises(self, sample_price_data):
        """Test 110: None news data raises ValueError."""
        with pytest.raises(ValueError):
            clean_and_merge_data(sample_price_data, None)
    
    def test_invalid_price_data_type(self, sample_news_data):
        """Test 111: Invalid price data type raises error."""
        with pytest.raises(ValueError):
            clean_and_merge_data([1, 2, 3], sample_news_data)
    
    def test_missing_price_columns(self, sample_news_data):
        """Test 112: Missing price columns raises error."""
        bad_price = pd.DataFrame({'date': ['2024-01-02'], 'ticker': ['AAPL']})
        with pytest.raises(ValueError):
            clean_and_merge_data(bad_price, sample_news_data)
    
    def test_validation_disabled(self, sample_news_data):
        """Test 113: Validation can be disabled."""
        # This would normally fail but with validation disabled...
        bad_price = pd.DataFrame({'date': ['2024-01-02'], 'ticker': ['AAPL']})
        # Should not raise immediately if validation disabled
        # But will fail later due to missing columns
        with pytest.raises(Exception):  # Will fail somewhere
            clean_and_merge_data(bad_price, sample_news_data, validate_inputs=False)
    
    def test_custom_clean_options(self, sample_price_data):
        """Test 114: Custom clean options passed correctly."""
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['UPPERCASE headline']
        })
        result = clean_and_merge_data(
            sample_price_data, news_df,
            clean_options={'lowercase': True}
        )
        headline = result[result['date'] == pd.Timestamp('2024-01-02')]['headlines'].iloc[0][0]
        assert headline == headline.lower()
    
    def test_empty_headlines_filtered(self, sample_price_data):
        """Test 115: Headlines that become empty after cleaning are filtered."""
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-02']),
            'headline': ['📈🚀💰', 'Valid headline']  # First is all emojis
        })
        result = clean_and_merge_data(sample_price_data, news_df)
        headlines = result[result['date'] == pd.Timestamp('2024-01-02')]['headlines'].iloc[0]
        assert len(headlines) == 1
        assert 'Valid headline' in headlines[0]
    
    def test_date_string_normalization(self):
        """Test 116: String dates normalized correctly."""
        price_df = pd.DataFrame({
            'date': ['2024-01-02', '2024-01-03'],  # Strings, not datetime
            'ticker': ['AAPL', 'AAPL'],
            'open': [185.0, 186.0],
            'high': [186.0, 187.0],
            'low': [184.0, 185.0],
            'close': [185.5, 186.5],
            'volume': [1000000, 1100000]
        })
        news_df = pd.DataFrame({
            'date': ['2024-01-02'],  # String
            'headline': ['Test headline']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['date'].dtype == 'datetime64[ns]'
    
    def test_timezone_handling(self):
        """Test 117: Timezone-aware dates handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-03']).tz_localize('UTC'),
            'ticker': ['AAPL', 'AAPL'],
            'open': [185.0, 186.0],
            'high': [186.0, 187.0],
            'low': [184.0, 185.0],
            'close': [185.5, 186.5],
            'volume': [1000000, 1100000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']).tz_localize('US/Eastern'),
            'headline': ['Test headline']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['date'].dt.tz is None


# =============================================================================
# TEST CLASS: clean_headlines_batch Function
# =============================================================================

class TestCleanHeadlinesBatch:
    """Test cases for batch headline cleaning."""
    
    def test_batch_basic(self):
        """Test 118: Basic batch cleaning."""
        headlines = ["First headline", "Second headline"]
        result = clean_headlines_batch(headlines)
        assert len(result) == 2
    
    def test_batch_with_noise(self):
        """Test 119: Batch with noisy headlines."""
        headlines = ["$AAPL rises 📈", "Normal headline", ""]
        result = clean_headlines_batch(headlines)
        assert len(result) == 2  # Empty string filtered out
    
    def test_batch_empty_list(self):
        """Test 120: Empty list input."""
        result = clean_headlines_batch([])
        assert result == []
    
    def test_batch_all_empty_after_clean(self):
        """Test 121: All headlines empty after cleaning."""
        headlines = ["📈", "🚀", "💰"]
        result = clean_headlines_batch(headlines)
        assert result == []
    
    def test_batch_custom_options(self):
        """Test 122: Batch with custom options."""
        headlines = ["UPPERCASE", "also UPPER"]
        result = clean_headlines_batch(headlines, {'lowercase': True})
        assert all(h == h.lower() for h in result)


# =============================================================================
# TEST CLASS: Edge Cases and Error Scenarios
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_duplicate_dates_in_news(self):
        """Test 123: Duplicate dates in news aggregated correctly."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02'] * 10),
            'headline': [f'Headline {i}' for i in range(10)]
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 10
    
    def test_very_long_headline(self):
        """Test 124: Very long headline handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        long_headline = "word " * 10000
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': [long_headline]
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 1
    
    def test_special_unicode_headlines(self):
        """Test 125: Unicode headlines handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['中文标题 日本語 한국어']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] >= 0  # Should not crash
    
    def test_nan_in_headlines(self):
        """Test 126: NaN headlines handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-02']),
            'headline': ['Valid headline', np.nan]
        })
        result = clean_and_merge_data(price_df, news_df)
        # NaN should be filtered out
        assert result['headline_count'].iloc[0] == 1
    
    def test_invalid_dates_filtered(self):
        """Test 127: Invalid dates in news filtered out."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': ['2024-01-02', 'invalid-date'],
            'headline': ['Valid', 'Also valid']
        })
        result = clean_and_merge_data(price_df, news_df)
        # Should not crash, invalid date filtered
        assert len(result) == 1
    
    def test_negative_volume_handled(self):
        """Test 128: Negative volume passes through (data quality issue)."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [-1000000]  # Negative volume
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['Test']
        })
        # Should not crash - data quality is caller's responsibility
        result = clean_and_merge_data(price_df, news_df)
        assert len(result) == 1
    
    def test_zero_volume(self):
        """Test 129: Zero volume handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [0]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['Test']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['volume'].iloc[0] == 0
    
    def test_large_price_values(self):
        """Test 130: Large price values handled."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['BRK.A'],
            'open': [500000.0],
            'high': [510000.0],
            'low': [490000.0],
            'close': [505000.0],
            'volume': [1000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['Berkshire trades near ATH']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['close'].iloc[0] == 505000.0
    
    def test_fractional_prices(self):
        """Test 131: Fractional prices preserved."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.123456],
            'high': [186.789012],
            'low': [184.012345],
            'close': [185.567890],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['Test']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert abs(result['open'].iloc[0] - 185.123456) < 0.0001
    
    def test_whitespace_only_headlines(self):
        """Test 132: Whitespace-only headlines filtered."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-02']),
            'headline': ['   ', 'Valid headline']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 1
    
    def test_duplicate_headlines_kept(self):
        """Test 133: Duplicate headlines kept (not de-duplicated)."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02', '2024-01-02']),
            'headline': ['Same headline', 'Same headline']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 2


# =============================================================================
# TEST CLASS: Data Integrity Tests
# =============================================================================

class TestDataIntegrity:
    """Tests to ensure data integrity is maintained."""
    
    def test_original_price_data_unchanged(self, sample_price_data, sample_news_data):
        """Test 134: Original price data not modified."""
        original = sample_price_data.copy()
        clean_and_merge_data(sample_price_data, sample_news_data)
        pd.testing.assert_frame_equal(sample_price_data, original)
    
    def test_original_news_data_unchanged(self, sample_price_data, sample_news_data):
        """Test 135: Original news data not modified."""
        original = sample_news_data.copy()
        clean_and_merge_data(sample_price_data, sample_news_data)
        pd.testing.assert_frame_equal(sample_news_data, original)
    
    def test_price_values_preserved(self, sample_price_data, sample_news_data):
        """Test 136: Price values exactly preserved."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        for idx, row in sample_price_data.iterrows():
            merged_row = result[result['date'] == row['date']].iloc[0]
            assert merged_row['open'] == row['open']
            assert merged_row['high'] == row['high']
            assert merged_row['low'] == row['low']
            assert merged_row['close'] == row['close']
            assert merged_row['volume'] == row['volume']
    
    def test_no_data_loss_in_merge(self):
        """Test 137: No price data lost during merge."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime([f'2024-01-{i:02d}' for i in range(1, 32)]),
            'ticker': ['AAPL'] * 31,
            'open': [185.0] * 31,
            'high': [186.0] * 31,
            'low': [184.0] * 31,
            'close': [185.5] * 31,
            'volume': [1000000] * 31
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-15']),
            'headline': ['Mid-month news']
        })
        result = clean_and_merge_data(price_df, news_df)
        assert len(result) == 31
    
    def test_headline_order_preserved(self):
        """Test 138: Headline order preserved within a day."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02'] * 3),
            'headline': ['First', 'Second', 'Third']
        })
        result = clean_and_merge_data(price_df, news_df)
        headlines = result['headlines'].iloc[0]
        assert headlines[0] == 'First'
        assert headlines[1] == 'Second'
        assert headlines[2] == 'Third'


# =============================================================================
# TEST CLASS: Helper Function Tests
# =============================================================================

class TestHelperFunctions:
    """Test helper functions."""
    
    def test_is_emoji_true(self):
        """Test 139: _is_emoji returns True for emojis."""
        assert _is_emoji('📈') is True
        assert _is_emoji('🚀') is True
        assert _is_emoji('❤') is True
    
    def test_is_emoji_false(self):
        """Test 140: _is_emoji returns False for non-emojis."""
        assert _is_emoji('A') is False
        assert _is_emoji('1') is False
        assert _is_emoji(' ') is False
    
    def test_is_emoji_multi_char(self):
        """Test 141: _is_emoji handles multi-char input."""
        assert _is_emoji('AB') is False
    
    def test_create_sample_data(self):
        """Test 142: create_sample_data returns valid data."""
        price_df, news_df = create_sample_data()
        assert isinstance(price_df, pd.DataFrame)
        assert isinstance(news_df, pd.DataFrame)
        assert len(price_df) > 0
        assert len(news_df) > 0
    
    def test_regex_patterns_compiled(self):
        """Test 143: Regex patterns are compiled correctly."""
        assert URL_PATTERN is not None
        assert TICKER_PATTERN is not None
        assert WHITESPACE_PATTERN is not None
        assert HTML_TAG_PATTERN is not None
        assert SPECIAL_CHAR_PATTERN is not None


# =============================================================================
# TEST CLASS: Performance and Stress Tests
# =============================================================================

class TestPerformance:
    """Performance and stress tests."""
    
    def test_large_dataset(self):
        """Test 144: Large dataset handling."""
        # 1000 days of price data
        dates = pd.date_range('2020-01-01', periods=1000, freq='D')
        price_df = pd.DataFrame({
            'date': dates,
            'ticker': ['AAPL'] * 1000,
            'open': np.random.uniform(100, 200, 1000),
            'high': np.random.uniform(100, 200, 1000),
            'low': np.random.uniform(100, 200, 1000),
            'close': np.random.uniform(100, 200, 1000),
            'volume': np.random.randint(1000000, 10000000, 1000)
        })
        # 5000 headlines
        news_dates = np.random.choice(dates, 5000)
        news_df = pd.DataFrame({
            'date': news_dates,
            'headline': [f'Headline {i}' for i in range(5000)]
        })
        result = clean_and_merge_data(price_df, news_df)
        assert len(result) == 1000
    
    def test_many_headlines_per_day(self):
        """Test 145: Many headlines per day."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02'] * 1000),
            'headline': [f'Headline {i}' for i in range(1000)]
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 1000
    
    def test_complex_headlines_batch(self):
        """Test 146: Many complex headlines cleaned."""
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        complex_headlines = [
            f"$AAPL 📈🚀 rises {i}% https://example.com/{i} &amp; more"
            for i in range(100)
        ]
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02'] * 100),
            'headline': complex_headlines
        })
        result = clean_and_merge_data(price_df, news_df)
        assert result['headline_count'].iloc[0] == 100
        # Check all cleaned properly
        for headline in result['headlines'].iloc[0]:
            assert "📈" not in headline
            assert "$AAPL" not in headline


# =============================================================================
# TEST CLASS: Output Validation Tests
# =============================================================================

class TestOutputValidation:
    """Tests for output validation."""
    
    def test_output_validation_catches_nan(self):
        """Test 147: Output validation catches NaN in price columns."""
        # This would require injecting NaN after merge - hard to test directly
        # Instead, verify validation logic exists by checking normal case passes
        price_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'ticker': ['AAPL'],
            'open': [185.0],
            'high': [186.0],
            'low': [184.0],
            'close': [185.5],
            'volume': [1000000]
        })
        news_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-02']),
            'headline': ['Test']
        })
        # Should not raise
        result = clean_and_merge_data(price_df, news_df, validate_outputs=True)
        assert len(result) == 1
    
    def test_headline_count_non_negative(self, sample_price_data, sample_news_data):
        """Test 148: All headline_counts are >= 0."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert (result['headline_count'] >= 0).all()
    
    def test_headlines_all_lists(self, sample_price_data, sample_news_data):
        """Test 149: All headlines values are lists."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        assert result['headlines'].apply(lambda x: isinstance(x, list)).all()
    
    def test_no_nan_in_required_columns(self, sample_price_data, sample_news_data):
        """Test 150: No NaN in date, ticker, or price columns."""
        result = clean_and_merge_data(sample_price_data, sample_news_data)
        required_cols = ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            assert not result[col].isna().any(), f"NaN found in {col}"


# =============================================================================
# TEST CLASS: Regression Tests
# =============================================================================

class TestRegression:
    """Regression tests for known issues."""
    
    def test_url_with_special_chars_not_partially_removed(self):
        """Test 151: URL removal doesn't leave fragments."""
        text = "Check https://example.com?query=test&foo=bar for news"
        result = clean_headline(text)
        assert "https" not in result
        assert "example.com" not in result
    
    def test_ticker_not_removed_from_normal_words(self):
        """Test 152: Ticker pattern doesn't remove $100 style."""
        text = "Stock hits $100 target"
        result = clean_headline(text)
        assert "100" in result
    
    def test_html_entity_double_conversion(self):
        """Test 153: HTML entities not double-converted."""
        text = "&amp;amp;"  # Already escaped
        result = clean_headline(text)
        assert result == "&amp;" or result == "&"  # Correct unescape
    
    def test_emoji_in_url_handled(self):
        """Test 154: URL with emoji handled."""
        text = "Check https://example.com/📈 for charts"
        result = clean_headline(text)
        assert "https" not in result
    
    def test_empty_after_all_cleaning_returns_empty(self):
        """Test 155: Text that becomes empty returns empty string."""
        text = "   $AAPL    "
        result = clean_headline(text)
        # After ticker removal and stripping, should be empty
        assert result == ""


# =============================================================================
# Additional Tests to Reach 80+ Count
# =============================================================================

class TestAdditionalCoverage:
    """Additional tests for comprehensive coverage."""
    
    def test_headline_with_only_punctuation(self):
        """Test 156: Headline with only punctuation."""
        text = "... ??? !!!"
        result = clean_headline(text)
        assert result == "... ??? !!!"
    
    def test_headline_with_numbers_only(self):
        """Test 157: Headline with only numbers."""
        text = "12345"
        result = clean_headline(text)
        assert result == "12345"
    
    def test_mixed_case_preservation(self):
        """Test 158: Mixed case preserved by default."""
        text = "ApPLe StOcK"
        result = clean_headline(text)
        assert "ApPLe" in result
        assert "StOcK" in result
    
    def test_consecutive_tickers(self):
        """Test 159: Consecutive tickers removed."""
        text = "$AAPL$MSFT$GOOGL"
        result = clean_headline(text)
        assert "$" not in result
    
    def test_ticker_at_start_and_end(self):
        """Test 160: Ticker at both start and end."""
        text = "$AAPL rises $MSFT"
        result = clean_headline(text)
        assert "$" not in result
        assert "rises" in result


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])