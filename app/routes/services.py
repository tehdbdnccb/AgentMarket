from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/v1", tags=["service"])


@router.get("/services")
async def services() -> dict:
    label = "X Layer Mainnet" if settings.x402_network == "eip155:196" else "X Layer Testnet"
    return {
        "services": [
            {
                "id": "financial_snapshot",
                "name": "AgentMarket Financial Snapshot",
                "description": "Fresh, structured financial intelligence for autonomous agents.",
                "method": "POST",
                "path": "/v1/intelligence/financial-snapshot",
                "price": f"${settings.service_price_usd}",
                "protocol": "x402",
                "network": settings.x402_network,
                "network_label": label,
                "asset": "xAAPL",
                "instrument_id": "XAAPL-USDT",
                "active": settings.payment_enabled,
            }
        ]
    }
