
"""
Limit Orders command line interface.
Usage: python limit_orders.py SYMBOL SIDE QUANTITY PRICE
Example: python limit_orders.py BTCUSDT BUY 0.01 30000
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

def limit_order(symbol, side, quantity, price):
    client = create_client()
    logger.info(f'Placing limit order: {side} {quantity} {symbol} at {price}')

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        logger.info(f"Limit order successful: {order}")
        print(f"Limit order placed: {side} {quantity} {symbol} at {price}")
        print(f"Order ID: {order.get('orderId', 'N/A')}")
        return order
    except Exception as e:
        logger.error(f"Limit order failed: {e}")
        print(f"Limit order failed: {e}")
        raise

def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)

    _, symbol, side, quantity, price = sys.argv
    try:
        limit_order(symbol, side.upper(), float(quantity), float(price))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
