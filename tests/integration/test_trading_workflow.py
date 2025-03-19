import unittest
from unittest.mock import MagicMock
import pandas as pd
from src.utils.config import load_config
from src.connector.mt5_connector import MT5Connector
from src.strategy.strategy_factory import StrategyFactory
from src.risk.risk_manager import RiskManager


class TestTradingWorkflow(unittest.TestCase):
    def setUp(self):
        # Laad de configuratie
        self.config = load_config("config/settings.json")

        # Mock MT5Connector
        self.mock_connector = MagicMock(spec=MT5Connector)
        sample_data = pd.DataFrame({
            'open': [1.1, 1.2], 'high': [1.15, 1.25], 'low': [1.05, 1.15],
            'close': [1.12, 1.22]
        }, index=pd.date_range(start='2023-01-01', periods=2, freq='4H'))
        self.mock_connector.get_historical_data.return_value = sample_data
        self.mock_connector.place_order.return_value = {"success": True}

        # Mock RiskManager
        self.mock_risk_manager = MagicMock(spec=RiskManager)
        self.mock_risk_manager.calculate_position_size.return_value = 0.1

        # Maak de strategie aan met de factory
        self.strategy = StrategyFactory.create_strategy(
            self.config["strategy"]["name"],
            self.mock_connector,
            self.mock_risk_manager,
            self.config
        )

    def test_complete_trading_cycle(self):
        symbol = "EURUSD"
        data = self.mock_connector.get_historical_data(symbol, "H4", 100)
        signal = self.strategy.process_symbol(symbol)
        if signal["signal"] != "NONE":
            position_size = self.mock_risk_manager.calculate_position_size(
                symbol, signal["entry_price"], signal["stop_loss"]
            )
            order_result = self.mock_connector.place_order(
                symbol, signal["signal"], position_size, signal["entry_price"],
                signal["stop_loss"], signal["take_profit"]
            )
            self.assertTrue(order_result["success"], "Order placement failed")

    def test_multiple_symbols_handling(self):
        symbols = self.config["mt5"]["symbols"]
        for symbol in symbols:
            data = self.mock_connector.get_historical_data(symbol, "H4", 100)
            signal = self.strategy.process_symbol(symbol)
            self.assertIn(signal["signal"], ["BUY", "SELL", "NONE"],
                          f"Invalid signal for {symbol}")

    def test_risk_management_integration(self):
        symbol = "EURUSD"
        entry_price = 1.2000
        stop_loss = 1.1950
        position_size = self.mock_risk_manager.calculate_position_size(symbol,
                                                                       entry_price,
                                                                       stop_loss)
        self.assertGreater(position_size, 0,
                           "Position size should be greater than zero")


if __name__ == "__main__":
    unittest.main()
