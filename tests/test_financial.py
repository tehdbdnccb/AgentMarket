from decimal import Decimal
import pytest
from app.domain.financial import annualized_daily_volatility, distance_from_high, momentum_state, percentage_change


def test_percentage_change():
    assert percentage_change(Decimal("105"), Decimal("100")) == Decimal("0.05")


def test_percentage_change_rejects_zero():
    with pytest.raises(ValueError):
        percentage_change(Decimal("100"), Decimal("0"))


def test_distance_from_high():
    assert distance_from_high(Decimal("90"), Decimal("100")) == Decimal("0.1")


def test_annualized_volatility_positive():
    closes = [Decimal("100"), Decimal("101"), Decimal("99"), Decimal("100")]
    assert annualized_daily_volatility(closes) > Decimal("0")


@pytest.mark.parametrize(("r5", "r20", "expected"), [("0.1", "0.2", "positive"), ("-0.1", "-0.2", "negative"), ("0.1", "-0.2", "mixed")])
def test_momentum(r5, r20, expected):
    assert momentum_state(Decimal(r5), Decimal(r20)) == expected
