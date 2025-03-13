# tests/unit/test_risk_manager.py
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.risk.risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        # Maak een mock logger
        self.logger = MagicMock()
        self.logger.log_info = MagicMock()

        # Patchen van de logger interface voor compatibiliteit
        self.logger.info = self.logger.log_info
        self.logger.warning = MagicMock()
        self.logger.error = MagicMock()

        # Standaard configuratie
        self.config = {
            "risk_per_trade": 0.01,  # Aangepaste parameternaam
            "daily_drawdown_limit": 0.05,  # Aangepaste parameternaam
            "total_drawdown_limit": 0.10,  # Aangepaste parameternaam
            "max_trades_per_day": 5,
            "profit_target": 0.10,
            "initial_balance": 100000,
        }

        # Mock MT5Connector toevoegen
        self.mock_connector = MagicMock()
        self.mock_connector.get_account_info.return_value = {
            "balance": 100000,
            "equity": 100000,
            "margin": 1000,
            "free_margin": 99000,
        }

        self.mock_connector.get_symbol_info.return_value = {
            "trade_tick_value": 0.0001,
            "trade_contract_size": 100000,
            "trade_tick_size": 0.00001,
            "volume_step": 0.01,
            "volume_min": 0.01,
            "volume_max": 100.0,
        }

        # Initialiseer risk manager
        self.risk_manager = RiskManager(self.config, self.logger, self.mock_connector)
        self.risk_manager.initialize()  # Initialize met account info

    def test_check_ftmo_limits_profit_target(self):
        # Test dat winstdoel correct wordt gedetecteerd
        # Simuleer account info met 10% winst
        self.mock_connector.get_account_info.return_value = {
            "balance": 110000,
            # 10% winst
            "equity": 110000,
        }

        # Haal ftmo status op
        ftmo_status = self.risk_manager.get_ftmo_status()

        # Controleer of de winst percentage correct is
        self.assertAlmostEqual(ftmo_status["profit_percentage"], 10.0, places=1)

        # Controleer of de winstdoel juist is
        self.assertEqual(ftmo_status["profit_target_percentage"], 10.0)

        # In onze nieuwe implementatie stopt trading niet automatisch bij winstdoel
        self.assertTrue(self.risk_manager.is_trading_allowed)

    def test_check_ftmo_limits_daily_drawdown(self):
        # Test dat dagelijkse drawdown limiet correct wordt gedetecteerd
        # Update dagelijkse P/L om drawdown te simuleren
        self.risk_manager.today_pl = -5000  # 5% verlies van 100k

        # Controleer ftmo status
        ftmo_status = self.risk_manager.get_ftmo_status()

        # Daily drawdown zou een positieve waarde moeten zijn in de status
        self.assertAlmostEqual(ftmo_status["daily_drawdown"], 5.0, places=1)

        # Check interne state
        self.risk_manager._check_trading_allowed()

        # Trading zou moeten stoppen bij deze drawdown
        self.assertFalse(self.risk_manager.is_trading_allowed)

    def test_check_ftmo_limits_total_drawdown(self):
        # Test dat totale drawdown limiet correct wordt gedetecteerd
        # Simuleer een situatie met maximale drawdown
        self.risk_manager.highest_balance = 100000
        self.mock_connector.get_account_info.return_value = {
            "balance": 90000,
            # 10% verlies
            "equity": 90000,
        }

        # Controleer ftmo status
        ftmo_status = self.risk_manager.get_ftmo_status()

        # Total drawdown zou een positieve waarde moeten zijn in de status
        self.assertAlmostEqual(ftmo_status["total_drawdown"], 10.0, places=1)

        # Check interne state
        self.risk_manager._check_trading_allowed()

        # Trading zou moeten stoppen bij deze drawdown
        self.assertFalse(self.risk_manager.is_trading_allowed)

    def test_check_ftmo_limits_no_violations(self):
        # Test dat geen limieten worden geschonden
        # Standaard setup heeft geen limieten overschreden

        # Controleer ftmo status
        ftmo_status = self.risk_manager.get_ftmo_status()

        # Alles zou binnen limieten moeten zijn
        self.assertLess(
            ftmo_status["daily_drawdown"], self.config["daily_drawdown_limit"] * 100
        )
        self.assertLess(
            ftmo_status["total_drawdown"], self.config["total_drawdown_limit"] * 100
        )

        # Trading zou toegestaan moeten zijn
        self.assertTrue(self.risk_manager.is_trading_allowed)

    def test_calculate_position_size(self):
        # Test positiegrootte berekening
        entry_price = 1.2000
        stop_loss = 1.1950  # 50 pips
        risk_pips = 50.0

        position_size = self.risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_pips=risk_pips,
        )

        # We verwachten een redelijke positiegrootte gebaseerd op 1% risico
        # van 100k account met 50 pips risico
        self.assertGreater(position_size, 0)

        # Logger zou moeten zijn aangeroepen
        self.logger.info.assert_called()

    def test_update_after_trade(self):
        # Test update na een trade
        symbol = "EURUSD"
        profit_loss = 1000.0  # $1000 winst
        close_time = datetime.now()  # Echte datetime

        # Huidige state bijhouden voor vergelijking
        initial_balance = self.mock_connector.get_account_info()["balance"]

        # Update na trade
        self.risk_manager.update_after_trade(symbol, profit_loss, close_time)

        # Verificatie dat trading days is bijgewerkt
        self.assertGreater(len(self.risk_manager.trading_days), 0)

        # Trading moet nog steeds toegestaan zijn
        self.assertTrue(self.risk_manager.is_trading_allowed)


if __name__ == "__main__":
    unittest.main()
