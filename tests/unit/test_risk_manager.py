# tests/unit/test_risk_manager.py
import os
import sys
import unittest
from unittest.mock import MagicMock

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.risk.risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        # Maak een mock logger
        self.logger = MagicMock()
        self.logger.log_info = MagicMock()

        # Standaard configuratie
        self.config = {
            'max_risk_per_trade': 0.01,
            'max_daily_drawdown': 0.05,
            'max_total_drawdown': 0.10,
            'leverage': 30,
            'account_balance': 100000
        }

        # Initialiseer risk manager
        self.risk_manager = RiskManager(self.config, self.logger)

    def test_check_ftmo_limits_profit_target(self):
        # Test dat winstdoel correct wordt gedetecteerd
        account_info = {
            'balance': 110000,  # 10% winst
            'equity': 110000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Winstdoel bereikt", reason)

    def test_check_ftmo_limits_daily_drawdown(self):
        # Test dat dagelijkse drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 95000,  # 5% verlies
            'equity': 95000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Dagelijkse verlieslimiet bereikt", reason)

    def test_check_ftmo_limits_total_drawdown(self):
        # Test dat totale drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 90000,  # 10% verlies
            'equity': 90000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Maximale drawdown bereikt", reason)

    def test_check_ftmo_limits_no_violations(self):
        # Test dat geen limieten worden geschonden
        account_info = {
            'balance': 105000,  # 5% winst
            'equity': 105000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertFalse(should_stop)
        self.assertIsNone(reason)

    def test_calculate_position_size(self):
        # Test positiegrootte berekening
        entry_price = 1.2000
        stop_loss = 1.1950  # 50 pips
        account_balance = 100000
        trend_strength = 0.8

        position_size = self.risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=entry_price,
            stop_loss=stop_loss,
            account_balance=account_balance,
            trend_strength=trend_strength
        )

        # Handmatige berekening voor vergelijking:
        # risk_amount = 100000 * 0.01 = 1000
        # adjusted_risk = 1000 * (0.5 + 0.8/2) = 1000 * 0.9 = 900
        # pips_at_risk = (1.2000 - 1.1950) / 0.0001 = 50
        # pip_value = 10 (standaard voor 1 lot)
        # lot_size = 900 / (50 * 10) = 1.8

        # We verwachten dat de waarde dichtbij 1.8 ligt (kan afwijken door afrondingen)
        self.assertGreater(position_size, 1.5)
        self.assertLessEqual(position_size, 2.0)

    def test_check_trade_risk(self):
        # Test trade risico validatie
        symbol = "EURUSD"
        volume = 0.5
        entry_price = 1.2000
        stop_loss = 1.1950

        # Reset dagelijkse limieten
        self.risk_manager.daily_trades_count = 0

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt goedgekeurd
        self.assertTrue(result)

        # Test trade limiet per dag
        self.risk_manager.daily_trades_count = self.risk_manager.max_daily_trades

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt afgewezen
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
