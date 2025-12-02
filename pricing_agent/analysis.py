from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Tuple, Dict

from .models import CompetitorProduct


BRAND_POSITION_WEIGHTS: dict[str, float] = {
    "value": 0.85,
    "mid": 1.0,
    "premium": 1.1,
}

DIFFERENTIATOR_WEIGHTS: dict[str, float] = {
    "clean-label": 0.05,
    "clean label": 0.05,
    "liposomal": 0.07,
    "botanical": 0.03,
    "gut-friendly": 0.04,
    "gut friendly": 0.04,
    "clinical-dose": 0.06,
    "clinical dose": 0.06,
    "sustained-release": 0.05,
    "sustained release": 0.05,
}


def _position_weight(position: str) -> float:
    """Get the weight for a given brand position."""
    return BRAND_POSITION_WEIGHTS.get(position.lower(), BRAND_POSITION_WEIGHTS["mid"])


def competitor_anchor(competitors: Iterable[CompetitorProduct]) -> float:
    """Calculate a weighted anchor price from competitor products."""
    
    weighted_sum = 0.0
    weight_total = 0.0

    for competitor in competitors:
        weight = _position_weight(competitor.brand_position) + competitor.strength_score
        weighted_sum += competitor.price * weight
        weight_total += weight

    if weight_total == 0:
        raise ValueError("No competitor data available to compute anchor price")

    return weighted_sum / weight_total


def differentiation_score(differentiators: Iterable[str]) -> Tuple[float, dict[str, float]]:
    """Score differentiators and return (score, contribution breakdown)."""
    
    contributions: dict[str, float] = defaultdict(float)
    
    for differentiator in differentiators:
        key = differentiator.lower()
        if key in DIFFERENTIATOR_WEIGHTS:
            contributions[key] += DIFFERENTIATOR_WEIGHTS[key]

    score = sum(contributions.values())
    return min(score, 0.35), dict(contributions)
