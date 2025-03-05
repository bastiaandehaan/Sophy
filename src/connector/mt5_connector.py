# src/connector/mt5_connector.py
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
import MetaTrader5 as mt5


class MT5Connector:
    """Verzorgt alle interacties met het MetaTrader 5 platform"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        """
        Initialiseer de MT5 connector met configuratie

        Args:
            config: Configuratie dictionary met MT5 connectie parameters
            logger: Logger instance voor het registreren van gebeurtenissen
        """
        self.config = config
        self.logger = logger
        self.connected = False
        self._initialize_error_messages()
        self.timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }

    def _initialize_error_messages(self) -> None:
        """Initialiseer foutmeldingen voor MT5 verbinding"""
        self.error_messages = {
            10013: "Ongeldige parameters voor verbinding",
            10014: "Verkeerde login of wachtwoord",
            10015: "Verkeerde server opgegeven",
            10016: "MT5 niet geïnstalleerd of niet gevonden",
            10018: "Verbinding met de server mislukt",
            10019: "Geen respons van server"
        }

    def connect(self) -> bool:
        """
        Maak verbinding met MT5 met uitgebreide foutafhandeling

        Returns:
            bool: True als verbinding succesvol, False anders
        """
        # Controleer of MT5 al is geïnitialiseerd
        if mt5.terminal_info() is not None and self.connected:
            self.logger.log_info("Al verbonden met MT5")
            return True

        # Sluit eerder gemaakte verbindingen
        mt5.shutdown()

        # Initialiseer MT5
        self.logger.log_info(f"Verbinden met MT5 op pad: {self.config.get('mt5_pathway', 'standaard pad')}")
        init_result = mt5.initialize(
            path=self.config.get('mt5_pathway'),
            login=self.config.get('login'),
            password=self.config.get('password'),
            server=self.config.get('server')
        )

        if not init_result:
            error_code = mt5.last_error()
            error_message = self.error_messages.get(
                error_code, f"Onbekende MT5 error: {error_code}")
            self.logger.log_info(f"MT5 initialisatie mislukt: {error_message}", level="ERROR")
            return False

        # Controleer verbinding
        if not mt5.terminal_info():
            self.logger.log_info("MT5 terminal info niet beschikbaar", level="ERROR")
            return False

        # Verbinding gemaakt
        self.connected = True
        account_info = mt5.account_info()

        if account_info:
            self.logger.log_info(f"Verbonden met MT5 account: {account_info.login}, "
                                 f"Server: {account_info.server}, "
                                 f"Type: {account_info.trade_mode_description}")
            return True
        else:
            self.logger.log_info("Kon geen account info ophalen", level="ERROR")
            return False

    def disconnect(self) -> None:
        """Sluit verbinding met MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.logger.log_info("Verbinding met MT5 afgesloten")

    def get_account_info(self) -> Dict[str, Any]:
        """
        Haal account informatie op van MT5

        Returns:
            Dict met account eigenschappen
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return {}

        account_info = mt5.account_info()
        if not account_info:
            self.logger.log_info("Kon account informatie niet ophalen", level="ERROR")
            return {}

        # Converteer naar dictionary
        result = {
            'login': account_info.login,
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'profit': account_info.profit,
            'margin_level': (account_info.equity / account_info.margin * 100
                             if account_info.margin > 0 else 0)
        }

        return result

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Converteer timeframe string naar MT5 constante

        Args:
            timeframe_str: Timeframe als string (bijv. 'H4')

        Returns:
            MT5 timeframe constante
        """
        return self.timeframe_map.get(timeframe_str, mt5.TIMEFRAME_H4)

    def get_historical_data(self,
                            symbol: str,
                            timeframe_or_str: Any,
                            bars_count: int = 100) -> pd.DataFrame:
        """
        Haal historische prijsdata op met geoptimaliseerde verwerking

        Args:
            symbol: Handelssymbool
            timeframe_or_str: MT5 timeframe constante of string ('H4', etc.)
            bars_count: Aantal bars om op te halen

        Returns:
            pd.DataFrame: DataFrame met historische data
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return pd.DataFrame()

        # Converteer timeframe string naar constante indien nodig
        timeframe = timeframe_or_str
        if isinstance(timeframe_or_str, str):
            timeframe = self.get_timeframe_constant(timeframe_or_str)

        # Probeer data op te halen met retry mechanisme
        retries = 3
        for attempt in range(retries):
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars_count)

            if rates is not None and len(rates) > 0:
                break

            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt om data op te halen voor {symbol}, opnieuw proberen...")
                time.sleep(1)

        if rates is None or len(rates) == 0:
            self.logger.log_info(f"Kon geen historische data ophalen voor {symbol} na {retries} pogingen",
                                 level="ERROR")
            return pd.DataFrame()

        # Converteer naar pandas DataFrame en bereken extra kolommen
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Hernoem kolommen naar lowercase voor consistentie
        df.columns = [col.lower() for col in df.columns]

        # Rename 'time' kolom naar 'date' voor consistentie in strategie code
        df.rename(columns={'time': 'date'}, inplace=True)

        return df

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """
        Haal actuele tick data op voor een symbool

        Args:
            symbol: Handelssymbool

        Returns:
            mt5.Tick object of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}. Error: {error_code}", level="ERROR")
            return None

        return tick

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Any]:
        """
        Haal open posities op

        Args:
            symbol: Optioneel filter op symbool

        Returns:
            Lijst met open posities
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return []

        positions = []

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            error_code = mt5.last_error()
            # Als er geen posities zijn is dit geen error
            if error_code == 0:
                return []
            self.logger.log_info(f"Kon geen posities ophalen. Error: {error_code}", level="ERROR")
            return []

        return list(positions)

    def place_order(self,
                    action: str,
                    symbol: str,
                    volume: float,
                    stop_loss: float = 0,
                    take_profit: float = 0,
                    comment: str = "") -> Optional[int]:
        """
        Plaats een order op het MT5 platform

        Args:
            action: "BUY" of "SELL"
            symbol: Handelssymbool
            volume: Order volume in lots
            stop_loss: Stop loss prijs (0 = geen stop loss)
            take_profit: Take profit prijs (0 = geen take profit)
            comment: Order commentaar

        Returns:
            Order ticket ID of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        # Haal symbool informatie op
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            self.logger.log_info(f"Kon geen informatie krijgen voor symbool {symbol}", level="ERROR")
            return None

        # Controleer of trading mogelijk is voor dit symbool
        if not symbol_info.visible or not symbol_info.trade_allowed:
            self.logger.log_info(f"Trading niet toegestaan voor {symbol}", level="ERROR")
            return None

        # Haal huidige prijs op
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}", level="ERROR")
            return None

        # Bepaal order type en prijs
        order_type = None
        price = None

        if action == "BUY":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        elif action == "SELL":
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            self.logger.log_info(f"Ongeldige actie: {action}", level="ERROR")
            return None

        # Bereid order request voor
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(stop_loss) if stop_loss > 0 else 0,
            "tp": float(take_profit) if take_profit > 0 else 0,
            "deviation": 10,  # prijsafwijking in punten
            "magic": 123456,  # magic number voor identificatie
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        # Stuur order naar MT5
        self.logger.log_info(
            f"Order versturen: {action} {volume} {symbol} @ {price}, SL: {stop_loss}, TP: {take_profit}")
        result = mt5.order_send(request)

        if result is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Order verzenden mislukt. Error code: {error_code}", level="ERROR")
            return None

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.log_info(f"Order mislukt. Retcode: {result.retcode}", level="ERROR")
            return None

        self.logger.log_info(f"Order succesvol geplaatst. Ticket: {result.order}")
        return result.order