from datetime import datetime
from typing import Dict, List, Any

import MetaTrader5 as mt5
import pandas as pd

# Voorbeeld imports (pas aan naar je daadwerkelijke module-structuur)
from src.connector.mt5_connector import MT5Connector  # Placeholder
from src.risk.risk_manager import RiskManager  # Placeholder
from src.strategy.base_strategy import Strategy
from src.utils.logger import Logger  # Placeholder


class TurtleStrategy(Strategy):
    """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO met ondersteuning voor swing modus."""

    def __init__(
        self,
        connector: MT5Connector,
        risk_manager: RiskManager,
        logger: Logger,
        config: dict,
    ):
        """
        Initialiseer de Turtle strategie.

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5.
        risk_manager : RiskManager
            Risicobeheer component.
        logger : Logger
            Component voor logging.
        config : dict
            Configuratie voor de strategie, inclusief mt5- en strategy-secties.
        """
        super().__init__(connector, risk_manager, logger, config)
        self.name = "Turtle Trading Strategy"
        self.position_initial_volumes: Dict[int, float] = (
            {}
        )  # Ticket -> initiële volume
        self.strategy_config = config.get("strategy", {})
        self.swing_mode = self.strategy_config.get("swing_mode", False)

        # Stel parameters in gebaseerd op modus
        if self.swing_mode:
            self.entry_period = self.strategy_config.get("entry_period", 40)
            self.exit_period = self.strategy_config.get("exit_period", 20)
            self.atr_period = self.strategy_config.get("atr_period", 20)
            self.atr_multiplier = self.strategy_config.get("atr_multiplier", 2.5)
            self.logger.log_info(
                "Strategie geïnitialiseerd in Swing modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )
        else:
            self.entry_period = self.strategy_config.get("entry_period", 20)
            self.exit_period = self.strategy_config.get("exit_period", 10)
            self.atr_period = self.strategy_config.get("atr_period", 20)
            self.atr_multiplier = self.strategy_config.get("atr_multiplier", 2.0)
            self.logger.log_info(
                "Strategie geïnitialiseerd in standaard modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )

        self.use_trend_filter = self.strategy_config.get("use_trend_filter", True)

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Bereken technische indicatoren voor de Turtle strategie.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close, tick_volume).

        Returns:
        --------
        Dict[str, Any]
            Berekende indicatoren voor de laatste rij.
        """
        if (
            df.empty
            or "high" not in df.columns
            or "low" not in df.columns
            or "close" not in df.columns
        ):
            return {}

        # Bereken ATR
        df["atr"] = self.calculate_atr(df)

        # Bereken Donchian kanalen
        df["high_entry"] = df["high"].rolling(window=self.entry_period).max()
        df["low_entry"] = df["low"].rolling(window=self.entry_period).min()
        df["high_exit"] = df["high"].rolling(window=self.exit_period).max()
        df["low_exit"] = df["low"].rolling(window=self.exit_period).min()

        # Voeg volume-indicator toe
        df["vol_avg_50"] = df["tick_volume"].rolling(window=50).mean()
        df["vol_ratio"] = df["tick_volume"] / df["vol_avg_50"].replace(
            0, 1
        )  # Vermijd deling door 0

        # Trendfilters
        if len(df) >= 50:
            df["ema_50"] = df["close"].ewm(span=50, adjust=False).mean()
        if len(df) >= 200:
            df["ema_200"] = df["close"].ewm(span=200, adjust=False).mean()

        if "ema_50" in df.columns:
            df["trend_bullish"] = df["close"] > df["ema_50"]
        if "ema_50" in df.columns and "ema_200" in df.columns:
            df["strong_trend"] = df["ema_50"] > df["ema_200"]
        if "ema_50" in df.columns:
            df["trend_strength"] = self.calculate_trend_strength(df)
        if "atr" in df.columns:
            df["high_volatility"] = self.calculate_market_volatility(df)

        # Retourneer laatste waarden
        return {
            "atr": df["atr"].iloc[-1] if "atr" in df else None,
            "high_entry": df["high_entry"].iloc[-2] if "high_entry" in df else None,
            "low_entry": df["low_entry"].iloc[-2] if "low_entry" in df else None,
            "high_exit": df["high_exit"].iloc[-2] if "high_exit" in df else None,
            "low_exit": df["low_exit"].iloc[-2] if "low_exit" in df else None,
            "trend_bullish": (
                df["trend_bullish"].iloc[-1] if "trend_bullish" in df else None
            ),
            "strong_trend": (
                df["strong_trend"].iloc[-1] if "strong_trend" in df else None
            ),
            "trend_strength": (
                df["trend_strength"].iloc[-1] if "trend_strength" in df else None
            ),
            "high_volatility": (
                df["high_volatility"].iloc[-1] if "high_volatility" in df else None
            ),
            "vol_ratio": df["vol_ratio"].iloc[-1] if "vol_ratio" in df else None,
        }

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """
        Bereken de Average True Range (ATR).

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close).

        Returns:
        --------
        pd.Series
            ATR waarden.
        """
        if "close" not in df.columns or df["close"].isna().all():
            return pd.Series([0] * len(df), index=df.index)
        high = df["high"]
        low = df["low"]
        close = df["close"].shift(1).fillna(method="bfill")

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)
        tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return tr.rolling(window=self.atr_period, min_periods=1).mean()

    def calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Bereken trendsterkte gebaseerd op EMA-afstand en -hoek.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        float
            Trendsterkte (0-1).
        """
        if "ema_50" not in df.columns or len(df) < 10:
            return 0.0
        latest_close = df["close"].iloc[-1]
        latest_ema = df["ema_50"].iloc[-1]
        ema_slope = (
            (df["ema_50"].iloc[-1] - df["ema_50"].iloc[-10]) / df["ema_50"].iloc[-10]
            if df["ema_50"].iloc[-10] != 0
            else 0
        )
        latest_atr = (
            df["atr"].iloc[-1]
            if "atr" in df and not pd.isna(df["atr"].iloc[-1])
            else latest_close * 0.01
        )
        distance = (latest_close - latest_ema) / latest_atr
        distance_score = min(1.0, max(0.0, distance / 3))
        slope_score = min(1.0, max(0.0, ema_slope * 20))
        return min(1.0, max(0.0, (distance_score * 0.7) + (slope_score * 0.3)))

    def calculate_market_volatility(self, df: pd.DataFrame) -> bool:
        """
        Bepaal of de markt in een hoge volatiliteitsperiode zit.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        bool
            True als volatiliteit hoog is.
        """
        if "atr" not in df.columns or len(df) < 20:
            return False
        avg_atr = df["atr"].iloc[-20:].mean()
        if pd.isna(avg_atr) or avg_atr == 0:
            return False
        current_atr = df["atr"].iloc[-1]
        return current_atr > (avg_atr * 1.3) if not pd.isna(current_atr) else False

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de Turtle strategie.

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool.

        Returns:
        --------
        Dict[str, Any]
            Resultaten inclusief signaal en actie.
        """
        result = {"signal": None, "action": None}
        if not self.risk_manager.can_trade():
            self.logger.log_info(
                f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}"
            )
            return result

        timeframe_str = self.config.get("mt5", {}).get("timeframe", "H4")
        bars_needed = (
            240 if timeframe_str == "H1" else 150 if timeframe_str == "H4" else 200
        )
        df = self.connector.get_historical_data(symbol, timeframe_str, bars_needed)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return result

        indicators = self.calculate_indicators(df)
        if not indicators:
            self.logger.log_info(f"Kon indicatoren niet berekenen voor {symbol}")
            return result

        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return result

        current_price = tick.ask
        last_high_entry = indicators.get("high_entry")
        last_low_exit = indicators.get("low_exit")
        current_atr = indicators.get("atr")
        if None in (current_atr, last_high_entry, last_low_exit):
            self.logger.log_info(f"Ontbrekende indicator waarden voor {symbol}")
            return result

        trend_bullish = indicators.get("trend_bullish", True)
        strong_trend = indicators.get("strong_trend", True)
        trend_strength = indicators.get("trend_strength", 0.5)
        high_volatility = indicators.get("high_volatility", False)
        volume_ratio = indicators.get("vol_ratio", 1.0)

        price_breakout = current_price > last_high_entry * 1.001
        volume_filter = volume_ratio > 1.1 if not pd.isna(volume_ratio) else True
        entry_conditions = price_breakout and current_atr > 0 and volume_filter

        if self.use_trend_filter:
            entry_conditions = entry_conditions and trend_bullish
        if self.swing_mode:
            entry_conditions = entry_conditions and strong_trend and not high_volatility

        if entry_conditions:
            self.logger.log_info(
                f"Breakout gedetecteerd voor {symbol} op {current_price}"
            )
            result["signal"] = "ENTRY"
            result["action"] = "BUY"

            sl_multiplier = (
                self.atr_multiplier + 0.5 if high_volatility else self.atr_multiplier
            )
            stop_loss = current_price - (sl_multiplier * current_atr)

            account_info = self.connector.get_account_info()
            account_balance = account_info.get(
                "balance", self.config.get("mt5", {}).get("account_balance", 100000)
            )
            lot_size = self.risk_manager.calculate_position_size(
                symbol, current_price, stop_loss, account_balance, trend_strength
            )

            if not self.risk_manager.check_trade_risk(
                symbol, lot_size, current_price, stop_loss
            ):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return result

            try:
                ticket = self.connector.place_order(
                    "BUY",
                    symbol,
                    lot_size,
                    stop_loss,
                    0,
                    comment=f"FTMO {'Swing' if self.swing_mode else 'Turtle'}",
                )
                if ticket:
                    self.position_initial_volumes[ticket] = lot_size
                    self.logger.log_trade(
                        symbol,
                        "BUY",
                        current_price,
                        lot_size,
                        stop_loss,
                        0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Entry (TS:{trend_strength:.2f})",
                        self.risk_manager.leverage,
                    )
                    result["ticket"] = ticket
                    result["volume"] = lot_size
                    result["stop_loss"] = stop_loss
            except Exception as e:
                self.logger.log_error(f"Fout bij plaatsen order voor {symbol}: {e}")
                return result

        self._manage_positions(symbol, current_price, last_low_exit, current_atr)
        return result

    def _manage_positions(
        self,
        symbol: str,
        current_price: float,
        last_low_exit: float,
        current_atr: float,
    ) -> None:
        """
        Beheer bestaande posities voor een symbool.

        Parameters:
        -----------
        symbol : str
            Trading symbool.
        current_price : float
            Huidige marktprijs.
        last_low_exit : float
            Laatste Donchian kanaal low exit.
        current_atr : float
            Huidige ATR waarde.
        """
        open_positions = self.connector.get_open_positions(symbol)
        if not open_positions:
            return

        for position in open_positions:
            position_age_days = (datetime.now().timestamp() - position.time) / (
                60 * 60 * 24
            )
            if position.type != mt5.POSITION_TYPE_BUY:
                continue

            entry_price = position.price_open
            profit_atr = 1.5 if self.swing_mode else 1.0
            profit_target_1 = entry_price + (profit_atr * current_atr)
            profit_target_2 = entry_price + (profit_atr * 2 * current_atr)
            min_hold_time = 2 if self.swing_mode else 1
            time_condition_met = position_age_days >= min_hold_time

            if (
                time_condition_met
                and current_price > profit_target_1
                and position.ticket in self.position_initial_volumes
            ):
                initial_volume = self.position_initial_volumes[position.ticket]
                partial_volume = round(initial_volume * 0.4, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(
                        f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}"
                    )
                    try:
                        partial_result = self.connector.place_order(
                            "SELL",
                            symbol,
                            partial_volume,
                            0,
                            0,
                            f"Partial Profit 40% - ticket:{position.ticket}",
                        )
                        if partial_result:
                            self.logger.log_trade(
                                symbol,
                                "SELL",
                                current_price,
                                partial_volume,
                                0,
                                0,
                                "Partial Profit 40%",
                            )
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                self.connector.modify_position(
                                    position.ticket,
                                    stop_loss=entry_price,
                                    take_profit=0,
                                )
                                self.position_initial_volumes[position.ticket] = (
                                    remaining_volume
                                )
                    except Exception as e:
                        self.logger.log_error(
                            f"Fout bij gedeeltelijke winstneming voor {symbol}: {e}"
                        )

            elif (
                time_condition_met
                and current_price > profit_target_2
                and position.ticket in self.position_initial_volumes
            ):
                initial_volume = self.position_initial_volumes[position.ticket]
                remaining_pct = 0.6
                partial_volume = round(initial_volume * remaining_pct * 0.5, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(
                        f"Gedeeltelijke winstneming (30%) voor {symbol} op {current_price}"
                    )
                    try:
                        partial_result = self.connector.place_order(
                            "SELL",
                            symbol,
                            partial_volume,
                            0,
                            0,
                            f"Partial Profit 30% - ticket:{position.ticket}",
                        )
                        if partial_result:
                            self.logger.log_trade(
                                symbol,
                                "SELL",
                                current_price,
                                partial_volume,
                                0,
                                0,
                                "Partial Profit 30%",
                            )
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                new_sl = entry_price + (
                                    (current_price - entry_price) * 0.5
                                )
                                self.connector.modify_position(
                                    position.ticket, stop_loss=new_sl, take_profit=0
                                )
                                self.position_initial_volumes[position.ticket] = (
                                    remaining_volume
                                )
                    except Exception as e:
                        self.logger.log_error(
                            f"Fout bij tweede winstneming voor {symbol}: {e}"
                        )

            elif current_price < last_low_exit:
                self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")
                try:
                    close_result = self.connector.place_order(
                        "SELL",
                        symbol,
                        position.volume,
                        0,
                        0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Exit - ticket:{position.ticket}",
                    )
                    if close_result:
                        self.logger.log_trade(
                            symbol,
                            "SELL",
                            current_price,
                            position.volume,
                            0,
                            0,
                            f"{'Swing' if self.swing_mode else 'Turtle'} System Exit",
                        )
                        if position.ticket in self.position_initial_volumes:
                            del self.position_initial_volumes[position.ticket]
                except Exception as e:
                    self.logger.log_error(
                        f"Fout bij sluiten positie voor {symbol}: {e}"
                    )

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op per symbool.

        Returns:
        --------
        Dict[str, List]
            Dictionary met open posities per symbool.
        """
        result = {}
        symbols = self.config.get("mt5", {}).get("symbols", [])
        for symbol in symbols:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result
