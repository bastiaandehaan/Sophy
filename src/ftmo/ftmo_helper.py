# src/ftmo/ftmo_helper.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional
import os
from datetime import datetime, date


class FTMOHelper:
    """Helper class for FTMO compliance checks and reporting"""

    def __init__(self, log_file: str, output_dir: str = 'data/ftmo_analysis'):
        self.log_file = log_file
        self.output_dir = output_dir

        # Create output directory if needed
        os.makedirs(output_dir, exist_ok=True)

        # Configure visualization style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # FTMO rules
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% profit target
            'max_daily_loss': 0.05,  # 5% max daily drawdown
            'max_total_loss': 0.10,  # 10% max total drawdown
            'min_trading_days': 4,  # Minimum 4 trading days
            'challenge_duration': 30,  # Challenge duration in days
            'verification_duration': 60  # Verification duration in days
        }

    def load_trade_data(self) -> pd.DataFrame:
        """Load trading data from log file"""
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            return df
        except Exception as e:
            print(f"Error loading trading data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance: float) -> Dict:
        """Check FTMO compliance with detailed analysis"""
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'No trading data available', 'details': {}}

        # Extract STATUS entries for balance tracking
        status_df = df[df['Type'] == 'STATUS'].copy()

        # Extract balance and process data
        # [Implementation details continue...]

        # For brevity, this method implementation is abbreviated

        return {
            'compliant': compliant,
            'reason': reason if not compliant else "Complies with all FTMO rules",
            'details': details
        }

    def generate_trading_report(self, initial_balance: float) -> bool:
        """Generate detailed FTMO trading report with visualizations"""
        # [Implementation details...]
        # This would generate a full report with visualizations
        return True