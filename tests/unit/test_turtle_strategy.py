import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from src.strategy.turtle_strategy import TurtleStrategy


@pytest.fixture
def mock_connector():
    """Fixture voor het creëren van een mock connector."""
    connector = MagicMock()

    # Configureer de get_historical_data methode om testdata terug te geven
    def mock_get_historical_data(symbol, timeframe, bars):
        # Creëer synthetische OHLC data
        date_range = pd.date_range(end=pd.Timestamp.now(), periods=bars, freq='4H')
        base_price = 1.2000

        # Creëer een standaard range met lichte opwaartse trend
        data = {
            'date': date_range,
            'open': np.linspace(base_price, base_price * 1.05, bars),
            'high': np.linspace(base_price, base_price * 1.05, bars) * 1.002,
            'low': np.linspace(base_price, base_price * 1.05, bars) * 0.998,
            'close': np.linspace(base_price, base_price * 1.05, bars) * 1.001,
            'tick_volume': np.random.randint(100, 1000, bars)
        }

        # Voeg duidelijke breakout toe rond bar 80
        if bars > 80:
            breakout_idx = 80
            data['high'][breakout_idx:] *= 1.01  # Verhoog highs na breakout
            data['low'][breakout_idx:] *= 1.005  # Verhoog lows na breakout
            data['close'][breakout_idx:] *= 1.008  # Verhoog close na breakout

        return pd.DataFrame(data)

    connector.get_historical_data.side_effect = mock_get_historical_data

    # Mock tick data
    tick = MagicMock()
    tick.ask = 1.2100
    tick.bid = 1.2095
    connector.get_symbol_tick.return_value = tick

    # Mock account info
    connector.get_account_info.return_value = {
        "balance": 100000,
        "equity": 100000,
        "margin": 1000,
        "free_margin": 99000
    }

    return connector


@pytest.fixture
def mock_risk_manager():
    """Fixture voor het creëren van een mock risk manager."""
    risk_manager = MagicMock()
    risk_manager.can_trade.return_value = True
    risk_manager.calculate_position_size.return_value = 1.0
    risk_manager.check_trade_risk.return_value = True
    return risk_manager


@pytest.fixture
def mock_logger():
    """Fixture voor het creëren van een mock logger."""
    return MagicMock()


@pytest.fixture
def turtle_strategy(mock_connector, mock_risk_manager, mock_logger):
    """Fixture voor het creëren van de te testen TurtleStrategy."""
    config = {
        'mt5': {
            'symbols': ['EURUSD'],
            'timeframe': 'H4'
        },
        'strategy': {
            'name': 'turtle',
            'swing_mode': False,
            'entry_period': 20,
            'exit_period': 10,
            'atr_period': 20,
            'atr_multiplier': 2.0,
            'use_trend_filter': True
        }
    }
    return TurtleStrategy(mock_connector, mock_risk_manager, mock_logger, config)


class TestTurtleStrategy:
    def test_calculate_atr(self, turtle_strategy):
        """Test ATR berekening."""
        # Creëer testdata
        data = pd.DataFrame({
            'high': [1.2010, 1.2020, 1.2030, 1.2025, 1.2040],
            'low': [1.1990, 1.2000, 1.2010, 1.2000, 1.2020],
            'close': [1.2000, 1.2010, 1.2020, 1.2015, 1.2030]
        })

        # Bereken ATR
        atr = turtle_strategy.calculate_atr(data)

        # Verifieer resultaten
        assert len(atr) == len(data)
        assert all(atr > 0)  # ATR moet altijd positief zijn
        # Handmatige berekening voor laatste waarde
        true_range = max(data['high'].iloc[-1] - data['low'].iloc[-1],
                         abs(data['high'].iloc[-1] - data['close'].iloc[-2]),
                         abs(data['low'].iloc[-1] - data['close'].iloc[-2]))
        expected_atr = (atr.iloc[-2] * (turtle_strategy.atr_period - 1) + true_range) / turtle_strategy.atr_period
        assert abs(atr.iloc[-1] - expected_atr) < 0.0001

    def test_calculate_indicators(self, turtle_strategy, mock_connector):
        """Test indicator berekeningen."""
        # Haal testdata op via de mock connector
        df = mock_connector.get_historical_data('EURUSD', 'H4', 100)

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(df)

        # Verifieer resultaten
        assert 'atr' in indicators
        assert indicators['atr'] > 0
        assert 'high_entry' in indicators
        assert 'low_entry' in indicators
        assert 'high_exit' in indicators
        assert 'low_exit' in indicators
        assert 'trend_bullish' in indicators

        # Verifieer dat high_entry hoger is dan low_entry
        assert indicators['high_entry'] > indicators['low_entry']

    def test_process_symbol_breakout(self, turtle_strategy, mock_connector):
        """Test verwerking van een breakout signaal."""
        # Configureer de mock om een breakout te simuleren
        tick = mock_connector.get_symbol_tick.return_value
        tick.ask = 1.2200  # Hoge prijs die boven entry niveau ligt

        # Configureer place_order om een ticket te returnen
        mock_connector.place_order.return_value = 12345

        # Verwerk symbool
        result = turtle_strategy.process_symbol('EURUSD')

        # Verifieer resultaten
        assert result['signal'] == 'ENTRY'
        assert result['action'] == 'BUY'
        assert result['ticket'] == 12345

        # Verifieer dat place_order werd aangeroepen
        mock_connector.place_order.assert_called_once()

        # Controleer parameters voor de order
        args, kwargs = mock_connector.place_order.call_args
        assert args[0] == 'BUY'  # Actie
        assert args[1] == 'EURUSD'  # Symbool
        assert args[2] == 1.0  # Volume (van mock risk manager)

    def test_process_symbol_no_signal(self, turtle_strategy, mock_connector):
        """Test verwerking zonder handelssignaal."""
        # Configureer de mock voor een normale prijs zonder breakout
        tick = mock_connector.get_symbol_tick.return_value
        tick.ask = 1.2000  # Prijs onder entry niveau

        # Verwerk symbool
        result = turtle_strategy.process_symbol('EURUSD')

        # Verifieer resultaten
        assert result['signal'] is None
        assert result['action'] is None

        # Verifieer dat place_order niet werd aangeroepen
        mock_connector.place_order.assert_not_called()