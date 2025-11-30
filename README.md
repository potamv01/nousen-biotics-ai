# nousen-biotics-ai
Core AI systems behind Nousen Biotics powering pricing, insights, competitive modelling and data-driven decisions for clean-label, high-absorption supplements.

# 🌿 Nousen Biotics — AI Systems

This repository contains the AI and data-driven components behind **[Nousen Biotics](https://nousenbiotics.com/)** — a clean-label, high-absorption supplement brand focused on science, transparency, and measurable wellbeing.

Our goal is to combine **advanced AI** with **nutritional science** to build smarter, ethical, evidence-informed supplement experiences.

---

## 🚀 What This Repo Includes

### **1. Pricing Intelligence Engine**
A modular pricing agent that:
- Calculates optimal RRP and wholesale pricing
- Analyses competitor products
- Scores differentiation using clean-label, liposomal, botanical, and gut-friendly strengths
- Provides human-readable justification for price decisions
- Ensures sustainable margin and responsible pricing

### **2. Competitive Matrix & Scoring Models**
Tools for:
- Mapping Nousen products against industry competitors
- Highlighting unique selling points
- Identifying gaps and pricing opportunities

### **3. Product Intelligence & Analytics**
Upcoming modules will introduce:
- Ingredient scoring
- Evidence-based formulation insights
- Consumer-reported outcome tracking
- AI-assisted product development

### **4. Agentic Workflows (Future)**
Planned integrations include:
- Multi-agent systems for R&D
- AI-powered customer insights
- Data-driven retail & practitioner channel tools

---

## 🧱 Repository Structure

- `pricing_agent/` — production-ready agent that blends competitor anchors, differentiation scores, and margin protection to output RRPs and wholesale guidance.
- `tests/` — unit tests covering the pricing agent behaviour and guardrails.

---

## 🧠 Pricing Agent

The pricing agent evaluates competitor benchmarks, Nousen differentiation, and margin guardrails to produce a recommended RRP, wholesale guidance, and human-readable narrative.

```python
from pricing_agent import (
    CompetitorProduct,
    PricingAgent,
    ProductProfile,
)

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
print(recommendation.rrp)             # recommended consumer price
print(recommendation.wholesale_price) # practitioner/retail guidance
print(recommendation.narrative)       # bullet-point justification
```

Key behaviours:
- **Margin protection:** never prices below the minimum sustainable margin.
- **Differentiation premium:** applies caps to prevent over-pricing while rewarding clean-label, liposomal, and clinically-dosed innovations.
- **Channel sensitivity:** optional adjustments for practitioner and retail channels.
- **Transparent narrative:** bullet points suitable for commercial and product teams.

---

## 🔬 Running Tests

Install dependencies (Python 3.10+ recommended) and run:

```bash
python -m pytest
```

---

## 📦 Deployment

You can install and run the pricing agent as a reusable Python package:

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the package in editable mode from the repository root:

   ```bash
   pip install -e .
   ```

3. Import and use the agent anywhere in your stack:

   ```python
   from pricing_agent import PricingAgent, ProductProfile, CompetitorProduct

   agent = PricingAgent()
   # ... construct product and competitor inputs, then call agent.recommend(...)
   ```

4. (Optional) Build a distributable wheel for deployment to an internal index or artifact store:

   ```bash
   pip install build
   python -m build
   ```

   The resulting wheel will appear in `dist/` and can be pushed to your chosen package repository.
