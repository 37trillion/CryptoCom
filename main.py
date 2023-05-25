import time
import ccxt
import logging
import talib
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create an instance of the Crypto.com exchange
exchange = ccxt.cryptocom({
    'apiKey': 'Your ApiKey',
    'secret': 'Your Secret ApiKey',
    # 'password': 'YOUR_API_PASSWORD',
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
            logging.info(f"Ticker data for {symbol}: {ticker}")

            current_price = ticker['close']
            buy_price = current_price

            # Calculate sell prices
            sell_prices = [buy_price * (1 + percentage) for percentage in [0.01, 0.02, 0.03]]  # Define multiple sell price levels

            # Calculate stop loss and take profit prices
            stop_loss_price = buy_price * 0.99  # 1% lower than buy price
            take_profit_prices = [buy_price * (1 + percentage) for percentage in [0.01, 0.02, 0.03]]  # Define multiple take profit levels

            # Check candlestick market data
            candle_data = exchange.fetch_ohlcv(symbol, '1m', limit=2)  # Fetch last 2 candles
            current_candle = candle_data[-1]
            previous_candle = candle_data[-2]

            # Check buy condition based on candlestick market data
            if current_candle[1] > previous_candle[4]:  # If current candle opens higher than the previous candle's close
                # Fetch account balance
                balance = exchange.fetch_balance()
                available_funds = balance['total']['USDT']  # Assuming your base currency is USDT

                # Calculate dynamic buy amount based on available funds
                buy_amount = available_funds * 0.15  # 1% of available funds

                # Generate random sell amounts within a certain range
                sell_amounts = [np.random.uniform(0.00001, 100000, buy_amount) for _ in range(len(sell_prices))]

                # Place a market buy order with the dynamic buy amount
                buy_order = exchange.create_market_buy_order(symbol, buy_amount)
                logging.info(f"Buy order placed for {symbol} at market price: {buy_order}")

                # Place sell orders at specified prices with random sell amounts
                for sell_price, sell_amount in zip(sell_prices, sell_amounts):
                    sell_order = exchange.create_limit_sell_order(symbol, sell_amount, sell_price)
                    logging.info(f"Sell order placed for {symbol} at price: {sell_price}")

                # Set stop loss and take profit orders
                for take_profit_price in take_profit_prices:
                    exchange.create_order(
                        symbol,
                        'limit',
                        'sell',
                        buy_amount,
                        price=take_profit_price,
                        params={'takeProfit': True}
                    )
                    logging.info(f"Take profit order placed for {symbol} at price: {take_profit_price}")

                exchange.create_order(
                    symbol,
                    'stop',
                    'sell',
                    buy_amount,
                    stopPrice=stop_loss_price,
                    params={'stopLoss': True}
                )
                logging.info(f"Stop loss order placed for {symbol} at price: {stop_loss_price}")

        except ccxt.InsufficientFunds as e:
            logging.info(f"Insufficient funds for {symbol}. Skipping to the next trading pair.")

        except ccxt.BaseError as e:
            if "symbol" in str(e).lower():
                logging.info(f"Invalid symbol ({symbol}). Skipping to the next trading pair.")
            else:
                logging.info(f"An error occurred for {symbol}. Skipping to the next trading pair.")

        except Exception as e:
            logging.info(f"An error occurred: {str(e)}")

        time.sleep(1)

# Run the execute_trade() function indefinitely
while True:
    try:
        execute_trade()
    except Exception as e:
        logging.info(f"An error occurred: {str(e)}")

    time.sleep(300)  # 5 minutes interval

