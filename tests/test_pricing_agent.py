from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pricing_agent import CompetitorProduct, PricingAgent, ProductProfile


def test_recommendation_balances_margin_and_market():
    agent = PricingAgent()
    product = ProductProfile(
        name="Liposomal Vitamin C",
        unit_cost=8.0,
        target_margin=0.65,
        differentiators=["liposomal", "clean-label", "gut-friendly"],
        brand_position="premium",
        channel="direct",
    )

    competitors = [
        CompetitorProduct(name="Market Mid", price=24.0, brand_position="mid", strength_score=0.55),
        CompetitorProduct(name="Premium Leader", price=29.0, brand_position="premium", strength_score=0.75),
        CompetitorProduct(name="Value Option", price=18.0, brand_position="value", strength_score=0.35),
    ]

    recommendation = agent.recommend(product, competitors)

    floor_price = product.unit_cost / (1 - agent.config.min_margin)
    assert recommendation.rrp >= round(floor_price, 2)
    assert recommendation.expected_margin >= agent.config.min_margin
    assert recommendation.wholesale_price < recommendation.rrp
    assert any("Differentiation premium" in bullet for bullet in recommendation.narrative)


def test_differentiation_caps_pricing():
    agent = PricingAgent()
    product = ProductProfile(
        name="Daily Multi",
        unit_cost=5.0,
        target_margin=0.6,
        differentiators=["clean-label", "clinical-dose", "sustained-release", "liposomal"],
        brand_position="mid",
        channel="retail",
    )
    competitors = [
        CompetitorProduct(name="Retail Mid", price=22.0, brand_position="mid", strength_score=0.45),
    ]

    recommendation = agent.recommend(product, competitors)

    assert recommendation.rrp <= recommendation.competitor_anchor * 1.5
    assert 0 < recommendation.differentiation_premium <= agent.config.max_premium


def test_bootstrap_arp_compatibility_layer():
    # Legacy notebooks referenced bootstrap_arp; keep that import path working.
    from bootstrap_arp import PricingAgent as LegacyAgent, PricingContext as LegacyContext, Product as LegacyProduct

    agent = LegacyAgent()
    assert isinstance(agent, PricingAgent)

    product = LegacyProduct(name="Legacy Product", unit_cost=4.0, target_margin=0.6)
    assert isinstance(product, ProductProfile)

    context = LegacyContext(min_margin=0.5)
    assert isinstance(context, agent.config.__class__)
