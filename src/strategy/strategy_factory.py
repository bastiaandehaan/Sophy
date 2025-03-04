# src/strategy/strategy_factory.py
from typing import Dict, Type, Optional

from src.strategy.base_strategy import BaseStrategy
from src.strategy.turtle_strategy import TurtleStrategy


def create_strategy(strategy_name: str, connector, risk_manager, logger, config) -> Optional[BaseStrategy]:
    """Create an instance of the requested strategy"""
    # Strategy mapping
    strategies = {
        "turtle": TurtleStrategy,
        "turtle_swing": TurtleStrategy,  # With different configuration
        # Add more strategies here when needed
    }

    if strategy_name not in strategies:
        logger.log_info(f"Unknown strategy: {strategy_name}", level="ERROR")
        return None

    strategy_class = strategies[strategy_name]

    # Apply special configuration if needed
    if strategy_name == "turtle_swing":
        config['strategy']['swing_mode'] = True

    try:
        return strategy_class(connector, risk_manager, logger, config)
    except Exception as e:
        logger.log_info(f"Error creating strategy: {e}", level="ERROR")
        return None


def list_available_strategies() -> list:
    """Return a list of available strategies"""
    return ["turtle", "turtle_swing"]