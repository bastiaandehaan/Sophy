# src/strategy/strategy_factory.py
from typing import Dict, Type, Optional, Any
import copy
import importlib
import os
import sys

from src.strategy.base_strategy import Strategy


class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies = {}

    @classmethod
    def _load_strategies(cls):
        """Laad beschikbare strategieën dynamisch uit de strategy directory"""
        if cls._strategies:
            return

        # Zoek naar strategie modules in de src/strategy directory
        strategy_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(strategy_dir):
            if filename.endswith('_strategy.py') and filename != 'base_strategy.py':
                module_name = filename[:-3]  # Verwijder .py

                try:
                    # Import de module
                    module_path = f"src.strategy.{module_name}"
                    module = importlib.import_module(module_path)

                    # Zoek naar classes die Strategy erven
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Strategy) and attr is not Strategy:
                            # Registreer de strategie
                            strategy_key = module_name.replace('_strategy', '')
                            cls._strategies[strategy_key] = attr
                except (ImportError, AttributeError) as e:
                    print(f"Kon strategie module {module_name} niet laden: {e}")

        # Voeg de turtle strategie toe als deze niet automatisch geladen is
        if 'turtle' not in cls._strategies:
            try:
                from src.strategy.turtle_strategy import TurtleStrategy
                cls._strategies['turtle'] = TurtleStrategy
            except ImportError:
                pass

    @classmethod
    def create_strategy(
            cls,
            strategy_name: str,
            connector: Optional[object],
            risk_manager: Optional[object],
            logger: Optional[object],
            config: Optional[dict]
    ) -> Strategy:
        """
        Creëert een instantie van de gevraagde strategie.

        Args:
            strategy_name (str): Naam van de strategie.
            connector: MT5 connector instantie.
            risk_manager: Risk manager instantie.
            logger: Logger instantie.
            config (dict): Configuratieobject.

        Returns:
            Strategy: Een instantie van de gevraagde strategie.

        Raises:
            ValueError: Als de strategie niet bestaat.
        """
        # Laad beschikbare strategieën
        cls._load_strategies()

        # Controleer of de gevraagde strategie bestaat
        if strategy_name not in cls._strategies:
            # Speciale geval: turtle_swing is dezelfde als turtle maar met swing modus
            if strategy_name == 'turtle_swing' and 'turtle' in cls._strategies:
                strategy_name = 'turtle'
                if config and 'strategy' in config:
                    config['strategy']['swing_mode'] = True
            else:
                if logger:
                    logger.log_info(f"Onbekende strategie: {strategy_name}", level="ERROR")
                raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Maak een kopie van de config om mutatie te vermijden
        local_config = copy.deepcopy(config) if config else {}

        return strategy_class(connector, risk_manager, logger, local_config)

    @classmethod
    def list_available_strategies(cls) -> list:
        """Geeft een lijst van beschikbare strategieën."""
        cls._load_strategies()
        return list(cls._strategies.keys())