from __future__ import (absolute_import, division, print_function, unicode_literals)
import yfinance as yf
import backtrader as bt
import datetime as dt
import argparse
from util.logger import Logger
from dateutil.relativedelta import relativedelta

import math

ticker = 'SPY'
last_n_years = 10
initial_cash = 2500000
final_close_price = -1
profit_percentage = 1.02
cash_for_purchase = 20000

# python3 _backtest_VSIP.py --ticker NIFTYBEES.NS --duration 5 --start 2011-01-01 --end 2022-12-31 --cash 2500000

# Strategy:
# Start with Initial Cash
# Equally split into 5 lots of cash.
# Enter Market by buying one lot worth of stock
# If Next Day price falls further by 2 percentage buy another lot (hold max of 5 lots)
# If Next Day price increases by 1% on any lot you have held, Close that lot
# Rinse and Repeat 
class DailyBuySellProfitStrategy(bt.Strategy):
    # params = (('order_percentage',0.9))

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        print("initializing strategy")
        self.data_ready = False
        self.dataclose = self.datas[0].close
        self.logger = Logger.instance()
        self.previous_close_price = None
        self.total_unit_holding = 0
        self.total_amt = 0
        global profit_percentage, cash_for_purchase
        self.profit_percentage = profit_percentage
        self.cash_for_purchase = cash_for_purchase

    def start(self):
        self.val_start = self.broker.get_cash()
    
    def get_current_value(self, current_price):
        return self.total_unit_holding *  current_price
    
    def get_buy_factor(self, current_price):
        return self.get_current_profit_loss_percent(current_price) * 0.4

    def get_current_profit_loss_percent(self, current_price):
        return 0 if self.total_amt == 0 else (self.get_current_value(current_price) - self.total_amt) / self.total_amt
    
    def is_profitting(self, current_price):
        return (self.profit_percentage * self.total_amt) < (self.get_current_value(current_price))

    def next(self):
        # self.log_data()
        global final_close_price, initial_cash

        final_close_price = self.dataclose[0]

        if self.total_unit_holding > 0 and self.is_profitting(final_close_price):
            self.sell(size=self.total_unit_holding)
            self.log(f'SELL, {self.dataclose[0]:,.2f}, {self.total_unit_holding}')
            self.total_unit_holding = 0
            self.total_amt = 0
        else:
            buy_factor = 0 if self.previous_close_price == None else self.get_buy_factor(final_close_price)
            buy_amt = self.cash_for_purchase + (buy_factor * self.cash_for_purchase)

            if buy_amt < self.broker.get_cash():
                buy_qty = math.floor(buy_amt / self.data)
                self.buy(size=buy_qty)
                self.total_unit_holding += buy_qty
                self.total_amt += (buy_qty * final_close_price)
                self.log(f'BUY, {self.dataclose[0]:,.2f}, {buy_qty}, {buy_amt:,.2f}, {self.total_unit_holding}, {self.total_amt:,.2f}')
        
        self.previous_close_price = final_close_price

    def log_data(self):
        text = '{}, O:{}, H:{}, L:{}, C:{}, V:{}'.format(
            str(self.data.datetime.datetime()), str(
                self.data.open[0]), str(self.data.high[0]),
            str(self.data.low[0]), str(self.data.close[0]), str(self.data.volume[0]))
        print(text)




# python3 _backtest_BuyDaily_SellOnProfit.py --ticker NIFTYBEES.NS --duration 1 --cash 1000000 --start 2020-01-01 --end 2020-12-31 | tail -1

def run_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tp', type=float, required=False, help="Sell target price percent", nargs='?', const=1.01)
    parser.add_argument('--cash', type=int, required=False, help="Money allocated for this strategy", nargs='?', const=100000)
    parser.add_argument('--ticker', type=str, required=True, help="Ticket symbol: e.g. SPY, NIFTYBEES.NS", nargs='?', const="NIFTYBEES.NS")
    parser.add_argument('--start', type=str, required=False, help="From date in YYYY-MM-DD format")
    parser.add_argument('--end', type=str, required=False, help="To date in YYYY-MM-DD format")
    parser.add_argument('--duration', type=int, required=False, help="Duration - last x years. If -f,-t is specified duration is ignored", nargs='?', const=10)
    parser.add_argument('--chart', type=bool, required=False, help="Show chart if specified.", nargs='?', const=False)
    args = parser.parse_args()

    if args.ticker:
        ticker = args.ticker
    if args.cash:
        initial_cash = args.cash
    if args.tp:
        target_profit_percentage = args.tp
    show_chart = args.chart

    if args.start and args.end:
        toDate = dt.datetime.strptime(args.end, "%Y-%m-%d")
        fromDate = dt.datetime.strptime(args.start, "%Y-%m-%d")
        if fromDate > toDate:
            raise "Incorrect Start and End Dates."
    else:
        if args.duration:
            last_n_years = args.duration
        toDate = dt.date.today();
        fromDate = toDate - relativedelta(years=last_n_years)


    # Create a cerebro entity - think of it is as your Car's Engine
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(initial_cash)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    # cerebro.addsizer(bt.sizers.PercentSizerInt, percents=80)
    cerebro.addstrategy(DailyBuySellProfitStrategy)
    print(f"Starting Value: {cerebro.broker.get_value()}")

    data = bt.feeds.PandasData(dataname=yf.download(ticker, start=fromDate,end=toDate))

    # Passing Price Data to cerebro
    cerebro.adddata(data)
    # cerebro.resampledata(data,timeframe=bt.TimeFrame.Days, compression=1)

    # start the engine
    cerebro.run()

    # print(cerebro.broker.getposition(data))
    final_value = cerebro.broker.get_value()

    print(f"""Ticker: {ticker}, Initial Cash: {initial_cash:,.2f}, \
Final Value: {final_value:,.2f}, Profit/Loss%: {100*(final_value-initial_cash)/initial_cash:,.2f}, Quantity: {cerebro.broker.getposition(data).size}, \
ClosePrice: {final_close_price:,.2f}, Cash In hand: {cerebro.broker.get_cash():,.2f}""")

    # # Plotting a chart
    if show_chart:
        cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()