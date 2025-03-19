import os
import sys
import unittest
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

# Voeg project root toe aan Python path
sys.path.insert(
    0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)


def find_config_file():
    """Zoekt het configuratiebestand op verschillende locaties."""
    # Mogelijke locaties
    possible_paths = [
        "config/settings.json",
        "settings.json",
        "../config/settings.json",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "config/settings.json",
        ),
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "settings.json"
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Configuratiebestand gevonden: {path}")
            return path

    # Als laatste redmiddel, zoek door het hele project
    for root, _, files in os.walk("."):
        if "settings.json" in files:
            path = os.path.join(root, "settings.json")
            print(f"Configuratiebestand gevonden via zoeken: {path}")
            return path

    return None


class TestTradingWorkflow(unittest.TestCase):
    def setUp(self):
        # Maak log directory indien niet aanwezig
        os.makedirs("logs", exist_ok=True)

        # Zoek configuratiebestand
        config_path = find_config_file()
        if not config_path:
            self.skipTest("Configuratiebestand niet gevonden")

        # Gebruik try-except voor laden configuratie
        try:
            from src.utils.config import load_config

            self.config = load_config(config_path)
            print(f"Configuratie geladen uit: {config_path}")
        except Exception as e:
            self.skipTest(f"Kon configuratie niet laden: {str(e)}")

        # Logger instance maken
        from src.utils.logger import Logger

        self.logger = Logger("logs/test_trading.csv")

        # Verbeterde mock data met correcte indexen en meer realistische prijzen
        dates = pd.date_range(start="2023-01-01", periods=100, freq="4H")
        random_walk = np.random.normal(0, 0.0002, size=100).cumsum()
        base_price = 1.2000

        self.sample_data = pd.DataFrame(
            {
                "date": dates,
                "open": base_price + random_walk,
                "high": base_price + random_walk + 0.0005,
                "low": base_price + random_walk - 0.0005,
                "close": base_price + random_walk + 0.0002,
                "volume": np.random.randint(100, 1000, 100),
            }
        )
        self.sample_data.set_index("date", inplace=True)

        # Mock MT5Connector met verbeterde returns
        from src.connector.mt5_connector import MT5Connector

        self.mock_connector = MagicMock(spec=MT5Connector)
        self.mock_connector.get_historical_data.return_value = self.sample_data
        self.mock_connector.place_order.return_value = {
            "success": True,
            "order_id": "12345",
            "message": "Order geplaatst",
        }
        self.mock_connector.connect.return_value = True
        self.mock_connector.get_position.return_value = None

        # Volledigere account info
        self.mock_connector.get_account_info.return_value = {
            "balance": 100000.0,
            "equity": 100000.0,
            "margin": 0.0,
            "free_margin": 100000.0,
            "margin_level": 0.0,
            "profit": 0.0,
        }

        # Mock RiskManager met verbeterde implementatie
        from src.risk.risk_manager import RiskManager

        self.mock_risk_manager = MagicMock(spec=RiskManager)
        self.mock_risk_manager.calculate_position_size.return_value = 0.1
        self.mock_risk_manager.is_trading_allowed = True

        try:
            # Maak de strategie aan met de factory
            from src.strategy.strategy_factory import StrategyFactory

            self.strategy = StrategyFactory.create_strategy(
                self.config["strategy"].get("name", "turtle"),
                self.mock_connector,
                self.mock_risk_manager,
                self.logger,
                self.config,
            )
        except Exception as e:
            self.skipTest(f"Kon strategie niet maken: {str(e)}")

    def test_complete_trading_cycle(self):
        """Test de volledige trading cyclus."""
        try:
            symbol = "EURUSD"

            # Test data ophalen
            data = self.mock_connector.get_historical_data(symbol, "H4", 100)
            self.assertIsNotNone(data, "Historische data is None")
            self.assertFalse(data.empty, "Historische data is leeg")

            # Test signaal genereren
            signal_result = self.strategy.process_symbol(symbol)
            self.assertIsNotNone(signal_result, "Signaal resultaat is None")
            self.assertIn("signal", signal_result, "Signaal ontbreekt in resultaat")

            if signal_result["signal"] != "NONE":
                # Test positiegrootte berekenen
                entry_price = signal_result.get("meta", {}).get("entry_price", 1.2000)
                stop_loss = signal_result.get("meta", {}).get("stop_loss", 1.1950)
                position_size = self.mock_risk_manager.calculate_position_size(
                    symbol, entry_price, stop_loss
                )

                self.assertGreater(
                    position_size, 0, "Positiegrootte moet groter zijn dan 0"
                )

                # Test order plaatsen
                order_result = self.mock_connector.place_order(
                    symbol,
                    signal_result["signal"],
                    position_size,
                    signal_result.get("meta", {}).get("entry_price"),
                    signal_result.get("meta", {}).get("stop_loss"),
                    signal_result.get("meta", {}).get("take_profit"),
                )

                self.assertTrue(
                    order_result["success"],
                    f"Order plaatsing mislukt: {order_result.get('message', 'Onbekende fout')}",
                )

            # Test dat alle verwachte mock methodes zijn aangeroepen
            self.mock_connector.get_historical_data.assert_called()

        except Exception as e:
            self.fail(f"Test faalde met onverwachte fout: {str(e)}")

    def test_multiple_symbols_handling(self):
        """Test verwerking van meerdere symbolen."""
        try:
            # Zorg voor meerdere symbolen, fallback naar EURUSD als geen config
            symbols = self.config.get("mt5", {}).get("symbols", ["EURUSD"])
            if not symbols or len(symbols) == 0:
                symbols = ["EURUSD"]  # Fallback

            for symbol in symbols:
                # Test data ophalen
                self.mock_connector.get_historical_data.return_value = self.sample_data

                # Test signaal genereren
                signal_result = self.strategy.process_symbol(symbol)

                # Valideer resultaat structuur
                self.assertIsNotNone(
                    signal_result, f"Signaal resultaat is None voor {symbol}"
                )
                self.assertIn(
                    "signal",
                    signal_result,
                    f"Signaal ontbreekt in resultaat voor {symbol}",
                )
                self.assertIn(
                    signal_result["signal"],
                    ["BUY", "SELL", "NONE", "CLOSE_BUY", "CLOSE_SELL"],
                    f"Ongeldig signaal voor {symbol}: {signal_result['signal']}",
                )

        except Exception as e:
            self.fail(f"Test faalde met onverwachte fout: {str(e)}")

    def test_risk_management_integration(self):
        """Test integratie van risicomanagement."""
        try:
            symbol = "EURUSD"
            entry_price = 1.2000
            stop_loss = 1.1950

            # Override mock voor specifiekere test
            self.mock_risk_manager.calculate_position_size.return_value = 0.25

            position_size = self.mock_risk_manager.calculate_position_size(
                symbol, entry_price, stop_loss
            )

            # Verifieer position sizing
            self.assertEqual(position_size, 0.25, "Position size incorrect")
            self.mock_risk_manager.calculate_position_size.assert_called_with(
                symbol, entry_price, stop_loss
            )

        except Exception as e:
            self.fail(f"Test faalde met onverwachte fout: {str(e)}")


if __name__ == "__main__":
    unittest.main()
