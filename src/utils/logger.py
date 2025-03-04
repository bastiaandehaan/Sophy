import csv
import json
import os
from datetime import datetime


class Logger:
    """Verbeterde klasse voor logging van trades en botactiviteit"""

    def __init__(self, log_file_path):
        """
        Initialiseer de logger

        Parameters:
        -----------
        log_file_path : str
            Pad naar het logbestand
        """
        self.log_file = log_file_path
        self.setup_log_file()

        # Logging voor presentation statistieken
        log_dir = os.path.dirname(log_file_path)
        self.stats_file = os.path.join(log_dir, 'performance_stats.json')
        self.initialize_stats()

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Type', 'Symbol', 'Action',
                    'Price', 'Volume', 'StopLoss', 'TakeProfit',
                    'Comment', 'Leverage', 'TrendStrength', 'Balance'
                ])

    def initialize_stats(self):
        """Initialiseer presentation statistieken bestand als het nog niet bestaat"""
        if not os.path.exists(self.stats_file):
            default_stats = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'break_even_trades': 0,
                'win_rate': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'net_profit': 0,
                'trades_by_symbol': {},
                'daily_performance': {},
                'trade_history': []
            }
            with open(self.stats_file, 'w') as file:
                json.dump(default_stats, file, indent=4)

    def log_trade(self, symbol, action, price, volume, sl, tp, comment, leverage=None, trend_strength=None,
                  balance=None):
        """
        Log een trade naar CSV met uitgebreide informatie

        Parameters:
        -----------
        symbol : str
            Handelssymbool
        action : str
            Trade actie (BUY, SELL, etc.)
        price : float
            Uitvoeringsprijs
        volume : float
            Order volume
        sl : float
            Stop Loss prijs
        tp : float
            Take Profit prijs
        comment : str
            Commentaar bij de trade
        leverage : float, optional
            Gebruikte hefboom
        trend_strength : float, optional
            Sterkte van de trend op moment van trade
        balance : float, optional
            Account balans na trade
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'TRADE', symbol, action,
                price, volume, sl, tp, comment,
                leverage, trend_strength, balance
            ])

        # Log ook naar trade history voor performancetracking
        self.update_trade_stats(timestamp, symbol, action, price, volume, comment)

    def log_info(self, message, level="INFO"):
        """
        Log een informatiebericht

        Parameters:
        -----------
        message : str
            Het te loggen bericht
        level : str, optional
            Logniveau (INFO, WARNING, ERROR, DEBUG)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, level, '', '', '', '', '', '',
                message, '', '', ''
            ])

    def log_status(self, account_info, open_positions):
        """
        Log huidige account status

        Parameters:
        -----------
        account_info : dict
            Informatie over de account
        open_positions : dict
            Informatie over open posities
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        positions_count = 0
        if isinstance(open_positions, dict):
            for symbol in open_positions:
                if open_positions[symbol]:
                    positions_count += len(open_positions[symbol])

        # Verzamel open posities details
        positions_detail = ""
        if positions_count > 0:
            positions_list = []
            for symbol in open_positions:
                if open_positions[symbol]:
                    for pos in open_positions[symbol]:
                        profit_pct = (pos.profit / account_info.get('balance', 100000)) * 100
                        positions_list.append(f"{symbol}:{pos.volume}@{profit_pct:.2f}%")
            positions_detail = ", ".join(positions_list)

        # Bereken dagelijkse verandering
        equity = account_info.get('equity', 0)
        balance = account_info.get('balance', 0)
        margin = account_info.get('margin', 0)
        margin_level = (equity / margin * 100) if margin > 0 else 0

        # Bereken provisie / spreads (als equity - balans)
        floating_pnl = equity - balance

        # Maak het statusbericht
        status_message = (
                f"Balance: {balance}, " +
                f"Equity: {equity}, " +
                f"Floating P/L: {floating_pnl:.2f}, " +
                f"Margin Level: {margin_level:.2f}%, " +
                f"Open positions: {positions_count}"
        )

        if positions_detail:
            status_message += f" ({positions_detail})"

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'STATUS', '', '', '', '', '', '',
                status_message, '', '', balance
            ])

    def update_trade_stats(self, timestamp, symbol, action, price, volume, comment):
        """
        Update presentation statistieken na een trade

        Parameters:
        -----------
        timestamp : str
            Tijdstempel van de trade
        symbol : str
            Handelssymbool
        action : str
            Trade actie (BUY, SELL, etc.)
        price : float
            Uitvoeringsprijs
        volume : float
            Order volume
        comment : str
            Commentaar bij de trade
        """
        try:
            # Laad huidige statistieken
            if not os.path.exists(self.stats_file):
                self.initialize_stats()

            with open(self.stats_file, 'r') as file:
                stats = json.load(file)

            # Voeg trade toe aan geschiedenis
            trade_record = {
                'timestamp': timestamp,
                'symbol': symbol,
                'action': action,
                'price': price,
                'volume': volume,
                'comment': comment
            }

            stats['trade_history'].append(trade_record)

            # Bijhouden trades per symbool
            if symbol not in stats['trades_by_symbol']:
                stats['trades_by_symbol'][symbol] = {
                    'total': 0, 'buys': 0, 'sells': 0
                }

            stats['trades_by_symbol'][symbol]['total'] += 1
            if action == 'BUY':
                stats['trades_by_symbol'][symbol]['buys'] += 1
            elif action == 'SELL':
                stats['trades_by_symbol'][symbol]['sells'] += 1

            # Update algemene statistieken
            stats['total_trades'] += 1

            # Sla bijgewerkte statistieken op
            with open(self.stats_file, 'w') as file:
                json.dump(stats, file, indent=4)

        except Exception as e:
            self.log_info(f"Fout bij bijwerken statistieken: {e}", level="ERROR")

    def log_performance_metrics(self, metrics):
        """
        Log prestatiemetrieken

        Parameters:
        -----------
        metrics : dict
            Dictionary met prestatiemetrieken
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            metrics_str = ", ".join([f"{k}: {v}" for k, v in metrics.items() if k != 'trade_history'])

            with open(self.log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    timestamp, 'METRICS', '', '', '', '', '', '',
                    metrics_str, '', '', ''
                ])

            # Update ook het stats bestand
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as file:
                    stats = json.load(file)

                # Update metrics
                for k, v in metrics.items():
                    if k in stats and k != 'trade_history':
                        stats[k] = v

                with open(self.stats_file, 'w') as file:
                    json.dump(stats, file, indent=4)

        except Exception as e:
            self.log_info(f"Fout bij loggen van metrics: {e}", level="ERROR")