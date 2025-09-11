"""
OCO Orders command line interface.
Usage: python advanced/oco.py SYMBOL QUANTITY TAKE_PROFIT_PRICE STOP_LOSS_PRICE
Example: python advanced/oco.py BTCUSDT 0.05 35000 29000
"""
import sys
import os
import pathlib

# Add src directory to Python path
src_path = pathlib.Path(__file__).parent.parent.resolve()
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from binance.client import Client
from logger_config import get_logger  # Now this works!
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

def oco_order(symbol, quantity, take_profit_price, stop_loss_price):
    client = create_client()
    logger.info(f'Placing OCO order: {quantity} {symbol} TP {take_profit_price}, SL {stop_loss_price}')
    
    try:
        tp_order = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='LIMIT',
            quantity=quantity,
            price=take_profit_price,
            timeInForce='GTC'
        )
        sl_order = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_loss_price
        )
        logger.info(f"OCO orders successful - TP: {tp_order.get('orderId', 'N/A')}, SL: {sl_order.get('orderId', 'N/A')}")
        print(f"OCO orders placed for {quantity} {symbol} TP {take_profit_price}, SL {stop_loss_price}")
        return {'take_profit': tp_order, 'stop_loss': sl_order}
    except Exception as e:
        logger.error(f"OCO order failed: {e}")
        print(f"OCO order failed: {e}")
        raise

def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    
    _, symbol, quantity, tp_price, sl_price = sys.argv
    try:
        oco_order(symbol, float(quantity), float(tp_price), float(sl_price))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
