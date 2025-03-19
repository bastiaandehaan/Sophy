#!/usr/bin/env python3
"""
Sophy Framework Verificatiescript

Dit script voert een reeks tests uit om te controleren of de Sophy Trading Framework
correct is geïnstalleerd en de basisfunctionaliteit werkt.
"""
import importlib
import json
import os
import sys
from datetime import datetime

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
        "src.strategy.base_strategy",
        "src.analysis.backtester",
        "src.ftmo.validator.py",
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
        },
        "risk": {
            "risk_per_trade": 0.01,
            "daily_drawdown_limit": 0.05,
            "total_drawdown_limit": 0.10,
            "initial_balance": 100000,
        },
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
        "logging": {"log_file": "logs/test_log.csv", "log_level": "INFO"},
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

        # Test logging methoden - LET OP: Gebruik log_info i.p.v. info!
        logger.log_info("Test info bericht")
        logger.log_info("Test warning bericht", level="WARNING")
        logger.log_info("Test error bericht", level="ERROR")

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

    # Patch de logger om compatibel te zijn met RiskManager verwachtingen
    # Dit zorgt ervoor dat calls naar logger.info worden omgeleid naar logger.log_info
    logger.info = logger.log_info
    logger.warning = lambda msg: logger.log_info(msg, level="WARNING")
    logger.error = lambda msg: logger.log_info(msg, level="ERROR")

    # Creëer een mock MT5Connector
    class MockMT5Connector:
        def get_account_info(self):
            return {
                "balance": 100000,
                "equity": 100000,
                "margin": 1000,
                "free_margin": 99000,
                "margin_level": 10000.0,
            }

        def get_symbol_info(self, symbol):
            return {
                "trade_tick_value": 0.0001,
                "trade_contract_size": 100000,
                "trade_tick_size": 0.00001,
                "volume_step": 0.01,
                "volume_min": 0.01,
                "volume_max": 100.0,
            }

    mock_connector = MockMT5Connector()

    config = {
        "risk_per_trade": 0.01,
        "daily_drawdown_limit": 0.05,
        "total_drawdown_limit": 0.10,
        "initial_balance": 100000,
        "max_trades_per_day": 5,
        "profit_target": 0.10,
    }

    try:
        # Initialiseer de risk manager met de mock connector
        risk_manager = RiskManager(config, logger, mock_connector)
        risk_manager.initialize()  # Dit initialiseert de risk manager met het account saldo

        # Test positiegrootte berekening
        position_size = risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=1.2000,
            stop_loss=1.1950,
            risk_pips=50.0,  # 50 pips risico
        )

        if position_size > 0:
            log_pass(f"Positiegrootte berekening succesvol: {position_size} lots")
        else:
            log_fail(f"Positiegrootte berekening onjuist: {position_size}")
            return False

        # Test FTMO status
        ftmo_status = risk_manager.get_ftmo_status()

        if ftmo_status and isinstance(ftmo_status, dict):
            log_pass("FTMO status check succesvol")
        else:
            log_fail("FTMO status check gefaald")
            return False

        # Test trading_allowed check
        is_allowed = risk_manager.is_trading_allowed

        if is_allowed is True:
            log_pass("Trading allowed check succesvol (trading is toegestaan)")
        else:
            log_fail(
                "Trading allowed check onjuist (trading zou toegestaan moeten zijn)"
            )
            return False

    except Exception as e:
        log_fail(f"Fout bij testen RiskManager: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def test_strategy_factory():
    """Test of de StrategyFactory correct werkt"""
    log_step("Testen van StrategyFactory...")

    from src.strategy.strategy_factory import StrategyFactory
    from src.utils.logger import Logger

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    # Patch de logger om compatibel te zijn met strategie verwachtingen
    logger.info = logger.log_info
    logger.warning = lambda msg: logger.log_info(msg, level="WARNING")
    logger.error = lambda msg: logger.log_info(msg, level="ERROR")

    # Creëer een mock connector die de verwachte methoden implementeert
    class MockConnector:
        def get_historical_data(self, symbol, timeframe, num_bars):
            import pandas as pd
            import numpy as np

            # Genereer mock data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=num_bars)
            data = pd.DataFrame(
                {
                    "open": np.linspace(1.1, 1.2, num_bars),
                    "high": np.linspace(1.12, 1.22, num_bars),
                    "low": np.linspace(1.09, 1.19, num_bars),
                    "close": np.linspace(1.11, 1.21, num_bars),
                },
                index=dates,
            )
            return data

        def get_position(self, symbol):
            return None

        def get_open_positions(self):
            return {}

    # Creëer mock risk manager
    class MockRiskManager:
        def __init__(self):
            self.is_trading_allowed = True

        def calculate_position_size(
            self, symbol, entry_price, stop_loss=None, risk_pips=None
        ):
            return 0.1

    config = {
        "strategy": {
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 14,
            "atr_multiplier": 2.0,
            "use_filters": True,
            "filter_period": 50,
        },
        "timeframe": "D1",
    }

    try:
        mock_connector = MockConnector()
        mock_risk_manager = MockRiskManager()

        # Test beschikbare strategieën ophalen
        available_strategies = StrategyFactory.list_available_strategies()

        if isinstance(available_strategies, list):
            log_pass(
                f"StrategyFactory beschikbare strategieën opgehaald: {available_strategies}"
            )
        else:
            log_fail("StrategyFactory kon geen lijst van strategieën ophalen")
            return False

        # Strategie maken
        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=mock_connector,
            risk_manager=mock_risk_manager,
            logger=logger,
            config=config,
        )

        if strategy:
            log_pass(
                f"StrategyFactory strategie succesvol aangemaakt: {strategy.get_name()}"
            )
        else:
            log_fail("StrategyFactory kon geen strategie aanmaken")
            return False

        # Test of de strategie de juiste methoden heeft
        if hasattr(strategy, "process_symbol") and callable(
            getattr(strategy, "process_symbol")
        ):
            log_pass("Strategie heeft de verwachte 'process_symbol' methode")
        else:
            log_fail("Strategie mist de verwachte 'process_symbol' methode")
            return False

        if hasattr(strategy, "calculate_indicators") and callable(
            getattr(strategy, "calculate_indicators")
        ):
            log_pass("Strategie heeft de verwachte 'calculate_indicators' methode")
        else:
            log_fail("Strategie mist de verwachte 'calculate_indicators' methode")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen StrategyFactory: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def test_turtle_strategy():
    """Test of de TurtleStrategy correct werkt"""
    log_step("Testen van TurtleStrategy...")

    from src.strategy.turtle_strategy import TurtleStrategy
    from src.utils.logger import Logger
    import pandas as pd
    import numpy as np

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    # Patch de logger om compatibel te zijn met strategie verwachtingen
    logger.info = logger.log_info
    logger.warning = lambda msg: logger.log_info(msg, level="WARNING")
    logger.error = lambda msg: logger.log_info(msg, level="ERROR")

    # Creëer mock connector
    class MockConnector:
        def get_historical_data(self, symbol, timeframe, num_bars):
            # Genereer mock data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=num_bars)
            data = pd.DataFrame(
                {
                    "open": np.linspace(1.1, 1.2, num_bars),
                    "high": np.linspace(1.12, 1.22, num_bars),
                    "low": np.linspace(1.09, 1.19, num_bars),
                    "close": np.linspace(1.11, 1.21, num_bars),
                },
                index=dates,
            )

            # Voeg een breakout toe
            if num_bars > 50:
                data.loc[dates[-10] :, "high"] *= 1.02

            return data

        def get_position(self, symbol):
            return None

        def get_open_positions(self):
            return {}

    # Creëer mock risk manager
    class MockRiskManager:
        def __init__(self):
            self.is_trading_allowed = True

        def calculate_position_size(
            self, symbol, entry_price, stop_loss=None, risk_pips=None
        ):
            return 0.1

    # Configuratie voor de strategie
    config = {
        "strategy": {
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 14,
            "atr_multiplier": 2.0,
            "use_filters": True,
            "filter_period": 50,
        },
        "timeframe": "D1",
    }

    try:
        mock_connector = MockConnector()
        mock_risk_manager = MockRiskManager()

        # Initialiseer strategie
        strategy = TurtleStrategy(mock_connector, mock_risk_manager, logger, config)

        # Test process_symbol methode
        result = strategy.process_symbol("EURUSD")

        if result and isinstance(result, dict) and "signal" in result:
            log_pass(f"TurtleStrategy process_symbol succesvol: {result['signal']}")
        else:
            log_fail(f"TurtleStrategy process_symbol gefaald: {result}")
            return False

        # Test calculate_indicators methode
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

        indicators = strategy.calculate_indicators(data)

        if indicators and isinstance(indicators, dict) and "data" in indicators:
            log_pass("TurtleStrategy calculate_indicators succesvol")
        else:
            log_fail("TurtleStrategy calculate_indicators gefaald")
            return False

        # Test on_order_filled methode
        try:
            strategy.on_order_filled(
                symbol="EURUSD",
                order_type="BUY",
                price=1.2000,
                volume=0.1,
                order_id="12345",
                timestamp="2023-01-01 12:00:00",
            )
            log_pass("TurtleStrategy on_order_filled succesvol")
        except Exception as e:
            log_fail(f"TurtleStrategy on_order_filled gefaald: {e}")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen TurtleStrategy: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def run_tests():
    """Voer alle tests uit en rapporteer resultaten"""
    print("\n" + "=" * 80)
    print(
        f"SOPHY FRAMEWORK VERIFICATIE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print("=" * 80)

    tests = [
        ("Module imports", test_imports),
        ("Config laden", test_config_loading),
        ("Logger", test_logger),
        ("RiskManager", test_risk_manager),
        ("StrategyFactory", test_strategy_factory),
        ("TurtleStrategy", test_turtle_strategy),
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
            import traceback

            traceback.print_exc()
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
