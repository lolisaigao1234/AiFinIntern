from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AMD', 'SMART', 'USD')

bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

df = util.df(bars)
print(df)

market_data = ib.reqMktData(contract, '', False, False)

def onPendingTickers(tickers):
    print("ticker received", tickers)

ib.pendingTickersEvent += onPendingTickers

ib.run()