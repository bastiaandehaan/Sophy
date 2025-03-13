def calculate_position_size(
    entry_price: float,
    stop_loss: float,
    account_balance: float,
    risk_percentage: float,
    pip_value: float,
    min_lot: float = 0.01,
    max_lot: float = 10.0,
) -> float:
    """
    Calculate optimal position size based on risk parameters

    Args:
        entry_price: Entry price for the position
        stop_loss: Stop loss price
        account_balance: Current account balance
        risk_percentage: Percentage of account to risk (0.01 = 1%)
        pip_value: Value of one pip in account currency
        min_lot: Minimum allowable lot size
        max_lot: Maximum allowable lot size

    Returns:
        Calculated position size in lots
    """
    if entry_price == stop_loss:
        return min_lot  # Avoid division by zero

    # Calculate risk amount in account currency
    risk_amount = account_balance * risk_percentage

    # Calculate pips at risk
    pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # For 4-digit forex pairs

    # Calculate lot size
    lot_size = risk_amount / (pips_at_risk * pip_value)

    # Enforce limits
    lot_size = max(min_lot, min(lot_size, max_lot))

    # Round to 2 decimal places
    lot_size = round(lot_size, 2)

    return lot_size
