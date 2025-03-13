# src/utils/config.py
import json
import os
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Laad configuratie uit JSON bestand met validatie

    Parameters:
    -----------
    config_path : str, optional
        Pad naar het configuratiebestand. Als niet opgegeven wordt standaard pad gebruikt.

    Returns:
    --------
    Dict[str, Any] : Geladen configuratie

    Raises:
    -------
    FileNotFoundError : Als het configuratiebestand niet gevonden kan worden
    ValueError : Als het configuratiebestand ongeldige JSON bevat
    """
    if config_path is None:
        config_path = os.environ.get("SOPHY_CONFIG_PATH", "config/settings.json")

    try:
        with open(config_path, "r") as file:
            config = json.load(file)

        # Valideer vereiste secties
        required_sections = ["mt5", "risk", "strategy"]
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Sectie '{section}' ontbreekt in configuratie")

        # Pas standaardwaarden toe
        if "mt5" in config:
            config["mt5"].setdefault("timeframe", "H4")
            config["mt5"].setdefault("symbols", ["EURUSD"])
            config["mt5"].setdefault("account_balance", 100000)

        if "risk" in config:
            config["risk"].setdefault("max_risk_per_trade", 0.01)
            config["risk"].setdefault("max_daily_drawdown", 0.05)
            config["risk"].setdefault("max_total_drawdown", 0.10)
            config["risk"].setdefault("leverage", 30)

        if "logging" not in config:
            config["logging"] = {
                "log_file": "logs/trading_log.csv",
                "log_level": "INFO",
            }

        return config
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        raise ValueError(f"Ongeldige JSON in configuratiebestand: {str(e)}")
