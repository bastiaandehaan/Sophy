# src/ftmo/ftmo_validator.py

import os
import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter

from src.utils.logger import Logger  # Importeer de Logger-klasse


class FTMOValidator:
    """Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels."""

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

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata, of lege DataFrame bij fout.

        Raises:
        -------
        ValueError
            Als het logbestand ongeldig is.
        """
        try:
            if not os.path.exists(self.log_file):
                raise ValueError(f"Logbestand niet gevonden: {self.log_file}")
            df = pd.read_csv(self.log_file)
            if df.empty or "Timestamp" not in df.columns:
                raise ValueError("Logbestand is leeg of ongeldig formaat")
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Date"] = df["Timestamp"].dt.date
            if self.logger:
                self.logger.log_info(f"Handelsdata geladen uit {self.log_file}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij laden handelsdata: {e}", level="ERROR")
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

        # Extraheer balans
        if "Balance" not in status_df.columns or status_df["Balance"].isna().all():

            def extract_balance(comment):
                if isinstance(comment, str) and "Balance: " in comment:
                    match = re.search(r"Balance:\s*([\d,.]+)", comment)
                    return float(match.group(1).replace(",", "")) if match else None
                return None

            status_df["Balance"] = status_df["Comment"].apply(extract_balance)

        if status_df["Balance"].isna().all():
            return {
                "compliant": False,
                "reason": "Geen balansdata beschikbaar",
                "details": {},
            }

        status_df["Balance"] = pd.to_numeric(status_df["Balance"], errors="coerce")
        daily_status = (
            status_df.groupby("Date")
            .agg(
                min_balance=("Balance", "min"),
                max_balance=("Balance", "max"),
                close_balance=("Balance", "last"),
            )
            .reset_index()
        )

        daily_status["prev_close"] = (
            daily_status["close_balance"].shift(1).fillna(initial_balance)
        )
        daily_status["daily_pnl"] = (
            daily_status["close_balance"] - daily_status["prev_close"]
        )
        daily_status["daily_pnl_pct"] = (
            daily_status["daily_pnl"] / daily_status["prev_close"]
        ) * 100
        daily_status["daily_drawdown"] = (
            (daily_status["min_balance"] - daily_status["prev_close"])
            / daily_status["prev_close"]
            * 100
        )
        daily_status["peak"] = daily_status["close_balance"].cummax()
        daily_status["drawdown_from_peak"] = (
            (daily_status["close_balance"] - daily_status["peak"])
            / daily_status["peak"]
            * 100
        )
        max_drawdown = daily_status["drawdown_from_peak"].min()

        latest_balance = daily_status["close_balance"].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        trade_df = df[df["Type"] == "TRADE"]
        unique_trading_days = trade_df["Date"].nunique()

        profit_target_met = total_pnl_pct >= self.ftmo_rules["profit_target"] * 100
        daily_loss_compliant = (
            daily_status["daily_drawdown"].min()
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

        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)"
            )
        if not daily_loss_compliant:
            worst_day_idx = daily_status["daily_drawdown"].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
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

        details = {
            "initial_balance": initial_balance,
            "final_balance": latest_balance,
            "total_pnl": total_pnl,
            "total_pnl_pct": total_pnl_pct,
            "max_drawdown": max_drawdown,
            "trading_days": unique_trading_days,
            "daily_stats": daily_status,
        }

        return {"compliant": compliant, "reason": reason, "details": details}

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
            if self.logger:
                self.logger.log_info(
                    "Onvoldoende data voor FTMO-analyse", level="ERROR"
                )
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

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ["green" if x >= 0 else "red" for x in daily_stats["daily_pnl"]]
        ax2.bar(daily_stats["Date"], daily_stats["daily_pnl"], color=colors, alpha=0.7)
        ax2.axhline(y=0, color="black", linestyle="-", alpha=0.3)
        ax2.set_title("Dagelijkse P&L ($)", fontsize=14)
        ax2.set_ylabel("P&L ($)", fontsize=12)
        ax2.grid(True, axis="y")

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(
            daily_stats["Date"],
            daily_stats["daily_drawdown"],
            0,
            where=(daily_stats["daily_drawdown"] < 0),
            color="red",
            alpha=0.3,
        )
        ax3.plot(daily_stats["Date"], daily_stats["daily_drawdown"], "r-", alpha=0.7)
        ax3.axhline(y=-5, color="orange", linestyle="--", label="-5% Daglimiet")
        ax3.set_title("Dagelijkse Drawdown (%)", fontsize=14)
        ax3.set_ylabel("Drawdown (%)", fontsize=12)
        ax3.set_ylim(max(-15, daily_stats["daily_drawdown"].min() * 1.2), 5)
        ax3.legend(loc="lower right", fontsize=10)
        ax3.grid(True)

        # 4. Cumulatieve drawdown vanaf piek
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(
            daily_stats["Date"],
            daily_stats["drawdown_from_peak"],
            0,
            color="purple",
            alpha=0.3,
        )
        ax4.plot(
            daily_stats["Date"], daily_stats["drawdown_from_peak"], "purple", alpha=0.7
        )
        ax4.axhline(y=-10, color="red", linestyle="--", label="-10% Max Drawdown")
        ax4.set_title("Maximale Drawdown vanaf Piek (%)", fontsize=14)
        ax4.set_ylabel("Drawdown (%)", fontsize=12)
        ax4.set_ylim(max(-12, daily_stats["drawdown_from_peak"].min() * 1.2), 2)
        ax4.legend(loc="lower right", fontsize=10)
        ax4.grid(True)

        # 5. Win/Loss Ratio
        trade_df = self.load_trade_data()[self.load_trade_data()["Type"] == "TRADE"]
        if not trade_df.empty:
            profits = trade_df[
                trade_df["Action"].isin(["SELL", "BUY"])
                & (trade_df["Price"].shift(-1) - trade_df["Price"] > 0)
            ]["Price"].count()
            losses = trade_df[
                trade_df["Action"].isin(["SELL", "BUY"])
                & (trade_df["Price"].shift(-1) - trade_df["Price"] < 0)
            ]["Price"].count()
            win_loss_ratio = profits / losses if losses > 0 else float("inf")
            ax5 = fig.add_subplot(gs[3, :])
            ax5.bar(["Wins", "Losses"], [profits, losses], color=["green", "red"])
            ax5.set_title("Win/Loss Ratio", fontsize=14)
            ax5.set_ylabel("Aantal Trades", fontsize=12)
            ax5.text(
                0.5,
                -0.1,
                f"Win/Loss Ratio: {win_loss_ratio:.2f}",
                transform=ax5.transAxes,
                ha="center",
            )
            ax5.grid(True, axis="y")

        # 6. Nalevingstabel
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
        if self.logger:
            self.logger.log_info(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
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
                if self.logger:
                    self.logger.log_info(
                        "Onvoldoende data voor rapportgeneratie", level="ERROR"
                    )
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)
            df = self.load_trade_data()
            trade_df = df[df["Type"] == "TRADE"].copy()

            # Instrumentanalyse
            symbol_stats = {}
            for symbol in trade_df["Symbol"].unique():
                symbol_df = trade_df[trade_df["Symbol"] == symbol]
                wins = len(
                    symbol_df[
                        symbol_df["Action"].isin(["SELL", "BUY"])
                        & (symbol_df["Price"].shift(-1) - symbol_df["Price"] > 0)
                    ]
                )
                losses = len(
                    symbol_df[
                        symbol_df["Action"].isin(["SELL", "BUY"])
                        & (symbol_df["Price"].shift(-1) - symbol_df["Price"] < 0)
                    ]
                )
                symbol_stats[symbol] = {
                    "total_trades": len(symbol_df),
                    "wins": wins,
                    "losses": losses,
                    "win_rate": (
                        (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
                    ),
                    "days_traded": symbol_df["Date"].nunique(),
                }

            # Rapportweergave
            report = "\n===== FTMO Handelsrapport =====\n"
            report += f"Periode: {df['Timestamp'].min().date() if not df.empty else 'N/A'} tot {df['Timestamp'].max().date() if not df.empty else 'N/A'}\n"
            report += f"Initiële balans: ${initial_balance:,.2f}\n"
            report += f"Eindebalans: ${compliance['details']['final_balance']:,.2f}\n"
            report += f"Totale P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)\n"
            report += (
                f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%\n"
            )
            report += f"Aantal handelsdagen: {compliance['details']['trading_days']}\n"
            report += "\nInstrumentanalyse:\n"
            for symbol, stats in symbol_stats.items():
                report += f"  {symbol}: {stats['total_trades']} trades ({stats['wins']} wins, {stats['losses']} losses, Win Rate: {stats['win_rate']:.2f}%) over {stats['days_traded']} dagen\n"
            report += f"\nFTMO Naleving: {'GESLAAGD' if compliance['compliant'] else 'GEFAALD'}\n"
            if not compliance["compliant"]:
                report += f"Reden: {compliance['reason']}\n"
            if compliance_path:
                report += f"\nNalevingsvisualisatie opgeslagen als: {os.path.basename(compliance_path)}\n"

            # Extra metrics
            total_trades = len(trade_df)
            avg_trade_size = trade_df["Volume"].mean() if not trade_df.empty else 0
            report += f"\nExtra Metrics:\n"
            report += f"  Totaal aantal trades: {total_trades}\n"
            report += f"  Gemiddelde trade grootte: {avg_trade_size:.2f} lots\n"

            print(report)

            if self.logger:
                self.logger.log_info(
                    f"FTMO Rapport gegenereerd - Compliant: {compliance['compliant']}"
                )
                if not compliance["compliant"]:
                    self.logger.log_info(
                        f"Reden voor niet-naleving: {compliance['reason']}"
                    )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(self.output_dir, f"ftmo_report_{timestamp}.txt")
            with open(report_path, "w") as f:
                f.write(report)

            return True
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij rapportgeneratie: {e}", level="ERROR")
            return False
