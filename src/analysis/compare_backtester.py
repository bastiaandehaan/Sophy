# scripts/compare_backtester.py
import argparse
import json
import os
from datetime import datetime

from src.analysis.backtrader_integration import BacktestingManager
from src.utils.config import load_config
from src.utils.logger import Logger


def main():
    """
    Run a comparative backtest between the Advanced Backtester and Backtrader.
    """
    parser = argparse.ArgumentParser(description="Compare backtesters")
    parser.add_argument("--strategy", type=str, default="turtle", help="Strategy name")
    parser.add_argument(
        "--symbols", type=str, default="EURUSD", help="Comma-separated symbols"
    )
    parser.add_argument(
        "--start_date", type=str, default="2022-01-01", help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end_date", type=str, default="2022-12-31", help="End date (YYYY-MM-DD)"
    )
    parser.add_argument("--timeframe", type=str, default="D1", help="Timeframe")
    parser.add_argument(
        "--config", type=str, default="config/settings.json", help="Config file path"
    )

    args = parser.parse_args()

    # Setup
    config = load_config(args.config)
    logger = Logger(
        config.get("logging", {}).get("log_file", "logs/compare_backtest.log")
    )

    logger.log_info("Starting backtest comparison")

    # Create backtesting manager
    backtesting_manager = BacktestingManager(config, logger)

    # Run comparison
    symbols = args.symbols.split(",")

    results = backtesting_manager.run_backtest(
        strategy_name=args.strategy,
        symbols=symbols,
        start_date=args.start_date,
        end_date=args.end_date,
        timeframe=args.timeframe,
        plot_results=True,
        engine="both",
    )

    # Save comparison results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = config.get("output", {}).get(
        "backtest_results_dir", "backtest_results"
    )
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir, f"backtest_comparison_{args.strategy}_{timestamp}.json"
    )

    with open(output_path, "w") as f:
        json.dump(results["comparison"], f, indent=4)

    # Print summary
    print("\n=== Backtest Comparison Summary ===")
    print(f"Strategy: {args.strategy}")
    print(f"Symbols: {args.symbols}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Timeframe: {args.timeframe}")
    print("\nMetrics Comparison:")

    adv_profit = results["advanced"]["profit_percentage"]
    bt_profit = results["backtrader"]["profit_percentage"]
    print(f"Profit %: Advanced={adv_profit:.2f}%, Backtrader={bt_profit:.2f}%")

    adv_trades = results["advanced"]["total_trades"]
    bt_trades = results["backtrader"]["total_trades"]
    print(f"Total Trades: Advanced={adv_trades}, Backtrader={bt_trades}")

    consistency = results["comparison"]["consistency_score"] * 100
    print(f"\nConsistency Score: {consistency:.2f}%")

    if consistency > 80:
        print("✅ Results are consistent between systems")
    else:
        print("⚠️ Significant differences detected")

    print(f"\nDetailed comparison saved to: {output_path}")


if __name__ == "__main__":
    main()
