# src/analysis/turtle_optimizer.py
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union

import matplotlib.pyplot as plt

from src.analysis.advanced_backtester import Backtester
from src.utils.config import load_config
from src.utils.logger import Logger

# Configureer logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("turtle_optimizer")


class WalkForwardOptimizer:
    """
    Walk-Forward Optimalisatie voor handelssystemen om overfitting te voorkomen.

    Deze klasse implementeert walk-forward optimalisatie met verschillende in-sample/out-of-sample
    periodes om een robuustere set van parameters te vinden die goed generaliseert naar nieuwe data.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de walk-forward optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = (
            logger
            if logger
            else Logger(
                self.config["logging"].get("log_file", "logs/optimizer_log.csv")
            )
        )

        # Output directory
        self.output_dir = self.config.get("output", {}).get(
            "data_dir", "data/optimization"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        # Visuele stijl instellen
        plt.style.use("ggplot")
        plt.rcParams["figure.figsize"] = (16, 10)

    def optimize(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        param_ranges: Dict[str, List[Any]],
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
        is_period_days: int = 180,
        oos_period_days: int = 60,
        windows: int = 3,
        metric: str = "sharpe_ratio",
        min_trades: int = 10,
        max_workers: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Voer walk-forward optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_ranges : Dict[str, List[Any]]
            Dictionary met parameter namen en mogelijke waarden
        start_date : Union[str, datetime]
            Start datum voor gehele test periode
        end_date : Union[str, datetime]
            Eind datum voor gehele test periode
        is_period_days : int
            Aantal dagen voor in-sample periode
        oos_period_days : int
            Aantal dagen voor out-of-sample periode
        windows : int
            Aantal walk-forward windows
        metric : str
            Prestatiemetric om te optimaliseren
        min_trades : int
            Minimum aantal trades voor een geldige test
        max_workers : Optional[int]
            Maximum aantal workers voor parallellisatie

        Returns:
        --------
        Dict[str, Any] : Resultaten van de walk-forward optimalisatie
        """
        self.logger.log_info(
            f"===== Starten Walk-Forward Optimalisatie: {strategy_name} ====="
        )
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Converteer data naar datetime
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Bereken tijdsperiodes
        total_days = (end_date - start_date).days
        window_size = is_period_days + oos_period_days

        if windows * window_size > total_days:
            windows = total_days // window_size
            self.logger.log_info(
                f"Aangepast aantal windows naar {windows} om binnen datumbereik te passen"
            )

        if windows < 1:
            self.logger.log_info(
                "Datumbereik te klein voor walk-forward optimalisatie", level="ERROR"
            )
            return {"success": False, "error": "Date range too small"}

        # Genereer datumvensters
        date_windows = []
        current_start = start_date

        for i in range(windows):
            is_end = current_start + timedelta(days=is_period_days)
            oos_end = is_end + timedelta(days=oos_period_days)

            if oos_end > end_date:
                oos_end = end_date

            date_windows.append(
                {
                    "window": i + 1,
                    "is_start": current_start,
                    "is_end": is_end,
                    "oos_start": is_end,
                    "oos_end": oos_end,
                }
            )

            current_start = is_end

        self.logger.log_info(f"Gegenereerd {len(date_windows)} walk-forward vensters")

        # Optimaliseer voor elk venster
        window_results = []
        oos_results = []
        best_params_per_window = []

        for window in date_windows:
            window_num = window["window"]
            is_start = window["is_start"].strftime("%Y-%m-%d")
            is_end = window["is_end"].strftime("%Y-%m-%d")
            oos_start = window["oos_start"].strftime("%Y-%m-%d")
            oos_end = window["oos_end"].strftime("%Y-%m-%d")

            self.logger.log_info(
                f"Window {window_num}: In-sample {is_start} tot {is_end}, "
                f"Out-of-sample {oos_start} tot {oos_end}"
            )

            # In-sample optimalisatie
            self.logger.log_info(f"In-sample optimalisatie voor window {window_num}...")

            is_results = self.backtester.run_optimization(
                strategy_name=strategy_name,
                symbols=symbols,
                param_ranges=param_ranges,
                start_date=is_start,
                end_date=is_end,
                metric=metric,
                max_workers=max_workers,
            )

            window_results.append(is_results)

            if not is_results["success"]:
                self.logger.log_info(
                    f"In-sample optimalisatie mislukt voor window {window_num}",
                    level="ERROR",
                )
                continue

            # Get best parameters
            best_params = is_results["best_parameters"]
            best_metrics = is_results["best_metrics"]

            self.logger.log_info(
                f"Beste parameters voor window {window_num}: {best_params}"
            )
            self.logger.log_info(
                f"In-sample {metric}: {best_metrics.get(metric, 0):.4f}"
            )

            # Valideer op out-of-sample periode
            self.logger.log_info(f"Out-of-sample validatie voor window {window_num}...")

            oos_result = self.backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                start_date=oos_start,
                end_date=oos_end,
                parameters=best_params,
                plot_results=False,
            )

            oos_results.append(oos_result)

            if not oos_result["success"]:
                self.logger.log_info(
                    f"Out-of-sample validatie mislukt voor window {window_num}",
                    level="ERROR",
                )
                continue

            oos_metrics = oos_result["metrics"]

            self.logger.log_info(
                f"Out-of-sample {metric}: {oos_metrics.get(metric, 0):.4f}"
            )
            self.logger.log_info(
                f"Out-of-sample net profit: {oos_metrics.get('net_profit_pct', 0):.2f}%"
            )

            # Sla beste params op per window
            best_params_per_window.append(
                {
                    "window": window_num,
                    "is_start": is_start,
                    "is_end": is_end,
                    "oos_start": oos_start,
                    "oos_end": oos_end,
                    "parameters": best_params,
                    "is_metric": best_metrics.get(metric, 0),
                    "oos_metric": oos_metrics.get(metric, 0),
                    "is_profit": best_metrics.get("net_profit_pct", 0),
                    "oos_profit": oos_metrics.get("net_profit_pct", 0),
                    "is_trades": best_metrics.get("total_trades", 0),
                    "oos_trades": oos_metrics.get("total_trades", 0),
                }
            )

        # Analyseer walk-forward resultaten
        if not best_params_per_window:
            self.logger.log_info("Geen geldige resultaten voor analyse", level="ERROR")
            return {"success": False, "error": "No valid results"}

        # Bepaal de meest robuuste parameters
        robust_params = self._find_robust_parameters(
            best_params_per_window, param_ranges
        )

        # Valideer de robuuste parameters op de gehele periode
        self.logger.log_info(
            f"Valideren robuuste parameters {robust_params} op volledige periode..."
        )

        full_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            parameters=robust_params,
            plot_results=True,
        )

        if full_result["success"]:
            full_metrics = full_result["metrics"]
            self.logger.log_info(
                f"Robuuste parameters validatie: {metric}={full_metrics.get(metric, 0):.4f}, "
                f"Net Profit={full_metrics.get('net_profit_pct', 0):.2f}%"
            )

        # Visualiseer en sla resultaten op
        self._plot_walk_forward_results(best_params_per_window, robust_params, metric)
        self._save_optimization_results(
            strategy_name,
            symbols,
            metric,
            best_params_per_window,
            robust_params,
            full_result,
        )

        return {
            "success": True,
            "best_params_per_window": best_params_per_window,
            "robust_params": robust_params,
            "full_result": full_result,
            "metric": metric,
        }

    def _find_robust_parameters(
        self, window_results: List[Dict], param_ranges: Dict[str, List[Any]]
    ) -> Dict[str, Any]:
        """
        Vind robuuste parameters die goed werken over meerdere periodes.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        param_ranges : Dict[str, List[Any]]
            Mogelijke parameter waarden

        Returns:
        --------
        Dict[str, Any] : Meest robuuste parameterset
        """
        if not window_results:
            return {}

        # Extraheer parameter keys
        param_keys = list(param_ranges.keys())

        # Bereken hoe vaak elke parameter waarde voorkomt
        param_frequency = {param: {} for param in param_keys}

        for result in window_results:
            params = result["parameters"]

            for param, value in params.items():
                if param in param_keys:
                    param_frequency[param][value] = (
                        param_frequency[param].get(value, 0) + 1
                    )

        # Kies de meest voorkomende waarde voor elke parameter
        robust_params = {}

        for param, freq in param_frequency.items():
            if freq:
                # De meest voorkomende waarde
                most_common = max(freq.items(), key=lambda x: x[1])[0]
                robust_params[param] = most_common
            else:
                # Fallback: gemiddelde waarde uit bereik
                values = param_ranges[param]
                if values and all(isinstance(v, (int, float)) for v in values):
                    robust_params[param] = sum(values) / len(values)
                elif values:
                    robust_params[param] = values[0]  # Eerste waarde als fallback

        return robust_params

    def _plot_walk_forward_results(
        self, window_results: List[Dict], robust_params: Dict[str, Any], metric: str
    ) -> str:
        """
        Visualiseer walk-forward optimalisatie resultaten.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if not window_results:
            return ""

        # Maak een figuur met 3 subplots
        fig, axs = plt.subplots(
            3, 1, figsize=(14, 16), gridspec_kw={"height_ratios": [2, 1, 2]}
        )

        # 1. Plot IS vs OOS performance
        windows = [r["window"] for r in window_results]
        is_metrics = [r["is_metric"] for r in window_results]
        oos_metrics = [r["oos_metric"] for r in window_results]

        axs[0].plot(windows, is_metrics, "b-", marker="o", label=f"In-Sample {metric}")
        axs[0].plot(
            windows, oos_metrics, "r-", marker="x", label=f"Out-of-Sample {metric}"
        )

        axs[0].set_title(
            f"Walk-Forward Optimalisatie: {metric} per Window", fontsize=16
        )
        axs[0].set_xlabel("Window #", fontsize=14)
        axs[0].set_ylabel(metric, fontsize=14)
        axs[0].grid(True)
        axs[0].legend(fontsize=12)

        # 2. Plot Profit
        is_profit = [r["is_profit"] for r in window_results]
        oos_profit = [r["oos_profit"] for r in window_results]

        axs[1].plot(windows, is_profit, "g-", marker="o", label="In-Sample Profit %")
        axs[1].plot(
            windows, oos_profit, "m-", marker="x", label="Out-of-Sample Profit %"
        )

        axs[1].set_title("Net Profit % per Window", fontsize=16)
        axs[1].set_xlabel("Window #", fontsize=14)
        axs[1].set_ylabel("Net Profit %", fontsize=14)
        axs[1].grid(True)
        axs[1].legend(fontsize=12)

        # 3. Parameter consistency plot
        param_keys = list(robust_params.keys())

        if param_keys:
            param_values = {param: [] for param in param_keys}

            for result in window_results:
                for param in param_keys:
                    param_values[param].append(result["parameters"].get(param, None))

            # Normalize for plotting
            normalized_values = {}
            for param, values in param_values.items():
                if all(isinstance(v, (int, float)) for v in values if v is not None):
                    min_val = min(v for v in values if v is not None)
                    max_val = max(v for v in values if v is not None)

                    if max_val > min_val:
                        normalized_values[param] = [
                            (
                                (v - min_val) / (max_val - min_val)
                                if v is not None
                                else None
                            )
                            for v in values
                        ]
                    else:
                        normalized_values[param] = [
                            0.5 if v is not None else None for v in values
                        ]
                else:
                    # Categorische waarden
                    unique_values = list(set(v for v in values if v is not None))
                    normalized_values[param] = [
                        (
                            unique_values.index(v) / max(1, len(unique_values) - 1)
                            if v in unique_values
                            else None
                        )
                        for v in values
                    ]

            # Plot normalized parameters
            for param, values in normalized_values.items():
                valid_points = [
                    (i, v) for i, v in enumerate(values, 1) if v is not None
                ]
                if valid_points:
                    x, y = zip(*valid_points)
                    axs[2].plot(x, y, "o-", label=param)

            axs[2].set_title("Parameter Consistency Across Windows", fontsize=16)
            axs[2].set_xlabel("Window #", fontsize=14)
            axs[2].set_ylabel("Normalized Parameter Value", fontsize=14)
            axs[2].grid(True)
            axs[2].legend(fontsize=12)

            # Voeg robuuste parameters toe als text box
            param_text = "Robust Parameters:\n" + "\n".join(
                [f"{k}: {v}" for k, v in robust_params.items()]
            )
            axs[2].text(
                0.02,
                0.02,
                param_text,
                transform=axs[2].transAxes,
                fontsize=12,
                bbox=dict(facecolor="white", alpha=0.7),
                verticalalignment="bottom",
            )

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"walk_forward_results_{timestamp}.png"
        )
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _save_optimization_results(
        self,
        strategy_name: str,
        symbols: List[str],
        metric: str,
        window_results: List[Dict],
        robust_params: Dict[str, Any],
        full_result: Dict,
    ) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        full_result : Dict
            Resultaat van backtest met robuuste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        results = {
            "strategy": strategy_name,
            "symbols": symbols,
            "metric": metric,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "window_results": window_results,
            "robust_params": robust_params,
            "full_metrics": (
                full_result.get("metrics", {})
                if full_result.get("success", False)
                else {}
            ),
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"walk_forward_{strategy_name}_{timestamp}.json"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.log_info(f"Walk-forward resultaten opgeslagen als {output_path}")
        return output_path


class BayesianOptimizer:
    """
    Bayesiaanse Optimalisatie voor het efficiënt zoeken naar optimale strategie parameters.

    Deze klasse implementeert Bayesiaanse optimalisatie om efficiënter dan grid search
    optimale parameters te vinden door een surrogaat model te gebruiken.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de Bayesiaanse optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = (
            logger
            if logger
            else Logger(
                self.config["logging"].get("log_file", "logs/bayesian_opt_log.csv")
            )
        )

        # Output directory
        self.output_dir = self.config.get("output", {}).get(
            "data_dir", "data/optimization"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        try:
            # Probeer scikit-optimize te importeren
            import skopt

            self.skopt_available = True
        except ImportError:
            self.logger.log_info(
                "scikit-optimize niet beschikbaar. Installeer met: pip install scikit-optimize",
                level="WARNING",
            )
            self.skopt_available = False

        # Visuele stijl instellen
        plt.style.use("ggplot")
        plt.rcParams["figure.figsize"] = (16, 10)

    def optimize(
        self,
        strategy_name: str,
        symbols: List[str],
        timeframe: str,
        param_space: Dict[str, Any],
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
        n_calls: int = 30,
        n_initial_points: int = 10,
        metric: str = "sharpe_ratio",
    ) -> Dict[str, Any]:
        """
        Voer Bayesiaanse optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_space : Dict[str, Any]
            Dictionary met parameter namen en bereiken:
            Bijvoorbeeld: {'entry_period': (10, 60), 'atr_multiplier': (1.0, 3.0)}
            Voor categorische: {'swing_mode': ['True', 'False']}
        start_date : Union[str, datetime]
            Start datum
        end_date : Union[str, datetime]
            Eind datum
        n_calls : int
            Aantal evaluatiepunten
        n_initial_points : int
            Aantal initiële random punten
        metric : str
            Prestatiemetric om te optimaliseren (bijv. 'sharpe_ratio', 'profit_factor', etc.)

        Returns:
        --------
        Dict[str, Any] : Resultaten van de optimalisatie
        """
        if not self.skopt_available:
            self.logger.log_info(
                "Kan Bayesiaanse optimalisatie niet uitvoeren zonder scikit-optimize",
                level="ERROR",
            )
            return {"success": False, "error": "scikit-optimize not available"}

        from skopt import gp_minimize
        from skopt.space import Real, Integer, Categorical
        from skopt.utils import use_named_args

        self.logger.log_info(
            f"===== Starten Bayesiaanse Optimalisatie: {strategy_name} ====="
        )
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Definieer parameter space in skopt formaat
        dimensions = []
        dimension_names = []

        for param_name, param_def in param_space.items():
            dimension_names.append(param_name)

            if isinstance(param_def, tuple) and len(param_def) == 2:
                low, high = param_def
                if isinstance(low, int) and isinstance(high, int):
                    dimensions.append(Integer(low, high, name=param_name))
                elif isinstance(low, (int, float)) and isinstance(high, (int, float)):
                    dimensions.append(Real(low, high, name=param_name))
            elif isinstance(param_def, list):
                dimensions.append(Categorical(param_def, name=param_name))

        # Conversie van strings naar booleans voor categorische opties
        def process_param_value(param_name, value):
            if param_name in param_space and isinstance(param_space[param_name], list):
                if value == "True":
                    return True
                elif value == "False":
                    return False
            return value

        # Definieer evaluatiefunctie
        @use_named_args(dimensions=dimensions)
        def evaluate_params(**params):
            # Converteer categoriën indien nodig
            processed_params = {
                name: process_param_value(name, value) for name, value in params.items()
            }

            self.logger.log_info(f"Evalueren parameters: {processed_params}")

            try:
                result = self.backtester.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    parameters=processed_params,
                    plot_results=False,
                )

                if not result["success"]:
                    return -100  # Penalty voor mislukte backtests

                metrics = result["metrics"]

                # We minimaliseren, dus negeer de metric
                metric_value = metrics.get(metric, 0)

                if metric in [
                    "sharpe_ratio",
                    "profit_factor",
                    "net_profit",
                    "net_profit_pct",
                    "win_rate",
                ]:
                    return -metric_value  # Negeer omdat we maximaliseren
                else:
                    return metric_value  # Voor metrics die we minimaliseren

            except Exception as e:
                self.logger.log_info(
                    f"Fout bij evalueren parameters: {str(e)}", level="ERROR"
                )
                return -100  # Penalty voor errors

        # Voer optimalisatie uit
        start_time = time.time()

        result = gp_minimize(
            evaluate_params,
            dimensions=dimensions,
            n_calls=n_calls,
            n_initial_points=n_initial_points,
            acq_func="EI",  # Expected Improvement
            noise=0.01,
            verbose=True,
        )

        elapsed = time.time() - start_time
        self.logger.log_info(f"Optimalisatie voltooid in {elapsed:.2f} seconden")

        # Analyseer resultaten
        best_params = dict(zip(dimension_names, result.x))

        # Converteer categoriën indien nodig
        best_params = {
            name: process_param_value(name, value)
            for name, value in best_params.items()
        }

        # Negatief van de score voor metrics die we maximaliseren
        best_score = (
            -result.fun
            if metric
            in [
                "sharpe_ratio",
                "profit_factor",
                "net_profit",
                "net_profit_pct",
                "win_rate",
            ]
            else result.fun
        )

        self.logger.log_info(f"Beste parameters gevonden: {best_params}")
        self.logger.log_info(f"Beste {metric}: {best_score:.4f}")

        # Run final backtest met beste parameters
        final_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            parameters=best_params,
            plot_results=True,
        )

        # Visualiseer resultaten
        self._plot_optimization_results(result, dimension_names, metric)
        self._save_optimization_results(
            strategy_name,
            symbols,
            metric,
            result,
            dimension_names,
            best_params,
            final_result,
        )

        return {
            "success": True,
            "best_parameters": best_params,
            "best_score": best_score,
            "optimization_result": result,
            "final_backtest": final_result,
        }

    def _plot_optimization_results(
        self, result, dimension_names: List[str], metric: str
    ) -> str:
        """
        Visualiseer optimalisatie resultaten.

        Parameters:
        -----------
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        try:
            import skopt
            from skopt.plots import plot_convergence, plot_objective, plot_evaluations

            # Maak één figuur met 3 subplots
            fig, axs = plt.subplots(3, 1, figsize=(14, 18))

            # 1. Convergentie plot
            plot_convergence(result, ax=axs[0])
            if metric in [
                "sharpe_ratio",
                "profit_factor",
                "net_profit",
                "net_profit_pct",
                "win_rate",
            ]:
                # Converteer y-as labels voor metrics die we maximaliseren
                axs[0].set_ylabel(f"Negative {metric}")

            axs[0].set_title(f"Convergence Plot for {metric} Optimization", fontsize=16)

            # 2. Objective plot (alleen voor 1-2 dimensies)
            if len(dimension_names) <= 2:
                try:
                    plot_objective(result, ax=axs[1])
                    axs[1].set_title(f"Objective Surface for {metric}", fontsize=16)
                except Exception as e:
                    self.logger.log_info(
                        f"Kon objective plot niet maken: {str(e)}", level="WARNING"
                    )
                    axs[1].set_visible(False)
            else:
                axs[1].set_visible(False)

            # 3. Evaluations plot
            try:
                plot_evaluations(result, ax=axs[2])
                axs[2].set_title("Parameter Evaluations", fontsize=16)
            except Exception as e:
                self.logger.log_info(
                    f"Kon evaluations plot niet maken: {str(e)}", level="WARNING"
                )
                axs[2].set_visible(False)

            plt.tight_layout()

            # Sla plot op
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(
                self.output_dir, f"bayesian_optimization_{timestamp}.png"
            )
            plt.savefig(output_path, dpi=150)
            plt.close()

            return output_path

        except Exception as e:
            self.logger.log_info(
                f"Fout bij plotten optimalisatie resultaten: {str(e)}", level="ERROR"
            )
            return ""

    def _save_optimization_results(
        self,
        strategy_name: str,
        symbols: List[str],
        metric: str,
        result,
        dimension_names: List[str],
        best_params: Dict[str, Any],
        final_result: Dict,
    ) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        best_params : Dict[str, Any]
            Beste gevonden parameters
        final_result : Dict
            Resultaat van backtest met beste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        optimization_data = {
            "strategy": strategy_name,
            "symbols": symbols,
            "metric": metric,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "best_params": best_params,
            "best_score": (
                -result.fun
                if metric
                in [
                    "sharpe_ratio",
                    "profit_factor",
                    "net_profit",
                    "net_profit_pct",
                    "win_rate",
                ]
                else result.fun
            ),
            "function_calls": result.nfev,
            "full_metrics": (
                final_result.get("metrics", {})
                if final_result.get("success", False)
                else {}
            ),
        }

        # Voeg alle evaluaties toe
        evaluations = []
        for i, (x, y) in enumerate(zip(result.x_iters, result.func_vals)):
            evaluations.append(
                {
                    "iteration": i + 1,
                    "parameters": dict(zip(dimension_names, x)),
                    "score": (
                        -y
                        if metric
                        in [
                            "sharpe_ratio",
                            "profit_factor",
                            "net_profit",
                            "net_profit_pct",
                            "win_rate",
                        ]
                        else y
                    ),
                }
            )

        optimization_data["evaluations"] = evaluations

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            self.output_dir, f"bayesian_opt_{strategy_name}_{timestamp}.json"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(optimization_data, f, indent=2, default=str)

        self.logger.log_info(
            f"Bayesiaanse optimalisatie resultaten opgeslagen als {output_path}"
        )
        return output_path


def run_walk_forward_optimization():
    """Voer walk-forward optimalisatie uit vanaf command line."""
    print("Walk-Forward Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config["logging"].get("log_file", "logs/wf_opt_log.csv")
    logger = Logger(log_file)
    logger.log_info("====== Sophy Walk-Forward Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = WalkForwardOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config["mt5"].get("symbols", ["EURUSD"])
    timeframe = config["mt5"].get("timeframe", "H4")
    strategy_name = config["strategy"].get("name", "turtle")

    # Definieer parameter bereiken voor turtle strategy
    param_ranges = {
        "entry_period": [20, 40, 60],
        "exit_period": [10, 20, 30],
        "atr_period": [14, 20, 30],
        "atr_multiplier": [1.5, 2.0, 2.5, 3.0],
        "swing_mode": [True, False],
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_ranges=param_ranges,
        start_date=start_date,
        end_date=end_date,
        is_period_days=180,  # 6 maanden in-sample
        oos_period_days=60,  # 2 maanden out-of-sample
        windows=3,  # 3 windows
        metric="sharpe_ratio",
    )

    if results["success"]:
        logger.log_info("Walk-Forward Optimalisatie voltooid")
        logger.log_info(f"Robuuste parameters gevonden: {results['robust_params']}")
    else:
        logger.log_info(
            f"Walk-Forward Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}",
            level="ERROR",
        )

    logger.log_info("====== Sophy Walk-Forward Optimalisatie Ended ======")


def run_bayesian_optimization():
    """Voer Bayesiaanse optimalisatie uit vanaf command line."""
    print("Bayesiaanse Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config["logging"].get("log_file", "logs/bayes_opt_log.csv")
    logger = Logger(log_file)
    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = BayesianOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config["mt5"].get("symbols", ["EURUSD"])
    timeframe = config["mt5"].get("timeframe", "H4")
    strategy_name = config["strategy"].get("name", "turtle")

    # Definieer parameter bereiken voor turtle strategy
    param_space = {
        "entry_period": (10, 60),
        "exit_period": (5, 30),
        "atr_period": (5, 30),
        "atr_multiplier": (1.0, 4.0),
        "swing_mode": ["True", "False"],
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_space=param_space,
        start_date=start_date,
        end_date=end_date,
        n_calls=30,  # 30 evaluatiepunten
        n_initial_points=10,  # 10 initiële random punten
        metric="sharpe_ratio",
    )

    if results["success"]:
        logger.log_info("Bayesiaanse Optimalisatie voltooid")
        logger.log_info(f"Beste parameters gevonden: {results['best_parameters']}")
        logger.log_info(f"Beste score: {results['best_score']:.4f}")
    else:
        logger.log_info(
            f"Bayesiaanse Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}",
            level="ERROR",
        )

    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Ended ======")


if __name__ == "__main__":
    # Kies welke optimalisatiemethode je wilt uitvoeren
    run_walk_forward_optimization()  # run_bayesian_optimization()  # Uncomment om Bayesiaanse optimalisatie uit te voeren
