import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from datetime import datetime, timedelta

# Voeg projectpad toe aan Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_dir)

# Importeer modules
from modules.mt5_connector import MT5Connector
from modules.strategy import TurtleStrategy
from modules.enhanced_strategy import EnhancedTurtleStrategy
from modules.backtester import DirectBacktester


def load_config(config_path):
    """Laad configuratie uit JSON bestand"""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        sys.exit(1)


def get_historical_data(symbol, timeframe, start_date, end_date=None):
    """
    Haal historische data op vanuit MT5

    Parameters:
    -----------
    symbol : str
        Het handelssymbool
    timeframe : int
        MT5 timeframe constante
    start_date : datetime
        Startdatum voor historische data
    end_date : datetime, optional
        Einddatum voor historische data, standaard is nu

    Returns:
    --------
    pandas.DataFrame
        DataFrame met historische data
    """
    if end_date is None:
        end_date = datetime.now()

    # Converteren naar timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # Data ophalen
    rates = mt5.copy_rates_range(symbol, timeframe, start_timestamp, end_timestamp)
    if rates is None or len(rates) == 0:
        print(f"Geen historische data beschikbaar voor {symbol}")
        return pd.DataFrame()

    # Converteren naar DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df


def run_comparative_test(symbol, timeframe, start_date, end_date=None, risk_per_trade=0.01):
    """
    Voer vergelijkende test uit tussen originele en verbeterde strategie

    Parameters:
    -----------
    symbol : str
        Het handelssymbool
    timeframe : int
        MT5 timeframe constante
    start_date : datetime
        Startdatum voor historische data
    end_date : datetime, optional
        Einddatum voor historische data
    risk_per_trade : float
        Risico per trade als percentage
    """
    print(f"\n{'=' * 50}")
    print(f"VERGELIJKENDE TEST VOOR {symbol}")
    print(f"{'=' * 50}")
    print(f"Periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d') if end_date else 'nu'}")
    print(f"Timeframe: {timeframe_to_string(timeframe)}")
    print(f"Risico per trade: {risk_per_trade * 100}%")

    # Initialiseer MT5 als dat nog niet is gebeurd
    if not mt5.initialize():
        print("MT5 initialisatie mislukt. Controleer of MT5 is geïnstalleerd en draait.")
        return

    try:
        # Laad configuratie
        config_path = os.path.join(project_dir, 'config', 'turtle_settings.json')
        config = load_config(config_path)

        # Pas configuratie aan voor het test symbool
        if symbol not in config['mt5']['symbols']:
            # Als symbool niet in config staat, voeg het tijdelijk toe
            config['mt5']['symbols'].append(symbol)

        # Haal historische data op
        data = get_historical_data(symbol, timeframe, start_date, end_date)

        if data.empty:
            print(f"Geen data beschikbaar voor {symbol}. Test gestopt.")
            return

        print(f"Data geladen: {len(data)} candles")

        # Maak output directory
        output_dir = os.path.join(project_dir, 'test_results', symbol)
        os.makedirs(output_dir, exist_ok=True)

        # Initialiseer backtesters voor beide strategieën
        original_backtest = DirectBacktester(data, symbol, config, output_dir=output_dir)
        enhanced_backtest = DirectBacktester(data, symbol, config, output_dir=output_dir)

        # Voer backtests uit
        print("\nTESTEN ORIGINELE STRATEGIE...")
        original_results, original_trades, original_stats = original_backtest.run_backtest(
            strategy_class=TurtleStrategy,
            risk_per_trade=risk_per_trade
        )

        print("\nTESTEN VERBETERDE STRATEGIE...")
        enhanced_results, enhanced_trades, enhanced_stats = enhanced_backtest.run_backtest(
            strategy_class=EnhancedTurtleStrategy,
            risk_per_trade=risk_per_trade
        )

        # Plot resultaten
        print("\nPlotten resultaten van originele strategie...")
        original_backtest.plot_results(original_results, original_trades, original_stats)

        print("\nPlotten resultaten van verbeterde strategie...")
        enhanced_backtest.plot_results(enhanced_results, enhanced_trades, enhanced_stats)

        # Vergelijk de resultaten
        compare_results(symbol, original_stats, enhanced_stats, original_trades, enhanced_trades)

    except Exception as e:
        print(f"Error tijdens test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Sluit MT5 verbinding
        mt5.shutdown()


def compare_results(symbol, original_stats, enhanced_stats, original_trades, enhanced_trades):
    """
    Vergelijk resultaten van beide strategieën

    Parameters:
    -----------
    symbol : str
        Het handelssymbool
    original_stats : dict
        Statistieken van originele strategie
    enhanced_stats : dict
        Statistieken van verbeterde strategie
    original_trades : pandas.DataFrame
        Trades van originele strategie
    enhanced_trades : pandas.DataFrame
        Trades van verbeterde strategie
    """
    print(f"\n{'=' * 50}")
    print(f"VERGELIJKING RESULTATEN VOOR {symbol}")
    print(f"{'=' * 50}")

    metrics = [
        ('total_trades', 'Aantal trades'),
        ('win_rate', 'Winratio', '{:.2%}'),
        ('profit_factor', 'Profit factor', '{:.2f}'),
        ('avg_win', 'Gemiddelde winst', '${:.2f}'),
        ('avg_loss', 'Gemiddeld verlies', '${:.2f}'),
        ('max_profit', 'Maximale winst', '${:.2f}'),
        ('max_loss', 'Maximaal verlies', '${:.2f}'),
        ('total_profit', 'Totale winst', '${:.2f}'),
        ('avg_hold_time', 'Gemiddelde houdduur', '{:.1f} dagen'),
        ('return', 'Rendement', '{:.2%}')
    ]

    print(f"{'Metriek':<25} {'Origineel':<15} {'Verbeterd':<15} {'Verschil':<15}")
    print('-' * 70)

    for metric, name, *fmt in metrics:
        format_str = fmt[0] if fmt else '{}'

        orig_val = original_stats.get(metric, 0)
        enh_val = enhanced_stats.get(metric, 0)

        if metric in ['win_rate', 'return']:
            # Voor percentages, bereken absolute verschil in procent-punten
            diff = (enh_val - orig_val) * 100
            diff_str = f"{diff:+.2f}%"
        elif metric in ['profit_factor', 'avg_hold_time']:
            # Voor ratio's, bereken procentueel verschil
            diff = ((enh_val / orig_val) - 1) * 100 if orig_val else float('inf')
            diff_str = f"{diff:+.2f}%" if diff != float('inf') else 'N/A'
        else:
            # Voor absolute waardes, bereken procentueel verschil
            diff = ((enh_val / orig_val) - 1) * 100 if orig_val else float('inf')
            diff_str = f"{diff:+.2f}%" if diff != float('inf') else 'N/A'

        # Format waarden
        orig_str = format_str.format(orig_val)
        enh_str = format_str.format(enh_val)

        print(f"{name:<25} {orig_str:<15} {enh_str:<15} {diff_str:<15}")

    # Plot vergelijkende equity curves
    if not original_trades.empty and not enhanced_trades.empty:
        plot_comparative_equity(symbol, original_trades, enhanced_trades)


def plot_comparative_equity(symbol, original_trades, enhanced_trades):
    """
    Plot vergelijkende equity curves

    Parameters:
    -----------
    symbol : str
        Het handelssymbool
    original_trades : pandas.DataFrame
        Trades van originele strategie
    enhanced_trades : pandas.DataFrame
        Trades van verbeterde strategie
    """
    # Bereken cumulatieve P&L voor beide strategieën
    if 'pnl' not in original_trades.columns or 'pnl' not in enhanced_trades.columns:
        return

    # Initiële balans
    initial_balance = 100000

    # Bereken equity curves
    original_equity = calculate_equity_curve(original_trades, initial_balance)
    enhanced_equity = calculate_equity_curve(enhanced_trades, initial_balance)

    # Plot vergelijkende equity curves
    plt.figure(figsize=(14, 7))

    plt.plot(original_equity['date'], original_equity['equity'], label='Originele Strategie')
    plt.plot(enhanced_equity['date'], enhanced_equity['equity'], label='Verbeterde Strategie')

    plt.title(f'Vergelijking Equity Curves - {symbol}')
    plt.xlabel('Datum')
    plt.ylabel('Account Equity ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Sla grafiek op
    output_dir = os.path.join(project_dir, 'test_results', symbol)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{symbol}_comparison.png"))

    plt.show()


def calculate_equity_curve(trades_df, initial_balance):
    """
    Bereken equity curve op basis van trades

    Parameters:
    -----------
    trades_df : pandas.DataFrame
        DataFrame met trades
    initial_balance : float
        Initiële account balans

    Returns:
    --------
    pandas.DataFrame
        DataFrame met equity curve
    """
    if trades_df.empty or 'pnl' not in trades_df.columns:
        return pd.DataFrame({'date': [], 'equity': []})

    # Sorteer trades op exit_time
    if 'exit_time' in trades_df.columns:
        trades_df = trades_df.sort_values('exit_time')

    # Maak equity curve
    equity = initial_balance
    equity_points = [{'date': trades_df['entry_time'].min(), 'equity': equity}]

    for _, trade in trades_df.iterrows():
        if 'pnl' in trade and pd.notna(trade['pnl']):
            equity += trade['pnl']
            if 'exit_time' in trade and pd.notna(trade['exit_time']):
                equity_points.append({'date': trade['exit_time'], 'equity': equity})

    return pd.DataFrame(equity_points)


def timeframe_to_string(timeframe):
    """Converteer MT5 timeframe constante naar string"""
    timeframes = {
        mt5.TIMEFRAME_M1: "M1",
        mt5.TIMEFRAME_M5: "M5",
        mt5.TIMEFRAME_M15: "M15",
        mt5.TIMEFRAME_M30: "M30",
        mt5.TIMEFRAME_H1: "H1",
        mt5.TIMEFRAME_H4: "H4",
        mt5.TIMEFRAME_D1: "D1",
        mt5.TIMEFRAME_W1: "W1",
        mt5.TIMEFRAME_MN1: "MN1"
    }
    return timeframes.get(timeframe, f"Unknown ({timeframe})")


if __name__ == "__main__":
    # Definieer test parameters
    symbol = "XAUUSD"  # of "EURUSD", "US30", etc.
    timeframe = mt5.TIMEFRAME_H4
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 jaar data
    risk_per_trade = 0.01  # 1% risico per trade

    # Voer test uit
    run_comparative_test(symbol, timeframe, start_date, end_date, risk_per_trade)