[Home](https://ddtrades.github.io/autotrade/)

### Program - Another strategy - Favourite one -  Golden Crossover strategy

[Previous](https://ddtrades.github.io/autotrade/lesson6)

#### Define your strategy in layman terms
* Define your fast moving average(fastSMA) and slow moving average(slowSMA)
* If fastSMA goes above slowSMA `AND` I am NOT holding any position Then: BUY
* If fastSMA goes below slowSMA `AND` I am holding position  Then: CLOSE/SELL


Let's see the Implementation.

Create a file under `tutorials` folder and name it as `04.backtrader_simple_buy_sell_strategy.py`

```python
import datetime as dt
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

    data = bt.feeds.YahooFinanceData(dataname="AAPL",fromdate=fromDate,todate=toDate)

    # Passing Price Data to cerebro
    # cerebro.adddata(data)
    cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)

    # start the engine
    cerebro.run()

    print(f"Final Value: {cerebro.broker.get_value()}")

    # # Plotting a chart
    cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()
```

If you observe closely there are vey minor changes in this program when compared with the previous program that we saw


You can run this strategy on your favourite tickers.
How does your chart look? Did you make profit or loss?

[Next](https://ddtrades.github.io/autotrade/lesson8)