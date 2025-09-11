# Binance Futures Order Bot

## Overview
This project is a CLI-based trading bot for Binance USDT-M Futures supporting multiple order types including Market, Limit, and advanced orders like Stop-Limit, OCO, TWAP, and Grid Orders.

## Features
- Market and Limit Orders
- Advanced Orders: Stop-Limit, OCO, TWAP, Grid
- Input validation and structured logging

## Setup Instructions
1. Install Python 3.8+.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set Binance API keys as environment variables:
   ```bash
   export BINANCE_API_KEY='your_api_key'
   export BINANCE_API_SECRET='your_api_secret'
   ```

## Usage
Example commands:

- Market Order:
  ```
  python src/market_orders.py BTCUSDT BUY 0.01
  ```

- Limit Order:
  ```
  python src/limit_orders.py BTCUSDT SELL 0.01 30000
  ```

- OCO Order:
  ```
  python src/advanced/oco.py BTCUSDT 0.01 35000 29000
  ```

- TWAP Order:
  ```
  python src/advanced/twap.py BTCUSDT BUY 1 5 60
  ```

- Grid Orders:
  ```
  python src/advanced/grid_orders.py BTCUSDT BUY 0.01 28000 35000 10
  ```

## Logging
All actions, API calls, errors, and order executions are logged in `src/bot.log`.

## Notes
- Replace placeholders with real Binance Futures API integration.
- Implement Stop-Limit order logic as needed.
