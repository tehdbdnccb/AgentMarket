# AgentMarket

**Machine-purchasable financial intelligence for autonomous agents.**

AgentMarket is an OKX Dev Day 2026 **Build a Company** submission. It exposes one specialist capability through a deterministic API:

`POST /v1/intelligence/financial-snapshot`

An agent requests fresh intelligence for `xAAPL`, receives an x402 payment challenge, pays per call, settles through X Layer, and receives an evidence-backed JSON result.

## Core flow

```text
Agent → OKX.AI / A2MCP → AgentMarket → HTTP 402
                                      ↓
                              OKX Payment SDK
                                      ↓
                                   X Layer
                                      ↓
                             payment verified
                                      ↓
                              real OKX data
                                      ↓
                           deterministic analytics
                                      ↓
                              evidence + hash
```

## Real user case

A developer operates an autonomous portfolio/treasury agent. Before a workflow involving tokenized Apple exposure, the agent buys a fresh `xAAPL` snapshot rather than maintaining multiple market-data and analytics integrations.

The result includes live market state, 24h return, 5-day and 20-day returns from confirmed UTC daily candles, realized volatility, spread, momentum state, source timestamp, freshness, methodology version, request ID and result hash.

**No fake market numbers are seeded into the application.**

## Quick start

Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 4021
```

For local x402 testing, use the X Layer testnet:

```env
APP_ENV=development
X402_NETWORK=eip155:1952
SERVICE_PRICE_USD=0.01
PAY_TO_ADDRESS=0xYourTestnetReceivingAddress
```

Set your OKX facilitator credentials in `.env`:

```env
OKX_API_KEY=
OKX_SECRET_KEY=
OKX_PASSPHRASE=
```

Open `http://localhost:4021`.

## Live data preview

```bash
curl http://localhost:4021/v1/market/xAAPL
```

This endpoint is intentionally read-only and exists for the human control plane. It calls the OKX public Market API at runtime.

## x402 self-check

```bash
curl -i -X POST http://localhost:4021/v1/intelligence/financial-snapshot \
  -H 'content-type: application/json' \
  -d '{"asset":"xAAPL","horizon":"24h","freshness_required_seconds":60}'
```

With valid payment configuration and no payment header, the expected result is:

```text
HTTP 402 Payment Required
PAYMENT-REQUIRED: <base64 challenge>
```

After an agent pays and replays the request, the endpoint returns the JSON capability.

## Production

Use:

```env
APP_ENV=production
X402_NETWORK=eip155:196
PAY_TO_ADDRESS=0xYourDedicatedXLayerReceivingAddress
```

Deploy the included Dockerfile to Railway or another HTTPS-capable host. OKX's A2MCP guide requires a public HTTPS endpoint and a successful 402 self-check before ASP registration.

## Submission assets

See:

- `docs/ARCHITECTURE.md`
- `docs/DEMO.md`
- `docs/SUBMISSION.md`
- `docs/SOURCES.md`
- `docs/BUILD_CHECKLIST.md`

## Known limitations

The MVP supports one capability and one asset (`xAAPL`). Historical analytics use OKX UTC daily candles and are descriptive, not investment advice. Live production proof still requires real OKX credentials, a dedicated receiving wallet, public HTTPS, testnet/mainnet payment execution and A2MCP registration.
