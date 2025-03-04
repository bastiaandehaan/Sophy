# main.py
import time

from sophy.core.config import load_config
from sophy.core.connector import MT5Connector
from sophy.core.risk_manager import RiskManager
from sophy.strategy_factory import create_strategy
from sophy.utils.logger import setup_logger


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Laad configuratie
    config = load_config()

    # Setup logging
    logger = setup_logger()
    logger.info("====== Sophy Trading System ======")

    # Creëer componenten
    connector = MT5Connector(config['mt5'], logger)
    risk_manager = RiskManager(config['risk'], logger)

    # Verbind met MT5
    if not connector.connect():
        logger.error("Kon geen verbinding maken met MT5. Programma wordt afgesloten.")
        return

    logger.info(f"Verbonden met MT5: {config['mt5']['server']}")

    # Haal strategie naam uit config
    strategy_name = config['strategy']['name']

    # Creëer strategie via factory
    strategy = create_strategy(strategy_name, connector, risk_manager, logger, config)

    if strategy is None:
        logger.error(f"Kon strategie '{strategy_name}' niet initialiseren. Programma wordt afgesloten.")
        return

    logger.info(f"Strategie geladen: {strategy.get_name()}")

    # Hoofdloop
    try:
        while True:
            # Verwerk symbolen volgens strategie
            for symbol in config['mt5']['symbols']:
                # Pas symbol mapping toe indien nodig
                symbol_map = config['mt5'].get('symbol_mapping', {})
                mapped_symbol = symbol_map.get(symbol, symbol)

                # Verwerk symbool
                results = strategy.process_symbol(mapped_symbol)

                # Log resultaten indien nodig
                if results.get('signal'):
                    logger.info(f"Signaal voor {mapped_symbol}: {results['signal']}")

            # Controleer FTMO limieten
            account_info = connector.get_account_info()
            should_stop, reason = risk_manager.check_ftmo_limits(account_info)

            if should_stop:
                logger.info(f"Stop trading: {reason}")
                break

            # Wacht voor volgende cyclus
            time.sleep(300)  # 5 minuten

    except KeyboardInterrupt:
        logger.info("Trading gestopt door gebruiker.")
    finally:
        # Cleanup
        connector.disconnect()
        logger.info("Sessie afgesloten.")


if __name__ == "__main__":
    main()