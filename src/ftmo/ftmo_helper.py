# src/ftmo/ftmo_helper.py
"""
FTMO Helper module voor het controleren van FTMO compliance en het genereren van rapporten.

Deze module biedt utilities voor het valideren van trading tegen FTMO regels
en het genereren van gedetailleerde compliance rapporten.
"""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter


class FTMOHelper:
    """
    Helper klasse voor het analyseren van trading data en controleren op FTMO rule compliance.
    """

    def __init__(self, log_file_path: str, output_dir: str = "ftmo_reports"):
        """
        Initialiseer de FTMO Helper.

        Args:
            log_file_path: Pad naar het trading logbestand
            output_dir: Directory voor het opslaan van rapportages
        """
        self.log_file = log_file_path
        self.output_dir = output_dir

        # Stel visuele stijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Maak output directory aan
        os.makedirs(output_dir, exist_ok=True)

        # FTMO regels
        self.ftmo_rules = {
            "profit_target": 0.10,  # 10% winstdoel
            "max_daily_loss": 0.05,  # 5% maximale dagelijkse drawdown
            "max_total_loss": 0.10,  # 10% maximale totale drawdown
            "min_trading_days": 4,  # Minimaal 4 handelsdagen
            "challenge_duration": 30,  # Challenge duur van 30 dagen
            "verification_duration": 60,  # Verificatie duur van 60 dagen
        }

        print(f"FTMO Helper geïnitialiseerd: log_file={log_file_path}")

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
            DataFrame met handelsdata, of lege DataFrame bij fout.
        """
        try:
            if not os.path.exists(self.log_file):
                print(f"Logbestand niet gevonden: {self.log_file}")
                return pd.DataFrame()

            df = pd.read_csv(self.log_file)

            if df.empty or "Timestamp" not in df.columns:
                print("Logbestand is leeg of ongeldig formaat")
                return pd.DataFrame()

            # Zet timestamp om naar datetime
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            df["Date"] = df["Timestamp"].dt.date

            print(f"Handelsdata geladen uit {self.log_file}: {len(df)} records")
            return df.dropna(
                subset=["Timestamp"])  # Verwijder rijen met ontbrekende timestamps

        except Exception as e:
            print(f"Fout bij laden handelsdata: {e}")
            return pd.DataFrame()

    def _extract_balance_from_dataframe(self, df: pd.DataFrame) -> pd.Series:
        """
        Helper functie om balanswaarden te extraheren uit dataframe.

        Args:
            df: DataFrame met handelsdata

        Returns:
            Series met balanswaarden
        """
        if "Balance" in df.columns and not df["Balance"].isna().all():
            return df["Balance"]

        # Als Balance kolom niet beschikbaar is, probeer uit Comment te extraheren
        def extract_balance(comment):
            if isinstance(comment, str) and "Balance:" in comment:
                match = re.search(r"Balance:\s*([\d,.]+)", comment)
                return float(match.group(1).replace(",", "")) if match else None
            return None

        return df["Comment"].apply(extract_balance)

    def _calculate_daily_statistics(self, status_df: pd.DataFrame,
                                    initial_balance: float) -> pd.DataFrame:
        """
        Bereken dagelijkse statistieken uit statusdata.

        Args:
            status_df: DataFrame met statusrecords
            initial_balance: Initiële accountbalans

        Returns:
            DataFrame met dagelijkse statistieken
        """
        # Groepeer per dag en bereken statistieken
        daily_stats = status_df.groupby("Date").agg(
            min_balance=("Balance", "min"),
            max_balance=("Balance", "max"),
            close_balance=("Balance", "last")
        ).reset_index()

        if daily_stats.empty:
            return daily_stats

        # Bereken dagelijkse metrics
        daily_stats["prev_close"] = daily_stats["close_balance"].shift(1).fillna(
            initial_balance)
        daily_stats["daily_pnl"] = daily_stats["close_balance"] - daily_stats[
            "prev_close"]
        daily_stats["daily_pnl_pct"] = (daily_stats["daily_pnl"] / daily_stats[
            "prev_close"]) * 100
        daily_stats["daily_drawdown"] = ((daily_stats["min_balance"] - daily_stats[
            "prev_close"]) / daily_stats["prev_close"]) * 100
        daily_stats["peak"] = daily_stats["close_balance"].cummax()
        daily_stats["drawdown_from_peak"] = ((daily_stats["close_balance"] -
                                              daily_stats["peak"]) / daily_stats[
                                                 "peak"]) * 100

        return daily_stats

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict[str, Any]:
        """
        Controleer FTMO compliance met gedetailleerde analyse van handelsdata.

        Args:
            initial_balance: Initiële accountbalans (default: 100000)

        Returns:
            Dict met compliance resultaten en details
        """
        initial_balance = initial_balance or 100000

        df = self.load_trade_data()
        if df.empty:
            return {
                "compliant": False,
                "reason": "Geen handelsdata beschikbaar",
                "details": {}
            }

        # Filter status entries
        status_df = df[df["Type"] == "STATUS"].copy()
        if status_df.empty:
            return {
                "compliant": False,
                "reason": "Geen statusdata beschikbaar",
                "details": {}
            }

        # Extraheer balance waardes
        balance_values = self._extract_balance_from_dataframe(status_df)

        if balance_values.isna().all():
            return {
                "compliant": False,
                "reason": "Geen balansdata beschikbaar",
                "details": {}
            }

        status_df["Balance"] = pd.to_numeric(balance_values, errors="coerce")

        # Bereken statistieken
        daily_stats = self._calculate_daily_statistics(status_df, initial_balance)
        if daily_stats.empty:
            return {
                "compliant": False,
                "reason": "Onvoldoende data voor analyse",
                "details": {}
            }

        # Bereken algemene metrics
        metrics = self._calculate_metrics(daily_stats, df, initial_balance)

        # Evalueer FTMO compliance
        compliance_result = self._evaluate_compliance(metrics, daily_stats)

        # Voeg details toe aan resultaat
        compliance_result["details"] = metrics
        compliance_result["details"]["daily_stats"] = daily_stats

        return compliance_result

    def _calculate_metrics(self, daily_stats: pd.DataFrame, full_df: pd.DataFrame,
                           initial_balance: float) -> Dict[str, Any]:
        """
        Bereken algemene metrics uit dagelijkse statistieken.

        Args:
            daily_stats: DataFrame met dagelijkse statistieken
            full_df: Complete DataFrame met handelsdata
            initial_balance: Initiële accountbalans

        Returns:
            Dict met berekende metrics
        """
        max_drawdown = daily_stats["drawdown_from_peak"].min()
        latest_balance = daily_stats["close_balance"].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Vind slechtste dag
        worst_daily_drawdown = daily_stats["daily_drawdown"].min()
        worst_day_idx = daily_stats["daily_drawdown"].idxmin()
        worst_day_date = daily_stats.iloc[worst_day_idx][
            "Date"] if worst_day_idx is not None else None

        # Check trading days
        trade_df = full_df[full_df["Type"] == "TRADE"]
        unique_trading_days = trade_df["Date"].nunique()

        return {
            "initial_balance": initial_balance,
            "final_balance": latest_balance,
            "total_pnl": total_pnl,
            "total_pnl_pct": total_pnl_pct,
            "max_drawdown": max_drawdown,
            "trading_days": unique_trading_days,
            "worst_daily_drawdown": worst_daily_drawdown,
            "worst_day_date": worst_day_date
        }

    def _evaluate_compliance(self, metrics: Dict[str, Any],
                             daily_stats: pd.DataFrame) -> Dict[str, Any]:
        """
        Evalueer FTMO compliance op basis van metrics.

        Args:
            metrics: Dict met berekende metrics
            daily_stats: DataFrame met dagelijkse statistieken

        Returns:
            Dict met compliance evaluatie
        """
        # Extract key metrics
        total_pnl_pct = metrics["total_pnl_pct"]
        max_drawdown = metrics["max_drawdown"]
        worst_daily_drawdown = metrics["worst_daily_drawdown"]
        unique_trading_days = metrics["trading_days"]

        # Check compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules["profit_target"] * 100
        daily_loss_compliant = worst_daily_drawdown > -self.ftmo_rules[
            "max_daily_loss"] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules["max_total_loss"] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules[
            "min_trading_days"]

        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Generate reason for non-compliance
        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)")

        if not daily_loss_compliant:
            reasons.append(
                f"Dagelijkse verlieslimiet overschreden: {worst_daily_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_daily_loss'] * 100}%)")

        if not total_loss_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")

        if not trading_days_compliant:
            reasons.append(
                f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO-regels"

        return {
            "compliant": compliant,
            "reason": reason,
            "details": {},
            "profit_target_met": profit_target_met,
            "daily_loss_compliant": daily_loss_compliant,
            "total_loss_compliant": total_loss_compliant,
            "trading_days_compliant": trading_days_compliant
        }

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO trading rapport met visualisaties.

        Args:
            initial_balance: Initiële accountbalans (default: 100000)

        Returns:
            bool: True als rapport succesvol gegenereerd
        """
        initial_balance = initial_balance or 100000

        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance.get("details"):
                print("Onvoldoende data voor rapportgeneratie")
                return False

            # Maak rapport figuur
            fig = plt.figure(figsize=(16, 14))
            fig.suptitle("FTMO Trading Compliance Rapport", fontsize=20, y=0.98)

            # Haal dagelijkse statistieken op
            daily_stats = compliance["details"]["daily_stats"]

            # Maak subplots
            gs = plt.GridSpec(3, 2, figure=fig, height_ratios=[2, 1, 1])

            # 1. Account Balance plot
            ax1 = fig.add_subplot(gs[0, :])
            ax1.plot(daily_stats["Date"], daily_stats["close_balance"], "b-",
                     marker="o", label="Account Balance")
            ax1.axhline(y=initial_balance, color="gray", linestyle=":",
                        label="Initial Balance")
            ax1.axhline(y=initial_balance * 1.10, color="green", linestyle="--",
                        label=f"+10% Target (${initial_balance * 1.10:,.2f})")
            ax1.axhline(y=initial_balance * 0.95, color="orange", linestyle="--",
                        label=f"-5% Daily Limit (${initial_balance * 0.95:,.2f})")
            ax1.axhline(y=initial_balance * 0.90, color="red", linestyle="--",
                        label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")

            ax1.set_title("Account Balance Progression", fontsize=16)
            ax1.set_ylabel("Balance ($)", fontsize=14)
            ax1.grid(True)
            ax1.legend(loc="best")

            # 2. Daily P&L plot
            ax2 = fig.add_subplot(gs[1, 0])
            daily_pnl = daily_stats["daily_pnl_pct"]
            bars = ax2.bar(daily_stats["Date"], daily_pnl,
                           color=[("green" if x >= 0 else "red") for x in daily_pnl])

            ax2.set_title("Daily P&L (%)", fontsize=16)
            ax2.set_ylabel("P&L (%)", fontsize=14)
            ax2.grid(True)

            # Voeg labels toe aan bars
            for bar in bars:
                height = bar.get_height()
                if height >= 0:
                    va = 'bottom'
                    y_offset = 0.1
                else:
                    va = 'top'
                    y_offset = -0.1
                ax2.text(bar.get_x() + bar.get_width() / 2., height + y_offset,
                         f"{height:.1f}%", ha='center', va=va, fontsize=9)

            # 3. Drawdown plot
            ax3 = fig.add_subplot(gs[1, 1])
            ax3.fill_between(daily_stats["Date"], daily_stats["drawdown_from_peak"], 0,
                             color="red", alpha=0.3)
            ax3.plot(daily_stats["Date"], daily_stats["drawdown_from_peak"], "r-",
                     label="Drawdown")

            ax3.axhline(y=-5, color="orange", linestyle="--", label="-5% (Daily Limit)")
            ax3.axhline(y=-10, color="red", linestyle="--", label="-10% (Max Drawdown)")

            ax3.set_title("Drawdown (%)", fontsize=16)
            ax3.set_ylabel("Drawdown (%)", fontsize=14)
            ax3.grid(True)
            ax3.legend(loc="best")

            # 4. FTMO Compliance Summary
            ax4 = fig.add_subplot(gs[2, :])
            ax4.axis("off")

            # Stel tabel op met compliance resultaten
            table_data = [
                ["Metric", "Value", "Target", "Status"],
                ["Profit", f"{compliance['details']['total_pnl_pct']:.2f}%",
                 f"≥ {self.ftmo_rules['profit_target'] * 100}%",
                 "✅" if compliance["profit_target_met"] else "❌"],
                ["Max Daily Drawdown",
                 f"{abs(compliance['details']['worst_daily_drawdown']):.2f}%",
                 f"< {self.ftmo_rules['max_daily_loss'] * 100}%",
                 "✅" if compliance["daily_loss_compliant"] else "❌"],
                ["Max Total Drawdown",
                 f"{abs(compliance['details']['max_drawdown']):.2f}%",
                 f"< {self.ftmo_rules['max_total_loss'] * 100}%",
                 "✅" if compliance["total_loss_compliant"] else "❌"],
                ["Trading Days", f"{compliance['details']['trading_days']}",
                 f"≥ {self.ftmo_rules['min_trading_days']}",
                 "✅" if compliance["trading_days_compliant"] else "❌"],
            ]

            tbl = ax4.table(cellText=table_data, loc="center", cellLoc="center",
                            colWidths=[0.25, 0.25, 0.25, 0.15])
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(14)
            tbl.scale(1, 2)

            # Stel kleuren in voor tabel
            header_color = "#40466e"
            pass_color = "#d8f3dc"
            fail_color = "#ffcccb"

            for (i, j), cell in tbl.get_celld().items():
                if i == 0:  # Header row
                    cell.set_facecolor(header_color)
                    cell.set_text_props(color="white", fontweight="bold")
                elif j == 3:  # Status column
                    cell.set_facecolor(
                        pass_color if table_data[i][3] == "✅" else fail_color)

            # Voeg overall status toe
            overall_status = "GESLAAGD" if compliance["compliant"] else "GEFAALD"
            status_color = "green" if compliance["compliant"] else "red"
            ax4.set_title(f"FTMO Compliance Status: {overall_status}",
                          fontsize=18, color=status_color, fontweight="bold")

            if not compliance["compliant"]:
                ax4.text(0.5, 0.05, compliance["reason"],
                         horizontalalignment="center", fontsize=12, color="red",
                         transform=ax4.transAxes)

            # Format plots
            plt.tight_layout(rect=[0, 0, 1, 0.95])

            # Sla rapport op
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"ftmo_report_{timestamp}.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)

            print(f"FTMO rapport gegenereerd: {output_path}")

            # Genereer een tekstsamenvatting in een apart bestand
            summary_path = os.path.join(self.output_dir,
                                        f"ftmo_summary_{timestamp}.txt")
            with open(summary_path, "w") as f:
                f.write("=== FTMO COMPLIANCE REPORT ===\n\n")
                f.write(
                    f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Initial Balance: ${initial_balance:,.2f}\n")
                f.write(
                    f"Final Balance: ${compliance['details']['final_balance']:,.2f}\n")
                f.write(
                    f"Total P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)\n")
                f.write(
                    f"Max Drawdown: {abs(compliance['details']['max_drawdown']):.2f}%\n")
                f.write(
                    f"Worst Daily Drawdown: {abs(compliance['details']['worst_daily_drawdown']):.2f}% on {compliance['details']['worst_day_date']}\n")
                f.write(f"Trading Days: {compliance['details']['trading_days']}\n\n")
                f.write(f"OVERALL STATUS: {overall_status}\n")
                f.write(f"Reason: {compliance['reason']}\n\n")
                f.write("=== FTMO RULES ===\n")
                f.write(f"Profit Target: {self.ftmo_rules['profit_target'] * 100}%\n")
                f.write(f"Max Daily Loss: {self.ftmo_rules['max_daily_loss'] * 100}%\n")
                f.write(f"Max Total Loss: {self.ftmo_rules['max_total_loss'] * 100}%\n")
                f.write(f"Min Trading Days: {self.ftmo_rules['min_trading_days']}\n")

            print(f"FTMO tekstsamenvatting gegenereerd: {summary_path}")
            return True

        except Exception as e:
            print(f"Fout bij rapportgeneratie: {e}")
            import traceback
            traceback.print_exc()
            return False
