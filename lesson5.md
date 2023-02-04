[Home](index.html)

#### Introduction - `backtrader` framework & use it to fetch and analyse pricing data to derive information   

[Previous](lesson4.html)

###### Introducing bactktrader framework - Understanding the framework & flow of steps

Simply put ==> `Define Strategy + Run Cerebro Engine`

Create a file under `tutorials` folder and name it as `03.backtrader_strategy_introduction.py`

```python
import datetime as dt
import yfinance as yf
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

    ticker = "SPY"
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start=fromDate,end=toDate))

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

The program fetches historical price & using the backtrader library and detects if we are in an uptrend or downtrend (in layman terms).

[Next](lesson6.html)
