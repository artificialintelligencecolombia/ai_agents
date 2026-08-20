# AI Engineering Stack — Tier List

Every tool/framework/protocol/service discussed across this session, plus the boundary domains (observability, cloud/infra, security, software architecture) needed for a comprehensive AI Engineering profile — ranked by current industry demand (adoption data, market share, official standards) rather than hype or recency. S = near-universal/foundational or mandatory; lower tiers = real and useful but narrower, earlier-stage, or more specialized.

---

## S-Tier — near-universal, foundational, or mandatory

| Item | Why S-tier |
|---|---|
| **Python** | The base language underneath nearly everything discussed |
| **RAG** (as a technique) | Consistently cited by employers as a core requirement |
| **MCP (Model Context Protocol)** | 10,000+ servers, 97M+ SDK downloads, adopted by every major platform, Linux Foundation-governed with a formal certification |
| **OpenAI API / ecosystem** | Still 63% enterprise LLM market share |
| **LangChain / LangGraph** | Explicitly reported as "becoming standard" for agentic applications |
| **AWS Bedrock** | More tokens flowed through Bedrock in Q1 2026 than in all prior years combined; customer spend up 170% quarter-over-quarter; AWS's own framing positions it as the foundation of a modern AI strategy alongside SageMaker |
| **Docker / containerization** | Not AI-specific, but a hard requirement the moment work moves past a notebook — underlies sandboxed code execution, reproducible inference environments, and virtually all production AI deployment |
| **OWASP LLM/GenAI Top 10** | The official, incident-data-grounded AI security standard (not just an expert-vote list anymore — now built on ~10,000 real-world incidents). Prompt injection has topped it three years running. This is baseline required knowledge, not a specialization |
| **Software architecture fundamentals** (API design, microservices vs. monolith, event-driven patterns, scalability) | Not AI-specific, but nothing else on this list scales, deploys, or survives a code review without it — the prerequisite underneath every other item here |

## A-Tier — strong, growing, widely adopted, not yet universal

| Item | Why A-tier |
|---|---|
| **Claude API / Claude Agent SDK / Claude Code** | Strong and fast-growing, especially in coding-agent work, but doesn't match OpenAI's overall enterprise share |
| **Agent Skills (open standard)** | Explosive adoption (Microsoft + OpenAI within 48 hours) — only months old, hasn't proven staying power yet |
| **Tool/function calling** | Foundational, usually bundled into "agentic AI" as a skill category rather than named separately |
| **CrewAI / AutoGen** | Real, production-used multi-agent frameworks in a genuinely fragmented landscape |
| **Vector databases** (as a category) | Foundational to RAG, effectively mandatory alongside it |
| **MLOps** | Broadly and consistently cited in "in-demand skills" reporting |
| **Managed/hosted agent platforms** (Anthropic Managed Agents, Bedrock AgentCore, Azure AI Foundry) | Rising fast, natively integrated into all three major clouds |
| **LangSmith** | Best-in-class tracing specifically for LangChain/LangGraph stacks — node-by-node state diffs, full execution graphs, "virtually no measurable overhead" |
| **AWS SageMaker** | Still critical for custom model building; the SageMaker/Bedrock line has blurred as SageMaker gains serverless, agent-guided workflows |

## B-Tier — real and useful, more specialized or earlier-stage

| Item | Why B-tier |
|---|---|
| **A2A (Agent2Agent) protocol** | 150+ orgs in production, narrower use case (cross-org agent coordination), no formal certification yet |
| **Ollama** | Extremely popular for local dev/prototyping/learning; rarely a named job-posting requirement the way MCP or RAG are |
| **Hugging Face** (hub, `transformers`, Inference Endpoints) | Foundational for open-weight model work, especially research/ML-engineering-leaning roles |
| **Google Gemini API** | Real and growing, doesn't match OpenAI's current enterprise share |
| **LiteLLM** | Valuable glue/abstraction layer, a supporting tool rather than a named skill on its own |
| **LlamaIndex** | Solid RAG-specific framework, generally less mindshare than LangChain currently |
| **Langfuse** | The best fully open-source LLM observability tool — self-hosting for compliance/data-residency needs, strong developer experience, unlimited users on all tiers. Genuinely aligned with an Open Source AI Engineer profile specifically, even though LangSmith currently leads on raw adoption |
| **Arize (Phoenix)** | Leads specifically in enterprise RAG evaluation and monitoring — a real specialization, not a general-purpose leader |

## C-Tier / Emerging — watch, not yet demanded

| Item | Why C-tier |
|---|---|
| **Related agent protocols (ACP, ANP)** | Explicitly flagged in the taxonomy source doc as "watch, don't yet standardize on" |
| **OpenCode** | Promising open-source agent CLI, not yet an established job-market requirement |
| **Kimi K2/K3, DeepSeek, Together AI** | Real, cost-effective alternatives — niche next to the OpenAI/Anthropic/Google trio |
| **Specific local open-weight models** (`qwen3:8b`, `gpt-oss:20b`, etc.) | Good for practice and cost control; employers care that you can work with LLMs generally, not that you know one specific model tag |
| **W&B, Confident AI, MLflow (for LLM observability specifically)** | Real tools, but each is either extending from a different heritage (W&B: ML training; MLflow: general MLOps) or positioned as newer/more niche (Confident AI: cross-stack governance standardization) than the A/B-tier observability leaders |
| **AWS Amplify** | Honest caveat: this is a full-stack web/mobile app deployment framework, not AI-specific. Relevant only if you're building the product/frontend *around* an AI feature — not a core AI engineering tool. Include it if your work spans full-stack product development; skip it if you're staying backend/AI-focused |

---

## Missing from everything discussed — still real gaps

- **Fine-tuning / LoRA / QLoRA** — reported as *the* most sought-after specialized skill in enterprise AI. Also the one thing this session established as **not feasible on your current hardware**.
- **Data engineering fundamentals** — Databricks, Snowflake, Apache Airflow, Apache Kafka — still not covered anywhere in this conversation.
- **PyTorch / TensorFlow** — this entire session was inference/API-focused; the training-framework side of AI engineering was never part of it.
- **AI governance/compliance beyond security** — OWASP covers the security angle now; broader regulatory/governance practice (model cards, audit trails, policy compliance) is still untouched.

---

## Takeaway

Your practical setup this session (Ollama + Claude Agent SDK + MCP + RAG understanding) directly touches four **S-tier** items (Python, RAG, MCP, and — once you containerize anything — Docker) plus several A/B-tier ones. The two domains added this round — **security (OWASP) and software architecture** — are both S-tier precisely because they're prerequisites, not specializations: every other item on this list depends on them to actually ship. The remaining real gap is unchanged from before: fine-tuning and the data-engineering/MLOps stack sit entirely outside what this session built toward.
