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
        # Dictionary om initiële volumes bij te houden voor gedeeltelijke winstneming
        self.position_initial_volumes = {}

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

    def calculate_trend_strength(self, df):
        """
        Bereken trendsterkte gebaseerd op de afstand van de prijs tot de EMA-50

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata

        Returns:
        --------
        float
            Trendsterkte-indicator (schaal 0-1)
        """
        if 'ema_50' not in df.columns or len(df) < 2:
            return 0

        # Haal de meest recente waarden op
        latest_close = df['close'].iloc[-1]
        latest_ema = df['ema_50'].iloc[-1]

        # Normaliseer de afstand met ATR
        latest_atr = df['atr'].iloc[-1] if 'atr' in df.columns and df['atr'].iloc[-1] > 0 else latest_close * 0.01
        distance = (latest_close - latest_ema) / latest_atr

        # Converteer naar een 0-1 schaal
        strength = min(1.0, max(0, distance / 3))
        return strength

    def process_symbol(self, symbol):
        """
        Verwerk een symbool volgens de verbeterde Turtle strategie

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool
        """
        # Controleer of de dagelijkse risicolimiet is bereikt
        if not self.risk_manager.can_trade():
            self.logger.log_info(f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}")
            return

        # Haal historische data op voor H4 timeframe
        timeframe = mt5.TIMEFRAME_H4  # Gewijzigd van D1 naar H4
        df = self.connector.get_historical_data(symbol, timeframe, 150)  # Meer bars nodig voor H4
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return

        # Bereken indicatoren
        df['atr'] = self.calculate_atr(df)
        df['high_20'] = df['high'].rolling(window=20).max()
        df['low_10'] = df['low'].rolling(window=10).min()

        # Voeg volume-indicator toe
        df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()

        # Voeg trendfilter en trendsterkte toe
        if len(df) >= 50:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            trend_bullish = df['close'].iloc[-1] > df['ema_50'].iloc[-1]
            trend_strength = self.calculate_trend_strength(df)
        else:
            trend_bullish = True
            trend_strength = 0

        # Haal huidige prijs en waarden op
        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return
        current_price = tick.ask
        last_high_20 = df['high_20'].iloc[-2]
        last_low_10 = df['low_10'].iloc[-2]
        current_atr = df['atr'].iloc[-1]

        # **Verbetering 1: Strengere entry-criteria**
        # Controleer of de prijs minstens 0.5% boven het breakout-niveau ligt
        breakout_threshold = last_high_20 * 1.005
        # Controleer of het volume boven het gemiddelde ligt
        volume_filter = df['tick_volume'].iloc[-1] > df['vol_avg_50'].iloc[-1]

        # Verbeterd entry-signaal met strengere filters
        if (current_price > breakout_threshold and
                current_atr > 0 and
                trend_bullish and
                volume_filter):
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")

            # Bereken stop loss
            stop_loss = current_price - (2 * current_atr)

            # **Verbetering 2: Dynamische positiegrootte gebaseerd op trendsterkte**
            # Pas het risico aan op basis van trendsterkte (tot 50% extra)
            adjusted_risk = self.config['mt5']['risk_per_trade'] * (1 + trend_strength * 0.5)
            risk_amount = self.config['mt5']['account_balance'] * adjusted_risk
            dollar_per_pip = risk_amount / (current_price - stop_loss)
            lot_size = round(dollar_per_pip / 10000, 2)
            lot_size = max(0.01, min(lot_size, 10.0))

            # Controleer risicolimiet
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
                comment="Enhanced Turtle System"
            )

            if ticket:
                # Sla initiële volume op voor gedeeltelijke winstneming
                self.position_initial_volumes[ticket] = lot_size
                self.logger.log_trade(
                    symbol=symbol,
                    action="BUY",
                    price=current_price,
                    volume=lot_size,
                    sl=stop_loss,
                    tp=0,
                    comment=f"Turtle Entry (Strength: {trend_strength:.2f})"
                )

        # Controleer bestaande posities voor exit of gedeeltelijke exit
        open_positions = self.connector.get_open_positions(symbol)
        if open_positions:
            for position in open_positions:
                if position.type == mt5.POSITION_TYPE_BUY:
                    entry_price = position.price_open
                    profit_target = entry_price + current_atr

                    # **Verbetering 3: Gedeeltelijke winstneming**
                    # Controleer of de prijs het winstmarget (1 ATR) heeft bereikt
                    if (current_price > profit_target and
                            position.ticket in self.position_initial_volumes):
                        initial_volume = self.position_initial_volumes[position.ticket]
                        if position.volume > initial_volume * 0.5:
                            half_volume = position.volume / 2
                            self.logger.log_info(f"Gedeeltelijke winstneming voor {symbol} op {current_price}")

                            # Sluit helft van de positie
                            partial_result = self.connector.place_order(
                                "SELL",
                                symbol,
                                half_volume,
                                0,
                                0,
                                comment=f"Partial Profit - ticket:{position.ticket}"
                            )
                            if partial_result:
                                self.logger.log_trade(
                                    symbol=symbol,
                                    action="SELL",
                                    price=current_price,
                                    volume=half_volume,
                                    sl=0,
                                    tp=0,
                                    comment="Partial Profit Taking"
                                )
                                # Optioneel: verplaats stop loss naar break-even (niet geïmplementeerd)

                    # Normale exit: prijs daalt onder de 10-daagse low
                    elif current_price < last_low_10:
                        self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")
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
                                comment="Turtle System Exit"
                            )
                            # Verwijder positie uit dictionary als volledig gesloten
                            if position.ticket in self.position_initial_volumes:
                                del self.position_initial_volumes[position.ticket]

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