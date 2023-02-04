[Home](index.html)

#### Introduction - `backtrader` framework & use it to fetch and analyse pricing data to derive information   

[Previous](lesson4.html)

###### Introducing bactktrader framework - Understanding the framework & flow of steps

Simply put ==> `Define Strategy + Run Cerebro Engine`

Create a file under `tutorials` folder and name it as `03.backtrader_strategy_introduction.py`

```python
import datetime as dt
import backtrader as bt

# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop
class MyStrategy(bt.Strategy):
    def __init__(self):
        print("initializing strategy")

    def start(self):
        print("start...")

    def prenext(self):
        print("prenext...")

    def nextstart(self):
        print("nextstart...")

    # looking for incoming data in order to operate on it
    def next(self):
        print("\nnext...")

    def stop(self):
        print("stop...")

def run_main():
    print("run_main...")
    fromDate = dt.datetime(2000, 1, 1)
    toDate = dt.datetime(2021, 10, 21)

    # Create a cerebro entity - think of it is as your Car's Engine
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.broker.setcash(100000)
    cerebro.addstrategy(MyStrategy)
    print(f"Starting Value: {cerebro.broker.get_value()}")

    data = bt.feeds.YahooFinanceData(dataname="SPY",fromdate=fromDate,todate=toDate)

    # Passing Price Data to cerebro
    # cerebro.adddata(data)
    cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)

    # start the engine
    cerebro.run()

    print(f"Final Value: {cerebro.broker.get_value()}")

    # # Plotting a chart
    # cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()
```

##### ***backtrader framework - delving deeper***

The two distinct area you need to develop while writing a trading algo with `backtrader`:
* Create a Strategy
  * Conceptualise your idea
  * Decide on potential adjustable parameters
  * Instantiate the Indicators you need in the Strategy
  * Write down the logic for entering/exiting the market

* Execute above defined strategy with the help of backtrader's Cerebro Engine
  * First: Inject the Strategy (or signal-based strategy)
  * Load & Inject a Data Feed (once created use cerebro.adddata)
  * Execute cerebro.run()
  * For visual feedback use: cerebro.plot()

Let's demostrate how we can use the backtrader strategy class to write a program that will detect the momentum of the market 

Copy & paste the below code in the file `03.backtrader_strategy_introduction.py`

```python
import datetime as dt
import backtrader as bt

# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop
class MyStrategy(bt.Strategy):
    def __init__(self):
        print("initializing strategy")
        # self.pre_next_count = 0
        # self.ma_fast = bt.indicators.SimpleMovingAverage(period=20)
        # self.ma_slow = bt.indicators.SimpleMovingAverage(period=50)

    def start(self):
        print("start...")

    def prenext(self):
        print("prenext...")
        # self.pre_next_count = self.pre_next_count + 1
        # print(f'prenext count {self.pre_next_count}')

    def nextstart(self):
        print("nextstart...")

    # looking for incoming data in order to operate on it
    def next(self):
        print("\nnext...")
        # # Get the price action on last candle
        # current_date = self.data.datetime.datetime().strftime('%a %Y-%m-%d')
        # open_price = self.data.open[0]
        # high_price = self.data.high[0]
        # low_price = self.data.low[0]
        # close_price = self.data.close[0]
        # volume = self.data.volume[0]
        # print('{}, open:{}, high:{}, low:{}, close:{}, vol:{}, fast_ma: {}, slow_ma: {}'.format(
        #     current_date, open_price, high_price, low_price, close_price, volume,
        #     round(self.ma_fast[0], 2), round(self.ma_slow[0], 2)))
        # if self.ma_fast >= self.ma_slow:
        #     # Do something
        #     print("Market is in an Uptrend...")
        #
        # elif self.ma_fast < self.ma_slow:
        #     print("Market is in a Downtrend...")

    def stop(self):
        print("stop...")

def run_main():
    print("run_main...")
    # fromDate = dt.datetime(2000, 1, 1)
    # toDate = dt.datetime(2021, 10, 21)
    #
    # # Create a cerebro entity - think of it is as your Car's Engine
    # cerebro = bt.Cerebro(stdstats=False)
    #
    # cerebro.broker.setcash(100000)
    # cerebro.addstrategy(MyStrategy)
    # print(f"Starting Value: {cerebro.broker.get_value()}")
    #
    # data = bt.feeds.YahooFinanceData(dataname="SPY",fromdate=fromDate,todate=toDate)
    #
    # # Passing Price Data to cerebro
    # # cerebro.adddata(data)
    # cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)
    #
    # # start the engine
    # cerebro.run()
    #
    # print(f"Final Value: {cerebro.broker.get_value()}")
    #
    # # Plotting a chart
    # cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()
```

The program fetches historical price & using the backtrader library and detects if we are in an uptrend or downtrend (in layman terms).

[Next](lesson6.html)
