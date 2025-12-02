"""Compatibility facade for historical Bootstrap ARP API names.

This module maps legacy class names used in earlier prototypes to the
current pricing_agent package so older code or notebooks keep working.
"""

from pricing_agent import (
    CompetitorProduct,
    PricingAgent,
    PricingAgentConfig,
    PricingRecommendation,
    ProductProfile,
)

# Legacy naming aliases
Product = ProductProfile
PricingContext = PricingAgentConfig

__all__ = [
    "PricingAgent",
    "Product",
    "PricingContext",
    "CompetitorProduct",
    "PricingRecommendation",
]
