from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass
class PricingAgentConfig:
    """Configuration options that shape how recommendations are produced."""

    wholesale_discount: float = 0.45
    min_margin: float = 0.45
    max_premium: float = 0.25

    def __post_init__(self) -> None:
        if not 0 < self.wholesale_discount < 1:
            raise ValueError("wholesale_discount must be between 0 and 1")
        if not 0 < self.min_margin < 1:
            raise ValueError("min_margin must be between 0 and 1")
        if not 0 < self.max_premium < 1:
            raise ValueError("max_premium must be between 0 and 1")


@dataclass
class ProductProfile:
    """Represents the Nousen product we are pricing."""

    name: str
    unit_cost: float
    target_margin: float = 0.65
    differentiators: List[str] = field(default_factory=list)
    brand_position: str = "premium"  # value | mid | premium
    channel: str = "direct"  # direct | practitioner | retail

    def __post_init__(self) -> None:
        if self.unit_cost <= 0:
            raise ValueError("unit_cost must be positive")
        if not 0 < self.target_margin < 1:
            raise ValueError("target_margin must be between 0 and 1")
        self.brand_position = self.brand_position.lower()
        self.channel = self.channel.lower()


@dataclass
class CompetitorProduct:
    """Competitor snapshot used to anchor our pricing band."""

    name: str
    price: float
    brand_position: str = "mid"  # value | mid | premium
    strength_score: float = 0.5  # 0-1 subjective quality/innovation score
    differentiators: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("price must be positive")
        self.brand_position = self.brand_position.lower()
        self.strength_score = max(0.0, min(1.0, self.strength_score))


@dataclass
class PricingRecommendation:
    """Structured output summarising the pricing decision."""

    rrp: float
    wholesale_price: float
    expected_margin: float
    competitor_anchor: float
    differentiation_premium: float
    narrative: Sequence[str]
    rationale: Dict[str, float]
