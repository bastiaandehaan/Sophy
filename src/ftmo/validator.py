# validator.py
import os
from datetime import datetime, date
from typing import Dict, Tuple, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FTMOValidator:
    """Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels"""

    def __init__(self, config: Dict[str, any], log_file: str, output_dir='data/ftmo_analysis',
                 logger: any = None) -> None:
        """
        Initialiseer de FTMO Validator met configuratie, logbestand en outputmap.

        Parameters:
        -----------
        config : Dict[str, any]
            Configuratiedictionary met risicoparameters (bijv. initial_balance)
        log_file : str
            Pad naar het logbestand met handelsdata
        output_dir : str, optional
            Map voor het opslaan van analyse-uitvoer (default: 'data/ftmo_analysis')
        logger : any, optional
            Logging-object voor het bijhouden van gebeurtenissen
        """
        self.config = config
        self.logger = logger
        self.initial_balance = config['risk'].get('account_balance', 100000)
        self.start_date = date.today()
        self.trade_days = set()
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak outputmap aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # FTMO-regels (geharmoniseerd)
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% winstdoel
            'max_daily_loss': 0.05,  # 5% maximale dagelijkse drawdown
            'max_total_loss': 0.10,  # 10% maximale totale drawdown
            'min_trading_days': 10,  # Minimaal 10 handelsdagen (van FTMOValidator)
            'challenge_duration': 30,  # Challenge-duur van 30 dagen
            'verification_duration': 60  # Verificatie-duur van 60 dagen
        }

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata
        """
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            return df
        except Exception as e:
            if self.logger:
                self.logger.error(f"Fout bij laden van handelsdata: {e}")
            return pd.DataFrame()

    def validate_account_state(self, account_info: Dict[str, float] = None) -> Tuple[bool, Optional[str]]:
        """
        Valideer de accountstatus volgens FTMO-regels, met optionele fallback op handelsdata.

        Args:
            account_info: Huidige accountinformatie (optioneel)

        Returns:
            Tuple[bool, Optional[str]]: (is_compliant, violation_reason)
        """
        if account_info is None:
            df = self.load_trade_data()
            if df.empty:
                return False, "Geen handelsdata beschikbaar"
            status_df = df[df['Type'] == 'STATUS'].copy()

            # Extraheer balans uit 'Comment' als 'Balance' ontbreekt
            if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
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

            if status_df['Balance'].isna().all():
                return False, "Geen balansdata beschikbaar"

            status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
            daily_status = status_df.groupby('Date').agg(
                close_balance=('Balance', 'last')
            ).reset_index()
            current_equity = daily_status['close_balance'].iloc[-1]
        else:
            current_equity = account_info.get('equity', self.initial_balance)

        # Bereken winst/verlies percentage
        profit_loss_pct = (current_equity - self.initial_balance) / self.initial_balance * 100

        # Registreer handelsdag
        self.trade_days.add(date.today())

        # Controleer winstdoel (10%)
        if profit_loss_pct >= self.ftmo_rules['profit_target'] * 100:
            return True, "Winstdoel bereikt"

        # Controleer dagelijkse verlieslimiet (5%)
        if profit_loss_pct <= -self.ftmo_rules['max_daily_loss'] * 100:
            return False, "Dagelijkse verlieslimiet overschreden"

        # Controleer maximale drawdown (10%)
        if profit_loss_pct <= -self.ftmo_rules['max_total_loss'] * 100:
            return False, "Maximale drawdown overschreden"

        # Controleer minimale handelsdagen (bijna einde challenge)
        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= self.ftmo_rules['challenge_duration'] - 2:
            unique_trading_days = len(self.trade_days)
            if unique_trading_days < self.ftmo_rules['min_trading_days']:
                if self.logger:
                    self.logger.warning(
                        f"Slechts {unique_trading_days} handelsdagen, FTMO vereist {self.ftmo_rules['min_trading_days']}")
                return False, f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})"

        return True, None

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict:
        """
        Controleer FTMO-naleving met gedetailleerde analyse van handelsdata.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config)

        Returns:
        --------
        Dict
            Resultaten van naleving met details
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'Geen handelsdata beschikbaar', 'details': {}}

        status_df = df[df['Type'] == 'STATUS'].copy()

        # Extraheer balans indien nodig
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
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

        if status_df['Balance'].isna().all():
            return {'compliant': False, 'reason': 'Geen balansdata beschikbaar', 'details': {}}

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        # Bereken dagelijkse P&L en drawdown
        daily_status['prev_close'] = daily_status['close_balance'].shift(1)
        daily_status.loc[0, 'prev_close'] = initial_balance
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_drawdown'] = (daily_status['min_balance'] - daily_status['prev_close']) / daily_status[
            'prev_close'] * 100

        # Bereken totale P&L en maximale drawdown
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = (daily_status['close_balance'] - daily_status['peak']) / daily_status[
            'peak'] * 100
        max_drawdown = daily_status['drawdown_from_peak'].min()

        # Controleer handelsactiviteit
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # Evalueer naleving
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() > -self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']
        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Reden voor niet-naleving
        reason = ''
        if not compliant:
            reasons = []
            if not profit_target_met:
                reasons.append(
                    f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)")
            if not daily_loss_compliant:
                worst_day_idx = daily_status['daily_drawdown'].idxmin()
                worst_day = daily_status.iloc[worst_day_idx]
                reasons.append(
                    f"Dagelijkse verlieslimiet overschreden: {worst_day['daily_drawdown']:.2f}% op {worst_day['Date']}")
            if not total_loss_compliant:
                reasons.append(
                    f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")
            if not trading_days_compliant:
                reasons.append(
                    f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")
            reason = "; ".join(reasons)

        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status
        }

        return {
            'compliant': compliant,
            'reason': reason if not compliant else "Voldoet aan alle FTMO-regels",
            'details': details
        }

    def plot_ftmo_compliance(self, initial_balance: float = None) -> Optional[str]:
        """
        Maak een visualisatie van FTMO-naleving.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config)

        Returns:
        --------
        str
            Pad naar opgeslagen grafiek, of None bij mislukking
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance['details']:
            print("Onvoldoende data voor FTMO-analyse")
            return None

        daily_stats = compliance['details']['daily_stats']
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(4, 2, height_ratios=[2, 1, 1, 1])

        # 1. Balansgrafiek
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(daily_stats['Date'], daily_stats['close_balance'], 'b-', label='Accountbalans')
        ax1.axhline(y=initial_balance, color='gray', linestyle=':', label='Initiële balans')
        ax1.axhline(y=initial_balance * 1.10, color='green', linestyle='--',
                    label=f"+10% Doel (${initial_balance * 1.10:,.2f})")
        ax1.axhline(y=initial_balance * 0.95, color='orange', linestyle='--',
                    label=f"-5% Daglimiet (${initial_balance * 0.95:,.2f})")
        ax1.axhline(y=initial_balance * 0.90, color='red', linestyle='--',
                    label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")
        ax1.set_title('FTMO Accountbalans Progressie', fontsize=16)
        ax1.set_ylabel('Balans ($)', fontsize=14)
        ax1.legend(loc='best', fontsize=12)
        ax1.grid(True)

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['green' if x >= 0 else 'red' for x in daily_stats['daily_pnl']]
        ax2.bar(daily_stats['Date'], daily_stats['daily_pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Dagelijkse P&L ($)', fontsize=14)
        ax2.set_ylabel('P&L ($)', fontsize=12)
        ax2.grid(True, axis='y')

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(daily_stats['Date'], daily_stats['daily_drawdown'], 0,
                         where=(daily_stats['daily_drawdown'] < 0), color='red', alpha=0.3)
        ax3.plot(daily_stats['Date'], daily_stats['daily_drawdown'], 'r-', alpha=0.7)
        ax3.axhline(y=-5, color='orange', linestyle='--', label='-5% Daglimiet')
        ax3.set_title('Dagelijkse Drawdown (%)', fontsize=14)
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_ylim(min(-10, daily_stats['daily_drawdown'].min() * 1.2), 1)
        ax3.legend(loc='lower right', fontsize=10)
        ax3.grid(True)

        # 4. Cumulatieve drawdown vanaf piek
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(daily_stats['Date'], daily_stats['drawdown_from_peak'], 0, color='purple', alpha=0.3)
        ax4.plot(daily_stats['Date'], daily_stats['drawdown_from_peak'], 'purple', alpha=0.7)
        ax4.axhline(y=-10, color='red', linestyle='--', label='-10% Max Drawdown')
        ax4.set_title('Maximale Drawdown vanaf Piek (%)', fontsize=14)
        ax4.set_ylabel('Drawdown (%)', fontsize=12)
        ax4.set_ylim(min(-12, daily_stats['drawdown_from_peak'].min() * 1.2), 1)
        ax4.legend(loc='lower right', fontsize=10)
        ax4.grid(True)

        # 5. Nalevingstabel
        ax5 = fig.add_subplot(gs[3, :])
        ax5.axis('off')
        compliance_data = [
            ['Metriek', 'Waarde', 'Vereiste', 'Status'],
            ['Totale P&L', f"{compliance['details']['total_pnl_pct']:.2f}%",
             f"≥ {self.ftmo_rules['profit_target'] * 100}%",
             '✅' if compliance['details']['total_pnl_pct'] >= 10 else '❌'],
            ['Max Dagelijkse Drawdown', f"{daily_stats['daily_drawdown'].min():.2f}%",
             f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
             '✅' if daily_status['daily_drawdown'].min() > -5 else '❌'],
            ['Max Totale Drawdown', f"{compliance['details']['max_drawdown']:.2f}%",
             f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
             '✅' if compliance['details']['max_drawdown'] > -10 else '❌'],
            ['Handelsdagen', f"{compliance['details']['trading_days']}", f"≥ {self.ftmo_rules['min_trading_days']}",
             '✅' if compliance['details']['trading_days'] >= 10 else '❌']
        ]
        tbl = ax5.table(cellText=compliance_data, loc='center', cellLoc='center', colWidths=[0.25, 0.25, 0.25, 0.15])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        header_color = '#40466e'
        pass_color = '#d8f3dc'
        fail_color = '#ffcccb'
        for (i, j), cell in tbl.get_celld().items():
            if i == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            elif j == 3:
                cell.set_facecolor(pass_color if compliance_data[i][3] == '✅' else fail_color)

        overall_status = 'GESLAAGD' if compliance['compliant'] else 'GEFAALD'
        status_color = 'green' if compliance['compliant'] else 'red'
        ax5.set_title(f"FTMO Naleving: {overall_status}", fontsize=18, color=status_color, fontweight='bold')
        if not compliance['compliant']:
            ax5.text(0.5, 0.1, compliance['reason'], horizontalalignment='center', fontsize=12, color='red',
                     transform=ax5.transAxes)

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()
        if self.logger:
            self.logger.info(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO handelsrapport.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config)

        Returns:
        --------
        bool
            True als rapport succesvol gegenereerd
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance['details']:
                print("Onvoldoende data voor rapportgeneratie")
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)
            df = self.load_trade_data()
            trade_df = df[df['Type'] == 'TRADE'].copy()

            # Instrumentanalyse
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

            # Rapportweergave
            print("\n===== FTMO Handelsrapport =====")
            print(f"Periode: {df['Timestamp'].min().date()} tot {df['Timestamp'].max().date()}")
            print(f"Initiële balans: ${initial_balance:,.2f}")
            print(f"Eindebalans: ${compliance['details']['final_balance']:,.2f}")
            print(
                f"Totale P&L: ${compliance['details']['final_balance'] - initial_balance:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)")
            print(f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%")
            print(f"Aantal handelsdagen: {compliance['details']['trading_days']}")
            print("\nInstrumentanalyse:")
            for symbol, stats in symbol_stats.items():
                print(
                    f"  {symbol}: {stats['total_trades']} trades ({stats['buys']} buys, {stats['sells']} sells) over {stats['days_traded']} dagen")
            print(f"\nFTMO Naleving: {'GESLAAGD' if compliance['compliant'] else 'GEFAALD'}")
            if not compliance['compliant']:
                print(f"Reden: {compliance['reason']}")
            if compliance_path:
                print(f"\nNalevingsvisualisatie opgeslagen als: {os.path.basename(compliance_path)}")

            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Fout bij rapportgeneratie: {e}")
            return False


if __name__ == "__main__":
    # Voorbeeldgebruik
    config = {'risk': {'account_balance': 100000}}
    validator = FTMOValidator(config, log_file="trade_log.csv")
    is_valid, reason = validator.validate_account_state()
    print(f"Validatieresultaat: {is_valid}, Reden: {reason}")
    compliance = validator.check_ftmo_compliance()
    print(f"Nalevingscontrole: {compliance['compliant']}, Reden: {compliance['reason']}")
    plot_path = validator.plot_ftmo_compliance()
    if plot_path:
        print(f"Grafiek opgeslagen op: {plot_path}")
    report_generated = validator.generate_trading_report()
    print(f"Rapport gegenereerd: {report_generated}")