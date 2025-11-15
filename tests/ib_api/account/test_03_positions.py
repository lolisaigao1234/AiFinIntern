"""
Test 03: Account Positions

Tests retrieval and validation of account positions.

Test Coverage:
- Request positions
- Position data structure
- Empty positions handling
- Position attributes validation
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
class TestPositions(BaseAccountTest):
    """Account positions tests"""

    def test_01_get_positions(self):
        """Test retrieving all positions"""
        self.log_test_info("Testing positions retrieval")

        positions = self.ib.positions()

        self.assertIsNotNone(positions, "Positions should not be None")
        self.assertIsInstance(positions, list, "Positions should be list")

        self.log_test_info(f"Retrieved {len(positions)} positions")

        if len(positions) > 0:
            for i, pos in enumerate(positions[:5]):
                self.log_test_info(f"   Position {i + 1}: {pos.contract.symbol} x{pos.position}")

        self.log_test_info("✅ Positions retrieved")

    def test_02_positions_structure(self):
        """Verify position data structure"""
        self.log_test_info("Testing position structure")

        positions = self.ib.positions()

        if len(positions) == 0:
            self.log_test_info("No positions to validate, skipping")
            return

        pos = positions[0]

        # Verify attributes
        self.assertTrue(hasattr(pos, 'account'), "Should have account")
        self.assertTrue(hasattr(pos, 'contract'), "Should have contract")
        self.assertTrue(hasattr(pos, 'position'), "Should have position size")
        self.assertTrue(hasattr(pos, 'avgCost'), "Should have avgCost")

        self.log_test_info(f"✅ Structure validated")
        self.log_test_info(f"   Account: {pos.account}")
        self.log_test_info(f"   Contract: {pos.contract.symbol}")
        self.log_test_info(f"   Position: {pos.position}")
        self.log_test_info(f"   Avg Cost: {pos.avgCost}")

    def test_03_empty_positions(self):
        """Handle empty positions gracefully"""
        self.log_test_info("Testing empty positions handling")

        positions = self.ib.positions()

        # Should return empty list, not None
        self.assertIsInstance(positions, list, "Should be list even if empty")

        if len(positions) == 0:
            self.log_test_info("✅ No positions (expected for new account)")
        else:
            self.log_test_info(f"Account has {len(positions)} positions")

    def test_04_specific_account_positions(self):
        """Get positions for specific account"""
        self.log_test_info("Testing account-specific positions")

        account = self.get_account()
        positions = self.ib.positions(account)

        self.assertIsInstance(positions, list, "Should be list")

        if len(positions) > 0:
            for pos in positions:
                self.assertEqual(pos.account, account, "Account should match")

        self.log_test_info(f"✅ Retrieved {len(positions)} positions for {account}")

    def test_05_position_validation(self):
        """Validate position numeric values"""
        self.log_test_info("Testing position value validation")

        positions = self.ib.positions()

        if len(positions) == 0:
            self.log_test_info("No positions to validate")
            return

        for pos in positions:
            # Position should be numeric
            self.assertIsInstance(pos.position, (int, float), "Position should be numeric")

            # Position should be non-zero
            self.assertNotEqual(pos.position, 0, "Position should not be zero")

            # Average cost should be numeric
            self.assertIsInstance(pos.avgCost, (int, float), "AvgCost should be numeric")

            self.log_test_info(f"   ✅ {pos.contract.symbol}: {pos.position} @ {pos.avgCost}")

        self.log_test_info(f"✅ Validated {len(positions)} positions")

    def test_06_portfolio_items(self):
        """Test portfolio items (detailed position info)"""
        self.log_test_info("Testing portfolio items retrieval")

        account = self.get_account()
        portfolio = self.ib.portfolio(account)

        self.assertIsInstance(portfolio, list, "Portfolio should be list")
        self.log_test_info(f"Portfolio has {len(portfolio)} items")

        if len(portfolio) > 0:
            item = portfolio[0]

            # Check additional portfolio attributes
            self.assertTrue(hasattr(item, 'marketPrice'), "Should have marketPrice")
            self.assertTrue(hasattr(item, 'marketValue'), "Should have marketValue")
            self.assertTrue(hasattr(item, 'unrealizedPNL'), "Should have unrealizedPNL")
            self.assertTrue(hasattr(item, 'realizedPNL'), "Should have realizedPNL")

            self.log_test_info(f"   Symbol: {item.contract.symbol}")
            self.log_test_info(f"   Market Price: {item.marketPrice}")
            self.log_test_info(f"   Market Value: {item.marketValue}")
            self.log_test_info(f"   Unrealized P&L: {item.unrealizedPNL}")

        self.log_test_info("✅ Portfolio items validated")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
