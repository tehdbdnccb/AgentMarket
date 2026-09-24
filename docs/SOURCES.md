# Sources used for the product

Checked against current official OKX sources on September 19, 2026.

## A2MCP
https://web3.okx.com/nb/onchainos/dev-docs/okxai/howtomcp

OKX documents A2MCP as a standardized service type. Stock quotes are an explicit example. Paid A2MCP uses x402: an unpaid call returns HTTP 402 with `PAYMENT-REQUIRED`; after payment the request is replayed to retrieve the result. OKX also requires a public HTTPS endpoint before ASP registration.

## x402 Python seller SDK
https://web3.okx.com/de/onchainos/dev-docs/payments/sdk-python

OKX documents package `okxweb3-app-x402`, `PaymentMiddlewareASGI`, `OKXFacilitatorClient`, `OKXAuthConfig`, `OKXFacilitatorConfig`, `PaymentOption`, `RouteConfig` and `ExactEvmScheme`. The SDK reference gives X Layer mainnet as CAIP-2 `eip155:196`.

## OKX payment integration
https://web3.okx.com/nb/onchainos/dev-docs/payments/service-seller-sdk

The seller quickstart documents use of the Payment SDK for HTTP 402 handling and on-chain verification, with a FastAPI example.

## OKX market API
https://www.okx.com/docs-v5/en/

The public Market API documents `GET /api/v5/market/ticker` for current price, best bid/ask and 24-hour trading volume, and `GET /api/v5/market/candles` for OHLCV bars, including `1Dutc` and confirmation state.

## xAAPL identifier
https://www.okx.com/en-ae/help/okx-to-update-the-ticker-display-format-for-unified-tokenized-stocks

OKX states that Unified Tokenized Stocks are displayed as `xAAPL`, while the API instrument ID remains `XAAPL-USDT`.

## Unified Tokenized Stocks / X Layer
https://www.okx.com/zh-hans/help/okx-to-list-unified-tokenized-stocks-for-spot-trading

OKX states that Unified Tokenized Stocks provide price exposure to an underlying stock and support xStocks deposits/withdrawals on Solana and X Layer, with 24/7 trading.

## Current xAAPL ecosystem activity
https://www.okx.com/help/category/announcements

OKX's announcement index shows a September 18, 2026 listing announcement for USDC trading pairs for tokenized stocks xAAPL and xAMZN.
