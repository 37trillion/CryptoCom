import ccxt

# Create an instance of the Crypto.com exchange
exchange = ccxt.cryptocom()

def fetch_tickers():
    tickers = exchange.fetch_tickers()
    return tickers

def fetch_order_book(symbol, limit=None):
    order_book = exchange.fetch_order_book(symbol, limit)
    return order_book

def fetch_trades(symbol, limit=None):
    trades = exchange.fetch_trades(symbol, limit)
    return trades

def fetch_ohlcv(symbol, timeframe='1d', since=None, limit=None):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    return ohlcv

def fetch_currencies():
    currencies = exchange.fetch_currencies()
    return currencies

def fetch_markets():
    markets = exchange.fetch_markets()
    return markets
