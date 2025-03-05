from typing import Dict, Type, Optional
from src.strategy.base_strategy import BaseStrategy
from src.strategy.turtle_strategy import TurtleStrategy
import copy

class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies: Dict[str, Type[BaseStrategy]] = {
        "turtle": TurtleStrategy,
        "turtle_swing": TurtleStrategy,  # Met andere configuratie
        # Voeg hier meer strategieën toe wanneer nodig
    }

    @classmethod
    def create_strategy(
        cls,
        strategy_name: str,
        connector: Optional[object],  # Type afhankelijk van je connector-klasse
        risk_manager: Optional[object],  # Type afhankelijk van je risk_manager-klasse
        logger: Optional[object],  # Type afhankelijk van je logger-klasse
        config: Optional[dict]  # Type afhankelijk van je config-structuur
    ) -> BaseStrategy:
        """
        Creëert een instantie van de gevraagde strategie.

        Args:
            strategy_name (str): Naam van de strategie.
            connector: MT5 connector instantie.
            risk_manager: Risk manager instantie.
            logger: Logger instantie.
            config (dict): Configuratieobject.

        Returns:
            BaseStrategy: Een instantie van de gevraagde strategie.

        Raises:
            ValueError: Als de strategie niet bestaat.
        """
        if strategy_name not in cls._strategies:
            logger.log_error(f"Onbekende strategie: {strategy_name}") if logger else None
            raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Maak een kopie van de config om mutatie te vermijden
        local_config = copy.deepcopy(config) if config else {}

        # Pas speciale configuratie toe als nodig
        if strategy_name == "turtle_swing":
            local_config['mt5'] = local_config.get('mt5', {})
            local_config['mt5']['swing_mode'] = True

        return strategy_class(connector, risk_manager, logger, local_config)

    @classmethod
    def list_available_strategies(cls) -> list[str]:
        """Geeft een lijst van beschikbare strategieën."""
        return list(cls._strategies.keys())