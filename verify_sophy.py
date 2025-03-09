#!/usr/bin/env python3
"""
Sophy Framework Verificatiescript

Dit script voert een reeks tests uit om te controleren of de Sophy Trading Framework
correct is geïnstalleerd en de basisfunctionaliteit werkt.
"""
import os
import sys
import json
import importlib
from datetime import datetime, timedelta

# Voeg src directory toe aan Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


def log_step(msg):
    """Log een stap naar console met duidelijke opmaak"""
    print(f"\n{'-' * 80}\n>> {msg}\n{'-' * 80}")


def log_pass(msg):
    """Log een succesvolle test"""
    print(f"✅ {msg}")


def log_fail(msg):
    """Log een mislukte test"""
    print(f"❌ {msg}")


def test_imports():
    """Test of alle benodigde modules kunnen worden geïmporteerd"""
    log_step("Testen van module imports...")

    modules_to_test = [
        "src.utils.config",
        "src.utils.logger",
        "src.connector.mt5_connector",
        "src.risk.risk_manager",
        "src.strategy.turtle_strategy",
        "src.strategy.strategy_factory",
        "src.analysis.backtester",
        "src.ftmo.ftmo_validator"
    ]

    all_passed = True
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            log_pass(f"Module {module_name} succesvol geïmporteerd")
        except ImportError as e:
            log_fail(f"Kan module {module_name} niet importeren: {e}")
            all_passed = False

    return all_passed


def test_config_loading():
    """Test of de configuratie correct kan worden geladen"""
    log_step("Testen van configuratie laden...")

    from src.utils.config import load_config

    # Test standaard config
    try:
        default_config = load_config()
        if default_config and isinstance(default_config, dict):
            log_pass("Standaard configuratie succesvol geladen")
        else:
            log_fail("Standaard configuratie niet correct geladen")
            return False
    except Exception as e:
        log_fail(f"Fout bij laden standaard configuratie: {e}")
        return False

    # Maak een test config file
    test_config_path = os.path.join(script_dir, "test_config.json")
    test_config = {
        "mt5": {
            "login": 1234567,
            "password": "test_password",
            "server": "Demo-Server",
            "symbols": ["EURUSD", "GBPUSD"],
            "timeframe": "H4",
            "account_balance": 100000
        },
        "risk": {
            "max_risk_per_trade": 0.01,
            "max_daily_drawdown": 0.05,
            "max_total_drawdown": 0.10,
            "leverage": 30
        },
        "strategy": {
            "name": "turtle",
            "swing_mode": False,
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 20,
            "atr_multiplier": 2.0
        },
        "logging": {
            "log_file": "logs/test_log.csv",
            "log_level": "INFO"
        }
    }

    try:
        with open(test_config_path, "w") as f:
            json.dump(test_config, f, indent=4)

        # Laad test config
        test_loaded_config = load_config(test_config_path)
        if test_loaded_config and isinstance(test_loaded_config, dict):
            log_pass("Test configuratie succesvol geladen")
        else:
            log_fail("Test configuratie niet correct geladen")
            return False

        # Verwijder test config file
        os.remove(test_config_path)

    except Exception as e:
        log_fail(f"Fout bij test configuratie: {e}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False

    return True


def test_logger():
    """Test of de logger correct werkt"""
    log_step("Testen van logger...")

    from src.utils.logger import Logger

    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "test_log.csv")

    try:
        # Maak logger aan
        logger = Logger(log_file)

        # Test logging methoden
        logger.log_info("Test info bericht")
        logger.log_info("Test warning bericht", level="WARNING")
        logger.log_info("Test error bericht", level="ERROR")

        logger.log_trade("EURUSD", "BUY", 1.2000, 0.1, 1.1950, 1.2100, "Test trade")

        account_info = {
            "balance": 100000,
            "equity": 100050,
            "margin": 500,
            "free_margin": 99550,
            "margin_level": 20010.0,
            "profit": 50
        }
        open_positions = {
            "EURUSD": [{
                "symbol": "EURUSD",
                "volume": 0.1,
                "profit": 50
            }]
        }
        logger.log_status(account_info, open_positions)

        # Controleer of bestand is aangemaakt
        if os.path.exists(log_file):
            log_pass(f"Logger heeft succesvol geschreven naar {log_file}")
        else:
            log_fail(f"Logger kon niet schrijven naar {log_file}")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen logger: {e}")
        return False

    return True


def test_risk_manager():
    """Test of de RiskManager correct werkt"""
    log_step("Testen van RiskManager...")

    from src.risk.risk_manager import RiskManager
    from src.utils.logger import Logger

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    config = {
        "max_risk_per_trade": 0.01,
        "max_daily_drawdown": 0.05,
        "max_total_drawdown": 0.10,
        "leverage": 30,
        "account_balance": 100000
    }

    try:
        risk_manager = RiskManager(config, logger)

        # Test positiegrootte berekening
        position_size = risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=1.2000,
            stop_loss=1.1950,
            account_balance=100000,
            trend_strength=0.5
        )

        if position_size > 0:
            log_pass(f"Positiegrootte berekening succesvol: {position_size} lots")
        else:
            log_fail(f"Positiegrootte berekening onjuist: {position_size}")
            return False

        # Test FTMO limieten checks
        account_info = {"balance": 100000, "equity": 100000}
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)

        if not should_stop:
            log_pass("FTMO limieten check succesvol (geen limieten overschreden)")
        else:
            log_fail(f"FTMO limieten check onjuist: {reason}")
            return False

        # Test trade risico check
        result = risk_manager.check_trade_risk("EURUSD", 0.1, 1.2000, 1.1950)

        if result:
            log_pass("Trade risico check succesvol")
        else:
            log_fail("Trade risico check gefaald")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen RiskManager: {e}")
        return False

    return True


def test_strategy_factory():
    """Test of de StrategyFactory correct werkt"""
    log_step("Testen van StrategyFactory...")

    from src.strategy.strategy_factory import StrategyFactory
    from src.utils.logger import Logger

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    config = {
        "mt5": {
            "login": 1234567,
            "password": "test_password",
            "server": "Demo-Server",
            "symbols": ["EURUSD", "GBPUSD"],
            "timeframe": "H4",
            "account_balance": 100000
        },
        "risk": {
            "max_risk_per_trade": 0.01,
            "max_daily_drawdown": 0.05,
            "max_total_drawdown": 0.10,
            "leverage": 30
        },
        "strategy": {
            "name": "turtle",
            "swing_mode": False,
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 20,
            "atr_multiplier": 2.0
        }
    }

    try:
        # Test beschikbare strategieën ophalen
        available_strategies = StrategyFactory.list_available_strategies()

        if "turtle" in available_strategies:
            log_pass(f"StrategyFactory lijst van strategieën succesvol: {available_strategies}")
        else:
            log_fail(f"StrategyFactory lijst van strategieën mist 'turtle': {available_strategies}")
            return False

        # Test strategie maken
        # Maak dummy connector en risk manager
        connector = type('DummyConnector', (), {})()
        risk_manager = type('DummyRiskManager', (), {})()

        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config
        )

        if strategy and strategy.get_name() == "Turtle Trading Strategy":
            log_pass("StrategyFactory succesvol strategie aangemaakt")
        else:
            log_fail(
                f"StrategyFactory kon geen strategie aanmaken of verkeerde naam: {strategy.get_name() if strategy else None}")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen StrategyFactory: {e}")
        return False

    return True


def run_tests():
    """Voer alle tests uit en rapporteer resultaten"""
    print("\n" + "=" * 80)
    print(f"SOPHY FRAMEWORK VERIFICATIE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    tests = [
        ("Module imports", test_imports),
        ("Config laden", test_config_loading),
        ("Logger", test_logger),
        ("RiskManager", test_risk_manager),
        ("StrategyFactory", test_strategy_factory),
    ]

    results = {}
    all_passed = True

    for test_name, test_func in tests:
        print(f"\nUitvoeren test: {test_name}")
        try:
            result = test_func()
            results[test_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Onverwachte fout bij test {test_name}: {e}")
            results[test_name] = False
            all_passed = False

    # Samenvattingsrapport
    print("\n" + "=" * 80)
    print("TESTRESULTATEN SAMENVATTING")
    print("=" * 80)

    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{status:10} - {test_name}")

    print("\n" + "=" * 80)
    overall_status = "PASSED" if all_passed else "FAILED"
    print(f"EINDRESULTAAT: {overall_status}")
    print("=" * 80 + "\n")

    return all_passed


if __name__ == "__main__":
    run_tests()