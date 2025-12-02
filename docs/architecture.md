# Architecture Overview

This repository delivers a modular pricing intelligence engine with lightweight integration surfaces for deployment and UI workflows.

## Core modules
- `pricing_agent/models.py` — data classes for configuration (`PricingAgentConfig`), inputs (`ProductProfile`, `CompetitorProduct`), and structured outputs (`PricingRecommendation`).
- `pricing_agent/analysis.py` — stateless helpers that derive weighted competitor anchors and differentiation scores from product signals.
- `pricing_agent/pricing_agent.py` — orchestrates analysis, applies brand/channel adjustments, enforces margin and premium caps, and assembles narratives plus rationale metadata.
- `pricing_agent/__init__.py` — exports the public API and keeps the legacy `bootstrap_arp` import path aligned.

## Execution flow
1. **Inputs** — caller provides a `ProductProfile`, a list of `CompetitorProduct` entries, and optional overrides via `PricingAgentConfig`.
2. **Anchoring** — `analysis.competitor_anchor` computes a weighted benchmark using competitor brand position and strength.
3. **Differentiation** — `analysis.differentiation_score` scores differentiators (clean-label, liposomal, clinical dose, etc.) with caps to avoid overpricing.
4. **Guardrails** — `PricingAgent` derives floor and target RRPs from unit cost and margin settings, then applies brand/channel adjustments with max premium ceilings.
5. **Outputs** — `PricingRecommendation` surfaces rounded RRP, wholesale guidance, expected margin, and bullet-point narrative/rationale for commercial review.

## Integration surfaces
- **Python package** — published via `pyproject.toml`; installable with `pip install -e .` for local work or built into a wheel for CI/CD.
- **Google ADK / Agent Builder** — exposed as a FastAPI webhook and containerised for Cloud Run (see `docs/google_adk.md`).
- **GitHub MCP bridge** — forwards MCP tool calls to the Cloud Run webhook for ADK parity in MCP clients (`docs/github_mcp_adk.md`).
- **Legacy compatibility** — `bootstrap_arp.py` preserves earlier notebooks/imports by proxying to the current `PricingAgent` API.

## Quality and guardrails
- Unit tests in `tests/` validate anchor computation, differentiation scoring, pricing guardrails, and the compatibility shim.
- `pytest.ini` pins discovery to the repo root so imports resolve without ad-hoc path tweaks.
- Configuration defaults favour conservative margins; validation in data classes prevents invalid pricing inputs.

## Extensibility notes
- Add new differentiator weights in `analysis.DIFFERENTIATOR_WEIGHTS` to model emerging product signals.
- Adjust channel/brand heuristics in `pricing_agent.PricingAgent` to support additional sales motions.
- UI teams can follow the `docs/development_ui.md` roadmap to build browser consoles on top of the existing webhook or package APIs.
