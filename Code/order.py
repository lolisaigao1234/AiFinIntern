import backtrader as bt
from ib_insync import *
import datetime
import numpy as np
from scipy.stats import norm


# Black-Scholes Model Implementation
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # Put option
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price


# Calculate implied volatility using Newton-Raphson method
def implied_volatility(price, S, K, T, r, option_type='call'):
    MAX_ITERATIONS = 100
    PRECISION = 1.0e-5
    sigma = 0.5  # Initial guess

    for i in range(MAX_ITERATIONS):
        price_estimate = black_scholes(S, K, T, r, sigma, option_type)
        vega = S * np.sqrt(T) * norm.pdf((np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T)))
        diff = price_estimate - price

        if abs(diff) < PRECISION:
            return sigma

        sigma = sigma - diff / vega

    return sigma  # If no convergence, return the last calculated sigma


# Define the aggressive Black-Scholes strategy
class AggressiveBlackScholesStrategy(bt.Strategy):
    params = (
        ('short_period', 10),
        ('long_period', 30),
        ('risk_free_rate', 0.02),  # Assuming 2% risk-free rate
        ('time_to_expiry', 30 / 365),  # 30 days to expiry
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)

    def next(self):
        current_price = self.data.close[0]

        # Calculate implied volatility
        atm_call_price = self.data.close[0] * 0.05  # Assuming ATM call price is 5% of stock price
        implied_vol = implied_volatility(atm_call_price, current_price, current_price,
                                         self.params.time_to_expiry, self.params.risk_free_rate)

        # Calculate option prices
        call_price = black_scholes(current_price, current_price, self.params.time_to_expiry,
                                   self.params.risk_free_rate, implied_vol, 'call')
        put_price = black_scholes(current_price, current_price, self.params.time_to_expiry,
                                  self.params.risk_free_rate, implied_vol, 'put')

        # Aggressive trading logic
        if not self.position:
            if self.crossover > 0 and call_price < current_price * 0.03:  # If call options seem undervalued
                self.buy()
            elif self.crossover < 0 and put_price < current_price * 0.03:  # If put options seem undervalued
                self.sell()
        else:
            if self.position.size > 0 and (self.crossover < 0 or call_price > current_price * 0.07):
                self.close()
            elif self.position.size < 0 and (self.crossover > 0 or put_price > current_price * 0.07):
                self.close()


# Connect to Interactive Brokers
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the contract
contract = Stock('AMD', 'SMART', 'USD')

# Fetch historical data
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='60 D',
    barSizeSetting='1 day', whatToShow='MIDPOINT', useRTH=True)

# Convert IB data to Backtrader format
data = bt.feeds.PandasData(dataname=util.df(bars))

# Create Backtrader Cerebro engine
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(data)

# Add strategy to Cerebro
cerebro.addstrategy(AggressiveBlackScholesStrategy)

# Set initial cash
cerebro.broker.setcash(100000.0)

# Run the backtest
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


# Function to execute trades in IB based on Backtrader signals
def execute_trade(action, quantity):
    if action == 'BUY':
        order = MarketOrder('BUY', quantity)
    elif action == 'SELL':
        order = MarketOrder('SELL', quantity)
    else:
        return

    trade = ib.placeOrder(contract, order)
    print(f"Placed {action} order for {quantity} shares")

    def order_status(trade, fill):
        print(f"Order {action} status: {trade.orderStatus.status}")
        print(f"Filled: {fill}")

    trade.fillEvent += order_status


# Main loop for live trading
def run_strategy():
    while True:
        # Fetch latest data
        latest_bar = ib.reqHistoricalData(
            contract, endDateTime='', durationStr='1 D',
            barSizeSetting='1 day', whatToShow='MIDPOINT', useRTH=True)[-1]

        # Update strategy with new data
        cerebro.adddata(bt.feeds.PandasData(dataname=util.df([latest_bar])))
        cerebro.run(runonce=False)

        # Check for signals and execute trades
        strategy = cerebro.runstrats[-1].strategy
        current_position = cerebro.broker.getposition(data).size

        if current_position == 0:
            if strategy.crossover > 0 and strategy.call_price < strategy.data.close[0] * 0.03:
                execute_trade('BUY', 100)
            elif strategy.crossover < 0 and strategy.put_price < strategy.data.close[0] * 0.03:
                execute_trade('SELL', 100)
        else:
            if (current_position > 0 and
                    (strategy.crossover < 0 or strategy.call_price > strategy.data.close[0] * 0.07)):
                execute_trade('SELL', abs(current_position))
            elif (current_position < 0 and
                  (strategy.crossover > 0 or strategy.put_price > strategy.data.close[0] * 0.07)):
                execute_trade('BUY', abs(current_position))

        # Wait for next trading day
        ib.sleep(24 * 60 * 60)


# Run the live trading strategy
run_strategy()

# Disconnect from IB
ib.disconnect()