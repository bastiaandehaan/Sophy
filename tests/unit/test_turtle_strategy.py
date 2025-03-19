# tests/unit/test_turtle_strategy.py
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from src.strategy.turtle_strategy import TurtleStrategy


@pytest.fixture
def mock_connector():
    """Fixture voor het creëren van een mock connector."""
    connector = MagicMock()

    # Configureer de get_historical_data methode om testdata terug te geven
    def mock_get_historical_data(symbol, timeframe, num_bars):
        # Creëer synthetische OHLC data
        date_range = pd.date_range(end=pd.Timestamp.now(), periods=num_bars, freq="4H")
        base_price = 1.2000

        # Creëer een standaard range met lichte opwaartse trend
        data = pd.DataFrame(
            {
                "open": np.linspace(base_price, base_price * 1.05, num_bars),
                "high": np.linspace(base_price, base_price * 1.05, num_bars) * 1.002,
                "low": np.linspace(base_price, base_price * 1.05, num_bars) * 0.998,
                "close": np.linspace(base_price, base_price * 1.05, num_bars) * 1.001,
                "tick_volume": np.random.randint(100, 1000, num_bars),
            },
            index=date_range,
        )

        # Voeg duidelijke breakout toe rond bar 80
        if num_bars > 80:
            breakout_idx = 80
            data["high"].iloc[breakout_idx:] *= 1.01  # Verhoog highs na breakout
            data["low"].iloc[breakout_idx:] *= 1.005  # Verhoog lows na breakout
            data["close"].iloc[breakout_idx:] *= 1.008  # Verhoog close na breakout

        return data

    connector.get_historical_data.side_effect = mock_get_historical_data

    # Mock positie informatie
    connector.get_position.return_value = None
    connector.get_open_positions.return_value = {}

    # Mock account info
    connector.get_account_info.return_value = {
        "balance": 100000,
        "equity": 100000,
        "margin": 1000,
        "free_margin": 99000,
    }

    return connector


@pytest.fixture
def mock_risk_manager():
    """Fixture voor het creëren van een mock risk manager."""
    risk_manager = MagicMock()
    risk_manager.is_trading_allowed = True
    risk_manager.calculate_position_size.return_value = 1.0
    return risk_manager


@pytest.fixture
def mock_logger():
    """Fixture voor het creëren van een mock logger."""
    logger = MagicMock()
    return logger


@pytest.fixture
def turtle_strategy(mock_connector, mock_risk_manager, mock_logger):
    """Fixture voor het creëren van de te testen TurtleStrategy."""
    config = {
        "strategy": {
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 14,
            "atr_multiplier": 2.0,
            "use_filters": True,
            "filter_period": 50,
            "units": 1,
            "swing_mode": False,
        },
        "timeframe": "D1",
        "symbols": ["EURUSD"],
    }
    return TurtleStrategy(mock_connector, mock_risk_manager, mock_logger, config)


class TestTurtleStrategy:
    def test_process_symbol(self, turtle_strategy, mock_connector):
        """Test de process_symbol methode."""
        # Roep de methode aan
        result = turtle_strategy.process_symbol("EURUSD")

        # Verifieer basis structuur van het resultaat
        assert isinstance(result, dict)
        assert "signal" in result
        assert "meta" in result

        # Verifieer dat get_historical_data werd aangeroepen
        mock_connector.get_historical_data.assert_called_once()

    def test_calculate_indicators(self, turtle_strategy):
        """Test de calculate_indicators methode."""
        # Maak testdata
        dates = pd.date_range(start="2023-01-01", periods=100)
        data = pd.DataFrame(
            {
                "open": np.linspace(1.0, 1.1, 100),
                "high": np.linspace(1.01, 1.11, 100),
                "low": np.linspace(0.99, 1.09, 100),
                "close": np.linspace(1.005, 1.105, 100),
            },
            index=dates,
        )

        # Voeg een breakout toe
        data.loc[dates[-20]:, "high"] *= 1.02

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(data)

        # Verifieer de output
        assert "data" in indicators
        assert "current_price" in indicators
        assert "previous_entry_high" in indicators
        assert "previous_entry_low" in indicators
        assert "current_atr" in indicators
        assert "trend_up" in indicators
        assert "trend_down" in indicators

        # Verifieer dat de getransformeerde data de verwachte kolommen bevat
        transformed_data = indicators["data"]
        assert "entry_high" in transformed_data.columns
        assert "entry_low" in transformed_data.columns
        assert "exit_high" in transformed_data.columns
        assert "exit_low" in transformed_data.columns
        assert "atr" in transformed_data.columns

    def test_generate_signal_long_entry(self, turtle_strategy):
        """Test signaal generatie voor long entry."""
        # Creëer test data met een duidelijk long entry signaal
        dates = pd.date_range(start="2023-01-01", periods=100)
        data = pd.DataFrame(
            {
                "open": np.linspace(1.0, 1.1, 100),
                "high": np.linspace(1.01, 1.11, 100),
                "low": np.linspace(0.99, 1.09, 100),
                "close": np.linspace(1.005, 1.105, 100),
            },
            index=dates,
        )

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(data)

        # Maak een breakout situatie
        indicators["current_price"] = indicators["previous_entry_high"] * 1.01
        indicators["trend_up"] = True

        # Genereer signaal
        result = turtle_strategy._generate_signal("EURUSD", data, indicators, None)

        # Verifieer resultaat
        assert result["signal"] == "BUY"
        assert "entry_price" in result["meta"]
        assert "stop_loss" in result["meta"]
        assert "risk_pips" in result["meta"]
        assert result["meta"]["reason"] == "long_entry_breakout"

    def test_generate_signal_short_entry(self, turtle_strategy):
        """Test signaal generatie voor short entry."""
        # Creëer test data met een duidelijk short entry signaal
        dates = pd.date_range(start="2023-01-01", periods=100)
        data = pd.DataFrame(
            {
                "open": np.linspace(1.1, 1.0, 100),
                "high": np.linspace(1.11, 1.01, 100),
                "low": np.linspace(1.09, 0.99, 100),
                "close": np.linspace(1.105, 1.005, 100),
            },
            index=dates,
        )

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(data)

        # Maak een breakout situatie
        indicators["current_price"] = indicators["previous_entry_low"] * 0.99
        indicators["trend_down"] = True

        # Genereer signaal
        result = turtle_strategy._generate_signal("EURUSD", data, indicators, None)

        # Verifieer resultaat
        assert result["signal"] == "SELL"
        assert "entry_price" in result["meta"]
        assert "stop_loss" in result["meta"]
        assert "risk_pips" in result["meta"]
        assert result["meta"]["reason"] == "short_entry_breakout"

    def test_generate_signal_long_exit(self, turtle_strategy):
        """Test signaal generatie voor het sluiten van een long positie."""
        # Creëer test data
        dates = pd.date_range(start="2023-01-01", periods=100)
        data = pd.DataFrame(
            {
                "open": np.linspace(1.1, 1.0, 100),
                "high": np.linspace(1.11, 1.01, 100),
                "low": np.linspace(1.09, 0.99, 100),
                "close": np.linspace(1.105, 1.005, 100),
            },
            index=dates,
        )

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(data)

        # Maak een exit situatie
        indicators["current_price"] = indicators["previous_exit_low"] * 0.99

        # Genereer signaal met een bestaande long positie
        result = turtle_strategy._generate_signal("EURUSD", data, indicators, "BUY")

        # Verifieer resultaat
        assert result["signal"] == "CLOSE_BUY"
        assert result["meta"]["reason"] == "long_exit_breakout"

    def test_get_position(self, turtle_strategy, mock_connector):
        """Test het ophalen van positie informatie."""
        # Setup mock
        expected_position = {"direction": "BUY", "entry_price": 1.2000, "volume": 0.5}
        mock_connector.get_position.return_value = expected_position

        # Haal positie op
        position = turtle_strategy.get_position("EURUSD")

        # Verifieer resultaat
        assert position == expected_position
        mock_connector.get_position.assert_called_once_with("EURUSD")

        # Test caching van positie
        turtle_strategy.positions["EURUSD"] = {
            "direction": "SELL",
            "entry_price": 1.1000,
        }
        position = turtle_strategy.get_position("EURUSD")

        # Moet de cached positie gebruiken
        assert position["direction"] == "SELL"
        assert position["entry_price"] == 1.1000

    def test_on_order_filled_buy(self, turtle_strategy, mock_logger):
        """Test order filled verwerking voor een BUY order."""
        # Roep methode aan
        turtle_strategy.on_order_filled(
            symbol="EURUSD",
            order_type="BUY",
            price=1.2000,
            volume=0.5,
            order_id="12345",
            timestamp="2023-01-01 12:00:00",
        )

        # Verifieer positie registratie
        assert "EURUSD" in turtle_strategy.positions
        assert turtle_strategy.positions["EURUSD"]["direction"] == "BUY"
        assert turtle_strategy.positions["EURUSD"]["entry_price"] == 1.2000
        assert turtle_strategy.positions["EURUSD"]["volume"] == 0.5

        # Verifieer logging
        mock_logger.info.assert_called()

    def test_on_order_filled_close(self, turtle_strategy, mock_logger):
        """Test order filled verwerking voor een CLOSE_BUY order."""
        # Setup een bestaande positie
        turtle_strategy.positions["EURUSD"] = {
            "direction": "BUY",
            "entry_price": 1.2000,
            "volume": 0.5,
            "order_id": "12345",
            "entry_time": "2023-01-01 12:00:00",
        }

        # Roep methode aan
        turtle_strategy.on_order_filled(
            symbol="EURUSD",
            order_type="CLOSE_BUY",
            price=1.2100,
            volume=0.5,
            order_id="67890",
            timestamp="2023-01-02 12:00:00",
        )

        # Verifieer positie verwijdering
        assert "EURUSD" not in turtle_strategy.positions

        # Verifieer logging
        mock_logger.info.assert_called()
