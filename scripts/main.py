# src/main.py
import time
from datetime import datetime

from src.connector.mt5_connector import MT5Connector
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Laad configuratie
    config = load_config()

    # Setup logging
    log_file = config['logging'].get('log_file', 'logs/trading_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Sessie gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Creëer componenten
    connector = MT5Connector(config['mt5'], logger)
    risk_manager = RiskManager(config['risk'], logger)

    # Verbind met MT5
    if not connector.connect():
        logger.log_info("Kon geen verbinding maken met MT5. Programma wordt afgesloten.", level="ERROR")
        return

    logger.log_info(f"Verbonden met MT5: {config['mt5']['server']}")

    # Haal strategie naam uit config
    strategy_name = config['strategy']['name']

    # Creëer strategie via factory
    try:
        strategy = StrategyFactory.create_strategy(strategy_name, connector, risk_manager, logger, config)
        logger.log_info(f"Strategie geladen: {strategy_name}")
    except ValueError as e:
        logger.log_info(f"Kon strategie '{strategy_name}' niet initialiseren: {str(e)}", level="ERROR")
        connector.disconnect()
        return

    # Hoofdloop
    try:
        logger.log_info("Trading loop gestart")

        # Log initiële account status
        account_info = connector.get_account_info()
        open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
        logger.log_status(account_info, open_positions)

        while True:
            # Verwerk symbolen volgens strategie
            for symbol in config['mt5']['symbols']:
                # Pas symbol mapping toe indien nodig
                symbol_map = config['mt5'].get('symbol_mapping', {})
                mapped_symbol = symbol_map.get(symbol, symbol)

                # Verwerk symbool
                strategy.process_symbol(mapped_symbol)

            # Controleer FTMO limieten
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
            logger.log_status(account_info, open_positions)

            should_stop, reason = risk_manager.check_ftmo_limits(account_info)
            if should_stop:
                logger.log_info(f"Stop trading: {reason}")
                break

            # Wacht voor volgende cyclus
            interval = config.get('interval', 300)  # Default 5 minuten
            logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.log_info("Trading gestopt door gebruiker.")
    except Exception as e:
        logger.log_info(f"Onverwachte fout: {str(e)}", level="ERROR")
    finally:
        # Cleanup
        connector.disconnect()
        logger.log_info("Sessie afgesloten.")


if __name__ == "__main__":
    main()
