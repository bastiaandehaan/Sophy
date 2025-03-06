# tests/unit/test_turtle_strategy.py
import os
import sys
import unittest
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.strategy.turtle_strategy import TurtleStrategy


class TestTurtleStrategy(unittest.TestCase):
    def setUp(self):
        # Maak mock objecten
        self.connector = MagicMock()
        self.risk_manager = MagicMock()
        self.logger = MagicMock()

        # Standaard configuratie
        self.config = {
            'mt5': {
                'symbols': ['EURUSD', 'GBPUSD'],
                'timeframe': 'H4',
                'account_balance': 100000
            },
            'strategy': {
                'name': 'turtle',
                'swing_mode': False,
                'entry_period': 20,
                'exit_period': 10,
                'atr_period': 20,
                'atr_multiplier': 2.0
            }
        }

        # Initialiseer strategie
        self.strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, self.config)

    def test_initialization(self):
        # Test dat de strategie correct wordt geïnitialiseerd
        self.assertEqual(self.strategy.name, "Turtle Trading Strategy")
        self.assertEqual(self.strategy.entry_period, 20)
        self.assertEqual(self.strategy.exit_period, 10)
        self.assertEqual(self.strategy.atr_period, 20)
        self.assertEqual(self.strategy.atr_multiplier, 2.0)
        self.assertFalse(self.strategy.swing_mode)

    def test_swing_mode_initialization(self):
        # Test swing mode initialisatie
        config = self.config.copy()
        config['strategy']['swing_mode'] = True

        strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, config)

        self.assertTrue(strategy.swing_mode)
        self.assertEqual(strategy.entry_period, 40)  # Standaard voor swing mode

    def test_calculate_indicators(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Bereken indicatoren
        indicators = self.strategy.calculate_indicators(df)

        # Test dat de belangrijkste indicatoren aanwezig zijn
        self.assertIn('atr', indicators)
        self.assertIn('high_entry', indicators)
        self.assertIn('low_exit', indicators)

    def test_calculate_atr(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=50, freq='4H')
        high = np.random.normal(1.2, 0.01, 50)
        low = high - np.random.uniform(0.001, 0.005, 50)
        close = low + np.random.uniform(0, 0.003, 50)

        df = pd.DataFrame({
            'date': dates,
            'high': high,
            'low': low,
            'close': close
        })

        # Bereken ATR
        atr = self.strategy.calculate_atr(df, 14)

        # Test eigenschappen
        self.assertEqual(len(atr), 50)
        self.assertTrue(atr.iloc[-1] > 0)

    def test_process_symbol_no_data(self):
        # Test gedrag wanneer er geen data is
        self.connector.get_historical_data.return_value = pd.DataFrame()

        result = self.strategy.process_symbol('EURUSD')

        # Test dat er geen signaal is
        self.assertIsNone(result.get('signal'))
        self.logger.log_info.assert_called_with("Geen historische data beschikbaar voor EURUSD")

    def test_process_symbol_with_breakout(self):
        # Configureer mocks voor een breakout scenario
        # 1. Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Zorg dat laatste candle een breakout is
        df['high'].iloc[-1] = 1.25  # Hogere high voor breakout

        self.connector.get_historical_data.return_value = df

        # 2. Configureer tick
        tick = MagicMock()
        tick.ask = 1.25
        tick.bid = 1.248
        self.connector.get_symbol_tick.return_value = tick

        # 3. Configureer risicomanager
        self.risk_manager.can_trade.return_value = True
        self.risk_manager.calculate_position_size.return_value = 0.5
        self.risk_manager.check_trade_risk.return_value = True

        # 4. Configureer account info
        account_info = {'balance': 100000, 'equity': 100000}
        self.connector.get_account_info.return_value = account_info

        # 5. Configureer order response
        self.connector.place_order.return_value = 12345  # ticket ID

        # Test de processsymbol functie met de ingerichte mocks
        result = self.strategy.process_symbol('EURUSD')

        # Verwacht een entry signaal
        self.assertEqual(result.get('signal'), 'ENTRY')
        self.assertEqual(result.get('action'), 'BUY')
        self.assertEqual(result.get('ticket'), 12345)

        # Controleer dat de place_order functie werd aangeroepen
        self.connector.place_order.assert_called_once()


if __name__ == '__main__':
    unittest.main()
