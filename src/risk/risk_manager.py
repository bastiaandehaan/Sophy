# sophy/core/risk_manager.py
from datetime import date, datetime
from typing import Dict, Optional, Tuple


class RiskManager:
    """
    Risicomanagement met FTMO compliance checks.

    Verantwoordelijk voor het bewaken van risicoparameters zoals dagelijkse verlieslimiet,
    maximale drawdown, en positiegrootte berekeningen volgens risicoregels.
    """

    def __init__(self, config: Dict, logger):
        """Initialiseer met configuratieparameters"""
        self.config = config
        self.logger = logger
        self.risk_config = config.get('risk', {})

        # Extraheer risicoparameters
        self.max_risk_per_trade = self.risk_config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.risk_config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.risk_config.get('max_total_drawdown', 0.10)
        self.leverage = self.risk_config.get('leverage', 30)

        # Initialiseer tracking variabelen
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.risk_config.get('account_balance', 100000)

    def check_ftmo_limits(self, account_info: Dict) -> Tuple[bool, Optional[str]]:
        """
        Controleer of huidige accountstatus voldoet aan FTMO-limieten

        Parameters:
        -----------
        account_info : Dict
            Dictionary met huidige accountinformatie

        Returns:
        --------
        Tuple van (stop_trading, reason)
        - stop_trading: True als trading gestopt moet worden
        - reason: Beschrijving waarom trading moet stoppen, of None
        """
        # Implementatie overnemen van je huidige risk_manager.py
        # ...