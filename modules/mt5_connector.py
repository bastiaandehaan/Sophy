import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time


class MT5Connector:
    """Klasse voor interactie met MetaTrader 5"""

    def __init__(self, mt5_config):
        """
        Initialiseer de MT5 connector

        Parameters:
        -----------
        mt5_config : dict
            Configuratie voor MT5 verbinding
        """
        self.config = mt5_config
        self.connected = False

    def connect(self):
        """Verbinding maken met MT5"""
        if not mt5.initialize(
                login=int(self.config['login']),
                password=self.config['password'],
                server=self.config['server'],
                path=self.config['mt5_pathway']
        ):
            print(f"MT5 initialisatie mislukt: {mt5.last_error()}")
            return False

        # Login naar MT5
        if not mt5.login(
                login=int(self.config['login']),
                password=self.config['password'],
                server=self.config['server']
        ):
            print(f"MT5 login mislukt: {mt5.last_error()}")
            mt5.shutdown()
            return False

        # Initialiseer symbolen
        for symbol in self.config['symbols']:
            if not self._initialize_symbol(symbol):
                print(f"Kon symbool {symbol} niet initialiseren")
                return False

        self.connected = True
        print(f"Verbonden met MT5: {mt5.account_info().server}")
        return True

    def disconnect(self):
        """Verbinding met MT5 verbreken"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            print("Verbinding met MT5 verbroken")

    def _initialize_symbol(self, symbol):
        """
        Initialiseer een symbool in MT5, met ondersteuning voor symbool mapping

        Parameters:
        -----------
        symbol : str
            Het te initialiseren symbool

        Returns:
        --------
        bool
            True als succesvol, anders False
        """
        # Controleer of er een mapping bestaat voor dit symbool
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config and symbol in self.config['symbol_mapping']:
            mapped_symbol = self.config['symbol_mapping'][symbol]
            print(f"Symbool mapping toegepast: {symbol} -> {mapped_symbol}")

        if not mt5.symbol_select(mapped_symbol, True):
            print(f"Symbool selectie mislukt voor {mapped_symbol}: {mt5.last_error()}")
            return False
        return True

    def get_historical_data(self, symbol, timeframe, bars_count):
        """
        Haal historische prijsdata op

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        timeframe : int
            MT5 timeframe constante (bijv. mt5.TIMEFRAME_D1)
        bars_count : int
            Aantal candles om op te halen

        Returns:
        --------
        pandas.DataFrame
            DataFrame met historische data of None bij fout
        """
        # Controleer verbinding
        if not self.connected:
            print("Niet verbonden met MT5")
            return None

        # Pas symbool mapping toe
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config and symbol in self.config['symbol_mapping']:
            mapped_symbol = self.config['symbol_mapping'][symbol]

        # Haal data op
        rates = mt5.copy_rates_from_pos(mapped_symbol, timeframe, 1, bars_count)
        if rates is None or len(rates) == 0:
            print(f"Geen historische data beschikbaar voor {mapped_symbol}")
            return pd.DataFrame()

        # Converteer naar DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def place_order(self, action, symbol, volume, sl, tp, price=0.0, comment=""):
        """
        Plaats een order in MT5

        Parameters:
        -----------
        action : str
            "BUY", "SELL", "BUY_STOP", "SELL_STOP", etc.
        symbol : str
            Het handelssymbool
        volume : float
            Order volume in lots
        sl : float
            Stop Loss prijs
        tp : float
            Take Profit prijs
        price : float, optional
            Limiet/Stop prijs (voor pending orders)
        comment : str, optional
            Commentaar bij de order

        Returns:
        --------
        int
            Order ticket nummer of None bij fout
        """
        # Controleer verbinding
        if not self.connected:
            print("Niet verbonden met MT5")
            return None

        # Pas symbool mapping toe
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config and symbol in self.config['symbol_mapping']:
            mapped_symbol = self.config['symbol_mapping'][symbol]

        # Maak request aan
        request = {
            "symbol": mapped_symbol,
            "volume": float(volume),
            "comment": comment,
        }

        # Type order bepalen
        if action == "BUY":
            request["action"] = mt5.TRADE_ACTION_DEAL
            request["type"] = mt5.ORDER_TYPE_BUY
            request["price"] = mt5.symbol_info_tick(mapped_symbol).ask
        elif action == "SELL":
            request["action"] = mt5.TRADE_ACTION_DEAL
            request["type"] = mt5.ORDER_TYPE_SELL
            request["price"] = mt5.symbol_info_tick(mapped_symbol).bid
        elif action == "BUY_STOP":
            request["action"] = mt5.TRADE_ACTION_PENDING
            request["type"] = mt5.ORDER_TYPE_BUY_STOP
            request["price"] = price
        elif action == "SELL_STOP":
            request["action"] = mt5.TRADE_ACTION_PENDING
            request["type"] = mt5.ORDER_TYPE_SELL_STOP
            request["price"] = price
        else:
            print(f"Onbekend actie type: {action}")
            return None

        # Voeg SL en TP toe
        if sl > 0:
            request["sl"] = sl
        if tp > 0:
            request["tp"] = tp

        # Voeg filling-type toe
        request["type_filling"] = mt5.ORDER_FILLING_IOC

        # Stuur order naar MT5
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order plaatsing mislukt: {result.retcode}, {result.comment}")
            return None

        print(f"Order succesvol geplaatst - ticket: {result.order}")
        return result.order

    def get_open_positions(self, symbol=None):
        """
        Haal open posities op

        Parameters:
        -----------
        symbol : str, optional
            Specifiek symbool of None voor alle posities

        Returns:
        --------
        list
            Lijst met open posities
        """
        if symbol:
            # Pas symbool mapping toe
            mapped_symbol = symbol
            if 'symbol_mapping' in self.config and symbol in self.config['symbol_mapping']:
                mapped_symbol = self.config['symbol_mapping'][symbol]
            return mt5.positions_get(symbol=mapped_symbol)
        return mt5.positions_get()

    def get_account_info(self):
        """
        Haal account informatie op

        Returns:
        --------
        dict
            Account informatie
        """
        account = mt5.account_info()
        if account is None:
            return {}

        return {
            'balance': account.balance,
            'equity': account.equity,
            'margin': account.margin,
            'free_margin': account.margin_free,
            'profit': account.profit
        }

    def get_symbol_tick(self, symbol):
        """
        Haal de huidige tick informatie op voor een symbool

        Parameters:
        -----------
        symbol : str
            Het handelssymbool

        Returns:
        --------
        tick object of None
            De huidige tick of None bij fout
        """
        # Controleer verbinding
        if not self.connected:
            print("Niet verbonden met MT5")
            return None

        # Pas symbool mapping toe
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config and symbol in self.config['symbol_mapping']:
            mapped_symbol = self.config['symbol_mapping'][symbol]

        return mt5.symbol_info_tick(mapped_symbol)