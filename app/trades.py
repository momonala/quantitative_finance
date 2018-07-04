import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_stock_data(ticker):
    ''' get data from web directly'''
    start = datetime.datetime(2012, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(ticker, 'morningstar', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df = df.drop("Symbol", axis=1)
    df.name = ticker
    return df.Close


def compute_band(s, factor, window):
    '''compute a bollinger band'''
    mean_ = s.rolling(window).mean()
    std_ = s.rolling(window).std()
    return mean_ + std_*factor


def get_df(ticker, low=-2.5, high=2.5, plot=False):
    # get stock and bollinger banks
    stock = get_stock_data(ticker)
    low_band = compute_band(stock, low, 100)
    up_band = compute_band(stock, high, 100)
    # mean_band = compute_band(stock, 0, 100)

    # build dataframe
    df = pd.DataFrame([stock, low_band, up_band], index=['stock', 'low', 'high']).T
    df['buy'] = df.stock < df.low
    df['sell'] = df.stock > df.high

    if plot:
        sells = stock[stock > up_band]
        sells.name = 'sells'
        buys = stock[stock < low_band]
        buys.name = 'buys'

        plt.figure(figsize=(15, 4))
        plt.title(ticker)
        plt.xlabel('time')
        plt.ylabel('price')

        stock.plot(c=[0, 0, 0, 0.7])
        df.low.plot(c=[0, .9, .1, 0.3])
        df.high.plot(c=[.9, 0, .1, 0.3])
        df.stock.plot(c=[0, 0, 0, 0.2])

        SIZE = 15
        plt.scatter(sells.index, sells, c='r', s=SIZE)
        plt.scatter(buys.index, buys, c='g', s=SIZE)

        plt.legend()
        plt.show()
    return df


class Investor:
    def __init__(self, prinical=1000, verbose=False):
        self.is_holding = False
        self.cash = prinical
        self.total_profit = 0
        self.holdings = 0
        self.n_stocks = 0

        self.stock_data = None
        self.state = None

        self.verbose = verbose

    def buy(self, price):
        assert self.is_holding is False
        self.is_holding = True

        self.n_stocks = np.floor(self.cash / price)
        self.holdings = self.n_stocks * price
        if self.verbose:
            print(str(self.state.name))
            print('bought {} stocks at ${}'.format(self.n_stocks, price))
            print('holding: ${:0.2f}\n'.format(self.holdings))

    def sell(self, price):
        assert self.is_holding is True
        self.is_holding = False

        sell_value = self.n_stocks * price
        profit = sell_value - self.holdings
        self.cash += profit
        self.total_profit += profit
        self.holdings -= profit

        if self.verbose:
            print(str(self.state.name))
            print('sold {} stocks at ${}'.format(self.n_stocks, price))
            print('sell value: ${:0.2f} profit ${:0.2f}\n'.format(sell_value, profit))
        self.n_stocks = 0

    def trade(self, stock, low, high, plot):
        self.stock_data = get_df(stock, low, high, plot)
        trading_days = self.stock_data.shape[0]

        for day in range(trading_days):
            self.state = self.stock_data.iloc[day]
            price = self.state['stock']

            if self.state['buy'] == True and self.is_holding == False:
                self.buy(price)
            if self.state['sell'] == True and self.is_holding == True:
                self.sell(price)
        print('{} profit: {:0.2f}'.format(stock, self.total_profit))
