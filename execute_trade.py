import random
import time
import ccxt
import logging
import talib
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create an instance of the Crypto.com exchange
exchange = ccxt.cryptocom({
    'apiKey': 'Your Api Key',
    'secret': 'Your Secret ApiKey',
    'password': 'YOUR_API_PASSWORD',
    # Additional exchange-specific options if needed
})


def calculate_sma(symbol, timeframe, period):
    # Get the OHLCV data for the specified symbol and timeframe
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=period)

    # Extract the closing prices from the OHLCV data
    close_prices = [candle[4] for candle in ohlcv]

    # Calculate the simple moving average (SMA) for the closing prices
    sma = sum(close_prices) / len(close_prices)

    return sma


def calculate_rsi(symbol, timeframe, period):
    # Get the OHLCV data for the specified symbol and timeframe
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=period)

    # Extract the closing prices from the OHLCV data
    close_prices = np.array([candle[4] for candle in ohlcv])

    # Calculate the RSI using the closing prices
    rsi = talib.RSI(close_prices, timeperiod=period)

    return rsi[-1]  # Get the latest RSI value


def execute_trade():
    # Get the list of available trading pairs
    markets = exchange.load_markets()

    for symbol in markets:
        try:
            # Get the latest ticker data
            ticker = exchange.fetch_ticker(symbol)
            logger.info(f"Ticker data for {symbol}: {ticker}")

            current_price = ticker['close']
            buy_price = current_price

            # Calculate sell prices
            sell_price_1 = buy_price * 1.01  # 1% higher than buy price
            sell_price_2 = buy_price * 1.011  # 1.1% higher than buy price

            # Calculate stop loss and take profit prices
            stop_loss_price = buy_price * 0.9991  # 0.09% lower than buy price
            take_profit_price = buy_price * 1.013  # 1.3% higher than buy price

            # Check candlestick market data
            candle_data = exchange.fetch_ohlcv(symbol, '1m', limit=2)  # Fetch last 2 candles
            current_candle = candle_data[-1]
            previous_candle = candle_data[-2]

            # Check buy condition based on candlestick market data
            if current_candle[1] > previous_candle[4]:  # If current candle opens higher than the previous candle's close
                # Generate random amounts for buy and sell
                buy_amount = random.uniform(0.00001, 100000.1)  # Random amount between 0.00001 and 100000.1
                sell_amount_1 = random.uniform(0.00001, 100000.1)
                sell_amount_2 = random.uniform(0.00001, 100000.1)

                # Place a market buy order with the random buy amount
                buy_order = exchange.create_market_buy_order(symbol, buy_amount)
                logger.info(f"Buy order placed for {symbol} at market price: {buy_order}")

                # Place sell orders at specified prices with random sell amounts
                sell_order_1 = exchange.create_limit_sell_order(symbol, sell_amount_1, sell_price_1)
                logger.info(f"Sell order placed for {symbol} at price: {sell_price_1}")
                sell_order_2 = exchange.create_limit_sell_order(symbol, sell_amount_2, sell_price_2)
                logger.info(f"Sell order placed for {symbol} at price: {sell_price_2}")

                # Set stop loss and take profit prices
                exchange.create_order(
                    symbol,
                    'stop',
                    'sell',
                    sell_amount_1,
                    stopPrice=stop_loss_price,
                    price=buy_price,
                    params={'stopLoss': True}
                )
                logger.info(f"Stop loss order placed for {symbol} at price: {stop_loss_price}")
                exchange.create_order(
                    symbol,
                    'limit',
                    'sell',
                    sell_amount_2,
                    price=take_profit_price,
                    params={'takeProfit': True}
                )
                logger.info(f"Take profit order placed for {symbol} at price: {take_profit_price}")

        except ccxt.InsufficientFunds as e:
            logger.info(f"Insufficient funds for {symbol}. Skipping to the next trading pair.")

        except ccxt.BaseError as e:
            if "symbol" in str(e).lower():
                logger.info(f"Invalid symbol ({symbol}). Skipping to the next trading pair.")
            else:
                logger.info(f"An error occurred for {symbol}. Skipping to the next trading pair.")

        except Exception as e:
            logger.info(f"An error occurred: {str(e)}")

        time.sleep(1)

# Run the execute_trade() function indefinitely
while True:
    try:
        execute_trade()
    except Exception as e:
        logger.info(f"An error occurred: {str(e)}")

    time.sleep(300)  # 5 minutes interval

