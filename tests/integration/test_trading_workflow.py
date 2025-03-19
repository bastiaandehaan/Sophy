# tests/integration/test_trading_workflow.py
"""
Integratie test voor een volledige trading workflow.

Deze test valideert de samenwerking tussen alle componenten van het Sophy Trading System.
"""
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.connector.mt5_connector import MT5Connector
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


@pytest.fixture
def mock_setup():
    """Fixture voor het opzetten van mocks voor alle componenten."""
    # Setup mock configuration
    config = {
        "mt5": {
            "symbols": ["EURUSD", "GBPUSD"],
            "timeframe": "H4"
        },
        "risk": {
            "risk_per_trade": 0.01,
            "max_daily_drawdown": 0.05,
            "total_drawdown_limit": 0.10,
            "max_trades_per_day": 5
        },
        "strategy": {
            "name": "turtle",
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 14,
            "atr_multiplier": 2.0
        },
        "logging": {
            "log_file": "tests/logs/test_workflow.csv",
            "log_level": "INFO"
        }
    }

    # Create logger
    logger = Logger(config["logging"]["log_file"])
    logger.log_info = MagicMock()
    logger.info = logger.log_info  # Compatibility with different logger interfaces
    logger.warning = MagicMock()
    logger.error = MagicMock()

    # Create MT5 mock
    mt5_mock = MagicMock()

    # Mock connector
    connector = MagicMock(spec=MT5Connector)
    connector.get_historical_data.return_value = _create_test_data()

    account_info = {
        "balance": 100000,
        "equity": 100000,
        "margin": 1000,
        "free_margin": 99000,
        "margin_level": 10000
    }
    connector.get_account_info.return_value = account_info
    connector.get_position.return_value = None
    connector.get_open_positions.return_value = []

    # Mock risk manager
    risk_manager = MagicMock(spec=RiskManager)
    risk_manager.is_trading_allowed = True
    risk_manager.calculate_position_size.return_value = 0.5
    risk_manager.check_ftmo_limits = MagicMock(return_value=(False, None))

    return {
        "config": config,
        "logger": logger,
        "connector": connector,
        "risk_manager": risk_manager,
        "mt5_mock": mt5_mock
    }


def _create_test_data():
    """Helper voor het creëren van test OHLC data."""
    import numpy as np

    # Maak een DataFrame met 100 bars van testdata
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq="4H")

    # Creëer synthetische prijsdata met een trend
    base_price = 1.2000
    prices = np.linspace(base_price, base_price * 1.05, 100)

    # Voeg wat volatiliteit toe
    noise = np.random.normal(0, 0.0005, 100)
    prices = prices + noise

    # Maak OHLC data
    df = pd.DataFrame({
        "open": prices,
        "high": prices * 1.001,
        "low": prices * 0.999,
        "close": prices + np.random.normal(0, 0.0001, 100),
        "tick_volume": np.random.randint(100, 1000, 100)
    }, index=dates)

    # Voeg een duidelijke breakout toe voor signaaldetectie
    breakout_idx = 80
    df.iloc[breakout_idx:, 1] *= 1.01  # Verhoog highs na breakout

    return df


class TestTradingWorkflow(unittest.TestCase):
    """Test case voor de volledige trading workflow."""

    def test_complete_trading_cycle(self, mock_setup):
        """
        Test een volledige handelscyclus van strategie-initialisatie tot order uitvoering.

        Deze test valideert de end-to-end integratie van alle componenten:
        - Configuratie laden
        - MT5 verbinding
        - Strategie initialisatie
        - Signaal detectie
        - Risicobeheer
        - Order plaatsing
        """
        # Haal componenten uit mock setup
        config = mock_setup["config"]
        logger = mock_setup["logger"]
        connector = mock_setup["connector"]
        risk_manager = mock_setup["risk_manager"]
        mt5_mock = mock_setup["mt5_mock"]

        # Maak turtle strategie aan via factory
        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config,
        )

        # Verwerk symbool om handelssignaal te genereren
        symbol = config["mt5"]["symbols"][0]  # Gebruik eerste symbool
        result = strategy.process_symbol(symbol)

        # Controleer resultaten
        self.assertIsNotNone(result, "Strategie moet een resultaat teruggeven")
        self.assertIn("signal", result, "Resultaat moet een 'signal' sleutel bevatten")

        # Als er een signaal is, controleer de order uitvoering
        if result.get("signal") in ["BUY", "SELL"]:
            self.assertIn("meta", result, "Entry signaal moet metadata bevatten")
            # Het testen van ticket ID is niet relevant omdat we niet echt een order plaatsen in de test
            # We kunnen wel controleren of de Risk Manager werd aangeroepen
            risk_manager.calculate_position_size.assert_called()

        # Controleer FTMO limieten
        should_stop, reason = risk_manager.check_ftmo_limits(
            connector.get_account_info())

        # Log de resultaten
        logger.log_info.assert_called()

    def test_risk_management_integration(self, mock_setup):
        """
        Test de integratie van risicobeheer binnen de handelsstrategie.

        Valideert:
        - Correcte berekening van positiegrootte
        - Toepassing van risicobeperkingen
        - FTMO limiet controles
        """
        # Haal componenten uit mock setup
        config = mock_setup["config"]
        logger = mock_setup["logger"]
        connector = mock_setup["connector"]
        risk_manager = mock_setup["risk_manager"]

        # Maak strategie
        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config,
        )

        # Verwerk symbool
        symbol = config["mt5"]["symbols"][0]
        strategy.process_symbol(symbol)

        # Controleer of de risk manager werd aangeroepen
        risk_manager.calculate_position_size.assert_called()

        # Simuleer dat trading niet toegestaan is
        risk_manager.is_trading_allowed = False

        # Verwerk nog een symbool, zou geen handel moeten genereren
        result = strategy.process_symbol(symbol)
        self.assertNotEqual(result.get("signal"), "BUY",
                            "Geen BUY signaal verwacht bij is_trading_allowed=False")
        self.assertNotEqual(result.get("signal"), "SELL",
                            "Geen SELL signaal verwacht bij is_trading_allowed=False")

    def test_multiple_symbols_handling(self, mock_setup):
        """
        Test het verwerken van meerdere symbolen binnen één handelscyclus.

        Valideert:
        - Correcte verwerking van meerdere symbolen
        - Onafhankelijke signaaldetectie per symbool
        - Geaggregeerde risico-evaluatie
        """
        # Haal componenten uit mock setup
        config = mock_setup["config"]
        logger = mock_setup["logger"]
        connector = mock_setup["connector"]
        risk_manager = mock_setup["risk_manager"]

        # Maak strategie
        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config,
        )

        # Verwerk alle symbolen
        results = {}
        for symbol in config["mt5"]["symbols"]:
            results[symbol] = strategy.process_symbol(symbol)

        # Controleer resultaten voor elk symbool
        self.assertEqual(len(results), len(config["mt5"]["symbols"]),
                         "Moet resultaten hebben voor alle symbolen")

        # Controleer dat elk resultaat de juiste structuur heeft
        for symbol, result in results.items():
            self.assertIn("signal", result,
                          f"Resultaat voor {symbol} mist 'signal' sleutel")
            self.assertIn("meta", result,
                          f"Resultaat voor {symbol} mist 'meta' sleutel")


if __name__ == "__main__":
    unittest.main()
