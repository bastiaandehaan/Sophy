# sophy/utils/indicators.py
import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    Bereken Average True Range (ATR) met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        ATR berekening periode

    Returns:
    --------
    np.ndarray : Array met ATR waarden
    """
    high = df['high'].values
    low = df['low'].values
    close = np.roll(df['close'].values, 1)
    close[0] = 0

    # Bereken true range componenten
    tr1 = high - low
    tr2 = np.abs(high - close)
    tr3 = np.abs(low - close)

    # Bereken true range als maximum van componenten
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    # Bereken ATR met rollend gemiddelde
    atr = np.zeros_like(tr)
    for i in range(len(tr)):
        if i < period:
            atr[i] = np.mean(tr[0:i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = np.mean(tr[i - period + 1:i + 1])

    return atr


def calculate_donchian_channel(df: pd.DataFrame, period: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bereken Donchian Channel met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        Lookback periode

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray] : Upper en lower channel waarden
    """
    # Implementatie...