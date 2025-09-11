
"""
Comprehensive test cases for all Binance Futures order types.
Tests both individual scripts and unified CLI.
"""
import subprocess
import time

commands = [
    # Individual scripts
    "python src/market_orders.py BTCUSDT BUY 0.001",
    "python src/limit_orders.py BTCUSDT BUY 0.001 114000",
    "python src/stop_limit_orders.py BTCUSDT BUY 0.001 114100 114000",
    "python src/advanced/oco.py BTCUSDT 0.001 115000 113000",
    "python src/advanced/twap.py BTCUSDT BUY 0.005 5 2",
    "python src/advanced/grid_orders.py BTCUSDT BUY 0.001 112000 116000 5",

    # Unified CLI
    "python src/bot_main.py market BTCUSDT BUY 0.001",
    "python src/bot_main.py limit BTCUSDT BUY 0.001 114000",
    "python src/bot_main.py stop BTCUSDT BUY 0.001 114100 114000",
    "python src/bot_main.py oco BTCUSDT 0.001 115000 113000",
    "python src/bot_main.py twap BTCUSDT BUY 0.005 5 2",
    "python src/bot_main.py grid BTCUSDT BUY 0.001 112000 116000 5",
]

def run_tests():
    pass_count = 0
    fail_count = 0
    for cmd in commands:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        if result.returncode == 0:
            print("Test PASSED")
            pass_count += 1
        else:
            print("Test FAILED")
            fail_count += 1
        print("-"*60)
        time.sleep(1)  # brief pause
    print(f"All tests completed. Passed: {pass_count}, Failed: {fail_count}")

if __name__ == "__main__":
    run_tests()
