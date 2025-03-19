# test_backtrader.py
from datetime import datetime, timedelta

from src.utils.config import load_config
from src.utils.logger import Logger


def test_backtrader():
    """Test de Backtrader integratie met de Turtle strategie"""
    # Configuratie laden
    import os

    config_path = os.path.join(os.path.dirname(__file__), "config", "settings.json")
    config = load_config(config_path)

    # Logger aanmaken
    os.makedirs("logs", exist_ok=True)
    logger = Logger("logs/backtrader_test.log")
    logger.log_info("Start Backtrader test")

    # Maak een directory voor testdata
    os.makedirs("data", exist_ok=True)

    try:
        # Import backtrader component
        from src.analysis.backtrader_integration import BacktestingManager

        # Maak backtesting manager
        manager = BacktestingManager(config, logger)

        # Voer een eenvoudige backtest uit
        results = manager.run_backtest(
            strategy_name="turtle",
            symbols=["EURUSD"],
            start_date=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            timeframe="D1",
            plot_results=True,
        )

        # Print resultaten
        print("\nBacktest Results:")
        print(f"Profit: {results.get('profit_percentage', 0):.2f}%")
        print(f"Total Trades: {results.get('total_trades', 0)}")
        print(f"Win Rate: {results.get('win_rate', 0):.2f}%")

        logger.log_info("Backtrader test succesvol")
        return True

    except Exception as e:
        logger.log_info(f"Error in Backtrader test: {str(e)}", level="ERROR")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_backtrader()
    print(f"\nTest {'succeeded' if success else 'failed'}")
