# src/connector/mt5_connector.py
# Voeg deze import toe bovenaan de file:
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

import MetaTrader5 as mt5
import pandas as pd


class MT5Connector:
    """Verzorgt alle interacties met het MetaTrader 5 platform"""

    def __init__(self, config: Dict[str, Any], logger: Any) -> None:
        """
        Initialiseer de MT5 connector met configuratie.

        Args:
            config (Dict[str, Any]): Configuratie dictionary met MT5 connectie parameters.
            logger (Any): Logger instance voor het registreren van gebeurtenissen.
        """
        self.config: Dict[str, Any] = config
        self.logger: Any = logger
        self.connected: bool = False
        self._initialize_error_messages()
        self.timeframe_map: Dict[str, int] = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }

    def _initialize_error_messages(self) -> None:
        """Initialiseer foutmeldingen voor MT5 verbinding."""
        self.error_messages: Dict[int, str] = {
            10013: "Ongeldige parameters voor verbinding",
            10014: "Verkeerde login of wachtwoord",
            10015: "Verkeerde server opgegeven",
            10016: "MT5 niet geïnstalleerd of niet gevonden",
            10018: "Verbinding met de server mislukt",
            10019: "Geen respons van server",
        }

    def connect(self, show_dialog: bool = True) -> bool:
        """
        Verbinding maken met het MT5 platform met verbeterde foutafhandeling.

        Args:
            show_dialog (bool): Of het dialoogvenster getoond moet worden bij inlogproblemen.

        Returns:
            bool: True als verbinding succesvol, anders False.
        """
        if self.connected:
            self.logger.log_info("Reeds verbonden met MT5")
            return True

        # Controleren of MT5 geïmporteerd kon worden
        if mt5 is None:
            self.logger.log_info("MetaTrader5 module niet beschikbaar", level="ERROR")
            return False

        # Initialiseren van MT5
        self.logger.log_info("Verbinding maken met MT5...")

        # Path valideren
        path = self.config.get("mt5_path", "")
        if not path or not os.path.exists(path):
            self.logger.log_info(f"MT5 pad niet gevonden: {path}", level="ERROR")
            self.logger.log_info("Zoeken naar standaard installatiepaden...")

            # Standaard installatielocaties proberen
            possible_paths = [
                r"C:\Program Files\MetaTrader 5\terminal64.exe",
                r"C:\Program Files (x86)\MetaTrader 5\terminal.exe",
                # Voeg meer standaard paden toe indien nodig
            ]

            for p in possible_paths:
                if os.path.exists(p):
                    path = p
                    self.logger.log_info(f"MT5 gevonden op: {path}")
                    break

        # Probeer te initialiseren
        initialized = False
        retries = 3

        for attempt in range(retries):
            try:
                if path and os.path.exists(path):
                    initialized = mt5.initialize(path=path)
                else:
                    # Probeer zonder pad
                    initialized = mt5.initialize()

                if initialized:
                    break

                error_code = mt5.last_error()
                self.logger.log_info(
                    f"MT5 initialisatie mislukt: {error_code[0]} - {error_code[1]}",
                    level="ERROR",
                )

            except Exception as e:
                self.logger.log_info(
                    f"Fout bij MT5 initialisatie: {str(e)}", level="ERROR"
                )

            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt, opnieuw proberen..."
                )
                time.sleep(2)

        if not initialized:
            self.logger.log_info(
                f"Kon MT5 niet initialiseren na {retries} pogingen", level="ERROR"
            )
            return False

        # Inloggen indien nodig
        login_required = False
        account_info = mt5.account_info()

        if account_info is None:
            login_required = True

        if login_required:
            login = self.config.get("mt5_login", 0)
            password = self.config.get("mt5_password", "")
            server = self.config.get("mt5_server", "")

            if login and password:
                self.logger.log_info(f"Inloggen bij account {login} op {server}...")

                login_result = False
                for attempt in range(retries):
                    try:
                        login_result = mt5.login(login, password, server)
                        if login_result:
                            break

                        error_code = mt5.last_error()
                        self.logger.log_info(
                            f"MT5 login mislukt: {error_code[0]} - {error_code[1]}",
                            level="ERROR",
                        )

                    except Exception as e:
                        self.logger.log_info(
                            f"Fout bij inloggen: {str(e)}", level="ERROR"
                        )

                    if attempt < retries - 1:
                        self.logger.log_info(
                            f"Login poging {attempt + 1} mislukt, opnieuw proberen..."
                        )
                        time.sleep(2)

                if not login_result:
                    self.logger.log_info("MT5 login mislukt", level="ERROR")
                    if show_dialog:
                        # Dialoogvenster tonen indien nodig
                        pass  # Implementatie afhankelijk van je UI
                    return False
            elif show_dialog:
                self.logger.log_info("Geen inloggegevens gevonden", level="WARNING")
                # Dialoogvenster tonen indien nodig
                pass  # Implementatie afhankelijk van je UI

        # Verbinding is nu succesvol
        self.connected = True
        account_info = mt5.account_info()

        if account_info:
            self.logger.log_info(
                f"Verbonden met account: {account_info.login} ({account_info.company})"
            )
            self.logger.log_info(
                f"Balans: {account_info.balance} {account_info.currency}"
            )

        return True

    def disconnect(self) -> None:
        """Sluit verbinding met MT5."""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.logger.log_info("Verbinding met MT5 afgesloten")

    def get_account_info(self) -> Dict[str, float]:
        """
        Haal account informatie op van MT5.

        Returns:
            Dict[str, float]: Dictionary met account eigenschappen.
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return {}

        account_info = mt5.account_info()
        if not account_info:
            self.logger.log_info("Kon account informatie niet ophalen", level="ERROR")
            return {}

        return {
            "login": float(account_info.login),
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin": account_info.margin,
            "free_margin": account_info.margin_free,
            "profit": account_info.profit,
            "margin_level": (
                account_info.equity / account_info.margin * 100
                if account_info.margin > 0
                else 0.0
            ),
        }

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Converteer timeframe string naar MT5 constante.

        Args:
            timeframe_str (str): Timeframe als string (bijv. 'H4').

        Returns:
            int: MT5 timeframe constante.

        Raises:
            ValueError: Als timeframe niet geldig is.
        """
        timeframe = self.timeframe_map.get(timeframe_str)
        if timeframe is None:
            raise ValueError(f"Ongeldige timeframe: {timeframe_str}")
        return timeframe

    def get_historical_data(
        self,
        symbol: str,
        timeframe_or_str: Union[str, int],
        bars_count: int = 100,
        start_pos: int = 0,
        from_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Haal historische prijsdata op met geoptimaliseerde verwerking.

        Args:
            symbol (str): Handelssymbool.
            timeframe_or_str (Union[str, int]): MT5 timeframe constante of string ('H4', etc.).
            bars_count (int): Aantal bars om op te halen.
            start_pos (int): Startpositie voor het ophalen van data (standaard 0).
            from_date (Optional[datetime]): Startdatum voor het ophalen van data (heeft voorrang op start_pos).

        Returns:
            pd.DataFrame: DataFrame met historische data.
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return pd.DataFrame()

        # Input validatie
        if not symbol or not isinstance(symbol, str):
            self.logger.log_info("Ongeldig symbool opgegeven", level="ERROR")
            return pd.DataFrame()

        if bars_count <= 0:
            self.logger.log_info("Aantal bars moet groter zijn dan 0", level="ERROR")
            return pd.DataFrame()

        timeframe = timeframe_or_str
        if isinstance(timeframe_or_str, str):
            timeframe = self.get_timeframe_constant(timeframe_or_str)

        retries = 3
        for attempt in range(retries):
            try:
                if from_date is not None:
                    # Haal data op vanaf specifieke datum als opgegeven
                    rates = mt5.copy_rates_from(
                        symbol, timeframe, from_date, bars_count
                    )
                else:
                    # Anders gebruik de positie
                    rates = mt5.copy_rates_from_pos(
                        symbol, timeframe, start_pos, bars_count
                    )

                if rates is not None and len(rates) > 0:
                    break
                if attempt < retries - 1:
                    self.logger.log_info(
                        f"Poging {attempt + 1} mislukt om data op te halen voor {symbol}, opnieuw proberen..."
                    )
                    time.sleep(1)
            except Exception as e:
                self.logger.log_info(f"Fout bij ophalen data: {str(e)}", level="ERROR")
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    return pd.DataFrame()

        if rates is None or len(rates) == 0:
            self.logger.log_info(
                f"Kon geen historische data ophalen voor {symbol} na {retries} pogingen",
                level="ERROR",
            )
            return pd.DataFrame()

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.columns = [col.lower() for col in df.columns]  # Correcte kolomnamen
        df.rename(columns={"time": "date"}, inplace=True)

        # Log het aantal opgehaalde bars
        self.logger.log_info(f"Succesvol {len(df)} bars opgehaald voor {symbol}")

        return df

    def get_symbol_tick(self, symbol: str) -> Optional[mt5.Tick]:
        """
        Haal actuele tick data op voor een symbool.

        Args:
            symbol (str): Handelssymbool.

        Returns:
            Optional[mt5.Tick]: Tick object of None bij fout.
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            error_code = mt5.last_error()
            self.logger.log_info(
                f"Kon geen tick informatie ophalen voor {symbol}. Error: {error_code}",
                level="ERROR",
            )
            return None
        return tick

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Any]:
        """
        Haal open posities op.

        Args:
            symbol (Optional[str]): Optioneel filter op symbool.

        Returns:
            List[mt5.Position]: Lijst met open posities.
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return []

        positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
        if positions is None:
            error_code = mt5.last_error()
            if error_code == 0:
                return []
            self.logger.log_info(
                f"Kon geen posities ophalen. Error: {error_code}", level="ERROR"
            )
            return []
        return list(positions)

    def place_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: Optional[float] = None,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        comment: str = "",
        magic: int = 0,
        expiration: Optional[datetime] = None,
    ) -> dict:
        """
        Plaats een handelsorder met foutafhandeling en validatie.

        Args:
            symbol (str): Handelssymbool.
            order_type (str): Type order ('BUY', 'SELL', 'BUY_LIMIT', etc.).
            volume (float): Volume in lots.
            price (Optional[float]): Prijs voor limit/stop orders.
            sl (Optional[float]): Stop Loss prijs.
            tp (Optional[float]): Take Profit prijs.
            comment (str): Commentaar bij de order.
            magic (int): Magic number voor de order.
            expiration (Optional[datetime]): Vervaldatum voor pending orders.

        Returns:
            dict: Resultaat met order informatie of foutbericht.
        """
        if not self.connected:
            error_msg = "Niet verbonden met MT5"
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        # Input validatie
        if not symbol or not isinstance(symbol, str):
            error_msg = "Ongeldig symbool opgegeven"
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        if volume <= 0:
            error_msg = "Volume moet groter zijn dan 0"
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        # Order type vertalen naar MT5 constanten
        order_type_map = {
            "BUY": mt5.ORDER_TYPE_BUY,
            "SELL": mt5.ORDER_TYPE_SELL,
            "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
            "BUY_STOP": mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP": mt5.ORDER_TYPE_SELL_STOP,
        }

        mt5_order_type = order_type_map.get(order_type.upper())
        if mt5_order_type is None:
            error_msg = f"Ongeldig order type: {order_type}"
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        # Minimaal handelslot controleren
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            error_msg = f"Symbool {symbol} niet gevonden"
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        min_lot = symbol_info.volume_min
        if volume < min_lot:
            error_msg = (
                f"Volume {volume} is lager dan minimaal toegestane volume {min_lot}"
            )
            self.logger.log_info(error_msg, level="ERROR")
            return {"success": False, "error": error_msg}

        # Order request aanmaken
        request = {
            "action": (
                mt5.TRADE_ACTION_DEAL
                if mt5_order_type in (mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL)
                else mt5.TRADE_ACTION_PENDING
            ),
            "symbol": symbol,
            "volume": volume,
            "type": mt5_order_type,
            "comment": comment,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,  # Good Till Cancelled
        }

        # Voorwaardelijke velden toevoegen
        if price is not None and mt5_order_type not in (
            mt5.ORDER_TYPE_BUY,
            mt5.ORDER_TYPE_SELL,
        ):
            request["price"] = price

        if sl is not None:
            request["sl"] = sl

        if tp is not None:
            request["tp"] = tp

        if expiration is not None and mt5_order_type not in (
            mt5.ORDER_TYPE_BUY,
            mt5.ORDER_TYPE_SELL,
        ):
            request["type_time"] = mt5.ORDER_TIME_SPECIFIED
            request["expiration"] = expiration

        # Voor market orders, huidige prijs invullen
        if mt5_order_type == mt5.ORDER_TYPE_BUY:
            request["price"] = symbol_info.ask
        elif mt5_order_type == mt5.ORDER_TYPE_SELL:
            request["price"] = symbol_info.bid

        # Order verzenden met retries
        retries = 3
        for attempt in range(retries):
            try:
                self.logger.log_info(f"Order verzenden: {request}")
                result = mt5.order_send(request)

                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    success_msg = f"Order succesvol geplaatst: Ticket #{result.order}"
                    self.logger.log_info(success_msg)
                    return {
                        "success": True,
                        "order_id": result.order,
                        "message": success_msg,
                        "request": request,
                        "result": {
                            "retcode": result.retcode,
                            "volume": result.volume,
                            "price": result.price,
                            "comment": result.comment,
                        },
                    }
                else:
                    error_msg = f"Order fout: {result.retcode}, {result.comment}"
                    self.logger.log_info(error_msg, level="ERROR")

                    # Specifieke fouten afhandelen
                    if result.retcode == mt5.TRADE_RETCODE_REQUOTE:
                        # Bij requote, probeer met nieuwe prijs
                        if mt5_order_type == mt5.ORDER_TYPE_BUY:
                            request["price"] = mt5.symbol_info_tick(symbol).ask
                        elif mt5_order_type == mt5.ORDER_TYPE_SELL:
                            request["price"] = mt5.symbol_info_tick(symbol).bid
                    elif result.retcode == mt5.TRADE_RETCODE_INVALID_VOLUME:
                        # Volume aanpassen naar toegestaan volume
                        request["volume"] = min_lot
            except Exception as e:
                error_msg = f"Uitzondering bij order verzenden: {str(e)}"
                self.logger.log_info(error_msg, level="ERROR")

            # Wacht voor volgende poging
            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt, opnieuw proberen..."
                )
                time.sleep(1)

        final_error = f"Order plaatsen mislukt na {retries} pogingen"
        self.logger.log_info(final_error, level="ERROR")
        return {"success": False, "error": final_error, "request": request}
