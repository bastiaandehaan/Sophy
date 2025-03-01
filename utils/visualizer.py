import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


class Visualizer:
    """Klasse voor visualisatie van trading resultaten"""

    def __init__(self, log_file, output_dir='data'):
        """
        Initialiseer de visualizer

        Parameters:
        -----------
        log_file : str
            Pad naar het logbestand
        output_dir : str, optional
            Map voor het opslaan van grafieken
        """
        self.log_file = log_file
        self.output_dir = output_dir

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

    def load_trade_data(self):
        """
        Laad trade data uit het logbestand

        Returns:
        --------
        pandas.DataFrame
            DataFrame met trade data
        """
        try:
            df = pd.read_csv(self.log_file)
            # Converteer timestamp naar datetime
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except Exception as e:
            print(f"Fout bij laden van trade data: {e}")
            return pd.DataFrame()

    def plot_equity_curve(self):
        """
        Plot de equity curve

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor equity curve")
            return None

        # Filter alleen op STATUS rijen
        status_df = df[df['Type'] == 'STATUS']
        if status_df.empty:
            print("Geen status data beschikbaar voor equity curve")
            return None

        # Extraheer balance en equity uit Comment kolom
        balances = []
        equities = []
        timestamps = []

        for _, row in status_df.iterrows():
            comment = row['Comment']
            timestamp = row['Timestamp']

            balance_str = comment.split('Balance: ')[1].split(',')[0] if 'Balance: ' in comment else None
            equity_str = comment.split('Equity: ')[1].split(',')[0] if 'Equity: ' in comment else None

            if balance_str and balance_str != 'N/A':
                balance = float(balance_str)
                balances.append(balance)
                timestamps.append(timestamp)

            if equity_str and equity_str != 'N/A':
                equity = float(equity_str)
                equities.append(equity)

        if not balances or not equities or len(balances) != len(equities):
            print("Onvolledige data voor equity curve")
            return None

        # Maak equity curve
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, balances, label='Balance')
        plt.plot(timestamps, equities, label='Equity')
        plt.title('Equity Curve')
        plt.xlabel('Tijd')
        plt.ylabel('Waarde ($)')
        plt.legend()
        plt.grid(True)

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path)
        plt.close()

        print(f"Equity curve opgeslagen als {output_path}")
        return output_path

    def plot_trade_results(self):
        """
        Plot de resultaten van trades

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor trade resultaten")
            return None

        # Filter alleen op TRADE rijen
        trade_df = df[df['Type'] == 'TRADE']
        if trade_df.empty:
            print("Geen trade data beschikbaar")
            return None

        # Groepeer trades per symbool
        symbols = trade_df['Symbol'].unique()

        # Maak plot voor elk symbool
        plt.figure(figsize=(15, 10))

        for i, symbol in enumerate(symbols, 1):
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Maak subplot voor dit symbool
            plt.subplot(len(symbols), 1, i)

            # Plot trades
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            if not buys.empty and not sells.empty:
                plt.scatter(buys['Timestamp'], buys['Price'], color='green', marker='^', label='Buy')
                plt.scatter(sells['Timestamp'], sells['Price'], color='red', marker='v', label='Sell')

                # Plot stop losses voor buy orders
                for _, row in buys.iterrows():
                    if row['StopLoss'] > 0:
                        plt.plot([row['Timestamp'], row['Timestamp']],
                                 [row['Price'], row['StopLoss']],
                                 'r--', alpha=0.5)

            plt.title(f'Trades voor {symbol}')
            plt.ylabel('Prijs')
            plt.grid(True)
            plt.legend()

        plt.xlabel('Tijd')
        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_results_{timestamp}.png")
        plt.savefig(output_path)
        plt.close()

        print(f"Trade resultaten opgeslagen als {output_path}")
        return output_path