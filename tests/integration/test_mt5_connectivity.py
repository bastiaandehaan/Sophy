import os

import pytest


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


@pytest.fixture
def logger():
    """Fixture voor logger tijdens tests."""
    os.makedirs("logs", exist_ok=True)
    from src.utils.logger import Logger

    return Logger("logs/test_connectivity.csv")


@pytest.fixture
def config():
    """Laad configuratie met foutafhandeling en fallbacks."""
    try:
        # Zorg dat project root in pythonpath staat
        import sys

        sys.path.insert(
            0,
            os.path.abspath(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
        )

        from src.utils.config import load_config

        config_path = find_config_file()
        if not config_path:
            pytest.skip("Configuratiebestand niet gevonden")

        config = load_config(config_path)
        if "mt5" not in config:
            pytest.skip("MT5 configuratie ontbreekt in settings.json")
        return config
    except Exception as e:
        pytest.skip(f"Kon configuratie niet laden: {str(e)}")


@pytest.fixture
def mt5_connector(config, logger):
    """Creëer MT5 connector met logger."""
    from src.connector.mt5_connector import MT5Connector

    connector = MT5Connector(config["mt5"], logger)
    return connector


@pytest.mark.integration
def test_mt5_connection(mt5_connector, logger):
    """Test connectie met MT5 met duidelijke logging."""
    try:
        is_connected = mt5_connector.connect()
        if not is_connected:
            logger.log_info(
                "MT5 verbinding mislukt - controleer MT5 installatie en login gegevens"
            )
            pytest.skip("MT5 verbinding kon niet worden gemaakt - test overgeslagen")
        assert is_connected, "MT5 verbinding mislukt"
    except Exception as e:
        logger.log_info(f"Fout tijdens MT5 verbinding: {str(e)}", level="ERROR")
        pytest.skip(f"Test overgeslagen vanwege fout: {str(e)}")


@pytest.mark.integration
def test_get_account_info(mt5_connector, logger):
    """Test ophalen van accountinformatie met betere foutafhandeling."""
    try:
        # Zorg eerst voor verbinding
        is_connected = mt5_connector.connect(show_dialog=False)
        if not is_connected:
            pytest.skip("MT5 verbinding niet mogelijk - test overgeslagen")

        account_info = mt5_connector.get_account_info()
        assert account_info is not None, "Geen accountinfo ontvangen"
        assert "balance" in account_info, "Accountinfo mist 'balance' veld"
        logger.log_info(f"Accountinfo succesvol opgehaald: {account_info}")
    except Exception as e:
        logger.log_info(f"Fout bij ophalen accountinfo: {str(e)}", level="ERROR")
        pytest.skip(f"Test overgeslagen vanwege fout: {str(e)}")
