"""
Test 03: Multiple Client Connections

Tests handling of multiple simultaneous client connections to IB Gateway/TWS.

Test Coverage:
- Multiple clients with different client IDs
- Concurrent connections
- Client isolation and independence
- Resource management with multiple clients
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from ib_insync import IB
from base_test import BaseConnectionTest
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

# Set up logging
setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.connection
@pytest.mark.fast
class TestMultipleClients(BaseConnectionTest):
    """
    Multiple client connection tests.

    Tests scenarios involving multiple simultaneous client connections.
    """

    def setUp(self):
        """Set up test with list to track multiple IB instances"""
        super().setUp()
        self.clients = []  # Track all client instances for cleanup

    def tearDown(self):
        """Clean up all client connections"""
        for client in self.clients:
            try:
                if client.isConnected():
                    client.disconnect()
            except Exception as e:
                self.log_test_warning(f"Error disconnecting client: {e}")

        self.clients.clear()
        super().tearDown()

    def test_01_two_clients_different_ids(self):
        """
        Test 03.1: Two clients with different client IDs

        Verifies that:
        - Two clients can connect simultaneously
        - Both clients have independent connections
        - Both clients can retrieve data independently
        """
        self.log_test_info("Testing two clients with different client IDs")

        # Create first client
        client1 = IB()
        self.clients.append(client1)

        # Create second client
        client2 = IB()
        self.clients.append(client2)

        # Connect first client
        self.log_test_info("Connecting client 1 (ID: 1)")
        client1.connect(self.HOST, self.PORT, clientId=1, timeout=self.TIMEOUT)
        self.assertTrue(client1.isConnected(), "Client 1 should be connected")

        # Connect second client
        self.log_test_info("Connecting client 2 (ID: 2)")
        client2.connect(self.HOST, self.PORT, clientId=2, timeout=self.TIMEOUT)
        self.assertTrue(client2.isConnected(), "Client 2 should be connected")

        # Verify both are connected
        self.assertTrue(client1.isConnected(), "Client 1 should remain connected")
        self.assertTrue(client2.isConnected(), "Client 2 should be connected")

        # Test independent data retrieval
        accounts1 = client1.managedAccounts()
        accounts2 = client2.managedAccounts()

        self.assertGreater(len(accounts1), 0, "Client 1 should have accounts")
        self.assertGreater(len(accounts2), 0, "Client 2 should have accounts")
        self.assertEqual(accounts1, accounts2, "Both clients should see same accounts")

        self.log_test_info(f"✅ Both clients connected successfully")
        self.log_test_info(f"   Client 1 accounts: {accounts1}")
        self.log_test_info(f"   Client 2 accounts: {accounts2}")

    def test_02_multiple_clients_sequential(self):
        """
        Test 03.2: Multiple clients connecting sequentially

        Verifies that:
        - Multiple clients can connect one after another
        - Each client maintains its own connection
        - No interference between clients
        """
        self.log_test_info("Testing sequential connection of 5 clients")

        num_clients = 5
        base_client_id = 10

        for i in range(num_clients):
            client_id = base_client_id + i
            self.log_test_info(f"Connecting client {i + 1}/{num_clients} (ID: {client_id})")

            client = IB()
            self.clients.append(client)

            # Connect
            client.connect(self.HOST, self.PORT, clientId=client_id, timeout=self.TIMEOUT)
            self.assertTrue(client.isConnected(), f"Client {i + 1} should be connected")

            # Verify can access data
            server_time = client.reqCurrentTime()
            self.assertIsNotNone(server_time, f"Client {i + 1} should get server time")

        # Verify all clients still connected
        for i, client in enumerate(self.clients):
            self.assertTrue(
                client.isConnected(),
                f"Client {i + 1} should still be connected"
            )

        self.log_test_info(f"✅ All {num_clients} clients connected successfully")

    def test_03_client_independence(self):
        """
        Test 03.3: Client independence and isolation

        Verifies that:
        - Disconnecting one client doesn't affect others
        - Each client has independent state
        """
        self.log_test_info("Testing client independence")

        # Create and connect 3 clients
        for i in range(3):
            client = IB()
            self.clients.append(client)
            client.connect(self.HOST, self.PORT, clientId=20 + i, timeout=self.TIMEOUT)
            self.assertTrue(client.isConnected(), f"Client {i + 1} should be connected")

        # Disconnect middle client
        self.log_test_info("Disconnecting client 2")
        self.clients[1].disconnect()
        self.assertFalse(self.clients[1].isConnected(), "Client 2 should be disconnected")

        # Verify other clients still connected
        self.assertTrue(self.clients[0].isConnected(), "Client 1 should remain connected")
        self.assertTrue(self.clients[2].isConnected(), "Client 3 should remain connected")

        # Verify other clients can still access data
        accounts1 = self.clients[0].managedAccounts()
        accounts3 = self.clients[2].managedAccounts()

        self.assertGreater(len(accounts1), 0, "Client 1 should still access accounts")
        self.assertGreater(len(accounts3), 0, "Client 3 should still access accounts")

        self.log_test_info("✅ Client independence verified")

    def test_04_reconnect_different_client_id(self):
        """
        Test 03.4: Reconnect with different client ID

        Verifies that:
        - Same IB instance can reconnect with different client ID
        - Previous client ID is released
        """
        self.log_test_info("Testing reconnection with different client ID")

        client = IB()
        self.clients.append(client)

        # Connect with client ID 30
        self.log_test_info("Connecting with client ID 30")
        client.connect(self.HOST, self.PORT, clientId=30, timeout=self.TIMEOUT)
        self.assertTrue(client.isConnected(), "Should be connected")

        accounts1 = client.managedAccounts()
        self.assertGreater(len(accounts1), 0, "Should have accounts")

        # Disconnect
        self.log_test_info("Disconnecting")
        client.disconnect()
        self.assertFalse(client.isConnected(), "Should be disconnected")

        # Small delay
        client.sleep(1)

        # Reconnect with different client ID
        self.log_test_info("Reconnecting with client ID 31")
        client.connect(self.HOST, self.PORT, clientId=31, timeout=self.TIMEOUT)
        self.assertTrue(client.isConnected(), "Should be reconnected")

        accounts2 = client.managedAccounts()
        self.assertEqual(accounts1, accounts2, "Should see same accounts")

        self.log_test_info("✅ Reconnection with different client ID successful")

    def test_05_max_concurrent_clients(self):
        """
        Test 03.5: Maximum concurrent clients

        Verifies that:
        - Multiple clients can be connected simultaneously
        - System handles reasonable number of concurrent connections
        - All clients remain functional
        """
        self.log_test_info("Testing maximum concurrent clients")

        max_clients = 10  # Test with 10 concurrent clients
        base_client_id = 40

        # Connect all clients
        for i in range(max_clients):
            client_id = base_client_id + i
            self.log_test_info(f"Connecting client {i + 1}/{max_clients} (ID: {client_id})")

            client = IB()
            self.clients.append(client)

            try:
                client.connect(self.HOST, self.PORT, clientId=client_id, timeout=self.TIMEOUT)

                if client.isConnected():
                    self.log_test_info(f"   ✅ Client {i + 1} connected")
                else:
                    self.log_test_warning(f"   ⚠️ Client {i + 1} failed to connect")

            except Exception as e:
                self.log_test_warning(f"   ⚠️ Client {i + 1} exception: {e}")

        # Count successful connections
        connected_count = sum(1 for c in self.clients if c.isConnected())

        self.log_test_info(f"Successfully connected: {connected_count}/{max_clients}")

        # Require at least 80% success rate
        success_rate = (connected_count / max_clients) * 100
        self.assertGreaterEqual(
            success_rate,
            80.0,
            f"Success rate too low: {success_rate:.1f}%"
        )

        # Verify all connected clients can access data
        working_clients = 0
        for i, client in enumerate(self.clients):
            if client.isConnected():
                try:
                    accounts = client.managedAccounts()
                    if len(accounts) > 0:
                        working_clients += 1
                except Exception as e:
                    self.log_test_warning(f"Client {i + 1} data access failed: {e}")

        working_rate = (working_clients / connected_count) * 100 if connected_count > 0 else 0
        self.log_test_info(f"Working clients: {working_clients}/{connected_count} ({working_rate:.1f}%)")

        self.assertGreaterEqual(
            working_rate,
            90.0,
            f"Too many connected clients unable to access data: {working_rate:.1f}%"
        )

        self.log_test_info(f"✅ Concurrent client test passed ({connected_count} clients)")

    def test_06_client_id_reuse(self):
        """
        Test 03.6: Reusing client IDs after disconnection

        Verifies that:
        - Client ID can be reused after disconnection
        - No conflicts with previously used IDs
        """
        self.log_test_info("Testing client ID reuse")

        client_id = 50

        # First client
        self.log_test_info(f"First connection with client ID {client_id}")
        client1 = IB()
        self.clients.append(client1)
        client1.connect(self.HOST, self.PORT, clientId=client_id, timeout=self.TIMEOUT)
        self.assertTrue(client1.isConnected(), "First client should connect")

        # Disconnect
        self.log_test_info("Disconnecting first client")
        client1.disconnect()
        self.assertFalse(client1.isConnected(), "First client should be disconnected")

        # Wait a moment for cleanup
        client1.sleep(1)

        # Second client with same ID
        self.log_test_info(f"Second connection with same client ID {client_id}")
        client2 = IB()
        self.clients.append(client2)
        client2.connect(self.HOST, self.PORT, clientId=client_id, timeout=self.TIMEOUT)
        self.assertTrue(client2.isConnected(), "Second client should connect with reused ID")

        # Verify can access data
        accounts = client2.managedAccounts()
        self.assertGreater(len(accounts), 0, "Should access accounts with reused ID")

        self.log_test_info("✅ Client ID reuse successful")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
