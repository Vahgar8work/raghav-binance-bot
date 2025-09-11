
"""
Stop-Limit Orders command line interface.
Usage: python stop_limit_orders.py SYMBOL SIDE QUANTITY STOP_PRICE LIMIT_PRICE
Example: python stop_limit_orders.py BTCUSDT BUY 0.02 27000 26980
"""
import sys
import os
from binance.client import Client
from logger_config import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

def create_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError("API keys must be set")

    return Client(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True
    )

def stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    client = create_client()
    logger.info(f'Placing stop-limit order: {side} {quantity} {symbol} stop={stop_price} limit={limit_price}')

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price,
            type='STOP',
            timeInForce='GTC'
        )
        logger.info(f"Stop-limit order successful: {order}")
        print(f"Stop-limit order placed: {side} {quantity} {symbol}")
        print(f"Order ID: {order.get('orderId', 'N/A')}")
        return order
    except Exception as e:
        logger.error(f"Stop-limit order failed: {e}")
        print(f"Stop-limit order failed: {e}")
        raise

def main():
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)

    _, symbol, side, quantity, stop_price, limit_price = sys.argv
    try:
        stop_limit_order(symbol, side.upper(), float(quantity), float(stop_price), float(limit_price))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
