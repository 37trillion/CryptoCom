import random
import time
import ccxt

# Create an instance of the Crypto.com exchange
exchange = ccxt.cryptocom({

    # Additional exchange-specific options if needed
})

# Dictionary to store trailing stop loss values for each symbol
trailing_stop_loss = {}

def execute_trade():
    # Get the list of available trading pairs
    markets = exchange.load_markets()

    for symbol in markets:
        try:
            # Get the latest ticker data
            ticker = exchange.fetch_ticker(symbol)

            # Calculate buy price and set the buy amount
            buy_price = ticker['close'] * 0.9972  # 0.45% below market price
            buy_amount = random.uniform(0.0000250, 1000)  # Random amount between 0.0000250 and 100000

            # Place a market buy order
            buy_order = exchange.create_limit_buy_order(symbol, buy_amount, buy_price)
            print(f"Buy order placed for {symbol} at {buy_price}: {buy_order}")

            # Update trailing stop loss value for the symbol
            trailing_stop_loss[symbol] = buy_price * 0.995  # 0.50% below buy value

            # Place a sell order when the price is 0.99% higher than the buy price
            if ticker['close'] >= buy_price * 1.0099:
                sell_order = exchange.create_market_sell_order(symbol, buy_amount)
                print(f"Sell order placed for {symbol} at market price: {sell_order}")

            # Check if the price is higher than the trailing stop loss value
            if ticker['close'] > trailing_stop_loss[symbol]:
                # Update the trailing stop loss value
                trailing_stop_loss[symbol] = ticker['close'] * 0.995  # 0.50% below the current price

                # Place a sell order at the updated trailing stop loss value
                sell_order = exchange.create_limit_sell_order(symbol, buy_amount, trailing_stop_loss[symbol])
                print(f"Trailing stop loss order placed for {symbol} at {trailing_stop_loss[symbol]}: {sell_order}")

            # Check if there's insufficient balance for the symbol
        except ccxt.InsufficientFunds as e:
            print(f"Insufficient funds for {symbol}. Skipping to the next trading pair.")

        # Handle invalid symbols or other exchange-related errors
        except ccxt.BaseError as e:
            if "symbol" in str(e).lower():
                print(f"Invalid symbol ({symbol}). Skipping to the next trading pair.")
            else:
                print(f"An error occurred for {symbol}. Skipping to the next trading pair.")

        # Wait for a short interval before processing the next trading pair
        time.sleep(1)

# Run the execute_trade() function indefinitely
while True:
    try:
        execute_trade()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Wait for a certain interval before executing the trades again
    time.sleep(60)  # Update the interval as per your requirement
