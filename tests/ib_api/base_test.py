"""
Base Test Class for IB API Tests

Provides common setup, teardown, and utility methods for all IB API tests.
"""

import unittest
import time
import logging
from typing import Optional
from ib_insync import IB, util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseIBTest(unittest.TestCase):
    """
    Base test class for Interactive Brokers API tests.

    Provides:
    - Common IB connection setup/teardown
    - Configuration management
    - Utility methods for waiting and verification
    - Error handling helpers
    """

    # Default connection parameters (can be overridden in subclasses)
    HOST = '127.0.0.1'
    PORT = 7497  # Paper trading port
    CLIENT_ID = 1
    TIMEOUT = 10  # Connection timeout in seconds

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources (runs once per test class)"""
        logger.info(f"Setting up test class: {cls.__name__}")
        util.startLoop()  # Start asyncio event loop for ib_insync

    @classmethod
    def tearDownClass(cls):
        """Clean up class-level resources (runs once per test class)"""
        logger.info(f"Tearing down test class: {cls.__name__}")

    def setUp(self):
        """Set up test - runs before each test method"""
        logger.info(f"Setting up test: {self._testMethodName}")
        self.ib: Optional[IB] = None
        self.connected = False

    def tearDown(self):
        """Clean up after test - runs after each test method"""
        logger.info(f"Tearing down test: {self._testMethodName}")
        if self.ib and self.connected:
            try:
                self.disconnect()
            except Exception as e:
                logger.warning(f"Error during disconnect: {e}")

    def connect(self, client_id: Optional[int] = None) -> bool:
        """
        Connect to IB Gateway/TWS.

        Args:
            client_id: Client ID to use (default: self.CLIENT_ID)

        Returns:
            bool: True if connected successfully, False otherwise
        """
        if client_id is None:
            client_id = self.CLIENT_ID

        try:
            self.ib = IB()
            self.ib.connect(
                host=self.HOST,
                port=self.PORT,
                clientId=client_id,
                timeout=self.TIMEOUT
            )
            self.connected = True
            logger.info(f"Connected to IB Gateway at {self.HOST}:{self.PORT} with client ID {client_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from IB Gateway/TWS"""
        if self.ib and self.connected:
            try:
                self.ib.disconnect()
                self.connected = False
                logger.info("Disconnected from IB Gateway")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
                raise

    def wait_for_condition(self, condition_func, timeout: int = 5, interval: float = 0.1) -> bool:
        """
        Wait for a condition to become true.

        Args:
            condition_func: Callable that returns True when condition is met
            timeout: Maximum time to wait in seconds
            interval: Check interval in seconds

        Returns:
            bool: True if condition met, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False

    def wait_for_data(self, data_list, min_items: int = 1, timeout: int = 5) -> bool:
        """
        Wait for data to be populated in a list.

        Args:
            data_list: List to monitor
            min_items: Minimum number of items required
            timeout: Maximum time to wait in seconds

        Returns:
            bool: True if data received, False if timeout
        """
        return self.wait_for_condition(
            lambda: len(data_list) >= min_items,
            timeout=timeout
        )

    def assert_connected(self):
        """Assert that connection to IB is established"""
        self.assertTrue(self.ib is not None, "IB instance is None")
        self.assertTrue(self.connected, "Not connected to IB Gateway")
        self.assertTrue(self.ib.isConnected(), "IB connection status is False")

    def assert_account_available(self):
        """Assert that at least one account is available"""
        self.assert_connected()
        accounts = self.ib.managedAccounts()
        self.assertIsNotNone(accounts, "No managed accounts returned")
        self.assertGreater(len(accounts), 0, "No accounts available")

    def get_account(self) -> str:
        """
        Get the first available account.

        Returns:
            str: Account number
        """
        self.assert_account_available()
        return self.ib.managedAccounts()[0]

    def sleep(self, seconds: float):
        """
        Sleep for specified seconds (uses ib_insync sleep to maintain event loop).

        Args:
            seconds: Time to sleep in seconds
        """
        self.ib.sleep(seconds)

    def log_test_info(self, message: str):
        """Log informational message for test"""
        logger.info(f"[{self._testMethodName}] {message}")

    def log_test_warning(self, message: str):
        """Log warning message for test"""
        logger.warning(f"[{self._testMethodName}] {message}")

    def log_test_error(self, message: str):
        """Log error message for test"""
        logger.error(f"[{self._testMethodName}] {message}")


class BaseConnectionTest(BaseIBTest):
    """Base class specifically for connection-related tests"""

    def setUp(self):
        """Set up connection test - does not auto-connect"""
        super().setUp()
        self.log_test_info("Connection test setup complete")


class BaseMarketDataTest(BaseIBTest):
    """Base class specifically for market data tests"""

    def setUp(self):
        """Set up market data test - auto-connects"""
        super().setUp()
        self.assertTrue(self.connect(), "Failed to connect for market data test")
        self.log_test_info("Market data test setup complete")


class BaseAccountTest(BaseIBTest):
    """Base class specifically for account-related tests"""

    def setUp(self):
        """Set up account test - auto-connects"""
        super().setUp()
        self.assertTrue(self.connect(), "Failed to connect for account test")
        self.log_test_info("Account test setup complete")


class BaseOrderTest(BaseIBTest):
    """Base class specifically for order/execution tests"""

    def setUp(self):
        """Set up order test - auto-connects"""
        super().setUp()
        self.assertTrue(self.connect(), "Failed to connect for order test")
        self.log_test_info("Order test setup complete")

    def cancel_all_orders(self):
        """Cancel all open orders (cleanup helper)"""
        if self.ib and self.connected:
            try:
                open_orders = self.ib.openOrders()
                for order in open_orders:
                    self.ib.cancelOrder(order)
                self.log_test_info(f"Cancelled {len(open_orders)} open orders")
            except Exception as e:
                self.log_test_warning(f"Error cancelling orders: {e}")
