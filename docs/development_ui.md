# Development UI — Next Steps

This roadmap outlines pragmatic next steps for building a developer-focused UI that surfaces the pricing agent, runs scenarios, and routes outputs to downstream tools (Google ADK/Agent Builder, MCP, and internal stakeholders).

## Objectives
- Provide a browser-based console for product managers and analysts to run pricing scenarios without using the Python API directly.
- Keep the UI thin: delegate calculations to the existing FastAPI/Cloud Run webhook or a local FastAPI dev server.
- Support observability (audit trail of inputs/outputs) and safe defaults so proposed prices respect the agent's guardrails.

## Implementation next steps
1. **Pick the stack and scaffold**
   - Use Vite + React + TypeScript (or your in-house equivalent) for fast local dev and typed request models.
   - Add a `.env.local` for the pricing API base URL (Cloud Run or local FastAPI) and optional API key header.
   - Include linting/formatting (ESLint + Prettier) and unit tests (Vitest) in the scaffold.
2. **Create a Pricing Workspace screen**
   - Form inputs for `ProductProfile` fields (name, unit_cost, target_margin, differentiators, brand_position, channel).
   - Dynamic list/table for competitor anchors (`name`, `price`, `brand_position`, `strength_score`).
   - Submit button that posts to `/price` (per `docs/google_adk.md`), with in-flight/loading state and validation.
3. **Render recommendations**
   - Card/table showing `rrp`, `wholesale_price`, `minimum_margin`, and the narrative bullet points returned by the agent.
   - Provide copy/export: copy-to-clipboard JSON and CSV/Markdown download for sharing.
4. **Add history and observability**
   - Client-side history of the last N runs (persisted in `localStorage`) with re-run capability.
   - Optional server-side audit log endpoint: append structured request/response objects for governance.
5. **Wire ADK and MCP contexts**
   - Toggle to send the same payload to the Google ADK Cloud Run webhook (reuse the API base URL) and show the response envelope ADK expects.
   - MCP users: include a help modal linking to `docs/github_mcp_adk.md` plus sample `servers.json` snippet for the UI.
6. **Authentication and safety**
   - If the Cloud Run service uses an API key or IAM token, surface this as a required env var and prevent requests without it.
   - Guardrails: client-side checks to prevent `target_margin` below the documented minimum and to warn when competitor anchors are empty.
7. **Deploy and share**
   - Build and deploy the static UI to Firebase Hosting, Vercel, or GitHub Pages; point it at the Cloud Run base URL.
   - Document a one-command preview deploy (e.g., `npm run deploy:preview`) for reviewers.

## Validation checklist for the UI
- [ ] Pricing requests succeed against both local FastAPI and Cloud Run endpoints.
- [ ] Form validation covers required fields and numeric ranges.
- [ ] Narrative and pricing outputs render legibly on mobile and desktop breakpoints.
- [ ] History replays reproduce identical API calls.
- [ ] API key/Tokens are never logged or stored in history.
