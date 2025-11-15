"""
Contract Helper Functions for Testing

Simplified contract creation functions using ib_insync.
Based on Interactive Brokers ContractSamples patterns.
"""

from ib_insync import Stock, Option, Future, Forex, Index, CFD, Bond, Crypto, Contract
from datetime import datetime, timedelta


class ContractHelpers:
    """
    Helper class for creating common contract types for testing.

    Uses ib_insync contract classes instead of ibapi Contract.
    All contracts are configured for paper trading testing.
    """

    # ===================================
    # Stock Contracts
    # ===================================

    @staticmethod
    def us_stock(symbol: str = 'AAPL', exchange: str = 'SMART', currency: str = 'USD') -> Stock:
        """
        Create US stock contract.

        Args:
            symbol: Stock symbol (default: AAPL)
            exchange: Exchange (default: SMART for best execution)
            currency: Currency (default: USD)

        Returns:
            Stock contract
        """
        return Stock(symbol=symbol, exchange=exchange, currency=currency)

    @staticmethod
    def us_stock_spy() -> Stock:
        """SPY ETF - highly liquid, good for testing"""
        return Stock('SPY', 'ARCA', 'USD')

    @staticmethod
    def us_stock_aapl() -> Stock:
        """Apple stock - NASDAQ"""
        return Stock('AAPL', 'SMART', 'USD')

    @staticmethod
    def us_stock_ibkr() -> Stock:
        """Interactive Brokers stock"""
        return Stock('IBKR', 'SMART', 'USD')

    @staticmethod
    def us_stock_tsla() -> Stock:
        """Tesla stock"""
        return Stock('TSLA', 'SMART', 'USD')

    @staticmethod
    def etf_qqq() -> Stock:
        """QQQ ETF - NASDAQ 100"""
        return Stock('QQQ', 'SMART', 'USD')

    @staticmethod
    def european_stock_bmw() -> Stock:
        """BMW stock - European"""
        return Stock('BMW', 'SMART', 'EUR', primaryExchange='IBIS')

    # ===================================
    # Option Contracts
    # ===================================

    @staticmethod
    def us_option_call(
        symbol: str = 'AAPL',
        strike: float = 150.0,
        expiry: str = None,
        exchange: str = 'SMART'
    ) -> Option:
        """
        Create US call option contract.

        Args:
            symbol: Underlying symbol
            strike: Strike price
            expiry: Expiration date (YYYYMMDD format, default: ~30 days out)
            exchange: Exchange (default: SMART)

        Returns:
            Option contract
        """
        if expiry is None:
            # Default to ~30 days out, third Friday
            expiry = ContractHelpers._get_next_expiry()

        return Option(
            symbol=symbol,
            lastTradeDateOrContractMonth=expiry,
            strike=strike,
            right='C',  # Call
            exchange=exchange,
            currency='USD'
        )

    @staticmethod
    def us_option_put(
        symbol: str = 'AAPL',
        strike: float = 150.0,
        expiry: str = None,
        exchange: str = 'SMART'
    ) -> Option:
        """
        Create US put option contract.

        Args:
            symbol: Underlying symbol
            strike: Strike price
            expiry: Expiration date (YYYYMMDD format, default: ~30 days out)
            exchange: Exchange (default: SMART)

        Returns:
            Option contract
        """
        if expiry is None:
            expiry = ContractHelpers._get_next_expiry()

        return Option(
            symbol=symbol,
            lastTradeDateOrContractMonth=expiry,
            strike=strike,
            right='P',  # Put
            exchange=exchange,
            currency='USD'
        )

    @staticmethod
    def spy_option_call(strike: float = 450.0) -> Option:
        """SPY call option for testing"""
        return ContractHelpers.us_option_call('SPY', strike)

    # ===================================
    # Futures Contracts
    # ===================================

    @staticmethod
    def es_future(expiry: str = None) -> Future:
        """
        E-mini S&P 500 futures contract.

        Args:
            expiry: Expiration (YYYYMM format, default: next quarter)

        Returns:
            Future contract
        """
        if expiry is None:
            expiry = ContractHelpers._get_next_quarterly_expiry()

        return Future(
            symbol='ES',
            lastTradeDateOrContractMonth=expiry,
            exchange='CME',
            currency='USD'
        )

    @staticmethod
    def nq_future(expiry: str = None) -> Future:
        """
        E-mini NASDAQ-100 futures contract.

        Args:
            expiry: Expiration (YYYYMM format, default: next quarter)

        Returns:
            Future contract
        """
        if expiry is None:
            expiry = ContractHelpers._get_next_quarterly_expiry()

        return Future(
            symbol='NQ',
            lastTradeDateOrContractMonth=expiry,
            exchange='CME',
            currency='USD'
        )

    @staticmethod
    def cl_future(expiry: str = None) -> Future:
        """
        Crude Oil futures contract.

        Args:
            expiry: Expiration (YYYYMM format, default: next month)

        Returns:
            Future contract
        """
        if expiry is None:
            expiry = ContractHelpers._get_next_monthly_expiry()

        return Future(
            symbol='CL',
            lastTradeDateOrContractMonth=expiry,
            exchange='NYMEX',
            currency='USD'
        )

    # ===================================
    # Forex Contracts
    # ===================================

    @staticmethod
    def forex_eur_usd() -> Forex:
        """EUR/USD forex pair"""
        return Forex('EUR', currency='USD')

    @staticmethod
    def forex_gbp_usd() -> Forex:
        """GBP/USD forex pair"""
        return Forex('GBP', currency='USD')

    @staticmethod
    def forex_usd_jpy() -> Forex:
        """USD/JPY forex pair"""
        return Forex('USD', currency='JPY')

    @staticmethod
    def forex_custom(base: str, quote: str) -> Forex:
        """
        Create custom forex pair.

        Args:
            base: Base currency (e.g., 'EUR')
            quote: Quote currency (e.g., 'USD')

        Returns:
            Forex contract
        """
        return Forex(base, currency=quote)

    # ===================================
    # Index Contracts
    # ===================================

    @staticmethod
    def spx_index() -> Index:
        """S&P 500 Index"""
        return Index('SPX', 'CBOE', 'USD')

    @staticmethod
    def vix_index() -> Index:
        """VIX Volatility Index"""
        return Index('VIX', 'CBOE', 'USD')

    # ===================================
    # CFD Contracts
    # ===================================

    @staticmethod
    def cfd_us_stock(symbol: str = 'IBM') -> CFD:
        """
        US Stock CFD.

        Args:
            symbol: Stock symbol

        Returns:
            CFD contract
        """
        return CFD(symbol=symbol, exchange='SMART', currency='USD')

    # ===================================
    # Crypto Contracts
    # ===================================

    @staticmethod
    def crypto_btc_usd() -> Crypto:
        """Bitcoin/USD"""
        return Crypto('BTC', 'PAXOS', 'USD')

    @staticmethod
    def crypto_eth_usd() -> Crypto:
        """Ethereum/USD"""
        return Crypto('ETH', 'PAXOS', 'USD')

    # ===================================
    # Helper Methods
    # ===================================

    @staticmethod
    def _get_next_expiry(days_ahead: int = 30) -> str:
        """
        Get next option expiration date (approximately).

        Args:
            days_ahead: Target days in future (default: 30)

        Returns:
            Expiration date in YYYYMMDD format
        """
        target_date = datetime.now() + timedelta(days=days_ahead)
        # Options typically expire on 3rd Friday
        # This is approximate; use actual option chain for production
        return target_date.strftime('%Y%m%d')

    @staticmethod
    def _get_next_monthly_expiry() -> str:
        """
        Get next month's expiry (YYYYMM format).

        Returns:
            Next month in YYYYMM format
        """
        next_month = datetime.now() + timedelta(days=30)
        return next_month.strftime('%Y%m')

    @staticmethod
    def _get_next_quarterly_expiry() -> str:
        """
        Get next quarterly expiry (YYYYMM format).
        Quarters: Mar, Jun, Sep, Dec

        Returns:
            Next quarter in YYYYMM format
        """
        now = datetime.now()
        year = now.year
        month = now.month

        # Find next quarterly month (3, 6, 9, 12)
        if month < 3:
            next_quarter = f"{year}03"
        elif month < 6:
            next_quarter = f"{year}06"
        elif month < 9:
            next_quarter = f"{year}09"
        elif month < 12:
            next_quarter = f"{year}12"
        else:
            next_quarter = f"{year + 1}03"

        return next_quarter

    # ===================================
    # Contract Validation
    # ===================================

    @staticmethod
    def validate_contract(contract: Contract) -> bool:
        """
        Basic validation of contract attributes.

        Args:
            contract: Contract to validate

        Returns:
            bool: True if basic validation passes
        """
        if contract.symbol is None or contract.symbol == '':
            return False
        if contract.exchange is None or contract.exchange == '':
            return False
        if contract.currency is None or contract.currency == '':
            return False
        return True

    # ===================================
    # Contract Info
    # ===================================

    @staticmethod
    def get_contract_description(contract: Contract) -> str:
        """
        Get human-readable contract description.

        Args:
            contract: Contract to describe

        Returns:
            str: Contract description
        """
        if isinstance(contract, Stock):
            return f"{contract.symbol} Stock ({contract.exchange})"
        elif isinstance(contract, Option):
            return f"{contract.symbol} {contract.right} {contract.strike} exp {contract.lastTradeDateOrContractMonth}"
        elif isinstance(contract, Future):
            return f"{contract.symbol} Future exp {contract.lastTradeDateOrContractMonth}"
        elif isinstance(contract, Forex):
            return f"{contract.symbol}/{contract.currency} Forex"
        elif isinstance(contract, Index):
            return f"{contract.symbol} Index"
        elif isinstance(contract, CFD):
            return f"{contract.symbol} CFD"
        elif isinstance(contract, Crypto):
            return f"{contract.symbol}/{contract.currency} Crypto"
        else:
            return f"{contract.symbol} ({contract.secType})"


# Convenience function aliases for quick access
def stock(symbol: str, exchange: str = 'SMART', currency: str = 'USD') -> Stock:
    """Quick stock contract creation"""
    return ContractHelpers.us_stock(symbol, exchange, currency)


def option_call(symbol: str, strike: float, expiry: str = None) -> Option:
    """Quick call option creation"""
    return ContractHelpers.us_option_call(symbol, strike, expiry)


def option_put(symbol: str, strike: float, expiry: str = None) -> Option:
    """Quick put option creation"""
    return ContractHelpers.us_option_put(symbol, strike, expiry)


def forex(base: str, quote: str) -> Forex:
    """Quick forex pair creation"""
    return ContractHelpers.forex_custom(base, quote)
