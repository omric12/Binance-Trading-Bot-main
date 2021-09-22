import os

from binance.client import Client
from binance.enums import *
# Handling .env variables
from dotenv import load_dotenv

load_dotenv()


# API KEY, get from your account on binance and set at .env file


class Pair:
    def __init__(self):
        self.key1 = os.environ.get("public_api_key")
        self.key2 = os.environ.get("secret_api_key")
        self.client = None
        self.trade = None
        self.balance = None
        self.startPrice = None
        self.trade_sym = None
        self.balance_sym = None

    def connect(self):
        self.client = Client(self.key1, self.key2)

    def initializer(self, trade_sym, balance_sym):
        self.trade_sym = trade_sym
        self.balance_sym = balance_sym
        self.trade = self.is_buyer()
        self.balance = self.set_qty()
        self.startPrice = self.last_trade()

    def sell(self, qty):
        self.client.create_order(
            symbol=self.trade_sym,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            # timeInForce=TIME_IN_FORCE_GTC,
            quantity=qty,
            # price=set_current(sym='BNBUSDT'
        )

    def buy(self, qty):
        self.client.create_order(
            symbol=self.trade_sym,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            # timeInForce=TIME_IN_FORCE_GTC,
            quantity=qty,
            # price=set_current(sym='BNBUSDT'
        )

    # set current price
    def get_current_price(self):
        current = self.client.get_recent_trades(symbol=self.trade_sym)
        current_price = current[-1]
        current_price = current_price['price']
        current_price = float(current_price)
        return current_price

    # set balance of selected wallet
    def set_qty(self):
        balance = self.client.get_asset_balance(asset=self.balance_sym)
        balance = balance['free']
        balance = float(balance)
        balance *= 100
        balance = int(balance)
        balance = float(balance)
        balance *= 0.9
        balance /= 100
        return balance

    # set price of last trade
    def last_trade(self):
        trades = self.client.get_my_trades(symbol=self.trade_sym)
        trades = trades[-1]
        trades = trades['price']
        trades = float(trades)
        return trades

    # indicate is buyer or seller
    def is_buyer(self):
        buyer = self.client.get_my_trades(symbol=self.trade_sym)
        buyer = buyer[-1]
        buyer = buyer['isBuyer']
        return buyer

    # returns sub between trade[-1] and trade[-2]
    def total(self, sym, i):
        total_trade = self.client.get_my_trades(symbol=sym)
        total_trade = total_trade[-1 * i]
        total_trade = total_trade['quoteQty']
        total_trade = float(total_trade)
        return total_trade
