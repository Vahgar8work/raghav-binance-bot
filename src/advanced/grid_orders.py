"""
Grid Orders command line interface.
Usage: python advanced/grid_orders.py SYMBOL SIDE QUANTITY LOWER_PRICE UPPER_PRICE GRID_LEVELS
Example: python advanced/grid_orders.py BTCUSDT BUY 0.01 28000 35000 10
"""
import sys
import os
import pathlib

# Add src directory to Python path
src_path = pathlib.Path(__file__).parent.parent.resolve()
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

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

def grid_orders(symbol, side, quantity, lower_price, upper_price, grid_levels):
    client = create_client()

    if lower_price >= upper_price:
        raise ValueError("Lower price must be less than upper price")
    if grid_levels <= 0:
        raise ValueError("Grid levels must be positive")

    price_step = (upper_price - lower_price) / (grid_levels - 1) if grid_levels > 1 else 0

    logger.info(f'Placing grid orders: {grid_levels} orders between {lower_price} and {upper_price}')

    try:
        for i in range(grid_levels):
            price = lower_price + (i * price_step)
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=round(price, 2),
                timeInForce='GTC'
            )
            logger.info(f"Grid order {i+1}/{grid_levels} placed at {price}: {order.get('orderId', 'N/A')}")
            print(f"Grid order {i+1}/{grid_levels}: {side} {quantity} {symbol} at {price}")
    except Exception as e:
        logger.error(f"Grid order failed: {e}")
        print(f"Grid order failed: {e}")
        raise

def main():
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)
    
    _, symbol, side, quantity, lower_price, upper_price, grid_levels = sys.argv
    try:
        grid_orders(symbol, side.upper(), float(quantity), float(lower_price), float(upper_price), int(grid_levels))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
