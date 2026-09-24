from __future__ import annotations

from x402 import x402ResourceServer
from x402.http import (
    OKXAuthConfig,
    OKXFacilitatorClient,
    OKXFacilitatorConfig,
    PaymentOption,
    RouteConfig,
)
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.mechanisms.evm.exact.server import ExactEvmScheme

from app.config import settings


def build_payment_components() -> tuple[dict, x402ResourceServer]:
    facilitator = OKXFacilitatorClient(
        OKXFacilitatorConfig(
            auth=OKXAuthConfig(
                api_key=settings.okx_api_key,
                secret_key=settings.okx_secret_key,
                passphrase=settings.okx_passphrase,
            ),
            base_url=settings.okx_base_url,
            sync_settle=True,
        )
    )
    server = x402ResourceServer(facilitator)
    server.register(settings.x402_network, ExactEvmScheme())
    routes = {
        "POST /v1/intelligence/financial-snapshot": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    price=f"${settings.service_price_usd}",
                    network=settings.x402_network,
                    pay_to=settings.pay_to_address,
                    max_timeout_seconds=300,
                )
            ],
            description=(
                "Fresh, structured and evidence-backed financial intelligence for autonomous agents."
            ),
            mime_type="application/json",
        )
    }
    return routes, server


def attach_payment_middleware(app) -> None:
    routes, server = build_payment_components()
    app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
