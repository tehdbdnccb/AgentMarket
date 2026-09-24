from __future__ import annotations

from decimal import Decimal
from math import sqrt
from statistics import stdev


def percentage_change(current: Decimal, previous: Decimal) -> Decimal:
    if previous == 0:
        raise ValueError("previous price must not be zero")
    return (current - previous) / previous


def sample_daily_volatility(closes: list[Decimal]) -> Decimal:
    if len(closes) < 2:
        raise ValueError("at least two closes are required")
    returns = [percentage_change(closes[i], closes[i - 1]) for i in range(1, len(closes))]
    return Decimal(str(stdev(float(value) for value in returns)))


def annualized_daily_volatility(closes: list[Decimal]) -> Decimal:
    return sample_daily_volatility(closes) * Decimal(str(sqrt(365)))


def distance_from_high(current: Decimal, high: Decimal) -> Decimal:
    if high == 0:
        raise ValueError("high must not be zero")
    return (high - current) / high


def momentum_state(return_5d: Decimal, return_20d: Decimal) -> str:
    if return_5d > 0 and return_20d > 0:
        return "positive"
    if return_5d < 0 and return_20d < 0:
        return "negative"
    return "mixed"
