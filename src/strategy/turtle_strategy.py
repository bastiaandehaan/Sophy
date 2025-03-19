# src/strategy/turtle_strategy.py
from typing import Dict, List, Optional, Any

import pandas as pd

from src.strategy.base_strategy import Strategy
from src.utils.indicators import calculate_atr


class TurtleStrategy(Strategy):
    """
    Implementatie van de klassieke Turtle Trading strategie als onderdeel van het Sophy framework.

    De strategie gebruikt breakouts van donchian channels voor entry en exits,
    gecombineerd met ATR voor positiegrootte en risicobeheer.
    """

    def __init__(self, connector, risk_manager, logger, config: Dict = None):
        """
        Initialiseer de Turtle Trading strategie.

        Args:
            connector: MT5 connector instantie
            risk_manager: Risk manager instantie
            logger: Logger instantie voor het loggen van strategie acties
            config: Configuratie dictionary met strategie parameters
        """
        super().__init__(connector, risk_manager, logger, config)

        if config is None:
            config = {}

        self.name = "Turtle Trading Strategy"

        # Haal strategie-specifieke configuratie op
        strategy_config = config.get("strategy", {})

        # Turtle specifieke parameters
        self.entry_period = strategy_config.get(
            "entry_period", 20
        )  # Klassieke waarde: 20-dagen breakout
        self.exit_period = strategy_config.get(
            "exit_period", 10
        )  # Klassieke waarde: 10-dagen breakout
        self.atr_period = strategy_config.get(
            "atr_period", 14
        )  # ATR berekening periode
        self.atr_multiplier = strategy_config.get(
            "atr_multiplier", 2.0
        )  # N-voud van ATR voor stops
        self.units = strategy_config.get(
            "units", 1
        )  # Aantal te nemen units (in originele strategie: 1 tot 4)
        self.use_filters = strategy_config.get(
            "use_filters", True
        )  # Gebruik trendfilters
        self.filter_period = strategy_config.get(
            "filter_period", 50
        )  # Periode voor trendfilter

        # Swing trading modus (optioneel, voor turtle_swing variant)
        self.swing_mode = strategy_config.get("swing_mode", False)

        # Voor het bijhouden van posities en staten
        self.positions = {}  # Bijhouden van open posities per symbool
        self.last_breakout_prices = {}  # Laatste breakout niveau per symbool

        self.logger.info(
            f"Turtle Strategy geïnitialiseerd: entry={self.entry_period}, "
            f"exit={self.exit_period}, ATR={self.atr_period}, "
            f"multiplier={self.atr_multiplier}, units={self.units}, "
            f"swing_mode={self.swing_mode}"
        )

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de Turtle Trading regels.

        Deze methode haalt historische data op en genereert handelssignalen.

        Args:
            symbol: Het te analyseren handelssymbool

        Returns:
            Dict met handelssignalen en metadata
        """
        # Timeframe bepalen (standaard D1 voor Turtle)
        timeframe = self.config.get("timeframe", "D1")

        # Bereken hoeveel bars we nodig hebben
        bars_needed = (
            max(
                self.entry_period, self.exit_period, self.atr_period, self.filter_period
            )
            + 50
        )

        # Haal historische data op via connector
        data = self.connector.get_historical_data(
            symbol=symbol, timeframe=timeframe, num_bars=bars_needed
        )

        if data is None or len(data) < bars_needed:
            self.logger.warning(
                f"Onvoldoende data voor {symbol} om signalen te genereren"
            )
            return {"signal": "GEEN", "meta": {"reason": "onvoldoende_data"}}

        # Bereken indicators en signalen
        indicators = self.calculate_indicators(data)

        # Bepaal huidige positie
        current_position = self.get_position(symbol)
        position_direction = (
            current_position.get("direction", None) if current_position else None
        )

        # Genereer signaal op basis van indicators en huidige positie
        return self._generate_signal(symbol, data, indicators, position_direction)

    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Bereken de technische indicatoren voor de Turtle Trading strategie.

        Args:
            data: DataFrame met OHLCV data

        Returns:
            Dictionary met berekende indicatoren
        """
        # Zorg dat data gesorteerd is op datum (oplopend)
        data = data.sort_index()

        # --- Bereken indicatoren ---
        # Entry channel (hoog van laatste N dagen)
        data["entry_high"] = data["high"].rolling(window=self.entry_period).max()
        data["entry_low"] = data["low"].rolling(window=self.entry_period).min()

        # Exit channel (hoog/laag van laatste N/2 dagen)
        data["exit_high"] = data["high"].rolling(window=self.exit_period).max()
        data["exit_low"] = data["low"].rolling(window=self.exit_period).min()

        # ATR berekenen
        data["atr"] = calculate_atr(data, period=self.atr_period)

        # Trendfilter (optioneel)
        if self.use_filters:
            data["ma"] = data["close"].rolling(window=self.filter_period).mean()
            trend_up = (
                data["close"].iloc[-1] > data["ma"].iloc[-1]
                if not data["ma"].isna().iloc[-1]
                else True
            )
            trend_down = (
                data["close"].iloc[-1] < data["ma"].iloc[-1]
                if not data["ma"].isna().iloc[-1]
                else True
            )
        else:
            trend_up = True
            trend_down = True

        # Veilige methode voor het ophalen van eerdere indicatorwaarden
        def safe_previous_value(series, default=None):
            """Haal veilig een eerdere waarde op, met fallback waarden."""
            non_na_values = series.dropna()
            if len(non_na_values) >= 2:
                return non_na_values.iloc[-2]
            elif len(non_na_values) == 1:
                return non_na_values.iloc[-1]  # Gebruik de enige beschikbare waarde
            else:
                # Als geen data beschikbaar, gebruik default of current price
                return default if default is not None else data["close"].iloc[-1]

        # Veilige current_price en ATR checks
        current_price = data["close"].iloc[-1]
        current_atr = data["atr"].iloc[-1] if not data["atr"].isna().iloc[-1] else 0.001

        # Return de berekende indicators met veilige waardes
        return {
            "data": data,
            "current_price": current_price,
            "previous_entry_high": safe_previous_value(data["entry_high"]),
            "previous_entry_low": safe_previous_value(data["entry_low"]),
            "previous_exit_high": safe_previous_value(data["exit_high"]),
            "previous_exit_low": safe_previous_value(data["exit_low"]),
            "current_atr": current_atr,
            "trend_up": trend_up,
            "trend_down": trend_down,
        }

    def _generate_signal(
        self,
        symbol: str,
        data: pd.DataFrame,
        indicators: Dict[str, Any],
        current_direction: Optional[str],
    ) -> Dict[str, Any]:
        """
        Genereer een handelssignaal op basis van de berekende indicators.

        Args:
            symbol: Handelssymbool
            data: DataFrame met OHLCV data
            indicators: Dictionary met berekende indicators
            current_direction: Huidige positierichting (BUY/SELL/None)

        Returns:
            Dictionary met handelssignaal en metadata
        """
        # Haal indicatorwaarden op
        current_price = indicators["current_price"]
        previous_entry_high = indicators["previous_entry_high"]
        previous_entry_low = indicators["previous_entry_low"]
        previous_exit_high = indicators["previous_exit_high"]
        previous_exit_low = indicators["previous_exit_low"]
        current_atr = indicators["current_atr"]
        trend_up = indicators["trend_up"]
        trend_down = indicators["trend_down"]

        # Standaard geen signaal
        signal = "GEEN"
        meta = {
            "atr": current_atr,
            "entry_price": None,
            "stop_loss": None,
            "risk_pips": None,
            "reason": None,
        }

        # Entry logica - als we geen positie hebben
        if not current_direction:
            # Long entry (breakout boven entry_high)
            if current_price > previous_entry_high and trend_up:
                signal = "BUY"
                entry_price = previous_entry_high
                stop_loss = entry_price - (self.atr_multiplier * current_atr)

                meta["entry_price"] = entry_price
                meta["stop_loss"] = stop_loss
                meta["risk_pips"] = self.atr_multiplier * current_atr
                meta["reason"] = "long_entry_breakout"

                # Update breakout prijs
                self.last_breakout_prices[symbol] = entry_price

            # Short entry (breakout onder entry_low)
            elif current_price < previous_entry_low and trend_down:
                signal = "SELL"
                entry_price = previous_entry_low
                stop_loss = entry_price + (self.atr_multiplier * current_atr)

                meta["entry_price"] = entry_price
                meta["stop_loss"] = stop_loss
                meta["risk_pips"] = self.atr_multiplier * current_atr
                meta["reason"] = "short_entry_breakout"

                # Update breakout prijs
                self.last_breakout_prices[symbol] = entry_price

        # Exit logica - voor bestaande posities
        else:
            if current_direction == "BUY":
                # Exit long positie als prijs onder exit_low daalt
                if current_price < previous_exit_low:
                    signal = "CLOSE_BUY"
                    meta["reason"] = "long_exit_breakout"

            elif current_direction == "SELL":
                # Exit short positie als prijs boven exit_high stijgt
                if current_price > previous_exit_high:
                    signal = "CLOSE_SELL"
                    meta["reason"] = "short_exit_breakout"

        # Aanpassingen voor swing modus (indien ingeschakeld)
        if self.swing_mode and signal in ["BUY", "SELL"]:
            # In swing modus nemen we minder risico met strakker stops
            meta["stop_loss"] = (
                meta["entry_price"] - (self.atr_multiplier * 0.75 * current_atr)
                if signal == "BUY"
                else meta["entry_price"] + (self.atr_multiplier * 0.75 * current_atr)
            )
            meta["risk_pips"] = self.atr_multiplier * 0.75 * current_atr
            meta["reason"] += "_swing"

        return {"signal": signal, "meta": meta}

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Haal de huidige positie op voor een symbool.

        Args:
            symbol: Handelssymbool

        Returns:
            Dictionary met positiegegevens of None als er geen positie is
        """
        # Controleer eerst in onze lokale positieadministratie
        if symbol in self.positions:
            return self.positions[symbol]

        # Anders vraag aan connector (indien beschikbaar)
        if self.connector:
            position = self.connector.get_position(symbol)
            if position:
                # Sla positie op in lokale administratie
                self.positions[symbol] = position
                return position

        return None

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op.

        Returns:
            Dictionary met open posities per symbool
        """
        # Haal posities op via connector
        if self.connector:
            positions = self.connector.get_open_positions()

            # Update onze lokale administratie
            for symbol, position in positions.items():
                self.positions[symbol] = position

            return positions

        # Als geen connector, gebruik lokale administratie
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
        Verwerk een gevulde order en update de positie administratie.

        Args:
            symbol: Handelssymbool
            order_type: Type order (BUY, SELL, etc.)
            price: Uitvoeringsprijs
            volume: Handelsvolume
            order_id: Unieke order ID
            timestamp: Tijdstip van uitvoering
        """
        if order_type in ["BUY", "SELL"]:
            direction = order_type

            # Nieuwe positie registreren
            self.positions[symbol] = {
                "direction": direction,
                "entry_price": price,
                "volume": volume,
                "order_id": order_id,
                "entry_time": timestamp,
            }

            self.logger.info(
                f"Nieuwe {direction} positie in {symbol}: prijs={price}, volume={volume}"
            )

        elif order_type in ["CLOSE_BUY", "CLOSE_SELL"]:
            # Positie verwijderen uit administratie na sluiting
            if symbol in self.positions:
                entry_price = self.positions[symbol]["entry_price"]
                direction = self.positions[symbol]["direction"]
                profit_loss = 0

                if direction == "BUY":
                    profit_loss = price - entry_price
                elif direction == "SELL":
                    profit_loss = entry_price - price

                self.logger.info(
                    f"Positie gesloten in {symbol}: entry={entry_price}, exit={price}, "
                    f"P/L={profit_loss}"
                )

                # Verwijder positie uit administratie
                del self.positions[symbol]

    def calculate_position_trailing_stop(
        self, symbol: str, current_price: float
    ) -> Optional[float]:
        """
        Bereken een trailing stop voor een bestaande positie volgens Turtle regels.

        Args:
            symbol: Handelssymbool
            current_price: Huidige marktprijs

        Returns:
            Nieuwe stop loss prijs of None als geen aanpassing nodig is
        """
        if symbol not in self.positions:
            return None

        position = self.positions[symbol]
        direction = position["direction"]
        entry_price = position["entry_price"]

        # Implementatie van 2-ATR breakeven stop na 1-ATR winst
        # (een vereenvoudigde versie van de Turtle regels)
        return None  # Uitbreidingsmogelijkheid voor verdere implementatie
