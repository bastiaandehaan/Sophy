# src/analysis/walk_forward.py
"""
Walk-Forward Optimalisatie Framework voor het Sophy Trading System.

Dit module implementeert Walk-Forward Analysis (WFA), een methode om overfitting
te voorkomen bij het optimaliseren van trading strategieën. In WFA wordt historische
data opgedeeld in opeenvolgende 'in-sample' (IS) en 'out-of-sample' (OOS) periodes:
1. Optimaliseer strategie parameters op IS data
2. Valideer deze parameters op OOS data
3. Schuif het window verder en herhaal

Dit zorgt voor een robuustere set van parameters die beter generaliseert naar nieuwe data.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import concurrent.futures
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

from src.utils.config import load_config
from src.utils.logger import Logger
from src.strategy.strategy_factory import StrategyFactory
from src.risk.risk_manager import RiskManager
from src.analysis.advanced_backtester import Backtester

try:
    from src.ftmo.validator import FTMOValidator
except ImportError:
    # Als we de gecombineerde validator.py hebben
    pass


class WalkForwardOptimizer:
    """
    Walk-Forward Optimalisatie voor het valideren van trading strategieën.

    Deze klasse implementeert walk-forward analyse door historische data op te splitsen
    in in-sample (IS) en out-of-sample (OOS) periodes. Parameters worden geoptimaliseerd
    op IS data en vervolgens gevalideerd op OOS data.

    Dit vermindert overfitting en zorgt voor robuustere strategie parameters.
    """

    def __init__(self, config: Optional[Dict] = None, logger: Optional[Logger] = None):
        """
        Initialiseer de Walk-Forward Optimizer.

        Args:
            config: Configuratie dictionary (als None, dan wordt standaard config geladen)
            logger: Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        log_file = self.config.get("logging", {}).get("log_file", "logs/wfo_log.csv")
        self.logger = logger if logger else Logger(log_file)

        # Stel output directory in
        self.output_dir = os.path.join(
            self.config.get("output", {}).get("data_dir", "data"),
            "walk_forward"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        # Setup plotting stijl
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Maak backtester voor optimalisatie en backtests
        self.backtester = Backtester(self.config, self.logger)

        self.logger.log_info("Walk-Forward Optimizer geïnitialiseerd")

    def _ensure_datetime(self, date_value: Union[str, datetime]) -> datetime:
        """Convert string date to datetime if needed"""
        if isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d")
        return date_value

    def _generate_windows(
        self,
        start_date: datetime,
        end_date: datetime,
        window_size_days: int,
        oos_size_days: int,
        step_size_days: int
    ) -> List[Dict[str, datetime]]:
        """
        Genereer windows voor walk-forward analyse.

        Args:
            start_date: Start datum voor gehele analyse
            end_date: Eind datum voor gehele analyse
            window_size_days: Grootte van elk window in dagen (in-sample)
            oos_size_days: Grootte van out-of-sample periode in dagen
            step_size_days: Aantal dagen om vooruit te stappen voor elk window

        Returns:
            List van dictionaries met start/einddatums voor elk window
        """
        windows = []

        # Totale periode in dagen
        total_period = (end_date - start_date).days

        # Controleer of we tenminste één window kunnen maken
        if total_period < window_size_days + oos_size_days:
            self.logger.log_info(
                f"Te korte periode ({total_period} dagen) voor window size ({window_size_days}) + OOS ({oos_size_days})",
                level="ERROR"
            )
            return []

        # Maak windows vanaf startdatum
        is_start = start_date
        window_idx = 1

        while True:
            # Bereken in-sample einddatum
            is_end = is_start + timedelta(days=window_size_days)

            # Bereken out-of-sample start- en einddatum
            oos_start = is_end
            oos_end = oos_start + timedelta(days=oos_size_days)

            # Stop als we voorbij de einddatum gaan
            if oos_end > end_date:
                break

            windows.append({
                "window": window_idx,
                "is_start": is_start,
                "is_end": is_end,
                "oos_start": oos_start,
                "oos_end": oos_end
            })

            # Update voor volgende window
            is_start = is_start + timedelta(days=step_size_days)
            window_idx += 1

        return windows

    def _optimize_parameters(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        param_ranges: Dict[str, List[Any]],
        start_date: datetime,
        end_date: datetime,
        metric: str,
        min_trades: int,
        max_threads: int
    ) -> Dict[str, Any]:
        """
        Optimaliseer strategie parameters op een bepaalde periode.

        Args:
            strategy_name: Naam van de trading strategie
            symbols: Lijst met handelssymbolen
            timeframe: Timeframe voor de analyse
            param_ranges: Dictionary met parameter ranges voor optimalisatie
            start_date: Start datum voor optimalisatie
            end_date: Eind datum voor optimalisatie
            metric: Prestatie-metric voor optimalisatie
            min_trades: Minimum aantal trades voor geldige backtest
            max_threads: Maximum aantal threads voor parallelle optimalisatie

        Returns:
            Dictionary met optimalisatieresultaten
        """
        self.logger.log_info(
            f"Optimaliseren parameters voor {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Genereer alle mogelijke parametercombinaties
        param_keys = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        param_combinations = list(itertools.product(*param_values))

        self.logger.log_info(
            f"Evalueren van {len(param_combinations)} parametercombinaties")

        # Evalueer alle combinaties (parallel indien mogelijk)
        results = []

        if max_threads > 1:
            # Parallelle uitvoering
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_threads) as executor:
                futures = []

                for params in param_combinations:
                    param_dict = dict(zip(param_keys, params))
                    futures.append(
                        executor.submit(
                            self._evaluate_parameters,
                            strategy_name,
                            symbols,
                            timeframe,
                            param_dict,
                            start_date,
                            end_date,
                            metric,
                            min_trades
                        )
                    )

                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        if result["valid"]:
                            results.append(result)
                    except Exception as e:
                        self.logger.log_info(f"Fout bij parameter evaluatie: {e}",
                                             level="ERROR")
        else:
            # Sequentiële uitvoering
            for params in param_combinations:
                param_dict = dict(zip(param_keys, params))
                result = self._evaluate_parameters(
                    strategy_name,
                    symbols,
                    timeframe,
                    param_dict,
                    start_date,
                    end_date,
                    metric,
                    min_trades
                )
                if result["valid"]:
                    results.append(result)

        # Sorteer resultaten op de optimalisatie-metric
        if results:
            results.sort(key=lambda x: x["metrics"][metric], reverse=True)
            best_result = results[0]

            return {
                "success": True,
                "best_params": best_result["parameters"],
                "metrics": best_result["metrics"],
                "all_results": results
            }
        else:
            return {
                "success": False,
                "error": "Geen valide parametercombinaties gevonden"
            }

    def _evaluate_parameters(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        parameters: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
        metric: str,
        min_trades: int
    ) -> Dict[str, Any]:
        """
        Evalueer één set parameters met een backtest.

        Args:
            strategy_name: Naam van de trading strategie
            symbols: Lijst met handelssymbolen
            timeframe: Timeframe voor de analyse
            parameters: Dictionary met strategie parameters
            start_date: Start datum voor backtest
            end_date: Eind datum voor backtest
            metric: Prestatie-metric voor evaluatie
            min_trades: Minimum aantal trades voor geldige backtest

        Returns:
            Dictionary met evaluatieresultaten
        """
        # Voer backtest uit
        backtest_result = self._backtest_parameters(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            parameters=parameters,
            start_date=start_date,
            end_date=end_date,
            metric=metric
        )

        if not backtest_result["success"]:
            return {
                "valid": False,
                "parameters": parameters,
                "error": backtest_result.get("error", "Backtest mislukt")
            }

        metrics = backtest_result["metrics"]
        trades = backtest_result.get("trades", [])

        # Controleer of we voldoende trades hebben
        if len(trades) < min_trades:
            return {
                "valid": False,
                "parameters": parameters,
                "metrics": metrics,
                "error": f"Te weinig trades: {len(trades)} (minimum: {min_trades})"
            }

        return {
            "valid": True,
            "parameters": parameters,
            "metrics": metrics,
            "num_trades": len(trades)
        }

    def _backtest_parameters(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        parameters: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
        metric: str
    ) -> Dict[str, Any]:
        """
        Voer een backtest uit met specifieke parameters.

        Args:
            strategy_name: Naam van de trading strategie
            symbols: Lijst met handelssymbolen
            timeframe: Timeframe voor de analyse
            parameters: Dictionary met strategie parameters
            start_date: Start datum voor backtest
            end_date: Eind datum voor backtest
            metric: Prestatie-metric voor evaluatie

        Returns:
            Dictionary met backtestresultaten
        """
        # Converteer datums naar strings voor backtester
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        # Voer backtest uit via backtester
        try:
            # Kopieer config en voeg parameters toe
            config = self.config.copy()

            # Update de backtest configuratie
            if "backtest" not in config:
                config["backtest"] = {}
            config["backtest"]["start_date"] = start_str
            config["backtest"]["end_date"] = end_str

            # Update de strategie configuratie
            if "strategy" not in config:
                config["strategy"] = {}
            config["strategy"].update(parameters)
            config["strategy"]["name"] = strategy_name

            # Zet symbolen en timeframe
            if "mt5" not in config:
                config["mt5"] = {}
            config["mt5"]["symbols"] = symbols
            config["mt5"]["timeframe"] = timeframe

            # Voer backtest uit
            result = self.backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                parameters=parameters,
                timeframe=timeframe,
                start_date=start_str,
                end_date=end_str
            )

            return result
        except Exception as e:
            self.logger.log_info(f"Fout bij backtest: {e}", level="ERROR")
            return {"success": False, "error": str(e)}

    def _find_robust_parameters(
        self,
        window_results: List[Dict[str, Any]],
        param_ranges: Dict[str, List[Any]]
    ) -> Dict[str, Any]:
        """
        Bepaal robuuste parameters op basis van window resultaten.

        Args:
            window_results: Lijst met resultaten voor elk window
            param_ranges: Dictionary met parameter ranges voor optimalisatie

        Returns:
            Dictionary met robuuste parameters
        """
        # Filter op succesvolle windows
        successful_windows = [w for w in window_results if w.get("success", False)]

        if not successful_windows:
            self.logger.log_info(
                "Geen succesvolle windows om robuuste parameters uit te bepalen",
                level="ERROR")
            # Gebruik gemiddelde waarden als fallback
            return {k: self._get_parameter_average(v) for k, v in param_ranges.items()}

        # Verzamel parameters per window
        all_params = {}
        for window in successful_windows:
            params = window.get("parameters", {})
            for key, value in params.items():
                if key not in all_params:
                    all_params[key] = []
                all_params[key].append(value)

        # Bepaal meest voorkomende waarde voor elke parameter
        robust_params = {}
        for key, values in all_params.items():
            if not values:
                continue

            # Voor numerieke parameters nemen we het gemiddelde
            if all(isinstance(v, (int, float)) for v in values):
                # Rond af naar dichtsbijzijnde waarde in param_ranges indien beschikbaar
                avg_value = sum(values) / len(values)
                if key in param_ranges:
                    valid_values = param_ranges[key]
                    closest_value = min(valid_values, key=lambda x: abs(x - avg_value))
                    robust_params[key] = closest_value
                else:
                    robust_params[key] = avg_value
            # Voor categorische parameters nemen we meest voorkomende waarde
            else:
                from collections import Counter
                counter = Counter(values)
                robust_params[key] = counter.most_common(1)[0][0]

        return robust_params

    def _get_parameter_average(self, values: List[Any]) -> Any:
        """Helper om gemiddelde waarde te bepalen, ondersteunt zowel numeriek als categorisch"""
        if not values:
            return None

        # Voor numerieke parameters
        if all(isinstance(v, (int, float)) for v in values):
            avg = sum(values) / len(values)
            # Rond af naar int indien alle waarden ints zijn
            if all(isinstance(v, int) for v in values):
                return int(round(avg))
            return avg

        # Voor categorische parameters (eerste waarde als fallback)
        return values[0]

    def _visualize_results(
        self,
        window_results: List[Dict[str, Any]],
        robust_params: Dict[str, Any],
        full_results: Dict[str, Any],
        metric: str
    ) -> str:
        """
        Visualiseer de resultaten van walk-forward optimalisatie.

        Args:
            window_results: Lijst met resultaten voor elk window
            robust_params: Dictionary met robuuste parameters
            full_results: Resultaten van backtest over volledige periode
            metric: Gebruikte prestatie-metric

        Returns:
            Pad naar opgeslagen visualisatie
        """
        # Filter op succesvolle windows
        successful_windows = [w for w in window_results if w.get("success", False)]

        if not successful_windows:
            self.logger.log_info("Geen succesvolle windows om te visualiseren",
                                 level="WARNING")
            return ""

        # Creëer figuur met subplots
        fig = plt.figure(figsize=(18, 16))
        gs = GridSpec(4, 2, figure=fig, height_ratios=[1.5, 1, 1, 1.5])

        # 1. Plot metric values (IS vs OOS)
        ax1 = fig.add_subplot(gs[0, :])

        # Extract data
        windows = [w["window"] for w in successful_windows]
        is_metrics = [w["is_metrics"].get(metric, 0) for w in successful_windows]
        oos_metrics = [w["oos_metrics"].get(metric, 0) for w in successful_windows]

        # Plot IS vs OOS metrics
        ax1.plot(windows, is_metrics, "b-o", label=f"In-Sample {metric}")
        ax1.plot(windows, oos_metrics, "r-o", label=f"Out-of-Sample {metric}")

        # Reference line for full period
        if full_results.get("success", False):
            full_metric = full_results.get("metrics", {}).get(metric, 0)
            ax1.axhline(y=full_metric, color="green", linestyle="--",
                        label=f"Volledige periode: {full_metric:.4f}")

        ax1.set_title(f"{metric} per Window (In-Sample vs Out-of-Sample)", fontsize=16)
        ax1.set_xlabel("Window", fontsize=14)
        ax1.set_ylabel(metric, fontsize=14)
        ax1.grid(True)
        ax1.legend(fontsize=12)

        # 2. Plot total returns
        ax2 = fig.add_subplot(gs[1, :])

        is_returns = [w["is_metrics"].get("total_return", 0) for w in
                      successful_windows]
        oos_returns = [w["oos_metrics"].get("total_return", 0) for w in
                       successful_windows]

        ax2.plot(windows, is_returns, "g-o", label="In-Sample Rendement (%)")
        ax2.plot(windows, oos_returns, "m-o", label="Out-of-Sample Rendement (%)")

        # Reference line for full period
        if full_results.get("success", False):
            full_return = full_results.get("metrics", {}).get("total_return", 0)
            ax2.axhline(y=full_return, color="green", linestyle="--",
                        label=f"Volledige periode: {full_return:.2f}%")

        ax2.set_title("Rendement per Window (%)", fontsize=16)
        ax2.set_xlabel("Window", fontsize=14)
        ax2.set_ylabel("Rendement (%)", fontsize=14)
        ax2.grid(True)
        ax2.legend(fontsize=12)

        # 3. Plot parameter consistency
        ax3 = fig.add_subplot(gs[2, :])

        # Collect parameter values across windows
        param_values = {}
        for w in successful_windows:
            for param, value in w.get("parameters", {}).items():
                if param not in param_values:
                    param_values[param] = []
                param_values[param].append(value)

        # Normalize parameter values for comparison
        normalized_values = {}
        for param, values in param_values.items():
            if all(isinstance(v, (int, float)) for v in values):
                min_val = min(values)
                max_val = max(values)
                if max_val > min_val:
                    normalized_values[param] = [(v - min_val) / (max_val - min_val) for
                                                v in values]
                else:
                    normalized_values[param] = [0.5 for _ in values]

        # Plot normalized parameters
        for param, values in normalized_values.items():
            if len(values) == len(windows):
                ax3.plot(windows, values, "o-", label=param)

        ax3.set_title("Parameter Consistency Across Windows", fontsize=16)
        ax3.set_xlabel("Window", fontsize=14)
        ax3.set_ylabel("Normalized Value", fontsize=14)
        ax3.grid(True)
        ax3.legend(fontsize=10, loc="upper right")

        # 4. Summary table with robust parameters
        ax4 = fig.add_subplot(gs[3, :])
        ax4.axis("off")

        # Create summary table content
        table_data = [["Parameter", "Robuuste Waarde", "Range"]]
        for param, value in robust_params.items():
            param_range = str(param_ranges.get(param, ["N/A"]))
            table_data.append([param, str(value), param_range])

        # Add full metrics to table
        if full_results.get("success", False):
            metrics = full_results.get("metrics", {})
            table_data.append(["", "", ""])
            table_data.append(["Metrics (Volledige Periode)", "Waarde", ""])
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    table_data.append([key, f"{value:.4f}", ""])

        # Create table
        table = ax4.table(
            cellText=table_data,
            loc="center",
            cellLoc="center",
            colWidths=[0.4, 0.3, 0.3]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)

        # Style table
        for (i, j), cell in table.get_celld().items():
            if i == 0 or (i == len(table_data) - 3 and j == 0):
                cell.set_text_props(weight="bold")
                cell.set_facecolor("#4472C4")
                cell.set_text_props(color="white")

        # Set overall title for figure
        plt.suptitle("Walk-Forward Optimization Results", fontsize=20, y=0.98)

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Save and return file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"wfo_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def run(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        param_ranges: Dict[str, List[Any]],
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
        window_size_days: int = 90,
        oos_size_days: int = 30,
        step_size_days: int = 30,
        metric: str = "sharpe_ratio",
        min_trades: int = 10,
        max_optimization_threads: int = 1,
        visualize: bool = True
    ) -> Dict[str, Any]:
        """
        Voer een complete walk-forward optimalisatie analyse uit.

        Args:
            strategy_name: Naam van de trading strategie
            symbols: Lijst met handelssymbolen
            timeframe: Timeframe voor de analyse (H1, H4, D1, etc.)
            param_ranges: Dictionary met parameter ranges voor optimalisatie
              bijv. {"entry_period": [20, 40, 60], "atr_multiplier": [1.5, 2.0, 2.5]}
            start_date: Start datum voor analyse (string YYYY-MM-DD of datetime)
            end_date: Eind datum voor analyse (string YYYY-MM-DD of datetime)
            window_size_days: Grootte van elk window in dagen (in-sample)
            oos_size_days: Grootte van out-of-sample periode in dagen
            step_size_days: Aantal dagen om vooruit te stappen voor elk window
            metric: Prestatie-metric die geoptimaliseerd moet worden
              opties: sharpe_ratio, profit_factor, total_return, win_rate
            min_trades: Minimum aantal trades voor een geldige backtest
            max_optimization_threads: Maximum aantal threads voor parallelle optimalisatie
            visualize: Genereer visualisaties van resultaten

        Returns:
            Dictionary met optimalisatieresultaten
        """
        # Converteer datums naar datetime objecten indien nodig
        start_date = self._ensure_datetime(start_date)
        end_date = self._ensure_datetime(end_date)

        self.logger.log_info(f"Starting Walk-Forward Analysis voor {strategy_name}")
        self.logger.log_info(
            f"Periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")
        self.logger.log_info(
            f"Window: {window_size_days} dagen, OOS: {oos_size_days} dagen, Stap: {step_size_days} dagen")
        self.logger.log_info(f"Parameters: {param_ranges}")

        # Genereer alle window periodes
        windows = self._generate_windows(start_date, end_date, window_size_days,
                                         oos_size_days, step_size_days)

        if not windows:
            self.logger.log_info(
                "Geen valide windows gegenereerd. Controleer datumrange en windowgroottes.",
                level="ERROR")
            return {"success": False, "error": "Geen valide windows"}

        self.logger.log_info(f"Gegenereerd {len(windows)} analyze windows")

        # Doorloop alle windows
        window_results = []

        for i, window in enumerate(windows):
            self.logger.log_info(f"Verwerken window {i + 1}/{len(windows)}: "
                                 f"IS {window['is_start'].strftime('%Y-%m-%d')} - {window['is_end'].strftime('%Y-%m-%d')}, "
                                 f"OOS {window['oos_start'].strftime('%Y-%m-%d')} - {window['oos_end'].strftime('%Y-%m-%d')}")

            # 1. Optimaliseer parameters op in-sample data
            is_results = self._optimize_parameters(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                param_ranges=param_ranges,
                start_date=window['is_start'],
                end_date=window['is_end'],
                metric=metric,
                min_trades=min_trades,
                max_threads=max_optimization_threads
            )

            if not is_results["success"]:
                self.logger.log_info(f"Optimalisatie mislukt voor window {i + 1}",
                                     level="WARNING")
                window_results.append({
                    "window": i + 1,
                    "is_start": window['is_start'],
                    "is_end": window['is_end'],
                    "oos_start": window['oos_start'],
                    "oos_end": window['oos_end'],
                    "success": False,
                    "error": is_results.get("error", "Onbekende fout")
                })
                continue

            best_params = is_results["best_params"]
            is_metrics = is_results["metrics"]

            self.logger.log_info(f"Beste parameters: {best_params}")
            self.logger.log_info(f"IS {metric}: {is_metrics.get(metric, 0):.4f}")

            # 2. Valideer parameters op out-of-sample data
            oos_results = self._backtest_parameters(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                parameters=best_params,
                start_date=window['oos_start'],
                end_date=window['oos_end'],
                metric=metric
            )

            if not oos_results["success"]:
                self.logger.log_info(f"OOS validatie mislukt voor window {i + 1}",
                                     level="WARNING")
                window_results.append({
                    "window": i + 1,
                    "is_start": window['is_start'],
                    "is_end": window['is_end'],
                    "oos_start": window['oos_start'],
                    "oos_end": window['oos_end'],
                    "parameters": best_params,
                    "is_metrics": is_metrics,
                    "success": False,
                    "error": oos_results.get("error",
                                             "Onbekende fout bij OOS validatie")
                })
                continue

            oos_metrics = oos_results["metrics"]

            self.logger.log_info(f"OOS {metric}: {oos_metrics.get(metric, 0):.4f}")
            self.logger.log_info(
                f"OOS rendement: {oos_metrics.get('total_return', 0):.2f}%")

            # Volledig resultaat opslaan
            window_results.append({
                "window": i + 1,
                "is_start": window['is_start'],
                "is_end": window['is_end'],
                "oos_start": window['oos_start'],
                "oos_end": window['oos_end'],
                "parameters": best_params,
                "is_metrics": is_metrics,
                "oos_metrics": oos_metrics,
                "success": True
            })

        # Analyseer resultaten om robuuste parameters te vinden
        if not any(r.get("success", False) for r in window_results):
            self.logger.log_info("Geen succesvol window gevonden", level="ERROR")
            return {"success": False,
                    "error": "Geen enkel window succesvol geoptimaliseerd"}

        robust_params = self._find_robust_parameters(window_results, param_ranges)
        self.logger.log_info(f"Robuuste parameters gevonden: {robust_params}")

        # Valideer robuuste parameters op de volledige periode
        full_results = self._backtest_parameters(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            parameters=robust_params,
            start_date=start_date,
            end_date=end_date,
            metric=metric
        )

        # Genereer visualisaties indien gewenst
        if visualize:
            plot_path = self._visualize_results(
                window_results=window_results,
                robust_params=robust_params,
                full_results=full_results,
                metric=metric
            )
            self.logger.log_info(f"Resultaten gevisualiseerd in {plot_path}")

        # Compileer eindresultaat en sla het op
        output_data = {
            "success": True,
            "strategy": strategy_name,
            "symbols": symbols,
            "timeframe": timeframe,
            "period": {
                "start": start_date.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d')
            },
            "windows": [
                {k: (v.strftime('%Y-%m-%d') if isinstance(v, datetime) else v)
                 for k, v in r.items()}
                for r in window_results
            ],
            "robust_parameters": robust_params,
            "full_period_metrics": full_results.get("metrics", {}),
            "optimization_metric": metric,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Sla resultaten op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir,
                                   f"wfo_{strategy_name}_{timestamp}.json")

        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4, default=str)

        self.logger.log_info(
            f"Walk-Forward Analyse resultaten opgeslagen in {output_file}")

        return output_data
