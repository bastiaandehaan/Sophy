# main.py
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
from modules.strategies.enhanced_turtle_strategy import EnhancedTurtleStrategy
from modules.risk_manager import RiskManager
from modules.backtester import Backtester
from utils.logger import Logger


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
    print(f"TurtleTrader bot gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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

    # Initialiseer risicomanager
    risk_manager = RiskManager(
        max_risk_per_trade=config['mt5']['risk_per_trade'],
        max_daily_drawdown=0.05,  # 5% maximale dagelijkse drawdown
        max_total_drawdown=0.1,  # 10% maximale totale drawdown
        leverage=config['mt5'].get('leverage', 1)
    )

    # Vraag welke strategie te gebruiken
    print("\nKies een strategie:")
    print("1. Originele Turtle Strategy")
    print("2. Verbeterde Turtle Strategy")

    strategy_choice = input("Keuze (1/2): ")

    # Initialiseer de gekozen strategie
    if strategy_choice == "2":
        print("Verbeterde Turtle Strategy gekozen")
        strategy = EnhancedTurtleStrategy(
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config
        )
    else:
        print("Originele Turtle Strategy gekozen")
        strategy = TurtleStrategy(
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config
        )

    # Hoofdlus
    try:
        while True:
            print(f"Verwerking cyclus gestart op {datetime.now().strftime('%H:%M:%S')}")
            for symbol in config['mt5']['symbols']:
                print(f"Verwerking {symbol}...")
                strategy.process_symbol(symbol)

            # Log status
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions()
            logger.log_status(account_info, open_positions)

            # Summary printen naar console
            print(f"Status: Balance={account_info.get('balance', 'N/A')}, Equity={account_info.get('equity', 'N/A')}")
            print(f"Wachten voor volgende cyclus...")

            # Wacht voordat we de volgende cyclus starten
            time.sleep(60)  # Check elke minuut

    except KeyboardInterrupt:
        print("Bot gestopt door gebruiker.")
    except Exception as e:
        print(f"Onverwachte fout: {e}")
        import traceback
        traceback.print_exc()
    finally:
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

        # Test data ophalen voor één symbool
        symbol = config['mt5']['symbols'][0]
        print(f"Data ophalen voor {symbol}...")
        df = connector.get_historical_data(symbol, mt5.TIMEFRAME_H4, 10)
        if not df.empty:
            print(f"✅ Data succesvol opgehaald voor {symbol}")
            print(df.tail(3))
        else:
            print(f"❌ Geen data opgehaald voor {symbol}")
    else:
        print("❌ Kon geen verbinding maken met MT5")

    # Verbreek verbinding
    connector.disconnect()
    print("Test afgerond.")


def run_backtest():
    """Voer een backtest uit van de trading strategie"""
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

        # Vraag om strategie keuze
        print("\nKies een strategie om te testen:")
        print("1. Originele Turtle Strategy")
        print("2. Verbeterde Turtle Strategy")
        print("3. Vergelijk beide strategieën")

        choice = input("Keuze (1/2/3): ")

        # Definieer test periode
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Standaard 1 jaar

        # Vraag naar aangepaste testperiode
        custom_period = input("Aangepaste testperiode? (j/n): ").lower()
        if custom_period == 'j':
            try:
                years = int(input("Aantal jaren terug: "))
                start_date = end_date - timedelta(days=365 * years)
            except ValueError:
                print("Ongeldige invoer, gebruik standaard 1 jaar.")

        print(f"Backtest periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Loop door symbolen of selecteer specifiek symbool
        symbols = config['mt5']['symbols'].copy()
        if len(symbols) > 1:
            print("\nKies een symbool:")
            for i, sym in enumerate(symbols, 1):
                print(f"{i}. {sym}")
            print(f"{len(symbols) + 1}. Alle symbolen")

            sym_choice = input(f"Keuze (1-{len(symbols) + 1}): ")
            try:
                sym_idx = int(sym_choice) - 1
                if 0 <= sym_idx < len(symbols):
                    symbols = [symbols[sym_idx]]
                elif sym_idx != len(symbols):
                    print("Ongeldige keuze, alle symbolen worden getest.")
            except ValueError:
                print("Ongeldige invoer, alle symbolen worden getest.")

        # Voer backtest(s) uit
        if choice == "1" or choice == "3":
            # Test Originele Turtle Strategy
            for symbol in symbols:
                results_df, trades_df, stats = backtester.run_backtest(
                    symbol=symbol,
                    strategy_class=TurtleStrategy,
                    start_date=start_date,
                    end_date=end_date
                )

                if results_df is not None:
                    backtester.plot_results(
                        results_df, trades_df, stats, symbol,
                        f"{symbol}_original_results.png"
                    )

        if choice == "2" or choice == "3":
            # Test Verbeterde Turtle Strategy
            for symbol in symbols:
                results_df, trades_df, stats = backtester.run_backtest(
                    symbol=symbol,
                    strategy_class=EnhancedTurtleStrategy,
                    start_date=start_date,
                    end_date=end_date
                )

                if results_df is not None:
                    backtester.plot_results(
                        results_df, trades_df, stats, symbol,
                        f"{symbol}_enhanced_results.png"
                    )

        # Optioneel: vergelijk resultaten van beide strategieën
        if choice == "3" and backtester.metrics:
            compare_strategies(backtester.metrics)

    except Exception as e:
        print(f"Fout tijdens backtesting: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connector.disconnect()
        print("Backtesting voltooid")


def compare_strategies(metrics):
    """
    Vergelijk de resultaten van verschillende strategieën

    Parameters:
    -----------
    metrics : dict
        Dictionary met metriek per strategie per symbool
    """
    print("\n" + "=" * 50)
    print("VERGELIJKING VAN STRATEGIEËN")
    print("=" * 50)

    # Toon tabel met resultaten per strategie en symbool
    headers = ["Symbool", "Strategie", "Trades", "Win%", "Profit Factor", "Rendement"]
    print(f"{headers[0]:<8} {headers[1]:<20} {headers[2]:<8} {headers[3]:<8} {headers[4]:<15} {headers[5]:<10}")
    print("-" * 70)

    # TODO: Implementeer vergelijking tussen TurtleStrategy en EnhancedTurtleStrategy


if __name__ == "__main__":
    print("\n==== TurtleTrader Menu ====")
    print("1. Start Live Trading")
    print("2. Run Connection Test")
    print("3. Run Backtest")
    print("0. Exit")

    choice = input("\nKies een optie: ")

    if choice == "1":
        main()
    elif choice == "2":
        test_connection()
    elif choice == "3":
        run_backtest()
    elif choice == "0":
        print("Programma afgesloten")
    else:
        print("Ongeldige keuze")