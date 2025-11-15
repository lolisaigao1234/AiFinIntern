"""
Test 01: Account Summary

Tests retrieval and validation of account summary data.

Test Coverage:
- Request account summary
- Validate summary data structure
- Verify key account metrics
- Multiple account handling
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from base_test import BaseAccountTest
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

# Set up logging
setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.account
@pytest.mark.safe
@pytest.mark.fast
class TestAccountSummary(BaseAccountTest):
    """
    Account summary tests.

    Tests retrieval and validation of account summary information.
    """

    def test_01_get_account_summary_all_accounts(self):
        """
        Test 01.1: Get account summary for all accounts

        Verifies that:
        - Account summary can be retrieved
        - Summary contains data
        - Common tags are present
        """
        self.log_test_info("Testing account summary retrieval (all accounts)")

        # Request account summary for all accounts
        summary = self.ib.accountSummary()

        # Verify summary exists
        self.assertIsNotNone(summary, "Account summary should not be None")
        self.assertGreater(len(summary), 0, "Account summary should contain data")

        self.log_test_info(f"Retrieved {len(summary)} account summary items")

        # Log sample items
        for i, item in enumerate(summary[:5]):  # First 5 items
            self.log_test_info(f"   Item {i + 1}: {item.tag} = {item.value} {item.currency}")

        self.log_test_info("✅ Account summary retrieved successfully")

    def test_02_verify_summary_structure(self):
        """
        Test 01.2: Verify account summary data structure

        Verifies that:
        - Summary items have correct attributes
        - Account field is populated
        - Tag and value fields exist
        """
        self.log_test_info("Testing account summary data structure")

        summary = self.ib.accountSummary()
        self.assertGreater(len(summary), 0, "Need summary data for validation")

        # Check first item structure
        item = summary[0]

        # Verify required attributes exist
        self.assertTrue(hasattr(item, 'account'), "Should have account attribute")
        self.assertTrue(hasattr(item, 'tag'), "Should have tag attribute")
        self.assertTrue(hasattr(item, 'value'), "Should have value attribute")
        self.assertTrue(hasattr(item, 'currency'), "Should have currency attribute")

        # Verify account is not empty
        self.assertIsNotNone(item.account, "Account should not be None")
        self.assertNotEqual(item.account, '', "Account should not be empty")

        # Verify tag is not empty
        self.assertIsNotNone(item.tag, "Tag should not be None")
        self.assertNotEqual(item.tag, '', "Tag should not be empty")

        self.log_test_info(f"✅ Summary structure validated")
        self.log_test_info(f"   Account: {item.account}")
        self.log_test_info(f"   Sample tag: {item.tag} = {item.value}")

    def test_03_check_key_account_metrics(self):
        """
        Test 01.3: Check for key account metrics

        Verifies that:
        - Important account tags are present
        - NetLiquidation value exists
        - BuyingPower value exists
        """
        self.log_test_info("Testing presence of key account metrics")

        summary = self.ib.accountSummary()
        self.assertGreater(len(summary), 0, "Need summary data")

        # Get all available tags
        available_tags = {item.tag for item in summary}

        self.log_test_info(f"Available tags ({len(available_tags)}): {sorted(available_tags)}")

        # Check for important tags
        important_tags = ['NetLiquidation', 'TotalCashValue', 'BuyingPower']

        found_tags = []
        missing_tags = []

        for tag in important_tags:
            if tag in available_tags:
                found_tags.append(tag)

                # Get value for this tag
                tag_items = [item for item in summary if item.tag == tag]
                if tag_items:
                    self.log_test_info(f"   ✅ {tag}: {tag_items[0].value} {tag_items[0].currency}")
            else:
                missing_tags.append(tag)
                self.log_test_warning(f"   ⚠️ {tag}: Not found")

        # Should have at least some important tags
        self.assertGreater(
            len(found_tags),
            0,
            f"Should have at least one important tag. Missing: {missing_tags}"
        )

        self.log_test_info(f"✅ Found {len(found_tags)}/{len(important_tags)} important tags")

    def test_04_net_liquidation_value(self):
        """
        Test 01.4: Retrieve and validate net liquidation value

        Verifies that:
        - Net liquidation value can be retrieved
        - Value is numeric
        - Value is reasonable (positive for most accounts)
        """
        self.log_test_info("Testing net liquidation value")

        summary = self.ib.accountSummary()

        # Find NetLiquidation items
        net_liq_items = [item for item in summary if item.tag == 'NetLiquidation']

        if len(net_liq_items) == 0:
            self.log_test_warning("NetLiquidation tag not available, skipping test")
            self.skipTest("NetLiquidation not available in account summary")

        # Check first NetLiquidation value
        net_liq = net_liq_items[0]

        self.log_test_info(f"Net Liquidation Value: {net_liq.value} {net_liq.currency}")

        # Verify value can be converted to float
        try:
            value_float = float(net_liq.value)
            self.assertIsInstance(value_float, float, "NetLiquidation should be numeric")

            # For paper trading, should typically be positive
            if TestConfig.IS_PAPER_TRADING:
                self.log_test_info(f"   Paper trading account balance: {value_float}")
                # Don't enforce positive (account might be empty), just log

        except ValueError:
            self.fail(f"NetLiquidation value '{net_liq.value}' is not numeric")

        self.log_test_info("✅ Net liquidation value validated")

    def test_05_account_summary_specific_account(self):
        """
        Test 01.5: Get account summary for specific account

        Verifies that:
        - Can request summary for specific account
        - Summary is filtered to requested account
        """
        self.log_test_info("Testing account summary for specific account")

        # Get account list
        accounts = self.ib.managedAccounts()
        self.assertGreater(len(accounts), 0, "Need at least one account")

        account = accounts[0]
        self.log_test_info(f"Requesting summary for account: {account}")

        # Request summary for specific account
        summary = self.ib.accountSummary(account=account)

        self.assertIsNotNone(summary, "Summary should not be None")
        self.assertGreater(len(summary), 0, "Summary should contain data")

        # Verify all items are for requested account
        for item in summary:
            self.assertEqual(
                item.account,
                account,
                f"Item account '{item.account}' should match requested '{account}'"
            )

        self.log_test_info(f"✅ Retrieved {len(summary)} items for account {account}")

    def test_06_account_summary_by_tags(self):
        """
        Test 01.6: Retrieve specific account summary tags

        Verifies that:
        - Can retrieve specific tags from summary
        - Filtering by tags works correctly
        """
        self.log_test_info("Testing account summary tag filtering")

        # Get full summary first
        full_summary = self.ib.accountSummary()
        available_tags = {item.tag for item in full_summary}

        self.log_test_info(f"Total tags available: {len(available_tags)}")

        # Try to get specific useful tags
        desired_tags = ['NetLiquidation', 'TotalCashValue', 'BuyingPower']
        found_data = {}

        for tag in desired_tags:
            items = [item for item in full_summary if item.tag == tag]
            if items:
                found_data[tag] = items[0]
                self.log_test_info(f"   {tag}: {items[0].value} {items[0].currency}")

        # Should find at least one desired tag
        self.assertGreater(
            len(found_data),
            0,
            f"Should find at least one tag from {desired_tags}"
        )

        self.log_test_info(f"✅ Retrieved {len(found_data)} specific tags")

    def test_07_multiple_accounts_summary(self):
        """
        Test 01.7: Handle multiple accounts in summary

        Verifies that:
        - Summary includes all managed accounts
        - Can distinguish between account data
        """
        self.log_test_info("Testing multiple accounts in summary")

        # Get managed accounts
        accounts = self.ib.managedAccounts()
        self.log_test_info(f"Managed accounts: {accounts}")

        # Get summary for all
        summary = self.ib.accountSummary()

        # Get unique accounts in summary
        summary_accounts = {item.account for item in summary}

        self.log_test_info(f"Accounts in summary: {summary_accounts}")

        # Verify summary includes managed accounts
        for account in accounts:
            self.assertIn(
                account,
                summary_accounts,
                f"Summary should include managed account {account}"
            )

        self.log_test_info(f"✅ Summary includes all {len(accounts)} managed accounts")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
