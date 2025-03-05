# run.py
# !/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime


def setup_environment():
    """Zet de omgeving op voor het uitvoeren van de applicatie"""
    # Voeg de huidige directory toe aan het pythonpath
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Sophy Trading Bot')
    parser.add_argument('--config', type=str, help='Pad naar configuratiebestand')
    parser.add_argument('--backtest', action='store_true', help='Voer backtest uit in plaats van live trading')
    parser.add_argument('--strategy', type=str, help='Te gebruiken strategie')
    parser.add_argument('--symbols', type=str, help='Komma-gescheiden lijst van symbolen')

    return parser.parse_args()


def main():
    """Main entry point for the application"""
    print(f"Sophy Trading Bot - Gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup environment
    setup_environment()

    # Parse arguments
    args = parse_arguments()

    # Set config path if provided
    if args.config:
        os.environ['SOPHY_CONFIG_PATH'] = args.config
        print(f"Gebruik configuratiebestand: {args.config}")

    # Override strategy if provided
    if args.strategy:
        print(f"Overschrijven strategie: {args.strategy}")
        # Dit wordt later in het programma verwerkt

    # Override symbols if provided
    if args.symbols:
        symbols = args.symbols.split(',')
        print(f"Overschrijven symbolen: {symbols}")
        # Dit wordt later in het programma verwerkt

    # Run in backtest mode or live mode
    if args.backtest:
        print("Starten in backtest modus")
        from src.analysis.backtester import run_backtest
        run_backtest()
    else:
        print("Starten in live trading modus")
        from src.main import main as run_live
        run_live()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramma onderbroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\nOnverwachte fout: {str(e)}")
        sys.exit(1)