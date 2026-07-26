# A Taxonomy of AI Systems

### From a Single Model to Agentic AI — a framework for identifying, classifying, and reasoning about what an AI solution is built from and why

**Version:** 2.1  **Last revised:** 2026-07-25  **Status:** Working reference, grounded to public industry and research sources (see *Sources*).

---

## 1. How to use this framework

Do **not** read this as a single ladder where each level replaces the one above it. Real systems are positioned on **two independent axes**:

- **Composition** — *how many interacting components* the system has. Ranges from a single model call to dozens of coordinated models, retrievers, and tools.
- **Autonomy (control flow)** — *who decides what happens next*. Ranges from fully developer-defined code paths (a **workflow**) to the model deciding its own next action from feedback (an **agent**).

These axes are orthogonal. A naive RAG pipeline is **highly compound but has near-zero autonomy**. A single ReAct agent is **barely compound but highly autonomous**. Classifying a system means locating it on *both* axes, not picking one rung.

A third, cross-cutting dimension is **level of grounding/reasoning** (does the model just recall, retrieve, or actively reason step-by-step), which is why reasoning models and RAG are called out explicitly below.

The governing engineering principle throughout: **use the simplest architecture that clears the accuracy/reliability bar for the task.** Every step up in composition or autonomy buys capability but costs latency, money, and debuggability.

> **Products vs. architectures.** "Chatbot," "copilot," and "assistant" are *product categories*, not architectures. Any of them can be built at any point on the two axes. Classify by architecture first (§2–§8), then label the product form (§10).

---

## 2. Layer 0 — The model layer (the atoms)

A model is not a "system" — it is the raw component. But you cannot classify a system without naming its engine.

| Entity | One-line description |
|---|---|
| **AI Model** | A single statistical model mapping inputs to outputs (e.g., a Transformer predicting the next token). |
| **Foundation Model** | A large model pre-trained on broad data, adaptable to many downstream tasks; the umbrella that includes LLMs and multimodal models. |
| **Large Language Model (LLM)** | A foundation model specialized for understanding and generating language; the default reasoning/generation engine. |
| **Small Language Model (SLM)** | A compact model tuned for a narrow task, favored for cost, latency, on-device use, and as a specialized component inside larger systems. |
| **Multimodal Model (MLLM)** | A model handling more than one modality (text + image / audio / video) in one network. |
| **Reasoning ("Thinking") Model** | A model trained to spend extra *test-time compute* on an internal chain of thought before answering (e.g., o-series, DeepSeek-R1, "thinking" variants); a distinct "System-2" paradigm vs. instant-answer "System-1" models. |
| **Fine-tuned / Adapted Model** | A base model further trained (SFT, RLHF, LoRA) on domain data; still a model, not a compound system. |
| **Embedding Model** | A model that converts text/data into vectors for similarity search; the backbone of *dense* retrieval (sparse/keyword methods like BM25 retrieve without one — see Hybrid RAG below). |
| **Mixture-of-Experts (MoE)** | *An internal model architecture*, not a system type — routes each token to a subset of expert sub-networks for efficiency. Listed to avoid mis-classifying it as a "compound system." |

---

## 3. Layer 1 — Single-call systems (autonomy: none)

The model is called once; developer code does everything else.

| Entity | One-line description |
|---|---|
| **Simple Query (single LLM call)** | One prompt in, one completion out — no memory, tools, or retrieval. Cheapest, fastest, least reliable on complex tasks. |
| **Prompt-engineered call** | The same single call shaped by few-shot examples, chain-of-thought, or structured-output constraints to raise accuracy without added infrastructure. |
| **Augmented LLM** | The atomic building block of everything below: an LLM able to invoke *retrieval, tools, and memory* on its own. Formally Anthropic's foundational agentic building block. |

---

## 4. Layer 2 — Component vocabulary (what systems are assembled from)

These are not standalone systems; they are the parts you compose. Naming them precisely is what makes classification reliable.

| Component | One-line description |
|---|---|
| **Retriever** | Fetches relevant external knowledge (vector, keyword, hybrid, or graph search) to ground generation. |
| **Tools / Function calling** | External APIs, code execution, or actions the model can invoke to read or change the world. Commonly grouped into three kinds (Huyen, *AI Engineering*, 2025): *knowledge augmentation* (retrieval, search — read-only), *capability extension* (calculators, interpreters, translators), and *write actions* (side-effecting calls that change external state). |
| **Short-term / Working memory** | The context window and scratchpad holding the current task's state. |
| **Long-term memory** | Persistent store (episodic, semantic, procedural) letting a system recall across sessions; typically vector- or database-backed. |
| **Orchestration** | The control logic that decides sequence, routing, and delegation among components. |
| **Guardrails / Safety layer** | Input/output filters, policy checks, and validators that constrain behavior before, during, and after generation. |

---

## 5. Layer 3 — Retrieval-Augmented Generation (the RAG family)

RAG grounds a generator in retrieved data instead of the model's frozen memory. It is the most common *compound* system in production and is itself a spectrum of maturity. (Note: RAG adds **composition**, not autonomy — until you reach Agentic RAG.)

| Entity | One-line description |
|---|---|
| **Naive / Simple RAG** | Single-step: embed query → fetch top-k chunks → stuff into prompt. Great for FAQs, weak on multi-step reasoning. |
| **Advanced RAG** | Adds query rewriting, hybrid search, and reranking; the sensible production default for most applications. |
| **Modular RAG** | A reconfigurable pipeline where retrieval, routing, and generation are swappable blocks (umbrella for advanced patterns). |
| **Hybrid RAG** | Blends sparse (keyword) and dense (semantic) retrieval to improve recall. |
| **GraphRAG** | Retrieves over a knowledge graph of entities and relationships instead of loose chunks; excels when the *connections between items* are the point (legal, biomedical, compliance). |
| **Multi-hop RAG** | Chains several retrieval steps to answer questions requiring facts connected across sources. |
| **Self-RAG / Corrective RAG (CRAG)** | The system evaluates whether retrieved evidence actually answers the query and re-retrieves if not. |
| **Adaptive RAG** | A classifier routes each query to the cheapest pipeline that can handle it (simple→naive, complex→agentic, relational→graph); the emerging cost/quality best practice. |
| **Agentic RAG** | *The intersection of RAG and agents* — an autonomous agent plans, iterates, and uses tools to orchestrate retrieval. Highest accuracy, highest latency and cost. This is the bridge from Layer 5 into RAG. |

---

## 6. Layer 4 — Compound systems & workflows (composition: high, autonomy: low–medium)

| Entity | One-line description |
|---|---|
| **Compound AI System** | The umbrella term (Berkeley/BAIR, Feb 2024): a system tackling tasks with *multiple interacting components* — multiple model calls, retrievers, or external tools. RAG and every workflow below are instances. |

**Workflows** are compound systems where the control flow is fixed in code. The five canonical workflow patterns (Anthropic, *Building Effective Agents*, Dec 2024):

| Pattern | One-line description |
|---|---|
| **Prompt Chaining** | Decompose a task into fixed sequential LLM steps, each feeding the next. Use when the steps are known in advance. |
| **Routing** | A classifier sends each input to the specialized prompt or model best suited to it. |
| **Parallelization** | Run subtasks concurrently (sectioning) or sample multiple times and vote (voting), then aggregate. |
| **Orchestrator-Workers** | A lead LLM dynamically decomposes a task, delegates subtasks to worker LLMs, and synthesizes their output. |
| **Evaluator-Optimizer** | One LLM generates, another critiques against explicit criteria, looping until quality passes. Strong when a clear rubric exists. |

---

## 7. Layer 5 — Agents (autonomy: high)

An agent is a system where the LLM **directs its own process and tool use**, driven by environment feedback in a loop, rather than following predefined code paths. Use only when the task genuinely needs open-ended, adaptive decision-making. (The term predates LLMs: classically, an agent is "anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators" — Russell & Norvig, *Artificial Intelligence: A Modern Approach*. The LLM-agent literature inherits this perceive→act framing directly.)

| Entity | One-line description |
|---|---|
| **AI Agent** | An LLM that dynamically chooses its next action from feedback, maintaining control over how it accomplishes a goal. |
| **ReAct Agent** | The common loop: interleave *reasoning* traces with *actions* (tool calls), observe results, repeat. |
| **Planning Agent** | Explicitly generates a multi-step plan up front, then executes and revises it. |
| **Tool-using Agent** | An agent whose core capability is selecting and calling external APIs/functions to act on the world. |
| **Reflection / Self-critique Agent** | An agent that reviews and revises its own output before finalizing, improving reliability at extra token cost. |

---

## 8. Layer 6 — Multi-agent systems & agentic AI (composition + autonomy: both high)

| Entity | One-line description |
|---|---|
| **Single-Agent System** | One agent running the Observe → Think → Act loop alone; simpler, cheaper, easier to audit; best for well-defined problems. |
| **Multi-Agent System (MAS)** | Several specialized agents coordinating on a shared goal (e.g., planner + researcher + validator); handles complexity that would overwhelm one agent, at the cost of coordination overhead. |
| **Orchestrator / Supervisor pattern** | A lead agent assigns work to sub-agents and integrates their results — the multi-agent form of orchestrator-workers. |
| **Agentic AI** *(contested term)* | Used for the paradigm of autonomous systems that plan, reason, and coordinate across many agents, tools, and systems toward broad goals. **Note:** the crisp "AI agent = one task / agentic AI = orchestrating layer" split comes from specific 2025 papers (e.g., Sapkota et al.); in practice the industry uses "agent" and "agentic AI" loosely and often interchangeably. Treat the distinction as a useful lens, not a settled standard. |

---

## 9. Cross-cutting layers (apply at any tier)

| Entity | One-line description |
|---|---|
| **Interoperability — MCP (Model Context Protocol)** | Open standard (Anthropic, Nov 2024) for the *vertical* connection between a model/agent and external tools, data, and resources — "a USB-C port for AI." |
| **Interoperability — A2A (Agent2Agent)** | Open standard (Google, Apr 2025) for *horizontal* communication and task delegation *between* agents across frameworks, via published "agent cards." Complementary to MCP, not competing. |
| **Related protocols (ACP, ANP)** | Emerging agent-communication / agent-network standards addressing richer intent modeling and open-internet discovery; watch, don't yet standardize on. |
| **Human-in-the-loop (HITL)** | A design choice — not a tier — inserting human review at checkpoints or on blockers; orthogonal to composition and autonomy. |
| **Agent / orchestration frameworks** | Implementation tools (LangGraph, CrewAI, AutoGen, Anthropic Agent SDK, OpenAI Agents SDK, LlamaIndex, Semantic Kernel). **These are how systems are *built*, not categories of system** — do not classify a solution *as* its framework. |

---

## 10. Product categories (the customer-facing label)

Situate these *after* architectural classification, since each can be built anywhere on the two axes.

| Entity | One-line description |
|---|---|
| **Chatbot / Conversational AI** | A dialogue interface; can be a single LLM call, a RAG system, or a full multi-agent system underneath. |
| **Copilot** | An assistant embedded in a specific tool/workflow that suggests and executes within that context (code, docs, spreadsheets). |
| **AI Assistant** | A general-purpose helper spanning tasks and tools; increasingly agentic under the hood. |
| **Vertical / Domain agent** | A product-branded agent specialized to one industry workflow (legal research, customer support, coding), often a MAS with domain guardrails. |

---

## 11. How to classify any AI solution (decision procedure)

Ask, in order:

1. **What is the engine?** Identify the model(s) — LLM, multimodal, reasoning model, fine-tuned/SLM. → fixes *Layer 0*.
2. **How many interacting components?** One model call → *single-call system* (Layer 1). Multiple interacting parts (models, retrievers, tools) → a *compound system* (Layer 3–4), and everything below lives under that umbrella.
3. **Is knowledge retrieved?** If external data is fetched to ground answers, it is in the *RAG family* (Layer 3) — then place it on the naive→agentic maturity spectrum.
4. **Who owns the control flow?** Fixed, developer-defined paths → *workflow*. The model decides its next step from feedback → *agent* (Layer 5).
5. **How many decision-makers?** One agent → *single-agent*. Several coordinating → *multi-agent / agentic AI* (Layer 6).
6. **How do parts connect and where do humans sit?** Note interoperability (MCP/A2A), guardrails, and HITL checkpoints (Layer 9).
7. **What product form is it sold as?** Label chatbot / copilot / assistant / vertical agent last (Layer 10).

**Output of the procedure:** a system is fully described by *(engine, composition level, retrieval strategy, control-flow type, agent count, connectivity, product form)* — not by a single tier name.

---

## 12. Revision history

**v2.1 (this version)** corrects v2.0 and adds cross-lab grounding:
- Fixed three wrong Layer cross-references in the §11 decision procedure (RAG cited as Layer 5, Agent as Layer 7, Multi-agent as Layer 8 — all off by +2 from their actual section headers; corrected to Layer 3, 5, and 6 respectively).
- Corrected the Layer-2 claim that embedding models are "the backbone of all retrieval" (overstated — sparse/keyword retrieval like BM25 needs none), and cross-referenced Hybrid RAG.
- Added OpenAI's Agents SDK/API docs and Chip Huyen's *AI Engineering* (2025) as sources; added OpenAI Agents SDK to the frameworks list; added Huyen's three-way tool taxonomy to the Tools component row.
- Added the classical (pre-LLM) Russell & Norvig agent definition as historical grounding for Layer 5.
- Re-verified all prior primary-source quotes (Anthropic, BAIR, Google A2A) directly against the source pages.

**v2.0** corrects and extends v1.0:
- Replaced the misleading single "simple→complex ladder" with two orthogonal axes (composition × autonomy) plus a reasoning/grounding dimension.
- Added the **reasoning-model** paradigm (test-time compute / System-2), **SLMs**, and a note on MoE as an internal architecture.
- Added a **component vocabulary** layer (retriever, tools, typed memory, orchestration, guardrails).
- Added the **interoperability layer** (MCP, A2A, and related protocols).
- Flagged **"agentic AI vs. AI agent"** as a contested, source-specific distinction rather than a settled standard.
- Separated **product categories** (chatbot/copilot/assistant) from architectures to prevent mis-classification.
- Clarified that **frameworks** are implementation tools, not system categories.

---

## 13. Sources (grounding)

Primary and authoritative references this framework is built on:

- **Berkeley AI Research (BAIR)** — *The Shift from Models to Compound AI Systems* (Zaharia, Khattab, Chen, Davis, Miller, Potts, Zou, Carbin, Frankle, Rao, Ghodsi; Feb 18 2024). Origin of the "compound AI system" definition: *"a system that tackles AI tasks using multiple interacting components, including multiple calls to models, retrievers, or external tools."*
- **Anthropic** — *Building Effective Agents* (Schluntz & Zhang, Dec 2024). Source of the augmented-LLM building block ("an LLM enhanced with augmentations such as retrieval, tools, and memory"), the workflow-vs-agent distinction ("Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents… are systems where LLMs dynamically direct their own processes and tool usage"), and the five workflow patterns; and the *Model Context Protocol* (Nov 25 2024).
- **Google** — *Agent2Agent (A2A) Protocol* announcement (Apr 9 2025). Horizontal agent-interoperability standard, explicitly positioned as complementary to MCP: *"A2A is an open protocol that complements Anthropic's Model Context Protocol (MCP), which provides helpful tools and context to agents."*
- **OpenAI** — Agents SDK / API documentation. Defines agents as *"applications that plan, call tools, collaborate across specialists, and keep enough state to complete multi-step work,"* distinguishing direct Responses-API calls (developer manages the loop) from SDK-orchestrated agent runs. Confirms the single-call → developer-orchestrated → model-orchestrated progression independently of Anthropic's framing, though OpenAI does not use "augmented LLM" terminology.
- **Chip Huyen** — *AI Engineering* (O'Reilly, 2025) and the companion essay "Agents" (huyenchip.com, Jan 2025). Source of the three-way tool taxonomy (knowledge augmentation / capability extension / write actions) and the planning-vs-execution distinction used in §4 and §7.
- **Russell & Norvig** — *Artificial Intelligence: A Modern Approach*. Source of the foundational, pre-LLM definition of "agent" (perceives environment via sensors, acts via actuators) that the current LLM-agent literature inherits.
- **RAG literature** — surveys and practitioner guides establishing the naive → advanced → graph → adaptive → agentic maturity spectrum (2024–2026).
- **Reasoning-model / test-time-compute literature** — Snell et al. (2024) and the o1/o3, DeepSeek-R1, and Gemini "thinking" model families (2024–2026).
- **Agent-taxonomy literature** — surveys on LLM-based autonomous agents and the (contested) agent vs. agentic-AI distinction (e.g., Sapkota et al., 2025).

> Terminology in this field is moving fast and is not fully standardized. Where usage is contested, this document flags it rather than picking a winner. Re-verify protocol dates and model names against primary sources before citing externally.
