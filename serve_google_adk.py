"""FastAPI entrypoint for exposing the pricing agent to Google ADK/Agent Builder.

This app mirrors the Cloud Run webhook shape described in docs/google_adk.md
so ADK tools can POST pricing scenarios to the `/price` route.
"""
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pricing_agent import CompetitorProduct, PricingAgent, ProductProfile

app = FastAPI(title="Nousen Pricing Agent")
agent = PricingAgent()


class CompetitorPayload(BaseModel):
    name: str
    price: float
    brand_position: str = Field(description="value|mid|premium")
    strength_score: float = Field(ge=0.0, le=1.0)


class ProductPayload(BaseModel):
    name: str
    unit_cost: float
    target_margin: float = Field(ge=0.0, le=1.0)
    differentiators: List[str]
    brand_position: str
    channel: str


class PriceRequest(BaseModel):
    product: ProductPayload
    competitors: List[CompetitorPayload]


@app.post("/price")
async def price(req: PriceRequest):
    """Return price recommendations for an ADK tool invocation."""
    try:
        product = ProductProfile(**req.product.dict())
        competitors = [CompetitorProduct(**c.dict()) for c in req.competitors]
        recommendation = agent.recommend(product, competitors)
        return recommendation.__dict__
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))


def get_app() -> FastAPI:
    """Expose the ASGI app for Cloud Run and local runners."""
    return app
