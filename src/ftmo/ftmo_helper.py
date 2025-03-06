import logging
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FTMOHelper:
    """Helper class for FTMO compliance checks and reporting"""

    def __init__(self, log_file: str, output_dir: str = 'data/ftmo_analysis'):
        self.log_file = log_file
        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

        # Configure visualization style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Logging setup
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # FTMO rules
        self.ftmo_rules = {
            'profit_target': 0.10,
            'max_daily_loss': -0.05,  # Corrected sign
            'max_total_loss': -0.10,  # Corrected sign
            'min_trading_days': 4,
            'challenge_duration': 30,
            'verification_duration': 60
        }

    def load_trade_data(self) -> pd.DataFrame:
        """Load trading data from log file"""
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df['Date'] = df['Timestamp'].dt.date
            return df.dropna(subset=['Timestamp'])  # Verwijder rijen met foutieve timestamps
        except Exception as e:
            logging.error(f"Error loading trading data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance: float) -> Dict:
        """Check FTMO compliance with detailed analysis"""
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'No trading data available', 'details': {}}

        # Extract STATUS entries for balance tracking
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'No account status data available', 'details': {}}

        # Convert balance to numeric
        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        status_df.dropna(subset=['Balance'], inplace=True)

        # Compute daily balance statistics
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        # Ensure we have data before proceeding
        if daily_status.empty:
            return {'compliant': False, 'reason': 'Insufficient balance data available', 'details': {}}

        # Calculate daily P&L and drawdowns
        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = ((daily_status['min_balance'] - daily_status['prev_close'])
                                          / daily_status['prev_close']) * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = ((daily_status['close_balance'] - daily_status['peak'])
                                              / daily_status['peak']) * 100

        # Calculate key metrics
        max_drawdown = daily_status['drawdown_from_peak'].min()
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Check trading days
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # Check FTMO rules compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() >= self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown >= self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']

        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Generate reason for non-compliance if applicable
        reasons = []
        if not profit_target_met:
            reasons.append(f"Profit target not reached: {total_pnl_pct:.2f}% "
                           f"(target: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(f"Daily loss limit exceeded: {worst_day['daily_drawdown']:.2f}% on {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(f"Maximum drawdown exceeded: {max_drawdown:.2f}% "
                           f"(limit: {self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(f"Insufficient trading days: {unique_trading_days} "
                           f"(minimum: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Complies with all FTMO rules"

        # Compile results
        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status.to_dict(orient='records')  # Converted for better JSON compatibility
        }

        return {
            'compliant': compliant,
            'reason': reason,
            'details': details
        }

    def generate_trading_report(self, initial_balance: float) -> bool:
        """Generate detailed FTMO trading report with visualizations"""
        try:
            results = self.check_ftmo_compliance(initial_balance)
            daily_status = pd.DataFrame(results['details'].get('daily_stats', []))

            if daily_status.empty:
                logging.warning("No data available for generating trading report.")
                return False

            # Plot balance over time
            plt.figure(figsize=(12, 6))
            plt.plot(daily_status['Date'], daily_status['close_balance'], marker='o', label='Balance')
            plt.fill_between(daily_status['Date'], daily_status['min_balance'], daily_status['max_balance'],
                             alpha=0.3, color='gray', label="Daily Range")
            plt.axhline(y=initial_balance, color='r', linestyle='--', label="Initial Balance")
            plt.title("Trading Balance Over Time")
            plt.xlabel("Date")
            plt.ylabel("Balance")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the figure
            report_path = os.path.join(self.output_dir, "trading_report.png")
            plt.savefig(report_path)
            logging.info(f"Trading report saved at {report_path}")

            return True
        except Exception as e:
            logging.error(f"Error generating trading report: {e}")
            return False
