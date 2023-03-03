import ccxt
import talib
import time

# Connect to the exchange
exchange = ccxt.binance()
symbol = 'BTC/USDT'

# Set up the RSI indicator
rsi_period = 14

# Set up the buy and sell thresholds
buy_threshold = 30
sell_threshold = 70

# Set up the initial balance and position
balance = exchange.fetch_balance()['USDT']
position = 0

while True:
    # Get the current Bitcoin price and RSI value
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    ohlcv = exchange.fetch_ohlcv(symbol, '1d')
    rsi = talib.RSI(ohlcv[:, 4], timeperiod=rsi_period)[-1]

    # Buy Bitcoin if the RSI dips below the buy threshold and we have enough USDT balance
    if rsi < buy_threshold and balance > 0:
        amount = balance / price
        exchange.create_market_buy_order(symbol, amount)
        position += amount
        balance = 0
        print('Bought', amount, 'Bitcoin at', price)

    # Sell Bitcoin if the RSI goes above the sell threshold and we have a position
    if rsi > sell_threshold and position > 0:
        amount = position
        exchange.create_market_sell_order(symbol, amount)
        balance += amount * price
        position = 0
        print('Sold', amount, 'Bitcoin at', price)

    # Sleep for 1 hour before checking again
    time.sleep(60 * 60)
