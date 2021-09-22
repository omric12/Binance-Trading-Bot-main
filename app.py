import time
from time import sleep

from pair import Pair

# Todo ADD PROFIT

# VARIABLES
# API KEY, get from your account on binance and set at .env file

#  Set up trading pair, sym=Coin symbol
trade_sym = 'BNBUSDT'
balance_sym = 'BNB'

# Trade initializer
pair = Pair()
pair.connect()
pair.initializer(trade_sym, balance_sym)
topValue = 2
vtopValue = topValue
floorValue = -1.4
vfloorValue = floorValue
# if starting from USDT set to False, if starting from BNB set to True
# trade = pair.is_buyer(trade_sym)

# counters for buy and sell
bought = 0
sold = 0

# balance = pair.set_qty(balance_sym)

# GET INITIAL PRICE
# for fixed price, insert number
# startPrice = pair.last_trade(trade_sym)
print('start price is %s' % pair.startPrice)
total = 0
x = 0
y = 0
z = 0

# price tracker
up_high = pair.startPrice

is_high = False
is_low = False

while True:  # -----  MAIN LOOP --------

    try:
        # Get current price
        current_price = pair.get_current_price()  # current
        print("Current price is %s" % current_price)  # print(f"current price is {correctPrice}")

        while not pair.trade:  # -------- WAITING TO BUY-------
            sleep(1)
            current_price = pair.get_current_price()  # Current
            # GOES UP      HOLDING USDT
            if current_price - pair.startPrice >= 0:  # sold and price went up
                print(f"waiting for price to go down ", current_price, "bought", bought, "sold ", sold, "total ", total,
                      "low ", floorValue, "high ", topValue)
            else:  # sold and price went down
                if current_price - pair.startPrice <= floorValue:  # lower than floorValue
                    current_price = pair.get_current_price()
                    up_high = current_price
                    floorValue = current_price - pair.startPrice
                    print('GOING DOWN!! ', current_price, "bought", bought, "sold ", sold, "total ", total, "low ",
                          floorValue, "high ", topValue)
                    print('new lowValue price: ', floorValue)
                    is_low = True
                # not of the while
                # <0
                else:
                    print("waiting for price to go down ", current_price, "bought", bought, "sold ", sold, "total ",
                          total,
                          "low ", floorValue, "high ", topValue)
                    if up_high - current_price > 0.15 * floorValue and is_low is True:
                        bought += 1
                        # --------SET ORDER TO BUY--------
                        pair.buy(0.4)
                        print("******************************************************")
                        print('B %s' % bought)
                        sleep(1)
                        pair.startPrice = pair.last_trade()
                        print("BOUGHT!!!!! ", pair.startPrice)
                        print("******************************************************")
                        floorValue = vfloorValue
                        pair.trade = True
                        is_low = False

        while pair.trade:  # ------ WAITING FOR SELL--------
            current_price = pair.get_current_price()  # current
            if current_price <= pair.startPrice:  # bought and price went down
                print("waiting for price to go up ", current_price, "bought", bought, "sold ", sold, "total ", total,
                      "low ",
                      floorValue, "high ", topValue)
            else:  # bought and price went up
                if (current_price - pair.startPrice >= topValue) and (is_high is False):
                    current_price = pair.get_current_price()
                    up_high = current_price
                    topValue = current_price - pair.startPrice
                    print('GOING UP!! ', current_price, "bought", bought, "sold ", sold, "total ", total, "low ",
                          floorValue,
                          "high ", topValue)
                    print('new upHigh price: ', up_high)
                    is_high = True
                else:
                    print("waiting for price to go up ", current_price, "bought", bought, "sold ", sold, "total ",
                          total,
                          "low ", floorValue, "high ", topValue)
                    if up_high - current_price > 0.15 * topValue and (is_high is True):
                        sold += 1
                        # --------SET ORDER TO SELL--------
                        pair.sell(0.4)
                        print("******************************************************")
                        print('S %s' % sold)
                        sleep(1)
                        pair.startPrice = pair.last_trade()
                        print("SOLD!!!!! ", pair.startPrice)
                        print("******************************************************")
                        topValue = vtopValue
                        x = pair.total(trade_sym, 1)
                        y = pair.total(trade_sym, 2)
                        z = x - y
                        total += z
                        pair.trade = False
                        is_high = False

    except Exception as e:
        print("********Error Occurred********")
        print(e)
        time.sleep(10)
