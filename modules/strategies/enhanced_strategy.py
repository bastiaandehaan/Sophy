import pandas as pd
import numpy as np
import MetaTrader5 as mt5


class EnhancedTurtleStrategy:
    """Verbeterde implementatie van de Turtle Trading strategie"""

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
        # Dictionary om trailing stops bij te houden
        self.trailing_stops = {}

        # Configureerbare strategie parameters met standaardwaarden
        # In de toekomst kunnen deze naar config.json worden verplaatst
        self.entry_period = 20
        self.exit_period = 10
        self.atr_period = 20
        self.atr_multiplier = 2
        self.breakout_confirmation = 0.001  # 0.1% boven breakout niveau
        self.use_volume_filter = True
        self.volume_threshold = 1.1  # Volume moet 10% boven gemiddelde zijn
        self.use_trend_filter = True
        self.use_partial_exits = True
        self.use_trailing_stops = True

        # Laden van configuratie-opties indien aanwezig
        if 'strategy' in self.config:
            strat_config = self.config['strategy']
            self.entry_period = strat_config.get('entry_period', self.entry_period)
            self.exit_period = strat_config.get('exit_period', self.exit_period)
            self.atr_period = strat_config.get('atr_period', self.atr_period)
            self.atr_multiplier = strat_config.get('atr_multiplier', self.atr_multiplier)
            self.breakout_confirmation = strat_config.get('breakout_confirmation', self.breakout_confirmation)
            self.use_volume_filter = strat_config.get('use_volume_filter', self.use_volume_filter)
            self.volume_threshold = strat_config.get('volume_threshold', self.volume_threshold)
            self.use_trend_filter = strat_config.get('use_trend_filter', self.use_trend_filter)
            self.use_partial_exits = strat_config.get('use_partial_exits', self.use_partial_exits)
            self.use_trailing_stops = strat_config.get('use_trailing_stops', self.use_trailing_stops)

    def calculate_atr(self, df, period=None):
        """
        Bereken Average True Range (ATR)

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata (moet 'high', 'low', 'close' columns bevatten)
        period : int, optional
            ATR periode, standaard wordt self.atr_period gebruikt

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

    def calculate_indicators(self, df):
        """
        Bereken alle benodigde indicatoren voor de strategie

        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame met prijsdata

        Returns:
        --------
        pandas.DataFrame
            DataFrame met toegevoegde indicatoren
        """
        # Maak een kopie van de DataFrame
        df = df.copy()

        # Bereken ATR
        df['atr'] = self.calculate_atr(df)

        # Bereken Donchian channels
        df['high_entry'] = df['high'].rolling(window=self.entry_period).max()
        df['low_exit'] = df['low'].rolling(window=self.exit_period).min()

        # Bereken volume-indicatoren als volume filter actief is
        if self.use_volume_filter:
            df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()
            df['rel_volume'] = df['tick_volume'] / df['vol_avg_50']

        # Bereken trend-indicatoren als trend filter actief is
        if self.use_trend_filter:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            df['trend_bullish'] = df['close'] > df['ema_50']

            # Bereken trendsterkte (afstand tussen prijs en EMA als percentage)
            df['trend_strength'] = (df['close'] - df['ema_50']) / df['close']

        return df

    def process_symbol(self, symbol):
        """
        Verwerk een symbool volgens de verbeterde Turtle strategie

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
        timeframe = mt5.TIMEFRAME_H4  # Gewijzigd van D1 naar H4 voor responsiever reageren
        df = self.connector.get_historical_data(symbol, timeframe, 150)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return

        # Bereken indicatoren
        df = self.calculate_indicators(df)

        # Verwerk eerst exits (voor bestaande posities)
        self._manage_exits(symbol, df)

        # Verwerk vervolgens potentiële entries
        self._process_entries(symbol, df)

    def _process_entries(self, symbol, df):
        """
        Verwerk potentiële entry signalen

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        df : pandas.DataFrame
            DataFrame met prijsdata en indicatoren
        """
        # Haal huidige prijs en indicator-waarden op
        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return

        current_price = tick.ask
        last_high_entry = df['high_entry'].iloc[-2]  # Gebruik vorige candle om look-ahead bias te voorkomen
        current_atr = df['atr'].iloc[-1]

        # CHECK 1: Basis breakout check (VERPLICHT)
        # Voeg bevestiging toe: prijs moet minimaal X% boven breakout niveau zijn
        breakout_threshold = last_high_entry * (1 + self.breakout_confirmation)
        breakout_valid = current_price > breakout_threshold

        if not breakout_valid:
            return  # Geen geldige breakout, stop verdere verwerking

        # CHECK 2: Volume filter (OPTIONEEL)
        volume_valid = True
        if self.use_volume_filter:
            relative_volume = df['rel_volume'].iloc[-1]
            volume_valid = relative_volume > self.volume_threshold

        # CHECK 3: Trend filter (OPTIONEEL)
        trend_valid = True
        if self.use_trend_filter:
            trend_valid = df['trend_bullish'].iloc[-1]

        # Als alle actieve checks geldig zijn, genereer een entry signaal
        if breakout_valid and volume_valid and trend_valid and current_atr > 0:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")

            # Bereken stop loss
            stop_loss = current_price - (self.atr_multiplier * current_atr)

            # Bereken positiegrootte met eventuele aanpassingen op basis van trend
            position_size_multiplier = 1.0

            if self.use_trend_filter and 'trend_strength' in df.columns:
                trend_strength = df['trend_strength'].iloc[-1]
                # Bij sterke trend (>1%) verhoog positiegrootte tot 50% extra
                if trend_strength > 0.01:
                    position_size_multiplier = min(1.5, 1 + trend_strength * 10)

            # Bepaal positiegrootte
            risk_amount = self.config['mt5']['account_balance'] * self.config['mt5'][
                'risk_per_trade'] * position_size_multiplier
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
                0,  # Geen take profit, we gebruiken trailing exits
                comment="Enhanced Turtle System"
            )

            if ticket:
                # Sla initiële volume op voor gedeeltelijke winstneming
                self.position_initial_volumes[ticket] = lot_size

                # Log extra details over de trade beslissing
                entry_details = f"Trend: {df['trend_strength'].iloc[-1]:.2f}" if self.use_trend_filter else ""
                entry_details += f", Vol: {df['rel_volume'].iloc[-1]:.1f}" if self.use_volume_filter else ""

                self.logger.log_trade(
                    symbol=symbol,
                    action="BUY",
                    price=current_price,
                    volume=lot_size,
                    sl=stop_loss,
                    tp=0,
                    comment=f"Enhanced Entry ({entry_details})"
                )

    def _manage_exits(self, symbol, df):
        """
        Beheer exits voor bestaande posities

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        df : pandas.DataFrame
            DataFrame met prijsdata en indicatoren
        """
        # Haal bestaande posities op
        open_positions = self.connector.get_open_positions(symbol)
        if not open_positions:
            return

        # Huidige prijs en indicator-waarden
        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            return

        current_price = tick.bid  # Gebruik bid voor verkopen
        last_low_exit = df['low_exit'].iloc[-2]  # Vorige candle
        current_atr = df['atr'].iloc[-1]

        for position in open_positions:
            if position.type == mt5.POSITION_TYPE_BUY:
                entry_price = position.price_open
                position_profit_pct = (current_price - entry_price) / entry_price * 100

                # Haal originele positiegrootte op indien beschikbaar
                initial_volume = self.position_initial_volumes.get(position.ticket, position.volume)

                # VERBETERING 1: Gedeeltelijke winstneming
                if self.use_partial_exits:
                    # Eerste exit: Neem 40% winst bij 1x ATR
                    first_target = entry_price + current_atr
                    if position.volume > initial_volume * 0.6 and current_price > first_target:
                        exit_size = position.volume * 0.4
                        self.logger.log_info(f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}")

                        partial_result = self.connector.place_order(
                            "SELL",
                            symbol,
                            exit_size,
                            0,
                            0,
                            comment=f"Partial Exit (40%) - ticket:{position.ticket}"
                        )

                        if partial_result:
                            # Verplaats stop loss naar break-even
                            self._modify_stop_loss(symbol, position.ticket, entry_price)

                            self.logger.log_trade(
                                symbol=symbol,
                                action="SELL",
                                price=current_price,
                                volume=exit_size,
                                sl=entry_price,
                                tp=0,
                                comment="Partial Exit (40%)"
                            )

                    # Tweede exit: Neem nog eens 30% winst bij 2x ATR
                    second_target = entry_price + (current_atr * 2)
                    if position.volume > initial_volume * 0.3 and position.volume <= initial_volume * 0.6 and current_price > second_target:
                        exit_size = position.volume * 0.5  # 50% van wat over is = 30% van origineel
                        self.logger.log_info(f"Tweede gedeeltelijke winstneming (30%) voor {symbol} op {current_price}")

                        partial_result = self.connector.place_order(
                            "SELL",
                            symbol,
                            exit_size,
                            0,
                            0,
                            comment=f"Partial Exit (30%) - ticket:{position.ticket}"
                        )

                        if partial_result:
                            # Verplaats stop loss naar 50% van de winst
                            new_stop = entry_price + (current_price - entry_price) * 0.5
                            self._modify_stop_loss(symbol, position.ticket, new_stop)

                            self.logger.log_trade(
                                symbol=symbol,
                                action="SELL",
                                price=current_price,
                                volume=exit_size,
                                sl=new_stop,
                                tp=0,
                                comment="Partial Exit (30%)"
                            )

                # VERBETERING 2: Trailing stop
                if self.use_trailing_stops:
                    # Als we al een partiële exit hebben gedaan (stop loss >= entry_price)
                    if position.sl >= entry_price:
                        # Bereken potentiële nieuwe trailing stop
                        potential_stop = current_price - (current_atr * 1.5)

                        # Alleen verhogen als nieuwe stop hoger is dan huidige
                        if potential_stop > position.sl:
                            self._modify_stop_loss(symbol, position.ticket, potential_stop)

                # Originele Turtle exit: Prijs zakt onder low van exit_period
                if current_price < last_low_exit:
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

                        # Positie opruimen uit dictionaries
                        if position.ticket in self.position_initial_volumes:
                            del self.position_initial_volumes[position.ticket]

    def _modify_stop_loss(self, symbol, ticket, new_stop):
        """
        Wijzig de stop loss van een bestaande positie

        Parameters:
        -----------
        symbol : str
            Het handelssymbool
        ticket : int
            Ticket nummer van de positie
        new_stop : float
            Nieuwe stop loss prijs

        Returns:
        --------
        bool
            True indien succesvol, anders False
        """
        # Creëer request voor MT5
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "sl": new_stop,
            "position": ticket
        }

        # Stuur request naar MT5
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.log_info(f"Wijzigen stop loss mislukt: {result.retcode}, {result.comment}")
            return False

        self.logger.log_info(f"Stop loss succesvol gewijzigd - ticket: {ticket}, nieuwe SL: {new_stop}")
        return True

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

