# src/utils/config.py
import json
import os
import logging
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from JSON file with validation"""
    if config_path is None:
        config_path = os.environ.get("SOPHY_CONFIG_PATH", "config/settings.json")

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Validate required sections
        required_sections = ['mt5', 'risk', 'strategy']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Section '{section}' missing in configuration")

        # Apply default values
        if 'mt5' in config:
            config['mt5'].setdefault('timeframe', 'H4')
            config['mt5'].setdefault('symbols', ['EURUSD'])
            config['mt5'].setdefault('account_balance', 100000)

        if 'risk' in config:
            config['risk'].setdefault('max_risk_per_trade', 0.01)
            config['risk'].setdefault('max_daily_drawdown', 0.05)
            config['risk'].setdefault('max_total_drawdown', 0.10)

        if 'logging' not in config:
            config['logging'] = {'log_file': 'logs/trading_log.csv', 'log_level': 'INFO'}

        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in configuration file: {config_path}")
        raise ValueError(f"Invalid JSON in configuration file: {str(e)}")