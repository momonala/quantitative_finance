from trades import Investor

for stock in ['fb', 'aapl', 'amzn', 'goog', 'tsla',
              'nvda', 'msft', 'ford', 'lulu', 'yelp']:
    me = Investor(5000, verbose=False)
    me.trade(stock, -1., 2.5, plot=False)
