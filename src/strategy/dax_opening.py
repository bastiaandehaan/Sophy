# src/strategy/dax_opening.py
import datetime
from typing import Dict, Any, List, Optional

import pandas as pd

from src.strategy.base_strategy import Strategy
from src.utils.indicators import calculate_atr


class DAXOpeningStrategy(Strategy):
    """
    Implementation of a DAX opening session breakout strategy.

    This strategy focuses on trading breakouts from the initial price range
    established during the first hour of the DAX trading session.

    Key components:
    1. Session opening detection (Frankfurt exchange opens at 8:00 AM CET)
    2. Initial price range formation (first 60 minutes)
    3. Breakout detection (price moves above/below the initial range)
    4. Stop loss and take profit based on ATR
    5. Trade filtering using market condition filters
    """

    def __init__(self, connector, risk_manager, logger, config: Dict = None):
        """
        Initialize the DAX Opening breakout strategy.

        Args:
            connector: MT5 connector instance
            risk_manager: Risk manager instance
            logger: Logger instance
            config: Configuration dictionary with strategy parameters
        """
        super().__init__(connector, risk_manager, logger, config)

        if config is None:
            config = {}

        self.name = "DAX Opening Strategy"

        # Get strategy configuration
        strategy_config = config.get("strategy", {})

        # Strategy-specific parameters
        self.session_start_hour = strategy_config.get(
            "session_start_hour", 8
        )  # Frankfurt open
        self.session_start_minute = strategy_config.get("session_start_minute", 0)
        self.breakout_period = strategy_config.get(
            "breakout_period", 60
        )  # Minutes for initial range
        self.stop_loss_multiplier = strategy_config.get("stop_loss_multiplier", 1.5)
        self.take_profit_multiplier = strategy_config.get("take_profit_multiplier", 2.0)
        self.use_filters = strategy_config.get("use_filters", True)

        # Position tracking
        self.positions = {}
        self.session_ranges = {}  # For storing today's session range

        self.logger.info(
            f"DAX Opening Strategy initialized: "
            f"session_start={self.session_start_hour}:{self.session_start_minute}, "
            f"breakout_period={self.breakout_period} min, "
            f"SL_mult={self.stop_loss_multiplier}, TP_mult={self.take_profit_multiplier}"
        )

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Process a symbol according to the DAX Opening strategy rules.

        This method retrieves historical data and generates trading signals.

        Args:
            symbol: The symbol to analyze

        Returns:
            Dict with trading signals and metadata
        """
        # Since this is specifically for DAX, check if symbol is DAX-related
        if not self._is_dax_symbol(symbol):
            return {"signal": "NONE", "meta": {"reason": "not_dax_symbol"}}

        # Get timeframe (M5 is typically used for intraday strategies)
        timeframe = self.config.get("timeframe", "M5")

        # Calculate how many bars we need (at least 1 full trading day)
        bars_needed = max(
            288, self.breakout_period * 2
        )  # 288 = typical bars in trading day for M5

        # Get historical data
        data = self.connector.get_historical_data(
            symbol=symbol, timeframe=timeframe, bars_count=bars_needed
        )

        if data is None or len(data) < bars_needed:
            self.logger.warning(f"Insufficient data for {symbol} to generate signals")
            return {"signal": "NONE", "meta": {"reason": "insufficient_data"}}

        # Current time check - only execute during market hours
        current_time = datetime.datetime.now().time()
        in_trading_hours = self._is_in_trading_hours(current_time)

        if not in_trading_hours:
            return {"signal": "NONE", "meta": {"reason": "outside_trading_hours"}}

        # Calculate indicators and detect session range
        indicators = self.calculate_indicators(data)

        # Get current position
        current_position = self.get_position(symbol)
        position_direction = (
            current_position.get("direction", None) if current_position else None
        )

        # Generate signal based on indicators and current position
        return self._generate_signal(symbol, data, indicators, position_direction)

    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate technical indicators for the DAX Opening strategy.

        Args:
            data: DataFrame with OHLC data

        Returns:
            Dictionary with calculated indicators
        """
        # Ensure data is sorted by date (ascending)
        data = data.sort_index()

        # Get current time
        current_time = datetime.datetime.now()
        current_date = current_time.date()

        # Calculate session open time for today
        session_open_time = datetime.datetime.combine(
            current_date,
            datetime.time(
                hour=self.session_start_hour, minute=self.session_start_minute
            ),
        )

        # Calculate session range close time
        range_close_time = session_open_time + datetime.timedelta(
            minutes=self.breakout_period
        )

        # Filter data for today's session and initial range
        today_data = data[data.index.date == current_date]
        initial_range = today_data[
            (today_data.index >= session_open_time)
            & (today_data.index <= range_close_time)
        ]

        # If we have enough data in the initial range, calculate high and low
        has_session_range = False
        session_high = 0.0
        session_low = 0.0

        if not initial_range.empty and len(initial_range) > 0:
            session_high = initial_range["high"].max()
            session_low = initial_range["low"].min()
            has_session_range = True

            # Store session range for this symbol
            self.session_ranges[data.index[-1].date()] = {
                "high": session_high,
                "low": session_low,
                "midpoint": (session_high + session_low) / 2,
            }

        # Calculate ATR for stop loss and take profit
        data["atr"] = calculate_atr(data, period=14)
        current_atr = data["atr"].iloc[-1]

        # Prepare market condition filters if enabled
        if self.use_filters:
            # Simple trend filter using moving averages
            data["ma_fast"] = data["close"].rolling(window=20).mean()
            data["ma_slow"] = data["close"].rolling(window=50).mean()

            trend_up = data["ma_fast"].iloc[-1] > data["ma_slow"].iloc[-1]
            trend_down = data["ma_fast"].iloc[-1] < data["ma_slow"].iloc[-1]
        else:
            trend_up = True
            trend_down = True

        return {
            "data": data,
            "current_price": data["close"].iloc[-1],
            "has_session_range": has_session_range,
            "session_high": session_high,
            "session_low": session_low,
            "current_atr": current_atr,
            "trend_up": trend_up,
            "trend_down": trend_down,
            "session_open_time": session_open_time,
            "range_close_time": range_close_time,
            "current_time": current_time,
        }

    def _generate_signal(
        self,
        symbol: str,
        data: pd.DataFrame,
        indicators: Dict[str, Any],
        current_direction: Optional[str],
    ) -> Dict[str, Any]:
        """
        Generate a trading signal based on calculated indicators.

        Args:
            symbol: Trading symbol
            data: DataFrame with OHLC data
            indicators: Dictionary with calculated indicators
            current_direction: Current position direction (BUY/SELL/None)

        Returns:
            Dictionary with trading signal and metadata
        """
        # Default to no signal
        signal = "NONE"
        meta = {
            "current_atr": indicators["current_atr"],
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "risk_pips": None,
            "reason": None,
        }

        # Check if we have a valid session range
        if not indicators["has_session_range"]:
            meta["reason"] = "no_session_range"
            return {"signal": signal, "meta": meta}

        current_price = indicators["current_price"]
        session_high = indicators["session_high"]
        session_low = indicators["session_low"]
        current_atr = indicators["current_atr"]
        current_time = indicators["current_time"]

        # Only generate entry signals after the range formation period
        if current_time <= indicators["range_close_time"]:
            meta["reason"] = "within_range_formation"
            return {"signal": signal, "meta": meta}

        # Entry logic - only if we don't have a position
        if not current_direction:
            # Breakout above session high
            if current_price > session_high and indicators["trend_up"]:
                signal = "BUY"
                entry_price = session_high
                stop_loss = entry_price - (self.stop_loss_multiplier * current_atr)
                take_profit = entry_price + (self.take_profit_multiplier * current_atr)

                meta["entry_price"] = entry_price
                meta["stop_loss"] = stop_loss
                meta["take_profit"] = take_profit
                meta["risk_pips"] = self.stop_loss_multiplier * current_atr
                meta["reason"] = "long_breakout"

            # Breakout below session low
            elif current_price < session_low and indicators["trend_down"]:
                signal = "SELL"
                entry_price = session_low
                stop_loss = entry_price + (self.stop_loss_multiplier * current_atr)
                take_profit = entry_price - (self.take_profit_multiplier * current_atr)

                meta["entry_price"] = entry_price
                meta["stop_loss"] = stop_loss
                meta["take_profit"] = take_profit
                meta["risk_pips"] = self.stop_loss_multiplier * current_atr
                meta["reason"] = "short_breakout"

        # Exit logic - for existing positions
        else:
            if current_direction == "BUY":
                # Exit long if price hits take profit or falls below midpoint
                if current_price <= (session_high + session_low) / 2:
                    signal = "CLOSE_BUY"
                    meta["reason"] = "midpoint_exit"

            elif current_direction == "SELL":
                # Exit short if price hits take profit or rises above midpoint
                if current_price >= (session_high + session_low) / 2:
                    signal = "CLOSE_SELL"
                    meta["reason"] = "midpoint_exit"

        return {"signal": signal, "meta": meta}

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get the current position for a symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Dictionary with position details or None if no position
        """
        # Check in local position tracking
        if symbol in self.positions:
            return self.positions[symbol]

        # Otherwise check with connector (if available)
        if self.connector:
            position = self.connector.get_position(symbol)
            if position:
                # Store position in local tracking
                self.positions[symbol] = position
                return position

        return None

    def get_open_positions(self) -> Dict[str, List]:
        """
        Get all open positions.

        Returns:
            Dictionary with open positions by symbol
        """
        # Get positions via connector
        if self.connector:
            positions = self.connector.get_open_positions()

            # Update local tracking
            for symbol, position in positions.items():
                self.positions[symbol] = position

            return positions

        # If no connector, use local tracking
        return self.positions

    def on_order_filled(
        self,
        symbol: str,
        order_type: str,
        price: float,
        volume: float,
        order_id: str,
        timestamp: str,
    ) -> None:
        """
        Process a filled order and update position tracking.

        Args:
            symbol: Trading symbol
            order_type: Type of order (BUY, SELL, etc.)
            price: Execution price
            volume: Trading volume
            order_id: Unique order ID
            timestamp: Execution timestamp
        """
        if order_type in ["BUY", "SELL"]:
            direction = order_type

            # Register new position
            self.positions[symbol] = {
                "direction": direction,
                "entry_price": price,
                "volume": volume,
                "order_id": order_id,
                "entry_time": timestamp,
            }

            self.logger.info(
                f"New {direction} position in {symbol}: "
                f"price={price}, volume={volume}"
            )

        elif order_type in ["CLOSE_BUY", "CLOSE_SELL"]:
            # Remove position from tracking after closing
            if symbol in self.positions:
                entry_price = self.positions[symbol]["entry_price"]
                direction = self.positions[symbol]["direction"]
                profit_loss = 0

                if direction == "BUY":
                    profit_loss = price - entry_price
                elif direction == "SELL":
                    profit_loss = entry_price - price

                self.logger.info(
                    f"Position closed in {symbol}: entry={entry_price}, "
                    f"exit={price}, P/L={profit_loss}"
                )

                # Remove position from tracking
                del self.positions[symbol]

    def _is_dax_symbol(self, symbol: str) -> bool:
        """
        Check if a symbol is DAX-related.

        Args:
            symbol: Trading symbol

        Returns:
            True if symbol is DAX-related, False otherwise
        """
        dax_symbols = ["DAX", "GER30", "DE30", "DEU40", "GDAXI"]
        return any(dax in symbol.upper() for dax in dax_symbols)

    def _is_in_trading_hours(self, current_time: datetime.time) -> bool:
        """
        Check if current time is within DAX trading hours.

        Args:
            current_time: Current time

        Returns:
            True if within trading hours, False otherwise
        """
        # DAX trading hours: 09:00 - 17:30 CET
        trading_start = datetime.time(hour=9, minute=0)
        trading_end = datetime.time(hour=17, minute=30)

        return trading_start <= current_time <= trading_end
