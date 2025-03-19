# src/analysis/strategy_adapter.py
from typing import Dict, Any, Optional

import backtrader as bt


class SophyStrategyAdapter(bt.Strategy):
    """
    Adapter om Sophy strategieën te gebruiken in Backtrader.
    """

    params = (
        ('sophy_strategy', None),  # Sophy strategie instance
        ('risk_per_trade', 0.01),  # Risico per trade
    )

    def __init__(self):
        """Initialize de strategie adapter."""
        self.sophy_strategy = self.params.sophy_strategy
        if self.sophy_strategy is None:
            raise ValueError("Je moet een Sophy strategie meegeven")

        # Houdt referenties bij naar actieve posities
        self.positions = {}
        self.orders = {}

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
        signal = self.sophy_strategy.generate_signal(symbol, data, indicators,
                                                     current_position)

        # Verwerk signaal
        self._process_signal(signal, symbol)

    def _convert_data(self):
        """Converteer Backtrader data naar Sophy formaat."""
        # Implementeer conversie voor jouw specifieke data formaat
        # ...

        # Placeholder implementatie
        return {
            'open': self.datas[0].open,
            'high': self.datas[0].high,
            'low': self.datas[0].low,
            'close': self.datas[0].close,
            'volume': self.datas[0].volume
        }

    def _get_current_position(self, symbol: str) -> Optional[str]:
        """Verkrijg de huidige positie voor een symbool."""
        if symbol in self.positions:
            return self.positions[symbol]

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
        action = signal.get('action', 'NONE')

        if action == 'BUY' and self.position.size <= 0:
            # Sluit eventuele short positie
            if self.position.size < 0:
                self.close()

            # Bepaal positiegrootte
            price = self.datas[0].close[0]
            size = self._calculate_position_size(signal, price)

            # Plaats order
            self.orders[symbol] = self.buy(size=size)
            self.positions[symbol] = "BUY"

        elif action == 'SELL' and self.position.size >= 0:
            # Sluit eventuele long positie
            if self.position.size > 0:
                self.close()

            # Bepaal positiegrootte
            price = self.datas[0].close[0]
            size = self._calculate_position_size(signal, price)

            # Plaats order
            self.orders[symbol] = self.sell(size=size)
            self.positions[symbol] = "SELL"

        elif action == 'CLOSE':
            # Sluit positie
            if self.position.size != 0:
                self.close()
                if symbol in self.positions:
                    del self.positions[symbol]

    def _calculate_position_size(self, signal: Dict[str, Any], price: float) -> float:
        """
        Bereken positiegrootte op basis van risicoparameters.

        Args:
            signal: Signaal dictionary
            price: Huidige prijs

        Returns:
            Positiegrootte
        """
        # Gebruik stop-loss indien aanwezig
        stop_loss = signal.get('stop_loss')
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
            if order.isbuy():
                pass  # Order is voltooid
            elif order.issell():
                pass  # Order is voltooid
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass  # Order is geannuleerd of geweigerd
