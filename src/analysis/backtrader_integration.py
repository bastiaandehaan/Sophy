# src/analysis/backtrader_integration.py
import os
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd

from src.analysis.advanced_backtester import Backtester
from src.analysis.backtrader_adapter import BacktraderAdapter


class BacktestingManager:
    """
    Integration manager that provides a unified interface to both backtesting systems.

    This allows for:
    1. Running tests on both systems to compare results
    2. Gradual migration to Backtrader as it proves reliable
    3. Using the appropriate engine based on the specific testing needs
    """

    def __init__(self, config: Dict[str, Any], logger):
        """
        Initialize both backtesting systems.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger

        # Initialize both engines
        self.advanced_backtester = Backtester(config, logger)
        self.backtrader_adapter = BacktraderAdapter(config, logger)

        # Default engine selection
        self.default_engine = "advanced"  # or "backtrader"

    def run_backtest(
        self,
        strategy_name: str,
        symbols: List[str],
        start_date: str,
        end_date: str,
        timeframe: str = "D1",
        parameters: Dict = None,
        plot_results: bool = True,
        engine: str = None,
    ) -> Dict[str, Any]:
        """
        Run a backtest with the specified engine.

        Args:
            strategy_name: Name of the strategy to test
            symbols: List of trading symbols
            start_date: Start date for the backtest (YYYY-MM-DD)
            end_date: End date for the backtest (YYYY-MM-DD)
            timeframe: Timeframe for the data
            parameters: Custom parameters for the strategy
            plot_results: Whether to generate plots
            engine: Which engine to use ("advanced", "backtrader", or "both")

        Returns:
            Dictionary with backtest results
        """
        # Determine which engine to use
        engine = engine or self.default_engine

        # Import strategy factory here to avoid circular imports
        from src.strategy.strategy_factory import StrategyFactory

        # Load the specified strategy
        strategy = StrategyFactory.create_strategy(
            strategy_name,
            connector=None,
            # Backtester will create mock connector
            risk_manager=None,  # Backtester will create mock risk manager
            logger=self.logger,
            config=self.config,
        )

        results = {}

        # Run with advanced backtester
        if engine in ["advanced", "both"]:
            self.logger.info(f"Running backtest with Advanced Backtester")
            results["advanced"] = self.advanced_backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                timeframe=timeframe,
                parameters=parameters,
                plot_results=plot_results,
            )

        # Run with backtrader
        if engine in ["backtrader", "both"]:
            self.logger.info(f"Running backtest with Backtrader")

            # Load data for each symbol
            for symbol in symbols:
                # Use the data loading mechanism from the advanced backtester
                data = self._load_historical_data(
                    symbol, start_date, end_date, timeframe
                )
                self.backtrader_adapter.add_data(symbol, data, timeframe)

            # Run backtest with backtrader
            results["backtrader"] = self.backtrader_adapter.run_backtest(
                strategy,
                debug=self.config.get("debug", False),
                risk_per_trade=self.config.get("risk", {}).get("risk_per_trade", 0.01),
            )

            if plot_results:
                # Generate backtrader plots
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                plot_path = os.path.join(
                    self.config.get("output", {}).get(
                        "backtest_results_dir", "backtest_results"
                    ),
                    f"{strategy_name}_backtrader_plot_{timestamp}.png",
                )
                self.backtrader_adapter.plot_results(plot_path)

        # If both engines were used, add comparison metrics
        if engine == "both":
            results["comparison"] = self._compare_results(
                results["advanced"], results["backtrader"]
            )

        return results

    def _load_historical_data(
        self, symbol: str, start_date: str, end_date: str, timeframe: str
    ) -> pd.DataFrame:
        """
        Load historical data for a symbol.

        This method creates a connector mock similar to the one in the advanced backtester
        to ensure both engines use the same data.

        Args:
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            timeframe: Timeframe

        Returns:
            DataFrame with OHLCV data
        """
        # Convert string dates to datetime objects
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)

        # Create a mock connector similar to what the advanced backtester does
        class ConnectorMock:
            def __init__(self, symbols, start_dt, end_dt, timeframe, logger):
                self.symbols = symbols
                self.start_dt = start_dt
                self.end_dt = end_dt
                self.timeframe = timeframe
                self.logger = logger
                self.data_cache = {}

            def get_historical_data(self, symbol, timeframe_str, bars_count=100):
                """Simulate loading historical data from CSV or generate test data."""
                # Look for data file in data directory
                data_dir = os.path.join("data")
                file_name = f"{symbol}_{timeframe}.csv"
                file_path = os.path.join(data_dir, file_name)

                if os.path.exists(file_path):
                    try:
                        # Load data from CSV
                        data = pd.read_csv(file_path)
                        data["date"] = pd.to_datetime(data["date"])
                        data = data[
                            (data["date"] >= self.start_dt)
                            & (data["date"] <= self.end_dt)
                        ]
                        return data
                    except Exception as e:
                        self.logger.error(f"Error loading data for {symbol}: {e}")
                        return self._generate_test_data(symbol)
                else:
                    # Generate test data if file not found
                    self.logger.warning(
                        f"Data file for {symbol} not found, generating test data"
                    )
                    return self._generate_test_data(symbol)

            def _generate_test_data(self, symbol):
                """Generate test OHLCV data."""
                import numpy as np

                # Generate date range
                dates = pd.date_range(self.start_dt, self.end_dt, freq="D")

                # Generate random prices with a slight trend
                base_price = 1.0 if "USD" in symbol else 100.0
                trend = np.linspace(0, 0.2, len(dates))
                random_factor = np.random.normal(0, 0.02, len(dates)).cumsum()

                # Calculate prices
                closes = base_price * (1 + trend + random_factor)
                opens = np.roll(closes, 1)
                opens[0] = closes[0] * 0.99
                highs = np.maximum(opens, closes) * 1.01
                lows = np.minimum(opens, closes) * 0.99
                volumes = np.random.randint(100, 1000, len(dates))

                # Create DataFrame
                data = pd.DataFrame(
                    {
                        "date": dates,
                        "open": opens,
                        "high": highs,
                        "low": lows,
                        "close": closes,
                        "volume": volumes,
                    }
                )

                return data

        # Create the connector mock
        connector_mock = ConnectorMock(
            [symbol], start_dt, end_dt, timeframe, self.logger
        )

        # Get the data
        data = connector_mock.get_historical_data(symbol, timeframe)

        return data

    @staticmethod
    def _compare_results(
        advanced_results: Dict[str, Any], backtrader_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare results from both engines to identify discrepancies.

        Args:
            advanced_results: Results from advanced backtester
            backtrader_results: Results from backtrader

        Returns:
            Dictionary with comparison metrics
        """
        comparison = {}

        # Compare profit percentages
        adv_profit = advanced_results.get("profit_percentage", 0)
        bt_profit = backtrader_results.get("profit_percentage", 0)
        profit_diff = abs(adv_profit - bt_profit)

        comparison["profit_percentage_diff"] = profit_diff
        comparison["profit_percentage_match"] = profit_diff < 1.0  # Within 1%

        # Compare trade counts
        adv_trades = advanced_results.get("total_trades", 0)
        bt_trades = backtrader_results.get("total_trades", 0)
        trade_diff = abs(adv_trades - bt_trades)

        comparison["trade_count_diff"] = trade_diff
        comparison["trade_count_match"] = trade_diff < 3  # Within 3 trades

        # Compare other key metrics
        key_metrics = ["win_rate", "max_drawdown", "sharpe_ratio"]
        for metric in key_metrics:
            adv_value = advanced_results.get("metrics", {}).get(metric, 0)
            bt_value = backtrader_results.get(metric, 0)

            # For win_rate, convert to percentage for consistent comparison
            if metric == "win_rate" and "win_rate" in backtrader_results:
                bt_value *= 100

            diff = abs(adv_value - bt_value)
            comparison[f"{metric}_diff"] = diff

            # Threshold depends on the metric
            threshold = 5.0 if metric == "win_rate" else 2.0
            comparison[f"{metric}_match"] = diff < threshold

        # Overall consistency score
        match_values = [v for k, v in comparison.items() if k.endswith("_match")]
        comparison["consistency_score"] = (
            sum(match_values) / len(match_values) if match_values else 0
        )

        return comparison
