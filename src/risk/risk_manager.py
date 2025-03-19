# src/risk/risk_manager.py
import random
import time
from datetime import datetime
from decimal import Decimal, getcontext, InvalidOperation
from typing import Dict, Optional, Any, Set

from src.connector.mt5_connector import MT5Connector
from src.utils.logger import Logger


class RiskManager:
    """
    Risicomanager die FTMO-regels implementeert en positiegrootte berekent.

    Belangrijkste functies:
    1. Berekent positiegrootte op basis van risico per trade.
    2. Houdt dagelijkse en totale drawdown bij volgens FTMO-regels.
    3. Bepaalt of trading mag doorgaan op basis van risicoparameters.
    """

    def __init__(
        self, config: Dict, logger: Logger, mt5_connector: MT5Connector
    ) -> None:
        """
        Initialiseer de risicomanager.

        Args:
            config (Dict): Configuratiedictionary met risicoparameters.
            logger (Logger): Logger instantie voor logging.
            mt5_connector (MT5Connector): MetaTrader 5 connector voor accountinformatie.
        """
        self.logger = logger
        self.mt5_connector = mt5_connector

        # Stel precisie in voor Decimal berekeningen (12 decimalen voor FX-trading)
        getcontext().prec = 12

        # Algemene risicoparameters
        self.risk_per_trade = Decimal(
            str(config.get("risk_per_trade", "0.01"))
        )  # 1% risico per trade
        self.max_trades_per_day = config.get("max_trades_per_day", 5)
        self.max_trades_per_symbol = config.get("max_trades_per_symbol", 1)

        # FTMO-specifieke parameters
        self.initial_balance = Decimal("0")  # Wordt ingesteld tijdens initialisatie
        self.daily_drawdown_limit = Decimal(
            str(config.get("daily_drawdown_limit", "0.05"))
        )  # 5% max dagelijks verlies
        self.total_drawdown_limit = Decimal(
            str(config.get("total_drawdown_limit", "0.10"))
        )  # 10% max totaal verlies
        self.profit_target = Decimal(
            str(config.get("profit_target", "0.10"))
        )  # 10% winstdoel
        self.min_trading_days = config.get(
            "min_trading_days", 4
        )  # Min. 4 dagen met trades

        # State bijhouden
        self.today_trades = 0
        self.today_pl = Decimal("0")
        self.trading_days: Set[datetime.date] = set()  # Correcte type-aanduiding
        self.highest_balance = Decimal("0")
        self.is_trading_allowed = True

        # Startdatum van de trading sessie
        self.start_date = datetime.now().date()

        self.logger.info(
            f"RiskManager geïnitialiseerd: risk_per_trade={self.risk_per_trade}, "
            f"daily_limit={self.daily_drawdown_limit * 100}%, "
            f"total_limit={self.total_drawdown_limit * 100}%"
        )

    def initialize(self) -> None:
        """
        Initialiseer de risk manager met de huidige accountgegevens.

        Haalt het huidige saldo op en stelt dit in als het initiële en hoogste saldo
        voor drawdown berekeningen.

        Raises:
            RuntimeError: Als initialisatie mislukt na meerdere pogingen.
        """
        account_info = self._retry_get_account_info(max_wait=10.0)
        if account_info:
            self.initial_balance = Decimal(str(account_info["balance"]))
            self.highest_balance = self.initial_balance
            self.logger.info(
                f"RiskManager geïnitialiseerd met saldo: {self.initial_balance}"
            )
        else:
            self.logger.error("Kon accountinformatie niet ophalen na meerdere pogingen")
            self.is_trading_allowed = False
            raise RuntimeError("RiskManager initialisatie mislukt")

    def _retry_get_account_info(
        self, retries: int = 3, delay: float = 1.0, max_wait: float = 10.0
    ) -> Optional[Dict[str, float]]:
        """
        Probeer accountinformatie op te halen met retries.

        Args:
            retries (int): Aantal retry-pogingen.
            delay (float): Basisvertraging tussen retries in seconden.
            max_wait (float): Maximale totale wachttijd in seconden.

        Returns:
            Optional[Dict[str, float]]: Accountinformatie of None als het mislukt.
        """
        total_wait = 0.0
        for attempt in range(retries):
            try:
                account_info = self.mt5_connector.get_account_info()
                if account_info:
                    return account_info
            except (ConnectionError, ValueError, InvalidOperation) as e:
                wait_time = delay + random.uniform(0, 0.5)  # Willekeurige vertraging
                total_wait += wait_time
                if total_wait > max_wait:
                    self.logger.error("Maximum wachttijd overschreden")
                    return None
                self.logger.warning(f"Poging {attempt + 1} mislukt: {e}")
                time.sleep(wait_time)
        self.logger.error("Kon accountinformatie niet ophalen na meerdere pogingen")
        return None

    def _retry_get_symbol_info(
        self, symbol: str, retries: int = 3, delay: float = 1.0, max_wait: float = 10.0
    ) -> Optional[Dict[str, Any]]:
        """
        Probeer symboolinformatie op te halen met retries.

        Args:
            symbol (str): Handelssymbool.
            retries (int): Aantal retry-pogingen.
            delay (float): Basisvertraging tussen retries in seconden.
            max_wait (float): Maximale totale wachttijd in seconden.

        Returns:
            Optional[Dict[str, Any]]: Symboolinformatie of None als het mislukt.
        """
        total_wait = 0.0
        for attempt in range(retries):
            try:
                symbol_info = self.mt5_connector.get_symbol_info(symbol)
                if symbol_info:
                    return symbol_info
            except (ConnectionError, ValueError, InvalidOperation) as e:
                wait_time = delay + random.uniform(0, 0.5)
                total_wait += wait_time
                if total_wait > max_wait:
                    self.logger.error(f"Maximum wachttijd overschreden voor {symbol}")
                    return None
                self.logger.warning(f"Poging {attempt + 1} mislukt: {e}")
                time.sleep(wait_time)
        self.logger.error(f"Kon symboolinformatie niet ophalen voor {symbol}")
        return None

    def calculate_position_size(
        self,
        symbol: str,
        entry_price: Decimal,
        stop_loss: Optional[Decimal] = None,
        risk_pips: Optional[Decimal] = None,
    ) -> float:
        """
        Calculate position size based on risk per trade.

        Args:
            symbol (str): Trading symbol.
            entry_price (Decimal): Entry price.
            stop_loss (Optional[Decimal]): Stop-loss price.
            risk_pips (Optional[Decimal]): Risk in pips.

        Returns:
            float: Volume in lots for the trade.

        Raises:
            ValueError: If essential calculations are invalid.
        """
        # Check if trading is allowed
        if not self.is_trading_allowed:
            return 0.0

        self._update_daily_state()
        if self.today_trades >= self.max_trades_per_day:
            self.logger.warning(
                f"Maximum daily trades reached: {self.max_trades_per_day}"
            )
            return 0.0

        # Get necessary information
        account_info = self._retry_get_account_info()
        symbol_info = self._retry_get_symbol_info(symbol)
        if not account_info or not symbol_info:
            self.logger.error(f"Could not retrieve information for {symbol}")
            return 0.0

        # Calculate risk amount
        account_balance = Decimal(str(account_info["balance"]))
        risk_amount = account_balance * self.risk_per_trade

        # Determine risk in pips
        actual_risk_pips = self._determine_risk_pips(
            symbol, entry_price, stop_loss, risk_pips
        )
        if actual_risk_pips <= Decimal("0"):
            self.logger.error(
                f"Invalid risk_pips calculated for {symbol}: {actual_risk_pips}"
            )
            return 0.0

        # Calculate pip value and position size
        pip_monetary_value = self._calculate_pip_monetary_value(symbol_info)
        if pip_monetary_value <= Decimal("0"):
            self.logger.error(f"Invalid pip value for {symbol}: {pip_monetary_value}")
            return 0.0

        # Calculate and adjust position size
        volume = risk_amount / (actual_risk_pips * pip_monetary_value)
        volume = self._adjust_volume_to_market_constraints(volume, symbol_info)

        self.logger.info(f"Calculated volume for {symbol}: {volume} lots")
        return float(volume)

    def _determine_risk_pips(
        self,
        symbol: str,
        entry_price: Decimal,
        stop_loss: Optional[Decimal],
        risk_pips: Optional[Decimal],
    ) -> Decimal:
        """Determine risk in pips for the trade."""
        if stop_loss is None and risk_pips is None:
            self.logger.warning(f"No stop-loss for {symbol}, using default 2%")
            return entry_price * Decimal("0.02")
        elif stop_loss is not None and risk_pips is None:
            return abs(entry_price - stop_loss)
        elif risk_pips is not None and risk_pips > Decimal("0"):
            return risk_pips
        else:
            self.logger.error(f"Invalid risk_pips for {symbol}: {risk_pips}")
            return Decimal("0")

    def _calculate_pip_monetary_value(self, symbol_info: Dict[str, Any]) -> Decimal:
        """Calculate the monetary value of a pip."""
        pip_value = Decimal(str(symbol_info.get("trade_tick_value", "0.0001")))
        contract_size = Decimal(str(symbol_info.get("trade_contract_size", "100000")))
        tick_size = Decimal(str(symbol_info.get("trade_tick_size", "0.00001")))
        points_per_pip = Decimal("0.0001") / tick_size
        return (pip_value * contract_size) / points_per_pip

    def _adjust_volume_to_market_constraints(
        self, volume: Decimal, symbol_info: Dict[str, Any]
    ) -> Decimal:
        """Adjust the calculated volume to match market constraints."""
        volume_step = Decimal(str(symbol_info.get("volume_step", "0.01")))
        volume = (volume / volume_step).quantize(volume_step) * volume_step

        min_volume = Decimal(str(symbol_info.get("volume_min", "0.01")))
        max_volume = Decimal(str(symbol_info.get("volume_max", "100.0")))
        return max(min_volume, min(volume, max_volume))

    def update_after_trade(
        self, symbol: str, profit_loss: Decimal, close_time: datetime
    ) -> None:
        """
        Update risk manager statistieken na een afgesloten trade.

        Args:
            symbol (str): Handelssymbool.
            profit_loss (Decimal): Winst of verlies van de trade.
            close_time (datetime): Sluitingstijd van de trade.
        """
        trade_date = close_time.date()
        self.trading_days.add(trade_date)

        if trade_date == datetime.now().date():
            self.today_pl += profit_loss

        account_info = self._retry_get_account_info()
        if account_info:
            current_balance = Decimal(str(account_info["balance"]))
            if current_balance > self.highest_balance:
                self.highest_balance = current_balance

        self.logger.info(
            f"Trade statistieken bijgewerkt: P/L=${profit_loss:.2f}, trading_dagen={len(self.trading_days)}"
        )
        self._check_trading_allowed()

    def _update_daily_state(self) -> None:
        """Reset dagelijkse statistieken als een nieuwe dag begint."""
        today = datetime.now().date()
        if self.start_date != today:
            self.today_trades = 0
            self.today_pl = Decimal("0")
            self.start_date = today
            self.logger.info(f"Nieuwe handelsdag gestart: {today}")

    def _check_trading_allowed(self) -> bool:
        """
        Controleer of trading is toegestaan volgens FTMO-regels.

        Returns:
            bool: Geeft aan of trading is toegestaan.
        """
        account_info = self._retry_get_account_info()
        if not account_info:
            self.logger.error("Kon accountinformatie niet ophalen voor controle")
            self.is_trading_allowed = False
            return False

        current_balance = Decimal(str(account_info["balance"]))

        daily_drawdown = Decimal("0")
        if self.initial_balance > Decimal("0"):
            daily_drawdown = (
                self.today_pl / self.initial_balance
                if self.today_pl < Decimal("0")
                else Decimal("0")
            )

        total_drawdown = Decimal("0")
        if self.highest_balance > Decimal("0"):
            total_drawdown = (
                self.highest_balance - current_balance
            ) / self.highest_balance

        if daily_drawdown >= self.daily_drawdown_limit:
            self.logger.warning(
                f"Dagelijkse drawdown limiet bereikt: {daily_drawdown * 100:.2f}% >= {self.daily_drawdown_limit * 100:.2f}%"
            )
            self.is_trading_allowed = False

        if total_drawdown >= self.total_drawdown_limit:
            self.logger.warning(
                f"Totale drawdown limiet bereikt: {total_drawdown * 100:.2f}% >= {self.total_drawdown_limit * 100:.2f}%"
            )
            self.is_trading_allowed = False

        if current_balance >= self.initial_balance * (
            Decimal("1") + self.profit_target
        ):
            self.logger.info(
                f"Winstdoel bereikt: ${current_balance:.2f} >= ${self.initial_balance * (Decimal('1') + self.profit_target):.2f}"
            )

        return self.is_trading_allowed

    def get_ftmo_status(self) -> Dict[str, float]:
        """
        Haal de huidige FTMO challenge status op.

        Returns:
            Dict[str, float]: Dictionary met FTMO status informatie.
        """
        account_info = self._retry_get_account_info()
        if not account_info:
            return {"error": 0.0}

        current_balance = Decimal(str(account_info["balance"]))
        profit_loss = current_balance - self.initial_balance
        profit_percentage = (
            profit_loss / self.initial_balance * 100
            if self.initial_balance > Decimal("0")
            else Decimal("0")
        )
        daily_drawdown = (
            abs(self.today_pl / self.initial_balance) * 100
            if self.today_pl < Decimal("0")
            else Decimal("0")
        )
        max_balance = max(self.highest_balance, current_balance)
        total_drawdown = (
            (max_balance - current_balance) / max_balance * 100
            if max_balance > Decimal("0")
            else Decimal("0")
        )

        trading_days_count = len(self.trading_days)
        trading_days_remaining = max(0, self.min_trading_days - trading_days_count)

        return {
            "initial_balance": float(self.initial_balance),
            "current_balance": float(current_balance),
            "profit_loss": float(profit_loss),
            "profit_percentage": float(profit_percentage),
            "profit_target_percentage": float(self.profit_target * 100),
            "profit_target_amount": float(self.initial_balance * self.profit_target),
            "daily_drawdown": float(daily_drawdown),
            "daily_drawdown_limit": float(self.daily_drawdown_limit * 100),
            "total_drawdown": float(total_drawdown),
            "total_drawdown_limit": float(self.total_drawdown_limit * 100),
            "trading_days": float(trading_days_count),
            "min_trading_days": float(self.min_trading_days),
            "trading_days_remaining": float(trading_days_remaining),
            "is_trading_allowed": float(int(self.is_trading_allowed)),
        }
