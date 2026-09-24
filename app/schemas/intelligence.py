from typing import Literal
from pydantic import BaseModel, Field


class FinancialSnapshotRequest(BaseModel):
    asset: Literal["xAAPL"] = Field(description="OKX Unified Tokenized Stock displayed as xAAPL.")
    horizon: Literal["24h"] = "24h"
    freshness_required_seconds: int = Field(default=60, ge=1, le=300)
