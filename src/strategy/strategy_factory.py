# src/strategy/strategy_factory.py
from typing import Dict, Type, Any

from src.strategy.base_strategy import BaseStrategy
from src.strategy.turtle_strategy import TurtleStrategy


class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies: Dict[str, Type[BaseStrategy]] = {
        "turtle": TurtleStrategy,
        "turtle_swing": TurtleStrategy,  # Met andere configuratie
        # Voeg hier meer strategieën toe wanneer nodig
    }

    @classmethod
    def create_strategy(cls, strategy_name: str, connector, risk_manager, logger, config) -> BaseStrategy:
        """
        Creëert een instance van de gevraagde strategie

        Args:
            strategy_name: Naam van de strategie
            connector: MT5 connector instantie
            risk_manager: Risk manager instantie
            logger: Logger instantie
            config: Configuratieobject

        Returns:
            Een instantie van de gevraagde strategie

        Raises:
            ValueError: Als de strategie niet bestaat
        """
        if strategy_name not in cls._strategies:
            raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Pas speciale configuratie toe als nodig
        if strategy_name == "turtle_swing":
            config['mt5']['swing_mode'] = True

        return strategy_class(connector, risk_manager, logger, config)

    @classmethod
    def list_available_strategies(cls) -> list:
        """Geeft een lijst van beschikbare strategieën"""
        return list(cls._strategies.keys())