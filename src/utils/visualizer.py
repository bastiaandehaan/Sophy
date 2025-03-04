import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import os
import json


class Visualizer:
    """Verbeterde klasse voor visualisatie van trading resultaten"""

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

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # Pad naar performance stats file
        log_dir = os.path.dirname(log_file)
        self.stats_file = os.path.join(log_dir, 'performance_stats.json')

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

    def load_performance_stats(self):
        """
        Laad performance statistieken uit JSON bestand

        Returns:
        --------
        dict
            Dictionary met performancestatistieken
        """
        if not os.path.exists(self.stats_file):
            print(f"Performance stats bestand niet gevonden: {self.stats_file}")
            return {}

        try:
            with open(self.stats_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Fout bij laden van performance stats: {e}")
            return {}

    def plot_equity_curve(self, include_drawdown=True):
        """
        Plot de equity curve met uitgebreide metrics

        Parameters:
        -----------
        include_drawdown : bool, optional
            Of drawdown analyse moet worden toegevoegd

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
        status_df = df[df['Type'] == 'STATUS'].copy()
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
            balance = row.get('Balance', None)

            # Probeer eerst uit de Balance kolom te halen
            if pd.notna(balance) and balance != '':
                balances.append(float(balance))
                timestamps.append(timestamp)
            else:
                # Als dat niet lukt, probeer uit de Comment te extraheren
                balance_str = comment.split('Balance: ')[1].split(',')[0] if 'Balance: ' in comment else None
                if balance_str and balance_str != 'N/A':
                    balances.append(float(balance_str))
                    timestamps.append(timestamp)

            # Extraheer equity uit comment
            equity_str = comment.split('Equity: ')[1].split(',')[0] if 'Equity: ' in comment else None
            if equity_str and equity_str != 'N/A':
                equities.append(float(equity_str))

        if not balances:
            print("Geen balance data gevonden voor equity curve")
            return None

        # Maak dataframe voor analyse
        equity_df = pd.DataFrame({
            'timestamp': timestamps,
            'balance': balances
        })

        if len(equities) == len(balances):
            equity_df['equity'] = equities

        # Bereken drawdown als die er is
        if 'equity' in equity_df.columns:
            equity_df['peak'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        else:
            equity_df['peak'] = equity_df['balance'].cummax()
            equity_df['drawdown'] = (equity_df['balance'] - equity_df['peak']) / equity_df['peak'] * 100

        # Bereken prestatie-metrieken
        initial_balance = equity_df['balance'].iloc[0] if not equity_df.empty else 100000
        final_balance = equity_df['balance'].iloc[-1] if not equity_df.empty else initial_balance
        total_return = ((final_balance / initial_balance) - 1) * 100
        max_drawdown = equity_df['drawdown'].min() if 'drawdown' in equity_df.columns else 0

        # Maak equity curve plot
        fig, axes = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})

        # Bovenste plot: Equity curve
        if 'equity' in equity_df.columns:
            axes[0].plot(equity_df['timestamp'], equity_df['equity'], label='Equity', color='blue', linewidth=2)

        axes[0].plot(equity_df['timestamp'], equity_df['balance'], label='Balance', color='green', linewidth=2)
        axes[0].plot(equity_df['timestamp'], equity_df['peak'], label='Peak Balance', color='darkgreen', linestyle='--',
                     alpha=0.6)

        # Voeg horizontale lijn toe voor beginbalans
        axes[0].axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')

        # Voeg horizontale lijnen toe voor 5% en 10% winst
        axes[0].axhline(y=initial_balance * 1.05, color='orange', linestyle=':', alpha=0.8, label='5% Profit')
        axes[0].axhline(y=initial_balance * 1.10, color='darkgreen', linestyle=':', alpha=0.8,
                        label='10% Profit (Target)')

        # Voeg horizontale lijnen toe voor FTMO limieten
        axes[0].axhline(y=initial_balance * 0.95, color='yellow', linestyle=':', alpha=0.8,
                        label='5% Loss (Daily Limit)')
        axes[0].axhline(y=initial_balance * 0.90, color='red', linestyle=':', alpha=0.8,
                        label='10% Loss (Max Drawdown)')

        # Voeg trade markers toe (optioneel)
        trade_df = df[df['Type'] == 'TRADE']
        if not trade_df.empty:
            buy_df = trade_df[trade_df['Action'] == 'BUY']
            sell_df = trade_df[trade_df['Action'] == 'SELL']

            if not buy_df.empty:
                axes[0].scatter(buy_df['Timestamp'], [initial_balance] * len(buy_df), marker='^', color='green',
                                s=80, label='Buy', alpha=0.7)
            if not sell_df.empty:
                axes[0].scatter(sell_df['Timestamp'], [initial_balance] * len(sell_df), marker='v', color='red',
                                s=80, label='Sell', alpha=0.7)

        # Formateer bovenste plot
        axes[0].set_title('Equity Curve & Balance History', fontsize=16)
        axes[0].set_ylabel('Account Value ($)', fontsize=14)
        axes[0].legend(loc='upper left', fontsize=12)
        axes[0].grid(True)

        # Voeg metrics toe aan de plot
        info_text = (
            f"Initial Balance: ${initial_balance:,.2f}\n"
            f"Final Balance: ${final_balance:,.2f}\n"
            f"Total Return: {total_return:.2f}%\n"
            f"Max Drawdown: {max_drawdown:.2f}%"
        )

        # Plaats info tekst in de rechterbovenhoek
        axes[0].text(0.02, 0.02, info_text, transform=axes[0].transAxes, fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        # Onderste plot: Drawdown
        axes[1].fill_between(equity_df['timestamp'], equity_df['drawdown'], 0,
                             color='red', alpha=0.3, label='Drawdown')
        axes[1].plot(equity_df['timestamp'], equity_df['drawdown'], color='red', linewidth=1)

        # Voeg horizontale lijnen toe voor drawdown limieten
        axes[1].axhline(y=-5, color='yellow', linestyle=':', alpha=0.8, label='5% Drawdown (Daily Limit)')
        axes[1].axhline(y=-10, color='red', linestyle=':', alpha=0.8, label='10% Drawdown (Max Limit)')

        # Formateer onderste plot
        axes[1].set_title('Drawdown (%)', fontsize=14)
        axes[1].set_xlabel('Datum', fontsize=14)
        axes[1].set_ylabel('Drawdown (%)', fontsize=14)
        axes[1].legend(loc='lower left', fontsize=12)
        axes[1].set_ylim(min(equity_df['drawdown'].min() * 1.2, -12), 1)  # Zorg voor goede y-as limieten
        axes[1].grid(True)

        # Formateer x-as voor beide plots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
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

        # Bereken aantal figuren nodig (1 rij per symbool)
        num_symbols = len(symbols)

        # Maak plot voor elk symbool
        fig, axes = plt.subplots(num_symbols, 1, figsize=(16, 6 * num_symbols), squeeze=False)

        for i, symbol in enumerate(symbols):
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Converteer kolommen naar numeriek waar nodig
            for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit', 'Leverage', 'TrendStrength']:
                if col in symbol_df.columns:
                    symbol_df[col] = pd.to_numeric(symbol_df[col], errors='coerce')

            # Filter buys en sells
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            ax = axes[i, 0]

            # Plot trades
            if not buys.empty:
                ax.scatter(buys['Timestamp'], buys['Price'], color='green', marker='^', s=100, label='Buy')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in buys.columns:
                    sizes = buys['Volume'] * 50 + 50  # Schaal volume voor marker grootte
                    ax.scatter(buys['Timestamp'], buys['Price'], s=sizes, color='green', marker='^', alpha=0.5)

                # Plot stop losses voor buy orders
                for _, row in buys.iterrows():
                    if pd.notna(row.get('StopLoss', None)) and row['StopLoss'] > 0:
                        ax.plot([row['Timestamp'], row['Timestamp']],
                                [row['Price'], row['StopLoss']],
                                'r--', alpha=0.5)

            if not sells.empty:
                ax.scatter(sells['Timestamp'], sells['Price'], color='red', marker='v', s=100, label='Sell')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in sells.columns:
                    sizes = sells['Volume'] * 50 + 50
                    ax.scatter(sells['Timestamp'], sells['Price'], s=sizes, color='red', marker='v', alpha=0.5)

            # Bereken en toon winst/verlies per trade als mogelijk
            paired_trades = self._pair_trades(symbol_df)
            for pair in paired_trades:
                if len(pair) == 2:  # Alleen complete trade paren
                    buy = pair[0]
                    sell = pair[1]
                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    # Toon label voor het resultaat
                    mid_time = buy['Timestamp'] + (sell['Timestamp'] - buy['Timestamp']) / 2
                    mid_price = (buy['Price'] + sell['Price']) / 2

                    color = 'green' if profit_pct > 0 else 'red'
                    ax.text(mid_time, mid_price, f"{profit_pct:.1f}%",
                            color=color, fontweight='bold', ha='center')

                    # Verbind buy en sell punt met lijn
                    ax.plot([buy['Timestamp'], sell['Timestamp']],
                            [buy['Price'], sell['Price']],
                            color=color, linestyle='-', alpha=0.5)

            # Formateer plot
            ax.set_title(f'Trades voor {symbol}', fontsize=16)
            ax.set_ylabel('Prijs', fontsize=14)

            # Voeg gridlines toe
            ax.grid(True)
            ax.legend(loc='upper left', fontsize=12)

            # Voeg labels toe voor buy/sell punten
            for idx, row in buys.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, 5), textcoords='offset points',
                            fontsize=9, color='darkgreen')

            for idx, row in sells.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, -15), textcoords='offset points',
                            fontsize=9, color='darkred')

            # Formateer x-as
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.xlabel('Tijd', fontsize=14)
        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Trade resultaten opgeslagen als {output_path}")
        return output_path

    def _pair_trades(self, trade_df):
        """
        Groepeer trades in buy/sell paren

        Parameters:
        -----------
        trade_df : pandas.DataFrame
            DataFrame met trades voor één symbool

        Returns:
        --------
        list
            Lijst met paren van trades (buy/sell)
        """
        # Sorteer trades op tijdstempel
        sorted_trades = trade_df.sort_values('Timestamp').to_dict('records')

        # Verzamel paren
        pairs = []
        current_pair = []

        for trade in sorted_trades:
            if trade['Action'] == 'BUY':
                # Als we al een open pair hebben, sluit deze eerst af
                if current_pair:
                    pairs.append(current_pair)
                    current_pair = [trade]
                else:
                    current_pair = [trade]
            elif trade['Action'] == 'SELL' and current_pair:
                current_pair.append(trade)
                pairs.append(current_pair)
                current_pair = []

        # Voeg laatste onvolledige paar toe indien aanwezig
        if current_pair:
            pairs.append(current_pair)

        return pairs

    def plot_performance_summary(self):
        """
        Plot een samenvatting van de handelsperformance

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        # Laad trade data
        df = self.load_trade_data()
        stats = self.load_performance_stats()

        if df.empty:
            print("Geen data beschikbaar voor performance summary")
            return None

        # Filter trades
        trade_df = df[df['Type'] == 'TRADE'].copy()

        if trade_df.empty:
            print("Geen trade data beschikbaar voor analyse")
            return None

        # Converteer numerieke kolommen
        for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit']:
            if col in trade_df.columns:
                trade_df[col] = pd.to_numeric(trade_df[col], errors='coerce')

        # Bereken metrics
        trades_by_symbol = {}
        symbol_performance = {}

        for symbol in trade_df['Symbol'].unique():
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Basic count metrics
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            trades_by_symbol[symbol] = {
                'buys': len(buys),
                'sells': len(sells),
                'total': len(symbol_df)
            }

            # Bereken performance als mogelijk
            pairs = self._pair_trades(symbol_df)
            wins = 0
            losses = 0
            total_profit_pct = 0
            total_loss_pct = 0

            for pair in pairs:
                if len(pair) == 2:  # Alleen complete trades
                    buy = pair[0]
                    sell = pair[1]

                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    if profit_pct > 0:
                        wins += 1
                        total_profit_pct += profit_pct
                    else:
                        losses += 1
                        total_loss_pct += profit_pct

            total_complete_trades = wins + losses
            win_rate = wins / total_complete_trades if total_complete_trades > 0 else 0
            avg_win = total_profit_pct / wins if wins > 0 else 0
            avg_loss = total_loss_pct / losses if losses > 0 else 0
            profit_factor = abs(total_profit_pct / total_loss_pct) if total_loss_pct < 0 else float('inf')

            symbol_performance[symbol] = {
                'win_rate': win_rate,
                'wins': wins,
                'losses': losses,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'net_profit_pct': total_profit_pct + total_loss_pct
            }

        # Maak plot
        fig = plt.figure(figsize=(20, 16))

        # Definieer grid layout
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

        # 1. Win/Loss Ratio per Symbol (Pie chart)
        ax1 = fig.add_subplot(gs[0, 0])

        symbols = list(symbol_performance.keys())
        win_rates = [symbol_performance[s]['win_rate'] * 100 for s in symbols]

        # Kleuren gebaseerd op win rate (rood naar groen)
        colors = [(1 - wr / 100, wr / 100, 0) for wr in win_rates]

        ax1.bar(symbols, win_rates, color=colors)
        ax1.set_title('Win Rate per Symbol (%)', fontsize=14)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y')

        # Voeg datawaarden toe aan bars
        for i, v in enumerate(win_rates):
            ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

        # 2. Average Win vs Loss per Symbol
        ax2 = fig.add_subplot(gs[0, 1])

        # Verzamel data
        symbols = list(symbol_performance.keys())
        avg_wins = [symbol_performance[s]['avg_win'] for s in symbols]
        avg_losses = [abs(symbol_performance[s]['avg_loss']) for s in symbols]

        x = np.arange(len(symbols))
        width = 0.35

        ax2.bar(x - width / 2, avg_wins, width, label='Avg Win %', color='green', alpha=0.7)
        ax2.bar(x + width / 2, avg_losses, width, label='Avg Loss %', color='red', alpha=0.7)

        ax2.set_title('Average Win vs Loss (%)', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(symbols)
        ax2.legend()
        ax2.grid(axis='y')

        # 3. Net Profit per Symbol
        ax3 = fig.add_subplot(gs[1, 0])

        net_profits = [symbol_performance[s]['net_profit_pct'] for s in symbols]
        colors = ['green' if p > 0 else 'red' for p in net_profits]

        ax3.bar(symbols, net_profits, color=colors, alpha=0.7)
        ax3.set_title('Net Profit per Symbol (%)', fontsize=14)
        ax3.grid(axis='y')

        # Voeg datawaarden toe
        for i, v in enumerate(net_profits):
            ax3.text(i, v + (0.1 if v >= 0 else -2), f"{v:.1f}%", ha='center', fontsize=12)

        # 4. Trades per Symbol
        ax4 = fig.add_subplot(gs[1, 1])

        # Verzamel data
        buys_per_symbol = [trades_by_symbol[s]['buys'] for s in symbols]
        sells_per_symbol = [trades_by_symbol[s]['sells'] for s in symbols]

        ax4.bar(x - width / 2, buys_per_symbol, width, label='Buy Orders', color='green', alpha=0.7)
        ax4.bar(x + width / 2, sells_per_symbol, width, label='Sell Orders', color='red', alpha=0.7)

        ax4.set_title('Number of Trades per Symbol', fontsize=14)
        ax4.set_xticks(x)
        ax4.set_xticklabels(symbols)
        ax4.legend()
        ax4.grid(axis='y')

        # 5. Overall Performance Metrics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')

        # Bereken totalen over alle symbolen
        total_trades = sum(trades_by_symbol[s]['total'] for s in symbols)
        total_wins = sum(symbol_performance[s]['wins'] for s in symbols)
        total_losses = sum(symbol_performance[s]['losses'] for s in symbols)

        total_win_rate = total_wins / (total_wins + total_losses) * 100 if (total_wins + total_losses) > 0 else 0
        total_profit = sum(symbol_performance[s]['net_profit_pct'] for s in symbols)

        # Custom tabel
        overall_metrics = [
            ('Total Trades', f"{total_trades}"),
            ('Win Rate', f"{total_win_rate:.1f}%"),
            ('Winning Trades', f"{total_wins}"),
            ('Losing Trades', f"{total_losses}"),
            ('Net Profit %', f"{total_profit:.2f}%"),
        ]

        table_data = []
        for metric, value in overall_metrics:
            table_data.append([metric, value])

        tbl = ax5.table(
            cellText=table_data,
            colLabels=['Metric', 'Value'],
            loc='center',
            cellLoc='center',
            colWidths=[0.3, 0.3]
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        # Stel kleuren in
        header_color = '#40466e'
        cell_color = '#f1f1f2'

        for i, key in enumerate(tbl.get_celld().keys()):
            cell = tbl.get_celld()[key]
            if i == 0:  # Header row
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            else:
                cell.set_facecolor(cell_color)

        ax5.set_title('Overall Performance Metrics', fontsize=16, pad=20)

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"performance_summary_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Performance samenvatting opgeslagen als {output_path}")
        return output_path