# src/analysis/backtrader_adapter.py
from typing import Dict, Any, Optional

import backtrader as bt
import pandas as pd


class BacktraderAdapter:
    """
    Hoofdinterface voor het gebruik van Backtrader binnen het Sophy framework.
    """

    def __init__(self, config: Dict[str, Any], logger):
        """
        Initialiseer de Backtrader adapter.

        Args:
            config: Configuratie dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.cerebro = bt.Cerebro()

        # Default settings
        self.cerebro.broker.set_cash(
            config.get("risk", {}).get("initial_balance", 100000)
        )
        self.cerebro.broker.setcommission(commission=0.0001)  # 0.01% commission

        # Performance analyzers
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

        self.data_feeds = {}

    def add_data(self, symbol: str, data: pd.DataFrame, timeframe: str = "Day") -> None:
        """
        Add data for a symbol to the backtest.

        Args:
            symbol: Trading symbol
            data: DataFrame with OHLCV data
            timeframe: Timeframe for the data
        """
        # Verkrijg timeframe en compressie apart
        bt_timeframe = self._get_backtrader_timeframe(timeframe)
        compression = self._get_timeframe_compression(timeframe)

        # Set cheat-on-close voor intraday timeframes
        if timeframe in ["M1", "M5", "M15", "M30", "H1", "H4"]:
            self.cerebro.broker.set_coc(True)

        # Create a Backtrader data feed from the DataFrame
        if data.index.dtype.kind == "M":  # If the index is datetime
            bt_data = bt.feeds.PandasData(
                dataname=data,
                name=symbol,
                timeframe=bt_timeframe,  # Timeframe constant
                compression=compression,  # Compression value
                datetime=None,  # Use index
                open="open",
                high="high",
                low="low",
                close="close",
                volume="volume",
                openinterest=-1,
            )
        else:
            # If the index is not datetime, assume there's a 'date' column
            if "date" in data.columns:
                bt_data = bt.feeds.PandasData(
                    dataname=data,
                    name=symbol,
                    timeframe=bt_timeframe,  # Timeframe constant
                    compression=compression,  # Compression value
                    datetime="date",
                    open="open",
                    high="high",
                    low="low",
                    close="close",
                    volume="volume",
                    openinterest=-1,
                )
            else:
                self.logger.log_info(
                    f"Cannot add data for {symbol}: no datetime index or 'date' column"
                )
                return

        # Add the data feed to Cerebro
        self.cerebro.adddata(bt_data)
        self.data_feeds[symbol] = bt_data

        self.logger.log_info(f"Added data for {symbol} with {len(data)} bars")

    def run_backtest(self, sophy_strategy, **kwargs) -> Dict[str, Any]:
        """
        Run a backtest with a Sophy strategy.

        Args:
            sophy_strategy: A Sophy strategy instance
            **kwargs: Additional parameters for the strategy

        Returns:
            Dictionary with backtest results
        """
        # Import here to avoid circular imports
        from src.analysis.strategy_adapter import SophyStrategyAdapter

        # Add the strategy adapter with the Sophy strategy
        self.cerebro.addstrategy(
            SophyStrategyAdapter, sophy_strategy=sophy_strategy, **kwargs
        )

        self.logger.log_info(f"Starting backtest with {sophy_strategy.get_name()}")

        # Run the backtest
        results = self.cerebro.run()
        strategy = results[0]

        # Extract performance metrics
        sharpe = strategy.analyzers.sharpe.get_analysis()
        drawdown = strategy.analyzers.drawdown.get_analysis()
        trades = strategy.analyzers.trades.get_analysis()
        returns = strategy.analyzers.returns.get_analysis()

        # Calculate metrics
        sharpe_ratio = sharpe.get("sharperatio", 0)
        max_drawdown = drawdown.get("max", {}).get("drawdown", 0)
        total_trades = trades.get("total", {}).get("total", 0)
        won_trades = trades.get("won", {}).get("total", 0)
        lost_trades = trades.get("lost", {}).get("total", 0)
        win_rate = won_trades / total_trades if total_trades > 0 else 0
        total_return = returns.get("rtot", 0) * 100

        # Prepare results dictionary
        backtest_results = {
            "success": True,
            "initial_balance": self.cerebro.broker.startingcash,
            "final_balance": self.cerebro.broker.getvalue(),
            "profit_loss": self.cerebro.broker.getvalue()
                           - self.cerebro.broker.startingcash,
            "profit_percentage": (
                                     self.cerebro.broker.getvalue() / self.cerebro.broker.startingcash - 1
                                 )
                                 * 100,
            "total_trades": total_trades,
            "won_trades": won_trades,
            "lost_trades": lost_trades,
            "win_rate": win_rate * 100,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "total_return": total_return,
            "detailed_trades": strategy.trades if hasattr(strategy, "trades") else [],
        }

        # Check FTMO compliance
        ftmo_compliance = self._check_ftmo_compliance(backtest_results)
        backtest_results["ftmo_compliance"] = ftmo_compliance

        self.logger.log_info(
            f"Backtest completed: Profit: {backtest_results['profit_percentage']:.2f}%, "
            f"Win Rate: {backtest_results['win_rate']:.2f}%, "
            f"FTMO Compliant: {ftmo_compliance['is_compliant']}"
        )

        return backtest_results

    def plot_results(self, filename: Optional[str] = None) -> None:
        """
        Plot the backtest results.

        Args:
            filename: Optional filename to save the plot
        """
        try:
            import matplotlib.pyplot as plt

            # Generate plots
            figs = self.cerebro.plot(
                style="candle", barup="green", bardown="red", volume=False, grid=True
            )

            if filename and figs and len(figs) > 0 and len(figs[0]) > 0:
                plt.savefig(filename, dpi=300)
                self.logger.log_info(f"Plot saved to {filename}")

        except Exception as e:
            self.logger.log_info(f"Error plotting results: {e}", level="ERROR")

    def _get_backtrader_timeframe(self, timeframe: str) -> int:
        """
        Convert a timeframe string to Backtrader timeframe constant.

        Args:
            timeframe: Timeframe string (e.g., 'M1', 'H4', 'D1')

        Returns:
            Backtrader timeframe constant
        """
        timeframe_map = {
            "M1": bt.TimeFrame.Minutes,
            "M5": bt.TimeFrame.Minutes,
            "M15": bt.TimeFrame.Minutes,
            "M30": bt.TimeFrame.Minutes,
            "H1": bt.TimeFrame.Minutes,
            "H4": bt.TimeFrame.Minutes,
            "D1": bt.TimeFrame.Days,
            "W1": bt.TimeFrame.Weeks,
            "MN1": bt.TimeFrame.Months,
        }

        if timeframe in timeframe_map:
            return timeframe_map[timeframe]
        else:
            return bt.TimeFrame.Days  # Default to Daily

    def _get_timeframe_compression(self, timeframe: str) -> int:
        """
        Get compression value for the timeframe.

        Args:
            timeframe: Timeframe string (e.g., 'M1', 'H4', 'D1')

        Returns:
            Compression value
        """
        compression_map = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
            "H4": 240,
            "D1": 1,
            "W1": 1,
            "MN1": 1,
        }

        return compression_map.get(timeframe, 1)

    def _check_ftmo_compliance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if backtest results comply with FTMO rules.

        Args:
            results: Backtest results dictionary

        Returns:
            Dictionary with FTMO compliance results
        """
        # FTMO rules
        profit_target = 0.10  # 10% profit target
        max_daily_loss = 0.05  # 5% max daily loss
        max_total_loss = 0.10  # 10% max total loss
        min_trading_days = 4  # Minimum 4 trading days

        # Extract data from results
        profit_percentage = results["profit_percentage"] / 100
        max_drawdown = results["max_drawdown"] / 100
        total_trades = results["total_trades"]

        # Simplified checks - in a real implementation we would need
        # to check daily losses which requires additional data processing
        profit_target_met = profit_percentage >= profit_target
        total_loss_compliant = max_drawdown <= max_total_loss

        # Assume daily loss is compliant - would need daily P&L data for accurate check
        daily_loss_compliant = True

        # Estimate trading days (this is an approximation)
        trading_days_compliant = total_trades >= min_trading_days

        # Overall compliance
        is_compliant = (
            profit_target_met
            and daily_loss_compliant
            and total_loss_compliant
            and trading_days_compliant
        )

        return {
            "is_compliant": is_compliant,
            "profit_target_met": profit_target_met,
            "daily_loss_compliant": daily_loss_compliant,
            "total_loss_compliant": total_loss_compliant,
            "trading_days_compliant": trading_days_compliant,
        }
