
"""
Unified CLI launcher.

Usage examples:
  python bot_main.py market BTCUSDT BUY 0.01
  python bot_main.py limit BTCUSDT SELL 0.01 30000
  python bot_main.py stop BTCUSDT BUY 0.01 27000 26950
  python bot_main.py oco BTCUSDT 0.01 35000 29000
  python bot_main.py twap BTCUSDT BUY 1.0 5 60
  python bot_main.py grid BTCUSDT BUY 0.01 28000 35000 10
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    order_type = sys.argv[1].lower()
    args = sys.argv[2:]

    script_map = {
        "market": "market_orders.py",
        "limit": "limit_orders.py",
        "stop": "stop_limit_orders.py",
        "oco": "advanced/oco.py",
        "twap": "advanced/twap.py",
        "grid": "advanced/grid_orders.py",
    }

    if order_type not in script_map:
        print(f"Unknown order type '{order_type}'. Available types: {list(script_map.keys())}")
        sys.exit(1)

    current_dir = Path(__file__).parent
    script_path = current_dir / script_map[order_type]

    if not script_path.exists():
        print(f"Script not found: {script_path}")
        sys.exit(1)

    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
