# scripts/main.py
# Main script voor Sophy Trading Framework
# Implementeert verschillende trading modes en integreert alle componenten

import argparse
import json
import os
import time
from datetime import datetime

import pandas as pd

# Gewijzigd: Gebruik de bestaande backtrader_integration in plaats van advanced_backtester
from src.analysis.backtrader_integration import BacktestingManager
from src.connector.mt5_connector import MT5Connector
from src.ftmo.validator import FTMOValidator
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Sophy Trading Framework")

    parser.add_argument(
        "--mode",
        type=str,
        choices=["live", "backtest", "paper"],
        default="backtest",
        help="Trading modus (live/backtest/paper)",
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config/settings.json",
        help="Pad naar configuratiebestand",
    )

    parser.add_argument(
        "--strategy_config",
        type=str,
        default="config/strategy_config.json",
        help="Pad naar strategie configuratiebestand",
    )

    parser.add_argument(
        "--strategy",
        type=str,
        default="turtle",
        help="Te gebruiken strategie (turtle, turtle_swing, etc.)",
    )

    parser.add_argument(
        "--symbols",
        type=str,
        nargs="+",
        default=["EURUSD"],
        help="Lijst met te verhandelen symbolen",
    )

    parser.add_argument(
        "--timeframe",
        type=str,
        default="D1",
        help="Timeframe voor trading (M1, M5, M15, M30, H1, H4, D1, W1, MN1)",
    )

    parser.add_argument(
        "--start_date",
        type=str,
        default="2021-01-01",
        help="Startdatum voor backtest (YYYY-MM-DD)",
    )

    parser.add_argument(
        "--end_date",
        type=str,
        default="2023-01-01",
        help="Einddatum voor backtest (YYYY-MM-DD)",
    )

    return parser.parse_args()


def setup_trading_environment(args):
    """Setup de trading omgeving op basis van de configuratie."""
    # Laad configuratie
    config = load_config(args.config)
    strategy_config = load_config(args.strategy_config)

    # Combineer configuraties
    config["strategy"] = strategy_config
    config["strategy_name"] = args.strategy
    config["timeframe"] = args.timeframe
    config["symbols"] = args.symbols

    # Setup logging
    log_dir = config.get("log_dir", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir, f"trading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    logger = Logger(log_file)

    logger.info(f"Sophy Trading Framework gestart in {args.mode} modus")
    logger.info(f"Gekozen strategie: {args.strategy}")

    # Initialize MT5 connector
    mt5_connector = MT5Connector(config, logger)

    # Connect to MT5 (alleen nodig in live en paper modus)
    if args.mode in ["live", "paper"]:
        connected = mt5_connector.connect()
        if not connected:
            logger.error("MT5 verbinding mislukt. Programma wordt afgesloten.")
            return None

    # Initialiseer risicomanager
    risk_manager = RiskManager(config, logger, mt5_connector)

    # Initialiseer risicomanager alleen voor live en paper modes
    if args.mode in ["live", "paper"]:
        risk_manager.initialize()

    # Initialiseer strategie via factory
    strategy = StrategyFactory.create_strategy(
        args.strategy, mt5_connector, risk_manager, logger, config
    )

    logger.info(f"Strategie {strategy.get_name()} succesvol geïnitialiseerd")

    # Initialiseer backtester (alleen voor backtest)
    backtester = None
    if args.mode == "backtest":
        backtester = BacktestingManager(config, logger)

    # Initialiseer FTMO validator
    validator = FTMOValidator(config, logger)

    # Maak een omgevings-dictionary om alles terug te geven
    environment = {
        "config": config,
        "logger": logger,
        "mt5_connector": mt5_connector,
        "strategy": strategy,
        "risk_manager": risk_manager,
        "backtester": backtester,
        "validator": validator,
    }

    return environment


def run_live_trading(args, environment):
    """Run het live trading proces."""
    # Haal componenten uit de environment
    config = environment["config"]
    logger = environment["logger"]
    mt5_connector = environment["mt5_connector"]
    strategy = environment["strategy"]
    risk_manager = environment["risk_manager"]
    validator = environment["validator"]

    logger.info("Live trading gestart")

    # Handelsfrequentie in seconden (standaard 5 minuten)
    trading_interval = config.get("trading_interval", 300)

    # Trading loop
    try:
        while True:
            current_time = datetime.now()
            logger.info(f"Trading cyclus gestart: {current_time}")

            # Controleer of trading is toegestaan (FTMO-regels)
            if not risk_manager.is_trading_allowed:
                logger.warning("Trading is gestopt vanwege risicobeperkingen")
                break

            # Loop door alle symbolen
            for symbol in args.symbols:
                # Verwerk signalen voor dit symbool
                result = strategy.process_symbol(symbol)
                signal = result.get("signal", "GEEN")
                meta = result.get("meta", {})

                # Log signaal
                logger.info(f"Signaal voor {symbol}: {signal}")

                # Verwerk signaal
                if signal in ["BUY", "SELL"]:
                    # Bereken risico en positiegrootte
                    entry_price = meta.get("entry_price", 0)
                    stop_loss = meta.get("stop_loss")
                    risk_pips = meta.get("risk_pips")

                    volume = risk_manager.calculate_position_size(
                        symbol=symbol,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        risk_pips=risk_pips,
                    )

                    if volume > 0:
                        # Plaats order
                        order_result = mt5_connector.place_order(
                            symbol=symbol,
                            order_type=signal,
                            volume=volume,
                            price=0.0,  # Market order
                            stop_loss=stop_loss,
                            take_profit=None,
                            # Geen take profit (Turtle systeem gebruikt trailing exits)
                            comment=f"Sophy_{signal}",
                        )

                        if order_result:
                            logger.info(
                                f"Order geplaatst: {symbol} {signal}, volume={volume}"
                            )

                            # Informeer de strategie over de gevulde order
                            strategy.on_order_filled(
                                symbol=symbol,
                                order_type=signal,
                                price=entry_price,
                                volume=volume,
                                order_id=order_result.get("order_id", "unknown"),
                                timestamp=current_time.strftime("%Y-%m-%d %H:%M:%S"),
                            )
                        else:
                            logger.error(
                                f"Order plaatsen mislukt voor {symbol} {signal}"
                            )

                elif signal in ["CLOSE_BUY", "CLOSE_SELL"]:
                    # Sluit bestaande positie
                    close_result = mt5_connector.close_position(
                        symbol=symbol, comment=f"Sophy_{signal}"
                    )

                    if close_result:
                        logger.info(f"Positie gesloten: {symbol} {signal}")

                        # Informeer de strategie over de gesloten positie
                        strategy.on_order_filled(
                            symbol=symbol,
                            order_type=signal,
                            price=close_result.get("price", 0),
                            volume=close_result.get("volume", 0),
                            order_id=close_result.get("order_id", "unknown"),
                            timestamp=current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        )

                        # Update risk manager
                        risk_manager.update_after_trade(
                            symbol=symbol,
                            profit_loss=close_result.get("profit", 0),
                            close_time=current_time,
                        )
                    else:
                        logger.error(f"Positie sluiten mislukt voor {symbol}")

            # Controleer FTMO status
            ftmo_status = risk_manager.get_ftmo_status()
            logger.info(f"FTMO Status: {json.dumps(ftmo_status, indent=2)}")

            # Valideer FTMO regels
            validator.validate(ftmo_status)

            # Wacht tot volgende interval
            logger.info(f"Wachten tot volgende cyclus ({trading_interval} seconden)")
            time.sleep(trading_interval)

    except KeyboardInterrupt:
        logger.info("Trading onderbroken door gebruiker")
    except Exception as e:
        logger.error(f"Fout in trading loop: {str(e)}")
    finally:
        # Disconnect van MT5
        mt5_connector.disconnect()
        logger.info("Trading beëindigd, MT5 verbinding gesloten")


def run_backtest(args, environment):
    """Run het backtest proces."""
    # Haal componenten uit de environment
    config = environment["config"]
    logger = environment["logger"]
    strategy = environment["strategy"]
    backtester = environment["backtester"]
    validator = environment["validator"]

    logger.info("Backtest gestart")

    # Start- en einddatum converteren
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Resultaten map
    results_dir = config.get("backtest_results_dir", "backtest_results")
    os.makedirs(results_dir, exist_ok=True)

    # Configureer backtester
    config["output_dir"] = results_dir

    # Loop door alle symbolen
    all_results = {}

    for symbol in args.symbols:
        logger.info(f"Backtest voor {symbol} gestart")

        # Probeer eerst data te laden uit cache
        data_cache_dir = config.get("data_cache_dir", "data_cache")
        os.makedirs(data_cache_dir, exist_ok=True)

        cache_file = os.path.join(
            data_cache_dir,
            f"{symbol}_{args.timeframe}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pkl",
        )

        if os.path.exists(cache_file):
            # Laad data uit cache
            logger.info(f"Data voor {symbol} geladen uit cache: {cache_file}")
            data = pd.read_pickle(cache_file)
        else:
            # Laad data uit CSV historie bestand (in een echt systeem zou dit MT5 API gebruiken)
            # Dit is een eenvoudig voorbeeld; je moet dit aanpassen aan je datageneratie proces
            try:
                # In een echt systeem zou je hier MT5 API gebruiken of een ander dataprovider
                # Voor dit voorbeeld veronderstellen we CSV bestanden in een data_history map
                data_file = os.path.join(
                    "data_history", f"{symbol}_{args.timeframe}.csv"
                )

                if not os.path.exists(data_file):
                    logger.error(f"Historische data bestand niet gevonden: {data_file}")
                    continue

                # Laad data
                data = pd.read_csv(data_file)
                data["time"] = pd.to_datetime(data["time"])
                data.set_index("time", inplace=True)

                # Filter op datum
                data = data[(data.index >= start_date) & (data.index <= end_date)]

                # Controleer of we genoeg data hebben
                if len(data) < 100:  # Minimaal 100 bars
                    logger.warning(f"Onvoldoende data voor {symbol}")
                    continue

                # Sla op in cache
                data.to_pickle(cache_file)
                logger.info(f"Data voor {symbol} opgeslagen in cache: {cache_file}")

            except Exception as e:
                logger.error(
                    f"Fout bij laden van historische data voor {symbol}: {str(e)}"
                )
                continue

        # Run de backtest
        backtest_results = backtester.run_backtest(
            strategy_name=args.strategy,
            symbols=[symbol],
            start_date=args.start_date,
            end_date=args.end_date,
            timeframe=args.timeframe,
            plot_results=True,
        )

        # Log resultaten
        logger.info(f"Backtest resultaten voor {symbol}:")
        logger.info(f"  - Eindbalans: ${backtest_results.get('final_balance', 0):.2f}")
        logger.info(
            f"  - Winst/Verlies: ${backtest_results.get('profit_loss', 0):.2f} ({backtest_results.get('profit_percentage', 0):.2f}%)"
        )
        logger.info(f"  - Totaal trades: {backtest_results.get('total_trades', 0)}")

        win_rate = backtest_results.get("performance_stats", {}).get("win_rate", 0)
        if win_rate is not None:
            logger.info(f"  - Win rate: {win_rate * 100:.2f}%")

        max_drawdown = backtest_results.get("performance_stats", {}).get(
            "max_drawdown", 0
        )
        if max_drawdown is not None:
            logger.info(f"  - Max drawdown: {abs(max_drawdown):.2f}%")

        # Controlleer FTMO compliance
        ftmo_compliance = backtest_results.get(
            "ftmo_compliance", {"is_compliant": False}
        )
        logger.info(f"FTMO Compliance: {ftmo_compliance.get('is_compliant', False)}")

        if not ftmo_compliance.get("is_compliant", False) and ftmo_compliance.get(
            "reason"
        ):
            reasons = ftmo_compliance.get("reason", [])
            if isinstance(reasons, str):
                reasons = [reasons]
            for reason in reasons:
                logger.warning(f"  - {reason}")

        # Bewaar resultaten
        all_results[symbol] = backtest_results

    # Genereer samenvattingsrapport
    summary_file = os.path.join(results_dir, "backtest_summary.json")
    with open(summary_file, "w") as f:
        json.dump(all_results, f, indent=4, default=str)

    logger.info(f"Backtest samenvatting opgeslagen in {summary_file}")
    logger.info("Backtest voltooid")


def main():
    """Hoofdfunctie om het Sophy Trading Framework te starten."""
    # Parse command line argumenten
    args = parse_arguments()

    # Setup trading omgeving
    environment = setup_trading_environment(args)

    if not environment:
        print("Kan trading omgeving niet initialiseren. Programma wordt afgesloten.")
        return

    # Voer juiste modus uit
    if args.mode == "live":
        run_live_trading(args, environment)
    elif args.mode == "paper":
        # Paper trading is vergelijkbaar met live trading maar met een demo account
        run_live_trading(args, environment)
    elif args.mode == "backtest":
        run_backtest(args, environment)
    else:
        environment["logger"].error(f"Ongeldige modus: {args.mode}")


if __name__ == "__main__":
    main()
