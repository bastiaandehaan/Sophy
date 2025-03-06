# src/strategy/base_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Strategy(ABC):
    """
    Abstracte basisklasse voor alle handelsstrategieën.

    Deze klasse definieert de interface die alle strategieën moeten implementeren.
    Door deze basisklasse te gebruiken, kunnen we gemakkelijk nieuwe strategieën
    toevoegen zonder de rest van de code aan te hoeven passen.
    """

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de strategie met de benodigde componenten

        Parameters:
        -----------
        connector : Connector naar handelsplatform (bijv. MT5)
        risk_manager : Risicobeheer component
        logger : Logging component
        config : Configuratiegegevens voor de strategie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config
        self.name = "Base Strategy"

    @abstractmethod
    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de strategie regels

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool

        Returns:
        --------
        Dict : Resultaten van de verwerking, inclusief eventuele signalen
        """
        pass

    @abstractmethod
    def calculate_indicators(self, data: Any) -> Dict[str, Any]:
        """
        Bereken de technische indicatoren voor de strategie

        Parameters:
        -----------
        data : Any
            Prijsgegevens en andere input

        Returns:
        --------
        Dict : Berekende indicatoren
        """
        pass

    def get_name(self) -> str:
        """
        Geef de naam van de strategie terug

        Returns:
        --------
        str : Strategienaam
        """
        return self.name

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op

        Returns:
        --------
        Dict : Dictionary met open posities per symbool
        """
        return {}
