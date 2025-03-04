# turtle_trader/risk/manager.py
from datetime import date, datetime
from typing import Dict, Optional, Tuple


class RiskManager:
    """Enhanced risk management with FTMO compliance checks"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        """Initialize with configuration parameters"""
        self.config = config
        self.logger = logger
        self.risk_config = config.get('risk', {})

        # Extract risk parameters
        self.max_risk_per_trade = self.risk_config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.risk_config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.risk_config.get('max_total_drawdown', 0.10)
        self.leverage = self.risk_config.get('leverage', 30)

        # Initialize tracking variables
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.risk_config.get('account_balance', 100000)
        self.position_registry = {}

    def check_ftmo_limits(self, account_info: Dict[str, float]) -> Tuple[bool, Optional[str]]:
        """
        Check if current account state complies with FTMO limits

        Args:
            account_info: Dictionary with current account information

        Returns:
            Tuple of (stop_trading, reason)
            - stop_trading: True if trading should be stopped
            - reason: Description of why trading should stop, or None
        """
        # Get current balance and equity
        current_balance = account_info.get('balance', self.initial_balance)
        current_equity = account_info.get('equity', current_balance)

        # Calculate drawdown from initial balance
        daily_pnl_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Check profit target (10% for FTMO)
        if daily_pnl_pct >= 0.10:  # 10% profit target
            return True, f"Profit target reached: {daily_pnl_pct:.2%}"

        # Check daily loss limit (5% for FTMO)
        if daily_pnl_pct <= -0.05:  # 5% daily loss limit
            return True, f"Daily loss limit reached: {daily_pnl_pct:.2%}"

        # Check maximum drawdown (10% for FTMO)
        if daily_pnl_pct <= -0.10:  # 10% maximum drawdown
            return True, f"Maximum drawdown reached: {daily_pnl_pct:.2%}"

        return False, None