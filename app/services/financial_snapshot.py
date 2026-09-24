from __future__ import annotations

import asyncio
import hashlib
import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.domain.financial import (
    annualized_daily_volatility,
    distance_from_high,
    momentum_state,
    percentage_change,
    sample_daily_volatility,
)
from app.infrastructure.okx_market import OKXMarketClient


class FinancialSnapshotService:
    def __init__(self, market_client: OKXMarketClient) -> None:
        self.market_client = market_client

    async def execute(self, asset: str, horizon: str, freshness_required_seconds: int) -> dict:
        if horizon != "24h":
            raise ValueError("MVP currently supports only horizon=24h")

        ticker_task = self.market_client.get_ticker(asset)
        candle_task = self.market_client.get_daily_candles(asset, limit=30)
        raw_ticker, raw_candles = await asyncio.gather(ticker_task, candle_task)
        ticker = self.market_client.normalize_ticker(asset, raw_ticker)
        closes = self.market_client.confirmed_daily_closes(raw_candles)

        now = datetime.now(timezone.utc)
        source_time = datetime.fromtimestamp(ticker["timestamp_ms"] / 1000, tz=timezone.utc)
        freshness_seconds = max(0, int((now - source_time).total_seconds()))
        if freshness_seconds > freshness_required_seconds:
            raise RuntimeError(
                f"market data is {freshness_seconds}s old; required <= {freshness_required_seconds}s"
            )
        if len(closes) < 21:
            raise RuntimeError("At least 21 confirmed daily candles are required")

        result = self._build_response(ticker, closes, freshness_seconds, now)
        result["request_id"] = f"req_{uuid.uuid4().hex[:16]}"
        result["status"] = "VERIFIED"
        canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
        result["result_hash"] = hashlib.sha256(canonical).hexdigest()
        return result

    @staticmethod
    def _build_response(
        ticker: dict,
        closes: list[Decimal],
        freshness_seconds: int,
        generated_at: datetime,
    ) -> dict:
        price = ticker["price"]
        spread = ticker["ask"] - ticker["bid"]
        midpoint = (ticker["ask"] + ticker["bid"]) / Decimal("2")
        spread_bps = spread / midpoint * Decimal("10000") if midpoint else Decimal("0")
        return_24h = percentage_change(price, ticker["open_24h"])
        latest_close = closes[-1]
        return_5d = percentage_change(latest_close, closes[-6])
        return_20d = percentage_change(latest_close, closes[-21])
        daily_vol = sample_daily_volatility(closes[-21:])
        annualized_vol = annualized_daily_volatility(closes[-21:])
        recent_high = max(closes[-21:])

        return {
            "asset": ticker["asset"],
            "underlying": "AAPL",
            "instrument_id": ticker["instrument_id"],
            "horizon": "24h",
            "market": {
                "price": str(price),
                "bid": str(ticker["bid"]),
                "ask": str(ticker["ask"]),
                "spread": str(spread),
                "spread_bps": str(spread_bps),
                "open_24h": str(ticker["open_24h"]),
                "high_24h": str(ticker["high_24h"]),
                "low_24h": str(ticker["low_24h"]),
                "volume_24h": str(ticker["volume_24h"]),
                "return_24h": str(return_24h),
            },
            "analytics": {
                "return_5d": str(return_5d),
                "return_20d": str(return_20d),
                "realized_daily_volatility": str(daily_vol),
                "annualized_volatility": str(annualized_vol),
                "distance_from_20d_high": str(distance_from_high(latest_close, recent_high)),
                "momentum_state": momentum_state(return_5d, return_20d),
            },
            "evidence": {
                "market_source": "OKX Public Market API",
                "source_endpoint": "GET /api/v5/market/ticker?instId=XAAPL-USDT",
                "candle_source_endpoint": "GET /api/v5/market/candles?instId=XAAPL-USDT&bar=1Dutc&limit=30",
                "source_timestamp": datetime.fromtimestamp(
                    ticker["timestamp_ms"] / 1000, tz=timezone.utc
                ).isoformat(),
                "generated_at": generated_at.isoformat(),
                "freshness_seconds": freshness_seconds,
                "methodology_version": "1.0.0",
                "daily_bar_convention": "1Dutc, confirmed candles only",
                "volatility_convention": "365-day annualization",
            },
        }
