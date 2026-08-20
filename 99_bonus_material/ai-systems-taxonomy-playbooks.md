# AI Systems Taxonomy — Practice Playbooks

Companion to `ai-systems-taxonomy.md` and `ai-systems-taxonomy-engines.md`. One playbook per taxonomy layer, grounded in what already exists in this repo (`agents/`) — reuse the reference implementation where one exists, port it to Ollama where you want the open-source version, and treat the gaps as your next build.

**Correction from earlier in this session:** Ollama's embeddings endpoint is `/api/embed` (current), not `/api/embeddings` (older path, may still work but isn't the documented one going forward). Use `/api/embed` below.

---

## Cost-reduction practices — official URLs

The three techniques from the last two messages (Batch API, prompt caching, effort control), straight from the source:

- **Batch API (50% off):** https://platform.claude.com/docs/en/build-with-claude/batch-processing.md
- **Prompt caching (~90% off repeated content):** https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md
- **Effort parameter (`low`/`medium`/`high`/`xhigh`/`max`):** https://platform.claude.com/docs/en/build-with-claude/effort.md

---

## Layer 0 — Model layer

**Repo reference:** none dedicated — every module below uses a model implicitly.
**Playbook:** confirm your three Ollama models (`qwen3:8b`, `nomic-embed-text`, `qwen3-vl:4b`) are pulled (`ollama list`); this is prerequisite setup you've already done.
**URL:** https://docs.ollama.com/api

## Layer 1 — Single-call systems

**Repo reference:** `2_claude/1_lab1/claude_agent_streaming.py` (single-query pattern), `2_openai/1_lab1.ipynb`.
**Playbook:** take the same prompt from `claude_agent_streaming.py`, send it to `qwen3:8b` via `/api/chat` instead, compare outputs side by side.
**URL:** https://docs.ollama.com/api

## Layer 2 — Components (retriever, tools, memory, orchestration, guardrails)

**Repo reference:** `4_langgraph/sidekick_tools.py` (tool definitions), `4_langgraph/memory.db` (long-term memory, SQLite-backed).
**Playbook:** use `sidekick_tools.py`'s tool schemas as your reference shape, reimplement with Ollama's `tools` param on `qwen3:8b`; reuse the same SQLite-file pattern from `memory.db` for your own long-term memory store (engine-agnostic — same file format works with either model).
**URL:** https://docs.ollama.com/api

## Layer 3 — RAG family

**Repo reference:** none in this repo — no dedicated RAG lab exists across any module. This is a genuine gap in the curriculum, not just your stack.
**Playbook:** build naive RAG first — `nomic-embed-text` for embeddings, `qwen3:8b` for generation — before attempting Advanced/Hybrid/Graph variants. Suggested location: a new folder alongside `2_claude/1_lab1`, e.g. `2_claude/2_rag/`.
**URL:** https://docs.ollama.com/api/embed

## Layer 4 — Compound systems & workflows

**Repo reference:** `2_openai/deep_research/` — `research_manager.py` orchestrates `planner_agent.py` → `search_agent.py` → `writer_agent.py` → `email_agent.py`. This *is* an Orchestrator-Workers implementation already built and running in your repo.
**Playbook:** read `research_manager.py` first — that's your orchestration reference — then port the same decomposition pattern to `qwen3:8b`, swapping OpenAI's Agents SDK calls for Ollama `/api/chat` calls with tool definitions.
**URL:** https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md

## Layer 5 — Agents

**Repo reference:** `2_claude/1_lab1/claude_agent_debugger.py` — a working ReAct-style, tool-using agent, already Pro-covered and confirmed running.
**Playbook:** this one's done on the Claude side. For the open-source version, rebuild the same debugging task against `qwen3:8b` with a hand-rolled loop (`while` on tool calls, same shape as the manual Anthropic SDK loop) and compare fix quality against Claude's result.
**URL:** https://code.claude.com/docs/en/agent-sdk

## Layer 6 — Multi-agent systems

**Repo reference:** `3_crew/*` (five CrewAI examples: `coder`, `debate`, `engineering_team`, `financial_researcher`, `stock_picker`), `5_autogen/*`, `6_mcp/trading_floor.py`. These are your richest existing MAS reference implementations.
**Playbook — swap these to Ollama directly, no rewrite needed, just config:**
- **CrewAI:** `llm = LLM(model="ollama/qwen3:8b", base_url="http://localhost:11434")`, and set `OPENAI_API_KEY="NA"` in your env (CrewAI validates this key exists at startup even when unused — confusing error otherwise).
- **AutoGen:** config dict with `"model": "qwen3:8b"`, `"base_url": "http://localhost:11434/v1"`, `"api_key": "ollama"` (placeholder — Ollama doesn't check it, the field just needs to be present).
- Confirm Ollama is running *before* starting either framework — a connection-refused error will otherwise look like a model config problem.
**URLs:** https://docs.crewai.com/en/learn/llm-connections · https://collabnix.com/running-ai-agents-locally-with-ollama-and-autogen/

## Layer 9 — Cross-cutting (MCP, A2A, HITL, frameworks)

**Repo reference:** `6_mcp/*` in full — `accounts_server.py`, `market_server.py`, `push_server.py` are real MCP servers; `mcp_params.py` shows client-side config.
**Playbook:** this module is your canonical MCP reference already. MCP itself is an open protocol, so these same servers can in principle be called by any MCP-aware client — but Ollama has no built-in MCP client, so pointing a local model at them means writing the MCP-client plumbing yourself (parse the server's tool list, translate to Ollama's `tools` schema, route responses back).
**URLs:** https://platform.claude.com/docs/en/managed-agents/mcp-connector.md · https://modelcontextprotocol.io

## Layer 10 — Product categories

**Repo reference:** `6_mcp/app.py`, `4_langgraph/app.py` — both are working product-layer wrappers (chatbot/assistant UI) over their respective agent backends.
**Playbook:** the product layer is engine-agnostic — study either `app.py` for the UI/wiring pattern, then swap the backend call from its current engine to `qwen3:8b` or Claude Agent SDK depending on which layer-5/6 build you're demoing.

---

## Priority order, given what already exists

1. **Layer 5 (Agents)** — already built and Pro-covered (`claude_agent_debugger.py`); cheapest next step is porting it to Ollama for comparison.
2. **Layer 6 (Multi-agent)** — richest existing reference material (`3_crew`, `5_autogen`, `6_mcp`); the CrewAI/AutoGen Ollama swap above is a config change, not new code — highest payoff for lowest effort.
3. **Layer 3 (RAG)** — the one true gap in the curriculum itself; building this from scratch is your best learning opportunity, not just a port.
4. **Layer 4 (Workflows)** — `2_openai/deep_research` is a strong template to study before building your own orchestrator.

Sources:
- [Connect to any LLM - CrewAI](https://docs.crewai.com/en/learn/llm-connections)
- [Running AI Agents Locally with Ollama and AutoGen](https://collabnix.com/running-ai-agents-locally-with-ollama-and-autogen/)
- [Ollama API Reference](https://docs.ollama.com/api)
- [Generate embeddings - Ollama](https://docs.ollama.com/api/embed)
