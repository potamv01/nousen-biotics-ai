# Pricing Agent Review Checklist

Use this checklist to decide whether to accept a change set for the pricing agent package and Google ADK deployment assets.

## Functional coverage
- Confirm the pricing agent core behaviours (margin protection, differentiation premiums, wholesale guidance) are exercised by the automated tests.
- For changes touching the Google ADK webhook or FastAPI sample, run the service locally to validate the webhook payload contract and response schema.

## Testing
- Run `python -m pytest -q` from the repository root to ensure all unit tests pass.
- If packaging or deployment scaffolding changed, build the wheel with `python -m build` and confirm installation via `pip install dist/*.whl`.

## Compatibility
- Verify the code still targets Python 3.7+ (avoids `|` union syntax, `list[str]` annotations, and dataclass slots).
- Ensure legacy imports via `bootstrap_arp` remain functional for downstream notebooks.

## Deployment
- For Google ADK/Agent Builder, follow the steps in `docs/google_adk.md` to confirm Cloud Run deployment and webhook configuration succeed.
- Check container image build logs for missing environment variables or dependency resolution issues.

## Documentation
- Ensure README and deployment guides reflect any new configuration flags, API parameters, or environment variables introduced by the change.
