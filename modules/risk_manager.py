from datetime import datetime, date


class RiskManager:
    """Klasse voor risicobeheer met ondersteuning voor leverage"""

    def __init__(self, max_risk_per_trade=0.015, max_daily_drawdown=0.05, max_total_drawdown=0.1, leverage=30):
        """
        Initialiseer de risicomanager met hefboomondersteuning

        Parameters:
        -----------
        max_risk_per_trade : float
            Maximum risico per trade (percentage van account)
        max_daily_drawdown : float
            Maximum dagelijkse drawdown (percentage van account)
        max_total_drawdown : float
            Maximum totale drawdown (percentage van account)
        leverage : float
            Hefboommultiplier (bijv. 30 voor 1:30 hefboom)
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

        print(f"Risicomanager geïnitialiseerd met leverage 1:{leverage}")

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

    def calculate_position_size(self, symbol, entry_price, stop_loss, account_balance, trend_strength=0):
        """
        Bereken optimale positiegrootte gebaseerd op risicobeheer en leverage

        Parameters:
        -----------
        symbol : str
            Handelssymbool
        entry_price : float
            Entry prijs
        stop_loss : float
            Stop Loss prijs
        account_balance : float
            Huidige account balance
        trend_strength : float, optional
            Trendsterktefactor (0-1) voor risicoscaling

        Returns:
        --------
        float
            Optimale positiegrootte in lots
        """
        # Bereken risicoscaling op basis van trendsterkte (tot 50% extra)
        adjusted_risk = self.max_risk_per_trade * (1 + trend_strength * 0.5)

        # Bereken risicobedrag
        risk_amount = account_balance * adjusted_risk

        # Bereken pips risico
        pips_at_risk = self._calculate_pips_at_risk(symbol, entry_price, stop_loss)

        if pips_at_risk <= 0:
            print(f"Waarschuwing: Ongeldige pips_at_risk voor {symbol}: {pips_at_risk}")
            return 0.01  # Minimale lotgrootte als fallback

        # Bereken basis pip-waarde per standaard lot
        pip_value_per_lot = self._get_pip_value_per_lot(symbol)

        # Bereken optimale positiegrootte
        position_size = risk_amount / (pips_at_risk * pip_value_per_lot)

        # Schaal positiegrootte op basis van leverage
        # Hogere leverage = hogere positiegrootte voor hetzelfde risico
        # Dit is al impliciet verwerkt in margin-vereisten

        # Rond af en zorg dat we binnen acceptabele grenzen blijven
        position_size = round(position_size, 2)
        position_size = max(0.01, min(position_size, 20.0))

        print(
            f"Berekende positiegrootte: {position_size} lots (Risico: {adjusted_risk:.2%}, Leverage: 1:{self.leverage})")
        return position_size

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
        pip_value_per_lot = self._get_pip_value_per_lot(symbol)
        pips_at_risk = self._calculate_pips_at_risk(symbol, entry_price, stop_loss)
        potential_loss = volume * pip_value_per_lot * pips_at_risk

        # Registreer het risico per symbool
        self.current_trade_risks[symbol] = potential_loss

        # Totaal risico berekenen
        total_risk = sum(self.current_trade_risks.values())

        # Controleer tegen account grootte (aangenomen $100,000 account)
        account_size = 100000  # Uit config halen in een echte implementatie
        risk_percentage = total_risk / account_size

        # Voeg extra risicofactor toe voor hoge leverage
        if self.leverage > 20:
            risk_percentage *= 1.2  # 20% extra risicoweging voor hoge leverage

        print(f"Trade risico gecontroleerd: {risk_percentage:.2%} (max: {self.max_risk_per_trade:.2%})")
        return risk_percentage <= self.max_risk_per_trade

    def _get_pip_value_per_lot(self, symbol):
        """
        Bepaal de waarde van een pip per standaard lot voor een symbool

        Parameters:
        -----------
        symbol : str
            Handelssymbool

        Returns:
        --------
        float
            Pip waarde per standaard lot
        """
        # Standaardwaardes voor gangbare instrumenten
        if symbol == "EURUSD" or symbol == "GBPUSD" or "USD" in symbol and symbol != "XAUUSD":
            return 10.0  # Voor de meeste forex pairs met USD
        elif symbol == "XAUUSD":
            return 10.0  # Voor goud
        elif symbol == "US30":
            return 10.0  # Voor US30 index
        else:
            return 10.0  # Algemene schatting

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
        if entry_price == stop_loss:
            return 1  # Voorkom deling door nul en geef minimale pip risk

        difference = abs(entry_price - stop_loss)

        if symbol == "EURUSD" or symbol == "GBPUSD" or ("USD" in symbol and symbol != "XAUUSD"):
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
        current_daily_drawdown = self.daily_losses / account_size

        # Voeg extra bescherming toe bij hoge leverage
        if self.leverage > 20:
            # Verlaag de effectieve drawdown limiet met 10% bij hoge leverage
            adjusted_max_drawdown = self.max_daily_drawdown * 0.9
            return current_daily_drawdown <= adjusted_max_drawdown

        return current_daily_drawdown <= self.max_daily_drawdown