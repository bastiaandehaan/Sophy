import pandas as pd
import MetaTrader5 as mt5


class TurtleStrategy:
    """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO Swing"""
    from src.strategy.base_strategy import BaseStrategy

    class TurtleStrategy(BaseStrategy):
        """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO Swing"""
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

        # Bepaal of we in swing modus opereren
        self.swing_mode = self.config['mt5'].get('swing_mode', False)

        # Parameters voor Swing modus
        if self.swing_mode:
            self.entry_period = 40  # Langere periode voor swing trading
            self.exit_period = 20  # Langere exit periode
            self.atr_period = 20
            self.atr_multiplier = 2.5  # Ruimere stop voor swing trading
            print("Strategie geïnitialiseerd in Swing modus met aangepaste parameters")
        else:
            self.entry_period = 20  # Standaard Turtle parameter
            self.exit_period = 10  # Standaard Turtle parameter
            self.atr_period = 20
            self.atr_multiplier = 2.0
            print("Strategie geïnitialiseerd in standaard modus")

    def calculate_atr(self, df, period=None):
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
        if period is None:
            period = self.atr_period

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
        en de hoek van de EMA

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata

        Returns:
        --------
        float
            Trendsterkte-indicator (schaal 0-1)
        """
        if 'ema_50' not in df.columns or len(df) < 10:
            return 0

        # Haal de meest recente waarden op
        latest_close = df['close'].iloc[-1]
        latest_ema = df['ema_50'].iloc[-1]

        # Bereken EMA-hoek (snelheid van verandering)
        ema_slope = (df['ema_50'].iloc[-1] - df['ema_50'].iloc[-10]) / df['ema_50'].iloc[-10]

        # Normaliseer de afstand met ATR
        latest_atr = df['atr'].iloc[-1] if 'atr' in df.columns and df['atr'].iloc[-1] > 0 else latest_close * 0.01
        distance = (latest_close - latest_ema) / latest_atr

        # Combineer afstand en hoek voor trendsterkte
        # Afstand is 70% van de score, hoek is 30%
        distance_score = min(1.0, max(0, distance / 3))
        slope_score = min(1.0, max(0, ema_slope * 20))  # Schaal hoek naar 0-1

        strength = (distance_score * 0.7) + (slope_score * 0.3)

        return min(1.0, strength)  # Begrens op maximum 1.0

    def calculate_market_volatility(self, df):
        """
        Bepaal of de markt zich in een hoge volatiliteitsperiode bevindt

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata

        Returns:
        --------
        bool
            True als volatiliteit hoog is, anders False
        """
        if 'atr' not in df.columns or len(df) < 20:
            return False

        # Bereken gemiddelde ATR over de laatste 20 periodes
        avg_atr_20 = df['atr'].rolling(window=20).mean().iloc[-1]

        # Vergelijk huidige ATR met gemiddelde
        current_atr = df['atr'].iloc[-1]

        # Als huidige ATR meer dan 30% boven gemiddelde is, beschouwen we het als hoge volatiliteit
        high_volatility = current_atr > (avg_atr_20 * 1.3)

        return high_volatility

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

        # Haal configuratie timeframe op en zet om naar MT5 constante
        timeframe_str = self.config['mt5'].get('timeframe', 'H4')
        timeframe = self.connector.get_timeframe_constant(timeframe_str)

        # Bepaal aantal bars op basis van timeframe (meer bars voor kortere timeframes)
        if timeframe == mt5.TIMEFRAME_H4:
            bars_needed = 150
        elif timeframe == mt5.TIMEFRAME_H1:
            bars_needed = 240
        else:
            bars_needed = 100

        # Haal historische data op
        df = self.connector.get_historical_data(symbol, timeframe, bars_needed)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return

        # Bereken indicatoren
        df['atr'] = self.calculate_atr(df)
        df['high_entry'] = df['high'].rolling(window=self.entry_period).max()
        df['low_exit'] = df['low'].rolling(window=self.exit_period).min()

        # Voeg volume-indicator toe
        df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ratio'] = df['tick_volume'] / df['vol_avg_50']

        # Voeg trendfilter en trendsterkte toe
        if len(df) >= 50:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean() if len(df) >= 200 else df['close']
            trend_bullish = df['close'].iloc[-1] > df['ema_50'].iloc[-1]
            strong_trend = df['ema_50'].iloc[-1] > df['ema_200'].iloc[-1] if len(df) >= 200 else True
            trend_strength = self.calculate_trend_strength(df)
        else:
            trend_bullish = True
            strong_trend = True
            trend_strength = 0

        # Bepaal volatiliteit
        high_volatility = self.calculate_market_volatility(df)

        # Haal huidige prijs en waarden op
        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return

        current_price = tick.ask
        last_high_entry = df['high_entry'].iloc[-2]  # Gebruik vorige candle
        last_low_exit = df['low_exit'].iloc[-2]
        current_atr = df['atr'].iloc[-1]

        # **Verbeterde entry-criteria voor FTMO Swing**
        # 1. Prijs moet boven breakout-niveau liggen
        # 2. Volume moet hoger zijn dan gemiddeld
        # 3. Trend moet bullish zijn
        # 4. Voor Swing: Extra bevestiging van sterke trend vereist

        price_breakout = current_price > last_high_entry * 1.001
        volume_filter = df['vol_ratio'].iloc[-1] > 1.1

        entry_conditions = (
                price_breakout and
                current_atr > 0 and
                trend_bullish and
                volume_filter
        )

        # Voeg extra voorwaarden toe voor Swing modus
        if self.swing_mode:
            # In Swing modus: alleen traden als er een sterke trend is en volatiliteit acceptabel
            entry_conditions = entry_conditions and strong_trend and not high_volatility

        if entry_conditions:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")

            # Bereken stop loss met variabele ATR multiplier
            # Bij swing trading gebruiken we een ruimere stop
            sl_multiplier = self.atr_multiplier
            if high_volatility:
                sl_multiplier += 0.5  # Ruimere stop bij hoge volatiliteit

            stop_loss = current_price - (sl_multiplier * current_atr)

            # Bereken positiegrootte op basis van risicomanagement
            account_info = self.connector.get_account_info()
            account_balance = account_info.get('balance', self.config['mt5']['account_balance'])

            lot_size = self.risk_manager.calculate_position_size(
                symbol=symbol,
                entry_price=current_price,
                stop_loss=stop_loss,
                account_balance=account_balance,
                trend_strength=trend_strength
            )

            # Controleer of positiegrootte voldoet aan risicolimieten
            if not self.risk_manager.check_trade_risk(symbol, lot_size, current_price, stop_loss):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return

            # Plaats order
            ticket = self.connector.place_order(
                "BUY",
                symbol,
                lot_size,
                stop_loss,
                0,  # Geen vaste take profit voor Turtle strategie
                comment=f"FTMO {'Swing' if self.swing_mode else 'Turtle'}"
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
                    comment=f"{'Swing' if self.swing_mode else 'Turtle'} Entry (TS:{trend_strength:.2f}, Leverage:1:{self.risk_manager.leverage})"
                )

        # Beheer bestaande posities (exit en gedeeltelijke winstneming)
        open_positions = self.connector.get_open_positions(symbol)
        if open_positions:
            for position in open_positions:
                position_age_days = (datetime.now() - pd.to_datetime(position.time, unit='s')).days

                if position.type == mt5.POSITION_TYPE_BUY:
                    entry_price = position.price_open
                    profit_atr = 1.5 if self.swing_mode else 1.0  # Hogere winstdoelen voor swing trading
                    profit_target_1 = entry_price + (profit_atr * current_atr)  # 1.5x ATR voor eerste winstneming
                    profit_target_2 = entry_price + (profit_atr * 2 * current_atr)  # 3x ATR voor tweede winstneming

                    # Controleer of positie lang genoeg open is voor Swing trading
                    min_hold_time = 1  # minimaal 1 dag voor normale trades
                    if self.swing_mode:
                        min_hold_time = 2  # minimaal 2 dagen voor swing trades

                    time_condition_met = position_age_days >= min_hold_time

                    # Gedeeltelijke winstneming bij eerste profit target (40%)
                    if (time_condition_met and
                            current_price > profit_target_1 and
                            position.ticket in self.position_initial_volumes):

                        initial_volume = self.position_initial_volumes[position.ticket]
                        partial_volume = round(initial_volume * 0.4, 2)  # Neem 40% winst

                        if position.volume >= partial_volume and partial_volume >= 0.01:
                            self.logger.log_info(f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}")

                            # Sluit deel van de positie
                            partial_result = self.connector.place_order(
                                "SELL",
                                symbol,
                                partial_volume,
                                0,
                                0,
                                comment=f"Partial Profit 40% - ticket:{position.ticket}"
                            )

                            if partial_result:
                                self.logger.log_trade(
                                    symbol=symbol,
                                    action="SELL",
                                    price=current_price,
                                    volume=partial_volume,
                                    sl=0,
                                    tp=0,
                                    comment="Partial Profit 40%"
                                )

                                # Verplaats stop loss naar break-even na eerste winstneming
                                remaining_volume = position.volume - partial_volume
                                if remaining_volume >= 0.01:
                                    self.connector.place_order(
                                        "SELL",
                                        symbol,
                                        remaining_volume,
                                        0,
                                        0,
                                        comment=f"Close and reopen at breakeven - ticket:{position.ticket}"
                                    )

                                    # Heropen positie met break-even stop loss
                                    new_ticket = self.connector.place_order(
                                        "BUY",
                                        symbol,
                                        remaining_volume,
                                        entry_price,  # Break-even stop loss
                                        0,
                                        comment=f"Reopen with breakeven SL - from:{position.ticket}"
                                    )

                                    if new_ticket:
                                        self.position_initial_volumes[new_ticket] = remaining_volume

                    # Gedeeltelijke winstneming bij tweede profit target (30%)
                    elif (time_condition_met and
                          current_price > profit_target_2 and
                          position.ticket in self.position_initial_volumes):

                        initial_volume = self.position_initial_volumes[position.ticket]
                        remaining_pct = 0.6  # Na eerste winstneming van 40% is 60% over
                        partial_volume = round(initial_volume * remaining_pct * 0.5,
                                               2)  # Neem helft van het resterende deel

                        if position.volume >= partial_volume and partial_volume >= 0.01:
                            self.logger.log_info(f"Gedeeltelijke winstneming (30%) voor {symbol} op {current_price}")

                            # Sluit deel van de positie
                            partial_result = self.connector.place_order(
                                "SELL",
                                symbol,
                                partial_volume,
                                0,
                                0,
                                comment=f"Partial Profit 30% - ticket:{position.ticket}"
                            )

                            if partial_result:
                                self.logger.log_trade(
                                    symbol=symbol,
                                    action="SELL",
                                    price=current_price,
                                    volume=partial_volume,
                                    sl=0,
                                    tp=0,
                                    comment="Partial Profit 30%"
                                )

                                # Verhoog stop loss naar 50% van de winst voor het resterende deel
                                remaining_volume = position.volume - partial_volume
                                if remaining_volume >= 0.01:
                                    new_sl = entry_price + ((current_price - entry_price) * 0.5)

                                    self.connector.place_order(
                                        "SELL",
                                        symbol,
                                        remaining_volume,
                                        0,
                                        0,
                                        comment=f"Close and reopen with trailing SL - ticket:{position.ticket}"
                                    )

                                    # Heropen positie met nieuwe stop loss
                                    new_ticket = self.connector.place_order(
                                        "BUY",
                                        symbol,
                                        remaining_volume,
                                        new_sl,
                                        0,
                                        comment=f"Reopen with trailing SL - from:{position.ticket}"
                                    )

                                    if new_ticket:
                                        self.position_initial_volumes[new_ticket] = remaining_volume

                    # Normale exit: prijs daalt onder de exit-periode low
                    elif current_price < last_low_exit:
                        self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")

                        # Sluit volledige positie
                        close_result = self.connector.place_order(
                            "SELL",
                            symbol,
                            position.volume,
                            0,
                            0,
                            comment=f"{'Swing' if self.swing_mode else 'Turtle'} Exit - ticket:{position.ticket}"
                        )

                        if close_result:
                            self.logger.log_trade(
                                symbol=symbol,
                                action="SELL",
                                price=current_price,
                                volume=position.volume,
                                sl=0,
                                tp=0,
                                comment=f"{'Swing' if self.swing_mode else 'Turtle'} System Exit"
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

    def check_daily_limit(self):
        """
        Controleer of de dagelijkse winstdoelen of verlieslimiet zijn bereikt

        Returns:
        --------
        tuple
            (stop_trading, reason)
            stop_trading: bool - True als het handelen gestopt moet worden
            reason: str - Reden voor het stoppen (indien van toepassing)
        """
        account_info = self.connector.get_account_info()

        # Haal de initiële balans op uit config
        initial_balance = self.config['mt5'].get('account_balance', 100000)

        # Bereken huidige winst/verlies
        current_balance = account_info.get('balance', initial_balance)
        daily_pnl_pct = (current_balance - initial_balance) / initial_balance

        # FTMO-regels: stop bij 10% winst of 5% dagelijks verlies
        profit_target = 0.10  # 10% winstdoel
        daily_loss_limit = -0.05  # 5% dagelijkse verlieslimiet

        if daily_pnl_pct >= profit_target:
            return True, f"Dagelijks winstdoel bereikt: {daily_pnl_pct:.2%}"

        if daily_pnl_pct <= daily_loss_limit:
            return True, f"Dagelijkse verlieslimiet bereikt: {daily_pnl_pct:.2%}"

        return False, None