import threading
from app import TraderBot
from multiprocessing.pool import ThreadPool

if __name__ == '__main__':
    #  Set up trading pair, sym=Coin symbol
    trade_sym = 'MBOXUSDT'
    balance_sym = 'MBOX'
    trade1 = TraderBot(trade_sym, balance_sym)

    trade_sym = 'BNBUSDT'
    balance_sym = 'BNB'
    trade2 = TraderBot(trade_sym, balance_sym)

    trade1.start_run()
    trade2.start_run()
    while True:
        pass
