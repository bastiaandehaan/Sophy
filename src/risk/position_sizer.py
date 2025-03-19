# src/risk/advanced_position_sizer.py
from typing import Optional, Union, Dict, Any
import numpy as np
from decimal import Decimal


def adaptive_position_size(
    entry_price: float,
    stop_loss: float,
    account_balance: float,
    risk_percentage: float,
    volatility_factor: float,
    atr_value: Optional[float] = None,
    market_condition: str = "normal",
    max_portfolio_risk: float = 0.05,
    current_risk_exposure: float = 0.0
) -> float:
    """
    Berekent de optimale positiegrootte aangepast aan marktvolatiliteit.

    Args:
        entry_price: Ingangsprijs van de trade
        stop_loss: Stop-loss niveau
        account_balance: Huidige account balans
        risk_percentage: Basis risicopercentage per trade (0.01 = 1%)
        volatility_factor: Huidige marktvolatiliteit vergeleken met historisch gemiddelde
        atr_value: Average True Range waarde (optioneel)
        market_condition: Marktomstandigheden ('high_volatility', 'normal', 'low_volatility')
        max_portfolio_risk: Maximum portfolio risico op elk moment (0.05 = 5%)
        current_risk_exposure: Huidige risico exposure in percentage (0.02 = 2%)

    Returns:
        Berekende positiegrootte in lots
    """
    # Basis risicobedrag
    risk_amount = account_balance * risk_percentage

    # Aanpassing op basis van marktvolatiliteit
    if market_condition == "high_volatility":
        # Verlaag risico bij hoge volatiliteit
        adjusted_risk = risk_amount * (1 / volatility_factor)
    elif market_condition == "low_volatility":
        # Verhoog risico bij lage volatiliteit
        adjusted_risk = risk_amount * min(2.0, 1.0 / volatility_factor)
    else:
        # Normale marktomstandigheden
        adjusted_risk = risk_amount

    # Check portfolio risico limiet
    available_risk = max_portfolio_risk - current_risk_exposure
    if available_risk <= 0:
        return 0.0  # Geen nieuwe positie mogelijk vanwege portfolio risico limiet

    # Begrens adjusted risk op basis van beschikbaar risico
    adjusted_risk = min(adjusted_risk, account_balance * available_risk)

    # Bereken risico per pip/punt
    if entry_price == stop_loss:  # Voorkom deling door nul
        return 0.01  # Minimale positiegrootte

    risk_per_unit = abs(entry_price - stop_loss)

    # Voeg extra veiligheidsmarge toe als ATR beschikbaar is
    if atr_value and atr_value > risk_per_unit:
        # Als de ATR groter is dan de stop afstand, vergroot de risico buffer
        risk_per_unit = risk_per_unit * 0.8 + atr_value * 0.2

    # Bereken positiegrootte
    position_size = adjusted_risk / risk_per_unit

    # Rond af naar beneden naar dichtstbijzijnde 0.01 lot
    position_size = np.floor(position_size * 100) / 100

    # Begrens op minimaal 0.01 en maximaal 10.0 lot
    return max(0.01, min(position_size, 10.0))
