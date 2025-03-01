from datetime import datetime, date

class RiskManager:
    """Klasse voor risicobeheer"""

    def __init__(self, max_risk_per_trade=0.015, max_daily_drawdown=0.05, max_total_drawdown=0.1, leverage=10):
        """
        Initialiseer de risicomanager met hefboomoverweging

        Parameters:
        -----------
        max_risk_per_trade : float
            Maximum risico per trade (percentage van account)
        max_daily_drawdown : float
            Maximum dagelijkse drawdown (percentage van account)
        max_total_drawdown : float
            Maximum totale drawdown (percentage van account)
        leverage : float
            Hefboommultiplier (bijv. 10 voor 1:10 hefboom)
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_drawdown = max_daily_drawdown
        self.max_total_drawdown = max_total_drawdown
        self.leverage = leverage

        # Bijhouden van dagelijkse verliezen
        self.daily_losses = 0
        self.current_date = date.today()

        # Bijhouden van trade risico
        self.current_trade_risks = {}

    def reset_daily_metrics(self):
        """Reset dagelijkse metrieken als de datum is veranderd"""
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.current_date = today

    def update_daily_loss(self, loss_amount, account_balance):
        """
        Update dagelijkse verliezen

        Parameters:
        -----------
        loss_amount : float
            Verlies bedrag
        account_balance : float
            Huidige account balance

        Returns:
        --------
        bool
            True als limiet niet overschreden is, anders False
        """
        self.reset_daily_metrics()

        if loss_amount <= 0:
            return True

        self.daily_losses += loss_amount
        daily_drawdown = self.daily_losses / account_balance

        return daily_drawdown <= self.max_daily_drawdown

    def check_trade_risk(self, symbol, volume, entry_price, stop_loss):
        """
        Controleer of een trade voldoet aan de risicolimieten

        Parameters:
        -----------
        symbol : str
            Handelssymbool
        volume : float
            Order volume in lots
        entry_price : float
            Entry prijs
        stop_loss : float
            Stop Loss prijs

        Returns:
        --------
        bool
            True als de trade binnen risicolimieten valt, anders False
        """
        # Bereken mogelijk verlies
        pip_value = self._calculate_pip_value(symbol, volume)
        pips_at_risk = self._calculate_pips_at_risk(symbol, entry_price, stop_loss)
        potential_loss = pip_value * pips_at_risk

        # Registreer het risico per symbool
        self.current_trade_risks[symbol] = potential_loss

        # Totaal risico berekenen
        total_risk = sum(self.current_trade_risks.values())

        # Controleer tegen account grootte (aangenomen $100,000 account)
        account_size = 100000  # Uit config halen in een echte implementatie
        risk_percentage = total_risk / account_size

        return risk_percentage <= self.max_risk_per_trade

    def _calculate_pip_value(self, symbol, volume):
        """
        Bereken de waarde van een pip voor een bepaald symbool en volume

        Parameters:
        -----------
        symbol : str
            Handelssymbool
        volume : float
            Order volume in lots

        Returns:
        --------
        float
            Waarde van 1 pip
        """
        # Vereenvoudigde berekening - dit moet verfijnd worden per symbool
        if symbol == "EURUSD" or symbol == "GBPUSD" or "USD" in symbol:
            return volume * 10  # Voor de meeste forex pairs met USD
        elif symbol == "XAUUSD":
            return volume * 10  # Voor goud
        elif symbol == "US30":
            return volume * 10  # Voor US30 index
        else:
            return volume * 10  # Algemene schatting

    def _calculate_pips_at_risk(self, symbol, entry_price, stop_loss):
        """
        Bereken het aantal pips risico

        Parameters:
        -----------
        symbol : str
            Handelssymbool
        entry_price : float
            Entry prijs
        stop_loss : float
            Stop Loss prijs

        Returns:
        --------
        float
            Aantal pips risico
        """
        # De berekening is afhankelijk van het type instrument
        difference = abs(entry_price - stop_loss)

        if symbol == "EURUSD" or symbol == "GBPUSD" or "USD" in symbol:
            return difference / 0.0001  # 4 decimalen voor forex
        elif symbol == "XAUUSD":
            return difference / 0.1  # 1 decimaal voor goud
        elif symbol == "US30":
            return difference / 1.0  # 0 decimalen voor indices
        else:
            return difference / 0.0001  # Standaard

    def can_trade(self):
        """
        Controleert of er gehandeld kan worden op basis van dagelijkse drawdown

        Returns:
        --------
        bool
            True als handelen is toegestaan, anders False
        """
        self.reset_daily_metrics()
        account_size = 100000  # Uit config halen in een echte implementatie
        return self.daily_losses / account_size <= self.max_daily_drawdown