import pandas as pd
import numpy as np
import MetaTrader5 as mt5


class TurtleStrategy:
    """Implementatie van de Turtle Trading strategie"""

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de Turtle strategie

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5
        risk_manager : RiskManager
            Risicobeheer component
        logger : Logger
            Component voor logging
        config : dict
            Strategie configuratie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config

    def calculate_atr(self, df, period=20):
        """
        Bereken Average True Range (ATR)

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata (moet 'high', 'low', 'close' columns bevatten)
        period : int, optional
            ATR periode

        Returns:
        --------
        pandas.Series
            ATR waarden
        """
        high = df['high']
        low = df['low']
        close = df['close'].shift(1)

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)

        tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
        atr = tr.rolling(window=period).mean()

        return atr

    def process_symbol(self, symbol):
        """
        Verwerk een symbool volgens de Turtle strategie

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool
        """
        # Controleer of dagelijkse risico-limiet al is bereikt
        if not self.risk_manager.can_trade():
            self.logger.log_info(f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}")
            return

        # Haal historische data op
        timeframe = mt5.TIMEFRAME_D1  # Dagelijkse timeframe
        df = self.connector.get_historical_data(symbol, timeframe, 60)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return

        # Bereken indicatoren
        df['atr'] = self.calculate_atr(df)
        df['high_20'] = df['high'].rolling(window=20).max()
        df['low_10'] = df['low'].rolling(window=10).min()

        # Huidige prijs en waarden ophalen
        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return
        current_price = tick.ask
        last_high_20 = df['high_20'].iloc[
            -2]  # Gebruik vorige candle om te voorkomen dat je huidige onvoltooid candle gebruikt
        last_low_10 = df['low_10'].iloc[-2]
        current_atr = df['atr'].iloc[-1]

        # Voeg trendfilter toe (optioneel)
        if len(df) >= 50:  # Zorg dat we genoeg data hebben
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            trend_bullish = df['close'].iloc[-1] > df['ema_50'].iloc[-1]
        else:
            trend_bullish = True  # Default als we niet genoeg data hebben

        # Check entry signaal (System 1: 20-dagen breakout) met trendfilter
        if current_price > last_high_20 and current_atr > 0 and trend_bullish:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")

            # Bereken stop loss
            stop_loss = current_price - (2 * current_atr)

            # Bepaal positiegrootte
            risk_amount = self.config['mt5']['account_balance'] * self.config['mt5']['risk_per_trade']
            dollar_per_pip = risk_amount / (current_price - stop_loss)

            # Converteer naar lot grootte (vereenvoudigd)
            lot_size = round(dollar_per_pip / 10000, 2)  # Aanpassen voor het specifieke instrument
            lot_size = max(0.01, min(lot_size, 10.0))  # Begrens tussen 0.01 en 10.0 lots

            # Controleer risico limiet
            if not self.risk_manager.check_trade_risk(symbol, lot_size, current_price, stop_loss):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return

            # Plaats order
            ticket = self.connector.place_order(
                "BUY",
                symbol,
                lot_size,
                stop_loss,
                0,  # Geen take profit
                comment="Turtle System 1"
            )

            if ticket:
                self.logger.log_trade(
                    symbol=symbol,
                    action="BUY",
                    price=current_price,
                    volume=lot_size,
                    sl=stop_loss,
                    tp=0,
                    comment="Turtle System 1 Entry"
                )

        # Check exit signaal voor bestaande posities
        open_positions = self.connector.get_open_positions(symbol)
        if open_positions:
            for position in open_positions:
                # We sluiten long posities als prijs onder 10-dagen low komt
                if position.type == mt5.POSITION_TYPE_BUY and current_price < last_low_10:
                    self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")

                    # Sluit positie
                    close_result = self.connector.place_order(
                        "SELL",
                        symbol,
                        position.volume,
                        0,
                        0,
                        comment=f"Turtle Exit - ticket:{position.ticket}"
                    )

                    if close_result:
                        self.logger.log_trade(
                            symbol=symbol,
                            action="SELL",
                            price=current_price,
                            volume=position.volume,
                            sl=0,
                            tp=0,
                            comment="Turtle System 1 Exit"
                        )

    def get_open_positions(self):
        """
        Haal alle open posities op

        Returns:
        --------
        dict
            Dictionary met open posities per symbool
        """
        result = {}
        for symbol in self.config['mt5']['symbols']:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result