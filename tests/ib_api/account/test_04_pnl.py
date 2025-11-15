"""
Test 04: Profit & Loss (P&L)

Tests P&L retrieval and real-time P&L updates.

Test Coverage:
- Request P&L data
- Single P&L subscriptions
- P&L data structure
- Real-time P&L updates
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from base_test import BaseAccountTest
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.account
@pytest.mark.safe
@pytest.mark.fast
class TestPnL(BaseAccountTest):
    """Profit & Loss tests"""

    def test_01_request_pnl(self):
        """Test requesting P&L for account"""
        self.log_test_info("Testing P&L request")

        account = self.get_account()
        self.log_test_info(f"Requesting P&L for account: {account}")

        # Request P&L
        pnl = self.ib.reqPnL(account)

        self.assertIsNotNone(pnl, "P&L object should not be None")

        # Wait brief moment for data
        self.ib.sleep(1)

        self.log_test_info(f"P&L Daily: {pnl.dailyPnL}")
        self.log_test_info(f"P&L Unrealized: {pnl.unrealizedPnL}")
        self.log_test_info(f"P&L Realized: {pnl.realizedPnL}")

        # Cancel P&L subscription
        self.ib.cancelPnL(account)

        self.log_test_info("✅ P&L request successful")

    def test_02_pnl_structure(self):
        """Verify P&L data structure"""
        self.log_test_info("Testing P&L structure")

        account = self.get_account()
        pnl = self.ib.reqPnL(account)

        # Wait for data
        self.ib.sleep(1)

        # Verify attributes
        self.assertTrue(hasattr(pnl, 'account'), "Should have account")
        self.assertTrue(hasattr(pnl, 'dailyPnL'), "Should have dailyPnL")
        self.assertTrue(hasattr(pnl, 'unrealizedPnL'), "Should have unrealizedPnL")
        self.assertTrue(hasattr(pnl, 'realizedPnL'), "Should have realizedPnL")

        self.assertEqual(pnl.account, account, "Account should match")

        # Cancel
        self.ib.cancelPnL(account)

        self.log_test_info("✅ P&L structure validated")

    def test_03_pnl_numeric_values(self):
        """Validate P&L numeric values"""
        self.log_test_info("Testing P&L numeric validation")

        account = self.get_account()
        pnl = self.ib.reqPnL(account)

        # Wait for data
        self.ib.sleep(1)

        # Check if values are numeric or None
        if pnl.dailyPnL is not None:
            self.assertIsInstance(pnl.dailyPnL, (int, float), "dailyPnL should be numeric")
            self.log_test_info(f"   Daily P&L: {pnl.dailyPnL}")

        if pnl.unrealizedPnL is not None:
            self.assertIsInstance(pnl.unrealizedPnL, (int, float), "unrealizedPnL should be numeric")
            self.log_test_info(f"   Unrealized P&L: {pnl.unrealizedPnL}")

        if pnl.realizedPnL is not None:
            self.assertIsInstance(pnl.realizedPnL, (int, float), "realizedPnL should be numeric")
            self.log_test_info(f"   Realized P&L: {pnl.realizedPnL}")

        # Cancel
        self.ib.cancelPnL(account)

        self.log_test_info("✅ P&L values validated")

    def test_04_single_pnl(self):
        """Test single position P&L"""
        self.log_test_info("Testing single position P&L")

        account = self.get_account()

        # Get positions
        positions = self.ib.positions(account)

        if len(positions) == 0:
            self.log_test_info("No positions for single P&L test, skipping")
            return

        # Get first position
        pos = positions[0]
        contract = pos.contract

        self.log_test_info(f"Requesting single P&L for {contract.symbol}")

        # Request single P&L
        pnl_single = self.ib.reqPnLSingle(account, '', contract.conId)

        # Wait for data
        self.ib.sleep(1)

        self.assertIsNotNone(pnl_single, "Single P&L should not be None")

        self.log_test_info(f"   Position: {pnl_single.position}")
        self.log_test_info(f"   Daily P&L: {pnl_single.dailyPnL}")
        self.log_test_info(f"   Unrealized P&L: {pnl_single.unrealizedPnL}")
        self.log_test_info(f"   Realized P&L: {pnl_single.realizedPnL}")
        self.log_test_info(f"   Value: {pnl_single.value}")

        # Cancel
        self.ib.cancelPnLSingle(account, '', contract.conId)

        self.log_test_info("✅ Single P&L retrieved")

    def test_05_pnl_updates(self):
        """Test P&L real-time updates"""
        self.log_test_info("Testing P&L real-time updates")

        account = self.get_account()
        pnl = self.ib.reqPnL(account)

        # Collect updates
        updates = []

        def on_update(pnl_obj):
            updates.append({
                'daily': pnl_obj.dailyPnL,
                'unrealized': pnl_obj.unrealizedPnL,
                'realized': pnl_obj.realizedPnL
            })

        pnl.updateEvent += on_update

        # Wait for potential updates
        self.ib.sleep(3)

        self.log_test_info(f"Received {len(updates)} P&L updates")

        if len(updates) > 0:
            self.log_test_info(f"   Last update: {updates[-1]}")

        # Cancel
        self.ib.cancelPnL(account)

        self.log_test_info("✅ P&L updates monitored")

    def test_06_multiple_pnl_subscriptions(self):
        """Test multiple P&L subscriptions"""
        self.log_test_info("Testing multiple P&L subscriptions")

        accounts = self.ib.managedAccounts()

        pnl_objects = []

        # Subscribe to P&L for all accounts
        for account in accounts:
            self.log_test_info(f"Subscribing to P&L for {account}")
            pnl = self.ib.reqPnL(account)
            pnl_objects.append((account, pnl))

        # Wait for data
        self.ib.sleep(2)

        # Check all subscriptions
        for account, pnl in pnl_objects:
            self.assertIsNotNone(pnl, f"P&L for {account} should not be None")
            self.log_test_info(f"   {account}: Daily P&L = {pnl.dailyPnL}")

        # Cancel all
        for account, _ in pnl_objects:
            self.ib.cancelPnL(account)

        self.log_test_info(f"✅ Managed {len(pnl_objects)} P&L subscriptions")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
