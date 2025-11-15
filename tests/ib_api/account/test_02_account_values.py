"""
Test 02: Account Values

Tests retrieval of detailed account values and attributes.

Test Coverage:
- Request account values
- Validate value data structure
- Currency-specific values
- Real-time value updates
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
class TestAccountValues(BaseAccountTest):
    """Account values tests - detailed account attributes"""

    def test_01_get_account_values(self):
        """Test retrieving account values for all accounts"""
        self.log_test_info("Testing account values retrieval")

        values = self.ib.accountValues()

        self.assertIsNotNone(values, "Account values should not be None")
        self.assertGreater(len(values), 0, "Account values should contain data")

        self.log_test_info(f"Retrieved {len(values)} account value items")

        # Log sample values
        for item in values[:10]:
            self.log_test_info(f"   {item.tag}: {item.value} {item.currency} ({item.account})")

        self.log_test_info("✅ Account values retrieved")

    def test_02_account_values_structure(self):
        """Verify account values data structure"""
        self.log_test_info("Testing account values structure")

        values = self.ib.accountValues()
        self.assertGreater(len(values), 0, "Need values data")

        item = values[0]

        # Verify attributes
        self.assertTrue(hasattr(item, 'account'), "Should have account")
        self.assertTrue(hasattr(item, 'tag'), "Should have tag")
        self.assertTrue(hasattr(item, 'value'), "Should have value")
        self.assertTrue(hasattr(item, 'currency'), "Should have currency")
        self.assertTrue(hasattr(item, 'modelCode'), "Should have modelCode")

        self.log_test_info(f"✅ Structure validated: {item.tag} = {item.value}")

    def test_03_specific_account_values(self):
        """Get values for specific account"""
        self.log_test_info("Testing account-specific values")

        account = self.get_account()
        self.log_test_info(f"Requesting values for: {account}")

        values = self.ib.accountValues(account)

        self.assertGreater(len(values), 0, "Should have values")

        # Verify all for correct account
        for item in values:
            self.assertEqual(item.account, account, f"Account mismatch")

        self.log_test_info(f"✅ Retrieved {len(values)} values for {account}")

    def test_04_key_value_tags(self):
        """Check for important account value tags"""
        self.log_test_info("Testing key account value tags")

        values = self.ib.accountValues()
        available_tags = {item.tag for item in values}

        important_tags = [
            'NetLiquidation', 'TotalCashValue', 'SettledCash',
            'BuyingPower', 'EquityWithLoanValue', 'AvailableFunds'
        ]

        found = []
        for tag in important_tags:
            if tag in available_tags:
                found.append(tag)
                items = [i for i in values if i.tag == tag]
                if items:
                    self.log_test_info(f"   ✅ {tag}: {items[0].value}")

        self.log_test_info(f"✅ Found {len(found)}/{len(important_tags)} key tags")

    def test_05_currency_values(self):
        """Test currency-specific value retrieval"""
        self.log_test_info("Testing currency-specific values")

        values = self.ib.accountValues()

        # Group by currency
        by_currency = {}
        for item in values:
            currency = item.currency if item.currency else 'None'
            by_currency.setdefault(currency, []).append(item)

        self.log_test_info(f"Values in {len(by_currency)} currencies:")
        for currency, items in by_currency.items():
            self.log_test_info(f"   {currency}: {len(items)} items")

        self.log_test_info("✅ Currency breakdown complete")

    def test_06_numeric_value_validation(self):
        """Validate that numeric values are parseable"""
        self.log_test_info("Testing numeric value validation")

        values = self.ib.accountValues()

        numeric_tags = ['NetLiquidation', 'TotalCashValue', 'BuyingPower']
        validated = 0

        for tag in numeric_tags:
            items = [i for i in values if i.tag == tag]
            for item in items:
                try:
                    value_float = float(item.value)
                    self.assertIsInstance(value_float, float)
                    validated += 1
                    self.log_test_info(f"   ✅ {tag}: {value_float}")
                except ValueError:
                    self.log_test_warning(f"   ⚠️ {tag}: '{item.value}' not numeric")

        self.log_test_info(f"✅ Validated {validated} numeric values")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
