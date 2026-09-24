from fastapi import APIRouter, HTTPException

from app.domain.financial import percentage_change
from app.infrastructure.okx_market import MarketDataError, OKXMarketClient

router = APIRouter(prefix="/v1/market", tags=["market"])
client = OKXMarketClient()


@router.get("/xAAPL")
async def x_aapl_preview() -> dict:
    try:
        raw = await client.get_ticker("xAAPL")
        ticker = client.normalize_ticker("xAAPL", raw)
    except (ValueError, MarketDataError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "asset": "xAAPL",
        "instrument_id": ticker["instrument_id"],
        "price": str(ticker["price"]),
        "bid": str(ticker["bid"]),
        "ask": str(ticker["ask"]),
        "high_24h": str(ticker["high_24h"]),
        "low_24h": str(ticker["low_24h"]),
        "volume_24h": str(ticker["volume_24h"]),
        "return_24h": str(percentage_change(ticker["price"], ticker["open_24h"])),
        "timestamp_ms": ticker["timestamp_ms"],
        "source": "OKX Public Market API",
        "read_only_preview": True,
    }
