from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.payment import attach_payment_middleware
from app.routes.health import router as health_router
from app.routes.intelligence import router as intelligence_router
from app.routes.market import router as market_router
from app.routes.services import router as services_router
from app.security import SecurityHeadersMiddleware, validate_pay_to_address


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.payment_enabled:
        validate_pay_to_address(settings.pay_to_address)
    yield


app = FastAPI(
    title="AgentMarket",
    version="1.0.0",
    description="Machine-purchasable financial intelligence for autonomous agents.",
    lifespan=lifespan,
)

if settings.configured_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.configured_hosts)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["PAYMENT-REQUIRED", "PAYMENT-RESPONSE", "X-AgentMarket-Request-ID"],
)

app.include_router(health_router)
app.include_router(services_router)
app.include_router(market_router)
app.include_router(intelligence_router)

if settings.payment_enabled:
    attach_payment_middleware(app)

app.mount("/", StaticFiles(directory="static", html=True), name="frontend")
