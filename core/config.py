# sophy/core/config.py
import json
import os
from typing import Dict, Optional


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Laad configuratie uit JSON bestand met foutafhandeling en standaardwaardes

    Parameters:
    -----------
    config_path : str, optional
        Pad naar configuratiebestand. Standaard is config/settings.json

    Returns:
    --------
    Dict : Geladen configuratie
    """
    if config_path is None:
        config_path = os.path.join('config', 'settings.json')

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Valideer essentiële configuratie-elementen
        validate_config(config)

        # Voeg standaardwaardes toe voor missende items
        add_default_values(config)

        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuratiebestand niet gevonden: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Ongeldige JSON in configuratiebestand: {config_path}")


def validate_config(config: Dict) -> None:
    """
    Controleer of alle vereiste configuratie-elementen aanwezig zijn

    Parameters:
    -----------
    config : Dict
        Te valideren configuratie
    """
    required_sections = ['mt5', 'risk', 'strategy']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missende configuratiesectie: {section}")

    # Controleer specifieke vereiste elementen
    if 'symbols' not in config['mt5']:
        raise ValueError("Geen handelssymbolen gespecificeerd in configuratie")


def add_default_values(config: Dict) -> None:
    """
    Voeg standaardwaardes toe voor missende configuratie-items

    Parameters:
    -----------
    config : Dict
        Configuratie om aan te vullen met standaardwaardes
    """
    # MT5 defaults
    if 'mt5' in config:
        config['mt5'].setdefault('timeframe', 'H4')

    # Risk defaults
    if 'risk' in config:
        config['risk'].setdefault('max_risk_per_trade', 0.01)
        config['risk'].setdefault('max_daily_drawdown', 0.05)
        config['risk'].setdefault('max_total_drawdown', 0.10)

    # Strategy defaults
    if 'strategy' in config:
        config['strategy'].setdefault('name', 'turtle_trader')