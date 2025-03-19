# src/analysis/strategy_adapter.py
from typing import Dict, Any, Optional

import backtrader as bt


class SophyStrategyAdapter(bt.Strategy):
    """
    Adapter om Sophy strategieën te gebruiken in Backtrader.
    """

    params = (
        ("sophy_strategy", None),  # Sophy strategie instance
        ("risk_per_trade", 0.01),  # Risico per trade
        ("debug", False),  # Debug modus toegevoegd
    )

    def __init__(self):
        """Initialize de strategie adapter."""
        self.sophy_strategy = self.params.sophy_strategy
        self.debug = self.params.debug  # Debug parameter nu ondersteund

        if self.sophy_strategy is None:
            raise ValueError("Je moet een Sophy strategie meegeven")

        # Hernoem positions naar tracked_positions om conflict te vermijden
        self.tracked_positions = {}  # Gewijzigd van self.positions
        self.orders = {}

        # Log debug informatie indien geactiveerd
        if self.debug:
            self.log(
                f"SophyStrategyAdapter geïnitialiseerd met strategie: {self.sophy_strategy.get_name()}")

    def log(self, message):
        """Logging hulpfunctie voor debug modus."""
        if self.debug:
            dt = self.datas[0].datetime.datetime(0)
            print(f"[{dt.isoformat()}] {message}")

    def next(self):
        """Deze methode wordt aangeroepen voor elke bar in de data."""
        # Controleer of er nog orders open staan
        if self.orders:
            return

        # Converteer data naar Sophy formaat
        data = self._convert_data()

        # Bereken indicatoren via Sophy strategie
        indicators = self.sophy_strategy.calculate_indicators(data)

        # Verkrijg signaal
        symbol = self.datas[0]._name
        current_position = self._get_current_position(symbol)

        # Aanpassing: gebruik process_symbol in plaats van generate_signal indien beschikbaar
        if hasattr(self.sophy_strategy, 'process_symbol'):
            signal_result = self.sophy_strategy.process_symbol(symbol)
            action = signal_result.get("signal", "NONE")  # Gebruik NONE als fallback
        else:
            signal_result = self.sophy_strategy.generate_signal(
                symbol, data, indicators, current_position
            )
            action = signal_result.get("action", "NONE")  # Gebruik NONE als fallback

        if self.debug:
            self.log(f"Signaal voor {symbol}: {action}")

        # Verwerk signaal
        self._process_signal(signal_result, symbol)

    def _convert_data(self):
        """Converteer Backtrader data naar Sophy formaat."""
        # Verbeterde implementatie voor dataconversie
        df = {}

        # Basisvelden toevoegen
        for field in ['open', 'high', 'low', 'close', 'volume']:
            if hasattr(self.datas[0], field):
                df[field] = getattr(self.datas[0], field)

        # Voeg datum toe indien beschikbaar
        if hasattr(self.datas[0], 'datetime'):
            df['date'] = self.datas[0].datetime

        return df

    def _get_current_position(self, symbol: str) -> Optional[str]:
        """Verkrijg de huidige positie voor een symbool."""
        # Aangepast om tracked_positions te gebruiken
        if symbol in self.tracked_positions:
            return self.tracked_positions[symbol]

        if self.position.size > 0:
            return "BUY"
        elif self.position.size < 0:
            return "SELL"

        return None

    def _process_signal(self, signal: Dict[str, Any], symbol: str) -> None:
        """
        Verwerk een signaal van de strategie.

        Args:
            signal: Signaal dictionary met action, params, etc.
            symbol: Symbool waarop het signaal betrekking heeft
        """
        # Ondersteuning voor beide signaalformaten (signal/action)
        action = signal.get("signal", signal.get("action", "NONE"))

        if action == "BUY" and self.position.size <= 0:
            # Sluit eventuele short positie
            if self.position.size < 0:
                self.close()

            # Bepaal positiegrootte
            price = self.datas[0].close[0]
            size = self._calculate_position_size(signal, price)

            if self.debug:
                self.log(f"BUY signaal: {symbol}, prijs={price}, size={size}")

            # Plaats order en update tracked_positions
            self.orders[symbol] = self.buy(size=size)
            self.tracked_positions[symbol] = "BUY"  # Aangepast

        elif action == "SELL" and self.position.size >= 0:
            # Sluit eventuele long positie
            if self.position.size > 0:
                self.close()

            # Bepaal positiegrootte
            price = self.datas[0].close[0]
            size = self._calculate_position_size(signal, price)

            if self.debug:
                self.log(f"SELL signaal: {symbol}, prijs={price}, size={size}")

            # Plaats order en update tracked_positions
            self.orders[symbol] = self.sell(size=size)
            self.tracked_positions[symbol] = "SELL"  # Aangepast

        elif action in ["CLOSE", "CLOSE_BUY", "CLOSE_SELL"]:
            # Sluit positie
            if self.position.size != 0:
                if self.debug:
                    self.log(f"CLOSE signaal: {symbol}")
                self.close()
                # Verwijder uit tracked_positions indien aanwezig
                if symbol in self.tracked_positions:
                    del self.tracked_positions[symbol]  # Aangepast

    def _calculate_position_size(self, signal: Dict[str, Any], price: float) -> float:
        """
        Bereken positiegrootte op basis van risicoparameters.

        Args:
            signal: Signaal dictionary
            price: Huidige prijs

        Returns:
            Positiegrootte
        """
        # Gebruik stop-loss indien aanwezig - zoek in meta of direct
        meta = signal.get("meta", {})
        stop_loss = meta.get("stop_loss") if isinstance(meta, dict) else signal.get(
            "stop_loss")

        if stop_loss:
            # Bereken risico per trade
            account_value = self.broker.getvalue()
            risk_amount = account_value * self.params.risk_per_trade

            # Bereken positiegrootte op basis van stop-loss afstand
            risk_per_unit = abs(price - stop_loss)
            if risk_per_unit > 0:
                size = risk_amount / risk_per_unit
            else:
                size = 1.0  # Default als stop-loss te dicht bij prijs ligt
        else:
            # Default sizing als geen stop-loss is opgegeven
            account_value = self.broker.getvalue()
            size = (account_value * self.params.risk_per_trade) / price

        return size

    def notify_order(self, order):
        """Verwerk order notificaties."""
        if order.status in [order.Submitted, order.Accepted]:
            return

        for symbol, ord in list(self.orders.items()):
            if ord is order:
                del self.orders[symbol]
                break

        if order.status in [order.Completed]:
            if self.debug:
                side = "BUY" if order.isbuy() else "SELL"
                self.log(f"Order uitgevoerd: {side} @ {order.executed.price}")

            if order.isbuy():
                pass  # Order is voltooid
            elif order.issell():
                pass  # Order is voltooid
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            if self.debug:
                self.log(f"Order niet uitgevoerd: {order.Status[order.status]}")
