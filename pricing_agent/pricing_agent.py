from __future__ import annotations

from typing import Iterable, List

from .analysis import competitor_anchor, differentiation_score
from .models import (
    CompetitorProduct,
    PricingAgentConfig,
    PricingRecommendation,
    ProductProfile,
)


CHANNEL_DISCOUNTS: dict[str, float] = {
    "direct": 0.0,
    "practitioner": 0.05,
    "retail": 0.08,
}


class PricingAgent:
    """Calculates recommended pricing while keeping Nousen principles in view."""

    def __init__(self, config: PricingAgentConfig | None = None) -> None:
        self.config = config or PricingAgentConfig()

    def _channel_adjustment(self, channel: str) -> float:
        return CHANNEL_DISCOUNTS.get(channel, 0.0)

    def recommend(
        self, product: ProductProfile, competitors: Iterable[CompetitorProduct]
    ) -> PricingRecommendation:
        anchor_price = competitor_anchor(competitors)
        differentiation, contributions = differentiation_score(product.differentiators)

        floor_price = product.unit_cost / (1 - self.config.min_margin)
        target_rrp = product.unit_cost / (1 - product.target_margin)

        brand_adjustment = self._brand_adjustment(product.brand_position)
        channel_adjustment = self._channel_adjustment(product.channel)

        competitor_based_rrp = anchor_price * (
            1 + min(differentiation, self.config.max_premium) + brand_adjustment + channel_adjustment
        )

        recommended_rrp = max(floor_price, target_rrp, competitor_based_rrp)
        ceiling = anchor_price * (1 + self.config.max_premium + brand_adjustment + channel_adjustment + 0.08)
        recommended_rrp = min(recommended_rrp, ceiling)

        wholesale_price = recommended_rrp * (1 - self.config.wholesale_discount)
        expected_margin = (recommended_rrp - product.unit_cost) / recommended_rrp

        narrative = self._build_narrative(
            product,
            anchor_price,
            floor_price,
            target_rrp,
            differentiation,
            recommended_rrp,
            wholesale_price,
            expected_margin,
            contributions,
        )

        rationale = {
            "floor_price": round(floor_price, 2),
            "target_rrp": round(target_rrp, 2),
            "competitor_anchor": round(anchor_price, 2),
            "brand_adjustment": round(brand_adjustment, 3),
            "channel_adjustment": round(channel_adjustment, 3),
            "differentiation": round(differentiation, 3),
        }

        return PricingRecommendation(
            rrp=round(recommended_rrp, 2),
            wholesale_price=round(wholesale_price, 2),
            expected_margin=round(expected_margin, 3),
            competitor_anchor=round(anchor_price, 2),
            differentiation_premium=round(differentiation, 3),
            narrative=narrative,
            rationale=rationale,
        )

    def _brand_adjustment(self, position: str) -> float:
        if position == "value":
            return -0.03
        if position == "premium":
            return 0.05
        return 0.0

    def _build_narrative(
        self,
        product: ProductProfile,
        anchor_price: float,
        floor_price: float,
        target_rrp: float,
        differentiation: float,
        recommended_rrp: float,
        wholesale_price: float,
        expected_margin: float,
        contributions: dict[str, float],
    ) -> List[str]:
        narrative: List[str] = []

        narrative.append(
            f"Competitor anchor of £{anchor_price:0.2f} was derived from market benchmarks with strength weighting."
        )
        narrative.append(
            f"Floor price set at £{floor_price:0.2f} to protect a minimum {self.config.min_margin:.0%} margin."
        )
        narrative.append(
            f"Target RRP based on desired margin is £{target_rrp:0.2f}; recommended RRP is £{recommended_rrp:0.2f}."
        )

        if differentiation:
            differentiator_details = ", ".join(
                f"{name} (+{weight:.0%})" for name, weight in contributions.items()
            )
            narrative.append(
                "Differentiation premium applied for: "
                f"{differentiator_details} (capped at {self.config.max_premium:.0%})."
            )

        narrative.append(
            f"Wholesale guidance set to £{wholesale_price:0.2f} after {self.config.wholesale_discount:.0%} discount."
        )
        narrative.append(
            f"Expected blended margin at recommended RRP is {expected_margin:.0%}."
        )

        return narrative
