# src/utils/indicators.py
"""
Indicator module voor technische analyse functies.

Deze module biedt efficiënte en gevectoriseerde implementaties
van veelgebruikte technische indicatoren voor het Sophy trading systeem.
"""

from typing import Tuple, Dict, Any

import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    Bereken Average True Range (ATR) met gevectoriseerde operaties.

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
    high = df["high"].values
    low = df["low"].values
    close = np.roll(df["close"].values, 1)
    close[0] = df["open"].values[0]  # Gebruik open van eerste candle als prev close

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
            atr[i] = np.mean(tr[0: i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = (
                         atr[i - 1] * (period - 1) + tr[i]
                     ) / period  # Exponential smoothing

    return atr


def calculate_donchian_channel(
    df: pd.DataFrame, period: int = 20
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bereken Donchian Channel met gevectoriseerde operaties.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        Lookback periode

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray, np.ndarray] : Upper, middle en lower channel waarden
    """
    high = df["high"].values
    low = df["low"].values

    # Initialiseer arrays
    upper = np.zeros_like(high)
    lower = np.zeros_like(low)

    # Bereken rolling max en min
    for i in range(len(high)):
        if i < period:
            upper[i] = np.max(high[0: i + 1])
            lower[i] = np.min(low[0: i + 1])
        else:
            upper[i] = np.max(high[i - period + 1: i + 1])
            lower[i] = np.min(low[i - period + 1: i + 1])

    # Bereken middle channel
    middle = (upper + lower) / 2

    return upper, middle, lower


def calculate_sma(prices: np.ndarray, period: int) -> np.ndarray:
    """
    Bereken Simple Moving Average.

    Parameters:
    -----------
    prices : np.ndarray
        Array met prijzen
    period : int
        Moving average periode

    Returns:
    --------
    np.ndarray : Array met SMA waarden
    """
    if len(prices) < period:
        # Als er minder datapunten zijn dan de periode, vul met NaN
        result = np.full_like(prices, np.nan, dtype=float)
        if len(prices) > 0:
            result[-1] = np.mean(prices)
        return result

    # Maak empty array
    sma = np.zeros_like(prices, dtype=float)

    # Vul eerste (period-1) waarden met NaN
    sma[: period - 1] = np.nan

    # Bereken SMA voor de rest
    for i in range(period - 1, len(prices)):
        sma[i] = np.mean(prices[i - period + 1: i + 1])

    return sma


def calculate_ema(prices: np.ndarray, period: int, alpha: float = None) -> np.ndarray:
    """
    Bereken Exponential Moving Average.

    Parameters:
    -----------
    prices : np.ndarray
        Array met prijzen
    period : int
        Moving average periode
    alpha : float, optional
        Smoothing factor (default: 2/(period+1))

    Returns:
    --------
    np.ndarray : Array met EMA waarden
    """
    if alpha is None:
        alpha = 2 / (period + 1)

    # Maak resultaat array
    ema = np.zeros_like(prices, dtype=float)

    # Gebruik SMA voor de eerste waarde
    if len(prices) >= period:
        ema[period - 1] = np.mean(prices[:period])
    else:
        ema[0] = prices[0]

    # Vul eerste waarden met NaN
    ema[: period - 1] = np.nan

    # Bereken EMA voor de rest
    for i in range(period, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]

    return ema


def calculate_rsi(prices: np.ndarray, period: int = 14) -> np.ndarray:
    """
    Bereken Relative Strength Index.

    Parameters:
    -----------
    prices : np.ndarray
        Array met prijzen
    period : int
        RSI periode

    Returns:
    --------
    np.ndarray : Array met RSI waarden
    """
    # Bereken prijs veranderingen
    deltas = np.diff(prices)
    deltas = np.append(0, deltas)  # voeg 0 toe aan begin voor juiste lengte

    # Scheid positieve en negatieve veranderingen
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    # Initialiseer arrays
    avg_gain = np.zeros_like(prices)
    avg_loss = np.zeros_like(prices)
    rsi = np.zeros_like(prices)

    # Eerste periode gebruikt simple average
    if len(gain) >= period:
        avg_gain[period - 1] = np.mean(gain[:period])
        avg_loss[period - 1] = np.mean(loss[:period])

    # Bereken smoothed averages
    for i in range(period, len(prices)):
        avg_gain[i] = ((period - 1) * avg_gain[i - 1] + gain[i]) / period
        avg_loss[i] = ((period - 1) * avg_loss[i - 1] + loss[i]) / period

    # Bereken RS en RSI
    rs = np.zeros_like(prices)
    for i in range(period, len(prices)):
        if avg_loss[i] == 0:
            rs[i] = 100  # Vermijd deling door nul
        else:
            rs[i] = avg_gain[i] / avg_loss[i]
        rsi[i] = 100 - (100 / (1 + rs[i]))

    # Vul eerste waarden met NaN
    rsi[:period] = np.nan

    return rsi


def calculate_bollinger_bands(
    prices: np.ndarray, period: int = 20, num_std: float = 2.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bereken Bollinger Bands.

    Parameters:
    -----------
    prices : np.ndarray
        Array met prijzen
    period : int
        Moving average periode
    num_std : float
        Aantal standaarddeviaties voor upper/lower bands

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray, np.ndarray] : Upper, middle en lower band waarden
    """
    # Bereken middle band (SMA)
    middle = calculate_sma(prices, period)

    # Bereken standaarddeviatie
    stdev = np.zeros_like(prices)
    for i in range(period - 1, len(prices)):
        stdev[i] = np.std(prices[i - period + 1: i + 1])

    # Vul eerste waarden met NaN
    stdev[: period - 1] = np.nan

    # Bereken upper en lower bands
    upper = middle + (stdev * num_std)
    lower = middle - (stdev * num_std)

    return upper, middle, lower


def calculate_macd(
    prices: np.ndarray,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bereken Moving Average Convergence Divergence.

    Parameters:
    -----------
    prices : np.ndarray
        Array met prijzen
    fast_period : int
        Periode voor fast EMA
    slow_period : int
        Periode voor slow EMA
    signal_period : int
        Periode voor signal line EMA

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray, np.ndarray] : MACD line, signal line, en histogram
    """
    # Bereken fast en slow EMAs
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)

    # MACD Line = Fast EMA - Slow EMA
    macd_line = fast_ema - slow_ema

    # Signal Line = EMA van MACD Line
    signal_line = calculate_ema(macd_line, signal_period)

    # Histogram = MACD Line - Signal Line
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


def add_all_indicators(df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Voeg meerdere technische indicatoren toe aan een DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    params : Dict[str, Any], optional
        Parameters voor indicatoren

    Returns:
    --------
    pd.DataFrame : DataFrame met toegevoegde indicatoren
    """
    # Default parameters
    if params is None:
        params = {
            "atr_period": 14,
            "sma_periods": [20, 50, 200],
            "ema_periods": [9, 21],
            "donchian_period": 20,
            "rsi_period": 14,
            "bb_period": 20,
            "bb_std": 2.0,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
        }

    # Maak kopie van DataFrame
    result = df.copy()

    # Voeg ATR toe
    result["atr"] = calculate_atr(df, params["atr_period"])

    # Voeg SMAs toe
    for period in params["sma_periods"]:
        result[f"sma_{period}"] = calculate_sma(df["close"].values, period)

    # Voeg EMAs toe
    for period in params["ema_periods"]:
        result[f"ema_{period}"] = calculate_ema(df["close"].values, period)

    # Voeg Donchian Channel toe
    upper, middle, lower = calculate_donchian_channel(df, params["donchian_period"])
    result["donchian_upper"] = upper
    result["donchian_middle"] = middle
    result["donchian_lower"] = lower

    # Voeg RSI toe
    result["rsi"] = calculate_rsi(df["close"].values, params["rsi_period"])

    # Voeg Bollinger Bands toe
    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(
        df["close"].values, params["bb_period"], params["bb_std"]
    )
    result["bb_upper"] = bb_upper
    result["bb_middle"] = bb_middle
    result["bb_lower"] = bb_lower

    # Voeg MACD toe
    macd, macd_signal, macd_hist = calculate_macd(
        df["close"].values,
        params["macd_fast"],
        params["macd_slow"],
        params["macd_signal"],
    )
    result["macd"] = macd
    result["macd_signal"] = macd_signal
    result["macd_hist"] = macd_hist

    return result
