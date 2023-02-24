from __future__ import (absolute_import, division, print_function, unicode_literals)
import yfinance as yf
import backtrader as bt
import time
import datetime as dt
import sys, math
import argparse

from operator import attrgetter
from dateutil.relativedelta import relativedelta

from util.logger import Logger

# python3 _backtest_VSIP.py --ticker NIFTYBEES.NS --duration 5 --start 2011-01-01 --end 2022-12-31 --cash 2500000

ticker = 'SPY'
initial_cash = 2500000
last_n_years = 10
enable_log = False
final_close_price = -1
dip_percentage = 0.98
target_profit_percentage = 1.01
max_lots = 3
my_account_holding = None

class Holding:
    def __init__(self, cost_price, quantity):
        global dip_percentage, target_profit_percentage
        self.dip_percentage = dip_percentage
        self.target_profit_percentage = target_profit_percentage
        self.cost_price = cost_price
        self.quantity = quantity
        self.target_price = self.target_profit_percentage * cost_price
        self.logger = Logger.instance()
        self.logger.log(f"Holding Added: cp: {self.cost_price}, tp: {self.target_price}, pp: {self.target_profit_percentage}, qty: {self.quantity}")

    def get_cost_price(self):
        return self.cost_price

    def is_nice_price_to_buy_again(self, lowest_cost_price):
        nice_price_to_buy = lowest_cost_price * self.dip_percentage
        return nice_price_to_buy

    def get_target_price(self):
        return self.target_price

    def get_quantity(self):
        return self.quantity

    def tostring(self):
        print(f"cp: {self.cost_price}, tp: {self.target_price}, pp: {self.target_profit_percentage}, qty: {self.quantity}")

class AccountHolding:
    def __init__(self):
        global max_lots
        self.my_holdings = [ ]
        self.max_lots = max_lots
        self.logger = Logger.instance()
    
    def how_much_cash_to_invest_for_new_purchase(self, available_cash):
        how_many_lots_can_we_still_purchase = self.max_lots - len(self.my_holdings)
        self.logger.log(f'available_cash: {available_cash}, lots:{how_many_lots_can_we_still_purchase}, max_lots:{self.max_lots}')
        return available_cash / how_many_lots_can_we_still_purchase


    def any_holding_to_sell(self, close_price):
        for h in self.my_holdings:
            if h is not None:
                if h.get_target_price >= close_price:
                    return h
        return None

    def get_holding_with_lowest_cost_price(self):
        if len(self.my_holdings) == 0:
            return None
        return min(self.my_holdings, key=attrgetter('cost_price'))

    def anything_to_sell(self, close_price):
        if len(self.my_holdings) == 0:
            return 0
        h = self.get_holding_with_lowest_cost_price()
        if close_price > h.get_target_price():
            self.logger.log(f"SELL SIGNAL ==> close_price: {close_price}, target_price: { h.get_target_price() }")
            return h.get_quantity()
        return 0

    def can_we_buy(self, close_price):
        if len(self.my_holdings) == 0:
            self.logger.log('my_holdings len == 0')
            return True
        elif not self.can_hold_more():
            return False
        else:
            h = self.get_holding_with_lowest_cost_price()
            return close_price < h.is_nice_price_to_buy_again(h.get_cost_price())

    def can_hold_more(self):
        return len(self.my_holdings) < self.max_lots

    def add_holding(self, cost_price, quantity):
        if self.can_hold_more():
            self.my_holdings.append(Holding(cost_price, quantity))
        else:
            raise "Error: Holding limit exceeded"

    def release_holding(self, quantity):
        # result = [x for x in holding.my_holdings if x.attribute != quantity]
        found = False
        new_holdings = []
        for h in self.my_holdings:
            if not found and h.get_quantity() == quantity:
                found = True
                continue
            new_holdings.append(h)
        self.my_holdings = new_holdings


# conception -> birth -> childhood -> adulthood -> death
# init -> start -> prenext -> next -> stop

# Strategy:
# Start with Initial Cash
# Equally split into 5 lots of cash.
# Enter Market by buying one lot worth of stock
# If Next Day price falls further by 2 percentage buy another lot (hold max of 5 lots)
# If Next Day price increases by 1% on any lot you have held, Close that lot
# Rinse and Repeat 
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
        self.logger = Logger.instance()

    def start(self):
        self.val_start = self.broker.get_cash()

    def next(self):
        # self.log_data()
        global my_account_holding, final_close_price, initial_cash

        final_close_price = self.dataclose[0]

        if my_account_holding.can_we_buy(self.dataclose[0]):
            # cash_for_purchase = my_account_holding.how_much_cash_to_invest_for_new_purchase(0.95 * self.broker.get_cash())
            cash_for_purchase = my_account_holding.how_much_cash_to_invest_for_new_purchase(0.95 * initial_cash)

            
            buy_qty = math.floor(cash_for_purchase / self.data)
            self.buy(size=buy_qty)
            self.log(f'BUY, {self.dataclose[0]:,.2f}, {buy_qty}')
            my_account_holding.add_holding(self.dataclose[0], buy_qty)
        
        sell_qty = my_account_holding.anything_to_sell(self.dataclose[0])
        if sell_qty > 0:
            self.sell(size=sell_qty)
            self.log(f'SELL, {self.dataclose[0]:,.2f}, {sell_qty}')
            my_account_holding.release_holding(sell_qty)

    # def notify_order(self, order):
    #     curdtstr = self.data.datetime.datetime().strftime('%a %Y-%m-%d %H:%M:%S')
    #     if order.status in [order.Completed] or True:
    #         if order.isbuy():
    #             if order.executed.dt is not None:
    #                 dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
    #                 self.logger.log('{}: BUY  EXECUTED, on: {}, qty {}'.format(curdtstr, dtstr, order.size))
    #                 self.order = None
    #             else:
    #                 dtstr = bt.num2date(order.created.dt).strftime('%a %Y-%m-%d %H:%M:%S')
    #                 #self.logger.log('{}: BUY {}, on: {}, dt {}'.format(curdtstr, order.getstatusname(), dtstr, order.created.dt))
    #         else:
    #             if order.executed.dt is not None:  # Sell
    #                 dtstr = bt.num2date(order.executed.dt).strftime('%a %Y-%m-%d %H:%M:%S')
    #                 self.logger.log('{}: SELL  EXECUTED, on: {}, qty: {}'.format(curdtstr, dtstr, order.size))
            

    def log_data(self):
        text = '{}, O:{}, H:{}, L:{}, C:{}, V:{}'.format(
            str(self.data.datetime.datetime()), str(
                self.data.open[0]), str(self.data.high[0]),
            str(self.data.low[0]), str(self.data.close[0]), str(self.data.volume[0]))
        print(text)

def run_main():
    global ticker, last_n_years, initial_cash, max_lots, my_account_holding, dip_percentage, target_profit_percentage

    parser = argparse.ArgumentParser()
    parser.add_argument('--td', type=float, required=False, help="Sell target price percent", nargs='?', const=1.01)
    parser.add_argument('--tp', type=float, required=False, help="Sell dip price percent", nargs='?', const=0.98)
    parser.add_argument('--cash', type=int, required=False, help="Money allocated for this strategy", nargs='?', const=100000)
    parser.add_argument('--lots', type=int, required=False, help="Max lots from allocated cash.", nargs='?', const=5)
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
    if args.td:
        dip_percentage = args.td
    if args.tp:
        target_profit_percentage = args.tp
    show_chart = args.chart
    if args.lots:
        print(f'ml: {args.lots}')
        max_lots = args.lots
    print(max_lots)


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

    my_account_holding = AccountHolding()


    # Create a cerebro entity - think of it is as your Car's Engine
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(initial_cash)
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

    # print(cerebro.broker.getposition(data))

    print(f"""Ticker: {ticker}, Initial Cash: {initial_cash:,.2f}, \
Final Value: {cerebro.broker.get_value():,.2f}, Quantity: {cerebro.broker.getposition(data).size}, \
ClosePrice: {final_close_price:,.2f}, Cash In hand: {cerebro.broker.get_cash():,.2f}""")

    # # Plotting a chart
    if show_chart:
        cerebro.plot(style='bar', numfigs=1, volume=True)

run_main()