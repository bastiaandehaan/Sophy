# modules/backtester.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import MetaTrader5 as mt5


class Backtester:
    """Backtesting module voor trading strategieën"""

    def __init__(self, connector, config, output_dir='test_results'):
        """
        Initialiseer de backtester

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5
        config : dict
            Configuratie voor de backtester
        output_dir : str, optional
            Map voor het opslaan van resultaten
        """
        self.connector = connector
        self.config = config
        self.output_dir = output_dir

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # Performance metrics
        self.metrics = {}

    def run_backtest(self, symbol, strategy_class, start_date, end_date,
                     risk_per_trade=0.01, timeframe=mt5.TIMEFRAME_H4):
        """
        Voer een backtest uit voor een symbool en strategie

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        strategy_class : class
            De strategie klasse om te testen
        start_date : datetime
            Start datum
        end_date : datetime
            Eind datum
        risk_per_trade : float, optional
            Risico per trade (percentage van account)
        timeframe : int, optional
            MT5 timeframe constante

        Returns:
        --------
        tuple
            (DataFrame met resultaten, Dictionary met statistieken)
        """
        print(f"\nBacktest starten voor {symbol} met {strategy_class.__name__}")
        print(f"Periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Pas configuratie aan voor backtest
        backtest_config = self.config.copy()
        backtest_config['mt5']['risk_per_trade'] = risk_per_trade

        # Haal historische data op
        df = self.get_historical_data(symbol, timeframe, start_date, end_date)
        if df.empty:
            print(f"Geen historische data beschikbaar voor {symbol}")
            return None, {}

        print(f"Data geladen: {len(df)} candles")

        # Creëer MockConnector en andere componenten voor de strategie
        mock_connector = self._create_mock_connector(df)
        mock_logger = self._create_mock_logger()
        risk_manager = self._create_risk_manager(risk_per_trade)

        # Initialiseer strategie
        strategy = strategy_class(
            connector=mock_connector,
            risk_manager=risk_manager,
            logger=mock_logger,
            config=backtest_config
        )

        # Voorbereiden voor simulatie
        account_balance = backtest_config['mt5'].get('account_balance', 100000)
        equity_curve = []
        trades = []

        # Simuleer verwerking van elke candle
        min_bars_needed = 50  # Minimaal aantal candles nodig voor indicatoren
        for i in range(len(df)):
            # Skip eerste candles totdat we genoeg data hebben voor alle indicatoren
            if i < min_bars_needed:
                continue

            # Update huidige data
            current_data = df.iloc[:i + 1].copy()
            current_time = current_data['time'].iloc[-1]

            # Update mock connector met huidige data
            mock_connector.update_data(current_data, i)

            # Verwerk symbool met strategie
            try:
                strategy.process_symbol(symbol)
            except Exception as e:
                print(f"Fout bij verwerken van {symbol} op {current_time}: {e}")
                import traceback
                traceback.print_exc()
                continue

            # Verwerk nieuwe trades
            new_trades = mock_logger.get_trades()
            for trade in new_trades:
                if trade['action'] == 'BUY':
                    # Nieuwe positie openen
                    open_trade = {
                        'entry_time': current_time,
                        'entry_price': trade['price'],
                        'volume': trade['volume'],
                        'stop_loss': trade['sl'],
                        'comment': trade['comment'],
                        'position_id': len(trades) + 1
                    }
                    trades.append(open_trade)
                    mock_connector.add_position(open_trade)
                elif trade['action'] == 'SELL':
                    # Zoek bijbehorende open positie
                    position = mock_connector.get_position_by_id(trade['position_id'])
                    if position:
                        # Bereken P&L
                        entry_price = position['entry_price']
                        exit_price = trade['price']
                        volume = position['volume']

                        pnl = self._calculate_pnl(symbol, entry_price, exit_price, volume)

                        # Update account balance
                        account_balance += pnl

                        # Update trade record
                        position['exit_time'] = current_time
                        position['exit_price'] = exit_price
                        position['pnl'] = pnl

                        # Verwijder positie
                        mock_connector.close_position(position['position_id'])

            # Update equity curve
            equity = account_balance
            for pos in mock_connector.get_open_positions():
                # Bereken unrealized P&L
                current_price = current_data['close'].iloc[-1]
                unrealized_pnl = self._calculate_pnl(
                    symbol, pos['entry_price'], current_price, pos['volume']
                )
                equity += unrealized_pnl

            equity_curve.append({
                'time': current_time,
                'balance': account_balance,
                'equity': equity,
                'open_positions': len(mock_connector.get_open_positions())
            })

        # Sluit eventuele open posities aan het einde
        final_price = df['close'].iloc[-1]
        for pos in mock_connector.get_open_positions():
            pnl = self._calculate_pnl(symbol, pos['entry_price'], final_price, pos['volume'])
            account_balance += pnl

            pos['exit_time'] = df['time'].iloc[-1]
            pos['exit_price'] = final_price
            pos['pnl'] = pnl

        # Maak resultaat DataFrames
        results_df = pd.DataFrame(equity_curve)
        trades_df = pd.DataFrame([t for t in trades if 'exit_price' in t])

        # Bereken statistieken
        stats = self._calculate_statistics(trades_df, backtest_config['mt5']['account_balance'])

        # Sla resultaten op
        self.metrics[symbol] = stats

        return results_df, trades_df, stats

    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        """
        Haal historische data op voor backtesting

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        timeframe : int
            MT5 timeframe constante
        start_date : datetime
            Start datum
        end_date : datetime
            Eind datum

        Returns:
        --------
        pandas.DataFrame
            DataFrame met historische data
        """
        # Converteer datums naar timestamps (met 1 uur correctie voor FTMO tijdverschil)
        start_timestamp = int((start_date - timedelta(hours=1)).timestamp())
        end_timestamp = int((end_date - timedelta(hours=1)).timestamp())

        # Haal data op via de connector (gebruik mapped_symbol indien nodig)
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config['mt5'] and symbol in self.config['mt5']['symbol_mapping']:
            mapped_symbol = self.config['mt5']['symbol_mapping'][symbol]

        # Haal data op van MT5
        rates = mt5.copy_rates_range(mapped_symbol, timeframe, start_timestamp, end_timestamp)
        if rates is None or len(rates) == 0:
            print(f"Geen historische data beschikbaar voor {mapped_symbol}")
            return pd.DataFrame()

        # Converteer naar DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df

    def _calculate_pnl(self, symbol, entry_price, exit_price, volume):
        """Bereken winst/verlies van een positie"""
        point_value = 0.1  # Standaard waarde

        # Aanpassen per symbool type
        if symbol == "EURUSD" or symbol == "GBPUSD" or "USD" in symbol and not symbol == "XAUUSD":
            point_value = 0.0001  # Forex
        elif symbol == "XAUUSD":
            point_value = 0.1  # Goud
        elif symbol == "US30":
            point_value = 1.0  # US30 index

        pip_value = 10  # Standaard pip waarde
        pips = (exit_price - entry_price) / point_value

        return pips * volume * pip_value

    def _create_mock_connector(self, data):
        """Creëer een mock connector voor backtesting"""

        class MockConnector:
            def __init__(self, data):
                self.data = data
                self.current_idx = 0
                self.open_positions = []
                self.next_position_id = 1

            def update_data(self, data, idx):
                self.data = data
                self.current_idx = idx

            def get_historical_data(self, symbol, timeframe, bars_count):
                available_bars = min(bars_count, self.current_idx + 1)
                return self.data.iloc[self.current_idx + 1 - available_bars:self.current_idx + 1].copy()

            def get_symbol_tick(self, symbol):
                if self.current_idx >= len(self.data):
                    return None

                class Tick:
                    pass

                tick = Tick()
                tick.ask = self.data['close'].iloc[self.current_idx]
                tick.bid = self.data['close'].iloc[self.current_idx]
                tick.time = self.data['time'].iloc[self.current_idx].timestamp()
                return tick

            def place_order(self, action, symbol, volume, sl, tp, price=0.0, comment=""):
                if action == "BUY":
                    position_id = self.next_position_id
                    self.next_position_id += 1
                    return position_id
                elif action == "SELL":
                    # Extract position ID from comment if possible
                    position_id = None
                    if "ticket:" in comment:
                        try:
                            position_id = int(comment.split("ticket:")[1].strip())
                        except:
                            pass
                    return position_id
                return None

            def get_open_positions(self, symbol=None):
                return self.open_positions

            def add_position(self, position):
                self.open_positions.append(position)

            def close_position(self, position_id):
                self.open_positions = [p for p in self.open_positions if p['position_id'] != position_id]

            def get_position_by_id(self, position_id):
                for pos in self.open_positions:
                    if pos['position_id'] == position_id:
                        return pos
                return None

            def modify_stop_loss(self, symbol, ticket, new_stop):
                for pos in self.open_positions:
                    if pos['position_id'] == ticket:
                        pos['stop_loss'] = new_stop
                        return True
                return False

        return MockConnector(data)

    def _create_mock_logger(self):
        """Creëer een mock logger voor backtesting"""

        class MockLogger:
            def __init__(self):
                self.trades = []

            def log_trade(self, symbol, action, price, volume, sl, tp, comment):
                position_id = None
                if "ticket:" in comment:
                    try:
                        position_id = int(comment.split("ticket:")[1].strip())
                    except:
                        pass

                self.trades.append({
                    'symbol': symbol,
                    'action': action,
                    'price': price,
                    'volume': volume,
                    'sl': sl,
                    'tp': tp,
                    'comment': comment,
                    'position_id': position_id
                })

            def log_info(self, message):
                pass  # Negeer info logs tijdens backtesting

            def log_status(self, account_info, open_positions):
                pass  # Negeer status logs tijdens backtesting

            def get_trades(self):
                trades = self.trades.copy()
                self.trades = []
                return trades

        return MockLogger()

    def _create_risk_manager(self, risk_per_trade):
        """Creëer een vereenvoudigde risicomanager voor backtesting"""

        class MockRiskManager:
            def __init__(self, risk_per_trade):
                self.max_risk_per_trade = risk_per_trade

            def can_trade(self):
                return True

            def check_trade_risk(self, symbol, volume, entry_price, stop_loss):
                return True

        return MockRiskManager(risk_per_trade)

    def _calculate_statistics(self, trades_df, initial_balance):
        """Bereken handelstatistieken"""
        if trades_df.empty:
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

        # Bereken handelsstatistieken
        total_trades = len(trades_df)

        # Winst/verlies statistieken
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] <= 0]

        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0

        gross_profit = winning_trades['pnl'].sum() if not winning_trades.empty else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if not losing_trades.empty else 0

        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        avg_win = winning_trades['pnl'].mean() if not winning_trades.empty else 0
        avg_loss = losing_trades['pnl'].mean() if not losing_trades.empty else 0

        max_profit = trades_df['pnl'].max() if not trades_df.empty else 0
        max_loss = trades_df['pnl'].min() if not trades_df.empty else 0

        total_profit = trades_df['pnl'].sum()

        # Bereken gemiddelde houdduur
        if 'entry_time' in trades_df.columns and 'exit_time' in trades_df.columns:
            trades_df['duration'] = (trades_df['exit_time'] - trades_df['entry_time']).dt.total_seconds() / (
                        60 * 60 * 24)
            avg_hold_time = trades_df['duration'].mean()
        else:
            avg_hold_time = 0

        # Bereken rendement
        return_pct = (initial_balance + total_profit) / initial_balance - 1

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
            'return': return_pct
        }

    def plot_results(self, results_df, trades_df, stats, symbol, filename=None):
        """
        Plot backtest resultaten

        Parameters:
        -----------
        results_df : pandas.DataFrame
            DataFrame met equity curve
        trades_df : pandas.DataFrame
            DataFrame met trades
        stats : dict
            Handelsstatistieken
        symbol : str
            Het handelssymbool
        filename : str, optional
            Bestandsnaam voor de plot
        """
        if results_df is None or results_df.empty:
            print(f"Geen resultaten om te plotten voor {symbol}")
            return

        # Maak plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

        # Plot 1: Equity Curve
        ax1.plot(results_df['time'], results_df['equity'], label='Equity', color='blue')
        ax1.plot(results_df['time'], results_df['balance'], label='Balance', color='green', alpha=0.7)

        # Markeer trades op de equity curve
        if not trades_df.empty:
            for _, trade in trades_df.iterrows():
                if 'entry_time' in trade and 'exit_time' in trade:
                    # Kleur gebaseerd op winst/verlies
                    color = 'green' if trade['pnl'] > 0 else 'red'
                    ax1.axvspan(trade['entry_time'], trade['exit_time'], alpha=0.1, color=color)

        ax1.set_title(f'Backtest Resultaten voor {symbol} - Rendement: {stats["return"] * 100:.2f}%')
        ax1.set_ylabel('Account Waarde ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Open Positions
        ax2.plot(results_df['time'], results_df['open_positions'], drawstyle='steps-post', color='purple')
        ax2.set_title('Open Posities')
        ax2.set_ylabel('Aantal')
        ax2.set_xlabel('Datum')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        # Sla plot op indien gewenst
        if filename:
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path)
            print(f"Plot opgeslagen als {output_path}")

        plt.show()

        # Toon handelsstatistieken
        print("\nHandelsstatistieken:")
        print(f"Totaal aantal trades: {stats['total_trades']}")
        print(f"Winratio: {stats['win_rate']:.2%}")
        print(f"Profit factor: {stats['profit_factor']:.2f}")
        print(f"Gemiddelde winst: ${stats['avg_win']:.2f}")
        print(f"Gemiddeld verlies: ${stats['avg_loss']:.2f}")
        print(f"Maximale winst: ${stats['max_profit']:.2f}")
        print(f"Maximaal verlies: ${stats['max_loss']:.2f}")
        print(f"Totale winst: ${stats['total_profit']:.2f}")
        print(f"Gemiddelde houdduur: {stats['avg_hold_time']:.1f} dagen")
        print(f"Rendement: {stats['return'] * 100:.2f}%")