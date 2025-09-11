"""
TWAP Orders command line interface.
Usage: python advanced/twap.py SYMBOL SIDE TOTAL_QUANTITY PARTS INTERVAL_SECONDS
Example: python advanced/twap.py BTCUSDT BUY 1.0 10 30
"""
import sys
import time
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

def twap_order(symbol, side, total_quantity, parts, interval_sec):
    client = create_client()
    chunk_quantity = total_quantity / parts
    
    logger.info(f'Starting TWAP order: {total_quantity} {symbol} in {parts} parts every {interval_sec} seconds')
    
    try:
        for i in range(parts):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=round(chunk_quantity, 6)
            )
            logger.info(f"TWAP chunk {i+1}/{parts} executed: {order.get('orderId', 'N/A')}")
            print(f"TWAP chunk {i+1}/{parts} submitted: {chunk_quantity} {symbol}")
            if i < parts - 1:
                time.sleep(interval_sec)
    except Exception as e:
        logger.error(f"TWAP order failed at chunk {i+1}: {e}")
        print(f"TWAP order failed: {e}")
        raise

def main():
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)
    
    _, symbol, side, total_qty, parts, interval = sys.argv
    try:
        twap_order(symbol, side.upper(), float(total_qty), int(parts), int(interval))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
