"""
Test Fixtures and Data for IB API Tests

Provides reusable test data, mock objects, and fixtures for testing.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from ib_insync import Stock, Option, Future, Forex, Order, Trade, Fill, AccountValue


class TestFixtures:
    """
    Collection of test fixtures and sample data for IB API testing.
    """

    # ===================================
    # Sample Contracts
    # ===================================

    @staticmethod
    def get_sample_stocks() -> List[Stock]:
        """Get list of sample stock contracts for testing"""
        return [
            Stock('AAPL', 'SMART', 'USD'),
            Stock('MSFT', 'SMART', 'USD'),
            Stock('SPY', 'ARCA', 'USD'),
            Stock('TSLA', 'SMART', 'USD'),
            Stock('IBKR', 'SMART', 'USD'),
        ]

    @staticmethod
    def get_sample_forex_pairs() -> List[Forex]:
        """Get list of sample forex pairs for testing"""
        return [
            Forex('EUR', currency='USD'),
            Forex('GBP', currency='USD'),
            Forex('USD', currency='JPY'),
            Forex('AUD', currency='USD'),
        ]

    @staticmethod
    def get_sample_futures() -> List[Future]:
        """Get list of sample futures contracts for testing"""
        # Use approximate next quarterly expiry
        next_quarter = TestFixtures._get_next_quarter_expiry()
        return [
            Future('ES', lastTradeDateOrContractMonth=next_quarter, exchange='CME', currency='USD'),
            Future('NQ', lastTradeDateOrContractMonth=next_quarter, exchange='CME', currency='USD'),
            Future('YM', lastTradeDateOrContractMonth=next_quarter, exchange='CBOT', currency='USD'),
        ]

    @staticmethod
    def get_sample_options() -> List[Option]:
        """Get list of sample option contracts for testing"""
        # Use approximate next monthly expiry
        next_month = TestFixtures._get_next_month_expiry()
        return [
            Option('AAPL', lastTradeDateOrContractMonth=next_month, strike=150, right='C', exchange='SMART'),
            Option('AAPL', lastTradeDateOrContractMonth=next_month, strike=150, right='P', exchange='SMART'),
            Option('SPY', lastTradeDateOrContractMonth=next_month, strike=450, right='C', exchange='SMART'),
        ]

    # ===================================
    # Sample Orders
    # ===================================

    @staticmethod
    def get_sample_market_order(action: str = 'BUY', quantity: float = 100) -> Order:
        """Get sample market order"""
        order = Order()
        order.action = action
        order.orderType = 'MKT'
        order.totalQuantity = quantity
        return order

    @staticmethod
    def get_sample_limit_order(
        action: str = 'BUY',
        quantity: float = 100,
        limit_price: float = 150.0
    ) -> Order:
        """Get sample limit order"""
        order = Order()
        order.action = action
        order.orderType = 'LMT'
        order.totalQuantity = quantity
        order.lmtPrice = limit_price
        return order

    @staticmethod
    def get_sample_stop_order(
        action: str = 'SELL',
        quantity: float = 100,
        stop_price: float = 145.0
    ) -> Order:
        """Get sample stop order"""
        order = Order()
        order.action = action
        order.orderType = 'STP'
        order.totalQuantity = quantity
        order.auxPrice = stop_price
        return order

    # ===================================
    # Sample Account Data
    # ===================================

    @staticmethod
    def get_sample_account_values() -> List[Dict[str, Any]]:
        """Get sample account value data"""
        return [
            {
                'account': 'DU123456',
                'tag': 'NetLiquidation',
                'value': '100000.00',
                'currency': 'USD',
                'modelCode': ''
            },
            {
                'account': 'DU123456',
                'tag': 'TotalCashValue',
                'value': '50000.00',
                'currency': 'USD',
                'modelCode': ''
            },
            {
                'account': 'DU123456',
                'tag': 'BuyingPower',
                'value': '200000.00',
                'currency': 'USD',
                'modelCode': ''
            },
            {
                'account': 'DU123456',
                'tag': 'GrossPositionValue',
                'value': '50000.00',
                'currency': 'USD',
                'modelCode': ''
            },
        ]

    @staticmethod
    def get_sample_positions() -> List[Dict[str, Any]]:
        """Get sample position data"""
        return [
            {
                'account': 'DU123456',
                'contract': Stock('AAPL', 'SMART', 'USD'),
                'position': 100.0,
                'avgCost': 150.00,
                'marketValue': 15500.00,
                'marketPrice': 155.00,
                'unrealizedPNL': 500.00,
                'realizedPNL': 0.00
            },
            {
                'account': 'DU123456',
                'contract': Stock('MSFT', 'SMART', 'USD'),
                'position': 50.0,
                'avgCost': 300.00,
                'marketValue': 15750.00,
                'marketPrice': 315.00,
                'unrealizedPNL': 750.00,
                'realizedPNL': 0.00
            },
        ]

    # ===================================
    # Sample Market Data
    # ===================================

    @staticmethod
    def get_sample_tick_data() -> Dict[str, Any]:
        """Get sample tick (market) data"""
        return {
            'symbol': 'AAPL',
            'bid': 149.95,
            'ask': 150.05,
            'last': 150.00,
            'bidSize': 100,
            'askSize': 200,
            'lastSize': 50,
            'volume': 1000000,
            'high': 151.50,
            'low': 148.50,
            'close': 149.00,
            'timestamp': datetime.now()
        }

    @staticmethod
    def get_sample_historical_bars() -> List[Dict[str, Any]]:
        """Get sample historical bar data"""
        bars = []
        base_date = datetime.now() - timedelta(days=5)

        for i in range(5):
            bar_date = base_date + timedelta(days=i)
            bars.append({
                'date': bar_date,
                'open': 150.0 + i,
                'high': 152.0 + i,
                'low': 149.0 + i,
                'close': 151.0 + i,
                'volume': 1000000 + (i * 100000),
                'barCount': 100,
                'average': 150.5 + i
            })

        return bars

    # ===================================
    # Sample Error Data
    # ===================================

    @staticmethod
    def get_sample_errors() -> List[Dict[str, Any]]:
        """Get sample error data"""
        return [
            {
                'reqId': 1,
                'errorCode': 2104,
                'errorString': 'Market data farm connection is OK:usfarm',
                'advancedOrderRejectJson': ''
            },
            {
                'reqId': 2,
                'errorCode': 2106,
                'errorString': 'HMDS data farm connection is OK:ushmds',
                'advancedOrderRejectJson': ''
            },
            {
                'reqId': -1,
                'errorCode': 502,
                'errorString': "Couldn't connect to TWS. Confirm that 'Enable ActiveX and Socket Clients' is enabled on the TWS 'Edit->Global Configuration...->API->Settings' menu.",
                'advancedOrderRejectJson': ''
            },
        ]

    # ===================================
    # Sample Order Status Data
    # ===================================

    @staticmethod
    def get_sample_order_statuses() -> List[str]:
        """Get list of possible order statuses"""
        return [
            'PendingSubmit',
            'PendingCancel',
            'PreSubmitted',
            'Submitted',
            'ApiCancelled',
            'Cancelled',
            'Filled',
            'Inactive',
        ]

    @staticmethod
    def get_sample_filled_order() -> Dict[str, Any]:
        """Get sample filled order data"""
        return {
            'orderId': 1,
            'status': 'Filled',
            'filled': 100.0,
            'remaining': 0.0,
            'avgFillPrice': 150.25,
            'permId': 123456789,
            'parentId': 0,
            'lastFillPrice': 150.25,
            'clientId': 1,
            'whyHeld': '',
            'mktCapPrice': 0.0
        }

    # ===================================
    # Sample Execution/Fill Data
    # ===================================

    @staticmethod
    def get_sample_execution() -> Dict[str, Any]:
        """Get sample execution data"""
        return {
            'execId': 'EX001',
            'time': datetime.now().strftime('%Y%m%d %H:%M:%S'),
            'acctNumber': 'DU123456',
            'exchange': 'SMART',
            'side': 'BOT',  # Bought
            'shares': 100.0,
            'price': 150.25,
            'permId': 123456789,
            'clientId': 1,
            'orderId': 1,
            'liquidation': 0,
            'cumQty': 100.0,
            'avgPrice': 150.25,
        }

    @staticmethod
    def get_sample_commission() -> Dict[str, Any]:
        """Get sample commission report data"""
        return {
            'execId': 'EX001',
            'commission': 1.00,
            'currency': 'USD',
            'realizedPNL': 0.0,
            'yield_': 0.0,
            'yieldRedemptionDate': 0,
        }

    # ===================================
    # Helper Methods
    # ===================================

    @staticmethod
    def _get_next_quarter_expiry() -> str:
        """Get next quarterly expiry (YYYYMM format)"""
        now = datetime.now()
        year = now.year
        month = now.month

        # Quarterly months: Mar(3), Jun(6), Sep(9), Dec(12)
        if month < 3:
            return f"{year}03"
        elif month < 6:
            return f"{year}06"
        elif month < 9:
            return f"{year}09"
        elif month < 12:
            return f"{year}12"
        else:
            return f"{year + 1}03"

    @staticmethod
    def _get_next_month_expiry() -> str:
        """Get next month expiry (YYYYMMDD format, 3rd Friday)"""
        now = datetime.now()
        next_month = now + timedelta(days=30)

        # Find 3rd Friday of next month (approximate)
        year = next_month.year
        month = next_month.month

        # Find first Friday
        first_day = datetime(year, month, 1)
        first_friday = first_day + timedelta(days=(4 - first_day.weekday()) % 7)

        # 3rd Friday is 2 weeks after first Friday
        third_friday = first_friday + timedelta(weeks=2)

        return third_friday.strftime('%Y%m%d')

    # ===================================
    # Test Scenario Builders
    # ===================================

    @staticmethod
    def build_simple_trade_scenario() -> Dict[str, Any]:
        """Build a complete trade scenario for testing"""
        return {
            'contract': Stock('AAPL', 'SMART', 'USD'),
            'entry_order': TestFixtures.get_sample_market_order('BUY', 100),
            'exit_order': TestFixtures.get_sample_market_order('SELL', 100),
            'expected_entry_price': 150.00,
            'expected_exit_price': 155.00,
            'expected_pnl': 500.00,
            'expected_commission': 2.00,
        }

    @staticmethod
    def build_bracket_order_scenario() -> Dict[str, Any]:
        """Build a bracket order scenario for testing"""
        return {
            'contract': Stock('SPY', 'SMART', 'USD'),
            'entry_price': 450.00,
            'take_profit_price': 455.00,
            'stop_loss_price': 447.00,
            'quantity': 100,
            'expected_risk': 300.00,  # (450 - 447) * 100
            'expected_reward': 500.00,  # (455 - 450) * 100
            'risk_reward_ratio': 1.67,  # 500 / 300
        }


# Create fixtures instance for easy import
fixtures = TestFixtures()
