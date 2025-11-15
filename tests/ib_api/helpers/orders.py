"""
Order Helper Functions for Testing

Simplified order creation functions using ib_insync.
Based on Interactive Brokers OrderSamples patterns, adapted for testing.
"""

from ib_insync import Order, LimitOrder, MarketOrder, StopOrder, StopLimitOrder
from typing import Optional, List


class OrderHelpers:
    """
    Helper class for creating common order types for testing.

    Uses ib_insync order classes and provides simplified interfaces.
    All orders are configured for paper trading testing.
    """

    # ===================================
    # Basic Order Types
    # ===================================

    @staticmethod
    def market_order(action: str, quantity: float) -> MarketOrder:
        """
        Create a market order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity (number of shares/contracts)

        Returns:
            MarketOrder object
        """
        return MarketOrder(action=action, totalQuantity=quantity)

    @staticmethod
    def limit_order(action: str, quantity: float, limit_price: float) -> LimitOrder:
        """
        Create a limit order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            limit_price: Limit price

        Returns:
            LimitOrder object
        """
        return LimitOrder(action=action, totalQuantity=quantity, lmtPrice=limit_price)

    @staticmethod
    def stop_order(action: str, quantity: float, stop_price: float) -> StopOrder:
        """
        Create a stop order (becomes market order when stop price hit).

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            stop_price: Stop trigger price

        Returns:
            StopOrder object
        """
        return StopOrder(action=action, totalQuantity=quantity, stopPrice=stop_price)

    @staticmethod
    def stop_limit_order(
        action: str,
        quantity: float,
        stop_price: float,
        limit_price: float
    ) -> StopLimitOrder:
        """
        Create a stop-limit order (becomes limit order when stop price hit).

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            stop_price: Stop trigger price
            limit_price: Limit price after stop is triggered

        Returns:
            StopLimitOrder object
        """
        return StopLimitOrder(
            action=action,
            totalQuantity=quantity,
            stopPrice=stop_price,
            lmtPrice=limit_price
        )

    # ===================================
    # Advanced Order Types
    # ===================================

    @staticmethod
    def bracket_order(
        parent_id: int,
        action: str,
        quantity: float,
        limit_price: float,
        take_profit_limit: float,
        stop_loss_price: float
    ) -> List[Order]:
        """
        Create a bracket order (parent + take profit + stop loss).

        Args:
            parent_id: Order ID for parent order
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            limit_price: Entry limit price
            take_profit_limit: Take profit limit price
            stop_loss_price: Stop loss trigger price

        Returns:
            List of 3 orders: [parent, take_profit, stop_loss]
        """
        # Determine child order actions (opposite of parent)
        child_action = 'SELL' if action == 'BUY' else 'BUY'

        # Parent order (entry)
        parent = LimitOrder(action=action, totalQuantity=quantity, lmtPrice=limit_price)
        parent.orderId = parent_id
        parent.transmit = False  # Don't transmit until children are attached

        # Take profit order
        take_profit = LimitOrder(
            action=child_action,
            totalQuantity=quantity,
            lmtPrice=take_profit_limit
        )
        take_profit.orderId = parent_id + 1
        take_profit.parentId = parent_id
        take_profit.transmit = False

        # Stop loss order
        stop_loss = StopOrder(
            action=child_action,
            totalQuantity=quantity,
            stopPrice=stop_loss_price
        )
        stop_loss.orderId = parent_id + 2
        stop_loss.parentId = parent_id
        stop_loss.transmit = True  # Transmit the final order (sends all 3)

        return [parent, take_profit, stop_loss]

    @staticmethod
    def market_on_open(action: str, quantity: float) -> Order:
        """
        Create a market-on-open order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity

        Returns:
            Order object
        """
        order = MarketOrder(action=action, totalQuantity=quantity)
        order.tif = 'OPG'  # Open price guaranteed
        return order

    @staticmethod
    def market_on_close(action: str, quantity: float) -> Order:
        """
        Create a market-on-close order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity

        Returns:
            Order object
        """
        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.orderType = 'MOC'  # Market on close
        return order

    @staticmethod
    def limit_if_touched(
        action: str,
        quantity: float,
        trigger_price: float,
        limit_price: float
    ) -> Order:
        """
        Create a limit-if-touched order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            trigger_price: Trigger price
            limit_price: Limit price after trigger

        Returns:
            Order object
        """
        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.orderType = 'LIT'
        order.auxPrice = trigger_price
        order.lmtPrice = limit_price
        return order

    @staticmethod
    def market_if_touched(action: str, quantity: float, trigger_price: float) -> Order:
        """
        Create a market-if-touched order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            trigger_price: Trigger price

        Returns:
            Order object
        """
        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.orderType = 'MIT'
        order.auxPrice = trigger_price
        return order

    # ===================================
    # Time-in-Force Variations
    # ===================================

    @staticmethod
    def good_till_date(order: Order, datetime_str: str) -> Order:
        """
        Set order to be good till specific date/time.

        Args:
            order: Order to modify
            datetime_str: Date/time string (format: "YYYYMMDD HH:MM:SS")

        Returns:
            Modified order
        """
        order.tif = 'GTD'
        order.goodTillDate = datetime_str
        return order

    @staticmethod
    def immediate_or_cancel(order: Order) -> Order:
        """
        Set order to Immediate-or-Cancel (IOC).

        Args:
            order: Order to modify

        Returns:
            Modified order
        """
        order.tif = 'IOC'
        return order

    @staticmethod
    def fill_or_kill(order: Order) -> Order:
        """
        Set order to Fill-or-Kill (FOK).

        Args:
            order: Order to modify

        Returns:
            Modified order
        """
        order.tif = 'FOK'
        return order

    @staticmethod
    def good_till_cancelled(order: Order) -> Order:
        """
        Set order to Good-Till-Cancelled (GTC).

        Args:
            order: Order to modify

        Returns:
            Modified order
        """
        order.tif = 'GTC'
        return order

    # ===================================
    # Order Modifiers
    # ===================================

    @staticmethod
    def set_outside_rth(order: Order, allow: bool = True) -> Order:
        """
        Allow order to trade outside regular trading hours.

        Args:
            order: Order to modify
            allow: True to allow outside RTH, False to restrict to RTH

        Returns:
            Modified order
        """
        order.outsideRth = allow
        return order

    @staticmethod
    def set_all_or_none(order: Order, enable: bool = True) -> Order:
        """
        Set all-or-none execution requirement.

        Args:
            order: Order to modify
            enable: True to enable all-or-none

        Returns:
            Modified order
        """
        order.allOrNone = enable
        return order

    @staticmethod
    def set_hidden(order: Order, enable: bool = True) -> Order:
        """
        Set order to be hidden (not displayed in order book).

        Args:
            order: Order to modify
            enable: True to hide order

        Returns:
            Modified order
        """
        order.hidden = enable
        return order

    @staticmethod
    def set_discretionary(order: Order, discretionary_amount: float) -> Order:
        """
        Set discretionary amount for order.

        Args:
            order: Order to modify
            discretionary_amount: Discretionary price amount

        Returns:
            Modified order
        """
        order.discretionaryAmt = discretionary_amount
        return order

    # ===================================
    # Algo Orders (for advanced testing)
    # ===================================

    @staticmethod
    def twap_order(
        action: str,
        quantity: float,
        strategy_type: str = 'Twap',
        start_time: str = '',
        end_time: str = ''
    ) -> Order:
        """
        Create a TWAP (Time-Weighted Average Price) algo order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            strategy_type: 'Twap' (default)
            start_time: Start time (HH:MM:SS format)
            end_time: End time (HH:MM:SS format)

        Returns:
            Order object with TWAP algo
        """
        order = MarketOrder(action=action, totalQuantity=quantity)
        order.algoStrategy = strategy_type

        if start_time:
            order.algoParams = []
            order.algoParams.append(('StartTime', start_time))
        if end_time:
            order.algoParams.append(('EndTime', end_time))

        return order

    @staticmethod
    def vwap_order(
        action: str,
        quantity: float,
        max_pct_volume: float = 10.0
    ) -> Order:
        """
        Create a VWAP (Volume-Weighted Average Price) algo order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            max_pct_volume: Maximum percentage of volume (default: 10%)

        Returns:
            Order object with VWAP algo
        """
        order = MarketOrder(action=action, totalQuantity=quantity)
        order.algoStrategy = 'Vwap'
        order.algoParams = [('MaxPctVol', str(max_pct_volume))]
        return order

    @staticmethod
    def adaptive_order(
        action: str,
        quantity: float,
        priority: str = 'Normal'
    ) -> Order:
        """
        Create an Adaptive algo order.

        Args:
            action: 'BUY' or 'SELL'
            quantity: Order quantity
            priority: 'Patient', 'Normal', 'Urgent' (default: 'Normal')

        Returns:
            Order object with Adaptive algo
        """
        order = MarketOrder(action=action, totalQuantity=quantity)
        order.algoStrategy = 'Adaptive'
        order.algoParams = [('adaptivePriority', priority)]
        return order

    # ===================================
    # Testing Helpers
    # ===================================

    @staticmethod
    def create_test_buy_market(quantity: float = 100) -> MarketOrder:
        """Quick test buy market order"""
        return OrderHelpers.market_order('BUY', quantity)

    @staticmethod
    def create_test_sell_market(quantity: float = 100) -> MarketOrder:
        """Quick test sell market order"""
        return OrderHelpers.market_order('SELL', quantity)

    @staticmethod
    def create_test_buy_limit(quantity: float = 100, price: float = 100.0) -> LimitOrder:
        """Quick test buy limit order"""
        return OrderHelpers.limit_order('BUY', quantity, price)

    @staticmethod
    def create_test_sell_limit(quantity: float = 100, price: float = 100.0) -> LimitOrder:
        """Quick test sell limit order"""
        return OrderHelpers.limit_order('SELL', quantity, price)

    # ===================================
    # Order Validation
    # ===================================

    @staticmethod
    def validate_order(order: Order) -> bool:
        """
        Basic validation of order attributes.

        Args:
            order: Order to validate

        Returns:
            bool: True if basic validation passes
        """
        if order.action not in ['BUY', 'SELL']:
            return False
        if order.totalQuantity is None or order.totalQuantity <= 0:
            return False
        if order.orderType is None or order.orderType == '':
            return False
        return True

    @staticmethod
    def get_order_description(order: Order) -> str:
        """
        Get human-readable order description.

        Args:
            order: Order to describe

        Returns:
            str: Order description
        """
        desc = f"{order.action} {order.totalQuantity} @ {order.orderType}"

        if hasattr(order, 'lmtPrice') and order.lmtPrice:
            desc += f" LMT={order.lmtPrice}"
        if hasattr(order, 'stopPrice') and order.stopPrice:
            desc += f" STP={order.stopPrice}"
        if hasattr(order, 'auxPrice') and order.auxPrice:
            desc += f" AUX={order.auxPrice}"
        if hasattr(order, 'tif') and order.tif:
            desc += f" TIF={order.tif}"

        return desc


# Convenience function aliases for quick access
def market(action: str, quantity: float) -> MarketOrder:
    """Quick market order creation"""
    return OrderHelpers.market_order(action, quantity)


def limit(action: str, quantity: float, price: float) -> LimitOrder:
    """Quick limit order creation"""
    return OrderHelpers.limit_order(action, quantity, price)


def stop(action: str, quantity: float, stop_price: float) -> StopOrder:
    """Quick stop order creation"""
    return OrderHelpers.stop_order(action, quantity, stop_price)


def stop_limit(action: str, quantity: float, stop_price: float, limit_price: float) -> StopLimitOrder:
    """Quick stop-limit order creation"""
    return OrderHelpers.stop_limit_order(action, quantity, stop_price, limit_price)


# Quick buy/sell helpers
def buy_market(quantity: float = 100) -> MarketOrder:
    """Quick buy market order"""
    return market('BUY', quantity)


def sell_market(quantity: float = 100) -> MarketOrder:
    """Quick sell market order"""
    return market('SELL', quantity)


def buy_limit(quantity: float, price: float) -> LimitOrder:
    """Quick buy limit order"""
    return limit('BUY', quantity, price)


def sell_limit(quantity: float, price: float) -> LimitOrder:
    """Quick sell limit order"""
    return limit('SELL', quantity, price)
