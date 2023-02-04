import datetime as dt
import yfinance as yf
import backtrader as bt

# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop
class MyStrategy(bt.Strategy):
    def __init__(self):
        print("initializing strategy")
        self.pre_next_count = 0
        self.ma_fast = bt.indicators.SimpleMovingAverage(period=20)
        self.ma_slow = bt.indicators.SimpleMovingAverage(period=50)

    def start(self):
        print("start...")

    def prenext(self):
        print("prenext...")
        self.pre_next_count = self.pre_next_count + 1
        print(f'prenext count {self.pre_next_count}')

    def nextstart(self):
        print("nextstart...")

    # looking for incoming data in order to operate on it
    def next(self):
        print("\nnext...")
        # Get the price action on last candle
        current_date = self.data.datetime.datetime().strftime('%a %Y-%m-%d')
        open_price = self.data.open[0]
        high_price = self.data.high[0]
        low_price = self.data.low[0]
        close_price = self.data.close[0]
        volume = self.data.volume[0]
        print('{}, open:{}, high:{}, low:{}, close:{}, vol:{}, fast_ma: {}, slow_ma: {}'.format(
            current_date, open_price, high_price, low_price, close_price, volume,
            round(self.ma_fast[0], 2), round(self.ma_slow[0], 2)))
        if self.ma_fast >= self.ma_slow:
            # Do something
            print("Market is in an Uptrend...")
        
        elif self.ma_fast < self.ma_slow:
            print("Market is in a Downtrend...")

    def stop(self):
        print("stop...")

def run_main():
    print("run_main...")
    fromDate = dt.datetime(2018, 1, 1)
    toDate = dt.date.today();
    
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
    
    # Plotting a chart
    cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()