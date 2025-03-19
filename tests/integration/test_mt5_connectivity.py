import pytest
from src.utils.config import load_config
from src.connector.mt5_connector import MT5Connector

@pytest.fixture
def config():
    return load_config("config/settings.json")

@pytest.fixture
def mt5_connector(config):
    return MT5Connector(config["mt5"])

def test_mt5_connection(mt5_connector):
    assert mt5_connector.connect(), "Failed to connect to MT5"

def test_get_account_info(mt5_connector):
    account_info = mt5_connector.get_account_info()
    assert account_info is not None, "Failed to get account info"
    assert "balance" in account_info, "Account info missing balance"
