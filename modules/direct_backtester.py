import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import os
import sys

# Projectpad toevoegen voor imports
sys.path.append(os.path.abspath('..'))

# Importeer TurtleTrader modules (toegevoegd TurtleStrategy import)
from modules.strategy import TurtleStrategy
from modules.risk_manager import RiskManager
from utils.logger import Logger

# Importeer TurtleTrader modules (duplicaat verwijderd, maar laten staan zoals origineel)
from modules.strategy import TurtleStrategy
from modules.risk_manager import RiskManager
from utils.logger import Logger

# Voeg het projectpad toe aan sys.path om imports te laten werken
sys.path.append(os.path.abspath('..'))

class DirectBacktester:
    """
    Klasse voor directe backtesting van de TurtleTrader strategie
    Gebruikt de werkelijke strategie-code in plaats van een herimplementatie
    """

    def __init__(self, historical_data, symbol, config, output_dir='backtest_results'):
        """
        Initialiseer de backtest

        Parameters:
        -----------
        historical_data : pandas.DataFrame
            DataFrame met historische prijsgegevens
        symbol : str
            Het te testen symbool
        config : dict
            Strategie configuratie
        output_dir : str, optional
            Map voor het opslaan van resultaten
        """
        self.data = historical_data.copy()
        self.symbol = symbol
        self.config = config
        self.output_dir = output_dir

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

    def run_backtest(self, strategy_class=TurtleStrategy, risk_per_trade=0.01,
                     initial_balance=100000, max_daily_drawdown=0.05):
        """
        Voer backtest uit met de opgegeven strategie

        Parameters:
        -----------
        strategy_class : class
            De strategie-class om te testen (bijv. TurtleStrategy of EnhancedTurtleStrategy)
        risk_per_trade : float
            Risico per trade als percentage van account
        initial_balance : float
            Initieel account saldo
        max_daily_drawdown : float
            Maximale dagelijkse drawdown als percentage

        Returns:
        --------
        tuple
            (results_df, trade_stats, equity_curve)
        """
        print(f"Starting backtest with {strategy_class.__name__}")
        print(f"Period: {self.data['time'].iloc[0]} to {self.data['time'].iloc[-1]}")
        print(f"Risk per trade: {risk_per_trade * 100}%")
        print(f"Initial balance: ${initial_balance:,.2f}")

        # Maak mock implementaties van benodigde componenten
        mock_connector = self._create_mock_connector()

        # Maak een aangepaste RiskManager
        risk_manager = RiskManager(
            max_risk_per_trade=risk_per_trade,
            max_daily_drawdown=max_daily_drawdown,
            max_total_drawdown=max_daily_drawdown * 2
        )

        # Maak een aangepaste logger die trades opslaat in een lijst
        logger = self._create_mock_logger()

        # Pas configuratie aan voor de backtest
        backtest_config = self.config.copy()
        backtest_config['mt5']['risk_per_trade'] = risk_per_trade
        backtest_config['mt5']['account_balance'] = initial_balance

        # Initialiseer de strategie met de mock componenten
        strategy = strategy_class(
            connector=mock_connector,
            risk_manager=risk_manager,
            logger=logger,
            config=backtest_config
        )
        # Added: Print strategy initialization
        print(f"Strategy initialized: {strategy.__class__.__name__}")

        # Resultaat tracking
        account_balance = initial_balance
        equity_curve = []
        trade_log = []
        positions = {}  # Actieve posities bijhouden
        daily_pnl = {}  # Dagelijkse P&L bijhouden

        # Loop door elke tijdstap in de historische data
        for i in range(len(self.data)):
            # Check if we have enough data for the indicators
            if i < 50:  # Need at least 50 bars for all indicators
                continue  # Skip this time step and move to the next

            # Added: Print every 100th candle
            if i % 100 == 0:  # Print every 100th candle to avoid too much output
                print(f"Processing time step {i}: {current_data['time'].iloc[-1]}")

            # Huidige tijdstap data
            current_data = self.data.iloc[:i + 1].copy()
            current_time = current_data['time'].iloc[-1]
            current_day = current_time.date()

            # Bijwerken van mock connector met huidige data
            mock_connector.set_historical_data(current_data)
            mock_connector.set_current_index(i)

            # Reset dagelijkse P&L bij nieuwe dag
            if current_day not in daily_pnl:
                daily_pnl[current_day] = 0

            # Verwerk het symbool met de strategie
            try:
                strategy.process_symbol(self.symbol)
            except Exception as e:
                print(f"Error processing {self.symbol} at {current_time}: {e}")
                continue

            # Verwerk trades van deze tijdstap
            trades = logger.get_recent_trades()

            for trade in trades:
                # Verwerk nieuwe posities
                if trade['action'] == 'BUY':
                    positions[trade['id']] = {
                        'entry_price': trade['price'],
                        'volume': trade['volume'],
                        'stop_loss': trade['sl'],
                        'entry_time': current_time,
                        'id': trade['id']
                    }
                    trade_log.append({
                        'entry_time': current_time,
                        'entry_price': trade['price'],
                        'volume': trade['volume'],
                        'stop_loss': trade['sl'],
                        'id': trade['id'],
                        'comment': trade['comment']
                    })

                # Verwerk exits
                elif trade['action'] == 'SELL':
                    # Vind bijbehorende open positie
                    if trade['id'] in positions:
                        position = positions[trade['id']]
                        # Bereken P&L
                        price_diff = trade['price'] - position['entry_price']
                        pnl = price_diff * position['volume'] * 10  # Vereenvoudigde P&L berekening

                        # Update account balance
                        account_balance += pnl

                        # Update dagelijkse P&L
                        daily_pnl[current_day] += pnl

                        # Update trade log
                        for t in trade_log:
                            if t['id'] == trade['id'] and 'exit_time' not in t:
                                t.update({
                                    'exit_time': current_time,
                                    'exit_price': trade['price'],
                                    'pnl': pnl,
                                    'hold_time': (current_time - t['entry_time']).days,
                                    'exit_comment': trade['comment']
                                })

                        # Verwijder positie
                        del positions[trade['id']]

            # Update equity curve
            equity = account_balance
            for pos_id, pos in positions.items():
                # Bereken unrealized P&L voor open posities
                current_price = current_data['close'].iloc[-1]
                price_diff = current_price - pos['entry_price']
                pos_pnl = price_diff * pos['volume'] * 10
                equity += pos_pnl

            equity_curve.append({
                'time': current_time,
                'balance': account_balance,
                'equity': equity,
                'open_positions': len(positions)
            })

        # Maak dataframe van resultaten
        results_df = pd.DataFrame(equity_curve)
        trades_df = pd.DataFrame(trade_log)

        # Bereken handelsstatistieken
        trade_stats = self._calculate_trade_stats(trades_df, initial_balance)

        return results_df, trades_df, trade_stats

    def _create_mock_connector(self):
        """Creëer een mock connector voor backtesting"""

        class MockConnector:
            def __init__(self, symbol):
                self.data = None
                self.current_idx = 0
                self.symbol = symbol
                self.connected = True
                self.order_id = 1000

            def set_historical_data(self, data):
                self.data = data

            def set_current_index(self, idx):
                self.current_idx = idx

            def get_historical_data(self, symbol, timeframe, bars_count):
                """Simuleer ophalen van historische data"""
                if self.data is None or len(self.data) == 0:
                    return pd.DataFrame()

                # Return zoveel data als beschikbaar tot huidige index
                available_bars = min(bars_count, self.current_idx + 1)
                return self.data.iloc[self.current_idx + 1 - available_bars:self.current_idx + 1].copy()

            def get_symbol_tick(self, symbol):
                """Simuleer ophalen van huidige tick data"""
                if self.data is None or len(self.data) <= self.current_idx:
                    return None

                # Maak een tick object met huidige prijzen
                class Tick:
                    pass

                tick = Tick()
                tick.ask = self.data['close'].iloc[self.current_idx]
                tick.bid = self.data['close'].iloc[self.current_idx]
                tick.time = self.data['time'].iloc[self.current_idx].timestamp()
                tick.volume = self.data['tick_volume'].iloc[self.current_idx]

                return tick

            def place_order(self, action, symbol, volume, sl, tp, price=0.0, comment=""):
                """Simuleer het plaatsen van een order"""
                self.order_id += 1
                return self.order_id - 1

            def get_open_positions(self, symbol=None):
                """Simuleer ophalen van open posities"""
                return []

            def modify_stop_loss(self, symbol, ticket, new_stop):
                """Simuleer wijzigen van stop loss"""
                return True

            def get_account_info(self):
                """Simuleer ophalen van account informatie"""
                return {
                    'balance': 100000,
                    'equity': 100000,
                    'margin': 0,
                    'free_margin': 100000,
                    'profit': 0
                }

        return MockConnector(self.symbol)

    def _create_mock_logger(self):
        """Creëer een mock logger voor backtesting"""

        class MockLogger:
            def __init__(self):
                self.trades = []
                self.info_logs = []
                self.status_logs = []
                self.trade_id = 0

            def log_trade(self, symbol, action, price, volume, sl, tp, comment):
                """Log een trade naar interne lijst"""
                self.trade_id += 1
                self.trades.append({
                    'time': datetime.now(),
                    'symbol': symbol,
                    'action': action,
                    'price': price,
                    'volume': volume,
                    'sl': sl,
                    'tp': tp,
                    'comment': comment,
                    'id': self.trade_id
                })

            def log_info(self, message):
                """Log een informatiebericht"""
                self.info_logs.append({
                    'time': datetime.now(),
                    'message': message
                })

            def log_status(self, account_info, open_positions):
                """Log status informatie"""
                self.status_logs.append({
                    'time': datetime.now(),
                    'account_info': account_info,
                    'open_positions': open_positions
                })

            def get_recent_trades(self):
                """Haal recente trades op en leeg de lijst"""
                trades = self.trades.copy()
                self.trades = []
                return trades

        return MockLogger()

    def _calculate_trade_stats(self, trades_df, initial_balance):
        """Bereken handelsstatistieken"""
        if trades_df.empty or 'pnl' not in trades_df.columns:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'max_profit': 0,
                'max_loss': 0,
                'total_profit': 0,
                'avg_hold_time': 0,
                'return': 0
            }

        # Filter op completed trades
        completed_trades = trades_df.dropna(subset=['exit_time'])

        # Basis statistieken
        total_trades = len(completed_trades)
        winning_trades = completed_trades[completed_trades['pnl'] > 0]
        losing_trades = completed_trades[completed_trades['pnl'] <= 0]

        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0

        # Winst/verlies statistieken
        total_profit = completed_trades['pnl'].sum()
        gross_profit = winning_trades['pnl'].sum() if not winning_trades.empty else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if not losing_trades.empty else 0

        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        avg_win = winning_trades['pnl'].mean() if not winning_trades.empty else 0
        avg_loss = losing_trades['pnl'].mean() if not losing_trades.empty else 0

        max_profit = completed_trades['pnl'].max() if not completed_trades.empty else 0
        max_loss = completed_trades['pnl'].min() if not completed_trades.empty else 0

        # Duur statistieken
        avg_hold_time = completed_trades['hold_time'].mean() if 'hold_time' in completed_trades.columns else 0

        # Return berekening
        percent_return = (initial_balance + total_profit) / initial_balance - 1

        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'total_profit': total_profit,
            'avg_hold_time': avg_hold_time,
            'return': percent_return
        }

    def plot_results(self, results_df, trades_df, trade_stats):
        """
        Plot backtest resultaten
        """
        plt.figure(figsize=(14, 10))

        # Plot equity curve
        plt.subplot(2, 1, 1)
        plt.plot(results_df['time'], results_df['equity'], label='Equity', color='blue')
        plt.plot(results_df['time'], results_df['balance'], label='Balance', color='green', alpha=0.7)

        # Markeer trades op de equity curve
        if not trades_df.empty and 'entry_time' in trades_df.columns:
            for i, trade in trades_df.iterrows():
                if 'exit_time' in trade and pd.notna(trade['exit_time']):
                    # Kleur op basis van winst/verlies
                    color = 'green' if trade.get('pnl', 0) > 0 else 'red'
                    plt.axvspan(trade['entry_time'], trade['exit_time'], alpha=0.2, color=color)

        plt.title(f'Equity Curve - {self.symbol} - Return: {trade_stats["return"] * 100:.2f}%')
        plt.ylabel('Equity ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Plot aantal open posities
        plt.subplot(2, 1, 2)
        plt.plot(results_df['time'], results_df['open_positions'], drawstyle='steps-post', color='purple')
        plt.title('Aantal Open Posities')
        plt.ylabel('Aantal Posities')
        plt.xlabel('Datum')
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"{self.symbol}_backtest_results.png"))
        plt.show()

        # Display trade statistics as a table
        print("\nHandelsstatistieken:")
        print(f"Totaal aantal trades: {trade_stats['total_trades']}")
        print(f"Winratio: {trade_stats['win_rate']:.2%}")
        print(f"Profit factor: {trade_stats['profit_factor']:.2f}")
        print(f"Gemiddelde winst: ${trade_stats['avg_win']:.2f}")
        print(f"Gemiddeld verlies: ${trade_stats['avg_loss']:.2f}")
        print(f"Maximale winst: ${trade_stats['max_profit']:.2f}")
        print(f"Maximaal verlies: ${trade_stats['max_loss']:.2f}")
        print(f"Totale winst: ${trade_stats['total_profit']:.2f}")
        print(f"Gemiddelde houdperiode: {trade_stats['avg_hold_time']:.1f} dagen")
        print(f"Rendement: {trade_stats['return'] * 100:.2f}%")

# Gebruiksvoorbeeld:
#
# # Laad historische data
# data = ... # DataFrame met historische data
#
# # Maak backtest object
# backtest = DirectBacktester(data, "EURUSD", config)
#
# # Voer backtest uit
# results_df, trades_df, trade_stats = backtest.run_backtest()
#
# # Plot resultaten
# backtest.plot_results(results_df, trades_df, trade_stats)