# turtle_trader/analysis/optimizer.py
import multiprocessing as mp
from itertools import product
from typing import Dict, List, Callable


class BacktestOptimizer:
    """Optimizes strategy parameters through extensive backtesting"""

    def __init__(self, backtester, config, logger):
        self.backtester = backtester
        self.config = config
        self.logger = logger

    def grid_search(self,
                    strategy: Callable,
                    param_grid: Dict[str, List],
                    symbols: List[str],
                    start_date: datetime,
                    end_date: datetime,
                    metric: str = 'sharpe_ratio',
                    use_parallel: bool = True) -> Dict:
        """
        Perform grid search optimization of parameters

        Args:
            strategy: Strategy to optimize
            param_grid: Dictionary of parameter names and possible values
            symbols: List of symbols to test on
            start_date: Start of backtest period
            end_date: End of backtest period
            metric: Performance metric to optimize
            use_parallel: Whether to use parallel processing

        Returns:
            Dict with best parameters and presentation metrics
        """
        # Generate all parameter combinations
        param_keys = list(param_grid.keys())
        param_values = list(param_grid.values())
        param_combinations = list(product(*param_values))

        self.logger.info(f"Starting grid search with {len(param_combinations)} parameter combinations")

        # Storage for results
        results = []

        # Define evaluation function
        def evaluate_params(params_idx):
            params_dict = {param_keys[i]: param_combinations[params_idx][i] for i in range(len(param_keys))}
            self.logger.info(f"Testing parameters: {params_dict}")

            # Run backtest with these parameters
            backtest_results = self.backtester.run_backtest(
                strategy=strategy,
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                parameters=params_dict,
                use_parallel=False  # Already parallelized at the parameter level
            )

            # Calculate presentation metrics
            metrics = self._calculate_performance_metrics(backtest_results)

            return {
                'parameters': params_dict,
                'metrics': metrics
            }

        # Execute evaluation in parallel if requested
        if use_parallel:
            with mp.Pool(processes=mp.cpu_count()) as pool:
                results = pool.map(evaluate_params, range(len(param_combinations)))
        else:
            results = [evaluate_params(i) for i in range(len(param_combinations))]

        # Find best parameters according to specified metric
        best_result = max(results, key=lambda x: x['metrics'].get(metric, -float('inf')))

        return best_result
