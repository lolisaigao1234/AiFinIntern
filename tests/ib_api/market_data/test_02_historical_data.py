"""Test 02: Historical Data - Bars, candles, and historical price data"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from base_test import BaseMarketDataTest
from helpers.contracts import ContractHelpers
from config.test_config import TestConfig
from config.logging_config import setup_logging, get_logger

setup_logging(verbose=TestConfig.VERBOSE_LOGGING)
logger = get_logger(__name__)


@pytest.mark.market_data
@pytest.mark.safe
class TestHistoricalData(BaseMarketDataTest):
    """Historical data tests"""

    def test_01_request_historical_bars(self):
        """Test historical data request"""
        self.log_test_info("Testing historical data request")

        contract = ContractHelpers.us_stock_spy()
        bars = self.ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='1 D',
            barSizeSetting='1 hour',
            whatToShow='TRADES',
            useRTH=True
        )

        self.assertIsNotNone(bars, "Bars should not be None")
        self.assertGreater(len(bars), 0, "Should have bars")

        self.log_test_info(f"Retrieved {len(bars)} bars")
        if len(bars) > 0:
            bar = bars[0]
            self.log_test_info(f"   First bar: O={bar.open} H={bar.high} L={bar.low} C={bar.close}")

        self.log_test_info("✅ Historical data retrieved")

    def test_02_different_bar_sizes(self):
        """Test various bar sizes"""
        self.log_test_info("Testing different bar sizes")

        contract = ContractHelpers.us_stock_aapl()
        bar_sizes = ['1 min', '5 mins', '1 hour']

        for bar_size in bar_sizes:
            self.log_test_info(f"Testing {bar_size} bars")
            bars = self.ib.reqHistoricalData(contract, '', '1 D', bar_size, 'TRADES', True)
            self.assertGreater(len(bars), 0, f"Should have {bar_size} bars")
            self.log_test_info(f"   {bar_size}: {len(bars)} bars")

        self.log_test_info("✅ All bar sizes retrieved")

    def test_03_bar_structure(self):
        """Verify historical bar structure"""
        self.log_test_info("Testing bar structure")

        contract = ContractHelpers.us_stock_spy()
        bars = self.ib.reqHistoricalData(contract, '', '1 D', '1 hour', 'TRADES', True)

        self.assertGreater(len(bars), 0, "Need bars")
        bar = bars[0]

        self.assertTrue(hasattr(bar, 'date'), "Should have date")
        self.assertTrue(hasattr(bar, 'open'), "Should have open")
        self.assertTrue(hasattr(bar, 'high'), "Should have high")
        self.assertTrue(hasattr(bar, 'low'), "Should have low")
        self.assertTrue(hasattr(bar, 'close'), "Should have close")
        self.assertTrue(hasattr(bar, 'volume'), "Should have volume")

        self.log_test_info("✅ Bar structure validated")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
