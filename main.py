import time
import sys
import os
import json
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import matplotlib.pyplot as plt

# Importeer modules
from modules.mt5_connector import MT5Connector
from modules.strategy import TurtleStrategy
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

    # Initialiseer risicomanager met de nieuwe leverage parameter
    risk_manager = RiskManager(
        max_risk_per_trade=config['mt5']['risk_per_trade'],
        max_daily_drawdown=0.05,  # 5% maximale dagelijkse drawdown
        max_total_drawdown=0.1,   # 10% maximale totale drawdown
        leverage=config['mt5'].get('leverage', 1)  # Haal leverage uit config, standaard 1
    )

    # Initialiseer strategie
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
        df = connector.get_historical_data(symbol, mt5.TIMEFRAME_D1, 10)
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

        # Definieer test periode (bijv. laatste 2 jaar)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 2)  # 2 jaar

        print(f"Backtest periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        # Test elke individuele strategie (testen per symbool)
        for symbol in config['mt5']['symbols']:
            print(f"\nBacktesting strategie op {symbol}...")
            result_df = backtester.run_backtest(symbol, start_date, end_date)

            if result_df is not None:
                # Plot resultaten
                backtester.plot_results(result_df, symbol, f"{symbol}_backtest_results.png")

        # Optioneel: parameter optimalisatie
        if input("Wil je parameter optimalisatie uitvoeren? (j/n): ").lower() == 'j':
            symbol = config['mt5']['symbols'][0]  # Kies een symbool voor optimalisatie
            print(f"\nParameter optimalisatie voor {symbol}...")

            # Start optimalisatie
            best_params = backtester.optimize_parameters(symbol, start_date, end_date)

            # Test de beste parameters
            print("\nTesten van beste parameters...")
            result_df = backtester.run_backtest(symbol, start_date, end_date, params=best_params['best_return_params'])
            backtester.plot_results(result_df, symbol, f"{symbol}_optimized_backtest.png")

    except Exception as e:
        print(f"Fout tijdens backtesting: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connector.disconnect()
        print("Backtesting voltooid")

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