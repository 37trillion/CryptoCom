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

# Additional functions

def fetch_symbol_info(symbol):
    symbol_info = exchange.fetch_symbol_info(symbol)
    return symbol_info

def fetch_trading_limits(symbol):
    trading_limits = exchange.fetch_trading_limits(symbol)
    return trading_limits

def fetch_trading_pairs():
    trading_pairs = exchange.fetch_trading_pairs()
    return trading_pairs

def fetch_exchange_info():
    exchange_info = exchange.fetch_exchange_info()
    return exchange_info

