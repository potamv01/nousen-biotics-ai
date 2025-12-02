# Deploying the Pricing Agent with Google ADK (Agent Builder)

This guide shows how to wrap the pricing agent in a minimal HTTP surface that Google ADK/Agent Builder can call as a tool, then deploy it to Cloud Run.

## 1) Prerequisites
- Python 3.7+
- Google Cloud SDK authenticated to your project (`gcloud auth login`) and configured (`gcloud config set project <PROJECT_ID>`)
- Docker and permissions to push to **Artifact Registry** (or **Container Registry**)
- (Optional) A dedicated service account for the Cloud Run service with the minimum needed roles

## 2) Add an HTTP entrypoint for ADK
Create a lightweight FastAPI app that exposes a `/price` endpoint. Google ADK tool calls can hit this endpoint as an HTTPS webhook.

```bash
pip install fastapi uvicorn
```

Create `serve_google_adk.py` at repo root:

```python
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
    differentiators: list[str]
    brand_position: str
    channel: str

class PriceRequest(BaseModel):
    product: ProductPayload
    competitors: list[CompetitorPayload]

@app.post("/price")
async def price(req: PriceRequest):
    try:
        product = ProductProfile(**req.product.dict())
        competitors = [CompetitorProduct(**c.dict()) for c in req.competitors]
        recommendation = agent.recommend(product, competitors)
        return recommendation.__dict__
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
```

Run locally for a quick check:

```bash
uvicorn serve_google_adk:app --reload --port 8080
```

## 3) Build and push the container

From the repo root:

```bash
# Build
PROJECT_ID=$(gcloud config get-value project)
REGION=europe-west1   # pick your region
IMAGE_NAME=nousen-pricing-agent

gcloud builds submit --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/pricing/${IMAGE_NAME}:latest" .
```

_The command uses Cloud Build; adjust the repository and tag to match your Artifact Registry setup._

## 4) Deploy to Cloud Run

```bash
gcloud run deploy nousen-pricing-agent \
  --image "${REGION}-docker.pkg.dev/${PROJECT_ID}/pricing/${IMAGE_NAME}:latest" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --platform managed
```

Take note of the HTTPS URL that Cloud Run prints (e.g., `https://nousen-pricing-agent-xyz.a.run.app`).

## 5) Wire up Google ADK / Agent Builder

1. In the **Google Cloud console**, open **Vertex AI > Agent Builder** and create (or edit) your agent.
2. Add a **tool** that uses an HTTPS endpoint. Point it to the Cloud Run URL `/price` you deployed above.
3. Define the tool input schema to match `PriceRequest` (product + competitors). Optionally add descriptions mirroring the Pydantic fields.
4. Publish the agent. ADK will call the Cloud Run webhook when the tool is invoked during conversations.

## 6) Security and ops considerations
- Prefer an authenticated Cloud Run URL; create an **invoker** service account and give your ADK agent that identity.
- Attach Cloud Monitoring/Logging and error reporting via standard GCP tooling.
- Set resource flags (CPU/memory/concurrency) on `gcloud run deploy` for your throughput needs.
- Pin the container tag (e.g., `:v1.0.0`) and roll forward with new tags to avoid accidental upgrades.

## 7) Minimal `Dockerfile` (if you don't already have one)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir . fastapi uvicorn
CMD ["uvicorn", "serve_google_adk:app", "--host", "0.0.0.0", "--port", "8080"]
```

You can adjust the Python version to your target runtime; Cloud Run supports many base images.

## 8) Quick validation
- `gcloud run services describe nousen-pricing-agent --region ${REGION}` to verify deployment.
- `curl -X POST https://<run-url>/price -H "Content-Type: application/json" -d @sample.json` to test the webhook manually.

This flow keeps the core pricing agent unchanged while exposing it as an ADK-compatible webhook.

## 9) Optional: bridge the webhook to GitHub MCP

If you also want GitHub MCP clients (e.g., Copilot Workspace) to call the same Cloud Run endpoint, use the reference `servers.json` entry and tool schema in [`docs/github_mcp_adk.md`](github_mcp_adk.md) to forward MCP requests to `/price`.
