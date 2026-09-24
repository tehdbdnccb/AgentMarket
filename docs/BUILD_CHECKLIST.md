# Final verification checklist

- [ ] `GET /health` = 200
- [ ] `GET /v1/services` returns the capability
- [ ] `GET /v1/market/xAAPL` returns live OKX data
- [ ] unpaid paid-endpoint call = HTTP 402
- [ ] `PAYMENT-REQUIRED` header present
- [ ] X Layer testnet wallet funded
- [ ] real x402 payment succeeds
- [ ] X Layer transaction is visible
- [ ] paid replay returns JSON
- [ ] source timestamp is visible
- [ ] result hash is visible
- [ ] public HTTPS endpoint works
- [ ] A2MCP listing registered
- [ ] 2–4 minute demo recorded
- [ ] no secrets committed
