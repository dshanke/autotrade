[Home](https://ddtrades.github.io/autotrade/)

### Live Trading - Interactive Brokers - Futures

[Previous](https://ddtrades.github.io/autotrade/lesson8)

#### Strategy based Futures Trading 
Create a file under `tutorials` folder and name it as `07.backtrader_live_trading_with_ibkr_futures.py`

```python
from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import time
import datetime
import pytz

class MyStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        print("initializing strategy")
        self.data_ready = False
        self.dataclose = self.datas[0].close
        self.ma_fast = bt.ind.SMA(period=8)
        self.ma_slow = bt.ind.SMA(period=20)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        self.log_data()
        if not self.data_ready:
            return
        self.log('EVALUATE ORDER [fma: {}, sma: {} @closeprice: {}]'.format(self.ma_fast[0], self.ma_slow[0], self.dataclose[0]))
        if not self.position:
            if self.crossover > 0:
                self.buy(size=10)
                self.log('BUY ORDER [fma: {}, sma: {} @closeprice: {}]'.format(self.ma_fast[0], self.ma_slow[0], self.dataclose[0]))
        elif self.crossover < 0:
            self.sell(size=10)
            self.log('SELL ORDER [fma: {}, sma: {} @closeprice: {}]'.format(self.ma_fast[0], self.ma_slow[0], self.dataclose[0]))

    def notify_data(self, data, status):
        print('Data Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True

    def notify_order(self, order):
        curdtstr = self.data.datetime.datetime().strftime('%a %Y-%m-%d %H:%M:%S')
        if order.status in [order.Completed] or True:

            if order.isbuy():
                if order.executed.dt is not None:
                    dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    print('{}: BUY  EXECUTED, on: {}, dt {}'.format(curdtstr, dtstr, order.executed.dt))
                    self.order = None
                else:
                    dtstr = bt.num2date(order.created.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    print('{}: BUY {}, on: {}, dt {}'.format(curdtstr, order.getstatusname(), dtstr, order.created.dt))
            else:
                if order.executed.dt is not None:  # Sell
                    dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
                    print('{}: SELL  EXECUTED, on: {}, dt {}'.format(curdtstr, dtstr, order.executed.dt))

    def log_data(self):
        text = '{}, O:{}, H:{}, L:{}, C:{}, V:{}'.format(
            str(self.data.datetime.datetime()), str(
                self.data.open[0]), str(self.data.high[0]),
            str(self.data.low[0]), str(self.data.close[0]), str(self.data.volume[0]))
        print(text)

def run_main():
    print("starting backtrader")
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(host='127.0.0.1', port=7497, clientId=1)
    #TICKER-FUT-EXCHANGE-CURRENCY-YYYYMM
    data = store.getdata(
            dataname='ES-FUT-GLOBEX-USD-202112', 
            tz=pytz.timezone('US/Eastern'), 
            timeframe=bt.TimeFrame.Seconds)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)
    cerebro.broker = store.getbroker()
    cerebro.addstrategy(MyStrategy)
    cerebro.run()

run_main()
```
[Home](https://ddtrades.github.io/autotrade/)