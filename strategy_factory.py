# sophy/strategy_factory.py
from typing import Dict, Optional

from sophy.core.connector import MT5Connector
from sophy.core.risk_manager import RiskManager
from sophy.strategies.turtle_trader.strategy import TurtleStrategy


# Toekomstige import: from sophy.strategies.dax_opener.strategy import DAXOpenerStrategy

def create_strategy(strategy_name: str, connector: MT5Connector, risk_manager: RiskManager,
                    logger, config: Dict) -> Optional['Strategy']:
    """
    Factory functie om de juiste strategie-instance te maken

    Parameters:
    -----------
    strategy_name : str
        Naam van de te maken strategie
    connector : MT5Connector
        Connector naar handelsplatform
    risk_manager : RiskManager
        Risicomanagement component
    logger :
        Logger instance
    config : Dict
        Configuratie voor de strategie

    Returns:
    --------
    Strategy : De gecreëerde strategie of None als de strategie niet gevonden is
    """
    # Strategy mapping
    strategies = {
        'turtle_trader': TurtleStrategy,
        # Toekomstige strategie: 'dax_opener': DAXOpenerStrategy,
    }

    # Haal de strategieklasse op
    strategy_class = strategies.get(strategy_name.lower())

    if strategy_class is None:
        logger.error(f"Ongeldige strategienaam: {strategy_name}")
        return None

    # Maak en return de strategie
    return strategy_class(connector, risk_manager, logger, config)