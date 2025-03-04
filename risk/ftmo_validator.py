# turtle_trader/risk/ftmo_validator.py
from typing import Dict, Tuple, Optional
from datetime import datetime, date, timedelta


class FTMOValidator:
    """Ensures trading activity complies with FTMO rules"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        self.config = config
        self.logger = logger
        self.initial_balance = config['risk'].get('account_balance', 100000)
        self.start_date = date.today()
        self.trade_days = set()

    def validate_account_state(self, account_info: Dict[str, float]) -> Tuple[bool, Optional[str]]:
        """
        Perform comprehensive FTMO rule validation

        Args:
            account_info: Current account information

        Returns:
            Tuple of (is_compliant, violation_reason)
        """
        # Get current metrics
        current_equity = account_info.get('equity', self.initial_balance)

        # Calculate metrics
        profit_loss_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Register trading day
        self.trade_days.add(date.today())

        # Check profit target (10%)
        if profit_loss_pct >= 0.10:
            return True, "Profit target achieved"

        # Check daily loss limit (5%)
        if profit_loss_pct <= -0.05:
            return False, "Daily loss limit exceeded"

        # Check max drawdown (10%)
        if profit_loss_pct <= -0.10:
            return False, "Maximum allowed drawdown exceeded"

        # Check minimum trading days (if near end of challenge)
        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= 28:  # Near end of challenge
            if len(self.trade_days) < 10:  # FTMO requires minimum 10 trading days
                self.logger.warning(f"Only {len(self.trade_days)} trading days registered, FTMO requires 10 minimum")

        return True, None