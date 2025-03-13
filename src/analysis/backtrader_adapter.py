# src/analysis/backtrader_adapter.py
from typing import Dict, Any, Optional, List

import backtrader as bt
import pandas as pd


class SophyStrategyAdapter(bt.Strategy):
    """
    Adapter to use Sophy strategies with the Backtrader backtesting framework.

    This class acts as a bridge between Sophy's strategy implementation and
    Backtrader's framework, allowing Sophy strategies to be backtested using
    Backtrader's powerful features.
    """

    params = (
        ("sophy_strategy", None),  # Sophy Strategy instance
        ("config", {}),  # Configuration dictionary
        ("risk_per_trade", 0.01),  # Risk per trade (1%)
        ("debug", False),  # Debug mode
    )

    def __init__(self):
        # Initialize Backtrader components
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sellprice = None
        self.sellcomm = None

        # Configure the Sophy strategy if provided
        self.strategy = self.params.sophy_strategy
        if self.strategy is None:
            raise ValueError("A Sophy strategy instance must be provided")

        # Set up track record
        self.trades = []
        self.drawdowns = []
        self.peak_equity = self.broker.getvalue()

        # Track positions for strategy
        self.positions = {}

        # Create indicator storage
        self.indicators = {}

        # Debug logging
        self.debug(f"SophyStrategyAdapter initialized with {self.strategy.get_name()}")

    def debug(self, msg: str) -> None:
        """Log debug messages if debug mode is enabled"""
        if self.params.debug:
            print(f"[DEBUG] {msg}")

    def notify_order(self, order: bt.Order) -> None:
        """
        Process order notifications from Backtrader

        Args:
            order: Backtrader order object
        """
        if order.status in [order.Submitted, order.Accepted]:
            # Order has been submitted/accepted - nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.debug(
                    f"BUY EXECUTED, Price: {order.executed.price}, "
                    f"Cost: {order.executed.value}, Comm: {order.executed.comm}"
                )

                # Update position tracking
                self._update_position(
                    symbol=self.datas[0]._name,
                    order_type="BUY",
                    price=order.executed.price,
                    volume=order.executed.size,
                    order_id=str(order.ref),
                    timestamp=bt.num2date(self.datas[0].datetime[0]),
                )

            elif order.issell():
                self.sellprice = order.executed.price
                self.sellcomm = order.executed.comm
                self.debug(
                    f"SELL EXECUTED, Price: {order.executed.price}, "
                    f"Cost: {order.executed.value}, Comm: {order.executed.comm}"
                )

                # Update position tracking
                self._update_position(
                    symbol=self.datas[0]._name,
                    order_type="SELL",
                    price=order.executed.price,
                    volume=order.executed.size,
                    order_id=str(order.ref),
                    timestamp=bt.num2date(self.datas[0].datetime[0]),
                )

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.debug(f"Order Canceled/Margin/Rejected: {order.status}")

        self.order = None

    def notify_trade(self, trade: bt.Trade) -> None:
        """
        Process trade notifications from Backtrader

        Args:
            trade: Backtrader trade object
        """
        if not trade.isclosed:
            return

        # Record closed trade
        trade_record = {
            "entry_date": bt.num2date(trade.dtopen),
            "exit_date": bt.num2date(trade.dtclose),
            "entry_price": trade.price,
            "exit_price": trade.pnlcomm / trade.size + trade.price,
            "size": trade.size,
            "pnl": trade.pnlcomm,
            "pnl_pct": trade.pnlcomm / self.broker.getvalue() * 100,
        }

        self.trades.append(trade_record)
        self.debug(
            f"OPERATION PROFIT, GROSS: {trade.pnl:.2f}, NET: {trade.pnlcomm:.2f}"
        )

    def next(self):
        """Main method called for each bar/candle"""
        # Skip if an order is pending
        if self.order:
            return

        # Convert Backtrader data to Sophy format
        data = self._convert_data()

        # Calculate indicators via Sophy strategy
        indicators = self.strategy.calculate_indicators(data)

        # Store indicators for reference
        self.indicators = indicators

        # Generate signals
        signal_result = self.strategy._generate_signal(
            self.datas[0]._name, data, indicators, self._get_current_position()
        )

        # Process the signal
        self._process_signal(signal_result)

        # Track drawdown
        current_value = self.broker.getvalue()
        self.peak_equity = max(self.peak_equity, current_value)
        drawdown_pct = (self.peak_equity - current_value) / self.peak_equity * 100

        if drawdown_pct > 0:
            self.drawdowns.append(
                {
                    "date": bt.num2date(self.datas[0].datetime[0]),
                    "value": current_value,
                    "peak": self.peak_equity,
                    "drawdown_pct": drawdown_pct,
                }
            )

    def _convert_data(self) -> pd.DataFrame:
        """
        Convert Backtrader data feeds to pandas DataFrame for Sophy strategy

        Returns:
            DataFrame with OHLCV data
        """
        # Get data store array
        size = len(self.datas[0])

        # Create Series for OHLCV
        date_series = [
            bt.num2date(self.datas[0].datetime.array[i]) for i in range(size)
        ]
        open_series = [self.datas[0].open.array[i] for i in range(size)]
        high_series = [self.datas[0].high.array[i] for i in range(size)]
        low_series = [self.datas[0].low.array[i] for i in range(size)]
        close_series = [self.datas[0].close.array[i] for i in range(size)]
        volume_series = [self.datas[0].volume.array[i] for i in range(size)]

        # Create DataFrame
        df = pd.DataFrame(
            {
                "open": open_series,
                "high": high_series,
                "low": low_series,
                "close": close_series,
                "volume": volume_series,
            },
            index=date_series,
        )

        return df

    def _get_current_position(self) -> Optional[str]:
        """
        Get the current position direction

        Returns:
            Current position direction ("BUY", "SELL", or None)
        """
        symbol = self.datas[0]._name

        if symbol in self.positions:
            return self.positions[symbol]["direction"]

        return None

    def _process_signal(self, signal_result: Dict[str, Any]) -> None:
        """
        Process a signal from the Sophy strategy

        Args:
            signal_result: Signal result from Sophy strategy
        """
        signal = signal_result.get("signal", "NONE")
        meta = signal_result.get("meta", {})

        if signal == "BUY":
            # Calculate position size based on risk per trade
            entry_price = meta.get("entry_price", self.dataclose[0])
            stop_loss = meta.get("stop_loss")
            account_value = self.broker.getvalue()
            risk_amount = account_value * self.params.risk_per_trade

            if stop_loss:
                risk_pips = abs(entry_price - stop_loss)
                position_size = risk_amount / risk_pips if risk_pips > 0 else 1.0
            else:
                position_size = risk_amount / (entry_price * 0.01)  # Default 1% risk

            # Limit position size
            position_size = min(position_size, account_value / entry_price * 0.95)
            position_size = max(position_size, 0.01)

            # Place the buy order
            self.order = self.buy(size=position_size)
            self.debug(f"BUY ORDER SENT: {position_size} @ {self.dataclose[0]}")

        elif signal == "SELL":
            # Calculate position size based on risk per trade
            entry_price = meta.get("entry_price", self.dataclose[0])
            stop_loss = meta.get("stop_loss")
            account_value = self.broker.getvalue()
            risk_amount = account_value * self.params.risk_per_trade

            if stop_loss:
                risk_pips = abs(entry_price - stop_loss)
                position_size = risk_amount / risk_pips if risk_pips > 0 else 1.0
            else:
                position_size = risk_amount / (entry_price * 0.01)  # Default 1% risk

            # Limit position size
            position_size = min(position_size, account_value / entry_price * 0.95)
            position_size = max(position_size, 0.01)

            # Place the sell order
            self.order = self.sell(size=position_size)
            self.debug(f"SELL ORDER SENT: {position_size} @ {self.dataclose[0]}")

        elif signal == "CLOSE_BUY" and self.position.size > 0:
            # Close buy position
            self.order = self.close()
            self.debug(f"CLOSE BUY ORDER SENT @ {self.dataclose[0]}")

        elif signal == "CLOSE_SELL" and self.position.size < 0:
            # Close sell position
            self.order = self.close()
            self.debug(f"CLOSE SELL ORDER SENT @ {self.dataclose[0]}")

    def _update_position(
        self,
        symbol: str,
        order_type: str,
        price: float,
        volume: float,
        order_id: str,
        timestamp: Any,
    ) -> None:
        """
        Update position tracking

        Args:
            symbol: Trading symbol
            order_type: Type of order (BUY, SELL, etc.)
            price: Execution price
            volume: Trading volume
            order_id: Unique order ID
            timestamp: Execution timestamp
        """
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if order_type in ["BUY", "SELL"]:
            direction = order_type

            # Register new position
            self.positions[symbol] = {
                "direction": direction,
                "entry_price": price,
                "volume": volume,
                "order_id": order_id,
                "entry_time": timestamp_str,
            }

            # Notify strategy of order fill
            self.strategy.on_order_filled(
                symbol, order_type, price, volume, order_id, timestamp_str
            )

        elif order_type in ["CLOSE", "CLOSE_BUY", "CLOSE_SELL"]:
            # Determine direction
            if order_type == "CLOSE":
                if symbol in self.positions:
                    order_type = f"CLOSE_{self.positions[symbol]['direction']}"
                else:
                    return

            # Notify strategy of closed position
            self.strategy.on_order_filled(
                symbol, order_type, price, volume, order_id, timestamp_str
            )

            # Remove position from tracking
            if symbol in self.positions:
                del self.positions[symbol]


class BacktraderAdapter:
    """
    Main adapter class for using Sophy strategies with Backtrader.

    This class provides a convenient way to backtest Sophy strategies using
    the Backtrader framework.
    """

    def __init__(self, config: Dict[str, Any], logger) -> None:
        """
        Initialize the Backtrader adapter.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.cerebro = bt.Cerebro()

        # Default settings
        self.cerebro.broker.set_cash(config.get("initial_balance", 100000))
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
        # Convert timeframe string to Backtrader timeframe
        bt_timeframe = self._get_backtrader_timeframe(timeframe)

        # Create a Backtrader data feed from the DataFrame
        if data.index.dtype.kind == "M":  # If the index is datetime
            bt_data = bt.feeds.PandasData(
                dataname=data,
                name=symbol,
                timeframe=bt_timeframe,
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
                    timeframe=bt_timeframe,
                    datetime="date",
                    open="open",
                    high="high",
                    low="low",
                    close="close",
                    volume="volume",
                    openinterest=-1,
                )
            else:
                self.logger.error(
                    f"Cannot add data for {symbol}: no datetime index or 'date' column"
                )
                return

        # Add the data feed to Cerebro
        self.cerebro.adddata(bt_data)
        self.data_feeds[symbol] = bt_data

        self.logger.info(f"Added data for {symbol} with {len(data)} bars")

    def run_backtest(self, sophy_strategy, **kwargs) -> Dict[str, Any]:
        """
        Run a backtest with a Sophy strategy.

        Args:
            sophy_strategy: A Sophy strategy instance
            **kwargs: Additional parameters for the strategy

        Returns:
            Dictionary with backtest results
        """
        # Add the strategy adapter with the Sophy strategy
        self.cerebro.addstrategy(
            SophyStrategyAdapter,
            sophy_strategy=sophy_strategy,
            config=self.config,
            **kwargs,
        )

        self.logger.info(f"Starting backtest with {sophy_strategy.get_name()}")

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
            "detailed_trades": strategy.trades,
            "detailed_drawdowns": strategy.drawdowns,
            "raw_results": results,
        }

        # Check FTMO compliance
        ftmo_compliance = self._check_ftmo_compliance(
            backtest_results, strategy.drawdowns
        )
        backtest_results["ftmo_compliance"] = ftmo_compliance

        self.logger.info(
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
            plt = self.cerebro.plot(
                style="candle", barup="green", bardown="red", volume=False, grid=True
            )

            if filename:
                plt[0][0].savefig(filename, dpi=300)
                self.logger.info(f"Plot saved to {filename}")

        except Exception as e:
            self.logger.error(f"Error plotting results: {e}")

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

        timeframe_compression = {
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

        if timeframe in timeframe_map:
            self.cerebro.broker.set_coc(True)  # Use cheat-on-close for intraday
            return (timeframe_map[timeframe], timeframe_compression[timeframe])
        else:
            return bt.TimeFrame.Days  # Default to Daily

    def _check_ftmo_compliance(
        self, results: Dict[str, Any], drawdowns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check if backtest results comply with FTMO rules.

        Args:
            results: Backtest results dictionary
            drawdowns: List of drawdown events

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
        max_drawdown = results["max_drawdown"] / 100 if "max_drawdown" in results else 0
        total_trades = results["total_trades"]

        # Check trading days
        unique_trading_days = len(
            set(trade["entry_date"].date() for trade in results["detailed_trades"])
        )

        # Check max daily loss
        daily_losses = {}
        for trade in results["detailed_trades"]:
            trade_date = trade["exit_date"].date()
            pnl_pct = trade["pnl_pct"] / 100

            if trade_date not in daily_losses:
                daily_losses[trade_date] = 0

            daily_losses[trade_date] += pnl_pct

        worst_daily_loss = min(daily_losses.values()) if daily_losses else 0
        daily_loss_violation = worst_daily_loss < -max_daily_loss

        # Check compliance
        profit_target_met = profit_percentage >= profit_target
        daily_loss_compliant = not daily_loss_violation
        total_loss_compliant = max_drawdown <= max_total_loss
        trading_days_compliant = unique_trading_days >= min_trading_days

        is_compliant = (
            profit_target_met
            and daily_loss_compliant
            and total_loss_compliant
            and trading_days_compliant
        )

        # Create reason list
        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Profit target not met: {profit_percentage * 100:.2f}% < {profit_target * 100}%"
            )
        if not daily_loss_compliant:
            reasons.append(
                f"Daily loss limit exceeded: {worst_daily_loss * 100:.2f}% < -{max_daily_loss * 100}%"
            )
        if not total_loss_compliant:
            reasons.append(
                f"Max drawdown exceeded: {max_drawdown * 100:.2f}% > {max_total_loss * 100}%"
            )
        if not trading_days_compliant:
            reasons.append(
                f"Insufficient trading days: {unique_trading_days} < {min_trading_days}"
            )

        return {
            "is_compliant": is_compliant,
            "profit_target_met": profit_target_met,
            "daily_loss_compliant": daily_loss_compliant,
            "total_loss_compliant": total_loss_compliant,
            "trading_days_compliant": trading_days_compliant,
            "profit_percentage": profit_percentage * 100,
            "max_drawdown": max_drawdown * 100,
            "worst_daily_loss": worst_daily_loss * 100,
            "unique_trading_days": unique_trading_days,
            "reason": reasons if not is_compliant else [],
        }
