"""
Test 01: Real-time Market Data Quotes

Tests real-time streaming market data (quotes, tickers).

Test Coverage:
- Request market data for stocks
- Streaming data updates
- Market data cancellation
- Data structure validation
"""

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
@pytest.mark.fast
class TestRealtimeQuotes(BaseMarketDataTest):
    """Real-time market data quote tests"""

    def test_01_request_market_data_stock(self):
        """Test requesting real-time market data for stock"""
        self.log_test_info("Testing market data request for stock")

        contract = ContractHelpers.us_stock_spy()
        self.log_test_info(f"Requesting market data for {contract.symbol}")

        ticker = self.ib.reqMktData(contract, '', False)
        self.assertIsNotNone(ticker, "Ticker should not be None")

        # Wait for data
        self.ib.sleep(2)

        self.log_test_info(f"   Bid: {ticker.bid}")
        self.log_test_info(f"   Ask: {ticker.ask}")
        self.log_test_info(f"   Last: {ticker.last}")

        # Cancel
        self.ib.cancelMktData(contract)

        self.log_test_info("✅ Market data retrieved")

    def test_02_ticker_structure(self):
        """Verify ticker data structure"""
        self.log_test_info("Testing ticker structure")

        contract = ContractHelpers.us_stock_aapl()
        ticker = self.ib.reqMktData(contract)

        self.ib.sleep(2)

        # Verify attributes
        self.assertTrue(hasattr(ticker, 'contract'), "Should have contract")
        self.assertTrue(hasattr(ticker, 'bid'), "Should have bid")
        self.assertTrue(hasattr(ticker, 'ask'), "Should have ask")
        self.assertTrue(hasattr(ticker, 'last'), "Should have last")
        self.assertTrue(hasattr(ticker, 'bidSize'), "Should have bidSize")
        self.assertTrue(hasattr(ticker, 'askSize'), "Should have askSize")

        self.ib.cancelMktData(contract)
        self.log_test_info("✅ Ticker structure validated")

    def test_03_multiple_contracts(self):
        """Request market data for multiple contracts"""
        self.log_test_info("Testing multiple market data requests")

        contracts = [
            ContractHelpers.us_stock_aapl(),
            ContractHelpers.us_stock_spy(),
            ContractHelpers.us_stock_tsla()
        ]

        tickers = []
        for contract in contracts:
            self.log_test_info(f"Requesting {contract.symbol}")
            ticker = self.ib.reqMktData(contract)
            tickers.append((contract, ticker))

        # Wait for data
        self.ib.sleep(3)

        # Check all tickers
        for contract, ticker in tickers:
            self.log_test_info(f"   {contract.symbol}: Bid={ticker.bid}, Ask={ticker.ask}")

        # Cancel all
        for contract, _ in tickers:
            self.ib.cancelMktData(contract)

        self.log_test_info(f"✅ Retrieved data for {len(tickers)} contracts")

    def test_04_realtime_updates(self):
        """Test real-time streaming updates"""
        self.log_test_info("Testing real-time updates")

        contract = ContractHelpers.us_stock_spy()
        ticker = self.ib.reqMktData(contract)

        updates = []

        def on_update(ticker):
            updates.append({'bid': ticker.bid, 'ask': ticker.ask, 'last': ticker.last})

        ticker.updateEvent += on_update

        # Wait for updates
        self.ib.sleep(5)

        self.log_test_info(f"Received {len(updates)} updates")

        if len(updates) > 0:
            self.log_test_info(f"   First: {updates[0]}")
            self.log_test_info(f"   Last: {updates[-1]}")

        self.ib.cancelMktData(contract)
        self.log_test_info("✅ Real-time updates monitored")

    def test_05_snapshot_data(self):
        """Test snapshot (non-streaming) market data"""
        self.log_test_info("Testing snapshot market data")

        contract = ContractHelpers.us_stock_aapl()
        ticker = self.ib.reqMktData(contract, snapshot=True)

        self.ib.sleep(2)

        self.log_test_info(f"   Bid: {ticker.bid}")
        self.log_test_info(f"   Ask: {ticker.ask}")

        # Snapshot should auto-cancel
        self.log_test_info("✅ Snapshot data retrieved")

    def test_06_cancel_market_data(self):
        """Test market data cancellation"""
        self.log_test_info("Testing market data cancellation")

        contract = ContractHelpers.us_stock_ibkr()
        ticker = self.ib.reqMktData(contract)

        self.ib.sleep(1)

        # Cancel
        self.log_test_info("Cancelling market data...")
        self.ib.cancelMktData(contract)

        # Should complete without errors
        self.log_test_info("✅ Market data cancelled")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
