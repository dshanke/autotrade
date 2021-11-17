[Home](index.html)

### Program - Get historical prices this time using the `backtrader` library and plot a price chart.

[Previous](lesson3.html)

#### What is [backtrader](https://www.backtrader.com/)?

It is a feature-rich Python framework for back-testing and live trading.  
`backtrader` allows you to focus on writing reusable trading strategies, indicators and analyzers instead of having to spend time building infrastructure.

Simply put it is a user-friendly library that you can use to write trading programs.

Let's proceed to write a program that will fetch the same historical data for SPY ticker using the backtrader library. 

Create a file under `tutorials` folder and name it as `02.backtrader_get_price_data_plot_price_chart`
```python
import datetime as dt
import backtrader as bt

def run_main():
    print("hello from run_main")
    # fromDate=dt.datetime(2010,1, 1)
    # toDate=dt.datetime(2021,10, 21)
    # 
    # # Create a cerebro entity - think of it is as your Car's Engine
    # cerebro = bt.Cerebro(stdstats=False)
    # 
    # cerebro.broker.setcash(100000)
    # print(f"Starting Value: {cerebro.broker.get_value()}")
    # 
    # data = bt.feeds.YahooFinanceCSVData(dataname="spy.csv",fromdate=fromDate,todate=toDate)
    # #data = bt.feeds.YahooFinanceData(dataname="SPY",fromdate=fromDate,todate=toDate)
    # 
    # # Passing Price Data to cerebro
    # # cerebro.adddata(data)
    # cerebro.resampledata(data,timeframe=bt.TimeFrame.Weeks, compression=1)
    # 
    # # # Adding Indicators
    # cerebro.addindicator(bt.indicators.SMA, period=20)
    # cerebro.addindicator(bt.indicators.SMA, period=50)
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

The program will fetch the historical price using the backtrader library and will plot a price chart.

[Next](lesson5.html)