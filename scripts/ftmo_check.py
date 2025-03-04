import json
import os
import sys

from utils.ftmo_helper import FTMOHelper


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
    print("\n==== FTMO Compliance Checker ====")
    print("Dit programma controleert of je trading prestaties voldoen aan de FTMO regels.")

    # Controleer of logbestand bestaat
    log_file = os.path.join('../logs', 'trading_journal.csv')
    if not os.path.exists(log_file):
        print(f"\nError: Log bestand niet gevonden: {log_file}")
        print("Voer eerst de TurtleTrader bot uit om trading data te genereren.")
        return

    # Laad configuratie voor initiële balans
    config_path = os.path.join('Sophy/config', 'settings.json')
    try:
        config = load_config(config_path)
        initial_balance = config['mt5'].get('account_balance', 100000)
    except:
        print("\nWaarschuwing: Kon configuratie niet laden, standaard account balans van $100,000 wordt gebruikt.")
        initial_balance = 100000

    print(f"\nAnalyseren van trading data met initiële balans: ${initial_balance:,.2f}")

    # Initialiseer FTMO helper
    ftmo_helper = FTMOHelper(log_file)

    # Genereer rapport
    print("\nGenereren van gedetailleerd FTMO compliance rapport...")
    ftmo_helper.generate_trading_report(initial_balance)

    print("\nWil je nog meer details zien? (j/n): ", end="")
    if input().lower() == 'j':
        # Voer meer gedetailleerde analyse uit
        compliance = ftmo_helper.check_ftmo_compliance(initial_balance)

        if compliance['details']:
            details = compliance['details']
            daily_stats = details['daily_stats']

            print("\n===== Dagelijkse Statistieken =====")
            print(f"{'Datum':<12} {'Balance':<12} {'Dagelijkse P&L':<15} {'Drawdown':<12}")
            print("-" * 55)

            for _, row in daily_stats.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                balance = f"${row['close_balance']:,.2f}"
                daily_pnl = f"${row['daily_pnl']:,.2f} ({row['daily_pnl_pct']:.2f}%)"
                drawdown = f"{row['daily_drawdown']:.2f}%"

                print(f"{date_str:<12} {balance:<12} {daily_pnl:<15} {drawdown:<12}")

            print("\nAls je voldoet aan alle FTMO regels, kun je doorgaan naar de volgende fase!")

    print("\nBedankt voor het gebruiken van de FTMO Compliance Checker.")


if __name__ == "__main__":
    main()