# Wiring GitHub MCP to the Google ADK Pricing Agent

This guide shows how to connect GitHub's Model Context Protocol (MCP) clients to the pricing agent that you deploy for Google ADK/Agent Builder. The flow reuses the Cloud Run webhook from [`docs/google_adk.md`](google_adk.md) so GitHub tools can invoke the same `/price` endpoint that ADK calls.

## Prerequisites
- The pricing agent container deployed to Cloud Run with the `/price` endpoint available over HTTPS (see [`docs/google_adk.md`](google_adk.md)).
- Node.js 18+ to run the MCP HTTP bridge.
- An MCP-capable client (e.g., GitHub Copilot Workspace, an MCP CLI, or any client that consumes an `mcp.json`/`servers.json` definition).

## 1) Install a lightweight MCP HTTP bridge
Install the reference HTTP bridge so MCP clients can call the Cloud Run webhook without writing a full server:

```bash
npm install -g @modelcontextprotocol/server-http
```

> If you prefer project-local installs, drop the `-g` flag and adjust the command paths below accordingly.

## 2) Create a pricing agent MCP server config
Add an entry to your MCP client configuration (for Copilot Workspace and most MCP CLIs this is `~/.config/mcp/servers.json`). Replace the URL with your Cloud Run endpoint:

```json
{
  "servers": {
    "nousen-pricing-agent": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-http",
        "--url",
        "https://<your-run-url>/price",
        "--name",
        "pricing-agent",
        "--description",
        "Nousen pricing agent webhook deployed for Google ADK"
      ],
      "env": {
        "SERVER_TIMEOUT": "30000"
      }
    }
  }
}
```

What this does:
- Registers a server called `nousen-pricing-agent` that forwards MCP tool calls to the Cloud Run `/price` webhook.
- Keeps the same request/response schema used by ADK, so you can reuse payloads from the FastAPI example in [`docs/google_adk.md`](google_adk.md).
- Uses `npx` to download and run the HTTP bridge on demand, avoiding global installs if you prefer.

## 3) Provide a sample MCP tool invocation
MCP tools typically expose a function-like interface. To mirror the ADK tool input, define the tool signature in your client configuration (example JSON fragment for clients that support inline tool schemas):

```json
{
  "name": "price",
  "description": "Get an RRP/wholesale recommendation for a product given competitor benchmarks.",
  "input_schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "product": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "unit_cost": {"type": "number"},
          "target_margin": {"type": "number"},
          "differentiators": {"type": "array", "items": {"type": "string"}},
          "brand_position": {"type": "string"},
          "channel": {"type": "string"}
        },
        "required": ["name", "unit_cost", "target_margin", "differentiators", "brand_position", "channel"]
      },
      "competitors": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"},
            "brand_position": {"type": "string"},
            "strength_score": {"type": "number"}
          },
          "required": ["name", "price", "brand_position", "strength_score"]
        }
      }
    },
    "required": ["product", "competitors"]
  }
}
```

Clients that support OpenAPI or tool schemas can embed this definition so prompts in Copilot Chat or other MCP-aware UIs surface the parameters. The payload aligns with the FastAPI `PriceRequest` used by Google ADK.

## 4) Test the end-to-end path
1. Start your MCP client so it loads the `servers.json` entry and spins up the HTTP bridge.
2. Call the `price` tool with a payload matching the schema above (you can reuse the sample JSON from `docs/google_adk.md`).
3. Confirm you receive the `rrp`, `wholesale_price`, and `narrative` fields from the Cloud Run deployment.

## 5) Security notes
- If your Cloud Run service requires authentication, configure the MCP client or bridge with an identity token (e.g., `gcloud auth print-identity-token` passed via an `Authorization: Bearer` header). Most MCP HTTP bridges expose a `--header` flag for this.
- Prefer pinned image tags and restricted service accounts on the Cloud Run side; MCP traffic should use the same hardened endpoint you expose to ADK.

This setup lets GitHub MCP clients reuse the same Google ADK-facing webhook, so both ecosystems call a single, consistent pricing service.
