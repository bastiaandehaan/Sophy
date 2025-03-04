# tests/integration/test_mt5_connectivity.py
from datetime import datetime, timedelta

import pytest
from turtle_trader.data.mt5_connector import MT5Connector
from turtle_trader.utils.config import load_config


@pytest.fixture
def mt5_connector():
    """Create a connector instance with test configuration"""
    config = load_config("tests/config/test_config.json")
    from turtle_trader.utils.logger import Logger
    logger = Logger("tests/logs/test_log.csv")
    return MT5Connector(config['mt5'], logger)


def test_mt5_connection(mt5_connector):
    """Test connection to MT5 platform"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Clean up
    mt5_connector.disconnect()


def test_historical_data_retrieval(mt5_connector):
    """Test retrieving historical data from MT5"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Get historical data
    symbol = "EURUSD"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = mt5_connector.get_historical_data(symbol, 16, 100)  # 16 = H4 timeframe

    # Validate data
    assert not df.empty, "No historical data retrieved"
    assert 'open' in df.columns, "Data missing expected columns"
    assert 'high' in df.columns, "Data missing expected columns"
    assert 'low' in df.columns, "Data missing expected columns"
    assert 'close' in df.columns, "Data missing expected columns"

    # Clean up
    mt5_connector.disconnect()