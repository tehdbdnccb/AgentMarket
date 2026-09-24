from fastapi import APIRouter, HTTPException, Response

from app.config import settings
from app.infrastructure.okx_market import MarketDataError, OKXMarketClient
from app.schemas.intelligence import FinancialSnapshotRequest
from app.services.financial_snapshot import FinancialSnapshotService

router = APIRouter(prefix="/v1/intelligence", tags=["intelligence"])
service = FinancialSnapshotService(OKXMarketClient())


@router.post("/financial-snapshot")
async def financial_snapshot(request: FinancialSnapshotRequest, response: Response) -> dict:
    if not settings.payment_enabled:
        raise HTTPException(status_code=503, detail="x402 payment configuration is required")
    try:
        result = await service.execute(
            request.asset,
            request.horizon,
            request.freshness_required_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (RuntimeError, MarketDataError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    response.headers["X-AgentMarket-Request-ID"] = result["request_id"]
    return result
