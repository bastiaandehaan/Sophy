# src/utils/logger.py
import csv
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class Logger:
    """Verbeterde klasse voor logging van trades en botactiviteit"""

    def __init__(self, log_file_path: str):
        """
        Initialiseer de logger.

        Parameters:
        -----------
        log_file_path : str
            Pad naar het logbestand.
        """
        self.log_file = log_file_path

        # Maak log directory indien nodig
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        self.setup_log_file()

        # Logging voor performance statistieken
        self.stats_file = os.path.join(
            os.path.dirname(log_file_path), "performance_stats.json"
        )
        self.initialize_stats()

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Timestamp",
                        "Type",
                        "Symbol",
                        "Action",
                        "Price",
                        "Volume",
                        "StopLoss",
                        "TakeProfit",
                        "Comment",
                        "Leverage",
                        "TrendStrength",
                        "Balance",
                    ]
                )
                # Voeg initiële INFO regel toe
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow(
                    [
                        timestamp,
                        "INFO",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "Log gestart",
                        "",
                        "",
                        "",
                    ]
                )

    def initialize_stats(self):
        """Initialiseer performance statistieken bestand als het nog niet bestaat."""
        if not os.path.exists(self.stats_file):
            default_stats = {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "break_even_trades": 0,
                "win_rate": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "profit_factor": 0.0,
                "max_drawdown": 0.0,
                "net_profit": 0.0,
                "trades_by_symbol": {},
                "daily_performance": {},
                "trade_history": [],
            }
            with open(self.stats_file, "w") as file:
                json.dump(default_stats, file, indent=4)

    def log_trade(
        self,
        symbol: str,
        action: str,
        price: float,
        volume: float,
        sl: float,
        tp: float,
        comment: str,
        leverage: Optional[float] = None,
        trend_strength: Optional[float] = None,
        balance: Optional[float] = None,
    ):
        """
        Log een trade naar CSV met uitgebreide informatie.

        Parameters:
        -----------
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        sl : float
            Stop Loss prijs.
        tp : float
            Take Profit prijs.
        comment : str
            Commentaar bij de trade.
        leverage : float, optional
            Gebruikte hefboom.
        trend_strength : float, optional
            Sterkte van de trend op moment van trade.
        balance : float, optional
            Account balans na trade.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    timestamp,
                    "TRADE",
                    symbol,
                    action,
                    price,
                    volume,
                    sl,
                    tp,
                    comment,
                    leverage if leverage is not None else "",
                    trend_strength if trend_strength is not None else "",
                    balance if balance is not None else "",
                ]
            )

        # Log ook naar trade history voor performancetracking
        self.update_trade_stats(timestamp, symbol, action, price, volume, comment)

    def log_info(self, message: str, level: str = "INFO"):
        """
        Log een informatiebericht.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        level : str, optional
            Logniveau (INFO, WARNING, ERROR, DEBUG).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [timestamp, level, "", "", "", "", "", "", message, "", "", ""]
            )
        print(f"[{timestamp}] {level}: {message}")

    # Standaard logger interface methoden voor compatibiliteit
    def info(self, message: str):
        """
        Standaard interface voor info logging.
        Delegeert naar log_info methode.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        """
        return self.log_info(message, level="INFO")

    def warning(self, message: str):
        """
        Standaard interface voor warning logging.
        Delegeert naar log_info methode.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        """
        return self.log_info(message, level="WARNING")

    def error(self, message: str):
        """
        Standaard interface voor error logging.
        Delegeert naar log_info methode.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        """
        return self.log_info(message, level="ERROR")

    def log_status(self, account_info: Dict[str, Any], open_positions: Dict[str, Any]):
        """
        Log huidige account status met verbeterde positieverwerking.

        Parameters:
        -----------
        account_info : Dict[str, Any]
            Informatie over de account.
        open_positions : Dict[str, Any]
            Informatie over open posities.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        positions_count = (
            sum(len(pos_list) for pos_list in open_positions.values())
            if open_positions
            else 0
        )
        positions_detail = ""

        if positions_count > 0:
            position_parts = []
            for symbol, pos_list in open_positions.items():
                for pos in pos_list:
                    # Controleer of we met een dict of een object werken
                    if isinstance(pos, dict):
                        vol = pos.get("volume", 0)
                        profit_pct = (
                            pos.get("profit", 0) / account_info.get("balance", 100000)
                        ) * 100
                    else:
                        # Object met attributen (zoals MT5 positie object)
                        vol = getattr(pos, "volume", 0)
                        profit_pct = (
                            getattr(pos, "profit", 0)
                            / account_info.get("balance", 100000)
                        ) * 100

                    position_parts.append(f"{symbol}:{vol}@{profit_pct:.2f}%")

            positions_detail = ", ".join(position_parts)

        equity = account_info.get("equity", 0)
        balance = account_info.get("balance", 0)
        margin = account_info.get("margin", 0)
        margin_level = (equity / margin * 100) if margin > 0 else 0
        floating_pnl = equity - balance

        status_message = (
            f"Balance: {balance}, Equity: {equity}, Floating P/L: {floating_pnl:.2f}, "
            f"Margin Level: {margin_level:.2f}%, Open positions: {positions_count}"
        )
        if positions_detail:
            status_message += f" ({positions_detail})"

        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    timestamp,
                    "STATUS",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    status_message,
                    "",
                    "",
                    balance,
                ]
            )

    def update_trade_stats(
        self,
        timestamp: str,
        symbol: str,
        action: str,
        price: float,
        volume: float,
        comment: str,
    ):
        """
        Update performance statistieken na een trade.

        Parameters:
        -----------
        timestamp : str
            Tijdstempel van de trade.
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        comment : str
            Commentaar bij de trade.
        """
        try:
            if not os.path.exists(self.stats_file):
                self.initialize_stats()

            with open(self.stats_file, "r") as file:
                stats = json.load(file)

            # Voeg trade toe aan geschiedenis
            trade_record = {
                "timestamp": timestamp,
                "symbol": symbol,
                "action": action,
                "price": price,
                "volume": volume,
                "comment": comment,
            }
            stats["trade_history"].append(trade_record)

            # Bijhouden trades per symbool
            if symbol not in stats["trades_by_symbol"]:
                stats["trades_by_symbol"][symbol] = {"total": 0, "buys": 0, "sells": 0}
            stats["trades_by_symbol"][symbol]["total"] += 1
            if action == "BUY":
                stats["trades_by_symbol"][symbol]["buys"] += 1
            elif action == "SELL":
                stats["trades_by_symbol"][symbol]["sells"] += 1

            # Update algemene statistieken
            stats["total_trades"] += 1

            # Sla bijgewerkte statistieken op
            with open(self.stats_file, "w") as file:
                json.dump(stats, file, indent=4)
        except json.JSONDecodeError:
            self.initialize_stats()  # Herinitialiseer bij corrupte JSON
            self.log_info(
                "Stats bestand herinitialiseerd vanwege corrupte data", level="WARNING"
            )
        except Exception as e:
            self.log_info(f"Fout bij bijwerken statistieken: {e}", level="ERROR")

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log prestatiemetrieken.

        Parameters:
        -----------
        metrics : dict
            Dictionary met prestatiemetrieken.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics_str = ", ".join(
            f"{k}: {v}" for k, v in metrics.items() if k != "trade_history"
        )

        try:
            with open(self.log_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        timestamp,
                        "METRICS",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        metrics_str,
                        "",
                        "",
                        "",
                    ]
                )

            if os.path.exists(self.stats_file):
                with open(self.stats_file, "r") as file:
                    stats = json.load(file)
                for k, v in metrics.items():
                    if k in stats and k != "trade_history":
                        stats[k] = v
                with open(self.stats_file, "w") as file:
                    json.dump(stats, file, indent=4)
        except Exception as e:
            self.log_info(f"Fout bij loggen van metrics: {e}", level="ERROR")
