from src.risk.position_sizer import calculate_position_size


class TestPositionSizer:
    def test_normal_market_conditions(self):
        """Test positiegrootte onder normale marktcondities."""
        # 50 pips stop loss op een forex pair
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1950,  # 50 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0
        )
        # Verwacht ~1.0 lot (100000 * 0.01 / (50 * 10))
        assert 0.9 <= result <= 1.1

    def test_high_volatility_conditions(self):
        """Test positiegrootte bij hoge volatiliteit (wijdere stop loss)."""
        # 100 pips stop loss op een forex pair
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1900,  # 100 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0
        )
        # Verwacht ~0.5 lot (100000 * 0.01 / (100 * 10))
        assert 0.4 <= result <= 0.6

    def test_gold_instrument(self):
        """Test positiegrootte voor XAUUSD."""
        # Goud heeft andere pip waarde berekening
        result = calculate_position_size(
            entry_price=1800.00,
            stop_loss=1790.00,  # $10 verschil
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Verifieer correcte positiegrootte voor goud
        assert 0.08 <= result <= 0.12

    def test_minimum_lot_size(self):
        """Test minimale lotgrootte restrictie."""
        # Zeer wijde stop loss die zou leiden tot kleine positiegrootte
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1500,  # 500 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Moet minimaal 0.01 lot zijn, ongeacht berekening
        assert result == 0.01

    def test_maximum_lot_size(self):
        """Test maximale lotgrootte restrictie."""
        # Zeer nauwe stop loss of hoog risicopercentage
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1990,  # 10 pips SL
            account_balance=100000,
            risk_percentage=0.05,  # 5% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Moet maximaal 10.0 lot zijn, ongeacht berekening
        assert result == 10.0

    def test_zero_stop_loss(self):
        """Test het geval waar stop loss gelijk is aan entry (zou deling door nul veroorzaken)."""
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.2000,  # Identiek aan entry
            account_balance=100000,
            risk_percentage=0.01,
            pip_value=10.0
        )
        # Moet minimale lotgrootte teruggeven om deling door nul te voorkomen
        assert result == 0.01