# modules/strategies/base_strategy.py
class BaseStrategy:
    """Basis interface voor alle trading strategieën"""

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de basis strategie

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5
        risk_manager : RiskManager
            Risicobeheer component
        logger : Logger
            Component voor logging
        config : dict
            Strategie configuratie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config

    def process_symbol(self, symbol):
        """
        Verwerk een symbool volgens de strategie

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool
        """
        raise NotImplementedError("Iedere strategie moet process_symbol implementeren")

    def get_open_positions(self):
        """
        Haal alle open posities op

        Returns:
        --------
        dict
            Dictionary met open posities per symbool
        """
        result = {}
        for symbol in self.config['mt5']['symbols']:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result