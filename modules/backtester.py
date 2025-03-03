import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('TkAgg')  # Stel backend in op TkAgg voor een apart venster
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import MetaTrader5 as mt5
import itertools


class Backtester:
    """Backtesting module voor de Turtle Trading strategie"""

    def __init__(self, connector, config, output_dir='data/backtest_results'):
        """
        Initialiseer de backtester

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5 voor het ophalen van historische data
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

        # Standaard parameters voor de Turtle strategie
        self.default_params = {
            'entry_period': 20,  # Breakout periode voor entry
            'exit_period': 10,  # Breakout periode voor exit
            'atr_period': 20,  # ATR berekeningsperiode
            'atr_multiplier': 2,  # Vermenigvuldiger voor stop loss berekening
            'risk_per_trade': 0.01,  # Risico per trade (1%)
            'use_trend_filter': True  # Gebruik EMA trendfilter
        }

        # Performance metrics
        self.metrics = {}

    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        """
        Haal historische data op voor backtesting

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        timeframe : int
            MT5 timeframe constante (bijv. mt5.TIMEFRAME_D1)
        start_date : datetime
            Start datum
        end_date : datetime
            Eind datum

        Returns:
        --------
        pandas.DataFrame
            DataFrame met historische data
        """
        # Converteer datums naar timestamps
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        # Haal data op via de connector (gebruik mapped_symbol indien nodig)
        mapped_symbol = symbol
        if 'symbol_mapping' in self.config['mt5'] and symbol in self.config['mt5']['symbol_mapping']:
            mapped_symbol = self.config['mt5']['symbol_mapping'][symbol]

        # Haal data op van MT5
        rates = mt5.copy_rates_range(mapped_symbol, timeframe, start_timestamp, end_timestamp)
        if rates is None or len(rates) == 0:
            print(f"Geen historische data beschikbaar voor {mapped_symbol} tussen {start_date} en {end_date}")
            return pd.DataFrame()

        # Converteer naar DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df

    def calculate_atr(self, df, period=20):
        """
        Bereken Average True Range (ATR)

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata
        period : int, optional
            ATR periode

        Returns:
        --------
        pandas.Series
            ATR waarden
        """
        high = df['high']
        low = df['low']
        close = df['close'].shift(1)

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)

        tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
        atr = tr.rolling(window=period).mean()

        return atr

    def run_backtest(self, symbol, start_date, end_date, timeframe=mt5.TIMEFRAME_D1, params=None):
        """
        Voer een backtest uit voor een bepaald symbool en periode

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        start_date : datetime
            Start datum
        end_date : datetime
            Eind datum
        timeframe : int, optional
            MT5 timeframe constante
        params : dict, optional
            Parameters voor de strategie, gebruikt standaard waardes indien niet opgegeven

        Returns:
        --------
        pandas.DataFrame
            DataFrame met backtest resultaten
        """
        # Veilige manier om de parameters te tonen
        print(f"\nBacktest starten voor {symbol} met timeframe {timeframe}")

        # Valideer datum parameters
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            print(f"Fout: start_date en end_date moeten datetime objecten zijn")
            print(f"Ontvangen types: start_date={type(start_date)}, end_date={type(end_date)}")
            return None

        print(f"Periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Gebruik standaard parameters als geen parameters zijn opgegeven
        if params is None:
            params = self.default_params

        # Haal historische data op
        df = self.get_historical_data(symbol, timeframe, start_date, end_date)
        if df.empty:
            print(f"Backtest overgeslagen voor {symbol}: geen data beschikbaar")
            return None

        # Bereken indicatoren
        df['atr'] = self.calculate_atr(df, params['atr_period'])
        df['high_entry'] = df['high'].rolling(window=params['entry_period']).max()
        df['low_exit'] = df['low'].rolling(window=params['exit_period']).min()

        # Voeg trendfilter toe indien gewenst
        if params['use_trend_filter']:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            df['trend_bullish'] = df['close'] > df['ema_50']
        else:
            df['trend_bullish'] = True

        # Initialiseer kolommen voor trades
        df['position'] = 0  # 0: geen positie, 1: long
        df['entry_price'] = np.nan
        df['stop_loss'] = np.nan
        df['position_size'] = np.nan
        df['equity'] = self.config['mt5']['account_balance']
        df['trade_result'] = np.nan
        df['trade_profit'] = np.nan

        # Simuleer trades
        account_balance = self.config['mt5']['account_balance']
        position = 0
        entry_price = 0
        stop_loss = 0
        position_size = 0

        # Loop door alle candlesticks
        for i in range(params['entry_period'] + 1, len(df)):
            current_price = df.iloc[i]['close']

            # Als we geen positie hebben, check voor entry signaal
            if position == 0:
                # Check breakout (huidige prijs > vorige high_entry) en trendfilter
                if (df.iloc[i]['close'] > df.iloc[i - 1]['high_entry'] and
                        df.iloc[i]['atr'] > 0 and
                        df.iloc[i]['trend_bullish']):
                    # Entry signaal: open positie
                    position = 1
                    entry_price = current_price
                    stop_loss = current_price - (params['atr_multiplier'] * df.iloc[i]['atr'])

                    # Bereken positiegrootte op basis van risico
                    risk_amount = account_balance * params['risk_per_trade']
                    dollar_per_pip = risk_amount / (entry_price - stop_loss)

                    # Vereenvoudigde berekening van lotgrootte (aan te passen per instrument)
                    position_size = round(dollar_per_pip / 10000, 2)
                    position_size = max(0.01, min(position_size, 10.0))

                    # Sla trade informatie op
                    df.at[df.index[i], 'position'] = position
                    df.at[df.index[i], 'entry_price'] = entry_price
                    df.at[df.index[i], 'stop_loss'] = stop_loss
                    df.at[df.index[i], 'position_size'] = position_size

            # Als we een positie hebben, check voor exit signaal
            elif position == 1:
                # Check exit criteria: prijs < vorige low_exit of stop loss geraakt
                if (current_price < df.iloc[i - 1]['low_exit'] or current_price <= stop_loss):
                    # Exit signaal: sluit positie
                    exit_price = current_price
                    trade_result = 1 if exit_price > entry_price else -1

                    # Bereken winst/verlies (vereenvoudigd)
                    pips_profit = exit_price - entry_price
                    trade_profit = pips_profit * position_size * 10000  # Aanpassen per instrument

                    # Update account balance
                    account_balance += trade_profit

                    # Sla trade resultaat op
                    df.at[df.index[i], 'position'] = 0
                    df.at[df.index[i], 'trade_result'] = trade_result
                    df.at[df.index[i], 'trade_profit'] = trade_profit

                    # Reset positie
                    position = 0
                    entry_price = 0
                    stop_loss = 0
                    position_size = 0

            # Update equity curve
            df.at[df.index[i], 'equity'] = account_balance

        # Bereken performance metrics
        self.calculate_performance_metrics(df, symbol, params)

        return df

    def calculate_performance_metrics(self, df, symbol, params):
        """
        Bereken performance metrics voor de backtest

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met backtest resultaten
        symbol : str
            Het handelssymbool
        params : dict
            Parameters gebruikt in de backtest
        """
        # Filter alleen trades
        trades_df = df[df['trade_result'].notna()]

        if len(trades_df) == 0:
            print(f"Geen trades gevonden voor {symbol}")
            self.metrics[symbol] = {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'avg_profit': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'return': 0,
                'params': params
            }
            return

        # Aantal trades
        total_trades = len(trades_df)

        # Win ratio
        winning_trades = len(trades_df[trades_df['trade_result'] > 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        # Profit factor
        gross_profit = trades_df[trades_df['trade_profit'] > 0]['trade_profit'].sum()
        gross_loss = abs(trades_df[trades_df['trade_profit'] < 0]['trade_profit'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')

        # Gemiddelde winst per trade
        avg_profit = trades_df['trade_profit'].mean()

        # Maximale drawdown
        df['peak'] = df['equity'].cummax()
        df['drawdown'] = (df['equity'] - df['peak']) / df['peak']
        max_drawdown = abs(df['drawdown'].min())

        # Sharpe ratio (vereenvoudigd, dagelijkse basis)
        if len(df) > 1:
            df['daily_return'] = df['equity'].pct_change()
            avg_return = df['daily_return'].mean()
            std_return = df['daily_return'].std()
            sharpe_ratio = (avg_return / std_return) * np.sqrt(252) if std_return != 0 else 0
        else:
            sharpe_ratio = 0

        # Totaal rendement
        total_return = (df['equity'].iloc[-1] - df['equity'].iloc[0]) / df['equity'].iloc[0]

        # Sla metrics op
        self.metrics[symbol] = {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_profit': avg_profit,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'return': total_return,
            'params': params
        }

        print(f"Backtest resultaten voor {symbol}:")
        print(f"  Totaal trades: {total_trades}")
        print(f"  Win rate: {win_rate:.2%}")
        print(f"  Profit factor: {profit_factor:.2f}")
        print(f"  Gemiddelde winst per trade: ${avg_profit:.2f}")
        print(f"  Maximale drawdown: {max_drawdown:.2%}")
        print(f"  Sharpe ratio: {sharpe_ratio:.2f}")
        print(f"  Totaal rendement: {total_return:.2%}")

    def plot_results(self, df, symbol, output_filename=None):
        """
        Plot de backtest resultaten

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met backtest resultaten
        symbol : str
            Het handelssymbool
        output_filename : str, optional
            Bestandsnaam voor het opslaan van de plot
        """
        if df is None or df.empty:
            print(f"Geen data om te plotten voor {symbol}")
            return

        # Maak plots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})

        # Plot 1: Prijs en trades
        ax1.plot(df['time'], df['close'], label='Prijs', color='blue', alpha=0.5)

        # Markeer entry en exit punten
        entries = df[df['position'] == 1]
        exits = df[df['trade_result'].notna()]

        if not entries.empty:
            ax1.scatter(entries['time'], entries['entry_price'], color='green', marker='^', label='Entry')

        if not exits.empty:
            # Kleur exits op basis van resultaat (groen = winst, rood = verlies)
            for idx, row in exits.iterrows():
                color = 'green' if row['trade_result'] > 0 else 'red'
                ax1.scatter(row['time'], row['close'], color=color, marker='v')

        # Voeg stop loss niveaus toe
        for idx, row in entries.iterrows():
            if not np.isnan(row['stop_loss']):
                ax1.plot([row['time'], row['time']], [row['entry_price'], row['stop_loss']], 'r--', alpha=0.5)

        ax1.set_title(f'Backtest resultaten voor {symbol}')
        ax1.set_ylabel('Prijs')
        ax1.legend()
        ax1.grid(True)

        # Plot 2: Equity curve
        ax2.plot(df['time'], df['equity'], label='Account Equity', color='purple')
        ax2.set_xlabel('Datum')
        ax2.set_ylabel('Equity ($)')
        ax2.grid(True)

        plt.tight_layout()

        # Sla plot op indien gewenst
        if output_filename:
            output_path = os.path.join(self.output_dir, output_filename)
            plt.savefig(output_path)
            print(f"Plot opgeslagen als {output_path}")

        plt.show()

    def optimize_parameters(self, symbol, start_date, end_date, param_grid=None):
        """
        Optimaliseer strategie parameters door grid search

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        start_date : datetime
            Start datum
        end_date : datetime
            Eind datum
        param_grid : dict, optional
            Grid van te testen parameters

        Returns:
        --------
        dict
            Beste parameters gevonden
        """
        if param_grid is None:
            # Standaard parameter grid voor optimalisatie
            param_grid = {
                'entry_period': [10, 20, 30, 40, 55],
                'exit_period': [5, 10, 15, 20],
                'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
                'use_trend_filter': [True, False]
            }

        # Stel alle mogelijke parameter combinaties samen
        param_keys = param_grid.keys()
        param_values = param_grid.values()
        param_combinations = list(itertools.product(*param_values))

        print(f"Optimalisatie gestart voor {symbol}...")
        print(f"Aantal parameter combinaties: {len(param_combinations)}")

        best_return = -float('inf')
        best_params = None
        best_sharpe = -float('inf')
        best_sharpe_params = None

        # Test elke parameter combinatie
        for i, combo in enumerate(param_combinations):
            params = dict(zip(param_keys, combo))

            # Voeg vaste parameters toe die niet geoptimaliseerd worden
            params['atr_period'] = 20
            params['risk_per_trade'] = self.default_params['risk_per_trade']

            print(f"Testing combination {i + 1}/{len(param_combinations)}: {params}")

            # Voer backtest uit met deze parameters

            result_df = self.run_backtest(symbol, start_date, end_date, mt5.TIMEFRAME_D1, params=params)

            # Haal metrics op
            if symbol in self.metrics:
                metrics = self.metrics[symbol]
                current_return = metrics['return']
                current_sharpe = metrics['sharpe_ratio']

                # Check if better than current best (by return)
                if current_return > best_return:
                    best_return = current_return
                    best_params = params.copy()

                # Check if better than current best (by Sharpe ratio)
                if current_sharpe > best_sharpe:
                    best_sharpe = current_sharpe
                    best_sharpe_params = params.copy()

        print("\nOptimalisatie resultaten:")
        print(f"\nBeste parameters op basis van rendement (return: {best_return:.2%}):")
        for key, value in best_params.items():
            print(f"  {key}: {value}")

        print(f"\nBeste parameters op basis van Sharpe ratio (Sharpe: {best_sharpe:.2f}):")
        for key, value in best_sharpe_params.items():
            print(f"  {key}: {value}")

        # Sla resultaten op
        self.best_params = best_params
        self.best_sharpe_params = best_sharpe_params

        return {
            'best_return_params': best_params,
            'best_sharpe_params': best_sharpe_params
        }