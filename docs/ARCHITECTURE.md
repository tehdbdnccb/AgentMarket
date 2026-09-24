# Architecture

```text
OKX.AI / A2MCP
      │
      ▼
FastAPI AgentMarket API
      │
      ├── x402 middleware
      │       ├── 402 challenge
      │       ├── verify
      │       └── settle
      │
      └── Financial Snapshot service
              ├── OKX ticker
              ├── OKX 1Dutc candles
              ├── deterministic calculations
              ├── evidence metadata
              └── SHA-256 result hash
```

The dashboard is a control plane. The paid API is the product.

There is intentionally no custom payment contract and no LLM-generated market numbers.
