# AI Engineering — Frontier Technology Roadmap

Companion to the taxonomy files in this folder. Covers only the technologies confirmed via official sources (Linux Foundation, Google, Anthropic) as actively moving from "emerging" to production-grade industry standard as of 2026 — not a general AI engineering curriculum.

---

## Stage 1: MCP (Model Context Protocol)

**What:** vendor-neutral standard for connecting models to tools/data/resources — donated by Anthropic to the Linux Foundation (Dec 9, 2025) as founding project of the new Agentic AI Foundation (AAIF), with Anthropic, Block, and OpenAI as founding contributors. 10,000+ published MCP servers, 97M+ monthly SDK downloads, adopted by ChatGPT, Gemini, Microsoft Copilot, Cursor, Replit, VS Code.

**Practice with what's already in this repo:** `6_mcp/` is a real MCP client/server implementation — study `accounts_server.py`, `market_server.py`, `mcp_params.py` first, then try connecting it to a local Ollama model instead of its current backend.

**Certification:** **MCP Associate (MCPA)** — the first official MCP certification, issued by the Linux Foundation.
- 120-minute exam, valid 2 years
- No formal prerequisites, but recommends foundational knowledge of JSON-RPC-style protocols and experience with LLM APIs — explicitly including "local models via Ollama"
- Advisory council: Anthropic, Google, AWS, Microsoft, Block, GitHub, Hugging Face
- https://training.linuxfoundation.org/certification/model-context-protocol-associate-mcpa/

---

## Stage 2: Agent Skills

**What:** Anthropic's open standard for packaging reusable agent instructions (`SKILL.md` format), published as an independent open standard on Dec 18, 2025 at `agentskills.io`. Adoption within 48 hours: Microsoft (VS Code), OpenAI (ChatGPT, Codex CLI). Partner skills at launch from Canva, Stripe, Notion, Zapier.

**Practice:** build one real skill for Claude Code, then hand-reimplement the same pattern for an Ollama-backed agent (no native Ollama support for Skills exists yet — this is a genuine gap worth closing yourself).

**Certification:** no standalone "Agent Skills" certification exists yet. Covered as a topic inside **Anthropic Academy**, Anthropic's free official training platform (launched March 2, 2026).
- 18 free, self-paced courses — prompting through agentic systems, Claude Code, MCP, Agent Skills, subagents, Claude Cowork
- Certificates issued directly by Anthropic, verifiable, shareable on LinkedIn
- No Anthropic account required — sign up with email
- https://anthropic.skilljar.com

---

## Stage 3: A2A (Agent2Agent)

**What:** Google's protocol for cross-platform, cross-organization agent-to-agent communication. Announced April 2025, now also Linux Foundation/AAIF-governed. At v1.2 as of 2026, with signed agent cards (cryptographic domain verification). 150+ organizations in production — including Google, Microsoft, AWS, Salesforce, SAP, ServiceNow, Workday, IBM. Natively integrated into Azure AI Foundry, Amazon Bedrock AgentCore, and Google Cloud.

**Practice:** harder to do solo — it's designed for cross-organization coordination — but a starting exercise is two of your own local agents (e.g., two `qwen3:8b` instances with different roles) exchanging a signed agent card and delegating a task.

**Certification:** **no formal certification exists yet**, unlike MCP. The closest official credential is a **codelab/workshop badge** from the Google Developer Program (Cloud Next 2026) — a hands-on exercise with a completion badge, not a full certification program.
- https://developers.google.com/profile/badges/events/cloud/next/2026/codelab/multi-agent-systems-with-the-a2a-protocol

---

## Umbrella: Agentic Infrastructure

**What:** the broader industry shift toward treating AI agents as first-class platform components — handling provisioning, configuration, deployment, and remediation as standard practice, not just chat/coding assistance. Agent framework adoption (LangChain, LangGraph, Pydantic AI, Vercel AI SDK) roughly doubled — 9.1% to 17.5% organizational adoption in about a year.

**Certification:** none specific — this is a practice discipline (observability, cost governance, production reliability for agent systems), not a named standard. It's what MCP + Agent Skills + A2A knowledge gets *applied toward*, not a fourth item to certify in separately.

---

## Suggested order

1. **MCP** — most concrete, most attainable certification, and you already have a working reference module (`6_mcp/`) in this repo.
2. **Agent Skills** — short, free, immediate certificates from Anthropic Academy.
3. **A2A** — conceptually builds on the other two, and currently has the least mature practice/certification path — treat it as the stretch goal.

---

## Sources

- [Introducing the MCPA — Agentic AI Foundation](https://aaif.io/blog/introducing-the-mcpa-the-first-official-certification-for-the-model-context-protocol)
- [Model Context Protocol Associate (MCPA) — Linux Foundation](https://training.linuxfoundation.org/certification/model-context-protocol-associate-mcpa/)
- [Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [A year of open collaboration: A2A anniversary — Google Open Source Blog](https://opensource.googleblog.com/2026/04/a-year-of-open-collaboration-celebrating-the-anniversary-of-a2a.html)
- [A2A Protocol: 150+ Organizations in One Year — Stellagent](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent)
- [Anthropic Opens Agent Skills Standard — Unite.AI](https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/)
- [Anthropic Academy: 13 Free Courses on Claude Code, API, MCP and Agent Skills](https://pasqualepillitteri.it/en/news/371/anthropic-academy-free-courses-claude)
