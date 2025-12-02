# Alignment notes for `google/adk-python`

This repository cannot currently reach `https://github.com/google/adk-python` from the build environment (HTTPS CONNECT returns 403), so the checklist below captures what was added locally plus the steps to run once network access is available.

## What changed locally
- Added a built-in FastAPI entrypoint (`serve_google_adk.py`) that mirrors the Cloud Run webhook shape described in `docs/google_adk.md`, so ADK tool calls can POST directly to `/price`.
- Added an `adk` optional dependency group in `pyproject.toml` (`fastapi`, `uvicorn[standard]`, `pydantic`) to simplify installing the runtime dependencies for the webhook.

## Follow-up checks when `google/adk-python` is accessible
1. Clone the repo and review its sample tool contract to ensure the `/price` payload matches their expected schema (field names, casing, and required/optional fields).
2. If their SDK offers a base `Tool` or schema helper, consider providing a thin adapter that wraps `PricingAgent.recommend` using that abstraction in addition to the HTTP webhook.
3. Compare any provided deployment manifests (Cloud Run service settings, Dockerfiles, IAM scopes) with ours and align defaults where they diverge.
4. Run any conformance or example tests shipped with `google/adk-python` against this project’s webhook to confirm compatibility.
5. If their repository publishes a PyPI package, add it as an optional dependency and document the usage pattern (e.g., CLI invocation, decorator-based tool registration).

Once connectivity is available, update this document with concrete findings and file any necessary code changes (e.g., schema tweaks or adapters) based on the upstream reference implementation.
