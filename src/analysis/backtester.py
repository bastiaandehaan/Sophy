# src/analysis/backtester.py
import os
from typing import Dict, Any, Optional, Union

import backtrader as bt
import pandas as pd


class SophyBacktester:
    """Interface voor Backtrader in het Sophy Framework."""

    def __init__(self, config: Dict[str, Any], logger: Any):
        """
        Initialiseer de backtester.

        Args:
            config: Configuratie dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.cerebro = bt.Cerebro()

        # Standaard instellingen
        initial_cash = config.get("initial_balance", 100000)
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=0.0001)  # 0.01%

        # Voeg analyzers toe
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

        self.logger.log_info("Backtester geïnitialiseerd")

    def add_data(self, df: pd.DataFrame, symbol: str, timeframe: str = "D1") -> None:
        """
        Voeg data toe aan de backtest.

        Args:
            df: DataFrame met OHLCV data
            symbol: Handelssymbool
            timeframe: Timeframe van de data
        """
        # Controleer en prepareer DataFrame
        if not isinstance(df.index, pd.DatetimeIndex):
            if "date" in df.columns:
                df = df.set_index("date")
            else:
                self.logger.log_info(
                    f"DataFrame voor {symbol} heeft geen datetime index",
                    level="WARNING",
                )
                return

        # Maak een datafeed
        data = bt.feeds.PandasData(
            dataname=df,
            name=symbol,
            datetime=None,  # Gebruik index
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest=-1,
        )

        # Voeg toe aan cerebro
        self.cerebro.adddata(data)
        self.logger.log_info(f"Data toegevoegd voor {symbol} met {len(df)} bars")

    def run(
        self, strategy_class: Any, strategy_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Voer backtest uit.

        Args:
            strategy_class: Backtrader strategie klasse
            strategy_params: Parameters voor de strategie

        Returns:
            Dict met backtest resultaten
        """
        # Voeg strategie toe
        if strategy_params:
            self.cerebro.addstrategy(strategy_class, **strategy_params)
        else:
            self.cerebro.addstrategy(strategy_class)

        # Voer backtest uit
        self.logger.log_info(
            f"Backtest starten met strategie: {strategy_class.__name__}"
        )
        results = self.cerebro.run()

        # Verwerk resultaten
        if not results:
            self.logger.log_info(
                "Backtest resulteerde in geen strategie instanties", level="ERROR"
            )
            return {"success": False, "message": "Geen resultaten"}

        # Verwerk analyses
        strategy = results[0]

        # Sharpe ratio
        sharpe = strategy.analyzers.sharpe.get_analysis()
        sharpe_ratio = sharpe.get("sharperatio", 0.0)

        # Drawdown
        dd = strategy.analyzers.drawdown.get_analysis()
        max_drawdown = dd.get("max", {}).get("drawdown", 0.0)

        # Trades
        trades_analysis = strategy.analyzers.trades.get_analysis()
        total_trades = trades_analysis.get("total", 0)
        won_trades = trades_analysis.get("won", {}).get("total", 0)

        # Bereken rendement
        final_value = self.cerebro.broker.getvalue()
        initial_value = self.config.get("initial_balance", 100000)
        profit_loss = final_value - initial_value
        return_pct = (final_value / initial_value - 1) * 100

        # Stel resultaat samen
        result = {
            "success": True,
            "initial_balance": initial_value,
            "final_balance": final_value,
            "profit_loss": profit_loss,
            "return_pct": return_pct,
            "max_drawdown_pct": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "total_trades": total_trades,
            "won_trades": won_trades,
            "win_rate": (won_trades / total_trades * 100) if total_trades > 0 else 0.0,
        }

        self.logger.log_info(
            f"Backtest voltooid: {return_pct:.2f}% rendement, {total_trades} trades"
        )
        return result

    def plot(self, filename: Optional[str] = None) -> None:
        """
        Genereer een plot van de backtest resultaten.

        Args:
            filename: Pad om plot op te slaan, indien None wordt geen bestand opgeslagen
        """
        try:
            # Maak output directory indien nodig
            if filename:
                os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Genereer plot
            figs = self.cerebro.plot(
                style="candle", barup="green", bardown="red", grid=True, volume=False
            )

            # Sla op indien filename gegeven
            if filename and figs and len(figs) > 0 and len(figs[0]) > 0:
                figs[0][0].savefig(filename, dpi=300)
                self.logger.log_info(f"Plot opgeslagen als {filename}")
        except Exception as e:
            self.logger.log_info(f"Fout bij plotten: {str(e)}", level="ERROR")


# Convenience functie
def run_backtest(
    strategy_class: Any,
    data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
    symbol: Optional[str] = None,
    strategy_params: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
    logger: Optional[Any] = None,
    plot: bool = True,
    plot_filename: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Eenvoudige functie om een backtest uit te voeren.

    Args:
        strategy_class: Backtrader strategie klasse
        data: DataFrame of dict van DataFrames per symbool
        symbol: Symbool voor de data (indien DataFrame)
        strategy_params: Parameters voor de strategie
        config: Configuratie dictionary
        logger: Logger instance
        plot: Of een plot gegenereerd moet worden
        plot_filename: Bestandsnaam voor plot

    Returns:
        Dict met backtest resultaten
    """
    from src.utils.config import load_config
    from src.utils.logger import Logger

    # Laad config en logger indien niet meegegeven
    if config is None:
        config = load_config()

    if logger is None:
        logger = Logger("logs/backtest.log")

    # Maak backtester
    backtester = SophyBacktester(config, logger)

    # Voeg data toe
    if isinstance(data, pd.DataFrame):
        if symbol is None:
            symbol = "UNKNOWN"
            logger.log_info(
                "Geen symbool gespecificeerd voor DataFrame", level="WARNING"
            )
        backtester.add_data(data, symbol)
    else:
        for sym, df in data.items():
            backtester.add_data(df, sym)

    # Voer backtest uit
    result = backtester.run(strategy_class, strategy_params)

    # Genereer plot indien gewenst
    if plot and result.get("success", False):
        backtester.plot(plot_filename)

    return result
