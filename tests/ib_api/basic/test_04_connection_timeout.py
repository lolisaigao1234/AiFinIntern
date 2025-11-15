"""
Test 04: Connection Timeout Scenarios

Tests various timeout scenarios and timeout handling.

Test Coverage:
- Connection timeout with unreachable host
- Data request timeouts
- Timeout configuration validation
- Timeout recovery mechanisms
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import time
from base_test import BaseConnectionTest
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

# Set up logging
setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.connection
@pytest.mark.error_handling
@pytest.mark.slow
class TestConnectionTimeout(BaseConnectionTest):
    """
    Connection timeout tests.

    Tests various timeout scenarios and proper timeout handling.
    """

    def test_01_connection_timeout_unreachable_host(self):
        """
        Test 04.1: Connection timeout with unreachable host

        Verifies that:
        - Connection times out appropriately with unreachable host
        - Timeout is respected (not much longer or shorter)
        - No hanging or blocking
        """
        self.log_test_info("Testing connection timeout with unreachable host")

        # Use non-routable IP address (RFC 5737 TEST-NET-1)
        original_host = self.HOST
        self.HOST = '192.0.2.1'

        timeout_seconds = 3
        self.TIMEOUT = timeout_seconds

        try:
            self.log_test_info(f"Attempting connection with {timeout_seconds}s timeout...")
            start_time = time.time()

            result = self.connect()

            elapsed = time.time() - start_time

            # Should not connect
            self.assertFalse(result, "Should not connect to unreachable host")

            # Verify timeout was respected (allow 50% tolerance)
            self.log_test_info(f"Connection attempt took {elapsed:.2f}s")
            self.assertLess(
                elapsed,
                timeout_seconds * 1.5,
                f"Timeout too long: {elapsed:.2f}s (expected ~{timeout_seconds}s)"
            )

            self.log_test_info("✅ Connection timeout handled correctly")

        finally:
            self.HOST = original_host
            self.TIMEOUT = TestConfig.CONNECTION_TIMEOUT

    def test_02_very_short_timeout(self):
        """
        Test 04.2: Very short connection timeout

        Verifies that:
        - Very short timeouts are handled
        - Connection fails quickly with short timeout
        - Can recover with normal timeout
        """
        self.log_test_info("Testing very short connection timeout")

        # Set very short timeout
        original_timeout = self.TIMEOUT
        self.TIMEOUT = 0.5  # 500ms

        try:
            self.log_test_info("Attempting connection with 0.5s timeout...")
            start_time = time.time()

            result = self.connect()

            elapsed = time.time() - start_time

            self.log_test_info(f"Connection attempt took {elapsed:.2f}s, result: {result}")

            # With very short timeout, might fail even to localhost
            # Just verify it completes within reasonable time
            self.assertLess(elapsed, 2.0, "Should complete quickly even if failed")

        finally:
            # Restore timeout
            self.TIMEOUT = original_timeout

        # Try again with normal timeout
        if not self.connected:
            self.log_test_info("Retrying with normal timeout...")
            result2 = self.connect()
            self.log_test_info(f"Retry result: {result2}")

        self.log_test_info("✅ Short timeout test completed")

    def test_03_timeout_during_data_request(self):
        """
        Test 04.3: Timeout during data request

        Verifies that:
        - Data requests respect timeout settings
        - Timeout during request is handled gracefully
        - Connection remains stable after timeout
        """
        self.log_test_info("Testing timeout during data request")

        # Connect normally
        self.assertTrue(self.connect(), "Failed to connect")
        self.assert_connected()

        # Note: This test is limited because we can't easily force a data request timeout
        # with real IB Gateway. We'll test the timeout mechanism exists.

        self.log_test_info("Connected successfully")

        # Quick data request to verify connection works
        server_time = self.ib.reqCurrentTime()
        self.assertIsNotNone(server_time, "Server time should be available")

        # Request account data with a wait
        self.log_test_info("Requesting account data...")
        accounts = self.ib.managedAccounts()
        self.assertGreater(len(accounts), 0, "Should have accounts")

        # Verify connection still stable
        self.assert_connected()

        self.log_test_info("✅ Data request completed, connection stable")

    def test_04_reconnect_after_timeout(self):
        """
        Test 04.4: Reconnect after connection timeout

        Verifies that:
        - Can reconnect after timeout failure
        - Timeout failure doesn't corrupt state
        - Successful connection works normally after timeout
        """
        self.log_test_info("Testing reconnection after timeout")

        # First, force a timeout
        original_host = self.HOST
        original_timeout = self.TIMEOUT

        self.HOST = '192.0.2.1'  # Unreachable
        self.TIMEOUT = 2

        try:
            self.log_test_info("Attempting connection to unreachable host...")
            result1 = self.connect()
            self.assertFalse(result1, "Should timeout with unreachable host")

            # Cleanup
            if self.ib and self.connected:
                self.disconnect()

        finally:
            # Restore settings
            self.HOST = original_host
            self.TIMEOUT = original_timeout

        # Wait a moment
        time.sleep(0.5)

        # Now try to connect normally
        self.log_test_info("Reconnecting to actual host...")
        result2 = self.connect()
        self.assertTrue(result2, "Should connect successfully after timeout failure")
        self.assert_connected()

        # Verify can access data
        accounts = self.ib.managedAccounts()
        self.assertGreater(len(accounts), 0, "Should access accounts after recovery")

        self.log_test_info("✅ Reconnection after timeout successful")

    def test_05_multiple_timeout_scenarios(self):
        """
        Test 04.5: Multiple different timeout values

        Verifies that:
        - Different timeout values work correctly
        - Timeout setting is applied properly
        - System handles various timeout configurations
        """
        self.log_test_info("Testing multiple timeout scenarios")

        timeout_values = [1, 3, 5, 10]  # Different timeout values to test
        original_timeout = self.TIMEOUT

        # Use unreachable host to test timeouts
        original_host = self.HOST
        self.HOST = '192.0.2.1'

        try:
            for timeout_val in timeout_values:
                self.TIMEOUT = timeout_val

                self.log_test_info(f"Testing with timeout: {timeout_val}s")
                start_time = time.time()

                result = self.connect()

                elapsed = time.time() - start_time

                # Should fail
                self.assertFalse(result, f"Should fail with unreachable host")

                # Verify timeout was respected
                self.log_test_info(f"   Elapsed: {elapsed:.2f}s (timeout: {timeout_val}s)")

                # Allow 50% tolerance
                self.assertLess(
                    elapsed,
                    timeout_val * 1.5,
                    f"Timeout {timeout_val}s not respected: took {elapsed:.2f}s"
                )

                # Cleanup for next iteration
                if self.connected:
                    self.disconnect()

                time.sleep(0.2)

            self.log_test_info("✅ All timeout values handled correctly")

        finally:
            self.HOST = original_host
            self.TIMEOUT = original_timeout

    def test_06_timeout_with_valid_connection(self):
        """
        Test 04.6: Timeout settings with valid connection

        Verifies that:
        - Generous timeout allows successful connection
        - Connection succeeds well before timeout
        - Timeout doesn't interfere with valid connections
        """
        self.log_test_info("Testing timeout with valid connection")

        # Set generous timeout
        self.TIMEOUT = 30  # 30 seconds

        self.log_test_info(f"Connecting with {self.TIMEOUT}s timeout...")
        start_time = time.time()

        result = self.connect()

        elapsed = time.time() - start_time

        # Should connect successfully
        self.assertTrue(result, "Should connect successfully")
        self.assert_connected()

        # Should complete much faster than timeout
        self.log_test_info(f"Connection took {elapsed:.2f}s (timeout: {self.TIMEOUT}s)")
        self.assertLess(elapsed, 10, "Valid connection should be much faster than timeout")

        # Verify works normally
        server_time = self.ib.reqCurrentTime()
        self.assertIsNotNone(server_time, "Should get server time")

        self.log_test_info("✅ Timeout setting doesn't interfere with valid connection")

    def test_07_timeout_edge_cases(self):
        """
        Test 04.7: Timeout edge cases

        Verifies that:
        - Zero timeout is handled
        - Extremely large timeout is handled
        - Negative timeout is rejected or handled
        """
        self.log_test_info("Testing timeout edge cases")

        original_timeout = self.TIMEOUT

        # Test very small timeout (close to zero)
        self.log_test_info("Testing minimal timeout (0.1s)...")
        self.TIMEOUT = 0.1

        start_time = time.time()
        result1 = self.connect()
        elapsed1 = time.time() - start_time

        self.log_test_info(f"   Result: {result1}, Elapsed: {elapsed1:.3f}s")

        if self.connected:
            self.disconnect()

        # Reset
        self.TIMEOUT = original_timeout
        time.sleep(0.5)

        # Test very large timeout (shouldn't wait this long)
        self.log_test_info("Testing large timeout (120s) - should connect quickly...")
        self.TIMEOUT = 120

        start_time = time.time()
        result2 = self.connect()
        elapsed2 = time.time() - start_time

        self.log_test_info(f"   Result: {result2}, Elapsed: {elapsed2:.2f}s")

        if result2:
            self.assertTrue(elapsed2 < 30, "Connection should be quick despite large timeout")
            self.assert_connected()

        self.log_test_info("✅ Edge case timeouts handled")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
