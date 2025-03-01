import csv
import os
from datetime import datetime


class Logger:
    """Klasse voor logging van trades en botactiviteit"""

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

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Type', 'Symbol', 'Action',
                    'Price', 'Volume', 'StopLoss', 'TakeProfit',
                    'Comment'
                ])

    def log_trade(self, symbol, action, price, volume, sl, tp, comment):
        """
        Log een trade naar CSV

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
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'TRADE', symbol, action,
                price, volume, sl, tp, comment
            ])

    def log_info(self, message):
        """
        Log een informatiebericht

        Parameters:
        -----------
        message : str
            Het te loggen bericht
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'INFO', '', '', '', '', '', '', message
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

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'STATUS', '', '', '', '', '', '',
                f"Balance: {account_info.get('balance', 'N/A')}, " +
                f"Equity: {account_info.get('equity', 'N/A')}, " +
                f"Open positions: {positions_count}"
            ])