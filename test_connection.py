
"""
Test Binance API connection using python-binance.
"""
import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            print("API keys not found in .env file")
            return False

        print("API keys loaded successfully")

        client = Client(api_key, api_secret, testnet=True)

        account = client.futures_account()
        print("Connection successful")
        print(f"Account balance: {account.get('totalWalletBalance', 'N/A')} USDT")

        ticker = client.futures_symbol_ticker(symbol="BTCUSDT")
        print(f"BTCUSDT Price: {ticker.get('price', 'N/A')}")

        stats = client.futures_ticker(symbol="BTCUSDT")
        print(f"24hr Change: {stats.get('priceChangePercent', 'N/A')}%")

        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
