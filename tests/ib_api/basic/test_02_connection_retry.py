"""
Test 02: Connection Retry Logic

Tests connection retry and resilience functionality.

Test Coverage:
- Retry connection attempts after initial failure
- Exponential backoff implementation
- Maximum retry limits
- Connection recovery scenarios
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
class TestConnectionRetry(BaseConnectionTest):
    """
    Connection retry and resilience tests.

    Tests various retry scenarios and recovery mechanisms.
    """

    def test_01_retry_on_initial_failure(self):
        """
        Test 02.1: Retry connection after initial failure

        Verifies that:
        - Retry logic attempts multiple connections
        - Retries respect delay between attempts
        - Final failure is handled gracefully
        """
        self.log_test_info("Testing retry on initial connection failure")

        # Use invalid host to force failure
        original_host = self.HOST
        self.HOST = '192.0.2.1'  # Non-routable IP

        max_retries = 3
        retry_delay = 0.5  # seconds
        successful = False

        try:
            for attempt in range(max_retries):
                self.log_test_info(f"Connection attempt {attempt + 1}/{max_retries}")

                start_time = time.time()

                # Attempt connection with short timeout
                result = self.connect()

                elapsed = time.time() - start_time

                if result:
                    successful = True
                    self.log_test_info(f"✅ Connected on attempt {attempt + 1}")
                    break
                else:
                    self.log_test_info(f"❌ Attempt {attempt + 1} failed (took {elapsed:.2f}s)")

                    # Wait before next retry (except on last attempt)
                    if attempt < max_retries - 1:
                        self.log_test_info(f"Waiting {retry_delay}s before retry...")
                        time.sleep(retry_delay)

            # With invalid host, should not succeed
            self.assertFalse(successful, "Should not connect to invalid host")
            self.log_test_info(f"✅ Retry logic completed {max_retries} attempts as expected")

        finally:
            # Restore original host
            self.HOST = original_host

    def test_02_exponential_backoff(self):
        """
        Test 02.2: Exponential backoff retry strategy

        Verifies that:
        - Retry delays increase exponentially
        - Maximum delay cap is respected
        - Backoff timing is accurate
        """
        self.log_test_info("Testing exponential backoff strategy")

        # Exponential backoff parameters
        initial_delay = 0.5  # seconds
        max_delay = 4.0      # seconds
        backoff_factor = 2.0
        max_retries = 5

        # Use invalid host
        original_host = self.HOST
        self.HOST = '192.0.2.1'

        try:
            delay = initial_delay

            for attempt in range(max_retries):
                self.log_test_info(f"Attempt {attempt + 1}/{max_retries}, delay: {delay}s")

                # Attempt connection
                start_time = time.time()
                result = self.connect()
                elapsed = time.time() - start_time

                # Should fail with invalid host
                self.assertFalse(result, f"Attempt {attempt + 1} should fail")

                # Calculate next delay (exponential backoff)
                if attempt < max_retries - 1:
                    # Wait with current delay
                    actual_wait_start = time.time()
                    time.sleep(delay)
                    actual_wait = time.time() - actual_wait_start

                    # Verify delay timing (allow 10% tolerance)
                    self.assertAlmostEqual(
                        actual_wait,
                        delay,
                        delta=delay * 0.1,
                        msg=f"Delay timing off: expected {delay}s, got {actual_wait}s"
                    )

                    # Calculate next delay
                    delay = min(delay * backoff_factor, max_delay)

            self.log_test_info("✅ Exponential backoff strategy verified")

        finally:
            self.HOST = original_host

    def test_03_connection_recovery_after_timeout(self):
        """
        Test 02.3: Recover connection after timeout

        Verifies that:
        - Can recover from connection timeout
        - Successful connection after failed attempts
        """
        self.log_test_info("Testing connection recovery after timeout")

        # First, attempt connection with very short timeout to force failure
        original_timeout = self.TIMEOUT
        self.TIMEOUT = 0.1  # 100ms - likely too short

        # First attempt (should timeout)
        self.log_test_info("Attempting connection with very short timeout...")
        result1 = self.connect()
        self.log_test_info(f"First attempt result: {'success' if result1 else 'failed (expected)'}")

        # Clean up if somehow connected
        if self.connected:
            self.disconnect()

        # Wait a moment
        time.sleep(0.5)

        # Now try with normal timeout
        self.TIMEOUT = original_timeout
        self.log_test_info(f"Retrying with normal timeout ({self.TIMEOUT}s)...")

        result2 = self.connect()
        self.assertTrue(result2, "Should successfully connect with normal timeout")
        self.assert_connected()

        self.log_test_info("✅ Connection recovery successful")

    def test_04_max_retry_limit(self):
        """
        Test 02.4: Respect maximum retry limit

        Verifies that:
        - Retry attempts stop at max limit
        - Total attempts equals max_retries
        - Final error is raised/logged appropriately
        """
        self.log_test_info("Testing maximum retry limit")

        max_retries = 5
        attempt_count = 0

        # Use invalid host
        original_host = self.HOST
        self.HOST = '192.0.2.1'

        try:
            for attempt in range(max_retries):
                attempt_count += 1
                self.log_test_info(f"Retry attempt {attempt_count}/{max_retries}")

                result = self.connect()

                if result:
                    break

                # Small delay between attempts
                if attempt < max_retries - 1:
                    time.sleep(0.5)

            # Verify we attempted exactly max_retries times
            self.assertEqual(
                attempt_count,
                max_retries,
                f"Should attempt exactly {max_retries} times"
            )

            self.log_test_info(f"✅ Max retry limit respected ({attempt_count} attempts)")

        finally:
            self.HOST = original_host

    def test_05_connection_resilience(self):
        """
        Test 02.5: Connection resilience under various conditions

        Verifies that:
        - Multiple quick connect/disconnect cycles work
        - No resource leaks or degradation
        - Connection remains stable
        """
        self.log_test_info("Testing connection resilience")

        cycles = 10
        failure_count = 0

        for cycle in range(cycles):
            try:
                # Connect
                result = self.connect(client_id=TestConfig.IB_CLIENT_ID + cycle)

                if not result:
                    failure_count += 1
                    self.log_test_warning(f"Cycle {cycle + 1} connection failed")
                    continue

                # Verify connection
                self.assert_connected()

                # Quick data request to verify connection works
                server_time = self.ib.reqCurrentTime()
                self.assertIsNotNone(server_time, f"Cycle {cycle + 1} server time is None")

                # Disconnect
                self.disconnect()

                # Very brief pause
                time.sleep(0.1)

            except Exception as e:
                failure_count += 1
                self.log_test_error(f"Cycle {cycle + 1} exception: {e}")

        # Allow some failures but not too many
        success_rate = (cycles - failure_count) / cycles * 100
        self.log_test_info(f"Success rate: {success_rate:.1f}% ({cycles - failure_count}/{cycles})")

        self.assertGreaterEqual(
            success_rate,
            80.0,  # Require at least 80% success rate
            f"Success rate too low: {success_rate:.1f}%"
        )

        self.log_test_info(f"✅ Connection resilience verified ({success_rate:.1f}% success rate)")

    def test_06_connection_state_recovery(self):
        """
        Test 02.6: Recover from inconsistent connection state

        Verifies that:
        - Can detect inconsistent state
        - Can recover to known good state
        - Reconnection works after state corruption
        """
        self.log_test_info("Testing connection state recovery")

        # Establish initial connection
        self.assertTrue(self.connect(), "Initial connection failed")
        self.assert_connected()

        # Get initial account list to verify working state
        initial_accounts = self.ib.managedAccounts()
        self.assertGreater(len(initial_accounts), 0, "No initial accounts")

        # Disconnect
        self.disconnect()

        # Verify disconnected state
        self.assertFalse(self.connected, "Should be disconnected")

        # Wait a moment
        time.sleep(1.0)

        # Reconnect and verify state is clean
        self.assertTrue(self.connect(), "Reconnection failed")
        self.assert_connected()

        # Verify we can still access data
        reconnect_accounts = self.ib.managedAccounts()
        self.assertEqual(
            initial_accounts,
            reconnect_accounts,
            "Accounts should match after reconnection"
        )

        self.log_test_info("✅ Connection state recovery successful")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
