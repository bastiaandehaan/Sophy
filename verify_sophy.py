import os
import sys
from src.utils.config import load_config

def check_mt5_executable(path):
    if not os.path.exists(path):
        print(f"MT5 executable not found at {path}")
        return False
    return True

def check_required_packages():
    required = ['MetaTrader5', 'pandas', 'numpy']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"Required package {package} is not installed")
            return False
    return True

def validate_config(config):
    if "mt5" not in config or "risk" not in config or "strategy" not in config:
        print("Configuration is missing required sections")
        return False
    return True

def check_directories(config):
    dirs = [
        os.path.dirname(config["logging"]["log_file"]),  # "logs"
        config["output"]["data_dir"],                    # "data"
        config["output"]["backtest_results_dir"]         # "backtest_results"
    ]
    for d in dirs:
        if not os.path.exists(d):
            try:
                os.makedirs(d)
                print(f"Created directory {d}")
            except Exception as e:
                print(f"Failed to create directory {d}: {e}")
                return False
    return True

def main():
    print("Verifying Sophy setup...")
    config = load_config("config/settings.json")
    if not config:
        print("Failed to load configuration")
        sys.exit(1)

    checks = [
        (check_mt5_executable, [config["mt5"]["mt5_pathway"]]),
        (check_required_packages, []),
        (validate_config, [config]),
        (check_directories, [config])
    ]

    all_passed = True
    for check, args in checks:
        if not check(*args):
            all_passed = False

    if all_passed:
        print("All checks passed. Sophy is ready to use.")
    else:
        print("Some checks failed. Please review the errors above.")

if __name__ == "__main__":
    main()
