import datetime as dt
import backtrader as bt
import yfinance as yf

def run_main():
    print("hello from run_main")
    # fromDate=dt.datetime(2019,2, 1)
    # toDate = dt.date.today();
    
    # # Create a cerebro entity - think of it is as your Car's Engine
    # cerebro = bt.Cerebro(stdstats=False)
    
    # cerebro.broker.setcash(100000)
    # print(f"Starting Value: {cerebro.broker.get_value()}")

    # ticker = "SPY"

    
    # data = bt.feeds.PandasData(dataname=yf.download(ticker, start=fromDate,end=toDate))

    # # Passing Price Data to cerebro
    # cerebro.adddata(data)
    # # cerebro.resampledata(data,timeframe=bt.TimeFrame.Weeks, compression=1)
    
    # # # Adding Indicators
    # cerebro.addindicator(bt.indicators.SMA, period=20)
    # cerebro.addindicator(bt.indicators.SMA, period=50)
    
    # # start the engine
    # cerebro.run()
    
    # print(f"Final Value: {cerebro.broker.get_value()}")
    
    # # Plotting a chart
    # cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()
