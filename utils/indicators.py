# turtle_trader/utils/indicators.py
import numpy as np
import pandas as pd
from typing import Union


def calculate_atr(df: pd.DataFrame, period: int = 20) -> np.ndarray:
    """
    Calculate Average True Range (ATR) using vectorized operations

    Args:
        df: DataFrame with OHLC data
        period: ATR calculation period

    Returns:
        NumPy array with ATR values
    """
    high = df['high'].values
    low = df['low'].values
    close = np.roll(df['close'].values, 1)
    close[0] = 0  # Avoid using the rolled value for first element

    # Calculate true range components
    tr1 = high - low
    tr2 = np.abs(high - close)
    tr3 = np.abs(low - close)

    # Calculate true range as the maximum of the components
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    # Calculate ATR using rolling mean
    atr = np.zeros_like(tr)
    for i in range(len(tr)):
        if i < period:
            atr[i] = np.mean(tr[0:i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = np.mean(tr[i - period + 1:i + 1])

    return atr


def calculate_donchian_channel(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Calculate Donchian Channel using vectorized operations

    Args:
        df: DataFrame with OHLC data
        period: Look-back period

    Returns:
        DataFrame with upper and lower channel values
    """
    # Implementation using sliding window operations
    # ...