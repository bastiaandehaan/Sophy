# src/analysis/backtrader_integration.py
import os
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd


class BacktestingManager:
    """
    Integration manager for Backtrader backtesting in the Sophy framework.
    """

    def __init__(self, config: Dict[str, Any], logger):
        """
        Initialize the backtesting manager.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger

        # Initialize Backtrader adapter
        from src.analysis.backtrader_adapter import BacktraderAdapter

        self.backtrader_adapter = BacktraderAdapter(config, logger)

    def run_backtest(self, strategy_name: str, symbols: List[str], start_date: str,
                     end_date: str, timeframe: str = "D1", parameters: Dict = None,
                     plot_results: bool = True, ) -> Dict[str, Any]:
        """
        Run a backtest with the specified settings.

        Args:
            strategy_name: Name of the strategy to test
            symbols: List of trading symbols
            start_date: Start date for the backtest (YYYY-MM-DD)
            end_date: End date for the backtest (YYYY-MM-DD)
            timeframe: Timeframe for the data
            parameters: Custom parameters for the strategy
            plot_results: Whether to generate plots

        Returns:
            Dictionary with backtest results
        """
        # Import strategy factory here to avoid circular imports
        from src.strategy.strategy_factory import StrategyFactory

        # Load the specified strategy
        strategy = StrategyFactory.create_strategy(strategy_name, connector=None,
                                                   # Backtester will create mock connector
                                                   risk_manager=None,
                                                   # Backtester will create mock risk manager
                                                   logger=self.logger,
                                                   config=self.config, )

        self.logger.log_info(f"Running backtest with {strategy_name}")

        # Load data for each symbol
        for symbol in symbols:
            data = self._load_historical_data(symbol, start_date, end_date, timeframe)
            self.backtrader_adapter.add_data(symbol, data, timeframe)

        # Run backtest
        results = self.backtrader_adapter.run_backtest(strategy,
                                                       debug=self.config.get("debug",
                                                                             False),
                                                       risk_per_trade=self.config.get(
                                                           "risk", {}).get(
                                                           "risk_per_trade", 0.01), )

        if plot_results:
            # Generate plots
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.config.get("output", {}).get("backtest_results_dir",
                                                           "backtest_results")
            os.makedirs(output_dir, exist_ok=True)

            plot_path = os.path.join(output_dir,
                                     f"{strategy_name}_backtest_plot_{timestamp}.png")
            self.backtrader_adapter.plot_results(plot_path)

        return results

    def _load_historical_data(self, symbol: str, start_date: str, end_date: str,
                              timeframe: str) -> pd.DataFrame:
        """
        Load historical data for a symbol.

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

        # Define data directory
        data_dir = os.path.join("data")
        file_name = f"{symbol}_{timeframe}.csv"
        file_path = os.path.join(data_dir, file_name)

        if os.path.exists(file_path):
            try:
                # Load data from CSV
                data = pd.read_csv(file_path)
                data["date"] = pd.to_datetime(data["date"])
                data = data[(data["date"] >= start_dt) & (data["date"] <= end_dt)]
                return data
            except Exception as e:
                self.logger.log_info(f"Error loading data for {symbol}: {e}")
                return self._generate_test_data(symbol, start_dt, end_dt)
        else:
            # Generate test data if file not found
            self.logger.log_info(
                f"Data file for {symbol} not found, generating test data")
            return self._generate_test_data(symbol, start_dt, end_dt)

    def _generate_test_data(self, symbol: str, start_dt, end_dt) -> pd.DataFrame:
        """
        Generate test OHLCV data with enough history for strategies.

        Args:
            symbol: Trading symbol
            start_dt: Start datetime
            end_dt: End datetime

        Returns:
            DataFrame with synthetic OHLCV data
        """
        import numpy as np

        # Bereken hoeveel extra warmup dagen we nodig hebben voor indicatoren
        # Voor turtle strategie hebben we minstens entry_period bars nodig (typisch 20-60)
        warmup_days = 100  # Ruime marge voor alle strategieën

        # Genereer date range met warmup
        extended_start = start_dt - pd.Timedelta(days=warmup_days)
        dates = pd.date_range(extended_start, end_dt, freq="D")

        # Genereer random prices met een lichte trend
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
            {"date": dates, "open": opens, "high": highs, "low": lows, "close": closes,
             "volume": volumes, })

        # Voeg opzettelijke breakouts toe voor turtle strategie
        # Dit zorgt ervoor dat de strategie interessante handelssignalen ziet
        for i in range(3):
            breakout_idx = int(len(data) * 0.25 * (i + 1))  # Op 25%, 50%, 75% punt
            if breakout_idx + 5 < len(data):
                # Creëer een opwaartse breakout
                data.loc[data.index[breakout_idx:breakout_idx + 5], 'high'] *= 1.03
                data.loc[data.index[breakout_idx:breakout_idx + 5], 'close'] *= 1.02

                # Creëer ook enkele neerwaartse breakouts
                reversal_idx = breakout_idx + 15
                if reversal_idx + 5 < len(data):
                    data.loc[data.index[reversal_idx:reversal_idx + 5], 'low'] *= 0.97
                    data.loc[data.index[reversal_idx:reversal_idx + 5], 'close'] *= 0.98

        return data

    def run_walk_forward_optimization(self, strategy_name: str, symbols: List[str],
                                      start_date: str, end_date: str,
                                      timeframe: str = "D1",
                                      window_size_days: int = 180,
                                      step_size_days: int = 30,
                                      param_grid: Dict[str, List] = None) -> Dict[
        str, Any]:
        """
        Uitvoeren van walk-forward optimalisatie.

        Args:
            strategy_name: Naam van de strategie
            symbols: Lijst van symbolen
            start_date: Startdatum (YYYY-MM-DD)
            end_date: Einddatum (YYYY-MM-DD)
            timeframe: Tijdsframe voor de data
            window_size_days: Grootte van elk window in dagen
            step_size_days: Aantal dagen om vooruit te schuiven
            param_grid: Dictionary met parameter ranges voor optimalisatie

        Returns:
            Dictionary met resultaten per window
        """
        # Converteer datums naar datetime
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)

        # Bepaal de windows
        windows = []
        current_start = start_dt

        while current_start + pd.Timedelta(days=window_size_days) <= end_dt:
            window_end = current_start + pd.Timedelta(days=window_size_days)
            windows.append((current_start, window_end))
            current_start += pd.Timedelta(days=step_size_days)

        # Als er geen parameters gegeven zijn, gebruik standaardwaarden
        if param_grid is None:
            param_grid = {
                "entry_period": [20, 30, 40, 50, 60],
                "exit_period": [10, 15, 20],
                "atr_multiplier": [1.5, 2.0, 2.5, 3.0]
            }

        # Resultaten per window bijhouden
        results = {}
        best_params = {}

        # Voor elk window, optimaliseer parameters
        for i, (window_start, window_end) in enumerate(windows):
            window_name = f"Window_{i + 1}"
            self.logger.log_info(
                f"Optimalisatie voor {window_name}: {window_start.date()} tot {window_end.date()}")

            # Train/test splitsing (80/20)
            train_days = int(window_size_days * 0.8)
            train_end = window_start + pd.Timedelta(days=train_days)

            # Resultaten voor dit window
            window_results = {
                "train_period": (
                window_start.strftime("%Y-%m-%d"), train_end.strftime("%Y-%m-%d")),
                "test_period": (
                train_end.strftime("%Y-%m-%d"), window_end.strftime("%Y-%m-%d")),
                "train_results": [],
                "test_results": None,
                "best_params": None
            }

            # Optimalisatie op trainingset
            # Simpele grid search implementatie
            best_train_sharpe = -float('inf')
            best_params_window = None

            # Voor elke parametercombinatie
            # (Hier zou je itertools.product kunnen gebruiken om alle combinaties te genereren)
            # Dit is een vereenvoudigde implementatie
            for entry_period in param_grid["entry_period"]:
                for exit_period in param_grid["exit_period"]:
                    for atr_multiplier in param_grid["atr_multiplier"]:
                        # Stel parameters in
                        params = {
                            "strategy": {
                                "entry_period": entry_period,
                                "exit_period": exit_period,
                                "atr_multiplier": atr_multiplier
                            }
                        }

                        # Maak tijdelijke config met deze parameters
                        temp_config = self.config.copy()
                        temp_config.update(params)

                        # Voer backtest uit op trainingsperiode
                        try:
                            backtest_mgr = BacktestingManager(temp_config, self.logger)
                            train_result = backtest_mgr.run_backtest(
                                strategy_name=strategy_name,
                                symbols=symbols,
                                start_date=window_start.strftime("%Y-%m-%d"),
                                end_date=train_end.strftime("%Y-%m-%d"),
                                timeframe=timeframe,
                                plot_results=False
                            )

                            # Bewaar resultaten
                            train_sharpe = train_result.get("sharpe_ratio", 0)

                            # Voeg resultaat toe aan trainingresultaten
                            window_results["train_results"].append({
                                "params": params["strategy"],
                                "sharpe": train_sharpe,
                                "profit_pct": train_result.get("profit_percentage", 0),
                                "win_rate": train_result.get("win_rate", 0),
                                "max_drawdown": train_result.get("max_drawdown", 0)
                            })

                            # Check of dit de beste parameters zijn
                            if train_sharpe > best_train_sharpe:
                                best_train_sharpe = train_sharpe
                                best_params_window = params["strategy"]

                        except Exception as e:
                            self.logger.log_info(f"Fout bij optimalisatie: {e}",
                                                 level="ERROR")

            # Sla beste parameters op
            window_results["best_params"] = best_params_window

            # Test de beste parameters op de testset
            if best_params_window:
                # Maak config met beste parameters
                test_config = self.config.copy()
                test_config.update({"strategy": best_params_window})

                # Voer backtest uit op testperiode
                try:
                    backtest_mgr = BacktestingManager(test_config, self.logger)
                    test_result = backtest_mgr.run_backtest(
                        strategy_name=strategy_name,
                        symbols=symbols,
                        start_date=train_end.strftime("%Y-%m-%d"),
                        end_date=window_end.strftime("%Y-%m-%d"),
                        timeframe=timeframe,
                        plot_results=False
                    )

                    # Bewaar testresultaten
                    window_results["test_results"] = {
                        "sharpe": test_result.get("sharpe_ratio", 0),
                        "profit_pct": test_result.get("profit_percentage", 0),
                        "win_rate": test_result.get("win_rate", 0),
                        "max_drawdown": test_result.get("max_drawdown", 0),
                        "total_trades": test_result.get("total_trades", 0)
                    }

                    # Log resultaten
                    self.logger.log_info(
                        f"Window {i + 1} resultaten: "
                        f"Sharpe: {window_results['test_results']['sharpe']:.2f}, "
                        f"Winst: {window_results['test_results']['profit_pct']:.2f}%, "
                        f"Win Rate: {window_results['test_results']['win_rate']:.2f}%"
                    )

                except Exception as e:
                    self.logger.log_info(f"Fout bij testen van beste parameters: {e}",
                                         level="ERROR")

            # Sla resultaten op voor dit window
            results[window_name] = window_results
            best_params[window_name] = best_params_window

        # Analyseer consistentie van parameters over windows
        param_stability = self._analyze_parameter_stability(best_params)

        # Voeg overall statistieken toe
        overall_results = {
            "windows": results,
            "parameter_stability": param_stability,
            "out_of_sample_performance": self._calculate_out_of_sample_stats(results),
            "best_overall_params": self._find_best_overall_params(results)
        }

        return overall_results

    def _analyze_parameter_stability(self, best_params: Dict[str, Dict]) -> Dict[
        str, Any]:
        """
        Analyseer de stabiliteit van parameters over verschillende windows.

        Args:
            best_params: Dictionary met beste parameters per window

        Returns:
            Dictionary met stabiliteits-metrics
        """
        # Een eenvoudige implementatie die kijkt naar variatie in parameters
        if not best_params:
            return {"stable": False, "reason": "Geen parameters beschikbaar"}

        # Verzamel alle parameterwaarden
        param_values = {}
        for window, params in best_params.items():
            if params:
                for param_name, value in params.items():
                    if param_name not in param_values:
                        param_values[param_name] = []
                    param_values[param_name].append(value)

        # Bereken variatie voor elke parameter
        param_variations = {}
        for param_name, values in param_values.items():
            if values:
                param_variations[param_name] = {
                    "min": min(values),
                    "max": max(values),
                    "mean": sum(values) / len(values),
                    "range_pct": (max(values) - min(values)) / max(values) * 100 if max(
                        values) > 0 else 0,
                    "values": values
                }

        # Bepaal stabiliteit
        unstable_params = []
        for param_name, stats in param_variations.items():
            # Als range meer dan 50% is van de maximumwaarde, beschouw als onstabiel
            if stats["range_pct"] > 50:
                unstable_params.append(param_name)

        return {
            "stable": len(unstable_params) == 0,
            "unstable_params": unstable_params,
            "variations": param_variations
        }

    def _calculate_out_of_sample_stats(self, results: Dict[str, Dict]) -> Dict[
        str, float]:
        """
        Bereken statistieken over out-of-sample prestaties.

        Args:
            results: Dictionary met resultaten per window

        Returns:
            Dictionary met out-of-sample statistieken
        """
        # Verzamel test resultaten van alle windows
        test_profits = []
        test_sharpes = []
        test_win_rates = []
        test_drawdowns = []

        for window_name, window_data in results.items():
            if window_data.get("test_results"):
                test_profits.append(window_data["test_results"].get("profit_pct", 0))
                test_sharpes.append(window_data["test_results"].get("sharpe", 0))
                test_win_rates.append(window_data["test_results"].get("win_rate", 0))
                test_drawdowns.append(
                    window_data["test_results"].get("max_drawdown", 0))

        # Return lege resultaten als geen testdata beschikbaar is
        if not test_profits:
            return {
                "avg_profit_pct": 0,
                "avg_sharpe": 0,
                "avg_win_rate": 0,
                "avg_drawdown": 0,
                "profit_consistency": 0,
                "windows_profitable": 0
            }

        # Bereken statistieken
        avg_profit = sum(test_profits) / len(test_profits)
        avg_sharpe = sum(test_sharpes) / len(test_sharpes)
        avg_win_rate = sum(test_win_rates) / len(test_win_rates)
        avg_drawdown = sum(test_drawdowns) / len(test_drawdowns)

        # Bereken consistentie (hoeveel % van windows was winstgevend)
        profitable_windows = sum(1 for p in test_profits if p > 0)
        profit_consistency = profitable_windows / len(test_profits) * 100

        return {
            "avg_profit_pct": avg_profit,
            "avg_sharpe": avg_sharpe,
            "avg_win_rate": avg_win_rate,
            "avg_drawdown": avg_drawdown,
            "profit_consistency": profit_consistency,
            "windows_profitable": profitable_windows
        }

    def _find_best_overall_params(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Vind de beste overall parameters op basis van out-of-sample prestaties.

        Args:
            results: Dictionary met resultaten per window

        Returns:
            Dictionary met beste parameters en prestatiemetrieken
        """
        # Verzamel resultaten per parameterset
        param_results = {}

        for window_name, window_data in results.items():
            if window_data.get("best_params") and window_data.get("test_results"):
                # Converteer params naar een tuple om te gebruiken als dictionary key
                param_key = tuple(
                    sorted((k, v) for k, v in window_data["best_params"].items()))

                if param_key not in param_results:
                    param_results[param_key] = {
                        "params": window_data["best_params"],
                        "test_results": [],
                        "windows": []
                    }

                param_results[param_key]["test_results"].append(
                    window_data["test_results"])
                param_results[param_key]["windows"].append(window_name)

        # Vind de parameterset met hoogste gemiddelde Sharpe ratio
        best_avg_sharpe = -float('inf')
        best_params = None

        for param_key, data in param_results.items():
            test_sharpes = [r.get("sharpe", 0) for r in data["test_results"]]
            avg_sharpe = sum(test_sharpes) / len(test_sharpes) if test_sharpes else 0

            if avg_sharpe > best_avg_sharpe:
                best_avg_sharpe = avg_sharpe
                best_params = data["params"]

        # Als geen beste parameters gevonden, return None
        if not best_params:
            return None

        # Return beste parameters met prestatiemetrieken
        return {
            "parameters": best_params,
            "metrics": {
                "avg_out_of_sample_sharpe": best_avg_sharpe,
                "frequency": len([w for pk, data in param_results.items()
                                  if data["params"] == best_params
                                  for w in data["windows"]]) / sum(
                    len(data["windows"]) for data in param_results.values())
            }
        }
