"""
Test Configuration for IB API Tests

Centralized configuration for all IB API testing.
Contains connection parameters, test symbols, timeouts, etc.
"""

import os
from typing import Dict, List


class TestConfig:
    """
    Configuration class for IB API tests.

    All test parameters should be configured here to ensure consistency
    across all test files.
    """

    # ===================================
    # IB Gateway / TWS Connection Settings
    # ===================================

    # Connection parameters
    IB_HOST = os.getenv('IB_HOST', '127.0.0.1')
    IB_PORT = int(os.getenv('IB_PORT', '7497'))  # 7497 = paper, 7496 = live
    IB_CLIENT_ID = int(os.getenv('IB_CLIENT_ID', '1'))
    IB_TIMEOUT = int(os.getenv('IB_TIMEOUT', '10'))  # Connection timeout in seconds

    # Trading mode verification
    IS_PAPER_TRADING = IB_PORT == 7497
    IS_LIVE_TRADING = IB_PORT == 7496

    # Safety check: Ensure we're using paper trading for tests
    @classmethod
    def verify_paper_trading(cls):
        """Verify that tests are running against paper trading account"""
        if not cls.IS_PAPER_TRADING:
            raise RuntimeError(
                f"SAFETY CHECK FAILED: Tests must use paper trading port (7497), "
                f"but configured port is {cls.IB_PORT}. "
                f"Set IB_PORT=7497 environment variable or update test_config.py"
            )

    # ===================================
    # Test Symbols
    # ===================================

    # Stocks
    TEST_STOCK_SYMBOLS = ['AAPL', 'MSFT', 'SPY', 'TSLA', 'IBKR']
    DEFAULT_STOCK_SYMBOL = 'AAPL'
    LIQUID_STOCK_SYMBOL = 'SPY'  # Highly liquid for testing

    # ETFs
    TEST_ETF_SYMBOLS = ['SPY', 'QQQ', 'IWM', 'DIA']

    # Forex
    TEST_FOREX_PAIRS = [
        ('EUR', 'USD'),
        ('GBP', 'USD'),
        ('USD', 'JPY'),
        ('AUD', 'USD')
    ]
    DEFAULT_FOREX_PAIR = ('EUR', 'USD')

    # Futures
    TEST_FUTURES_SYMBOLS = ['ES', 'NQ', 'YM', 'CL']
    DEFAULT_FUTURE_SYMBOL = 'ES'  # E-mini S&P 500

    # Indices
    TEST_INDEX_SYMBOLS = ['SPX', 'VIX', 'NDX']

    # ===================================
    # Test Order Quantities
    # ===================================

    # Small quantity for basic tests
    SMALL_ORDER_QTY = 1

    # Medium quantity for standard tests
    MEDIUM_ORDER_QTY = 10

    # Large quantity for volume tests
    LARGE_ORDER_QTY = 100

    # Default test quantity
    DEFAULT_ORDER_QTY = SMALL_ORDER_QTY

    # ===================================
    # Test Price Levels
    # ===================================

    # Offset from current price for limit orders (dollars)
    LIMIT_ORDER_OFFSET = 1.0

    # Offset from current price for stop orders (dollars)
    STOP_ORDER_OFFSET = 2.0

    # Take profit offset for bracket orders (dollars)
    TAKE_PROFIT_OFFSET = 5.0

    # Stop loss offset for bracket orders (dollars)
    STOP_LOSS_OFFSET = 3.0

    # ===================================
    # Timeouts and Delays
    # ===================================

    # Connection timeout (seconds)
    CONNECTION_TIMEOUT = 10

    # Data request timeout (seconds)
    DATA_REQUEST_TIMEOUT = 5

    # Order placement timeout (seconds)
    ORDER_TIMEOUT = 10

    # Market data update wait (seconds)
    MARKET_DATA_WAIT = 2

    # Sleep between tests (seconds)
    TEST_SLEEP = 0.5

    # Retry delay for connection attempts (seconds)
    RETRY_DELAY = 2

    # Maximum retry attempts
    MAX_RETRIES = 3

    # ===================================
    # Historical Data Settings
    # ===================================

    # Default historical data duration
    HISTORICAL_DURATION = '1 D'  # 1 day

    # Default bar size
    HISTORICAL_BAR_SIZE = '1 hour'

    # Alternative bar sizes for testing
    BAR_SIZES = ['1 min', '5 mins', '15 mins', '1 hour', '1 day']

    # What to show options
    WHAT_TO_SHOW_OPTIONS = ['TRADES', 'MIDPOINT', 'BID', 'ASK']

    # ===================================
    # Market Data Settings
    # ===================================

    # Generic tick types for market data
    GENERIC_TICK_LIST = ''  # Empty for basic data

    # Snapshot mode (True = single snapshot, False = streaming)
    DEFAULT_SNAPSHOT = False

    # ===================================
    # Account Settings
    # ===================================

    # Account tags to retrieve in summary
    ACCOUNT_SUMMARY_TAGS = [
        'AccountType',
        'NetLiquidation',
        'TotalCashValue',
        'SettledCash',
        'AccruedCash',
        'BuyingPower',
        'EquityWithLoanValue',
        'GrossPositionValue',
        'MaintMarginReq',
        'InitMarginReq',
        'AvailableFunds',
        'ExcessLiquidity'
    ]

    # ===================================
    # Test Behavior Flags
    # ===================================

    # Enable verbose logging in tests
    VERBOSE_LOGGING = os.getenv('VERBOSE_LOGGING', 'False').lower() == 'true'

    # Enable order placement (safety: False by default)
    ENABLE_ORDER_PLACEMENT = os.getenv('ENABLE_ORDER_PLACEMENT', 'False').lower() == 'true'

    # Cancel orders after test completion
    AUTO_CANCEL_ORDERS = True

    # Skip tests requiring market hours
    SKIP_MARKET_HOURS_TESTS = os.getenv('SKIP_MARKET_HOURS', 'False').lower() == 'true'

    # Run only connection tests (skip data/order tests)
    CONNECTION_TESTS_ONLY = os.getenv('CONNECTION_TESTS_ONLY', 'False').lower() == 'true'

    # ===================================
    # Test Result Settings
    # ===================================

    # Directory for test results
    RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

    # Enable CSV export of test results
    EXPORT_RESULTS_CSV = True

    # Enable JSON export of test results
    EXPORT_RESULTS_JSON = True

    # ===================================
    # Error Handling Settings
    # ===================================

    # Error codes to ignore (informational only)
    IGNORE_ERROR_CODES = [
        2104,  # Market data farm connection is OK
        2106,  # HMDS data farm connection is OK
        2158,  # Sec-def data farm connection is OK
    ]

    # Error codes that should fail tests
    CRITICAL_ERROR_CODES = [
        502,   # Couldn't connect to TWS
        504,   # Not connected
        1100,  # Connectivity between IB and TWS has been lost
        2110,  # Connectivity between TWS and server is broken
    ]

    # ===================================
    # Helper Methods
    # ===================================

    @classmethod
    def get_connection_params(cls) -> Dict[str, any]:
        """
        Get connection parameters as dictionary.

        Returns:
            Dict with host, port, clientId, timeout
        """
        return {
            'host': cls.IB_HOST,
            'port': cls.IB_PORT,
            'clientId': cls.IB_CLIENT_ID,
            'timeout': cls.IB_TIMEOUT
        }

    @classmethod
    def is_market_hours(cls) -> bool:
        """
        Check if current time is during market hours (approximate).

        Returns:
            bool: True if during market hours (9:30 AM - 4:00 PM ET)

        Note: This is a simplified check. Use IB API for accurate trading hours.
        """
        from datetime import datetime
        import pytz

        # Get current time in Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now_et = datetime.now(eastern)

        # Check if weekday
        if now_et.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False

        # Check if during market hours (9:30 AM - 4:00 PM ET)
        market_open = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now_et.replace(hour=16, minute=0, second=0, microsecond=0)

        return market_open <= now_et <= market_close

    @classmethod
    def get_test_account(cls, ib_instance) -> str:
        """
        Get first available test account from IB connection.

        Args:
            ib_instance: Connected IB instance

        Returns:
            str: Account number
        """
        accounts = ib_instance.managedAccounts()
        if not accounts:
            raise RuntimeError("No accounts available")

        account = accounts[0]

        # Verify it's a paper trading account (should start with 'D')
        if cls.IS_PAPER_TRADING and not account.startswith('D'):
            raise RuntimeError(
                f"Account {account} does not appear to be a paper trading account "
                f"(should start with 'D')"
            )

        return account

    @classmethod
    def print_config_summary(cls):
        """Print test configuration summary"""
        print("=" * 60)
        print("IB API Test Configuration")
        print("=" * 60)
        print(f"Host: {cls.IB_HOST}")
        print(f"Port: {cls.IB_PORT}")
        print(f"Client ID: {cls.IB_CLIENT_ID}")
        print(f"Timeout: {cls.IB_TIMEOUT}s")
        print(f"Trading Mode: {'PAPER' if cls.IS_PAPER_TRADING else 'LIVE'}")
        print(f"Default Stock: {cls.DEFAULT_STOCK_SYMBOL}")
        print(f"Default Quantity: {cls.DEFAULT_ORDER_QTY}")
        print(f"Order Placement: {'ENABLED' if cls.ENABLE_ORDER_PLACEMENT else 'DISABLED'}")
        print(f"Verbose Logging: {'YES' if cls.VERBOSE_LOGGING else 'NO'}")
        print("=" * 60)


# Create config instance
config = TestConfig()

# Perform safety check on import
if __name__ != '__main__':
    TestConfig.verify_paper_trading()
