from __future__ import (absolute_import, division, print_function, unicode_literals)
import yfinance as yf
import backtrader as bt
import time
import datetime as dt
import sys, math
from dateutil.relativedelta import relativedelta

ticker = 'SPY'
last_n_years = 10
sma_fast_period = 20
sma_slow_period = 50

# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop

# Strategy:
# If I am Not holding any position & price goes above sma Then: BUY
# If I am holding position & price goes below sma Then: CLOSE/SELL
class MyStrategy(bt.Strategy):
    # params = (('order_percentage',0.9))

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        print("initializing strategy")
        self.data_ready = False
        self.dataclose = self.datas[0].close
        self.ma_fast = bt.ind.SMA(self.dataclose, period=sma_fast_period)
        self.ma_slow = bt.ind.SMA(self.dataclose, period=sma_slow_period)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)
        self.qty = 0

    def start(self):
        self.val_start = self.broker.get_cash()

    def next(self):
        # self.log_data()
        # self.log('EVALUATE ORDER [fma: {}, sma: {} @closeprice: {}]'.format(self.ma_fast[0], self.ma_slow[0], self.dataclose[0]))
        if self.position.size > 0:
            if self.crossover < 0:
                self.sell(size=self.qty)
                self.log('SELL ORDER [fma: {}, sma: {} @closeprice: {}, qty: {}]'.format(self.ma_fast[0], self.ma_slow[0], self.dataclose[0], self.qty))
        elif self.crossover > 0:
            self.qty = math.floor(0.80 * self.broker.get_cash() / self.data)
            self.buy(size=self.qty)
            self.log(f'BUY ORDER [fma: {self.ma_fast[0]}, sma: {self.ma_slow[0]} @closeprice: {self.dataclose[0]}, qty: {self.qty}]')

    def notify_order(self, order):
        curdtstr = self.data.datetime.datetime().strftime('%a %Y-%m-%d %H:%M:%S')
        if order.status in [order.Completed] or True:
            if order.isbuy():
                if order.executed.dt is not None:
                    dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    print('{}: BUY  EXECUTED, on: {}, qty {}'.format(curdtstr, dtstr, order.size))
                    self.order = None
                else:
                    dtstr = bt.num2date(order.created.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    #print('{}: BUY {}, on: {}, dt {}'.format(curdtstr, order.getstatusname(), dtstr, order.created.dt))
            else:
                if order.executed.dt is not None:  # Sell
                    dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    print('{}: SELL  EXECUTED, on: {}, qty: {}'.format(curdtstr, dtstr, order.size))
            # print(self.position)

    def log_data(self):
        text = '{}, O:{}, H:{}, L:{}, C:{}, V:{}'.format(
            str(self.data.datetime.datetime()), str(
                self.data.open[0]), str(self.data.high[0]),
            str(self.data.low[0]), str(self.data.close[0]), str(self.data.volume[0]))
        print(text)

def run_main():
    global ticker
    last_n_years = int(sys.argv[1:][0])
    sma_fast_period = int(sys.argv[1:][1])
    sma_fast_period = int(sys.argv[1:][2])
    if len(sys.argv) >= 5:
        ticker = sys.argv[1:][3]

    print(f'{last_n_years}, {sma_fast_period}, {sma_fast_period}, {ticker}')

    toDate = dt.date.today();
    fromDate = toDate - relativedelta(years=last_n_years)

    # Create a cerebro entity - think of it is as your Car's Engine
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(100000)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    # cerebro.addsizer(bt.sizers.PercentSizerInt, percents=80)
    cerebro.addstrategy(MyStrategy)
    print(f"Starting Value: {cerebro.broker.get_value()}")

    data = bt.feeds.PandasData(dataname=yf.download(ticker, start=fromDate,end=toDate))

    # Passing Price Data to cerebro
    cerebro.adddata(data)
    # cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)

    # start the engine
    cerebro.run()

    print(f"Cash In hand: {cerebro.broker.get_cash()}, Final Value: {cerebro.broker.get_value()}")


    # print(cerebro.broker.getposition(data))

    # # Plotting a chart
    cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()