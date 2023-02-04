import datetime as dt
import yfinance as yf
import backtrader as bt

# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop

#strategy:
# If I am Not holding any position & price goes above sma Then: BUY
# If I am holding position & price goes below sma Then: CLOSE/SELL
class MyStrategy(bt.Strategy):
    def __init__(self):
        print("initializing strategy")
        self.fastsma = bt.indicators.MovingAverageSimple(period=20)
        self.slowsma = bt.indicators.MovingAverageSimple(period=50)

    def next(self):
        print("next...")
        close_price = self.data.close[0]
        # If I am NOT holding any position
        if not self.position:
            # And if fast sma is above slow sma - BUY
            if round(self.fastsma[0], 2)  > round(self.slowsma[0], 2):
                self.buy()
        # If I am holding a position And if slow sma goes above slow sma - SELL
        elif round(self.slowsma[0], 2)  > round(self.fastsma[0], 2):
            self.sell()

def run_main():
    fromDate = dt.datetime(2020, 1, 1)
    toDate = dt.datetime(2021, 10, 21)

    # Create a cerebro entity - think of it is as your Car's Engine
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(100000)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=80)
    cerebro.addstrategy(MyStrategy)
    print(f"Starting Value: {cerebro.broker.get_value()}")

    ticker = "SPY"
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start=fromDate,end=toDate))

    # Passing Price Data to cerebro
    # cerebro.adddata(data)
    cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)

    # start the engine
    cerebro.run()

    print(f"Final Value: {cerebro.broker.get_value()}")

    # # Plotting a chart
    cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()