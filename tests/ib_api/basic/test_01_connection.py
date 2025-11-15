"""
Test 01: Basic IB Gateway/TWS Connection

Tests basic connection functionality to IB Gateway or TWS.
This is the most fundamental test - all other tests depend on successful connection.

Test Coverage:
- Connect to IB Gateway/TWS
- Verify connection status
- Retrieve server time
- Get managed accounts
- Disconnect cleanly
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from base_test import BaseConnectionTest
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

# Set up logging
setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.connection
@pytest.mark.critical
@pytest.mark.smoke
@pytest.mark.fast
class TestBasicConnection(BaseConnectionTest):
    """
    Basic connection tests for IB Gateway/TWS.

    These tests verify that we can establish and manage connections
    to IB Gateway or TWS successfully.
    """

    def test_01_verify_config(self):
        """
        Test 01.1: Verify test configuration is correct

        Verifies that:
        - Port is 7497 (paper trading)
        - Host is 127.0.0.1 (localhost)
        - Client ID is valid
        """
        self.log_test_info("Verifying test configuration")

        # Verify paper trading port
        self.assertEqual(
            TestConfig.IB_PORT,
            7497,
            f"Must use paper trading port 7497, not {TestConfig.IB_PORT}"
        )

        # Verify localhost
        self.assertEqual(
            TestConfig.IB_HOST,
            '127.0.0.1',
            f"Must use localhost 127.0.0.1, not {TestConfig.IB_HOST}"
        )

        # Verify client ID is positive
        self.assertGreater(
            TestConfig.IB_CLIENT_ID,
            0,
            "Client ID must be positive"
        )

        self.log_test_info(f"Configuration verified: {TestConfig.IB_HOST}:{TestConfig.IB_PORT} (Client ID: {TestConfig.IB_CLIENT_ID})")

    def test_02_connect_success(self):
        """
        Test 01.2: Successful connection to IB Gateway

        Verifies that:
        - Connection can be established
        - Connection status is True
        - No errors during connection
        """
        self.log_test_info("Testing successful connection")

        # Attempt connection
        result = self.connect()

        # Verify connection succeeded
        self.assertTrue(result, "Connection should succeed")
        self.assert_connected()

        self.log_test_info("✅ Connection successful")

    def test_03_get_server_time(self):
        """
        Test 01.3: Retrieve server time

        Verifies that:
        - Server time can be retrieved
        - Server time is valid datetime
        - Server time is recent (within last minute)
        """
        self.log_test_info("Testing server time retrieval")

        # Connect
        self.assertTrue(self.connect(), "Failed to connect")

        # Get server time
        server_time = self.ib.reqCurrentTime()

        # Verify server time is not None
        self.assertIsNotNone(server_time, "Server time should not be None")

        # Log server time
        self.log_test_info(f"Server time: {server_time}")

        # Verify it's a datetime object
        from datetime import datetime
        self.assertIsInstance(server_time, datetime, "Server time should be datetime object")

        # Verify time is recent (within last 1 minute)
        import time
        time_diff = abs(time.time() - server_time.timestamp())
        self.assertLess(time_diff, 60, "Server time should be within 1 minute of current time")

        self.log_test_info("✅ Server time retrieved successfully")

    def test_04_get_managed_accounts(self):
        """
        Test 01.4: Retrieve managed accounts

        Verifies that:
        - Managed accounts can be retrieved
        - At least one account is available
        - Account format is valid (paper account starts with 'D')
        """
        self.log_test_info("Testing managed accounts retrieval")

        # Connect
        self.assertTrue(self.connect(), "Failed to connect")

        # Get managed accounts
        accounts = self.ib.managedAccounts()

        # Verify accounts exist
        self.assertIsNotNone(accounts, "Accounts should not be None")
        self.assertGreater(len(accounts), 0, "Should have at least one account")

        # Log accounts
        self.log_test_info(f"Managed accounts: {accounts}")

        # Verify paper trading account format (should start with 'D')
        if TestConfig.IS_PAPER_TRADING:
            for account in accounts:
                self.assertTrue(
                    account.startswith('D'),
                    f"Paper trading account should start with 'D', got: {account}"
                )
                self.log_test_info(f"✅ Valid paper trading account: {account}")
        else:
            self.log_test_warning("Not running on paper trading port!")

        self.log_test_info("✅ Managed accounts retrieved successfully")

    def test_05_disconnect_success(self):
        """
        Test 01.5: Clean disconnection

        Verifies that:
        - Disconnection completes without errors
        - Connection status becomes False after disconnect
        """
        self.log_test_info("Testing clean disconnection")

        # Connect first
        self.assertTrue(self.connect(), "Failed to connect")
        self.assert_connected()

        # Disconnect
        self.disconnect()

        # Verify disconnection
        self.assertFalse(self.connected, "Should be disconnected")
        self.assertFalse(self.ib.isConnected(), "IB should show disconnected status")

        self.log_test_info("✅ Disconnection successful")

    def test_06_reconnect_success(self):
        """
        Test 01.6: Reconnection after disconnect

        Verifies that:
        - Can disconnect and reconnect successfully
        - Multiple connect/disconnect cycles work
        """
        self.log_test_info("Testing reconnection capability")

        # Test 3 connection cycles
        for cycle in range(3):
            self.log_test_info(f"Connection cycle {cycle + 1}/3")

            # Connect
            result = self.connect()
            self.assertTrue(result, f"Connection cycle {cycle + 1} failed")
            self.assert_connected()

            # Verify account access
            accounts = self.ib.managedAccounts()
            self.assertGreater(len(accounts), 0, f"No accounts in cycle {cycle + 1}")

            # Disconnect
            self.disconnect()
            self.assertFalse(self.connected, f"Disconnect cycle {cycle + 1} failed")

            # Small delay between cycles
            if cycle < 2:
                self.ib.sleep(0.5)

        self.log_test_info("✅ Reconnection test successful (3 cycles)")

    def test_07_connection_timeout(self):
        """
        Test 01.7: Connection timeout handling

        Verifies that:
        - Connection attempt times out gracefully with invalid host
        - No hanging or crashes

        Note: This test uses a non-routable IP to force timeout
        """
        self.log_test_info("Testing connection timeout handling")

        # Save original settings
        original_host = self.HOST
        original_timeout = self.TIMEOUT

        try:
            # Use non-routable IP (192.0.2.0 is reserved for documentation)
            self.HOST = '192.0.2.1'
            self.TIMEOUT = 2  # Short timeout for faster test

            # Attempt connection (should timeout)
            result = self.connect()

            # Should fail to connect
            self.assertFalse(result, "Connection should timeout/fail with invalid host")
            self.assertFalse(self.connected, "Should not be connected")

            self.log_test_info("✅ Connection timeout handled correctly")

        finally:
            # Restore original settings
            self.HOST = original_host
            self.TIMEOUT = original_timeout

    def test_08_duplicate_client_id(self):
        """
        Test 01.8: Duplicate client ID handling

        Verifies that:
        - Second connection with same client ID is handled
        - Error message is appropriate

        Note: This test behavior depends on IB Gateway settings
        """
        self.log_test_info("Testing duplicate client ID handling")

        # First connection
        self.assertTrue(self.connect(client_id=100), "First connection failed")
        self.assert_connected()

        # Create second IB instance with same client ID
        from ib_insync import IB
        ib2 = IB()

        try:
            # Attempt second connection with same client ID
            # This might succeed or fail depending on IB Gateway settings
            ib2.connect(self.HOST, self.PORT, clientId=100, timeout=5)

            # If we get here, IB allows duplicate client IDs
            self.log_test_warning("IB Gateway allowed duplicate client ID")

            # Clean up second connection
            ib2.disconnect()

        except Exception as e:
            # Expected behavior: connection should fail
            self.log_test_info(f"Duplicate client ID correctly rejected: {e}")

        finally:
            # Ensure cleanup
            if ib2.isConnected():
                ib2.disconnect()

        self.log_test_info("✅ Duplicate client ID test completed")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
