# src/analysis/advanced_backtester.py
import json
import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.ftmo.ftmo_validator import FTMOValidator
from src.risk.risk_manager import RiskManager
from src.strategy.base_strategy import Strategy
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("advanced_backtester")


@dataclass
class BacktestTrade:
    """Dataklasse om een enkele trade in backtesting te vertegenwoordigen."""
    symbol: str
    action: str  # 'BUY' of 'SELL'
    entry_date: datetime
    entry_price: float
    volume: float
    stop_loss: float = 0.0
    take_profit: float = 0.0
    exit_date: Optional[datetime] = None
    exit_price: float = 0.0
    exit_reason: str = ""
    profit: float = 0.0
    profit_pips: float = 0.0
    commission: float = 0.0
    swap: float = 0.0
    risk_reward_ratio: float = 0.0
    ticket: int = 0


@dataclass
class BacktestCandle:
    """Dataklasse om een enkele candlestick in backtesting te vertegenwoordigen."""
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    tick_volume: int
    timeframe: str


class BacktestTick:
    """Klasse om een tick prijs te simuleren."""

    def __init__(self, candle: BacktestCandle, spread_pips: float = 2.0):
        self.symbol = candle.symbol
        self.date = candle.date
        self.time = candle.date.timestamp()
        self.bid = candle.close
        # Simuleer de ask prijs met spread
        self.ask = candle.close + (spread_pips * self._get_pip_size(candle.symbol))

    @staticmethod
    def _get_pip_size(symbol: str) -> float:
        """Bepaal pip grootte voor symbool."""
        if symbol in ['XAUUSD', 'GOLD']:
            return 0.01  # Goud: 0.01 = 1 pip
        elif any(index in symbol for index in ['US30', 'US500', 'USTEC']):
            return 0.1  # Indices
        else:
            return 0.0001  # Forex pairs


class EventType:
    """Constanten voor event types in backtesting."""
    CANDLE = "CANDLE"
    TICK = "TICK"
    TRADE = "TRADE"
    ACCOUNT = "ACCOUNT"
    DAY_START = "DAY_START"
    DAY_END = "DAY_END"
    MARKER = "MARKER"


@dataclass
class Event:
    """Dataklasse om events in de backtest event loop te vertegenwoordigen."""
    type: str
    time: datetime
    data: Any


class BacktestConnector:
    """Een connector simulatie voor backtesting doeleinden met event-based architectuur."""

    def __init__(self, data_dir: str, initial_balance: float = 100000,
                 commission: float = 5.0, spread_pips: float = 2.0,
                 slippage_pips: float = 1.0, swap_pct: float = 0.01 / 365):
        """
        Initialiseer de backtest connector.

        Parameters:
        -----------
        data_dir : str
            Directory met historische data files
        initial_balance : float
            Startbalans voor het account
        commission : float
            Commissie per trade (per side) in de account valuta
        spread_pips : float
            Vaste spread in pips
        slippage_pips : float
            Vaste slippage in pips
        swap_pct : float
            Dagelijkse swap percentage
        """
        self.data_dir = data_dir
        self.initial_balance = initial_balance
        self.commission = commission
        self.spread_pips = spread_pips
        self.slippage_pips = slippage_pips
        self.swap_pct = swap_pct

        # Runtime data
        self.data_cache = {}
        self.current_time = None
        self.balance = initial_balance
        self.equity = initial_balance
        self.open_positions = {}
        self.closed_positions = []
        self.daily_pl = {}
        self.ticket_counter = 1
        self.symbol_data = {}
        self.events = []

        # Account details
        self.account_info = {
            'balance': initial_balance,
            'equity': initial_balance,
            'margin': 0,
            'free_margin': initial_balance,
            'margin_level': 0,
            'profit': 0
        }

        self.logger = logger

    def load_all_data(self, symbols: List[str], timeframe: str,
                      start_date: datetime, end_date: datetime) -> Tuple[bool, Dict]:
        """
        Laad historische data voor alle symbolen in een dictionary.

        Parameters:
        -----------
        symbols : List[str]
            Lijst met symbolen om te laden
        timeframe : str
            Timeframe om te gebruiken ('H1', 'H4', etc.)
        start_date : datetime
            Start datum voor backtesting
        end_date : datetime
            Eind datum voor backtesting

        Returns:
        --------
        Tuple[bool, Dict]
            (succes status, dictionary met geladen data)
        """
        all_data = {}
        for symbol in symbols:
            df = self._load_historical_data(symbol, timeframe)

            if df.empty:
                self.logger.error(f"Kon geen data laden voor {symbol} {timeframe}")
                continue

            # Filter data volgens datum bereik
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

            if df.empty:
                self.logger.error(f"Geen data voor {symbol} binnen datumbereik")
                continue

            all_data[symbol] = df
            self.logger.info(f"Geladen: {symbol} {timeframe} - {len(df)} candles")

        if not all_data:
            self.logger.error("Geen data geladen voor backtesting")
            return False, {}

        self.symbol_data = all_data
        return True, all_data

    def _load_historical_data(self, symbol: str, timeframe_str: str) -> pd.DataFrame:
        """Laad historische data uit CSV bestanden met caching."""
        cache_key = f"{symbol}_{timeframe_str}"
        if cache_key in self.data_cache:
            return self.data_cache[cache_key].copy()

        # Probeer meerdere bestandsformaten en locaties
        filename_options = [
            f"{symbol}_{timeframe_str}.csv",
            f"{symbol}.csv",
            f"{symbol.replace('/', '')}.csv",
            f"{symbol.lower()}_{timeframe_str.lower()}.csv"
        ]

        for filename in filename_options:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.logger.info(f"Laden van {filepath}")
                    df = pd.read_csv(filepath)

                    # Normalize column names
                    df.columns = [col.lower() for col in df.columns]

                    # Handle date/time column
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                    elif 'time' in df.columns:
                        df['date'] = pd.to_datetime(df['time'])
                        df.drop('time', axis=1, inplace=True)
                    else:
                        # Zoek naar een datetime kolom
                        for col in df.columns:
                            if df[col].dtype == 'object' and df[col].iloc[0] and any(
                                    c in str(df[col].iloc[0]) for c in [':', '-']):
                                df['date'] = pd.to_datetime(df[col])
                                if col != 'date':
                                    df.drop(col, axis=1, inplace=True)
                                break

                    # Controleer dat we alle benodigde kolommen hebben
                    required_cols = {'open', 'high', 'low', 'close'}

                    # Als volume of tick_volume ontbreekt, voeg het toe als dummy
                    if 'volume' not in df.columns and 'tick_volume' not in df.columns:
                        df['tick_volume'] = 100

                    if 'tick_volume' not in df.columns and 'volume' in df.columns:
                        df['tick_volume'] = df['volume']

                    if not all(col in df.columns for col in required_cols):
                        self.logger.warning(
                            f"Bestand {filename} mist vereiste kolommen: {required_cols - set(df.columns)}")
                        continue

                    self.data_cache[cache_key] = df
                    return df.copy()

                except Exception as e:
                    self.logger.error(f"Fout bij laden van {filepath}: {e}")

        self.logger.error(f"Kon geen bruikbaar bestand vinden voor {symbol}_{timeframe_str}")
        return pd.DataFrame()

    def generate_events(self, all_data: Dict[str, pd.DataFrame]) -> List[Event]:
        """
        Genereer alle events in chronologische volgorde voor backtesting.

        Parameters:
        -----------
        all_data : Dict[str, pd.DataFrame]
            Dictionary met historische data per symbool

        Returns:
        --------
        List[Event]
            Lijst met events in chronologische volgorde
        """
        events = []

        # Bepaal de start and eind datum over alle symbolen
        min_date = None
        max_date = None

        for symbol, df in all_data.items():
            if df.empty:
                continue

            sym_min = df['date'].min()
            sym_max = df['date'].max()

            if min_date is None or sym_min < min_date:
                min_date = sym_min

            if max_date is None or sym_max > max_date:
                max_date = sym_max

        if min_date is None or max_date is None:
            self.logger.error("Geen geldige data om events te genereren")
            return []

        # Genereer candle events voor elk symbool
        for symbol, df in all_data.items():
            for _, row in df.iterrows():
                candle = BacktestCandle(
                    symbol=symbol,
                    date=row['date'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    tick_volume=row['tick_volume'],
                    timeframe="H4"  # Update met dynamische timeframe indien nodig
                )

                # Voeg candle event toe
                events.append(Event(
                    type=EventType.CANDLE,
                    time=row['date'],
                    data=candle
                ))

                # Voeg tick event toe (iets na candle event)
                tick = BacktestTick(candle, self.spread_pips)
                events.append(Event(
                    type=EventType.TICK,
                    time=row['date'] + timedelta(microseconds=1),
                    data=tick
                ))

        # Genereer dag start/eind events
        current_date = min_date.date()
        end_date = max_date.date()

        while current_date <= end_date:
            day_start = datetime.combine(current_date, datetime.min.time())
            day_end = datetime.combine(current_date, datetime.max.time())

            events.append(Event(
                type=EventType.DAY_START,
                time=day_start,
                data={"date": current_date}
            ))

            events.append(Event(
                type=EventType.DAY_END,
                time=day_end,
                data={"date": current_date}
            ))

            current_date += timedelta(days=1)

        # Sorteer alle events op tijd
        events.sort(key=lambda x: x.time)

        self.logger.info(f"Gegenereerd: {len(events)} events van {min_date} tot {max_date}")
        return events

    def process_event(self, event: Event, strategy: Strategy) -> List[Dict]:
        """
        Verwerk een enkel event in de backtest.

        Parameters:
        -----------
        event : Event
            Het te verwerken event
        strategy : Strategy
            De handelsstrategie om te gebruiken

        Returns:
        --------
        List[Dict]
            Lijst met actie resultaten voor logging
        """
        results = []
        self.current_time = event.time

        if event.type == EventType.CANDLE:
            # Update de interne candle cache
            candle = event.data
            symbol = candle.symbol

            # Sla strategie verwerking over bij candle events, die doen we bij tick events
            results.append({
                "time": self.current_time,
                "type": "CANDLE",
                "symbol": symbol,
                "close": candle.close,
                "data": candle
            })

        elif event.type == EventType.TICK:
            # Elke tick kunnen we de strategie evalueren
            tick = event.data
            symbol = tick.symbol

            # Simuleer MT5 get_symbol_tick
            def get_symbol_tick_mock(sym):
                if sym == symbol:
                    return tick
                return None

            # Vervang de connector's get_symbol_tick functie tijdelijk
            original_get_tick = strategy.connector.get_symbol_tick
            strategy.connector.get_symbol_tick = get_symbol_tick_mock

            # Evalueer de strategie
            strategy_result = strategy.process_symbol(symbol)

            # Herstel de originele functie
            strategy.connector.get_symbol_tick = original_get_tick

            if strategy_result.get('signal') == 'ENTRY':
                # Plaats trade
                action = strategy_result.get('action')
                volume = strategy_result.get('volume', 0.1)
                stop_loss = strategy_result.get('stop_loss', 0)

                # Simuleer het plaatsen van een order
                price = tick.ask if action == 'BUY' else tick.bid
                # Voeg slippage toe
                if action == 'BUY':
                    price += self.slippage_pips * self._get_pip_size(symbol)
                else:
                    price -= self.slippage_pips * self._get_pip_size(symbol)

                ticket = self.place_order(action, symbol, volume, price, stop_loss, 0)

                results.append({
                    "time": self.current_time,
                    "type": "TRADE",
                    "action": "ENTRY",
                    "symbol": symbol,
                    "price": price,
                    "volume": volume,
                    "stop_loss": stop_loss,
                    "ticket": ticket
                })

            # Verwerk eventuele exit signalen
            for pos in list(self.open_positions.values()):
                if pos['symbol'] == symbol:
                    # Controleer stop loss
                    current_price = tick.bid if pos['action'] == 'BUY' else tick.ask

                    if (pos['action'] == 'BUY' and current_price <= pos['stop_loss'] and pos['stop_loss'] > 0) or \
                            (pos['action'] == 'SELL' and current_price >= pos['stop_loss'] and pos['stop_loss'] > 0):
                        self.close_position(pos['ticket'], current_price, "Stop Loss", tick.time)
                        results.append({
                            "time": self.current_time,
                            "type": "TRADE",
                            "action": "EXIT",
                            "symbol": symbol,
                            "price": current_price,
                            "volume": pos['volume'],
                            "reason": "Stop Loss",
                            "ticket": pos['ticket'],
                            "profit": pos['profit']
                        })

            # Update open positie waarderingen
            self._mark_positions_to_market(tick)

        elif event.type == EventType.DAY_START:
            # Reset dagelijkse P&L tracking
            day_date = event.data['date']
            self.daily_pl[day_date] = 0

            results.append({
                "time": self.current_time,
                "type": "DAY_START",
                "date": day_date
            })

        elif event.type == EventType.DAY_END:
            # Bereken dagelijkse swap op open posities
            day_date = event.data['date']
            for pos in self.open_positions.values():
                # Simuleer swap kosten (interest) op open posities
                days_held = (self.current_time.date() - pos['entry_time'].date()).days

                if days_held > 0:
                    swap_amount = pos['volume'] * pos['entry_price'] * self.swap_pct
                    pos['swap'] += swap_amount
                    pos['profit'] -= swap_amount
                    self.equity -= swap_amount

            # Update dagelijkse P&L
            self.daily_pl[day_date] = self.equity - self.account_info['balance']

            # Update account info
            self.account_info['equity'] = self.equity

            results.append({
                "time": self.current_time,
                "type": "DAY_END",
                "date": day_date,
                "daily_pl": self.daily_pl[day_date],
                "equity": self.equity,
                "balance": self.balance
            })

        return results

    def place_order(self, action: str, symbol: str, volume: float, price: float,
                    stop_loss: float, take_profit: float, comment: str = "") -> int:
        """
        Simuleer het plaatsen van een order.

        Parameters:
        -----------
        action : str
            'BUY' of 'SELL'
        symbol : str
            Handelssymbool
        volume : float
            Ordervolume in lots
        price : float
            Uitvoeringsprijs
        stop_loss : float
            Stop loss prijs (0 = geen)
        take_profit : float
            Take profit prijs (0 = geen)
        comment : str
            Order commentaar

        Returns:
        --------
        int : Ticket ID
        """
        # Genereer ticket nummer
        ticket = self.ticket_counter
        self.ticket_counter += 1

        # Bereken commissie
        commission = volume * self.commission

        # Maak positie
        position = {
            'ticket': ticket,
            'symbol': symbol,
            'action': action,
            'volume': volume,
            'entry_price': price,
            'current_price': price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_time': self.current_time,
            'profit': -commission,  # Begin met negatieve winst vanwege commissie
            'commission': commission,
            'swap': 0.0,
            'comment': comment
        }

        # Voeg toe aan open posities
        self.open_positions[ticket] = position

        # Update account
        self.equity -= commission

        return ticket

    def close_position(self, ticket: int, close_price: float, reason: str = "",
                       close_time: Optional[float] = None) -> bool:
        """
        Sluit een open positie.

        Parameters:
        -----------
        ticket : int
            Ticket ID van de positie
        close_price : float
            Sluitingsprijs
        reason : str
            Reden voor sluiting
        close_time : Optional[float]
            Timestamp van sluiting (gebruikt voor datetime conversie)

        Returns:
        --------
        bool : True als succesvol gesloten
        """
        if ticket not in self.open_positions:
            return False

        pos = self.open_positions[ticket]
        pos['exit_price'] = close_price
        pos['exit_time'] = datetime.fromtimestamp(close_time) if close_time else self.current_time
        pos['exit_reason'] = reason

        # Bereken P&L
        pip_size = self._get_pip_size(pos['symbol'])
        price_diff = close_price - pos['entry_price']

        if pos['action'] == 'SELL':
            price_diff = -price_diff

        # Bereken winst in account valuta
        profit_pips = price_diff / pip_size
        raw_profit = profit_pips * pip_size * pos['volume'] * 100000
        total_profit = raw_profit - pos['commission'] - pos['swap']

        pos['profit_pips'] = profit_pips
        pos['profit'] = total_profit

        # Update account
        self.balance += total_profit
        self.equity = self.balance
        self.account_info['balance'] = self.balance
        self.account_info['equity'] = self.equity

        # Voeg toe aan gesloten posities
        self.closed_positions.append(pos.copy())

        # Verwijder uit open posities
        del self.open_positions[ticket]

        return True

    def _mark_positions_to_market(self, tick) -> None:
        """
        Update de waardering van alle open posities voor een symbool op de huidige marktprijzen.

        Parameters:
        -----------
        tick : BacktestTick
            Huidige tick voor het symbool
        """
        symbol = tick.symbol

        for pos in self.open_positions.values():
            if pos['symbol'] == symbol:
                # Update huidige prijs
                pos['current_price'] = tick.bid if pos['action'] == 'BUY' else tick.ask

                # Herbereken winst
                pip_size = self._get_pip_size(symbol)
                price_diff = pos['current_price'] - pos['entry_price']

                if pos['action'] == 'SELL':
                    price_diff = -price_diff

                profit_pips = price_diff / pip_size
                raw_profit = profit_pips * pip_size * pos['volume'] * 100000
                total_profit = raw_profit - pos['commission'] - pos['swap']

                # Update positie en account
                old_profit = pos['profit']
                pos['profit'] = total_profit
                profit_change = total_profit - old_profit

                self.equity += profit_change
                self.account_info['equity'] = self.equity
                self.account_info['profit'] = sum(p['profit'] for p in self.open_positions.values())

    def get_account_info(self) -> Dict[str, Any]:
        """
        Haal huidige account info op.

        Returns:
        --------
        Dict[str, Any] : Account informatie
        """
        # Update margin en marge level
        total_margin = sum(
            p['volume'] * p['current_price'] * 100000 / self.account_info.get('leverage', 100)
            for p in self.open_positions.values()
        )

        self.account_info['margin'] = total_margin
        self.account_info['free_margin'] = self.equity - total_margin

        if total_margin > 0:
            self.account_info['margin_level'] = (self.equity / total_margin) * 100
        else:
            self.account_info['margin_level'] = 0

        return self.account_info.copy()

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Haal open posities op.

        Parameters:
        -----------
        symbol : Optional[str]
            Filter op specifiek symbool

        Returns:
        --------
        List[Dict] : Lijst met open posities
        """
        if symbol:
            return [p for p in self.open_positions.values() if p['symbol'] == symbol]
        else:
            return list(self.open_positions.values())

    def get_closed_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Haal gesloten posities op.

        Parameters:
        -----------
        symbol : Optional[str]
            Filter op specifiek symbool

        Returns:
        --------
        List[Dict] : Lijst met gesloten posities
        """
        if symbol:
            return [p for p in self.closed_positions if p['symbol'] == symbol]
        else:
            return self.closed_positions.copy()

    def reset(self) -> None:
        """Reset de backtest state."""
        self.balance = self.initial_balance
        self.equity = self.initial_balance
        self.open_positions = {}
        self.closed_positions = []
        self.daily_pl = {}
        self.ticket_counter = 1
        self.current_time = None

        self.account_info = {
            'balance': self.initial_balance,
            'equity': self.initial_balance,
            'margin': 0,
            'free_margin': self.initial_balance,
            'margin_level': 0,
            'profit': 0
        }

    @staticmethod
    def _get_pip_size(symbol: str) -> float:
        """Bepaal pip grootte voor symbool."""
        if symbol in ['XAUUSD', 'GOLD']:
            return 0.01  # Goud: 0.01 = 1 pip
        elif any(index in symbol for index in ['US30', 'US500', 'USTEC']):
            return 0.1  # Indices
        else:
            return 0.0001  # Forex pairs


class Backtester:
    """Geavanceerde backtester met event-driven architectuur en parallelisatie."""

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de backtester.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/backtest_log.csv'))

        self.output_dir = self.config.get('output', {}).get('data_dir', 'data')
        os.makedirs(self.output_dir, exist_ok=True)

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def run_backtest(self, strategy_name: str = None, symbols: List[str] = None,
                     timeframe: str = None, start_date: str = None, end_date: str = None,
                     initial_balance: float = None, commission: float = 5.0,
                     spread_pips: float = 2.0, slippage_pips: float = 1.0,
                     parameters: Dict[str, Any] = None, optimize: bool = False,
                     plot_results: bool = True) -> Dict[str, Any]:
        """
        Voer een backtest uit met de opgegeven parameters.

        Parameters:
        -----------
        strategy_name : Optional[str]
            Naam van de strategie (als None, dan uit config)
        symbols : Optional[List[str]]
            Lijst met handelssymbolen (als None, dan uit config)
        timeframe : Optional[str]
            Timeframe voor analyse (als None, dan uit config)
        start_date : Optional[str]
            Startdatum in formaat 'YYYY-MM-DD'
        end_date : Optional[str]
            Einddatum in formaat 'YYYY-MM-DD'
        initial_balance : Optional[float]
            Startbalans (als None, dan uit config)
        commission : float
            Commissie per trade
        spread_pips : float
            Spread in pips
        slippage_pips : float
            Slippage in pips
        parameters : Optional[Dict[str, Any]]
            Strategie parameters om de standaard config te overschrijven
        optimize : bool
            Of parameter optimalisatie uitgevoerd moet worden
        plot_results : bool
            Of resultaten geplot moeten worden

        Returns:
        --------
        Dict[str, Any] : Resultaten van de backtest
        """
        # Stel waarden in uit config of parameters
        strategy_name = strategy_name or self.config['strategy'].get('name', 'turtle')
        symbols = symbols or self.config['mt5'].get('symbols', ['EURUSD'])
        timeframe = timeframe or self.config['mt5'].get('timeframe', 'H4')
        initial_balance = initial_balance or self.config['mt5'].get('account_balance', 100000)

        # Parse datums
        default_end = datetime.now()
        default_start = default_end - timedelta(days=365)

        if start_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_dt = self.config.get('backtest', {}).get('start_date', default_start)
            if isinstance(start_dt, str):
                start_dt = datetime.strptime(start_dt, '%Y-%m-%d')

        if end_date:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_dt = self.config.get('backtest', {}).get('end_date', default_end)
            if isinstance(end_dt, str):
                end_dt = datetime.strptime(end_dt, '%Y-%m-%d')

        self.logger.log_info(f"===== Starten Backtest: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}")
        self.logger.log_info(f"Periode: {start_dt.strftime('%Y-%m-%d')} tot {end_dt.strftime('%Y-%m-%d')}")

        # Maak data directory indien nodig
        data_dir = self.config.get('output', {}).get('data_dir', 'data')

        # Initialiseer connector
        connector = BacktestConnector(
            data_dir=data_dir,
            initial_balance=initial_balance,
            commission=commission,
            spread_pips=spread_pips,
            slippage_pips=slippage_pips
        )

        # Laad historische data
        success, all_data = connector.load_all_data(symbols, timeframe, start_dt, end_dt)

        if not success:
            self.logger.log_info("Backtest afgebroken wegens ontbrekende data", level="ERROR")
            return {"success": False, "error": "Missing data"}

        # Maak aangepaste configuratie voor de strategie
        strategy_config = self.config.copy()

        # Pas parameters aan indien opgegeven
        if parameters:
            if 'strategy' not in strategy_config:
                strategy_config['strategy'] = {}

            for key, value in parameters.items():
                strategy_config['strategy'][key] = value

            self.logger.log_info(f"Aangepaste parameters: {parameters}")

        # Initialiseer risk manager
        risk_manager = RiskManager(self.config['risk'], self.logger)

        # Maak strategie
        strategy = StrategyFactory.create_strategy(
            strategy_name, connector, risk_manager, self.logger, strategy_config
        )

        # Genereer events voor backtesting
        events = connector.generate_events(all_data)

        if not events:
            self.logger.log_info("Geen events gegenereerd voor backtest", level="ERROR")
            return {"success": False, "error": "No events generated"}

        # Run event loop
        start_time = time.time()
        self.logger.log_info(f"Start backtest met {len(events)} events...")

        backtest_log = []

        for event in events:
            results = connector.process_event(event, strategy)
            backtest_log.extend(results)

        elapsed = time.time() - start_time
        self.logger.log_info(f"Backtest voltooid in {elapsed:.2f} seconden")

        # Analyseer resultaten
        trades = connector.get_closed_positions()
        account_data = self._extract_account_data(backtest_log)

        # Bereken performancemetrics
        metrics = self._calculate_performance_metrics(
            trades, account_data, initial_balance, start_dt, end_dt
        )

        # Log performance metrics
        self.logger.log_info(f"Totaal aantal trades: {metrics['total_trades']}")
        self.logger.log_info(f"Winstgevende trades: {metrics['winning_trades']} ({metrics['win_rate']:.2f}%)")
        self.logger.log_info(f"Verliesgevende trades: {metrics['losing_trades']}")
        self.logger.log_info(f"Profit factor: {metrics['profit_factor']:.2f}")
        self.logger.log_info(f"Netto winst: {metrics['net_profit']:.2f} ({metrics['net_profit_pct']:.2f}%)")
        self.logger.log_info(f"Max drawdown: {metrics['max_drawdown_pct']:.2f}%")
        self.logger.log_info(f"Gemiddelde trade: {metrics['avg_trade']:.2f}")

        # Plot resultaten
        if plot_results:
            self._plot_equity_curve(account_data, initial_balance, metrics)
            self._plot_drawdown_curve(account_data)
            self._plot_monthly_returns(account_data)
            self._plot_trade_analysis(trades)

        # Check FTMO compliance
        metrics['ftmo_compliance'] = self._check_ftmo_compliance(
            account_data, initial_balance, metrics
        )

        # Sla resultaten op voor analyse
        self._save_backtest_results(
            strategy_name, symbols, metrics, trades, account_data, parameters
        )

        # Compileer resultaten
        results = {
            "success": True,
            "metrics": metrics,
            "trades": trades,
            "account_data": account_data,
            "parameters": parameters or self.config['strategy']
        }

        return results

    def run_optimization(self, strategy_name: str, symbols: List[str],
                         param_ranges: Dict[str, List[Any]], start_date: str, end_date: str,
                         initial_balance: float = 100000, metric: str = 'sharpe_ratio',
                         max_workers: int = None) -> Dict[str, Any]:
        """
        Voer parameter optimalisatie uit met parallelle verwerking.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie om te optimaliseren
        symbols : List[str]
            Lijst met handelssymbolen
        param_ranges : Dict[str, List[Any]]
            Dictionary met parameter namen en mogelijke waarden
        start_date : str
            Startdatum in formaat 'YYYY-MM-DD'
        end_date : str
            Einddatum in formaat 'YYYY-MM-DD'
        initial_balance : float
            Startbalans
        metric : str
            Prestatiemetric om te optimaliseren
        max_workers : Optional[int]
            Maximum aantal workers voor parallellisatie

        Returns:
        --------
        Dict[str, Any] : Resultaten van de optimalisatie
        """
        self.logger.log_info(f"===== Starten Parameter Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Genereer alle parametercombinaties
        param_keys = list(param_ranges.keys())
        param_values = [param_ranges[key] for key in param_keys]

        # Recursieve functie om alle combinaties te maken
        def generate_combinations(keys, values, current_idx=0, current_dict=None):
            if current_dict is None:
                current_dict = {}

            if current_idx == len(keys):
                return [current_dict.copy()]

            result = []
            for val in values[current_idx]:
                current_dict[keys[current_idx]] = val
                result.extend(generate_combinations(keys, values, current_idx + 1, current_dict))

            return result

        param_combinations = generate_combinations(param_keys, param_values)

        self.logger.log_info(f"Gegenereerd: {len(param_combinations)} parametercombinaties")

        # Functie om één parameterset te evalueren
        def evaluate_params(params):
            try:
                self.logger.log_info(f"Evalueren parameters: {params}")
                result = self.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    start_date=start_date,
                    end_date=end_date,
                    initial_balance=initial_balance,
                    parameters=params,
                    plot_results=False
                )

                if not result['success']:
                    return {
                        'parameters': params,
                        'success': False,
                        'error': result.get('error', 'Unknown error'),
                        'metrics': {}
                    }

                return {
                    'parameters': params,
                    'success': True,
                    'metrics': result['metrics']
                }
            except Exception as e:
                self.logger.log_info(f"Fout bij evalueren parameters {params}: {str(e)}", level="ERROR")
                return {
                    'parameters': params,
                    'success': False,
                    'error': str(e),
                    'metrics': {}
                }

        # Voer optimalisatie parallel uit
        results = []
        start_time = time.time()

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(evaluate_params, params) for params in param_combinations]

            for i, future in enumerate(as_completed(futures)):
                try:
                    result = future.result()
                    results.append(result)

                    # Log voortgang
                    if (i + 1) % 10 == 0 or (i + 1) == len(param_combinations):
                        self.logger.log_info(f"Voortgang: {i + 1}/{len(param_combinations)} combinaties geëvalueerd")

                except Exception as e:
                    self.logger.log_info(f"Fout in worker: {str(e)}", level="ERROR")

        elapsed = time.time() - start_time
        self.logger.log_info(f"Optimalisatie voltooid in {elapsed:.2f} seconden")

        # Filter succesvolle resultaten
        valid_results = [r for r in results if r['success']]

        if not valid_results:
            self.logger.log_info("Geen geldige resultaten gevonden tijdens optimalisatie", level="ERROR")
            return {"success": False, "error": "No valid results"}

        # Vind de beste parameters volgens de metric
        try:
            best_result = max(
                valid_results,
                key=lambda x: x['metrics'].get(metric, float('-inf'))
            )

            # Sla optimalisatieresultaten op
            self._save_optimization_results(strategy_name, symbols, metric, results, best_result)

            # Genereer optimalisatierapport
            self._plot_optimization_results(results, param_keys, metric)

            self.logger.log_info(f"Beste parameters gevonden: {best_result['parameters']}")
            self.logger.log_info(f"Beste {metric}: {best_result['metrics'].get(metric, 'N/A')}")

            # Run nog een keer met de beste parameters om plots te maken
            final_result = self.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                initial_balance=initial_balance,
                parameters=best_result['parameters'],
                plot_results=True
            )

            return {
                "success": True,
                "best_parameters": best_result['parameters'],
                "best_metrics": best_result['metrics'],
                "all_results": results,
                "final_result": final_result
            }

        except Exception as e:
            self.logger.log_info(f"Fout bij verwerken optimalisatieresultaten: {str(e)}", level="ERROR")
            return {"success": False, "error": str(e), "results": results}

    def _extract_account_data(self, backtest_log: List[Dict]) -> pd.DataFrame:
        """
        Extraheer account data uit backtest log.

        Parameters:
        -----------
        backtest_log : List[Dict]
            Log van backtest events

        Returns:
        --------
        pd.DataFrame : Account data per timestamp
        """
        # Filter relevante events
        account_events = [
            event for event in backtest_log
            if event['type'] in ['DAY_END', 'TRADE']
        ]

        if not account_events:
            return pd.DataFrame()

        # Converteer naar DataFrame
        df = pd.DataFrame(account_events)

        # Voeg ontbrekende kolommen toe indien nodig
        if 'equity' not in df.columns:
            df['equity'] = np.nan
        if 'balance' not in df.columns:
            df['balance'] = np.nan
        if 'daily_pl' not in df.columns:
            df['daily_pl'] = np.nan

        # Vul missende waarden in
        df['equity'].fillna(method='ffill', inplace=True)
        df['balance'].fillna(method='ffill', inplace=True)

        # Zorg dat we een datetime kolom hebben
        if 'time' in df.columns:
            df['date'] = pd.to_datetime(df['time'])
        elif 'date' in df.columns and isinstance(df['date'].iloc[0], str):
            df['date'] = pd.to_datetime(df['date'])

        # Resample naar dagelijkse data
        df.set_index('date', inplace=True)
        daily_df = df.resample('D').last()

        # Reset index
        daily_df.reset_index(inplace=True)
        return daily_df

    def _calculate_performance_metrics(self, trades: List[Dict], account_data: pd.DataFrame,
                                       initial_balance: float, start_date: datetime,
                                       end_date: datetime) -> Dict[str, Any]:
        """
        Bereken performancemetrics.

        Parameters:
        -----------
        trades : List[Dict]
            Lijst met afgesloten trades
        account_data : pd.DataFrame
            Account data per dag
        initial_balance : float
            Initiële balans
        start_date : datetime
            Start datum van backtest
        end_date : datetime
            Eind datum van backtest

        Returns:
        --------
        Dict[str, Any] : Performancemetrics
        """
        metrics = {}

        # Basis trade metrics
        metrics['total_trades'] = len(trades)

        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'net_profit': 0,
                'net_profit_pct': 0,
                'max_drawdown': 0,
                'max_drawdown_pct': 0,
                'sharpe_ratio': 0,
                'avg_trade': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'largest_win': 0,
                'largest_loss': 0,
                'max_consecutive_wins': 0,
                'max_consecutive_losses': 0,
                'total_trading_days': 0,
                'success': False
            }

        # Win/loss metrics
        winning_trades = [t for t in trades if t['profit'] > 0]
        losing_trades = [t for t in trades if t['profit'] <= 0]

        metrics['winning_trades'] = len(winning_trades)
        metrics['losing_trades'] = len(losing_trades)
        metrics['win_rate'] = (metrics['winning_trades'] / metrics['total_trades']) * 100 if metrics[
                                                                                                 'total_trades'] > 0 else 0

        # Profit metrics
        total_profit = sum(t['profit'] for t in winning_trades)
        total_loss = sum(t['profit'] for t in losing_trades)

        metrics['gross_profit'] = total_profit
        metrics['gross_loss'] = total_loss
        metrics['net_profit'] = total_profit + total_loss
        metrics['net_profit_pct'] = (metrics['net_profit'] / initial_balance) * 100
        metrics['profit_factor'] = abs(total_profit / total_loss) if total_loss < 0 else float('inf')

        # Gemiddeldes
        metrics['avg_trade'] = metrics['net_profit'] / metrics['total_trades'] if metrics['total_trades'] > 0 else 0
        metrics['avg_win'] = total_profit / metrics['winning_trades'] if metrics['winning_trades'] > 0 else 0
        metrics['avg_loss'] = total_loss / metrics['losing_trades'] if metrics['losing_trades'] > 0 else 0

        # Drawdown berekening
        if not account_data.empty and 'equity' in account_data.columns:
            equity = account_data['equity'].values
            peak = np.maximum.accumulate(equity)
            drawdown = equity - peak
            max_drawdown_idx = np.argmin(drawdown)

            metrics['max_drawdown'] = abs(drawdown[max_drawdown_idx])
            metrics['max_drawdown_pct'] = (metrics['max_drawdown'] / peak[max_drawdown_idx]) * 100

            # Bereken drawdown duur
            if max_drawdown_idx > 0:
                # Vind begin van huidige drawdown periode
                i = max_drawdown_idx
                while i > 0 and equity[i - 1] != peak[max_drawdown_idx]:
                    i -= 1

                drawdown_start = i

                # Vind einde van huidige drawdown periode
                i = max_drawdown_idx
                while i < len(equity) - 1 and equity[i + 1] < peak[max_drawdown_idx]:
                    i += 1

                drawdown_end = i

                metrics['max_drawdown_duration'] = drawdown_end - drawdown_start
            else:
                metrics['max_drawdown_duration'] = 0
        else:
            metrics['max_drawdown'] = 0
            metrics['max_drawdown_pct'] = 0
            metrics['max_drawdown_duration'] = 0

        # Berekenen Sharpe ratio (als we dagelijkse returns hebben)
        if not account_data.empty and 'equity' in account_data.columns:
            equity = account_data['equity'].values
            daily_returns = np.diff(equity) / equity[:-1]

            if len(daily_returns) > 0:
                avg_return = np.mean(daily_returns)
                std_return = np.std(daily_returns)

                if std_return > 0:
                    # Annualiseer Sharpe (252 trading dagen per jaar)
                    annual_factor = np.sqrt(252)
                    metrics['sharpe_ratio'] = (avg_return / std_return) * annual_factor
                else:
                    metrics['sharpe_ratio'] = 0
            else:
                metrics['sharpe_ratio'] = 0
        else:
            metrics['sharpe_ratio'] = 0

        # Berekenen trading statistieken
        metrics['largest_win'] = max([t['profit'] for t in winning_trades]) if winning_trades else 0
        metrics['largest_loss'] = min([t['profit'] for t in losing_trades]) if losing_trades else 0

        # Consecutive win/loss streaks
        profit_series = [1 if t['profit'] > 0 else 0 for t in trades]

        if profit_series:
            # Win streaks
            win_streaks = []
            current_streak = 0

            for p in profit_series:
                if p == 1:
                    current_streak += 1
                else:
                    if current_streak > 0:
                        win_streaks.append(current_streak)
                    current_streak = 0

            if current_streak > 0:
                win_streaks.append(current_streak)

            # Loss streaks
            loss_streaks = []
            current_streak = 0

            for p in profit_series:
                if p == 0:
                    current_streak += 1
                else:
                    if current_streak > 0:
                        loss_streaks.append(current_streak)
                    current_streak = 0

            if current_streak > 0:
                loss_streaks.append(current_streak)

            metrics['max_consecutive_wins'] = max(win_streaks) if win_streaks else 0
            metrics['max_consecutive_losses'] = max(loss_streaks) if loss_streaks else 0
        else:
            metrics['max_consecutive_wins'] = 0
            metrics['max_consecutive_losses'] = 0

        # Trading dagen
        if not account_data.empty and 'date' in account_data.columns:
            metrics['total_trading_days'] = account_data['date'].nunique()
        else:
            # Bereken uit trades
            trade_dates = set()
            for trade in trades:
                if 'entry_time' in trade and isinstance(trade['entry_time'], datetime):
                    trade_dates.add(trade['entry_time'].date())
                elif 'exit_time' in trade and isinstance(trade['exit_time'], datetime):
                    trade_dates.add(trade['exit_time'].date())

            metrics['total_trading_days'] = len(trade_dates)

        metrics['success'] = True
        return metrics

    def _check_ftmo_compliance(self, account_data: pd.DataFrame, initial_balance: float,
                               metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Controleer of de handelsresultaten voldoen aan FTMO-regels.

        Parameters:
        -----------
        account_data : pd.DataFrame
            Account data per dag
        initial_balance : float
            Initiële balans
        metrics : Dict[str, Any]
            Prestatiestatistieken

        Returns:
        --------
        Dict[str, Any] : FTMO compliance resultaten
        """
        # Initialiseer FTMO validator
        ftmo_validator = FTMOValidator(self.config, self.logger.log_file)

        # FTMO regels
        profit_target = 10  # 10% winstdoel
        max_daily_loss = 5  # 5% max dagelijkse drawdown
        max_total_drawdown = 10  # 10% maximale totale drawdown
        min_trading_days = 4  # Minimaal 4 handelsdagen

        # Controle op dagelijkse limiet
        daily_drawdown_compliant = True
        daily_drawdown_violations = []

        if not account_data.empty and 'equity' in account_data.columns and 'date' in account_data.columns:
            # Bereken dagelijkse balans veranderingen
            account_data = account_data.copy()
            account_data['prev_equity'] = account_data['equity'].shift(1).fillna(initial_balance)
            account_data['daily_change_pct'] = (account_data['equity'] - account_data['prev_equity']) / account_data[
                'prev_equity'] * 100

            # Controleer dagelijkse limieten
            violations = account_data[account_data['daily_change_pct'] < -max_daily_loss]

            if not violations.empty:
                daily_drawdown_compliant = False

                for _, row in violations.iterrows():
                    daily_drawdown_violations.append({
                        'date': row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], datetime) else row['date'],
                        'change_pct': row['daily_change_pct'],
                        'equity': row['equity']
                    })

        # Evalueer alle regels
        profit_target_met = metrics['net_profit_pct'] >= profit_target
        total_drawdown_compliant = metrics['max_drawdown_pct'] <= max_total_drawdown
        trading_days_compliant = metrics['total_trading_days'] >= min_trading_days

        # Overall compliance
        is_compliant = (
                profit_target_met and
                daily_drawdown_compliant and
                total_drawdown_compliant and
                trading_days_compliant
        )

        # Bepaal reden van non-compliance
        reasons = []

        if not profit_target_met:
            reasons.append(f"Winstdoel niet bereikt: {metrics['net_profit_pct']:.2f}% (doel: {profit_target}%)")

        if not daily_drawdown_compliant:
            reasons.append(f"Dagelijkse drawdown limiet overschreden ({len(daily_drawdown_violations)} keer)")

        if not total_drawdown_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {metrics['max_drawdown_pct']:.2f}% (limiet: {max_total_drawdown}%)")

        if not trading_days_compliant:
            reasons.append(f"Onvoldoende handelsdagen: {metrics['total_trading_days']} (min: {min_trading_days})")

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO regels"

        # Maak FTMO rapport
        ftmo_report_path = None
        try:
            ftmo_report_path = ftmo_validator.plot_ftmo_compliance(initial_balance)
        except Exception as e:
            self.logger.log_info(f"Kon FTMO compliance plot niet maken: {str(e)}", level="ERROR")

        return {
            'compliant': is_compliant,
            'reason': reason,
            'profit_target_met': profit_target_met,
            'daily_drawdown_compliant': daily_drawdown_compliant,
            'total_drawdown_compliant': total_drawdown_compliant,
            'trading_days_compliant': trading_days_compliant,
            'daily_drawdown_violations': daily_drawdown_violations,
            'report_path': ftmo_report_path
        }

    def _plot_equity_curve(self, account_data: pd.DataFrame, initial_balance: float,
                           metrics: Dict[str, Any]) -> str:
        """
        Plot equity curve en opslag als bestand.

        Parameters:
        -----------
        account_data : pd.DataFrame
            Account data per dag
        initial_balance : float
            Initiële balans
        metrics : Dict[str, Any]
            Prestatiestatistieken

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if account_data.empty or 'equity' not in account_data.columns:
            self.logger.log_info("Onvoldoende data voor equity curve", level="ERROR")
            return ""

        # Maak plot
        fig, ax = plt.subplots(figsize=(16, 10))

        # Plot equity curve
        ax.plot(account_data['date'], account_data['equity'], label='Equity', color='blue', linewidth=2)

        if 'balance' in account_data.columns:
            ax.plot(account_data['date'], account_data['balance'], label='Balance', color='green', linewidth=2)

        # Voeg horizontale lijnen toe voor targets
        ax.axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')
        ax.axhline(y=initial_balance * 1.10, color='green', linestyle='--', label='+10% (Target)')
        ax.axhline(y=initial_balance * 0.95, color='orange', linestyle='--', label='-5% (Daily Limit)')
        ax.axhline(y=initial_balance * 0.90, color='red', linestyle='--', label='-10% (Max Drawdown)')

        # Formateer plot
        ax.set_title('Equity Curve & Balance History', fontsize=16)
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel('Account Value', fontsize=14)
        ax.legend(loc='best', fontsize=12)
        ax.grid(True)

        # Voeg stats toe
        stats_text = (
            f"Net Profit: ${metrics['net_profit']:.2f} ({metrics['net_profit_pct']:.2f}%)\n"
            f"Total Trades: {metrics['total_trades']}\n"
            f"Win Rate: {metrics['win_rate']:.2f}%\n"
            f"Profit Factor: {metrics['profit_factor']:.2f}\n"
            f"Max Drawdown: ${metrics['max_drawdown']:.2f} ({metrics['max_drawdown_pct']:.2f}%)\n"
            f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}"
        )

        # Plaats tekst rechtsonder
        ax.text(0.97, 0.03, stats_text, transform=ax.transAxes, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7), va='bottom', ha='right')

        # Format x-as
        fig.autofmt_xdate()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _plot_drawdown_curve(self, account_data: pd.DataFrame) -> str:
        """
        Plot drawdown curve en opslag als bestand.

        Parameters:
        -----------
        account_data : pd.DataFrame
            Account data per dag

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if account_data.empty or 'equity' not in account_data.columns:
            return ""

        # Bereken drawdown
        equity = account_data['equity'].values
        peak = np.maximum.accumulate(equity)
        drawdown_pct = ((equity - peak) / peak) * 100

        # Maak plot
        fig, ax = plt.subplots(figsize=(16, 6))

        # Plot drawdown
        ax.fill_between(account_data['date'], drawdown_pct, 0,
                        where=(drawdown_pct < 0), color='red', alpha=0.3)
        ax.plot(account_data['date'], drawdown_pct, 'r-', linewidth=1)

        # Voeg limieten toe
        ax.axhline(y=-5, color='orange', linestyle='--', label='-5% (Daily Limit)')
        ax.axhline(y=-10, color='red', linestyle='--', label='-10% (Max Drawdown)')

        # Formateer plot
        ax.set_title('Drawdown (%)', fontsize=16)
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel('Drawdown (%)', fontsize=14)
        ax.legend()
        ax.grid(True)

        # Begrens y-as
        min_dd = min(drawdown_pct) * 1.1  # 10% marge
        ax.set_ylim(min(min_dd, -12), 1)  # Minimaal -12% tonen

        # Format x-as
        fig.autofmt_xdate()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"drawdown_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _plot_monthly_returns(self, account_data: pd.DataFrame) -> str:
        """
        Plot maandelijkse returns als heatmap.

        Parameters:
        -----------
        account_data : pd.DataFrame
            Account data per dag

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if account_data.empty or 'equity' not in account_data.columns or 'date' not in account_data.columns:
            return ""

        # Converteer dates indien nodig
        if not pd.api.types.is_datetime64_dtype(account_data['date']):
            account_data['date'] = pd.to_datetime(account_data['date'])

        # Voeg maand en jaar kolommen toe
        account_data['year'] = account_data['date'].dt.year
        account_data['month'] = account_data['date'].dt.month

        # Maak maandelijkse returns tabel
        monthly_returns = []

        for (year, month), group in account_data.groupby(['year', 'month']):
            start_equity = group['equity'].iloc[0]
            end_equity = group['equity'].iloc[-1]
            monthly_return = ((end_equity / start_equity) - 1) * 100

            monthly_returns.append({
                'year': year,
                'month': month,
                'return': monthly_return
            })

        if not monthly_returns:
            return ""

        # Converteer naar DataFrame
        returns_df = pd.DataFrame(monthly_returns)

        # Pivot voor heatmap
        pivot_returns = returns_df.pivot(index='year', columns='month', values='return')

        # Maak plot
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot heatmap
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Gebruik divergerend kleurenschema (rood voor negatief, groen voor positief)
        cmap = plt.cm.RdYlGn

        im = ax.imshow(pivot_returns, cmap=cmap, aspect='auto')

        # Voeg colorbar toe
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Return (%)')

        # Configureer assen
        ax.set_title('Monthly Returns (%)', fontsize=16)
        ax.set_xticks(np.arange(len(months)))
        ax.set_xticklabels(months)
        ax.set_yticks(np.arange(len(pivot_returns.index)))
        ax.set_yticklabels(pivot_returns.index)

        # Voeg return waarden toe in cellen
        for i in range(len(pivot_returns.index)):
            for j in range(len(months)):
                if j < pivot_returns.shape[1]:
                    value = pivot_returns.iloc[i, j]
                    if not pd.isna(value):
                        text_color = 'black' if abs(value) < 10 else 'white'
                        ax.text(j, i, f"{value:.1f}%", ha="center", va="center", color=text_color)

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"monthly_returns_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _plot_trade_analysis(self, trades: List[Dict]) -> str:
        """
        Plot handelsanalyse.

        Parameters:
        -----------
        trades : List[Dict]
            Lijst met afgesloten trades

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if not trades:
            return ""

        # Extraheer symbolen
        symbols = list(set(t['symbol'] for t in trades if 'symbol' in t))

        # Maak 2x2 subplots
        fig, axs = plt.subplots(2, 2, figsize=(16, 14))

        # 1. Profit/Loss distributie histogram
        profits = [t['profit'] for t in trades]
        axs[0, 0].hist(profits, bins=20, color=['green' if p > 0 else 'red' for p in profits])
        axs[0, 0].set_title('Profit/Loss Distribution', fontsize=14)
        axs[0, 0].set_xlabel('Profit/Loss ($)', fontsize=12)
        axs[0, 0].set_ylabel('Count', fontsize=12)
        axs[0, 0].grid(True)

        # 2. Wins/Losses per symbool
        symbol_results = {}
        for symbol in symbols:
            symbol_trades = [t for t in trades if t['symbol'] == symbol]
            wins = len([t for t in symbol_trades if t['profit'] > 0])
            losses = len([t for t in symbol_trades if t['profit'] <= 0])
            symbol_results[symbol] = {'wins': wins, 'losses': losses}

        if symbol_results:
            symbols_sorted = sorted(symbol_results.keys())
            wins = [symbol_results[s]['wins'] for s in symbols_sorted]
            losses = [symbol_results[s]['losses'] for s in symbols_sorted]

            x = np.arange(len(symbols_sorted))
            width = 0.35

            axs[0, 1].bar(x - width / 2, wins, width, label='Wins', color='green')
            axs[0, 1].bar(x + width / 2, losses, width, label='Losses', color='red')

            axs[0, 1].set_title('Wins/Losses by Symbol', fontsize=14)
            axs[0, 1].set_xticks(x)
            axs[0, 1].set_xticklabels(symbols_sorted, rotation=45, ha='right')
            axs[0, 1].set_ylabel('Count', fontsize=12)
            axs[0, 1].legend()
            axs[0, 1].grid(True)

        # 3. Profit/Loss per symbool (boxplot)
        symbol_profits = {}
        for symbol in symbols:
            symbol_profits[symbol] = [t['profit'] for t in trades if t['symbol'] == symbol]

        if symbol_profits:
            boxplot_data = [symbol_profits[s] for s in symbols_sorted]
            axs[1, 0].boxplot(boxplot_data, labels=symbols_sorted)
            axs[1, 0].set_title('P/L Distribution by Symbol', fontsize=14)
            axs[1, 0].set_ylabel('Profit/Loss ($)', fontsize=12)
            axs[1, 0].set_xticklabels(symbols_sorted, rotation=45, ha='right')
            axs[1, 0].grid(True)

        # 4. Cumulatieve P/L curve
        if 'entry_time' in trades[0]:
            # Sort trades by entry time
            sorted_trades = sorted(trades, key=lambda x: x['entry_time'])
            cumulative_profit = np.cumsum([t['profit'] for t in sorted_trades])

            entry_times = [t['entry_time'] for t in sorted_trades]

            axs[1, 1].plot(entry_times, cumulative_profit, 'b-', linewidth=2)
            axs[1, 1].set_title('Cumulative P/L', fontsize=14)
            axs[1, 1].set_xlabel('Date', fontsize=12)
            axs[1, 1].set_ylabel('Cumulative P/L ($)', fontsize=12)
            axs[1, 1].grid(True)

            fig.autofmt_xdate()

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_analysis_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _plot_optimization_results(self, results: List[Dict], param_keys: List[str], metric: str) -> str:
        """
        Plot optimalisatieresultaten.

        Parameters:
        -----------
        results : List[Dict]
            Lijst met optimalisatieresultaten
        param_keys : List[str]
            Lijst met parameter namen
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        # Filter geldige resultaten
        valid_results = [r for r in results if r['success']]

        if not valid_results:
            return ""

        # Maak plot gebaseerd op aantal parameters
        n_params = len(param_keys)

        if n_params == 1:
            # 1D plot (parameter vs metric)
            param = param_keys[0]
            fig, ax = plt.subplots(figsize=(12, 8))

            # Extraheer data
            x_values = [r['parameters'][param] for r in valid_results]
            y_values = [r['metrics'].get(metric, 0) for r in valid_results]

            # Plot
            ax.plot(x_values, y_values, 'o-', linewidth=2)
            ax.set_title(f'Optimization Results: {param} vs {metric}', fontsize=16)
            ax.set_xlabel(param, fontsize=14)
            ax.set_ylabel(metric, fontsize=14)
            ax.grid(True)

        elif n_params == 2:
            # 2D heatmap plot
            param1, param2 = param_keys
            fig, ax = plt.subplots(figsize=(12, 10))

            # Verzamel unieke parameterwaarden
            param1_values = sorted(list(set(r['parameters'][param1] for r in valid_results)))
            param2_values = sorted(list(set(r['parameters'][param2] for r in valid_results)))

            # Maak data matrix
            data = np.zeros((len(param1_values), len(param2_values)))
            data.fill(np.nan)

            for r in valid_results:
                i = param1_values.index(r['parameters'][param1])
                j = param2_values.index(r['parameters'][param2])
                data[i, j] = r['metrics'].get(metric, 0)

            # Plot heatmap
            im = ax.imshow(data, cmap='viridis')

            # Configureer assen
            ax.set_xticks(np.arange(len(param2_values)))
            ax.set_yticks(np.arange(len(param1_values)))
            ax.set_xticklabels(param2_values)
            ax.set_yticklabels(param1_values)

            ax.set_xlabel(param2, fontsize=14)
            ax.set_ylabel(param1, fontsize=14)
            ax.set_title(f'Optimization Results: {param1} vs {param2} (color={metric})', fontsize=16)

            # Voeg colorbar toe
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label(metric)

            # Voeg waarden toe in cellen
            for i in range(len(param1_values)):
                for j in range(len(param2_values)):
                    if not np.isnan(data[i, j]):
                        text_color = 'white' if data[i, j] > np.nanmean(data) else 'black'
                        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color=text_color)

        else:
            # Parallelle coördinatenplot voor meer dan 2 parameters
            fig, ax = plt.subplots(figsize=(14, 8))

            # Extraheer data
            param_values = {param: [] for param in param_keys}
            metric_values = []

            for r in valid_results:
                for param in param_keys:
                    param_values[param].append(r['parameters'][param])
                metric_values.append(r['metrics'].get(metric, 0))

            # Normaliseer waarden voor plot
            normalized_data = {}
            for param in param_keys:
                values = np.array(param_values[param])
                if len(np.unique(values)) > 1:
                    normalized_data[param] = (values - np.min(values)) / (np.max(values) - np.min(values))
                else:
                    normalized_data[param] = np.zeros_like(values)

            # Normaliseer metric
            metric_array = np.array(metric_values)
            if len(np.unique(metric_array)) > 1:
                normalized_metric = (metric_array - np.min(metric_array)) / (
                        np.max(metric_array) - np.min(metric_array))
            else:
                normalized_metric = np.zeros_like(metric_array)

            # Maak kleurschemam gebaseerd op metric
            colors = plt.cm.viridis(normalized_metric)

            # Teken parallelle lijnen
            x = np.arange(len(param_keys))

            for i, result_idx in enumerate(range(len(valid_results))):
                y = [normalized_data[param][result_idx] for param in param_keys]
                ax.plot(x, y, color=colors[i], alpha=0.5)

            # Configureer assen
            ax.set_xticks(x)
            ax.set_xticklabels(param_keys, rotation=45)
            ax.set_title(f'Parameter Combinations vs {metric}', fontsize=16)
            ax.set_ylim(0, 1)
            ax.grid(True)

            # Voeg colorbar toe
            sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
                                       norm=plt.Normalize(vmin=min(metric_values), vmax=max(metric_values)))
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax)
            cbar.set_label(metric)

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"optimization_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _save_backtest_results(self, strategy_name: str, symbols: List[str],
                               metrics: Dict[str, Any], trades: List[Dict],
                               account_data: pd.DataFrame, parameters: Dict[str, Any]) -> str:
        """
        Sla backtestresultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metrics : Dict[str, Any]
            Prestatiestatistieken
        trades : List[Dict]
            Lijst met afgesloten trades
        account_data : pd.DataFrame
            Account data per dag
        parameters : Dict[str, Any]
            Strategie parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        results = {
            'strategy': strategy_name,
            'symbols': symbols,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'parameters': parameters,
            'metrics': metrics,
            'trades': [
                {k: str(v) if isinstance(v, datetime) else v for k, v in t.items()}
                for t in trades
            ],
            'account_data': account_data.to_dict(orient='records') if not account_data.empty else []
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"backtest_results_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.log_info(f"Backtest resultaten opgeslagen als {output_path}")
        return output_path

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, results: List[Dict], best_result: Dict) -> str:
        """
        Sla optimalisatieresultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        results : List[Dict]
            Lijst met optimalisatieresultaten
        best_result : Dict
            Beste resultaat

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        optimization_results = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'best_parameters': best_result['parameters'],
            'best_metrics': best_result['metrics'],
            'all_results': [
                {
                    'parameters': r['parameters'],
                    'metrics': r['metrics'] if r['success'] else {},
                    'success': r['success']
                }
                for r in results
            ]
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"optimization_results_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(optimization_results, f, indent=2, default=str)

        self.logger.log_info(f"Optimalisatie resultaten opgeslagen als {output_path}")
        return output_path


def run_advanced_backtest():
    """Voer een geavanceerde backtest uit met configuratie en analyse."""
    print("Geavanceerde Backtester module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/backtest_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Advanced Backtest Started ======")

    # Initialiseer backtester
    backtester = Backtester(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Start backtest
    results = backtester.run_backtest(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        plot_results=True
    )

    if results['success']:
        metrics = results['metrics']
        logger.log_info(
            f"Backtest voltooid. Totale winst: {metrics['net_profit']:.2f} ({metrics['net_profit_pct']:.2f}%)")
        logger.log_info(f"Win Rate: {metrics['win_rate']:.2f}%, Max Drawdown: {metrics['max_drawdown_pct']:.2f}%")
        logger.log_info(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

        # FTMO Compliance rapport
        if 'ftmo_compliance' in metrics:
            compliance = metrics['ftmo_compliance']
            if compliance['compliant']:
                logger.log_info("FTMO Compliance: GESLAAGD ✅")
            else:
                logger.log_info(f"FTMO Compliance: GEFAALD ❌ - {compliance['reason']}")
    else:
        logger.log_info(f"Backtest mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Advanced Backtest Ended ======")


def run_parameter_optimization():
    """Voer parameter optimalisatie uit."""
    print("Parameter Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/optimization_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Parameter Optimalisatie Started ======")

    # Initialiseer backtester
    backtester = Backtester(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter ranges voor turtle strategy
    param_ranges = {
        'entry_period': [20, 40, 60],
        'exit_period': [10, 20, 30],
        'atr_period': [14, 20, 30],
        'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
        'swing_mode': [True, False]
    }

    # Start optimalisatie
    results = backtester.run_optimization(
        strategy_name=strategy_name,
        symbols=symbols,
        param_ranges=param_ranges,
        start_date=(datetime.now() - timedelta(days=365 * 2)).strftime('%Y-%m-%d'),
        end_date=datetime.now().strftime('%Y-%m-%d'),
        metric='sharpe_ratio'
    )

    if results['success']:
        best_params = results['best_parameters']
        best_metrics = results['best_metrics']

        logger.log_info("Optimalisatie voltooid")
        logger.log_info(f"Beste parameters gevonden: {best_params}")
        logger.log_info(f"Met metrieken: Sharpe Ratio: {best_metrics.get('sharpe_ratio', 0):.2f}, "
                        f"Net Profit: {best_metrics.get('net_profit_pct', 0):.2f}%, "
                        f"Win Rate: {best_metrics.get('win_rate', 0):.2f}%")
    else:
        logger.log_info(f"Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Parameter Optimalisatie Ended ======")


if __name__ == "__main__":
    run_advanced_backtest()
