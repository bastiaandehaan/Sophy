import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


class DummyConnector:
    """Dummy connector voor backtest doeleinden met geavanceerde datahandling."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def get_historical_data(self, symbol: str, timeframe_str: str, bars_count: int) -> pd.DataFrame:
        """Haal historische data op uit CSV bestanden met caching."""
        cache_key = f"{symbol}_{timeframe_str}"
        if cache_key in self.data_cache:
            df = self.data_cache[cache_key]
            return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

        filename = f"{symbol}_{timeframe_str}.csv"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Bestand niet gevonden: {filepath}")
            return pd.DataFrame()

        df = pd.read_csv(filepath)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif 'time' in df.columns:
            df['date'] = pd.to_datetime(df['time'])
            df.drop('time', axis=1, inplace=True)

        df.columns = [col.lower() for col in df.columns]
        required_cols = {'open', 'high', 'low', 'close', 'tick_volume'}
        if not all(col in df.columns for col in required_cols):
            print(f"Ongeldige data voor {symbol}: ontbrekende kolommen")
            return pd.DataFrame()

        self.data_cache[cache_key] = df
        return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """Simuleer huidige tick gebaseerd op laatste data."""
        cache_key = f"{symbol}_H4"
        if cache_key not in self.data_cache:
            self.get_historical_data(symbol, "H4", 1000)

        if cache_key not in self.data_cache:
            return None

        df = self.data_cache[cache_key]
        last_row = df.iloc[-1]

        class Tick:
            pass

        tick = Tick()
        tick.ask = last_row['close']
        tick.bid = last_row['close'] * 0.999  # Simpele bid/ask spread
        tick.time = last_row['date'].timestamp()
        return tick

    def get_account_info(self) -> Dict[str, Any]:
        """Geef geüpdatete accountinformatie tijdens backtest."""
        return {
            'balance': 100000,
            'equity': 100000,
            'margin': 0,
            'free_margin': 100000,
            'margin_level': 0,
            'profit': 0
        }

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Geef open posities terug."""
        return [pos for pos in self.open_positions.values()] if symbol is None else \
            [pos for pos in self.open_positions.values() if pos.get('symbol') == symbol]

    def place_order(self, action: str, symbol: str, volume: float, stop_loss: float, take_profit: float,
                    comment: str) -> Optional[int]:
        """Simuleer het plaatsen van een order."""
        if action not in ['BUY', 'SELL']:
            return None
        ticket = len(self.open_positions) + 1
        self.open_positions[ticket] = {
            'ticket': ticket,
            'symbol': symbol,
            'type': mt5.POSITION_TYPE_BUY if action == 'BUY' else mt5.POSITION_TYPE_SELL,
            'volume': volume,
            'price_open': self.get_symbol_tick(symbol).ask if action == 'BUY' else self.get_symbol_tick(symbol).bid,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'time': datetime.now().timestamp(),
            'profit': 0.0
        }
        return ticket

    def modify_position(self, ticket: int, stop_loss: float, take_profit: float) -> bool:
        """Simuleer het aanpassen van een positie."""
        if ticket in self.open_positions:
            self.open_positions[ticket]['stop_loss'] = stop_loss
            self.open_positions[ticket]['take_profit'] = take_profit
            return True
        return False

    open_positions = {}


class BacktestStrategy:
    """Wrapper voor strategie tijdens backtesting met geavanceerde logica."""

    def __init__(self, strategy, initial_balance: float = 100000):
        self.strategy = strategy
        self.balance = initial_balance
        self.equity = initial_balance
        self.positions: Dict[int, Dict] = {}
        self.trades: List[Dict] = []
        self.logger = self.strategy.logger  # Gebruik de logger van de strategie

    def process_candle(self, symbol: str, candle: Dict[str, Any]) -> Dict[str, Any]:
        """Verwerk een enkele candle en simuleer trades."""
        result = {'signal': None, 'action': None}
        candle_df = pd.DataFrame([candle])
        indicators = self.strategy.calculate_indicators(candle_df)

        # Simuleer tick-gebaseerde data
        tick = self.strategy.connector.get_symbol_tick(symbol)
        if tick is None:
            return result

        process_result = self.strategy.process_symbol(symbol)
        if process_result.get('signal') == 'ENTRY' and process_result.get('action'):
            action = process_result['action']
            volume = process_result.get('volume', 0.1)
            stop_loss = process_result.get('stop_loss', 0)
            ticket = self.strategy.connector.place_order(action, symbol, volume, stop_loss, 0, "Backtest Trade")
            if ticket:
                self.positions[ticket] = {
                    'symbol': symbol,
                    'action': action,
                    'volume': volume,
                    'entry_price': tick.ask if action == 'BUY' else tick.bid,
                    'stop_loss': stop_loss,
                    'open_time': datetime.fromtimestamp(tick.time)
                }
                self.logger.log_trade(symbol, action, tick.ask, volume, stop_loss, 0, "Backtest Entry")
                result.update(process_result)

        # Beheer open posities
        for ticket, pos in list(self.positions.items()):
            current_price = tick.ask if pos['action'] == 'BUY' else tick.bid
            profit = (current_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            pos['profit'] = profit
            self.equity = self.balance + sum(p['profit'] for p in self.positions.values())

            # Simuleer stop loss
            if (pos['action'] == 'BUY' and current_price <= pos['stop_loss']) or \
                    (pos['action'] == 'SELL' and current_price >= pos['stop_loss']):
                self.close_position(ticket, current_price)
                result['signal'] = 'EXIT'
                result['action'] = 'CLOSE'

        return result

    def close_position(self, ticket: int, close_price: float):
        """Sluit een positie en update balans."""
        if ticket in self.positions:
            pos = self.positions[ticket]
            profit = (close_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            self.balance += profit
            self.trades.append({
                'symbol': pos['symbol'],
                'action': pos['action'],
                'entry_price': pos['entry_price'],
                'exit_price': close_price,
                'volume': pos['volume'],
                'profit': profit,
                'open_time': pos['open_time'],
                'close_time': datetime.now()
            })
            self.logger.log_trade(pos['symbol'], 'SELL' if pos['action'] == 'BUY' else 'BUY', close_price,
                                  pos['volume'], 0, 0, f"Backtest Exit, Profit: {profit:.2f}")
            del self.positions[ticket]


def run_backtest():
    """Voer een geavanceerde backtest uit met configuratie en analyse."""
    print("Backtester module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/backtest_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Backtest Started ======")

    # Haal symbols en timeframe op
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    start_date = config.get('backtest', {}).get('start_date',
                                                (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date = config.get('backtest', {}).get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Setup dummy connector
    data_dir = config.get('data_dir', 'data')
    connector = DummyConnector(data_dir)
    connector.open_positions = {}  # Initialiseer open posities

    # Laad data
    data = {}
    for symbol in symbols:
        df = connector.get_historical_data(symbol, timeframe, 10000)
        if not df.empty:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            data[symbol] = df
            logger.log_info(
                f"Geladen: {symbol} {timeframe} - {len(df)} candles van {df['date'].min()} tot {df['date'].max()}")
        else:
            logger.log_info(f"Kon geen data laden voor {symbol} {timeframe}", level="ERROR")
            continue

    if not data:
        logger.log_info("Geen data geladen, backtest gestopt", level="ERROR")
        return

    # Maak strategie aan
    strategy_name = config['strategy'].get('name', 'turtle')
    strategy = StrategyFactory.create_strategy(strategy_name, connector, None, logger, config)
    if not strategy:
        logger.log_info(f"Kon strategie {strategy_name} niet aanmaken", level="ERROR")
        return

    backtest = BacktestStrategy(strategy)
    equity_curve = []

    # Voer backtest uit
    for symbol, df in data.items():
        for _, candle in df.iterrows():
            candle_dict = candle.to_dict()
            result = backtest.process_candle(symbol, candle_dict)
            equity_curve.append(backtest.equity)

            # Log status
            account_info = connector.get_account_info()
            account_info['equity'] = backtest.equity
            account_info['balance'] = backtest.balance
            logger.log_status(account_info, connector.get_open_positions())

    # Analyseer resultaten
    total_profit = backtest.balance - 100000
    trades = len(backtest.trades)
    winning_trades = sum(1 for t in backtest.trades if t['profit'] > 0)
    win_rate = (winning_trades / trades * 100) if trades > 0 else 0
    avg_profit = np.mean([t['profit'] for t in backtest.trades if t['profit'] > 0]) if winning_trades > 0 else 0
    avg_loss = np.mean([t['profit'] for t in backtest.trades if t['profit'] < 0]) if len(
        [t for t in backtest.trades if t['profit'] < 0]) > 0 else 0
    drawdown = min(0, min(equity_curve) - 100000) if equity_curve else 0

    logger.log_performance_metrics({
        'total_trades': trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'total_profit': total_profit,
        'max_drawdown': drawdown,
        'trade_history': backtest.trades
    })

    # Visualiseer resultaten
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label='Equity Curve')
    plt.title(f'Backtest Resultaten - {strategy_name}')
    plt.xlabel('Candles')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(log_file), 'backtest_equity_curve.png'))
    plt.close()

    logger.log_info(
        f"Backtest voltooid. Totale winst: {total_profit:.2f}, Win Rate: {win_rate:.2f}%, Max Drawdown: {drawdown:.2f}")
    logger.log_info("====== Sophy Backtest Ended ======")


if __name__ == "__main__":
    run_backtest()
