from decimal import Decimal
from app.infrastructure.okx_market import OKXMarketClient


def test_normalize_ticker():
    ticker = {"instId":"XAAPL-USDT","last":"335.02","bidPx":"335.00","askPx":"335.05","open24h":"337.00","high24h":"338.00","low24h":"334.00","vol24h":"1234.5","ts":"1770000000000"}
    result = OKXMarketClient.normalize_ticker("xAAPL", ticker)
    assert result["instrument_id"] == "XAAPL-USDT"
    assert result["price"] == Decimal("335.02")


def test_confirmed_candles_are_reversed():
    candles = [["3","0","0","0","103","0","0","0","1"],["2","0","0","0","102","0","0","0","0"],["1","0","0","0","101","0","0","0","1"]]
    assert OKXMarketClient.confirmed_daily_closes(candles) == [Decimal("101"), Decimal("103")]
