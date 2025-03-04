import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta


class FTMOHelper:
    """Helper class voor FTMO-specifieke functionaliteit en regelverificatie"""

    def __init__(self, log_file, output_dir='data/ftmo_analysis'):
        """
        Initialiseer de FTMO helper

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

        # FTMO regels
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% winstdoel
            'max_daily_loss': 0.05,  # 5% maximale dagelijkse drawdown
            'max_total_loss': 0.10,  # 10% maximale totale drawdown
            'min_trading_days': 4,  # Minimaal 4 handelsdagen vereist
            'challenge_duration': 30,  # Challenge duurt 30 dagen
            'verification_duration': 60  # Verificatie duurt 60 dagen
        }

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

            # Extraheer datum component
            df['Date'] = df['Timestamp'].dt.date

            return df
        except Exception as e:
            print(f"Fout bij laden van trade data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance=100000):
        """
        Controleer of de trading prestaties voldoen aan de FTMO regels

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans

        Returns:
        --------
        dict
            Compliance resultaten met uitleg
        """
        df = self.load_trade_data()
        if df.empty:
            return {
                'compliant': False,
                'reason': 'Geen trading data beschikbaar',
                'details': {}
            }

        # 1. Bereken dagelijkse P&L en drawdown
        status_df = df[df['Type'] == 'STATUS'].copy()

        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            # Probeer balance te extraheren uit Comment kolom
            def extract_balance(comment):
                if not isinstance(comment, str):
                    return None
                try:
                    if 'Balance: ' in comment:
                        balance_str = comment.split('Balance: ')[1].split(',')[0]
                        return float(balance_str) if balance_str != 'N/A' else None
                except:
                    return None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        # Als nog steeds geen balansgegevens, kunnen we niet doorgaan
        if status_df['Balance'].isna().all():
            return {
                'compliant': False,
                'reason': 'Geen balansgegevens beschikbaar',
                'details': {}
            }

        # Converteer naar numeriek
        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')

        # Groepeer per dag voor dagelijkse min/max/close
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last'),
            count=('Balance', 'count')
        ).reset_index()

        # Bereken dagelijkse P&L en drawdown
        daily_status['prev_close'] = daily_status['close_balance'].shift(1)
        daily_status.loc[0, 'prev_close'] = initial_balance  # Eerste dag

        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = daily_status['daily_pnl'] / daily_status['prev_close'] * 100
        daily_status['daily_drawdown'] = (daily_status['min_balance'] - daily_status['prev_close']) / daily_status[
            'prev_close'] * 100

        # 2. Bereken totale P&L en maximale drawdown
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Berekenen van de maximale drawdown vanaf het hoogste punt
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = (daily_status['close_balance'] - daily_status['peak']) / daily_status[
            'peak'] * 100
        max_drawdown = daily_status['drawdown_from_peak'].min()

        # 3. Controleer handelsactiviteit
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # 4. Resultaten verzamelen
        worst_day_idx = daily_status['daily_drawdown'].idxmin()
        worst_day = daily_status.iloc[worst_day_idx]
        worst_day_date = worst_day['Date']
        worst_day_drawdown = worst_day['daily_drawdown']

        # Controleer alle regels
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() > -self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']

        # Compliance evaluatie
        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Reden voor non-compliance
        reason = ''
        if not compliant:
            reasons = []
            if not profit_target_met:
                reasons.append(
                    f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (target: {self.ftmo_rules['profit_target'] * 100}%)")
            if not daily_loss_compliant:
                reasons.append(
                    f"Dagelijkse verliesgrens overschreden: {worst_day_drawdown:.2f}% op {worst_day_date} (limiet: -{self.ftmo_rules['max_daily_loss'] * 100}%)")
            if not total_loss_compliant:
                reasons.append(
                    f"Totale verliesgrens overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")
            if not trading_days_compliant:
                reasons.append(
                    f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")
            reason = "; ".join(reasons)

        # Gedetailleerde resultaten
        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'worst_day_date': worst_day_date,
            'worst_day_drawdown': worst_day_drawdown,
            'trading_days': unique_trading_days,
            'profit_target_met': profit_target_met,
            'daily_loss_compliant': daily_loss_compliant,
            'total_loss_compliant': total_loss_compliant,
            'trading_days_compliant': trading_days_compliant,
            'daily_stats': daily_status
        }

        return {
            'compliant': compliant,
            'reason': reason if not compliant else "Voldoet aan alle FTMO regels",
            'details': details
        }

    def plot_ftmo_compliance(self, initial_balance=100000):
        """
        Maak een visualisatie van FTMO-compliance

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        # Compliance resultaten ophalen
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance['details']:
            print("Onvoldoende data voor FTMO compliance analyse")
            return None

        details = compliance['details']
        daily_stats = details['daily_stats']

        # Maak plot
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(4, 2, height_ratios=[2, 1, 1, 1])

        # 1. Balance curve
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(daily_stats['Date'], daily_stats['close_balance'], 'b-', label='Account Balance')

        # Voeg horizontale lijnen toe
        ax1.axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')
        ax1.axhline(y=initial_balance * 1.10, color='green', linestyle='--', alpha=0.8,
                    label=f"+10% Target (${initial_balance * 1.10:,.2f})")
        ax1.axhline(y=initial_balance * 0.95, color='orange', linestyle='--', alpha=0.8,
                    label=f"-5% Daily Limit (${initial_balance * 0.95:,.2f})")
        ax1.axhline(y=initial_balance * 0.90, color='red', linestyle='--', alpha=0.8,
                    label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")

        # Formatteren
        ax1.set_title('FTMO Account Balance Progression', fontsize=16)
        ax1.set_ylabel('Balance ($)', fontsize=14)
        ax1.legend(loc='best', fontsize=12)
        ax1.grid(True)

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['green' if x >= 0 else 'red' for x in daily_stats['daily_pnl']]
        ax2.bar(daily_stats['Date'], daily_stats['daily_pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)

        # Formatteren
        ax2.set_title('Daily P&L ($)', fontsize=14)
        ax2.set_ylabel('P&L ($)', fontsize=12)
        ax2.grid(True, axis='y')

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(daily_stats['Date'], daily_stats['daily_drawdown'], 0,
                         where=(daily_stats['daily_drawdown'] < 0),
                         color='red', alpha=0.3)
        ax3.plot(daily_stats['Date'], daily_stats['daily_drawdown'], 'r-', alpha=0.7)
        ax3.axhline(y=-5, color='orange', linestyle='--', alpha=0.8, label='-5% Daily Limit')

        # Formatteren
        ax3.set_title('Daily Drawdown (%)', fontsize=14)
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_ylim(min(-10, daily_stats['daily_drawdown'].min() * 1.2), 1)
        ax3.legend(loc='lower right', fontsize=10)
        ax3.grid(True)

        # 4. Cumulative Drawdown van peak
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(daily_stats['Date'], daily_stats['drawdown_from_peak'], 0,
                         color='purple', alpha=0.3)
        ax4.plot(daily_stats['Date'], daily_stats['drawdown_from_peak'], 'purple', alpha=0.7)
        ax4.axhline(y=-10, color='red', linestyle='--', alpha=0.8, label='-10% Max Drawdown Limit')

        # Formatteren
        ax4.set_title('Maximum Drawdown from Peak (%)', fontsize=14)
        ax4.set_ylabel('Drawdown (%)', fontsize=12)
        ax4.set_ylim(min(-12, daily_stats['drawdown_from_peak'].min() * 1.2), 1)
        ax4.legend(loc='lower right', fontsize=10)
        ax4.grid(True)

        # 5. Compliance samenvatting tabel
        ax5 = fig.add_subplot(gs[3, :])
        ax5.axis('off')

        compliance_data = [
            ['Metric', 'Value', 'Requirement', 'Status'],
            ['Total P&L', f"{details['total_pnl_pct']:.2f}%", f"≥ {self.ftmo_rules['profit_target'] * 100}%",
             '✅' if details['profit_target_met'] else '❌'],
            ['Max Daily Drawdown', f"{details['worst_day_drawdown']:.2f}%",
             f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
             '✅' if details['daily_loss_compliant'] else '❌'],
            ['Max Total Drawdown', f"{details['max_drawdown']:.2f}%", f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
             '✅' if details['total_loss_compliant'] else '❌'],
            ['Trading Days', f"{details['trading_days']}", f"≥ {self.ftmo_rules['min_trading_days']}",
             '✅' if details['trading_days_compliant'] else '❌']
        ]

        tbl = ax5.table(
            cellText=[row for row in compliance_data],
            loc='center',
            cellLoc='center',
            colWidths=[0.25, 0.25, 0.25, 0.15]
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        # Opmaak van tabel
        header_color = '#40466e'
        pass_color = '#d8f3dc'
        fail_color = '#ffcccb'

        for (i, j), cell in tbl.get_celld().items():
            if i == 0:  # Header row
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            elif j == 3:  # Status column
                if compliance_data[i][3] == '✅':
                    cell.set_facecolor(pass_color)
                else:
                    cell.set_facecolor(fail_color)

        # Titel en compliance status
        overall_status = 'PASSED' if compliance['compliant'] else 'FAILED'
        status_color = 'green' if compliance['compliant'] else 'red'
        title = f"FTMO Compliance Check: {overall_status}"

        ax5.set_title(title, fontsize=18, color=status_color, fontweight='bold')

        if not compliance['compliant']:
            ax5.text(0.5, 0.1, compliance['reason'],
                     horizontalalignment='center', fontsize=12, color='red',
                     transform=ax5.transAxes)

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"FTMO compliance rapport opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance=100000):
        """
        Genereer een uitgebreid FTMO trading rapport

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans

        Returns:
        --------
        bool
            True als rapport succesvol is gegenereerd
        """
        try:
            # Compliance check
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance['details']:
                print("Onvoldoende data voor FTMO rapport generatie")
                return False

            # Visualisatie maken
            compliance_path = self.plot_ftmo_compliance(initial_balance)

            # Laad trade data voor extra analyses
            df = self.load_trade_data()
            trade_df = df[df['Type'] == 'TRADE'].copy()

            # Analyse per instrument
            symbol_stats = {}
            for symbol in trade_df['Symbol'].unique():
                symbol_df = trade_df[trade_df['Symbol'] == symbol]

                buys = symbol_df[symbol_df['Action'] == 'BUY']
                sells = symbol_df[symbol_df['Action'] == 'SELL']

                symbol_stats[symbol] = {
                    'total_trades': len(symbol_df),
                    'buys': len(buys),
                    'sells': len(sells),
                    'days_traded': symbol_df['Date'].nunique()
                }

            # Toon resultaten
            print("\n===== FTMO Trading Rapport =====")
            print(f"Periode: {df['Timestamp'].min().date()} tot {df['Timestamp'].max().date()}")
            print(f"Initiële balans: ${initial_balance:,.2f}")
            print(f"Eindebalans: ${compliance['details']['final_balance']:,.2f}")
            print(
                f"Totale P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)")
            print(f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%")
            print(
                f"Slechtste dag: {compliance['details']['worst_day_date']} ({compliance['details']['worst_day_drawdown']:.2f}%)")
            print(f"Aantal handelsdagen: {compliance['details']['trading_days']}")
            print("\nInstrumentanalyse:")

            for symbol, stats in symbol_stats.items():
                print(
                    f"  {symbol}: {stats['total_trades']} trades ({stats['buys']} buys, {stats['sells']} sells) over {stats['days_traded']} dagen")

            print(f"\nFTMO Compliance: {'PASSED' if compliance['compliant'] else 'FAILED'}")
            if not compliance['compliant']:
                print(f"Reden: {compliance['reason']}")

            # Compliance visualisatie
            if compliance_path:
                print(f"\nCompliance visualisatie opgeslagen als: {os.path.basename(compliance_path)}")

            return True

        except Exception as e:
            print(f"Fout tijdens rapport generatie: {e}")
            import traceback
            traceback.print_exc()
            return False