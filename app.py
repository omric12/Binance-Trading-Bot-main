import threading
import time
from pair import Pair
from time import sleep


# Todo ADD PROFIT

# VARIABLES
# API KEY, get from your account on binance and set at .env file


class TraderBot:
    def __init__(self, trade_sym, balance_sym):
        # Trade initializer
        self.pair = Pair()
        self.pair.connect()
        self.pair.initializer(trade_sym, balance_sym)
        self.topValue = 2
        self.vtopValue = self.topValue
        self.floorValue = -1.4
        self.vfloorValue = self.floorValue
        # if starting from USDT set to False, if starting from BNB set to True
        # counters for buy and sell
        self.bought = 0
        self.sold = 0
        # GET INITIAL PRICE
        # for fixed price, insert number
        # startPrice = pair.last_trade(trade_sym)
        print('start price is %s' % self.pair.startPrice)
        self.total = 0
        self.x = 0
        self.y = 0
        self.z = 0
        # price tracker
        self.up_high = self.pair.startPrice
        self.is_high = False
        self.is_low = False

    def start_run(self):
        print('***************************************************************')
        x = threading.Thread(target=self.main_function, daemon=True)
        x.start()

    def main_function(self):
        while True:  # -----  MAIN LOOP --------
            try:
                # Get current price
                current_price = self.pair.get_current_price()  # current
                print("Current price is %s" % current_price)  # print(f"current price is {correctPrice}")

                while not self.pair.trade:  # -------- WAITING TO BUY-------

                    current_price = self.pair.get_current_price()  # Current
                    # GOES UP      HOLDING USDT
                    if current_price - self.pair.startPrice >= 0:  # sold and price went up
                        print(threading.get_ident(), f"waiting for price to go down ", current_price, "bought",
                              self.bought, "sold ",
                              self.sold,
                              "total ",
                              self.total,
                              "low ", self.floorValue, "high ", self.topValue)
                    else:  # sold and price went down
                        if current_price - self.pair.startPrice <= self.floorValue:  # lower than floorValue
                            current_price = self.pair.get_current_price()
                            self.up_high = current_price
                            floorValue = current_price - self.pair.startPrice
                            print('GOING DOWN!! ', current_price, "bought", self.bought, "sold ", self.sold, "total ",
                                  self.total,
                                  "low ",
                                  floorValue, "high ", self.topValue)
                            print('new lowValue price: ', floorValue)
                            self.is_low = True
                        # not of the while
                        # <0
                        else:
                            print(threading.get_ident(), "waiting for price to go down ", current_price, "bought",
                                  self.bought, "sold ",
                                  self.sold,
                                  "total ",
                                  self.total,
                                  "low ", self.floorValue, "high ", self.topValue)
                            if self.up_high - current_price > 0.15 * self.floorValue and self.is_low is True:
                                self.bought += 1
                                # --------SET ORDER TO BUY--------
                                self.pair.buy(0.4)
                                print("******************************************************")
                                print('B %s' % self.bought)
                                sleep(1)
                                self.pair.startPrice = self.pair.last_trade()
                                print("BOUGHT!!!!! ", self.pair.startPrice)
                                print("******************************************************")
                                self.floorValue = vfloorValue
                                self.pair.trade = True
                                self.is_low = False

                while self.pair.trade:  # ------ WAITING FOR SELL--------
                    current_price = self.pair.get_current_price()  # current
                    if current_price <= self.pair.startPrice:  # bought and price went down
                        print(threading.get_ident(), "waiting for price to go up ", current_price, "bought",
                              self.bought, "sold ", self.sold,
                              "total ",
                              self.total,
                              "low ",
                              self.floorValue, "high ", self.topValue)
                    else:  # bought and price went up
                        if (current_price - self.pair.startPrice >= self.topValue) and (self.is_high is False):
                            current_price = self.pair.get_current_price()
                            up_high = current_price
                            topValue = current_price - self.pair.startPrice
                            print('GOING UP!! ', current_price, "bought", self.bought, "sold ", self.sold, "total ",
                                  self.total,
                                  "low ",
                                  self.floorValue,
                                  "high ", topValue)
                            print('new upHigh price: ', up_high)
                            self.is_high = True
                        else:
                            print(threading.get_ident(), "waiting for price to go up ", current_price, "bought",
                                  self.bought, "sold ",
                                  self.sold,
                                  "total ",
                                  self.total,
                                  "low ", self.floorValue, "high ", self.topValue)
                            if self.up_high - current_price > 0.15 * self.topValue and (self.is_high is True):
                                self.sold += 1
                                # --------SET ORDER TO SELL--------
                                self.pair.sell(0.4)
                                print("******************************************************")
                                print('S %s' % self.sold)
                                sleep(1)
                                self.pair.startPrice = self.pair.last_trade()
                                print("SOLD!!!!! ", self.pair.startPrice)
                                print("******************************************************")
                                self.topValue = vtopValue
                                x = self.pair.total(trade_sym, 1)
                                y = self.pair.total(trade_sym, 2)
                                z = x - y
                                self.total += z
                                self.pair.trade = False
                                self.is_high = False

            except Exception as e:
                print("********Error Occurred********")
                print(e)
                time.sleep(10)
