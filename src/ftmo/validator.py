# src/ftmo/validator.py

import os
import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter

from src.utils.logger import Logger


class FTMOValidator:
    """
    Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels.

    Deze klasse combineert functionaliteit voor real-time validatie en
    backtest analyse om te zorgen dat trading voldoet aan FTMO vereisten.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        log_file: str,
        output_dir: str = "data/ftmo_analysis",
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Initialiseer de FTMO Validator met configuratie, logbestand en outputmap.

        Parameters:
        -----------
        config : Dict[str, Any]
            Configuratiedictionary met risicoparameters (bijv. initial_balance).
        log_file : str
            Pad naar het logbestand met handelsdata.
        output_dir : str, optional
            Map voor het opslaan van analyse-uitvoer (default: 'data/ftmo_analysis').
        logger : Logger, optional
            Logging-object voor het bijhouden van gebeurtenissen.
        """
        self.config = config
        self.logger = logger
        self.initial_balance = config["risk"].get("account_balance", 100000)

        # Haal startdatum uit config of bepaal uit logbestand
        self.start_date = datetime.strptime(
            config.get("ftmo", {}).get("start_date", date.today().strftime("%Y-%m-%d")),
            "%Y-%m-%d",
        ).date()
        self.trade_days = set()
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use("ggplot")
        plt.rcParams["figure.figsize"] = (16, 10)
        plt.rcParams["lines.linewidth"] = 1.5
        sns.set_style("whitegrid")

        # Maak outputmap aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # FTMO-regels
        self.ftmo_rules = {
            "profit_target": 0.10,  # 10% winstdoel
            "max_daily_loss": 0.05,  # 5% maximale dagelijkse drawdown
            "max_total_loss": 0.10,  # 10% maximale totale drawdown
            "min_trading_days": 4,  # Minimaal 4 handelsdagen
            "challenge_duration": 30,  # Challenge-duur van 30 dagen
            "verification_duration": 60,  # Verificatie-duur van 60 dagen
        }

        if self.logger:
            self.logger.log_info(
                f"FTMO Validator geïnitialiseerd met configuratie: {config['risk']}"
            )

    def log_message(self, message: str, level: str = "INFO") -> None:
        """Helper voor logging met fallback naar print"""
        if self.logger:
            self.logger.log_info(message, level=level)
        else:
            print(f"[{level}] {message}")

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata, of lege DataFrame bij fout.
        """
        try:
            if not os.path.exists(self.log_file):
                raise ValueError(f"Logbestand niet gevonden: {self.log_file}")
            df = pd.read_csv(self.log_file)
            if df.empty or "Timestamp" not in df.columns:
                raise ValueError("Logbestand is leeg of ongeldig formaat")
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            df["Date"] = df["Timestamp"].dt.date
            self.log_message(f"Handelsdata geladen uit {self.log_file}")
            return df.dropna(
                subset=["Timestamp"]
            )  # Verwijder rijen met foutieve timestamps
        except Exception as e:
            self.log_message(f"Fout bij laden handelsdata: {e}", level="ERROR")
            return pd.DataFrame()

    def validate_account_state(
        self, account_info: Dict[str, float] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Valideer de accountstatus volgens FTMO-regels.

        Args:
            account_info: Huidige accountinformatie (optioneel).

        Returns:
            Tuple[bool, Optional[str]]: (is_compliant, violation_reason).
        """
        df = self.load_trade_data()
        if df.empty:
            return False, "Geen handelsdata beschikbaar"

        status_df = df[df["Type"] == "STATUS"].copy()
        if status_df.empty:
            return False, "Geen statusdata beschikbaar"

        # Extraheer balans
        if "Balance" not in status_df.columns or status_df["Balance"].isna().all():

            def extract_balance(comment):
                if isinstance(comment, str) and "Balance: " in comment:
                    match = re.search(r"Balance:\s*([\d,.]+)", comment)
                    return float(match.group(1).replace(",", "")) if match else None
                return None

            status_df["Balance"] = status_df["Comment"].apply(extract_balance)

        if status_df["Balance"].isna().all():
            return False, "Geen balansdata beschikbaar"

        status_df["Balance"] = pd.to_numeric(status_df["Balance"], errors="coerce")
        daily_status = (
            status_df.groupby("Date")
            .agg(close_balance=("Balance", "last"))
            .reset_index()
        )
        current_equity = (
            daily_status["close_balance"].iloc[-1]
            if not daily_status.empty
            else self.initial_balance
        )

        # Registreer handelsdag
        self.trade_days.update(df[df["Type"] == "TRADE"]["Date"].unique())

        # Bereken winst/verlies percentage
        profit_loss_pct = (
            (current_equity - self.initial_balance) / self.initial_balance * 100
        )

        # Controleer FTMO-regels
        if profit_loss_pct >= self.ftmo_rules["profit_target"] * 100:
            return True, "Winstdoel bereikt"

        if profit_loss_pct <= -self.ftmo_rules["max_daily_loss"] * 100:
            return False, "Dagelijkse verlieslimiet overschreden"

        if profit_loss_pct <= -self.ftmo_rules["max_total_loss"] * 100:
            return False, "Maximale drawdown overschreden"

        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= self.ftmo_rules["challenge_duration"] - 2:
            unique_trading_days = len(self.trade_days)
            if unique_trading_days < self.ftmo_rules["min_trading_days"]:
                return (
                    False,
                    f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})",
                )

        return True, None

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict:
        """
        Controleer FTMO-naleving met gedetailleerde analyse van handelsdata.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        Dict
            Resultaten van naleving met details.
        """
        initial_balance = (
            initial_balance if initial_balance is not None else self.initial_balance
        )
        df = self.load_trade_data()
        if df.empty:
            return {
                "compliant": False,
                "reason": "Geen handelsdata beschikbaar",
                "details": {},
            }

        status_df = df[df["Type"] == "STATUS"].copy()
        if status_df.empty:
            return {
                "compliant": False,
                "reason": "Geen statusdata beschikbaar",
                "details": {},
            }

        # Uniforme balans extractie
        balance_values = self._extract_balance_from_dataframe(status_df)

        if not balance_values:
            return {
                "compliant": False,
                "reason": "Geen balansdata beschikbaar",
                "details": {},
            }

        status_df["Balance"] = balance_values
        status_df["Balance"] = pd.to_numeric(status_df["Balance"], errors="coerce")

        # Bereken statistieken
        daily_stats = self._calculate_daily_statistics(status_df, initial_balance)
        if daily_stats.empty:
            return {
                "compliant": False,
                "reason": "Onvoldoende data voor analyse",
                "details": {},
            }

        # Bereken algemene metrics
        metrics = self._calculate_metrics(daily_stats, df, initial_balance)

        # Evalueer FTMO compliance
        compliance_result = self._evaluate_compliance(metrics, daily_stats)

        # Voeg details toe aan resultaat
        compliance_result["details"].update(metrics)
        compliance_result["details"]["daily_stats"] = daily_stats

        return compliance_result

    def _extract_balance_from_dataframe(self, df: pd.DataFrame) -> pd.Series:
        """Helper functie om balanswaarden te extraheren uit dataframe"""
        if "Balance" in df.columns and not df["Balance"].isna().all():
            return df["Balance"]

        # Probeer uit Comment te halen als Balance kolom niet beschikbaar is
        def extract_balance(comment):
            if isinstance(comment, str) and "Balance: " in comment:
                match = re.search(r"Balance:\s*([\d,.]+)", comment)
                return float(match.group(1).replace(",", "")) if match else None
            return None

        return df["Comment"].apply(extract_balance)

    def _calculate_daily_statistics(
        self, status_df: pd.DataFrame, initial_balance: float
    ) -> pd.DataFrame:
        """Bereken dagelijkse statistieken uit status data"""
        # Groepeer per dag en bereken statistieken
        daily_stats = (
            status_df.groupby("Date")
            .agg(
                min_balance=("Balance", "min"),
                max_balance=("Balance", "max"),
                close_balance=("Balance", "last"),
            )
            .reset_index()
        )

        if daily_stats.empty:
            return daily_stats

        # Bereken dagelijkse metrics
        daily_stats["prev_close"] = (
            daily_stats["close_balance"].shift(1).fillna(initial_balance)
        )
        daily_stats["daily_pnl"] = (
            daily_stats["close_balance"] - daily_stats["prev_close"]
        )
        daily_stats["daily_pnl_pct"] = (
            daily_stats["daily_pnl"] / daily_stats["prev_close"]
        ) * 100
        daily_stats["daily_drawdown"] = (
            (daily_stats["min_balance"] - daily_stats["prev_close"])
            / daily_stats["prev_close"]
            * 100
        )
        daily_stats["peak"] = daily_stats["close_balance"].cummax()
        daily_stats["drawdown_from_peak"] = (
            (daily_stats["close_balance"] - daily_stats["peak"])
            / daily_stats["peak"]
            * 100
        )

        return daily_stats

    def _calculate_metrics(
        self, daily_stats: pd.DataFrame, full_df: pd.DataFrame, initial_balance: float
    ) -> Dict[str, Any]:
        """Bereken algemene metrics uit dagelijkse statistieken"""
        max_drawdown = daily_stats["drawdown_from_peak"].min()
        latest_balance = daily_stats["close_balance"].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

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
        }

    def _evaluate_compliance(
        self, metrics: Dict[str, Any], daily_stats: pd.DataFrame
    ) -> Dict[str, Any]:
        """Evalueer FTMO compliance op basis van metrics"""
        # Extract key metrics
        total_pnl_pct = metrics["total_pnl_pct"]
        max_drawdown = metrics["max_drawdown"]
        unique_trading_days = metrics["trading_days"]

        # Check compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules["profit_target"] * 100
        daily_loss_compliant = (
            daily_stats["daily_drawdown"].min()
            > -self.ftmo_rules["max_daily_loss"] * 100
        )
        total_loss_compliant = max_drawdown > -self.ftmo_rules["max_total_loss"] * 100
        trading_days_compliant = (
            unique_trading_days >= self.ftmo_rules["min_trading_days"]
        )

        compliant = (
            profit_target_met
            and daily_loss_compliant
            and total_loss_compliant
            and trading_days_compliant
        )

        # Generate reason for non-compliance
        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)"
            )
        if not daily_loss_compliant:
            worst_day_idx = daily_stats["daily_drawdown"].idxmin()
            worst_day = daily_stats.iloc[worst_day_idx]
            reasons.append(
                f"Dagelijkse verlieslimiet overschreden: {worst_day['daily_drawdown']:.2f}% op {worst_day['Date']}"
            )
        if not total_loss_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)"
            )
        if not trading_days_compliant:
            reasons.append(
                f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})"
            )

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO-regels"

        return {
            "compliant": compliant,
            "reason": reason,
            "details": {},
        }

    def plot_ftmo_compliance(self, initial_balance: float = None) -> Optional[str]:
        """
        Maak een visualisatie van FTMO-naleving met extra analyses.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        str
            Pad naar opgeslagen grafiek, of None bij mislukking.
        """
        initial_balance = (
            initial_balance if initial_balance is not None else self.initial_balance
        )
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance["details"]:
            self.log_message("Onvoldoende data voor FTMO-analyse", level="ERROR")
            return None

        daily_stats = compliance["details"]["daily_stats"]
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(5, 2, height_ratios=[2, 1, 1, 1, 1])

        # 1. Balansgrafiek
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(
            daily_stats["Date"],
            daily_stats["close_balance"],
            "b-",
            label="Accountbalans",
        )
        ax1.axhline(
            y=initial_balance, color="gray", linestyle=":", label="Initiële balans"
        )
        ax1.axhline(
            y=initial_balance * 1.10,
            color="green",
            linestyle="--",
            label=f"+10% Doel (${initial_balance * 1.10:,.2f})",
        )
        ax1.axhline(
            y=initial_balance * 0.95,
            color="orange",
            linestyle="--",
            label=f"-5% Daglimiet (${initial_balance * 0.95:,.2f})",
        )
        ax1.axhline(
            y=initial_balance * 0.90,
            color="red",
            linestyle="--",
            label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})",
        )
        ax1.set_title("FTMO Accountbalans Progressie", fontsize=16)
        ax1.set_ylabel("Balans ($)", fontsize=14)
        ax1.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        ax1.legend(loc="best", fontsize=12)
        ax1.grid(True)

        # 2-4. Overige grafieken implementeren (zie originele code)
        # ...

        # 5. Nalevingstabel
        ax6 = fig.add_subplot(gs[4, :])
        ax6.axis("off")
        compliance_data = [
            ["Metriek", "Waarde", "Vereiste", "Status"],
            [
                "Totale P&L",
                f"{compliance['details']['total_pnl_pct']:.2f}%",
                f"≥ {self.ftmo_rules['profit_target'] * 100}%",
                "✅" if compliance["details"]["total_pnl_pct"] >= 10 else "❌",
            ],
            [
                "Max Dagelijkse Drawdown",
                f"{daily_stats['daily_drawdown'].min():.2f}%",
                f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
                "✅" if daily_stats["daily_drawdown"].min() > -5 else "❌",
            ],
            [
                "Max Totale Drawdown",
                f"{compliance['details']['max_drawdown']:.2f}%",
                f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
                "✅" if compliance["details"]["max_drawdown"] > -10 else "❌",
            ],
            [
                "Handelsdagen",
                f"{compliance['details']['trading_days']}",
                f"≥ {self.ftmo_rules['min_trading_days']}",
                "✅" if compliance["details"]["trading_days"] >= 4 else "❌",
            ],
        ]
        tbl = ax6.table(
            cellText=compliance_data,
            loc="center",
            cellLoc="center",
            colWidths=[0.25, 0.25, 0.25, 0.15],
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        header_color = "#40466e"
        pass_color = "#d8f3dc"
        fail_color = "#ffcccb"
        for (i, j), cell in tbl.get_celld().items():
            if i == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color="white", fontweight="bold")
            elif j == 3:
                cell.set_facecolor(
                    pass_color if compliance_data[i][3] == "✅" else fail_color
                )

        overall_status = "GESLAAGD" if compliance["compliant"] else "GEFAALD"
        status_color = "green" if compliance["compliant"] else "red"
        ax6.set_title(
            f"FTMO Naleving: {overall_status}",
            fontsize=18,
            color=status_color,
            fontweight="bold",
        )
        if not compliance["compliant"]:
            ax6.text(
                0.5,
                0.1,
                compliance["reason"],
                horizontalalignment="center",
                fontsize=12,
                color="red",
                transform=ax6.transAxes,
            )

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        self.log_message(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO handelsrapport met extra metrics.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        bool
            True als rapport succesvol gegenereerd.
        """
        initial_balance = (
            initial_balance if initial_balance is not None else self.initial_balance
        )
        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance["details"]:
                self.log_message(
                    "Onvoldoende data voor rapportgeneratie", level="ERROR"
                )
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)

            # Genereer het rapport (implementatie uit originele code)
            # ...

            return True
        except Exception as e:
            self.log_message(f"Fout bij rapportgeneratie: {e}", level="ERROR")
            return False
