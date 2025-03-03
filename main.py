import time
import sys
import os
import json
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import matplotlib.pyplot as plt

# Importeer modules
from modules.mt5_connector import MT5Connector
from modules.strategies.turtle_strategy import TurtleStrategy
from modules.risk_manager import RiskManager
from modules.backtester import Backtester
from utils.logger import Logger
from utils.visualizer import Visualizer


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


def main():
    """Hoofdfunctie van de tradingbot"""
    print(f"Starting TurtleTrader bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Laad configuratie
    config_path = os.path.join('config', 'turtle_settings.json')
    config = load_config(config_path)

    # Initialiseer componenten
    connector = MT5Connector(config['mt5'])
    if not connector.connect():
        print("Kon geen verbinding maken met MT5. Bot stopt.")
        return

    # Initialiseer logger
    log_dir = os.path.join('logs')
    os.makedirs(log_dir, exist_ok=True)
    logger = Logger(os.path.join(log_dir, 'trading_journal.csv'))

    # Initialiseer risicomanager met de leverage parameter
    risk_manager = RiskManager(
        max_risk_per_trade=config['mt5']['risk_per_trade'],
        max_daily_drawdown=0.05,  # 5% maximale dagelijkse drawdown
        max_total_drawdown=0.1,  # 10% maximale totale drawdown
        leverage=config['mt5'].get('leverage', 30)  # Gebruik leverage uit config, standaard 30 voor FTMO Swing
    )

    # Initialiseer strategie
    strategy = TurtleStrategy(
        connector=connector,
        risk_manager=risk_manager,
        logger=logger,
        config=config
    )

    # Initialiseer visualizer
    visualizer = Visualizer(os.path.join(log_dir, 'trading_journal.csv'), 'data')

    # Toon configuratie-instellingen
    print("\n=== Configuratie ===")
    print(f"Symbolen: {', '.join(config['mt5']['symbols'])}")
    print(f"Timeframe: {config['mt5'].get('timeframe', 'H4')}")
    print(f"FTMO Swing Mode: {'Ingeschakeld' if config['mt5'].get('swing_mode', False) else 'Uitgeschakeld'}")
    print(f"Leverage: 1:{config['mt5'].get('leverage', 30)}")
    print(f"Risico per trade: {config['mt5']['risk_per_trade'] * 100:.1f}%")
    print(f"Max. dagelijkse drawdown: 5%")
    print(f"Max. totale drawdown: 10%")
    print("===================\n")

    # Hoofdlus
    try:
        # Loop teller voor periodic checks
        cycle_count = 0

        while True:
            cycle_time = datetime.now()
            print(f"\nVerwerking cyclus #{cycle_count + 1} gestart op {cycle_time.strftime('%H:%M:%S')}")

            # Check account status en FTMO limieten
            stop_trading, reason = strategy.check_daily_limit()
            if stop_trading:
                logger.log_info(f"Trading gestopt: {reason}", level="WARNING")
                print(f"\n⚠️ TRADING GESTOPT: {reason}")
                print("Bot zal blijven draaien voor monitoring, maar geen nieuwe trades openen.")

                # Toon huidige equity curve
                visualizer.plot_equity_curve()

                # Blijf draaien voor monitoring zonder te traden
                while True:
                    time.sleep(300)  # Check elke 5 minuten
                    account_info = connector.get_account_info()
                    open_positions = strategy.get_open_positions()
                    logger.log_status(account_info, open_positions)
                    print(
                        f"Monitoring: Balance={account_info.get('balance', 'N/A')}, Equity={account_info.get('equity', 'N/A')}")

            # Verwerk symbolen
            for symbol in config['mt5']['symbols']:
                print(f"Verwerking {symbol}...")
                strategy.process_symbol(symbol)

            # Log status
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions()
            logger.log_status(account_info, open_positions)

            # Summary printen naar console
            print(f"Status: Balance={account_info.get('balance', 'N/A')}, Equity={account_info.get('equity', 'N/A')}")

            # Verhoog cycle counter
            cycle_count += 1

            # Periodieke visualisatie (elke 10 cycli)
            if cycle_count % 10 == 0:
                print("Periodieke analyse uitvoeren...")
                visualizer.plot_equity_curve()
                visualizer.plot_trade_results()

            # Bereken wachttijd tot volgende cyclus
            elapsed = (datetime.now() - cycle_time).total_seconds()
            wait_time = max(60 - elapsed, 5)  # Minimaal 5 seconden wachten

            print(f"Wachten voor volgende cyclus: {wait_time:.0f} seconden...")
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\nBot gestopt door gebruiker.")
    except Exception as e:
        print(f"Onverwachte fout: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Laatste visualisaties bijwerken bij afsluiten
        try:
            visualizer.plot_equity_curve()
            visualizer.plot_trade_results()
            visualizer.plot_performance_summary()
        except Exception as viz_error:
            print(f"Kon visualisaties niet genereren bij afsluiten: {viz_error}")

        connector.disconnect()
        print("Bot gestopt en verbinding gesloten.")


def test_connection():
    """Test alleen de verbinding met MT5"""
    print("Test verbinding met MT5...")
    config_path = os.path.join('config', 'turtle_settings.json')
    config = load_config(config_path)

    connector = MT5Connector(config['mt5'])
    connected = connector.connect()

    if connected:
        print("✅ Verbinding met MT5 succesvol!")
        account_info = connector.get_account_info()
        print(f"Account balans: {account_info.get('balance', 'Onbekend')}")
        print(f"Account equity: {account_info.get('equity', 'Onbekend')}")
        print(f"Account leverage: 1:{account_info.get('leverage', 'Onbekend')}")

        # Test data ophalen voor één symbool
        symbol = config['mt5']['symbols'][0]
        print(f"Data ophalen voor {symbol}...")

        # Gebruik timeframe uit config
        timeframe_str = config['mt5'].get('timeframe', 'H4')
        timeframe = connector.get_timeframe_constant(timeframe_str)

        df = connector.get_historical_data(symbol, timeframe, 10)
        if not df.empty:
            print(f"✅ Data succesvol opgehaald voor {symbol} ({timeframe_str})")
            print(df.tail(3))
        else:
            print(f"❌ Geen data opgehaald voor {symbol}")
    else:
        print("❌ Kon geen verbinding maken met MT5")

    # Verbreek verbinding
    connector.disconnect()
    print("Test afgerond.")


def run_backtest():
    """Voer een backtest uit van de Turtle Trading strategie"""
    print("Backtesting module gestart...")

    # Laad configuratie
    config_path = os.path.join('config', 'turtle_settings.json')
    config = load_config(config_path)

    # Initialiseer connector
    connector = MT5Connector(config['mt5'])
    if not connector.connect():
        print("Kon geen verbinding maken met MT5. Backtest gestopt.")
        return

    try:
        # Initialiseer backtester
        backtester = Backtester(connector, config)

        # Definieer test periode
        end_date = datetime.now()
        period_choice = input("Backtest periode (1=1 maand, 3=3 maanden, 6=6 maanden, 12=1 jaar, 24=2 jaar): ")
        try:
            months = int(period_choice)
            if months not in [1, 3, 6, 12, 24]:
                months = 6  # Default 6 maanden
        except ValueError:
            months = 6  # Default bij ongeldige invoer

        start_date = end_date - timedelta(days=30 * months)  # 30 dagen per maand

        print(f"Backtest periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Bepaal juiste timeframe uit config
        timeframe_str = config['mt5'].get('timeframe', 'H4')
        timeframe = connector.get_timeframe_constant(timeframe_str)

        # Test elke individuele strategie (testen per symbool)
        for symbol in config['mt5']['symbols']:
            print(f"\nBacktesting strategie op {symbol}...")

            # Pas parameters aan voor FTMO Swing mode
            custom_params = {
                'entry_period': 40 if config['mt5'].get('swing_mode', False) else 20,
                'exit_period': 20 if config['mt5'].get('swing_mode', False) else 10,
                'atr_period': 20,
                'atr_multiplier': 2.5 if config['mt5'].get('swing_mode', False) else 2.0,
                'risk_per_trade': config['mt5']['risk_per_trade'],
                'use_trend_filter': True
            }

            # Voer backtest uit en geef correcte parameters door
            result_df = backtester.run_backtest(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                timeframe=timeframe,
                params=custom_params
            )

            if result_df is not None:
                # Plot resultaten
                backtester.plot_results(result_df, symbol, f"{symbol}_backtest_results.png")

        # Optioneel: parameter optimalisatie
        if input("Wil je parameter optimalisatie uitvoeren? (j/n): ").lower() == 'j':
            symbol = config['mt5']['symbols'][0]  # Kies een symbool voor optimalisatie
            print(f"\nParameter optimalisatie voor {symbol}...")

            # Aangepast parameter grid voor FTMO Swing
            if config['mt5'].get('swing_mode', False):
                param_grid = {
                    'entry_period': [30, 40, 50, 60],
                    'exit_period': [15, 20, 25, 30],
                    'atr_multiplier': [2.0, 2.5, 3.0, 3.5],
                    'use_trend_filter': [True]
                }
            else:
                param_grid = {
                    'entry_period': [10, 20, 30, 40],
                    'exit_period': [5, 10, 15, 20],
                    'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
                    'use_trend_filter': [True, False]
                }

            # Start optimalisatie
            best_params = backtester.optimize_parameters(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                param_grid=param_grid
            )

            # Test de beste parameters
            print("\nTesten van beste parameters...")
            result_df = backtester.run_backtest(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                timeframe=timeframe,
                params=best_params['best_return_params']
            )
            backtester.plot_results(result_df, symbol, f"{symbol}_optimized_backtest.png")

    except Exception as e:
        print(f"Fout tijdens backtesting: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connector.disconnect()
        print("Backtesting voltooid")


def analyze_performance():
    """Analyseer trading performance en genereer grafieken"""
    print("Performance analyse gestart...")

    # Controleer of logs bestaan
    log_file = os.path.join('logs', 'trading_journal.csv')
    if not os.path.exists(log_file):
        print(f"Log bestand niet gevonden: {log_file}")
        print("Voer eerst de bot uit om logs te genereren.")
        return

    # Initialiseer visualizer
    visualizer = Visualizer(log_file, 'data/analysis')

    try:
        # Genereer alle beschikbare visualisaties
        print("Genereren van equity curve...")
        equity_path = visualizer.plot_equity_curve()

        print("Genereren van trades overzicht...")
        trades_path = visualizer.plot_trade_results()

        print("Genereren van performance samenvatting...")
        summary_path = visualizer.plot_performance_summary()

        print("\nAnalyse voltooid. Grafieken opgeslagen in de 'data/analysis' map:")
        if equity_path:
            print(f"- Equity curve: {os.path.basename(equity_path)}")
        if trades_path:
            print(f"- Trades overzicht: {os.path.basename(trades_path)}")
        if summary_path:
            print(f"- Performance samenvatting: {os.path.basename(summary_path)}")

    except Exception as e:
        print(f"Fout tijdens analyse: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n==== TurtleTrader FTMO Swing Edition ====")
    print("1. Start Live Trading")
    print("2. Run Connection Test")
    print("3. Run Backtest")
    print("4. Analyze Performance")
    print("0. Exit")

    choice = input("\nKies een optie: ")

    if choice == "1":
        main()
    elif choice == "2":
        test_connection()
    elif choice == "3":
        run_backtest()
    elif choice == "4":
        analyze_performance()
    elif choice == "0":
        print("Programma afgesloten")
    else:
        print("Ongeldige keuze")