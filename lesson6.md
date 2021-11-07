[Home](https://ddtrades.github.io/autotrade/)

### Program - First Buy/Sell backtrader trading strategy applied on historical data.

[Previous](https://ddtrades.github.io/autotrade/lesson5)

#### Define your strategy in layman terms

* If price goes above sma `AND` I am NOT holding any position Then: BUY
* If I am holding position `AND` price goes below sma Then: CLOSE/SELL


Let's Implement the strategy using backtrader library and then using the backtrader engine let's see how are strategy performs on historical data.

Create a file under `tutorials` folder and name it as `04.backtrader_simple_buy_sell_strategy.py`

```python
import datetime as dt
import backtrader as bt

#strategy:
# If I am Not holding any position & price goes above sma Then: BUY
# If I am holding position & price goes below sma Then: CLOSE/SELL
class MyStrategy(bt.Strategy):
    def __init__(self):
        print("initializing strategy")
        self.sma = bt.indicators.MovingAverageSimple(period=40)

    def next(self):
        print("next...")
        close_price = self.data.close[0]
        # If I am NOT holding any position
        if not self.position:
            # And if the price has closed above sma - buy
            if close_price > round(self.sma[0], 2):
                self.buy()
        # If I am holding a position and if the price has closed below sma - sell
        elif close_price < round(self.sma[0], 2):
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

You can run this strategy on your favourite tickers.
How does your chart look? Did you make profit or loss?

[Next](https://ddtrades.github.io/autotrade/lesson7)