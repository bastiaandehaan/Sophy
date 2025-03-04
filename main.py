import time
import json
import os
import logging
from datetime import datetime, timedelta
from modules.mt5_connector import MT5Connector
from modules.risk_manager import RiskManager
from modules.startegy.turtle import TurtleStrategy
from analysis.backtester import Backtester
from utils.logger import Logger
from utils.visualizer import Visualizer

# Logging configuratie
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("logs/turtle_trader.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, config_path="config/config.json"):
        """Initialiseer de trading bot met configuratie en modules."""
        self.config = self._load_config(config_path)
        self.connector = MT5Connector(self.config["mt5"])
        self.risk_manager = RiskManager(
            max_risk_per_trade=self.config["risk"]["max_risk_per_trade"],
            max_daily_drawdown=self.config["risk"]["max_daily_drawdown"],
            max_total_drawdown=self.config["risk"]["max_total_drawdown"],
            leverage=self.config["risk"]["leverage"]
        )
        self.logger = Logger(self.config["log_file"])
        self.visualizer = Visualizer(self.config["log_file"], self.config["output_dir"])
        self.strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, self.config)
        self.backtester = Backtester(self.connector, self.config)  # Voeg Backtester toe
        self.is_running = False

        if not self.connector.connect():
            raise ConnectionError("Kan niet verbinden met MT5")

    def _load_config(self, config_path):
        """Laad configuratie uit JSON-bestand."""
        if not os.path.exists(config_path):
            logger.error(f"Configuratiebestand niet gevonden: {config_path}")
            raise FileNotFoundError(f"{config_path} bestaat niet")
        with open(config_path, "r") as f:
            return json.load(f)

    def start(self):
        """Start de bot bij markopening."""
        market_open = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        if datetime.now() < market_open:
            wait_time = (market_open - datetime.now()).total_seconds()
            logger.info(f"Wachten tot markopening om {market_open}. Slaaptijd: {wait_time} seconden.")
            time.sleep(wait_time)

        self.is_running = True
        logger.info("Trading bot gestart.")
        while self.is_running:
            self._run_cycle()
            time.sleep(300)  # Controleer elke 5 minuten

    def _run_cycle(self):
        """Voer één cyclus van de tradingstrategie uit."""
        try:
            if not self.risk_manager.can_trade():
                logger.warning("Dagelijkse risicolimiet bereikt. Pauzeer trading.")
                return

            for symbol in self.config["mt5"]["symbols"]:
                self.strategy.process_symbol(symbol)

            account_info = self.connector.get_account_info()
            open_positions = self.strategy.get_open_positions()
            self.logger.log_status(account_info, open_positions)

            stop_trading, reason = self.strategy.check_daily_limit()
            if stop_trading:
                logger.info(f"Stop trading: {reason}")
                self.is_running = False
                self.visualizer.plot_equity_curve()
                self.visualizer.plot_trade_results()
                self.visualizer.plot_performance_summary()

        except Exception as e:
            logger.error(f"Fout in cyclus: {e}")
            self.is_running = False

    def stop(self):
        """Stop de bot en ruim op."""
        self.is_running = False
        self.connector.disconnect()
        logger.info("Trading bot gestopt.")

    def test_connection(self):
        """Test de verbinding met MT5."""
        logger.info("Test verbinding met MT5...")
        account_info = self.connector.get_account_info()
        if account_info:
            logger.info("✅ Verbinding met MT5 succesvol!")
            logger.info(f"Account balans: {account_info.get('balance', 'Onbekend')}")
            logger.info(f"Account equity: {account_info.get('equity', 'Onbekend')}")
            logger.info(f"Account leverage: 1:{account_info.get('leverage', 'Onbekend')}")
            symbol = self.config["mt5"]["symbols"][0]
            timeframe_str = self.config["mt5"].get("timeframe", "H4")
            timeframe = self.connector.get_timeframe_constant(timeframe_str)
            df = self.connector.get_historical_data(symbol, timeframe, 10)
            if not df.empty:
                logger.info(f"✅ Data succesvol opgehaald voor {symbol} ({timeframe_str})")
                logger.info(df.tail(3).to_string())
            else:
                logger.info(f"❌ Geen data opgehaald voor {symbol}")
        else:
            logger.error("❌ Kon geen verbinding maken met MT5")

    def run_backtest(self):
        """Voer een backtest uit met de bestaande Backtester-module."""
        logger.info("Backtesting module gestart...")
        end_date = datetime.now()
        period_choice = input("Backtest periode (1=1 maand, 3=3 maanden, 6=6 maanden, 12=1 jaar, 24=2 jaar): ")
        months = int(period_choice) if period_choice in ['1', '3', '6', '12', '24'] else 6
        start_date = end_date - timedelta(days=30 * months)
        logger.info(f"Backtest periode: {start_date.strftime('%Y-%m-%d')} tot {end_date.strftime('%Y-%m-%d')}")

        timeframe_str = self.config["mt5"].get("timeframe", "H4")
        timeframe = self.connector.get_timeframe_constant(timeframe_str)

        for symbol in self.config["mt5"]["symbols"]:
            logger.info(f"\nBacktesting strategie op {symbol}...")
            custom_params = {
                'entry_period': 40 if self.config['mt5'].get('swing_mode', False) else 20,
                'exit_period': 20 if self.config['mt5'].get('swing_mode', False) else 10,
                'atr_period': 20,
                'atr_multiplier': 2.5 if self.config['mt5'].get('swing_mode', False) else 2.0,
                'risk_per_trade': self.config['mt5']['risk_per_trade'],
                'use_trend_filter': True
            }
            result_df = self.backtester.run_backtest(symbol, start_date, end_date, timeframe, custom_params)
            if result_df is not None:
                self.backtester.plot_results(result_df, symbol, f"{symbol}_backtest_results.png")

        if input("Wil je parameter optimalisatie uitvoeren? (j/n): ").lower() == 'j':
            symbol = self.config["mt5"]["symbols"][0]
            logger.info(f"\nParameter optimalisatie voor {symbol}...")
            param_grid = {
                'entry_period': [30, 40, 50, 60],
                'exit_period': [15, 20, 25, 30],
                'atr_multiplier': [2.0, 2.5, 3.0, 3.5],
                'use_trend_filter': [True]
            } if self.config['mt5'].get('swing_mode', False) else {
                'entry_period': [10, 20, 30, 40],
                'exit_period': [5, 10, 15, 20],
                'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
                'use_trend_filter': [True, False]
            }
            best_params = self.backtester.optimize_parameters(symbol, start_date, end_date, param_grid)
            logger.info("\nTesten van beste parameters...")
            result_df = self.backtester.run_backtest(symbol, start_date, end_date, timeframe, best_params['best_return_params'])
            self.backtester.plot_results(result_df, symbol, f"{symbol}_optimized_backtest.png")

    def analyze_performance(self):
        """Analyseer trading performance."""
        logger.info("Performance analyse gestart...")
        if not os.path.exists(self.config["log_file"]):
            logger.warning(f"Log bestand niet gevonden: {self.config['log_file']}. Voer eerst de bot uit om logs te genereren.")
            return

        try:
            logger.info("Genereren van equity curve...")
            equity_path = self.visualizer.plot_equity_curve()
            logger.info("Genereren van trades overzicht...")
            trades_path = self.visualizer.plot_trade_results()
            logger.info("Genereren van performance samenvatting...")
            summary_path = self.visualizer.plot_performance_summary()
            logger.info("\nAnalyse voltooid. Grafieken opgeslagen in 'data/analysis' map:")
            if equity_path:
                logger.info(f"- Equity curve: {os.path.basename(equity_path)}")
            if trades_path:
                logger.info(f"- Trades overzicht: {os.path.basename(trades_path)}")
            if summary_path:
                logger.info(f"- Performance samenvatting: {os.path.basename(summary_path)}")
        except Exception as e:
            logger.error(f"Fout tijdens analyse: {e}")
            import traceback
            traceback.print_exc()

def run_menu():
    """Toon een menu en roep de juiste methode aan."""
    logger.info("\n==== TurtleTrader FTMO Swing Edition ====")
    logger.info("1. Start Live Trading")
    logger.info("2. Run Connection Test")
    logger.info("3. Run Backtest")
    logger.info("4. Analyze Performance")
    logger.info("0. Exit")

    choice = input("\nKies een optie: ")
    bot = TradingBot()

    if choice == "1":
        bot.start()
    elif choice == "2":
        bot.test_connection()
    elif choice == "3":
        bot.run_backtest()
    elif choice == "4":
        bot.analyze_performance()
    elif choice == "0":
        logger.info("Programma afgesloten")
    else:
        logger.warning("Ongeldige keuze")
    bot.stop()

if __name__ == "__main__":
    try:
        run_menu()
    except Exception as e:
        logger.critical(f"Programma mislukt: {e}")
    finally:
        logger.info("Sessie afgesloten.")