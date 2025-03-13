# src/analysis/backtester.py
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter

from src.ftmo.ftmo_validator import FTMOValidator
from src.risk.position_sizer import calculate_position_size
from src.strategy.base_strategy import Strategy
from src.strategy.strategy_factory import StrategyFactory
from src.utils.logger import Logger


class Backtester:
    """
    Advanced backtesting engine for evaluating trading strategies with realistic execution modeling.

    Features:
    - Multiple timeframe backtesting
    - Transaction cost modeling (spread, commission, slippage)
    - Position sizing based on risk management rules
    - Detailed performance metrics and analytics
    - FTMO compliance validation
    - Equity curve visualization
    - Monte Carlo simulation
    """

    def __init__(self, config: Dict, logger: Logger):
        """
        Initialize the backtester.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger

        # Initialize backtesting parameters
        self.initial_balance = config.get("risk", {}).get("initial_balance", 100000)
        self.risk_per_trade = config.get("risk", {}).get("risk_per_trade", 0.01)
        self.max_risk_per_day = config.get("risk", {}).get("max_daily_drawdown", 0.05)
        self.max_risk_total = config.get("risk", {}).get("total_drawdown_limit", 0.10)

        # Transaction costs
        self.spread = config.get("backtest", {}).get("spread", 2.0)  # Spread in pips
        self.commission = config.get("backtest", {}).get(
            "commission", 0.0
        )  # Commission in $ per lot
        self.slippage = config.get("backtest", {}).get(
            "slippage", 1.0
        )  # Slippage in pips

        # Output settings
        self.output_dir = config.get("output", {}).get(
            "backtest_results_dir", "backtest_results"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        # FTMO validator
        self.ftmo_validator = FTMOValidator(config, logger=logger, log_file=None)

        # Trading state
        self.balance = self.initial_balance
        self.equity = self.initial_balance
        self.peak_balance = self.initial_balance
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.daily_stats = []

        # Performance metrics
        self.metrics = {}

        # Custom plot styling
        plt.style.use("seaborn-v0_8-darkgrid")
        plt.rcParams["figure.figsize"] = (16, 10)
        plt.rcParams["font.size"] = 12

        self.logger.info(
            f"Backtester initialized: initial_balance=${self.initial_balance}, "
            f"risk_per_trade={self.risk_per_trade*100}%, "
            f"max_daily_drawdown={self.max_risk_per_day*100}%, "
            f"max_total_drawdown={self.max_risk_total*100}%"
        )

    def run_backtest(
        self,
        strategy_name: str,
        symbols: List[str],
        start_date: str,
        end_date: str,
        timeframe: str = "D1",
        parameters: Dict = None,
        plot_results: bool = True,
    ) -> Dict[str, Any]:
        """
        Run a backtest for a specific strategy on multiple symbols.

        Args:
            strategy_name: Name of the strategy to test
            symbols: List of trading symbols
            start_date: Start date for the backtest (YYYY-MM-DD)
            end_date: End date for the backtest (YYYY-MM-DD)
            timeframe: Timeframe for the data ('M1', 'H1', 'D1', etc.)
            parameters: Custom parameters for the strategy
            plot_results: Whether to generate and save performance plots

        Returns:
            Dictionary with backtest results
        """
        self.logger.info(
            f"Starting backtest for {strategy_name} on {symbols} from {start_date} to {end_date}"
        )

        # Convert dates to datetime
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)

        # Create MT5 connector mock for loading data
        connector_mock = self._create_connector_mock(
            symbols, start_dt, end_dt, timeframe
        )

        # Create risk manager mock
        risk_manager_mock = self._create_risk_manager_mock()

        # Initialize strategy using factory
        try:
            if parameters:
                # Use custom parameters if provided
                strategy_config = self.config.copy()
                strategy_config["strategy"] = parameters
                strategy = StrategyFactory.create_strategy(
                    strategy_name,
                    connector_mock,
                    risk_manager_mock,
                    self.logger,
                    strategy_config,
                )
            else:
                strategy = StrategyFactory.create_strategy(
                    strategy_name,
                    connector_mock,
                    risk_manager_mock,
                    self.logger,
                    self.config,
                )

            self.logger.info(f"Strategy {strategy.get_name()} initialized for backtest")
        except ValueError as e:
            self.logger.error(f"Failed to create strategy: {e}")
            return {"success": False, "error": str(e)}

        # Reset trading state for new backtest
        self._reset_trading_state()

        # Run the backtest process
        try:
            self._run_backtest_process(strategy, symbols, start_dt, end_dt, timeframe)

            # Calculate performance metrics
            self._calculate_performance_metrics()

            # Check FTMO compliance
            ftmo_compliance = self._check_ftmo_compliance()

            # Generate plots
            if plot_results:
                plot_paths = self._generate_performance_plots(
                    strategy_name, symbols, start_date, end_date
                )
                self.logger.info(f"Generated {len(plot_paths)} performance plots")

            # Prepare results
            results = {
                "success": True,
                "strategy": strategy_name,
                "symbols": symbols,
                "timeframe": timeframe,
                "start_date": start_date,
                "end_date": end_date,
                "initial_balance": self.initial_balance,
                "final_balance": self.balance,
                "total_trades": len(self.trades),
                "profit_loss": self.balance - self.initial_balance,
                "profit_percentage": ((self.balance / self.initial_balance) - 1) * 100,
                "metrics": self.metrics,
                "ftmo_compliance": ftmo_compliance,
            }

            # Save results to file
            self._save_backtest_results(results, strategy_name)

            self.logger.info(
                f"Backtest completed: Profit={results['profit_percentage']:.2f}%, "
                f"Trades={results['total_trades']}, Compliance={ftmo_compliance['is_compliant']}"
            )

            return results

        except Exception as e:
            self.logger.error(f"Error during backtest: {e}")
            import traceback

            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def run_optimization(
        self,
        strategy_name: str,
        symbols: List[str],
        param_ranges: Dict[str, List[Any]],
        start_date: str,
        end_date: str,
        timeframe: str = "D1",
        metric: str = "sharpe_ratio",
        max_workers: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Run parameter optimization for a strategy.

        Args:
            strategy_name: Name of the strategy to optimize
            symbols: List of trading symbols
            param_ranges: Dictionary of parameter names and their possible values
            start_date: Start date for the backtest (YYYY-MM-DD)
            end_date: End date for the backtest (YYYY-MM-DD)
            timeframe: Timeframe for the data
            metric: Metric to optimize ('sharpe_ratio', 'profit_factor', etc.)
            max_workers: Maximum number of parallel workers for optimization

        Returns:
            Dictionary with optimization results
        """
        self.logger.info(f"Starting optimization for {strategy_name} on {symbols}")
        self.logger.info(f"Parameter ranges: {param_ranges}")

        # Generate all parameter combinations
        param_combinations = self._generate_parameter_combinations(param_ranges)
        total_combinations = len(param_combinations)

        self.logger.info(f"Testing {total_combinations} parameter combinations")

        # Setup parallel processing if available
        use_parallel = max_workers and max_workers > 1

        if use_parallel:
            try:
                from concurrent.futures import ProcessPoolExecutor

                self.logger.info(
                    f"Using parallel processing with {max_workers} workers"
                )
            except ImportError:
                use_parallel = False
                self.logger.warning(
                    "concurrent.futures not available, falling back to sequential processing"
                )

        # Track progress and results
        start_time = time.time()
        results = []

        # Function to run a single backtest
        def run_single_test(params):
            try:
                backtest_result = self.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    start_date=start_date,
                    end_date=end_date,
                    timeframe=timeframe,
                    parameters=params,
                    plot_results=False,  # Don't generate plots for each run
                )

                if backtest_result["success"]:
                    metrics = backtest_result["metrics"]

                    # Return the key metrics and parameters
                    return {
                        "parameters": params,
                        "net_profit_pct": backtest_result["profit_percentage"],
                        "total_trades": backtest_result["total_trades"],
                        "win_rate": metrics.get("win_rate", 0) * 100,
                        "profit_factor": metrics.get("profit_factor", 0),
                        "max_drawdown": metrics.get("max_drawdown", 0),
                        "sharpe_ratio": metrics.get("sharpe_ratio", 0),
                        "sortino_ratio": metrics.get("sortino_ratio", 0),
                        "ftmo_compliant": backtest_result.get(
                            "ftmo_compliance", {}
                        ).get("is_compliant", False),
                    }
                else:
                    return {
                        "parameters": params,
                        "error": backtest_result.get("error", "Unknown error"),
                    }
            except Exception as e:
                return {"parameters": params, "error": str(e)}

        # Run optimizations
        if use_parallel:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(run_single_test, param_combinations))
        else:
            for i, params in enumerate(param_combinations):
                self.logger.info(
                    f"Testing combination {i+1}/{total_combinations}: {params}"
                )
                result = run_single_test(params)
                results.append(result)

                # Log progress every 10% of combinations
                if (i + 1) % max(1, total_combinations // 10) == 0:
                    elapsed = time.time() - start_time
                    progress = (i + 1) / total_combinations
                    estimated_total = elapsed / progress if progress > 0 else 0
                    remaining = estimated_total - elapsed

                    self.logger.info(
                        f"Progress: {progress*100:.1f}% - "
                        f"Elapsed: {elapsed:.1f}s, "
                        f"Remaining: {remaining:.1f}s"
                    )

        # Filter out errors
        valid_results = [r for r in results if "error" not in r]

        if not valid_results:
            self.logger.error("No valid optimization results")
            return {"success": False, "error": "No valid optimization results"}

        # Find best result based on the target metric
        if metric in [
            "sharpe_ratio",
            "sortino_ratio",
            "profit_factor",
            "net_profit_pct",
            "win_rate",
        ]:
            # Higher is better
            best_result = max(valid_results, key=lambda x: x.get(metric, -float("inf")))
        elif metric in ["max_drawdown"]:
            # Lower is better
            best_result = min(valid_results, key=lambda x: x.get(metric, float("inf")))
        else:
            self.logger.warning(
                f"Unknown optimization metric: {metric}, defaulting to net_profit_pct"
            )
            best_result = max(
                valid_results, key=lambda x: x.get("net_profit_pct", -float("inf"))
            )

        # Run a final backtest with the best parameters and generate plots
        best_params = best_result["parameters"]

        self.logger.info(f"Best parameters found: {best_params}")
        self.logger.info(f"Best {metric}: {best_result.get(metric, 'N/A')}")

        final_result = self.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            timeframe=timeframe,
            parameters=best_params,
            plot_results=True,
        )

        # Create optimization report
        optimization_results = {
            "success": True,
            "strategy": strategy_name,
            "symbols": symbols,
            "start_date": start_date,
            "end_date": end_date,
            "optimization_metric": metric,
            "total_combinations": total_combinations,
            "valid_combinations": len(valid_results),
            "best_parameters": best_params,
            "best_metrics": {
                metric: best_result.get(metric),
                "net_profit_pct": best_result.get("net_profit_pct"),
                "total_trades": best_result.get("total_trades"),
                "win_rate": best_result.get("win_rate"),
                "profit_factor": best_result.get("profit_factor"),
                "max_drawdown": best_result.get("max_drawdown"),
                "sharpe_ratio": best_result.get("sharpe_ratio"),
                "sortino_ratio": best_result.get("sortino_ratio"),
            },
            "final_backtest": final_result,
            "all_results": valid_results,
            "elapsed_time": time.time() - start_time,
        }

        # Save optimization results
        self._save_optimization_results(optimization_results, strategy_name)

        # Generate parameter impact visualization
        self._plot_parameter_impact(valid_results, param_ranges, metric, strategy_name)

        return optimization_results

    def run_monte_carlo_simulation(
        self, backtest_results: Dict[str, Any], num_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation on backtest results to assess strategy robustness.

        Args:
            backtest_results: Results from a previous backtest
            num_simulations: Number of Monte Carlo simulations to run

        Returns:
            Dictionary with simulation results
        """
        trades = self.trades  # Use trades from the most recent backtest

        if not trades:
            self.logger.error("No trades available for Monte Carlo simulation")
            return {"success": False, "error": "No trades available"}

        self.logger.info(
            f"Running Monte Carlo simulation with {num_simulations} iterations"
        )

        # Extract trade returns
        trade_returns = [
            trade.get("profit_loss", 0) / self.initial_balance for trade in trades
        ]

        # Generate random sequences of trades
        random_sequences = []
        np.random.seed(42)  # For reproducibility

        for _ in range(num_simulations):
            # Randomly reorder trades with replacement
            random_sequence = np.random.choice(trade_returns, len(trade_returns))
            random_sequences.append(random_sequence)

        # Calculate equity curves for each simulation
        equity_curves = []
        final_balances = []
        max_drawdowns = []

        for sequence in random_sequences:
            equity = [self.initial_balance]
            peak = self.initial_balance

            for return_pct in sequence:
                new_equity = equity[-1] * (1 + return_pct)
                equity.append(new_equity)
                peak = max(peak, new_equity)

                # Track drawdown
                drawdown = (peak - new_equity) / peak if peak > 0 else 0
                max_drawdowns.append(drawdown * 100)

            equity_curves.append(equity)
            final_balances.append(equity[-1])

        # Calculate statistics
        final_balance_mean = np.mean(final_balances)
        final_balance_median = np.median(final_balances)
        final_balance_std = np.std(final_balances)
        final_balance_min = np.min(final_balances)
        final_balance_max = np.max(final_balances)

        # Calculate percentiles
        percentiles = {
            "5th": np.percentile(final_balances, 5),
            "25th": np.percentile(final_balances, 25),
            "50th": np.percentile(final_balances, 50),
            "75th": np.percentile(final_balances, 75),
            "95th": np.percentile(final_balances, 95),
        }

        # Calculate worst drawdown
        worst_drawdown = np.max(max_drawdowns)

        # Calculate probability of loss
        prob_loss = (
            len([b for b in final_balances if b < self.initial_balance])
            / num_simulations
        )

        # Create Monte Carlo plot
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(14, 12), gridspec_kw={"height_ratios": [2, 1]}
        )

        # Plot equity curves
        for i, equity in enumerate(equity_curves):
            if i < 100:  # Only plot a subset for clarity
                ax1.plot(equity, color="blue", alpha=0.1)

        # Plot original equity curve
        original_equity = [self.initial_balance]
        for trade in trades:
            original_equity.append(original_equity[-1] + trade.get("profit_loss", 0))

        ax1.plot(original_equity, color="red", linewidth=2, label="Original Backtest")

        # Plot percentiles
        ax1.axhline(
            y=percentiles["5th"],
            color="orange",
            linestyle="--",
            label=f'5th Percentile: ${percentiles["5th"]:.2f}',
        )
        ax1.axhline(
            y=percentiles["95th"],
            color="green",
            linestyle="--",
            label=f'95th Percentile: ${percentiles["95th"]:.2f}',
        )

        ax1.set_title("Monte Carlo Simulation: Equity Curves", fontsize=14)
        ax1.set_ylabel("Account Balance ($)", fontsize=12)
        ax1.legend()
        ax1.grid(True)

        # Plot histogram of final balances
        ax2.hist(final_balances, bins=50, alpha=0.7, color="blue")
        ax2.axvline(
            x=self.initial_balance,
            color="black",
            linestyle="-",
            label=f"Initial Balance: ${self.initial_balance}",
        )
        ax2.axvline(
            x=final_balance_mean,
            color="red",
            linestyle="-",
            label=f"Mean Final Balance: ${final_balance_mean:.2f}",
        )

        ax2.set_title("Distribution of Final Account Balances", fontsize=14)
        ax2.set_xlabel("Final Balance ($)", fontsize=12)
        ax2.set_ylabel("Frequency", fontsize=12)
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()

        # Save the plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        strategy_name = backtest_results.get("strategy", "unknown")
        plot_path = os.path.join(
            self.output_dir, f"monte_carlo_{strategy_name}_{timestamp}.png"
        )
        plt.savefig(plot_path)
        plt.close(fig)

        # Prepare results
        simulation_results = {
            "success": True,
            "num_simulations": num_simulations,
            "final_balance_stats": {
                "mean": final_balance_mean,
                "median": final_balance_median,
                "std": final_balance_std,
                "min": final_balance_min,
                "max": final_balance_max,
                "percentiles": percentiles,
            },
            "worst_drawdown": worst_drawdown,
            "probability_of_loss": prob_loss,
            "plot_path": plot_path,
        }

        self.logger.info(
            f"Monte Carlo simulation completed: "
            f"Mean final balance=${final_balance_mean:.2f}, "
            f"Worst drawdown={worst_drawdown:.2f}%"
        )

        return simulation_results

    def _create_connector_mock(
        self, symbols: List[str], start_dt: datetime, end_dt: datetime, timeframe: str
    ) -> Any:
        """
        Create a mock MT5 connector for loading historical data.

        Args:
            symbols: List of symbols to prepare data for
            start_dt: Start date
            end_dt: End date
            timeframe: Timeframe string

        Returns:
            Mock connector object
        """

        # Create a simple connector mock with the necessary methods
        class MT5ConnectorMock:
            def __init__(self, symbols, start_dt, end_dt, timeframe, logger):
                self.symbols = symbols
                self.start_dt = start_dt
                self.end_dt = end_dt
                self.timeframe = timeframe
                self.logger = logger
                self.data_cache = {}

            def get_historical_data(self, symbol, timeframe_or_str, bars_count=100):
                """Simulate loading historical data from CSV or generate random data."""
                if symbol in self.data_cache:
                    # Return cached data
                    return self.data_cache[symbol]

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

                        # Cache the data
                        self.data_cache[symbol] = data

                        self.logger.info(
                            f"Loaded {len(data)} bars for {symbol} from {file_path}"
                        )
                        return data
                    except Exception as e:
                        self.logger.error(f"Error loading data for {symbol}: {e}")
                        return self._generate_random_data(symbol)
                else:
                    # Generate random data if file not found
                    self.logger.warning(
                        f"Data file for {symbol} not found, generating random data"
                    )
                    return self._generate_random_data(symbol)

            def _generate_random_data(self, symbol):
                """Generate random OHLCV data for testing."""
                # Generate date range
                dates = pd.date_range(self.start_dt, self.end_dt, freq="D")

                # Generate random prices
                base_price = 1.0 if "USD" in symbol else 100.0

                # Create slight upward trend
                trend = np.linspace(0, 0.2, len(dates))

                # Add some randomness
                np.random.seed(hash(symbol) % 2**32)
                random_factor = np.random.normal(0, 0.02, len(dates)).cumsum()

                # Calculate prices
                closes = base_price * (1 + trend + random_factor)
                opens = closes.shift(1).fillna(closes[0])
                highs = np.maximum(opens, closes) * (
                    1 + np.random.uniform(0, 0.01, len(dates))
                )
                lows = np.minimum(opens, closes) * (
                    1 - np.random.uniform(0, 0.01, len(dates))
                )
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

                # Cache the data
                self.data_cache[symbol] = data

                self.logger.info(f"Generated {len(data)} random bars for {symbol}")
                return data

            def get_position(self, symbol):
                """Return None as we don't have positions in backtest mode."""
                return None

            def get_open_positions(self):
                """Return empty dict as we don't have positions in backtest mode."""
                return {}

            def get_account_info(self):
                """Return mock account info."""
                return {
                    "balance": 100000,
                    "equity": 100000,
                    "margin": 0,
                    "free_margin": 100000,
                }

            def place_order(self, symbol, action, volume, price, sl, tp, comment):
                """Mock order placement."""
                return {
                    "order_id": f"mock_{int(time.time())}",
                    "volume": volume,
                    "price": price,
                }

            def close_position(self, symbol, comment=None):
                """Mock position closing."""
                return {"success": True}

        return MT5ConnectorMock(symbols, start_dt, end_dt, timeframe, self.logger)

    def _create_risk_manager_mock(self) -> Any:
        """
        Create a mock risk manager.

        Returns:
            Mock risk manager object
        """

        # Create a simple risk manager mock
        class RiskManagerMock:
            def __init__(self, risk_per_trade, logger):
                self.risk_per_trade = risk_per_trade
                self.logger = logger
                self.is_trading_allowed = True

            def calculate_position_size(
                self, symbol, entry_price, stop_loss=None, risk_pips=None
            ):
                """Calculate position size based on risk per trade."""
                # Use the position_sizer utility
                account_balance = 100000
                pip_value = 10.0  # Default for most forex pairs

                if stop_loss is None and risk_pips is None:
                    # Default to 2% of price as risk
                    risk_pips = entry_price * 0.02
                elif stop_loss is not None and risk_pips is None:
                    risk_pips = abs(entry_price - stop_loss)

                return calculate_position_size(
                    entry_price=entry_price,
                    stop_loss=(
                        stop_loss if stop_loss is not None else entry_price - risk_pips
                    ),
                    account_balance=account_balance,
                    risk_percentage=self.risk_per_trade,
                    pip_value=pip_value,
                )

            def check_ftmo_limits(self, account_info):
                """Check FTMO risk limits."""
                return True, None  # Always allow trading in backtest

        return RiskManagerMock(self.risk_per_trade, self.logger)

    def _reset_trading_state(self) -> None:
        """Reset the trading state for a new backtest."""
        self.balance = self.initial_balance
        self.equity = self.initial_balance
        self.peak_balance = self.initial_balance
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.daily_stats = []
        self.metrics = {}

    def _run_backtest_process(
        self,
        strategy: Strategy,
        symbols: List[str],
        start_dt: datetime,
        end_dt: datetime,
        timeframe: str,
    ) -> None:
        """
        Run the full backtest process.

        Args:
            strategy: Strategy instance to test
            symbols: List of symbols to trade
            start_dt: Start datetime
            end_dt: End datetime
            timeframe: Timeframe for the test
        """
        self.logger.info(f"Running backtest process from {start_dt} to {end_dt}")

        # Step 1: Determine the date steps based on the timeframe
        time_step = self._get_time_step(timeframe)

        # Step 2: Prepare the date range
        current_date = start_dt

        # Create initial equity point
        self.equity_curve.append(
            {
                "date": current_date,
                "balance": self.balance,
                "equity": self.equity,
                "open_positions": 0,
            }
        )

        # Track trading days for statistics
        trading_days = set()
        daily_balances = {}

        # Step 3: Process each day
        while current_date <= end_dt:
            # Update date for logging
            date_str = current_date.strftime("%Y-%m-%d")

            # Skip weekends for daily+ timeframes
            if timeframe in ["D1", "W1", "MN1"] and current_date.weekday() >= 5:
                current_date += time_step
                continue

            # Store daily opening balance
            if date_str not in daily_balances:
                daily_balances[date_str] = self.balance

            # Process each symbol
            for symbol in symbols:
                # Check if we have an open position for this symbol
                position = self.positions.get(symbol)

                # Generate trading signals
                signal_result = strategy.process_symbol(symbol)

                # Process signals
                if signal_result:
                    signal = signal_result.get("signal", "NONE")
                    meta = signal_result.get("meta", {})

                    # Log signal
                    if signal != "NONE":
                        self.logger.info(f"Signal for {symbol} on {date_str}: {signal}")

                    # Entry signals
                    if signal in ["BUY", "SELL"] and not position:
                        # Create new position
                        entry_price = meta.get("entry_price", 0)
                        stop_loss = meta.get("stop_loss")
                        take_profit = meta.get("take_profit")
                        risk_pips = meta.get("risk_pips")

                        # Calculate position size
                        volume = strategy.risk_manager.calculate_position_size(
                            symbol=symbol,
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            risk_pips=risk_pips,
                        )

                        # Apply transaction costs
                        if signal == "BUY":
                            adjusted_price = (
                                entry_price + (self.spread + self.slippage) * 0.0001
                            )
                        else:
                            adjusted_price = (
                                entry_price - (self.spread + self.slippage) * 0.0001
                            )

                        # Create position
                        self.positions[symbol] = {
                            "symbol": symbol,
                            "direction": signal,
                            "entry_date": current_date,
                            "entry_price": adjusted_price,
                            "volume": volume,
                            "stop_loss": stop_loss,
                            "take_profit": take_profit,
                        }

                        # Add trading day
                        trading_days.add(date_str)

                        self.logger.info(
                            f"Opened {signal} position on {symbol}: "
                            f"price={adjusted_price}, volume={volume}"
                        )

                    # Exit signals
                    elif signal in ["CLOSE_BUY", "CLOSE_SELL"] and position:
                        expected_direction = "BUY" if signal == "CLOSE_BUY" else "SELL"

                        if position["direction"] == expected_direction:
                            # Get current price
                            if signal == "CLOSE_BUY":
                                exit_price = (
                                    meta.get("exit_price", 0)
                                    - (self.spread + self.slippage) * 0.0001
                                )
                            else:
                                exit_price = (
                                    meta.get("exit_price", 0)
                                    + (self.spread + self.slippage) * 0.0001
                                )

                            # Calculate P&L
                            entry_price = position["entry_price"]
                            volume = position["volume"]

                            if position["direction"] == "BUY":
                                points = exit_price - entry_price
                            else:
                                points = entry_price - exit_price

                            # Calculate profit/loss
                            profit_loss = points * volume * 100000  # Standard lot size

                            # Apply commission
                            profit_loss -= self.commission * volume

                            # Update balance
                            self.balance += profit_loss

                            # Track peak balance for drawdown calculation
                            self.peak_balance = max(self.peak_balance, self.balance)

                            # Record trade
                            trade = {
                                "symbol": symbol,
                                "direction": position["direction"],
                                "entry_date": position["entry_date"],
                                "exit_date": current_date,
                                "entry_price": entry_price,
                                "exit_price": exit_price,
                                "volume": volume,
                                "profit_loss": profit_loss,
                                "stop_loss": position.get("stop_loss"),
                                "take_profit": position.get("take_profit"),
                                "reason": meta.get("reason", "exit_signal"),
                            }

                            self.trades.append(trade)

                            # Add trading day
                            trading_days.add(date_str)

                            # Remove position
                            del self.positions[symbol]

                            self.logger.info(
                                f"Closed {position['direction']} position on {symbol}: "
                                f"profit_loss=${profit_loss:.2f}"
                            )

                # Check for stop loss/take profit hits
                elif position:
                    # Get price data for the current bar
                    historical_data = strategy.connector.get_historical_data(
                        symbol=symbol, timeframe_or_str=timeframe, bars_count=1
                    )

                    if historical_data is not None and not historical_data.empty:
                        # Get high/low prices
                        high = historical_data["high"].iloc[-1]
                        low = historical_data["low"].iloc[-1]

                        # Check if stop loss was hit
                        stop_loss_hit = False
                        take_profit_hit = False

                        if position["direction"] == "BUY":
                            if (
                                position.get("stop_loss")
                                and low <= position["stop_loss"]
                            ):
                                stop_loss_hit = True
                                exit_price = position["stop_loss"]
                            elif (
                                position.get("take_profit")
                                and high >= position["take_profit"]
                            ):
                                take_profit_hit = True
                                exit_price = position["take_profit"]
                        else:  # SELL
                            if (
                                position.get("stop_loss")
                                and high >= position["stop_loss"]
                            ):
                                stop_loss_hit = True
                                exit_price = position["stop_loss"]
                            elif (
                                position.get("take_profit")
                                and low <= position["take_profit"]
                            ):
                                take_profit_hit = True
                                exit_price = position["take_profit"]

                        # Process stop loss/take profit hit
                        if stop_loss_hit or take_profit_hit:
                            # Calculate P&L
                            entry_price = position["entry_price"]
                            volume = position["volume"]

                            if position["direction"] == "BUY":
                                points = exit_price - entry_price
                            else:
                                points = entry_price - exit_price

                            # Calculate profit/loss
                            profit_loss = points * volume * 100000  # Standard lot size

                            # Apply commission
                            profit_loss -= self.commission * volume

                            # Update balance
                            self.balance += profit_loss

                            # Track peak balance for drawdown calculation
                            self.peak_balance = max(self.peak_balance, self.balance)

                            # Record trade
                            trade = {
                                "symbol": symbol,
                                "direction": position["direction"],
                                "entry_date": position["entry_date"],
                                "exit_date": current_date,
                                "entry_price": entry_price,
                                "exit_price": exit_price,
                                "volume": volume,
                                "profit_loss": profit_loss,
                                "stop_loss": position.get("stop_loss"),
                                "take_profit": position.get("take_profit"),
                                "reason": (
                                    "stop_loss" if stop_loss_hit else "take_profit"
                                ),
                            }

                            self.trades.append(trade)

                            # Add trading day
                            trading_days.add(date_str)

                            # Remove position
                            del self.positions[symbol]

                            self.logger.info(
                                f"{'Stop loss' if stop_loss_hit else 'Take profit'} hit on {symbol}: "
                                f"profit_loss=${profit_loss:.2f}"
                            )

            # Update equity curve
            self.equity = (
                self.balance
            )  # In a real system, this would include unrealized P&L

            self.equity_curve.append(
                {
                    "date": current_date,
                    "balance": self.balance,
                    "equity": self.equity,
                    "open_positions": len(self.positions),
                }
            )

            # Move to next day
            current_date += time_step

        # Calculate daily statistics
        for date_str in sorted(set(daily_balances.keys()) | set(trading_days)):
            # Get start and end balance for the day
            start_balance = daily_balances.get(date_str, self.initial_balance)

            # Find the last equity curve entry for this day
            end_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
            day_equity = [
                e
                for e in self.equity_curve
                if e["date"].strftime("%Y-%m-%d") == date_str
            ]

            if day_equity:
                end_balance = day_equity[-1]["balance"]

                # Calculate daily P&L
                daily_pnl = end_balance - start_balance
                daily_pnl_pct = (
                    (daily_pnl / start_balance) * 100 if start_balance > 0 else 0
                )

                # Get trades for the day
                day_trades = [
                    t
                    for t in self.trades
                    if t["exit_date"].strftime("%Y-%m-%d") == date_str
                ]

                # Calculate intraday drawdown
                day_low = (
                    min([e["balance"] for e in day_equity])
                    if day_equity
                    else end_balance
                )
                day_high = (
                    max([e["balance"] for e in day_equity])
                    if day_equity
                    else end_balance
                )

                intraday_drawdown = (
                    ((day_high - day_low) / day_high) * 100 if day_high > 0 else 0
                )

                # Record daily stats
                self.daily_stats.append(
                    {
                        "date": date_str,
                        "start_balance": start_balance,
                        "end_balance": end_balance,
                        "daily_pnl": daily_pnl,
                        "daily_pnl_pct": daily_pnl_pct,
                        "num_trades": len(day_trades),
                        "intraday_drawdown": intraday_drawdown,
                    }
                )

            # Update daily balance for next day
            next_day = (
                datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
            ).strftime("%Y-%m-%d")
            if next_day not in daily_balances:
                daily_balances[next_day] = end_balance if day_equity else start_balance

        self.logger.info(
            f"Backtest process completed with {len(self.trades)} trades across {len(trading_days)} trading days"
        )

    def _calculate_performance_metrics(self) -> None:
        """Calculate detailed performance metrics from the backtest results."""
        if not self.trades:
            self.metrics = {
                "total_trades": 0,
                "win_rate": 0,
                "profit_factor": 0,
                "average_profit": 0,
                "average_loss": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0,
                "sortino_ratio": 0,
                "expectancy": 0,
            }
            return

        # Basic trade statistics
        winning_trades = [t for t in self.trades if t["profit_loss"] > 0]
        losing_trades = [t for t in self.trades if t["profit_loss"] <= 0]

        total_trades = len(self.trades)
        winning_trades_count = len(winning_trades)
        losing_trades_count = len(losing_trades)

        win_rate = winning_trades_count / total_trades if total_trades > 0 else 0

        # Profit metrics
        gross_profit = sum(t["profit_loss"] for t in winning_trades)
        gross_loss = sum(t["profit_loss"] for t in losing_trades)

        profit_factor = (
            abs(gross_profit / gross_loss) if gross_loss != 0 else float("inf")
        )

        average_profit = (
            gross_profit / winning_trades_count if winning_trades_count > 0 else 0
        )
        average_loss = (
            gross_loss / losing_trades_count if losing_trades_count > 0 else 0
        )

        # Drawdown calculation from equity curve
        max_drawdown = 0
        peak = self.initial_balance

        for point in self.equity_curve:
            balance = point["balance"]
            peak = max(peak, balance)
            drawdown = (peak - balance) / peak if peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)

        max_drawdown *= 100  # Convert to percentage

        # Calculate daily returns
        if len(self.equity_curve) > 1:
            daily_returns = []

            for i in range(1, len(self.equity_curve)):
                prev_balance = self.equity_curve[i - 1]["balance"]
                curr_balance = self.equity_curve[i]["balance"]

                if prev_balance > 0:
                    daily_return = (curr_balance - prev_balance) / prev_balance
                    daily_returns.append(daily_return)

            # Calculate Sharpe Ratio (assuming 0% risk-free rate)
            if daily_returns:
                returns_mean = np.mean(daily_returns)
                returns_std = np.std(daily_returns)

                sharpe_ratio = (
                    (returns_mean / returns_std) * np.sqrt(252)
                    if returns_std > 0
                    else 0
                )

                # Calculate Sortino Ratio (downside deviation only)
                negative_returns = [r for r in daily_returns if r < 0]
                downside_deviation = np.std(negative_returns) if negative_returns else 0

                sortino_ratio = (
                    (returns_mean / downside_deviation) * np.sqrt(252)
                    if downside_deviation > 0
                    else 0
                )
            else:
                sharpe_ratio = 0
                sortino_ratio = 0
        else:
            sharpe_ratio = 0
            sortino_ratio = 0

        # Calculate expectancy
        avg_win = average_profit
        avg_loss = abs(average_loss) if average_loss < 0 else average_loss

        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        expectancy_ratio = (
            (win_rate * avg_win) / ((1 - win_rate) * avg_loss)
            if losing_trades_count > 0
            else float("inf")
        )

        # Calculate Kelly percentage
        w = win_rate
        r = avg_win / avg_loss if avg_loss > 0 else float("inf")

        kelly_percentage = ((w * r) - (1 - w)) / r if r != float("inf") else w

        # Calculate average holding periods
        if total_trades > 0:
            holding_periods = []

            for trade in self.trades:
                entry_date = trade["entry_date"]
                exit_date = trade["exit_date"]

                if isinstance(entry_date, str):
                    entry_date = pd.to_datetime(entry_date)

                if isinstance(exit_date, str):
                    exit_date = pd.to_datetime(exit_date)

                holding_period = (
                    exit_date - entry_date
                ).total_seconds() / 3600  # in hours
                holding_periods.append(holding_period)

            avg_holding_period = np.mean(holding_periods)
            max_holding_period = np.max(holding_periods)
            min_holding_period = np.min(holding_periods)
        else:
            avg_holding_period = 0
            max_holding_period = 0
            min_holding_period = 0

        # Compile all metrics
        self.metrics = {
            "total_trades": total_trades,
            "winning_trades": winning_trades_count,
            "losing_trades": losing_trades_count,
            "win_rate": win_rate,
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "net_profit": gross_profit + gross_loss,
            "profit_factor": profit_factor,
            "average_profit": average_profit,
            "average_loss": average_loss,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "expectancy": expectancy,
            "expectancy_ratio": expectancy_ratio,
            "kelly_percentage": kelly_percentage,
            "avg_holding_period": avg_holding_period,
            "max_holding_period": max_holding_period,
            "min_holding_period": min_holding_period,
            "trading_days": len(
                set(t["exit_date"].strftime("%Y-%m-%d") for t in self.trades)
            ),
            "avg_trades_per_day": (
                total_trades
                / len(set(t["exit_date"].strftime("%Y-%m-%d") for t in self.trades))
                if self.trades
                else 0
            ),
            "largest_win": (
                max(t["profit_loss"] for t in winning_trades) if winning_trades else 0
            ),
            "largest_loss": (
                min(t["profit_loss"] for t in losing_trades) if losing_trades else 0
            ),
            "consecutive_wins": self._calculate_max_consecutive(self.trades, True),
            "consecutive_losses": self._calculate_max_consecutive(self.trades, False),
        }

    def _check_ftmo_compliance(self) -> Dict[str, Any]:
        """
        Check FTMO compliance for the backtest results.

        Returns:
            Dictionary with FTMO compliance results
        """
        # FTMO rules
        profit_target = 0.10  # 10% profit target
        max_daily_loss = 0.05  # 5% max daily loss
        max_total_loss = 0.10  # 10% max total loss
        min_trading_days = 4  # Minimum 4 trading days

        # Check profit target
        profit_amount = self.balance - self.initial_balance
        profit_percentage = (
            profit_amount / self.initial_balance if self.initial_balance > 0 else 0
        )
        profit_target_met = profit_percentage >= profit_target

        # Check max drawdown
        max_drawdown_percentage = (
            self.metrics.get("max_drawdown", 0) / 100
        )  # Convert from percentage
        total_loss_compliant = max_drawdown_percentage <= max_total_loss

        # Check daily loss limit
        worst_daily_loss = 0

        for daily_stat in self.daily_stats:
            daily_pnl_pct = daily_stat.get("daily_pnl_pct", 0)

            if daily_pnl_pct < worst_daily_loss:
                worst_daily_loss = daily_pnl_pct

        worst_daily_loss_percentage = abs(worst_daily_loss / 100)  # Convert to decimal
        daily_loss_compliant = worst_daily_loss_percentage <= max_daily_loss

        # Check minimum trading days
        trading_days = set()

        for trade in self.trades:
            exit_date = trade["exit_date"]

            if isinstance(exit_date, str):
                exit_date = pd.to_datetime(exit_date)

            trading_days.add(exit_date.strftime("%Y-%m-%d"))

        trading_days_count = len(trading_days)
        trading_days_compliant = trading_days_count >= min_trading_days

        # Overall compliance
        is_compliant = (
            profit_target_met
            and total_loss_compliant
            and daily_loss_compliant
            and trading_days_compliant
        )

        # Create compliance result
        result = {
            "is_compliant": is_compliant,
            "profit_target_met": profit_target_met,
            "total_loss_compliant": total_loss_compliant,
            "daily_loss_compliant": daily_loss_compliant,
            "trading_days_compliant": trading_days_compliant,
            "profit_percentage": profit_percentage * 100,
            "max_drawdown": self.metrics.get("max_drawdown", 0),
            "worst_daily_loss": worst_daily_loss,
            "trading_days": trading_days_count,
        }

        # Add reasons for non-compliance
        if not is_compliant:
            reasons = []

            if not profit_target_met:
                reasons.append(
                    f"Profit target not met: {profit_percentage * 100:.2f}% < {profit_target * 100}%"
                )

            if not total_loss_compliant:
                reasons.append(
                    f"Maximum drawdown exceeded: {max_drawdown_percentage * 100:.2f}% > {max_total_loss * 100}%"
                )

            if not daily_loss_compliant:
                reasons.append(
                    f"Daily loss limit exceeded: {worst_daily_loss_percentage * 100:.2f}% > {max_daily_loss * 100}%"
                )

            if not trading_days_compliant:
                reasons.append(
                    f"Insufficient trading days: {trading_days_count} < {min_trading_days}"
                )

            result["reasons"] = reasons

        return result

    def _generate_performance_plots(
        self, strategy_name: str, symbols: List[str], start_date: str, end_date: str
    ) -> List[str]:
        """
        Generate performance visualization plots.

        Args:
            strategy_name: Name of the strategy
            symbols: List of traded symbols
            start_date: Start date
            end_date: End date

        Returns:
            List of paths to the generated plots
        """
        plot_paths = []

        # Create timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Equity Curve
        equity_plot_path = self._plot_equity_curve(strategy_name, timestamp)
        if equity_plot_path:
            plot_paths.append(equity_plot_path)

        # 2. Drawdown Plot
        drawdown_plot_path = self._plot_drawdown(strategy_name, timestamp)
        if drawdown_plot_path:
            plot_paths.append(drawdown_plot_path)

        # 3. Trade P&L Distribution
        pnl_plot_path = self._plot_pnl_distribution(strategy_name, timestamp)
        if pnl_plot_path:
            plot_paths.append(pnl_plot_path)

        # 4. Monthly Returns
        monthly_plot_path = self._plot_monthly_returns(strategy_name, timestamp)
        if monthly_plot_path:
            plot_paths.append(monthly_plot_path)

        # 5. Performance Summary
        summary_plot_path = self._plot_performance_summary(strategy_name, timestamp)
        if summary_plot_path:
            plot_paths.append(summary_plot_path)

        return plot_paths

    def _plot_equity_curve(self, strategy_name: str, timestamp: str) -> Optional[str]:
        """
        Plot equity curve with annotations for trades.

        Args:
            strategy_name: Name of the strategy
            timestamp: Timestamp for filename

        Returns:
            Path to the saved plot or None
        """
        if not self.equity_curve:
            return None

        fig, ax = plt.subplots(figsize=(14, 8))

        # Extract data
        dates = [point["date"] for point in self.equity_curve]
        balance = [point["balance"] for point in self.equity_curve]

        # Plot equity curve
        ax.plot(dates, balance, label="Account Balance", linewidth=2)

        # Add horizontal line for initial balance
        ax.axhline(
            y=self.initial_balance,
            color="grey",
            linestyle="--",
            label=f"Initial Balance (${self.initial_balance:,.2f})",
        )

        # Add horizontal line for 10% profit target
        profit_target = self.initial_balance * 1.10
        ax.axhline(
            y=profit_target,
            color="green",
            linestyle="--",
            label=f"Profit Target (${profit_target:,.2f})",
        )

        # Add horizontal line for 10% drawdown limit
        drawdown_limit = self.initial_balance * 0.90
        ax.axhline(
            y=drawdown_limit,
            color="red",
            linestyle="--",
            label=f"Drawdown Limit (${drawdown_limit:,.2f})",
        )

        # Add annotations for trades
        for trade in self.trades:
            exit_date = trade["exit_date"]
            if isinstance(exit_date, str):
                exit_date = pd.to_datetime(exit_date)

            profit_loss = trade["profit_loss"]
            trade_balance = None

            # Find the equity point closest to this trade
            for point in self.equity_curve:
                if point["date"] >= exit_date:
                    trade_balance = point["balance"]
                    break

            if trade_balance is not None:
                color = "green" if profit_loss > 0 else "red"

                # Avoid cluttering the chart with too many annotations
                if abs(profit_loss) > 500:  # Only annotate significant trades
                    ax.scatter(exit_date, trade_balance, color=color, s=50, zorder=5)

        # Format the plot
        ax.set_title(f"{strategy_name} - Equity Curve", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Account Balance ($)", fontsize=12)
        ax.legend()
        ax.grid(True)

        # Format date axis
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)

        # Add performance stats
        profit_amount = self.balance - self.initial_balance
        profit_percentage = (
            (profit_amount / self.initial_balance) * 100
            if self.initial_balance > 0
            else 0
        )

        stats_text = (
            f"Net Profit: ${profit_amount:,.2f} ({profit_percentage:.2f}%)\n"
            f"Max Drawdown: {self.metrics.get('max_drawdown', 0):.2f}%\n"
            f"Sharpe Ratio: {self.metrics.get('sharpe_ratio', 0):.2f}\n"
            f"Win Rate: {self.metrics.get('win_rate', 0) * 100:.2f}%\n"
            f"Profit Factor: {self.metrics.get('profit_factor', 0):.2f}"
        )

        # Add text box with stats
        props = dict(boxstyle="round", facecolor="white", alpha=0.7)
        ax.text(
            0.02,
            0.98,
            stats_text,
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=props,
        )

        plt.tight_layout()

        # Save plot
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_equity_curve_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _plot_drawdown(self, strategy_name: str, timestamp: str) -> Optional[str]:
        """
        Plot drawdown chart.

        Args:
            strategy_name: Name of the strategy
            timestamp: Timestamp for filename

        Returns:
            Path to the saved plot or None
        """
        if not self.equity_curve:
            return None

        fig, ax = plt.subplots(figsize=(14, 6))

        # Extract data
        dates = [point["date"] for point in self.equity_curve]
        balances = [point["balance"] for point in self.equity_curve]

        # Calculate drawdown
        drawdowns = []
        peak = self.initial_balance

        for balance in balances:
            peak = max(peak, balance)
            drawdown = (peak - balance) / peak * 100 if peak > 0 else 0
            drawdowns.append(drawdown)

        # Plot drawdown
        ax.fill_between(dates, drawdowns, 0, color="red", alpha=0.3)
        ax.plot(dates, drawdowns, color="red", label="Drawdown")

        # Add horizontal line for 5% daily drawdown limit
        ax.axhline(
            y=5.0, color="orange", linestyle="--", label="Daily Drawdown Limit (5%)"
        )

        # Add horizontal line for 10% total drawdown limit
        ax.axhline(
            y=10.0, color="red", linestyle="--", label="Total Drawdown Limit (10%)"
        )

        # Format the plot
        ax.set_title(f"{strategy_name} - Drawdown Chart", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Drawdown (%)", fontsize=12)
        ax.legend()
        ax.grid(True)

        # Set y-axis limit to make small drawdowns visible
        max_drawdown = max(drawdowns) if drawdowns else 0
        ax.set_ylim(0, max(12, max_drawdown * 1.2))

        # Format date axis
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save plot
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_drawdown_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _plot_pnl_distribution(
        self, strategy_name: str, timestamp: str
    ) -> Optional[str]:
        """
        Plot P&L distribution.

        Args:
            strategy_name: Name of the strategy
            timestamp: Timestamp for filename

        Returns:
            Path to the saved plot or None
        """
        if not self.trades:
            return None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Extract P&L data
        pnl_values = [trade["profit_loss"] for trade in self.trades]

        # 1. Histogram of P&L values
        bins = min(max(10, int(len(pnl_values) / 5)), 30)  # Adaptive bin size

        # Create histogram
        n, bins, patches = ax1.hist(pnl_values, bins=bins, alpha=0.7)

        # Color profits green and losses red
        for i in range(len(patches)):
            if bins[i] >= 0:
                patches[i].set_facecolor("green")
            else:
                patches[i].set_facecolor("red")

        # Format histogram
        ax1.set_title("P&L Distribution", fontsize=14)
        ax1.set_xlabel("Profit/Loss ($)", fontsize=12)
        ax1.set_ylabel("Frequency", fontsize=12)
        ax1.grid(True, alpha=0.3)

        # Add vertical line at zero
        ax1.axvline(x=0, color="black", linestyle="--")

        # Add text with key stats
        stats_text = (
            f"Total Trades: {len(pnl_values)}\n"
            f"Average Profit: ${np.mean([p for p in pnl_values if p > 0]) if any(p > 0 for p in pnl_values) else 0:.2f}\n"
            f"Average Loss: ${np.mean([p for p in pnl_values if p <= 0]) if any(p <= 0 for p in pnl_values) else 0:.2f}\n"
            f"Largest Profit: ${max(pnl_values) if pnl_values else 0:.2f}\n"
            f"Largest Loss: ${min(pnl_values) if pnl_values else 0:.2f}"
        )

        props = dict(boxstyle="round", facecolor="white", alpha=0.7)
        ax1.text(
            0.05,
            0.95,
            stats_text,
            transform=ax1.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=props,
        )

        # 2. Win/Loss pie chart
        winning_trades = len([t for t in self.trades if t["profit_loss"] > 0])
        losing_trades = len([t for t in self.trades if t["profit_loss"] <= 0])

        labels = [
            f"Wins\n{winning_trades} ({winning_trades/len(self.trades)*100:.1f}%)",
            f"Losses\n{losing_trades} ({losing_trades/len(self.trades)*100:.1f}%)",
        ]
        sizes = [winning_trades, losing_trades]
        colors = ["green", "red"]
        explode = (0.1, 0)  # explode the wins slice

        ax2.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        ax2.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        ax2.set_title("Win/Loss Ratio", fontsize=14)

        plt.tight_layout()

        # Save plot
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_pnl_distribution_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _plot_monthly_returns(
        self, strategy_name: str, timestamp: str
    ) -> Optional[str]:
        """
        Plot monthly returns heatmap.

        Args:
            strategy_name: Name of the strategy
            timestamp: Timestamp for filename

        Returns:
            Path to the saved plot or None
        """
        if not self.trades:
            return None

        # Calculate monthly returns
        monthly_returns = {}

        for trade in self.trades:
            exit_date = trade["exit_date"]

            if isinstance(exit_date, str):
                exit_date = pd.to_datetime(exit_date)

            year_month = exit_date.strftime("%Y-%m")

            if year_month not in monthly_returns:
                monthly_returns[year_month] = 0

            monthly_returns[year_month] += trade["profit_loss"]

        if not monthly_returns:
            return None

        # Convert to DataFrame for heatmap
        years = sorted(set(int(ym.split("-")[0]) for ym in monthly_returns.keys()))
        months = range(1, 13)

        # Create empty DataFrame
        data = np.zeros((len(years), 12))

        # Fill with returns (as percentage of initial balance)
        for i, year in enumerate(years):
            for j, month in enumerate(months):
                year_month = f"{year}-{month:02d}"

                if year_month in monthly_returns:
                    data[i, j] = (
                        monthly_returns[year_month] / self.initial_balance
                    ) * 100

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))

        # Create heatmap
        cmap = sns.diverging_palette(
            10, 133, as_cmap=True
        )  # green for positive, red for negative

        # Plot
        heatmap = sns.heatmap(
            data,
            cmap=cmap,
            center=0,
            annot=True,
            fmt=".2f",
            xticklabels=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            yticklabels=years,
            ax=ax,
            cbar_kws={"label": "Return (%)"},
        )

        # Format
        ax.set_title(f"{strategy_name} - Monthly Returns (%)", fontsize=16)
        ax.set_ylabel("Year", fontsize=12)

        plt.tight_layout()

        # Save plot
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_monthly_returns_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _plot_performance_summary(
        self, strategy_name: str, timestamp: str
    ) -> Optional[str]:
        """
        Plot performance summary dashboard.

        Args:
            strategy_name: Name of the strategy
            timestamp: Timestamp for filename

        Returns:
            Path to the saved plot or None
        """
        # Create a summary dashboard with multiple plots
        fig = plt.figure(figsize=(16, 12))

        # Define grid layout
        gs = fig.add_gridspec(3, 3)

        # 1. Cumulative P&L
        ax1 = fig.add_subplot(gs[0, :])

        if self.equity_curve:
            dates = [point["date"] for point in self.equity_curve]
            balance = [point["balance"] for point in self.equity_curve]

            ax1.plot(dates, balance, label="Account Balance", linewidth=2)
            ax1.axhline(
                y=self.initial_balance,
                color="grey",
                linestyle="--",
                label=f"Initial Balance (${self.initial_balance:,.2f})",
            )

            ax1.set_title("Cumulative P&L", fontsize=14)
            ax1.set_ylabel("Account Balance ($)", fontsize=12)
            ax1.legend()
            ax1.grid(True)
            ax1.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

        # 2. FTMO Compliance
        ax2 = fig.add_subplot(gs[1, 0])

        compliance = self._check_ftmo_compliance()
        compliance_data = [
            [
                "Profit Target",
                f"{compliance.get('profit_percentage', 0):.2f}%",
                "Yes" if compliance.get("profit_target_met", False) else "No",
            ],
            [
                "Daily Loss",
                f"{abs(compliance.get('worst_daily_loss', 0)):.2f}%",
                "Yes" if compliance.get("daily_loss_compliant", False) else "No",
            ],
            [
                "Max Drawdown",
                f"{compliance.get('max_drawdown', 0):.2f}%",
                "Yes" if compliance.get("total_loss_compliant", False) else "No",
            ],
            [
                "Trading Days",
                f"{compliance.get('trading_days', 0)}",
                "Yes" if compliance.get("trading_days_compliant", False) else "No",
            ],
        ]

        # Create table
        table = ax2.table(
            cellText=compliance_data,
            colLabels=["Metric", "Value", "Compliant?"],
            loc="center",
            cellLoc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)

        # Color the cells based on compliance
        for i in range(1, len(compliance_data) + 1):
            if compliance_data[i - 1][2] == "Yes":
                table[(i, 2)].set_facecolor("#c8e6c9")  # light green
            else:
                table[(i, 2)].set_facecolor("#ffcdd2")  # light red

        ax2.set_title("FTMO Compliance", fontsize=14)
        ax2.axis("off")

        # 3. Trade Statistics
        ax3 = fig.add_subplot(gs[1, 1])

        stats_data = [
            ["Total Trades", f"{self.metrics.get('total_trades', 0)}"],
            ["Win Rate", f"{self.metrics.get('win_rate', 0) * 100:.2f}%"],
            ["Profit Factor", f"{self.metrics.get('profit_factor', 0):.2f}"],
            ["Avg Profit", f"${self.metrics.get('average_profit', 0):.2f}"],
            ["Avg Loss", f"${self.metrics.get('average_loss', 0):.2f}"],
            ["Expectancy", f"${self.metrics.get('expectancy', 0):.2f}"],
        ]

        table = ax3.table(
            cellText=stats_data,
            colLabels=["Metric", "Value"],
            loc="center",
            cellLoc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)

        ax3.set_title("Trade Statistics", fontsize=14)
        ax3.axis("off")

        # 4. Risk Metrics
        ax4 = fig.add_subplot(gs[1, 2])

        risk_data = [
            ["Max Drawdown", f"{self.metrics.get('max_drawdown', 0):.2f}%"],
            ["Sharpe Ratio", f"{self.metrics.get('sharpe_ratio', 0):.2f}"],
            ["Sortino Ratio", f"{self.metrics.get('sortino_ratio', 0):.2f}"],
            ["Kelly %", f"{self.metrics.get('kelly_percentage', 0) * 100:.2f}%"],
            ["Consecutive Wins", f"{self.metrics.get('consecutive_wins', 0)}"],
            ["Consecutive Losses", f"{self.metrics.get('consecutive_losses', 0)}"],
        ]

        table = ax4.table(
            cellText=risk_data,
            colLabels=["Metric", "Value"],
            loc="center",
            cellLoc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)

        ax4.set_title("Risk Metrics", fontsize=14)
        ax4.axis("off")

        # 5. P&L by Symbol
        ax5 = fig.add_subplot(gs[2, :2])

        # Group trades by symbol
        symbol_pnl = {}

        for trade in self.trades:
            symbol = trade["symbol"]

            if symbol not in symbol_pnl:
                symbol_pnl[symbol] = 0

            symbol_pnl[symbol] += trade["profit_loss"]

        # Create bar chart
        if symbol_pnl:
            symbols = list(symbol_pnl.keys())
            pnls = list(symbol_pnl.values())

            # Sort by P&L
            sorted_indices = np.argsort(pnls)
            symbols = [symbols[i] for i in sorted_indices]
            pnls = [pnls[i] for i in sorted_indices]

            # Set colors
            colors = ["green" if p > 0 else "red" for p in pnls]

            # Create horizontal bar chart
            ax5.barh(symbols, pnls, color=colors)

            ax5.set_title("P&L by Symbol", fontsize=14)
            ax5.set_xlabel("Profit/Loss ($)", fontsize=12)
            ax5.grid(True, axis="x")

            # Add values to bars
            for i, p in enumerate(pnls):
                ax5.text(
                    p + (p * 0.02 if p > 0 else p * 0.02),
                    i,
                    f"${p:.2f}",
                    va="center",
                    fontsize=10,
                )

        # 6. Summary
        ax6 = fig.add_subplot(gs[2, 2])

        final_balance = self.balance
        profit_amount = final_balance - self.initial_balance
        profit_percentage = (
            (profit_amount / self.initial_balance) * 100
            if self.initial_balance > 0
            else 0
        )

        summary_text = (
            f"Strategy: {strategy_name}\n\n"
            f"Initial Balance: ${self.initial_balance:,.2f}\n"
            f"Final Balance: ${final_balance:,.2f}\n"
            f"Net Profit: ${profit_amount:,.2f}\n"
            f"Return: {profit_percentage:.2f}%\n\n"
            f"FTMO Compliant: {'Yes' if compliance.get('is_compliant', False) else 'No'}\n\n"
            f"Total Trades: {self.metrics.get('total_trades', 0)}\n"
            f"Trading Days: {self.metrics.get('trading_days', 0)}\n"
            f"Win Rate: {self.metrics.get('win_rate', 0) * 100:.2f}%\n"
            f"Max Drawdown: {self.metrics.get('max_drawdown', 0):.2f}%\n"
        )

        ax6.text(
            0.5,
            0.5,
            summary_text,
            transform=ax6.transAxes,
            fontsize=12,
            verticalalignment="center",
            horizontalalignment="center",
        )

        ax6.set_title("Performance Summary", fontsize=14)
        ax6.axis("off")

        # Add title
        fig.suptitle(
            f"{strategy_name} - Backtest Performance Summary", fontsize=18, y=0.98
        )

        plt.tight_layout(rect=[0, 0, 1, 0.97])

        # Save plot
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_performance_summary_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _plot_parameter_impact(
        self,
        results: List[Dict[str, Any]],
        param_ranges: Dict[str, List[Any]],
        metric: str,
        strategy_name: str,
    ) -> Optional[str]:
        """
        Plot parameter impact analysis from optimization results.

        Args:
            results: List of optimization results
            param_ranges: Dictionary of parameter ranges
            metric: Optimization metric
            strategy_name: Name of the strategy

        Returns:
            Path to the saved plot or None
        """
        if not results:
            return None

        # Create a figure with subplots for each parameter
        param_names = list(param_ranges.keys())

        if not param_names:
            return None

        # Calculate grid size
        n_params = len(param_names)
        n_cols = min(3, n_params)
        n_rows = (n_params + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))

        # Handle case with only one parameter
        if n_params == 1:
            axes = np.array([axes])

        # Flatten axes for easy iteration
        axes = axes.flatten()

        # Plot for each parameter
        for i, param_name in enumerate(param_names):
            ax = axes[i]

            # Extract parameter values and corresponding metric values
            param_values = []
            metric_values = []

            for result in results:
                if param_name in result["parameters"]:
                    param_values.append(result["parameters"][param_name])
                    metric_values.append(result.get(metric, 0))

            # If no data, skip
            if not param_values:
                ax.set_visible(False)
                continue

            # Group by parameter value for box plot
            param_value_map = {}

            for val, met in zip(param_values, metric_values):
                if val not in param_value_map:
                    param_value_map[val] = []

                param_value_map[val].append(met)

            # Prepare data for box plot
            labels = []
            data = []

            for val in sorted(param_value_map.keys()):
                labels.append(str(val))
                data.append(param_value_map[val])

            # Create box plot
            ax.boxplot(data, labels=labels)

            # For numeric parameters, also plot scatter + trend line
            if all(isinstance(v, (int, float)) for v in param_values):
                ax_right = ax.twinx()

                # Scatter plot
                sc = ax_right.scatter(param_values, metric_values, alpha=0.5, c="red")

                # Try to fit a trend line if we have enough data
                if len(param_values) > 2:
                    try:
                        z = np.polyfit(param_values, metric_values, 1)
                        p = np.poly1d(z)

                        # Plot trend line
                        x_range = np.linspace(min(param_values), max(param_values), 100)
                        ax_right.plot(x_range, p(x_range), "r--", alpha=0.7)
                    except:
                        pass

                # Hide right y-axis labels to avoid clutter
                ax_right.set_yticks([])

            ax.set_title(f"Impact of {param_name}", fontsize=12)
            ax.set_xlabel(param_name, fontsize=10)
            ax.set_ylabel(metric, fontsize=10)
            ax.grid(True, axis="y", alpha=0.3)

            # Rotate x-axis labels if many or long
            if len(labels) > 5 or any(len(str(l)) > 5 for l in labels):
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        # Hide any unused subplots
        for i in range(n_params, len(axes)):
            axes[i].set_visible(False)

        # Add overall title
        fig.suptitle(
            f"{strategy_name} - Parameter Impact Analysis ({metric})", fontsize=16
        )

        plt.tight_layout(rect=[0, 0, 1, 0.97])

        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_parameter_impact_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        return output_path

    def _save_backtest_results(
        self, results: Dict[str, Any], strategy_name: str
    ) -> None:
        """
        Save backtest results to a file.

        Args:
            results: Dictionary with backtest results
            strategy_name: Name of the strategy
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_results_{timestamp}.json"
        )

        # Create a serializable version of the results
        serializable_results = results.copy()

        # Convert trades to serializable format
        trades_list = []

        for trade in self.trades:
            trade_dict = trade.copy()

            # Convert dates to strings
            for date_field in ["entry_date", "exit_date"]:
                if date_field in trade_dict and not isinstance(
                    trade_dict[date_field], str
                ):
                    trade_dict[date_field] = trade_dict[date_field].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

            trades_list.append(trade_dict)

        serializable_results["detailed_trades"] = trades_list

        # Convert equity curve to serializable format
        equity_list = []

        for point in self.equity_curve:
            point_dict = point.copy()

            if "date" in point_dict and not isinstance(point_dict["date"], str):
                point_dict["date"] = point_dict["date"].strftime("%Y-%m-%d %H:%M:%S")

            equity_list.append(point_dict)

        serializable_results["equity_curve"] = equity_list

        # Convert daily stats to serializable format
        daily_stats_list = self.daily_stats.copy()

        serializable_results["daily_stats"] = daily_stats_list

        # Add detailed metrics
        serializable_results["detailed_metrics"] = self.metrics

        # Write to file
        with open(output_path, "w") as f:
            json.dump(serializable_results, f, indent=4)

        self.logger.info(f"Backtest results saved to {output_path}")

    def _save_optimization_results(
        self, results: Dict[str, Any], strategy_name: str
    ) -> None:
        """
        Save optimization results to a file.

        Args:
            results: Dictionary with optimization results
            strategy_name: Name of the strategy
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"{strategy_name}_optimization_{timestamp}.json"
        )

        # Create a serializable version of the results
        serializable_results = results.copy()

        # Remove the raw results object which may not be serializable
        if "raw_results" in serializable_results:
            del serializable_results["raw_results"]

        # Write to file
        with open(output_path, "w") as f:
            json.dump(serializable_results, f, indent=4)

        self.logger.info(f"Optimization results saved to {output_path}")

    def _get_time_step(self, timeframe: str) -> timedelta:
        """
        Get the time step for a timeframe.

        Args:
            timeframe: Timeframe string (M1, H1, D1, etc.)

        Returns:
            Time step as timedelta
        """
        if timeframe == "M1":
            return timedelta(minutes=1)
        elif timeframe == "M5":
            return timedelta(minutes=5)
        elif timeframe == "M15":
            return timedelta(minutes=15)
        elif timeframe == "M30":
            return timedelta(minutes=30)
        elif timeframe == "H1":
            return timedelta(hours=1)
        elif timeframe == "H4":
            return timedelta(hours=4)
        elif timeframe == "D1":
            return timedelta(days=1)
        elif timeframe == "W1":
            return timedelta(weeks=1)
        elif timeframe == "MN1":
            return timedelta(days=30)
        else:
            return timedelta(days=1)  # Default to daily

    def _calculate_max_consecutive(
        self, trades: List[Dict[str, Any]], wins: bool
    ) -> int:
        """
        Calculate maximum consecutive wins or losses.

        Args:
            trades: List of trade dictionaries
            wins: If True, calculate wins, otherwise losses

        Returns:
            Maximum consecutive count
        """
        if not trades:
            return 0

        # Sort trades by exit date
        sorted_trades = sorted(trades, key=lambda t: t["exit_date"])

        max_streak = 0
        current_streak = 0

        for trade in sorted_trades:
            is_win = trade["profit_loss"] > 0

            if is_win == wins:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    def _generate_parameter_combinations(
        self, param_ranges: Dict[str, List[Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate all combinations of parameters for grid search.

        Args:
            param_ranges: Dictionary with parameter ranges

        Returns:
            List of parameter combinations
        """
        import itertools

        # Extract parameter names and values
        param_names = list(param_ranges.keys())
        param_values = list(param_ranges.values())

        # Generate all combinations
        combinations = []

        for values in itertools.product(*param_values):
            combination = dict(zip(param_names, values))
            combinations.append(combination)

        return combinations
