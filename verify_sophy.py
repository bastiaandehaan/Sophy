#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logger():
    """Maakt een simpele logging helper."""
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/verify_sophy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def log(message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
        print(f"[{level}] {message}")

    return log


def find_config_file(log, config_path=None):
    """Zoekt het configuratiebestand op verschillende locaties."""
    if config_path and os.path.exists(config_path):
        log(f"Configuratiebestand gevonden op opgegeven pad: {config_path}", "SUCCESS")
        return config_path

    # Mogelijke locaties
    possible_paths = [
        "config/settings.json",
        "settings.json",
        "../config/settings.json",
        str(Path.home() / "Sophy/config/settings.json"),
        os.path.join(os.path.dirname(__file__), "config/settings.json"),
        os.path.join(os.path.dirname(__file__), "settings.json"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            log(f"Configuratiebestand gevonden: {path}", "SUCCESS")
            return path

    # Als laatste redmiddel, zoek door het hele project
    for root, dirs, files in os.walk("."):
        if "settings.json" in files:
            path = os.path.join(root, "settings.json")
            log(f"Configuratiebestand gevonden via zoeken: {path}", "SUCCESS")
            return path

    log("Configuratiebestand niet gevonden op standaard locaties", "ERROR")
    return None


def check_mt5_executable(log, path):
    """Controleert of MT5 executable bestaat."""
    if not path:
        log("MT5 pad niet opgegeven in configuratie", "WARNING")
        return False

    if not os.path.exists(path):
        log(f"MT5 executable niet gevonden op pad: {path}", "ERROR")
        log("Controleer of FTMO MetaTrader 5 correct is geïnstalleerd", "INFO")
        return False

    log(f"MT5 executable gevonden: {path}", "SUCCESS")
    return True


def check_required_packages(log):
    """Controleert of alle benodigde packages geïnstalleerd zijn."""
    required = [
        "MetaTrader5",
        "pandas",
        "numpy",
        "matplotlib",
        "backtrader",
        "seaborn",
        "pytest",
    ]

    missing = []
    for package in required:
        try:
            __import__(package)
            log(f"Package {package} is geïnstalleerd", "SUCCESS")
        except ImportError:
            log(f"Benodigde package {package} is niet geïnstalleerd", "ERROR")
            missing.append(package)

    if missing:
        log(
            f"Installeer missende packages met: pip install {' '.join(missing)}", "INFO"
        )
        return False
    return True


def validate_config(log, config):
    """Valideert de configuratie uitgebreid."""
    required_sections = ["mt5", "risk", "strategy"]
    missing_sections = [s for s in required_sections if s not in config]

    if missing_sections:
        log(
            f"Configuratie mist verplichte secties: {', '.join(missing_sections)}",
            "ERROR",
        )
        return False

    # Controleer MT5 sectie
    mt5_section = config.get("mt5", {})
    required_mt5_fields = ["login", "password", "server"]
    missing_mt5_fields = [f for f in required_mt5_fields if f not in mt5_section]

    if missing_mt5_fields:
        log(
            f"MT5 configuratie mist verplichte velden: {', '.join(missing_mt5_fields)}",
            "ERROR",
        )
        return False

    # Controleer risk sectie
    risk_section = config.get("risk", {})
    if "risk_per_trade" not in risk_section:
        log("Risk configuratie mist 'risk_per_trade' parameter", "WARNING")

    # Controleer symbols configuration
    if not mt5_section.get("symbols"):
        log("Geen handelssymbolen geconfigureerd in MT5 sectie", "WARNING")

    log("Configuratie is geldig en bevat alle benodigde secties", "SUCCESS")
    return True


def check_directories(log, config):
    """Controleert of alle benodigde directories bestaan."""
    # Definieer standaardwaarden voor ontbrekende configuratie
    log_dir = config.get("logging", {}).get("log_file", "logs/trading_log.csv")
    log_dir = os.path.dirname(log_dir)

    data_dir = config.get("output", {}).get("data_dir", "data")
    backtest_dir = config.get("output", {}).get(
        "backtest_results_dir", "backtest_results"
    )

    dirs = [log_dir, data_dir, backtest_dir]

    for d in dirs:
        if not os.path.exists(d):
            try:
                os.makedirs(d, exist_ok=True)
                log(f"Directory {d} aangemaakt", "SUCCESS")
            except Exception as e:
                log(f"Kon directory {d} niet aanmaken: {str(e)}", "ERROR")
                return False
        else:
            log(f"Directory {d} bestaat", "SUCCESS")

    return True


def check_mt5_connectivity(log, config):
    """Controleert connectiviteit met MT5."""
    try:
        # Importeer alleen bij deze test
        from src.connector.mt5_connector import MT5Connector
        from src.utils.logger import Logger

        test_logger = Logger("logs/connectivity_test.csv")
        connector = MT5Connector(config.get("mt5", {}), test_logger)

        log("MT5 connector succesvol geïnitialiseerd", "SUCCESS")

        # Probeer verbinding te maken
        log("Proberen te verbinden met MT5...")
        if connector.connect(show_dialog=False):
            log("Verbinding met MT5 succesvol", "SUCCESS")

            # Probeer account info op te halen
            account_info = connector.get_account_info()
            if account_info:
                log(
                    f"Account info opgehaald: Balance={account_info.get('balance', 'N/A')}",
                    "SUCCESS",
                )
            else:
                log("Kon account info niet ophalen", "WARNING")

            # Verbreek verbinding
            connector.disconnect()
            log("MT5 verbinding verbroken", "SUCCESS")
            return True
        else:
            log("Kon geen verbinding maken met MT5", "ERROR")
            log("Controleer login, password en server instellingen", "INFO")
            return False

    except Exception as e:
        log(f"Fout bij testen MT5 connectiviteit: {str(e)}", "ERROR")
        return False


def check_project_structure(log):
    """Controleert of de belangrijkste modules en bestanden aanwezig zijn."""
    required_files = [
        "run.py",
        "src/strategy/turtle_strategy.py",
        "src/connector/mt5_connector.py",
        "src/risk/risk_manager.py",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            log(f"Essentieel bestand ontbreekt: {file_path}", "ERROR")
            missing_files.append(file_path)

    if missing_files:
        return False

    log("Alle essentiële projectbestanden zijn aanwezig", "SUCCESS")
    return True


def create_config_dir_and_copy_settings(log):
    """Kopieert settings.json naar config/ map als deze niet bestaat."""
    if os.path.exists("settings.json") and not os.path.exists("config/settings.json"):
        try:
            os.makedirs("config", exist_ok=True)
            import shutil

            shutil.copy("settings.json", "config/settings.json")
            log("settings.json gekopieerd naar config/settings.json", "SUCCESS")
            return True
        except Exception as e:
            log(f"Kon settings.json niet kopiëren naar config/: {str(e)}", "ERROR")
    return False


def main():
    """Hoofdfunctie voor verificatie van Sophy setup."""
    # Argumenten parser
    parser = argparse.ArgumentParser(
        description="Verificatie tool voor Sophy Trading System"
    )
    parser.add_argument(
        "--config",
        default="config/settings.json",
        help="Pad naar configuratiebestand (default: config/settings.json)",
    )
    parser.add_argument(
        "--skip-mt5-test", action="store_true", help="Sla MT5 connectiviteitstest over"
    )

    args = parser.parse_args()
    log = setup_logger()

    log("Sophy Trading System verificatie gestart...")
    log(f"Huidige map: {os.getcwd()}")

    # Zorg dat project root in de Python path staat
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    # Probeer settings.json te kopiëren als deze op de verkeerde plek staat
    create_config_dir_and_copy_settings(log)

    # Laad configuratie
    config_path = find_config_file(log, args.config)
    if not config_path:
        log("Oplossingsmogelijkheden:", "INFO")
        log("1. Kopieer je settings.json naar de map config/", "INFO")
        log("2. Geef het volledige pad op met --config argument", "INFO")
        log("3. Plaats het bestand in één van de gezochte locaties", "INFO")
        sys.exit(1)

    try:
        from src.utils.config import load_config

        config = load_config(config_path)
        log(f"Configuratie geladen uit {config_path}", "SUCCESS")
    except Exception as e:
        log(f"Kon configuratie niet laden: {str(e)}", "ERROR")
        log("Controleer of het configuratiebestand geldige JSON bevat", "INFO")
        sys.exit(1)

    # Voer alle tests uit
    checks = [
        (check_project_structure, []),
        (check_required_packages, []),
        (validate_config, [config]),
        (check_directories, [config]),
        (check_mt5_executable, [config.get("mt5", {}).get("mt5_pathway")]),
    ]

    # Voeg MT5 connectiviteitstest toe indien niet overgeslagen
    if not args.skip_mt5_test:
        checks.append((check_mt5_connectivity, [config]))

    # Voer tests uit
    all_passed = True
    results = {}

    for check_func, check_args in checks:
        check_name = check_func.__name__
        try:
            result = check_func(log, *check_args)
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            log(f"Fout bij uitvoeren van {check_name}: {str(e)}", "ERROR")
            results[check_name] = False
            all_passed = False

    # Toon resultaat
    log("\n=== Verificatie Resultaten ===")
    for check_name, result in results.items():
        status = "GESLAAGD" if result else "MISLUKT"
        log(f"{check_name}: {status}")

    if all_passed:
        log(
            "\nAlle tests geslaagd! Sophy Trading System is klaar voor gebruik.",
            "SUCCESS",
        )
    else:
        log(
            "\nSommige tests zijn mislukt. Los de bovenstaande fouten op voor optimale werking.",
            "WARNING",
        )

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
