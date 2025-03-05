# src/risk/risk_manager.py
from datetime import date
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

        # Extraheer risicoparameters
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.config.get('max_total_drawdown', 0.10)
        self.leverage = self.config.get('leverage', 30)

        # Initialiseer tracking variabelen
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.config.get('account_balance', 100000)
        self.daily_trades_count = 0
        self.max_daily_trades = self.config.get('max_daily_trades', 10)

        self.logger.log_info(f"RiskManager geïnitialiseerd met max risk per trade: {self.max_risk_per_trade * 100}%, "
                             f"max daily drawdown: {self.max_daily_drawdown * 100}%, "
                             f"max total drawdown: {self.max_total_drawdown * 100}%, "
                             f"leverage: {self.leverage}")

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
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today
            self.logger.log_info("Dagelijkse risico limieten gereset (nieuwe handelsdag)")

        # Haal account data op
        current_balance = account_info.get('balance', 0)
        current_equity = account_info.get('equity', 0)

        # Bereken winst/verlies percentages
        balance_change_pct = (current_balance - self.initial_balance) / self.initial_balance
        equity_change_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Controleer of winstdoel is bereikt (10%)
        if balance_change_pct >= 0.10:
            return True, f"Winstdoel bereikt: {balance_change_pct:.2%}"

        # Controleer dagelijkse verlieslimiet (5%)
        if equity_change_pct <= -self.max_daily_drawdown:
            return True, f"Dagelijkse verlieslimiet bereikt: {equity_change_pct:.2%}"

        # Controleer totale verlieslimiet (10%)
        if equity_change_pct <= -self.max_total_drawdown:
            return True, f"Maximale drawdown bereikt: {equity_change_pct:.2%}"

        # Alles is binnen limieten
        return False, None

    def calculate_position_size(self,
                                symbol: str,
                                entry_price: float,
                                stop_loss: float,
                                account_balance: float,
                                trend_strength: float = 0.5) -> float:
        """
        Bereken optimale positiegrootte gebaseerd op risicoparameters

        Parameters:
        -----------
        symbol : str
            Trading symbool
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs
        account_balance : float
            Huidige account balans
        trend_strength : float
            Sterkte van de trend (0-1), gebruikt voor positiegrootte aanpassing

        Returns:
        --------
        float : Berekende positiegrootte in lots
        """
        if entry_price == 0 or stop_loss == 0:
            self.logger.log_info(f"Ongeldige entry of stop loss voor {symbol}", level="ERROR")
            return 0.01

        # Voorkom delen door nul
        if entry_price == stop_loss:
            self.logger.log_info(f"Entry gelijk aan stop loss voor {symbol}", level="WARNING")
            return 0.01

        # Bereken risicobedrag in accountvaluta
        risk_amount = account_balance * self.max_risk_per_trade

        # Pas risico aan op basis van trendsterkte
        adjusted_risk = risk_amount * (0.5 + trend_strength / 2)  # 50-100% van normaal risico

        # Bereken pips op risico
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # Voor 4-cijferige forex paren

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01  # Voor goud (0.01 = 1 pip)
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1  # Voor indices

        # Schat pip waarde (kan worden verbeterd met exacte berekening per symbool)
        pip_value = 10.0  # Standaard pip waarde voor 1 lot

        # Bereken lot size
        lot_size = adjusted_risk / (pips_at_risk * pip_value)

        # Rond af naar 2 decimalen en begrens tussen min/max waarden
        min_lot = 0.01
        max_lot = 10.0
        lot_size = max(min_lot, min(lot_size, max_lot))
        lot_size = round(lot_size, 2)

        self.logger.log_info(f"Berekende positiegrootte voor {symbol}: {lot_size} lots "
                             f"(Risk: ${adjusted_risk:.2f}, Pips: {pips_at_risk:.1f})")

        return lot_size

    def check_trade_risk(self,
                         symbol: str,
                         volume: float,
                         entry_price: float,
                         stop_loss: float) -> bool:
        """
        Controleer of een trade binnen de risicolimieten valt

        Parameters:
        -----------
        symbol : str
            Trading symbool
        volume : float
            Positiegrootte in lots
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs

        Returns:
        --------
        bool : True als trade binnen risicolimieten valt, anders False
        """
        # Controleer dagelijks aantal trades
        self.daily_trades_count += 1
        if self.daily_trades_count > self.max_daily_trades:
            self.logger.log_info(f"Maximaal aantal dagelijkse trades bereikt: {self.max_daily_trades}", level="WARNING")
            return False

        # Als er geen stop loss is, is dit een hoog risico en accepteren we de trade niet
        if stop_loss == 0:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Geen stop loss ingesteld", level="WARNING")
            return False

        # Berekening potentieel verlies
        pip_value = 10.0  # Standaard pip waarde voor 1 lot
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1

        potential_loss = pips_at_risk * pip_value * volume

        # Controleer tegen dagelijkse verlieslimiet
        max_daily_loss = self.initial_balance * self.max_daily_drawdown
        if self.daily_losses + potential_loss > max_daily_loss:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Zou dagelijkse verlieslimiet overschrijden",
                                 level="WARNING")
            return False

        # Extra validatie voor extreem grote posities
        if volume > 5.0:  # Voorbeeld van een arbitraire limiet
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Volume te groot ({volume} lots)", level="WARNING")
            return False

        # Trade geaccepteerd
        return True

    def can_trade(self) -> bool:
        """
        Controleert of trading is toegestaan op basis van huidige limieten

        Returns:
        --------
        bool : True als trading is toegestaan, anders False
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Controleer dagelijks aantal trades
        if self.daily_trades_count >= self.max_daily_trades:
            return False

        return True

    def update_daily_loss(self, loss_amount: float) -> None:
        """
        Update het dagelijkse verliestotaal

        Parameters:
        -----------
        loss_amount : float
            Verliesbedrag (positief voor verlies, negatief voor winst)
        """
        # Reset als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Update dagelijkse verliezen
        if loss_amount > 0:  # Alleen verliesposities bijhouden
            self.daily_losses += loss_amount
            self.logger.log_info(f"Dagelijks verlies bijgewerkt: ${self.daily_losses:.2f} "
                                 f"(Max: ${self.initial_balance * self.max_daily_drawdown:.2f})")