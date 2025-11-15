"""
IB API Wrapper Helper for Testing

Simplified wrapper around ib_insync for test scenarios.
Provides additional convenience methods and state tracking.
"""

import logging
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from ib_insync import IB, Contract, Order, Trade, Fill, PortfolioItem, AccountValue

logger = logging.getLogger(__name__)


class IBTestWrapper:
    """
    Wrapper around ib_insync.IB for testing purposes.

    Provides:
    - Simplified connection management
    - Event callback registration
    - State tracking for test verification
    - Error handling and logging
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        """
        Initialize IB test wrapper.

        Args:
            host: IB Gateway/TWS host (default: 127.0.0.1)
            port: IB Gateway/TWS port (default: 7497 for paper trading)
            client_id: Client ID for connection
        """
        self.host = host
        self.port = port
        self.client_id = client_id

        self.ib = IB()
        self.connected = False

        # Event tracking
        self.errors: List[Dict[str, Any]] = []
        self.order_statuses: List[Dict[str, Any]] = []
        self.executions: List[Fill] = []
        self.commissions: List[Dict[str, Any]] = []

        # Callbacks
        self._error_callbacks: List[Callable] = []
        self._order_status_callbacks: List[Callable] = []
        self._execution_callbacks: List[Callable] = []

    def connect(self, timeout: int = 10) -> bool:
        """
        Connect to IB Gateway/TWS.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            bool: True if connected successfully
        """
        try:
            self.ib.connect(
                host=self.host,
                port=self.port,
                clientId=self.client_id,
                timeout=timeout
            )
            self.connected = True

            # Register event handlers
            self._register_event_handlers()

            logger.info(f"Connected to IB at {self.host}:{self.port} (Client ID: {self.client_id})")
            return True

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from IB Gateway/TWS"""
        if self.connected:
            try:
                self.ib.disconnect()
                self.connected = False
                logger.info("Disconnected from IB")
            except Exception as e:
                logger.error(f"Disconnect error: {e}")
                raise

    def _register_event_handlers(self):
        """Register event handlers for tracking"""
        self.ib.errorEvent += self._on_error
        self.ib.orderStatusEvent += self._on_order_status
        self.ib.execDetailsEvent += self._on_execution
        self.ib.commissionReportEvent += self._on_commission

    def _on_error(self, reqId: int, errorCode: int, errorString: str, contract: Contract):
        """Handle error events"""
        error_info = {
            'timestamp': datetime.now(),
            'reqId': reqId,
            'errorCode': errorCode,
            'errorString': errorString,
            'contract': contract
        }
        self.errors.append(error_info)
        logger.warning(f"Error {errorCode}: {errorString} (ReqId: {reqId})")

        # Trigger callbacks
        for callback in self._error_callbacks:
            try:
                callback(error_info)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")

    def _on_order_status(self, trade: Trade):
        """Handle order status events"""
        status_info = {
            'timestamp': datetime.now(),
            'orderId': trade.order.orderId,
            'status': trade.orderStatus.status,
            'filled': trade.orderStatus.filled,
            'remaining': trade.orderStatus.remaining,
            'avgFillPrice': trade.orderStatus.avgFillPrice
        }
        self.order_statuses.append(status_info)
        logger.info(f"Order {trade.order.orderId} status: {trade.orderStatus.status}")

        # Trigger callbacks
        for callback in self._order_status_callbacks:
            try:
                callback(trade)
            except Exception as e:
                logger.error(f"Error in order status callback: {e}")

    def _on_execution(self, trade: Trade, fill: Fill):
        """Handle execution events"""
        self.executions.append(fill)
        logger.info(f"Execution: {fill.execution.shares} shares @ {fill.execution.price}")

        # Trigger callbacks
        for callback in self._execution_callbacks:
            try:
                callback(trade, fill)
            except Exception as e:
                logger.error(f"Error in execution callback: {e}")

    def _on_commission(self, trade: Trade, fill: Fill, report):
        """Handle commission report events"""
        commission_info = {
            'timestamp': datetime.now(),
            'execId': report.execId,
            'commission': report.commission,
            'currency': report.currency
        }
        self.commissions.append(commission_info)
        logger.info(f"Commission: {report.commission} {report.currency}")

    # Callback registration methods
    def on_error(self, callback: Callable):
        """Register error callback"""
        self._error_callbacks.append(callback)

    def on_order_status(self, callback: Callable):
        """Register order status callback"""
        self._order_status_callbacks.append(callback)

    def on_execution(self, callback: Callable):
        """Register execution callback"""
        self._execution_callbacks.append(callback)

    # Convenience methods
    def get_managed_accounts(self) -> List[str]:
        """Get list of managed accounts"""
        return self.ib.managedAccounts()

    def get_account_summary(self, account: str = '') -> List[AccountValue]:
        """
        Get account summary.

        Args:
            account: Account number (default: all accounts)

        Returns:
            List of AccountValue objects
        """
        return self.ib.accountSummary(account)

    def get_account_values(self, account: str = '') -> List[AccountValue]:
        """
        Get account values.

        Args:
            account: Account number (default: all accounts)

        Returns:
            List of AccountValue objects
        """
        return self.ib.accountValues(account)

    def get_positions(self, account: str = '') -> List[PortfolioItem]:
        """
        Get current positions.

        Args:
            account: Account number (default: all accounts)

        Returns:
            List of PortfolioItem objects
        """
        return self.ib.positions(account)

    def place_order(self, contract: Contract, order: Order) -> Trade:
        """
        Place an order.

        Args:
            contract: Contract to trade
            order: Order details

        Returns:
            Trade object
        """
        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Placed order: {order.action} {order.totalQuantity} {contract.symbol}")
        return trade

    def cancel_order(self, order: Order):
        """
        Cancel an order.

        Args:
            order: Order to cancel
        """
        self.ib.cancelOrder(order)
        logger.info(f"Cancelled order: {order.orderId}")

    def get_open_orders(self) -> List[Trade]:
        """Get all open orders"""
        return self.ib.openOrders()

    def get_trades(self) -> List[Trade]:
        """Get all trades"""
        return self.ib.trades()

    def req_market_data(self, contract: Contract, snapshot: bool = False):
        """
        Request market data for a contract.

        Args:
            contract: Contract to get data for
            snapshot: If True, request snapshot (not live streaming)

        Returns:
            Ticker object
        """
        return self.ib.reqMktData(contract, snapshot=snapshot)

    def cancel_market_data(self, contract: Contract):
        """
        Cancel market data subscription.

        Args:
            contract: Contract to cancel data for
        """
        self.ib.cancelMktData(contract)

    def req_historical_data(
        self,
        contract: Contract,
        end_datetime: str = '',
        duration: str = '1 D',
        bar_size: str = '1 hour',
        what_to_show: str = 'TRADES',
        use_rth: bool = True
    ):
        """
        Request historical data.

        Args:
            contract: Contract to get data for
            end_datetime: End date/time ('' for now)
            duration: Duration string (e.g., '1 D', '1 W', '1 M')
            bar_size: Bar size (e.g., '1 min', '5 mins', '1 hour', '1 day')
            what_to_show: Data type ('TRADES', 'MIDPOINT', 'BID', 'ASK')
            use_rth: Use regular trading hours only

        Returns:
            BarDataList
        """
        return self.ib.reqHistoricalData(
            contract,
            endDateTime=end_datetime,
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow=what_to_show,
            useRTH=use_rth
        )

    def sleep(self, seconds: float):
        """
        Sleep for specified seconds (maintains event loop).

        Args:
            seconds: Time to sleep in seconds
        """
        self.ib.sleep(seconds)

    def wait_for_update(self, timeout: float = 2.0):
        """
        Wait for next update event.

        Args:
            timeout: Maximum time to wait
        """
        self.ib.waitOnUpdate(timeout=timeout)

    # State checking methods
    def is_connected(self) -> bool:
        """Check if connected to IB"""
        return self.connected and self.ib.isConnected()

    def has_errors(self) -> bool:
        """Check if any errors occurred"""
        return len(self.errors) > 0

    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """Get most recent error"""
        return self.errors[-1] if self.errors else None

    def clear_errors(self):
        """Clear error list"""
        self.errors.clear()

    def clear_tracking(self):
        """Clear all tracking data"""
        self.errors.clear()
        self.order_statuses.clear()
        self.executions.clear()
        self.commissions.clear()
