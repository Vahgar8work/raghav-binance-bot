
"""
Market Orders command line interface.
Usage: python market_orders.py SYMBOL SIDE QUANTITY
Example: python market_orders.py BTCUSDT BUY 0.01
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

def market_order(symbol, side, quantity):
    client = create_client()
    logger.info(f'Placing market order: {side} {quantity} {symbol}')

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        logger.info(f"Market order successful: {order}")
        print(f"Market order placed: {side} {quantity} {symbol}")
        print(f"Order ID: {order.get('orderId', 'N/A')}")
        return order
    except Exception as e:
        logger.error(f"Market order failed: {e}")
        print(f"Market order failed: {e}")
        raise

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    _, symbol, side, quantity = sys.argv
    try:
        market_order(symbol, side.upper(), float(quantity))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
