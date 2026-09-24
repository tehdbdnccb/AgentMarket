from __future__ import annotations

import asyncio
from collections.abc import Sequence
from decimal import Decimal
from typing import Any

import httpx

from app.config import settings

ASSET_TO_INSTRUMENT = {"xAAPL": "XAAPL-USDT"}
TICKER_PATH = "/api/v5/market/ticker"
CANDLES_PATH = "/api/v5/market/candles"


class MarketDataError(RuntimeError):
    pass


class OKXMarketClient:
    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        self.base_url = (base_url or settings.okx_market_base_url).rstrip("/")
        self.timeout = timeout or settings.market_timeout_seconds
        self.max_retries = settings.market_max_retries

    async def _get(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(f"{self.base_url}{path}", params=params)
                response.raise_for_status()
                payload = response.json()
                if payload.get("code") != "0":
                    raise MarketDataError(f"OKX market API error: code={payload.get('code')}")
                return payload
            except (httpx.HTTPError, ValueError, MarketDataError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(0.25 * (attempt + 1))
        raise MarketDataError("OKX market data request failed") from last_error

    async def get_ticker(self, asset: str) -> dict[str, Any]:
        instrument_id = ASSET_TO_INSTRUMENT.get(asset)
        if instrument_id is None:
            raise ValueError(f"Unsupported asset: {asset}")
        payload = await self._get(TICKER_PATH, {"instId": instrument_id})
        if not payload.get("data"):
            raise MarketDataError("OKX ticker response did not contain data")
        return payload["data"][0]

    async def get_daily_candles(self, asset: str, limit: int = 30) -> list[list[str]]:
        instrument_id = ASSET_TO_INSTRUMENT.get(asset)
        if instrument_id is None:
            raise ValueError(f"Unsupported asset: {asset}")
        payload = await self._get(
            CANDLES_PATH,
            {"instId": instrument_id, "bar": "1Dutc", "limit": str(min(limit, 300))},
        )
        return payload.get("data", [])

    @staticmethod
    def normalize_ticker(asset: str, ticker: dict[str, str]) -> dict[str, Any]:
        return {
            "asset": asset,
            "instrument_id": ticker["instId"],
            "price": Decimal(ticker["last"]),
            "bid": Decimal(ticker["bidPx"]),
            "ask": Decimal(ticker["askPx"]),
            "open_24h": Decimal(ticker["open24h"]),
            "high_24h": Decimal(ticker["high24h"]),
            "low_24h": Decimal(ticker["low24h"]),
            "volume_24h": Decimal(ticker["vol24h"]),
            "timestamp_ms": int(ticker["ts"]),
        }

    @staticmethod
    def confirmed_daily_closes(candles: Sequence[Sequence[str]]) -> list[Decimal]:
        confirmed = [Decimal(row[4]) for row in candles if len(row) >= 9 and row[8] == "1"]
        return list(reversed(confirmed))
