#!/usr/bin/env python3
# run.py
"""
Sophy Trading System - Hoofdscript

Dit script start het Sophy trading systeem in live of backtest modus
en zorgt voor de integratie van alle componenten.
"""
import argparse
import os
import sys
import time
from datetime import datetime


def setup_environment():
    """Zet de omgeving op voor het uitvoeren van de applicatie"""
    # Voeg de huidige directory toe aan het pythonpath
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Maak log directory aan indien nodig
    log_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Maak data directory aan indien nodig
    data_dir = os.path.join(script_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def parse_arguments():
    """Parse command line arguments met uitgebreide opties"""
    parser = argparse.ArgumentParser(description="Sophy Trading System")
    parser.add_argument("--config", type=str, help="Pad naar configuratiebestand")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["live", "backtest", "paper"],
        default="backtest",
        help="Trading modus (default: backtest)",
    )
    parser.add_argument("--strategy", type=str, help="Te gebruiken strategie")
    parser.add_argument(
        "--symbols", type=str, help="Komma-gescheiden lijst van symbolen"
    )
    parser.add_argument("--interval", type=int, help="Update interval in seconden")
    parser.add_argument(
        "--initial_balance", type=float, help="Initiële account balans voor backtest"
    )
    parser.add_argument(
        "--swing", action="store_true", help="Gebruik swing modus voor Turtle strategie"
    )
    parser.add_argument(
        "--start_date", type=str, help="Startdatum voor backtest (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end_date", type=str, help="Einddatum voor backtest (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--optimize", action="store_true", help="Voer parameteroptimalisatie uit"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Valideer FTMO compliance"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Genereer visualisaties na afloop"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Toon gedetailleerde log output"
    )

    return parser.parse_args()


def load_config(config_path=None):
    """Laad configuratie met mogelijkheid tot pad-override"""
    from src.utils.config import load_config as load_config_util

    try:
        return load_config_util(config_path)
    except Exception as e:
        print(f"Fout bij laden configuratie: {e}")
        sys.exit(1)


def create_logger(config):
    """Maak logger instance gebaseerd op configuratie"""
    from src.utils.logger import Logger

    log_file = config["logging"].get("log_file", "logs/trading_log.csv")
    return Logger(log_file)


def run_backtest(config, args, logger):
    """Voer backtesting uit met opgegeven configuratie"""
    print(f"Starten in backtest modus - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Gewijzigd: Import de correcte bestaande backtest module
        from src.analysis.backtrader_integration import BacktestingManager

        # Override config met command line argumenten
        if args.symbols:
            config["mt5"]["symbols"] = args.symbols.split(",")
        if args.initial_balance:
            config["mt5"]["account_balance"] = args.initial_balance
        if args.strategy:
            config["strategy"]["name"] = args.strategy
        if args.swing:
            config["strategy"]["swing_mode"] = True
        if args.start_date or args.end_date:
            if "backtest" not in config:
                config["backtest"] = {}
            if args.start_date:
                config["backtest"]["start_date"] = args.start_date
            if args.end_date:
                config["backtest"]["end_date"] = args.end_date

        # Log configuratie
        logger.log_info(
            f"Backtest configuratie: strategie={config['strategy']['name']}, "
            f"symbolen={config['mt5']['symbols']}"
        )

        # Maak backtesting manager en voer backtest uit
        btm = BacktestingManager(config, logger)

        # Bepaal parameters voor backtest
        strategy_name = config['strategy']['name']
        symbols = config['mt5']['symbols']
        timeframe = config.get('timeframe',
                               config.get('mt5', {}).get('timeframe', 'D1'))
        start_date = config.get('backtest', {}).get('start_date', '2020-01-01')
        end_date = config.get('backtest', {}).get('end_date',
                                                  datetime.now().strftime('%Y-%m-%d'))

        # Voer backtest uit
        results = btm.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            timeframe=timeframe,
            plot_results=args.visualize
        )

        # Voer FTMO validatie uit indien gewenst
        if args.validate:
            from src.ftmo.ftmo_validator import FTMOValidator

            validator = FTMOValidator(config, logger.log_file, logger=logger)
            validator.generate_trading_report()
            logger.log_info("FTMO validatie rapport gegenereerd")

        # Genereer visualisaties indien gewenst
        if args.visualize:
            from src.utils.visualizer import Visualizer

            visualizer = Visualizer(logger.log_file)
            visualizer.plot_equity_curve()
            visualizer.plot_trade_results()
            visualizer.plot_performance_summary()
            logger.log_info("Visualisaties gegenereerd")

        print("Backtest voltooid")

    except Exception as e:
        logger.log_info(f"Fout tijdens backtest: {str(e)}", level="ERROR")
        print(f"Fout tijdens backtest: {str(e)}")
        return False

    return True


def run_live_trading(config, args, logger):
    """Start live trading met opgegeven configuratie"""
    print(
        f"Starten in live trading modus - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        from src.connector.mt5_connector import MT5Connector
        from src.risk.risk_manager import RiskManager
        from src.strategy.strategy_factory import StrategyFactory

        # Override config met command line argumenten
        if args.symbols:
            config["mt5"]["symbols"] = args.symbols.split(",")
        if args.strategy:
            config["strategy"]["name"] = args.strategy
        if args.swing:
            config["strategy"]["swing_mode"] = True
        if args.interval:
            config["interval"] = args.interval

        # Log configuratie
        logger.log_info(
            f"Live trading configuratie: strategie={config['strategy']['name']}, "
            f"symbolen={config['mt5']['symbols']}"
        )

        # Maak componenten aan
        connector = MT5Connector(config["mt5"], logger)
        risk_manager = RiskManager(config["risk"], logger, connector)

        # Maak verbinding met MT5
        if not connector.connect():
            logger.log_info("Kan geen verbinding maken met MT5", level="ERROR")
            return False

        # Creëer strategie
        strategy_name = config["strategy"]["name"]
        try:
            strategy = StrategyFactory.create_strategy(
                strategy_name, connector, risk_manager, logger, config
            )
        except ValueError as e:
            logger.log_info(
                f"Kan strategie '{strategy_name}' niet maken: {e}", level="ERROR"
            )
            connector.disconnect()
            return False

        # Start trading loop
        logger.log_info("Trading loop gestart")

        stop_trading = False
        while not stop_trading:
            try:
                # Verwerk alle symbolen
                for symbol in config["mt5"]["symbols"]:
                    # Pas symbol mapping toe indien nodig
                    symbol_map = config["mt5"].get("symbol_mapping", {})
                    mapped_symbol = symbol_map.get(symbol, symbol)

                    # Verwerk symbool volgens strategie
                    result = strategy.process_symbol(mapped_symbol)

                    if result.get("signal"):
                        logger.log_info(
                            f"Signaal voor {mapped_symbol}: {result['signal']} {result.get('action', '')}"
                        )

                # Controleer account status en FTMO limieten
                account_info = connector.get_account_info()
                positions = strategy.get_open_positions()
                logger.log_status(account_info, positions)

                should_stop, reason = risk_manager.check_ftmo_limits(account_info)
                if should_stop:
                    logger.log_info(f"Trading gestopt: {reason}")
                    break

                # Wacht tot volgende cyclus
                interval = config.get("interval", 300)  # Default 5 minuten
                logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
                time.sleep(interval)

            except KeyboardInterrupt:
                logger.log_info("Trading gestopt door gebruiker")
                stop_trading = True
            except Exception as e:
                logger.log_info(f"Fout in trading loop: {str(e)}", level="ERROR")
                # Bij ernstige fouten, stop trading
                if "MT5 connection" in str(e):
                    stop_trading = True

        # Cleanup
        connector.disconnect()
        logger.log_info("Trading sessie afgesloten")

    except Exception as e:
        logger.log_info(f"Fout tijdens live trading: {str(e)}", level="ERROR")
        print(f"Fout tijdens live trading: {str(e)}")
        return False

    return True


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Setup
    setup_environment()

    # Parse arguments
    args = parse_arguments()

    # Stel config pad in indien opgegeven
    config_path = args.config
    if config_path and not os.path.exists(config_path):
        print(f"Waarschuwing: Opgegeven configuratiebestand {config_path} bestaat niet")
        config_path = None

    # Laad configuratie
    config = load_config(config_path)

    # Maak logger
    logger = create_logger(config)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Opgestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Bepaal modus en start juiste functie
    mode = args.mode.lower()

    if mode == "backtest":
        success = run_backtest(config, args, logger)
    elif mode in ("live", "paper"):
        success = run_live_trading(config, args, logger)
    else:
        logger.log_info(f"Onbekende modus: {mode}", level="ERROR")
        success = False

    # Afsluiten
    logger.log_info(
        f"Sophy Trading System afgesloten - Status: {'Succes' if success else 'Fout'}"
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramma onderbroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\nOnverwachte fout: {str(e)}")
        sys.exit(1)
