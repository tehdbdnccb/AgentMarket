from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    okx_api_key: str = ""
    okx_secret_key: str = ""
    okx_passphrase: str = ""
    okx_base_url: str = "https://web3.okx.com"
    x402_network: str = "eip155:1952"
    pay_to_address: str = ""
    service_price_usd: str = "0.01"
    okx_market_base_url: str = "https://www.okx.com"
    market_timeout_seconds: float = 10.0
    market_max_retries: int = 2
    default_freshness_seconds: int = 60
    allowed_hosts: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("x402_network")
    @classmethod
    def validate_network(cls, value: str) -> str:
        if value not in {"eip155:196", "eip155:1952"}:
            raise ValueError("X402_NETWORK must be eip155:196 or eip155:1952")
        return value

    @property
    def payment_enabled(self) -> bool:
        return all((self.okx_api_key, self.okx_secret_key, self.okx_passphrase, self.pay_to_address))

    @property
    def configured_hosts(self) -> list[str]:
        return [v.strip() for v in self.allowed_hosts.split(",") if v.strip()]


settings = Settings()
