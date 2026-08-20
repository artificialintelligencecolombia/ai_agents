# AI Systems Taxonomy — Recommended Engine & Open-Source Stack Coverage

Companion to `ai-systems-taxonomy.md`. **Engine** = best-fit option overall (Claude Agent SDK via Pro subscription, or Ollama with a specific model). **Stack coverage** = can this be built *today* with your open-source-only stack (Ollama — `qwen3:8b`, `qwen3:4b`, `qwen3-vl:4b`, `nomic-embed-text`, optionally `gpt-oss:20b`), independent of Claude — since Claude is proprietary and doesn't count toward the Open Source AI Engineer goal even though it's free-to-you via Pro.

✅ = fully coverable now · ⚠️ = coverable but degraded (weaker model, hand-rolled vs. native, sequential vs. concurrent) · ❌ = not realistically coverable with current hardware/stack

## Layer 0 — Model layer

| Entity | Engine | Stack coverage |
|---|---|---|
| AI Model | Ollama — `qwen3:8b` | ✅ |
| Foundation Model | Ollama — `qwen3:8b` | ✅ |
| Large Language Model (LLM) | Claude (Pro) primary; Ollama `qwen3:8b` free alt | ✅ |
| Small Language Model (SLM) | Ollama — `qwen3:4b` | ✅ |
| Multimodal Model (MLLM) | Ollama — `qwen3-vl:4b` | ✅ |
| Reasoning ("Thinking") Model | Claude (Pro, adaptive thinking) preferred | ⚠️ `gpt-oss:20b` works but is slow/CPU-bound on your GPU |
| Fine-tuned / Adapted Model | Cloud notebook (Colab) — not local | ❌ 6GB VRAM too tight even for QLoRA |
| Embedding Model | Ollama — `nomic-embed-text` | ✅ |
| Mixture-of-Experts (MoE) | Architecture note, not a pick | ✅ `gpt-oss:20b` is a MoE already in your toolkit |

## Layer 1 — Single-call systems

| Entity | Engine | Stack coverage |
|---|---|---|
| Simple Query (single call) | Ollama — `qwen3:8b` | ✅ |
| Prompt-engineered call | Ollama — `qwen3:8b` | ✅ |
| Augmented LLM | Claude Agent SDK (Pro, built-in) | ⚠️ tools/retrieval/memory all hand-rolled with Ollama, not native |

## Layer 2 — Components

| Entity | Engine | Stack coverage |
|---|---|---|
| Retriever | Ollama — `nomic-embed-text` + your own vector store | ✅ |
| Tools / Function calling | Ollama — `qwen3:8b` (`tools` param) | ✅ |
| Short-term / Working memory | N/A — `num_ctx` setting | ✅ |
| Long-term memory | N/A — your own store, engine-agnostic | ✅ |
| Orchestration | N/A — your own code | ✅ |
| Guardrails / Safety layer | Ollama — `qwen3:4b` filter pass or plain code | ✅ |

## Layer 3 — RAG family

| Entity | Engine | Stack coverage |
|---|---|---|
| Naive / Simple RAG | Ollama — `qwen3:8b` + `nomic-embed-text` | ✅ |
| Advanced RAG | Same + reranking | ⚠️ **correction:** no dedicated reranker model in your pulled toolkit — you'd prompt `qwen3:8b` to score relevance (works, but a real cross-encoder reranker would need an extra pull) |
| Modular RAG | N/A — pattern, your components | ✅ |
| Hybrid RAG | `nomic-embed-text` + BM25 (your own code, no model needed for the sparse half) | ✅ |
| GraphRAG | Claude (Pro) preferred | ⚠️ `qwen3:8b` can do entity/relation extraction, weaker on nuanced graphs |
| Multi-hop RAG | Claude (Pro) preferred | ⚠️ workable locally, less reliable across many hops |
| Self-RAG / Corrective RAG | Claude (Pro) preferred | ⚠️ self-evaluation is weaker when the same model grades itself |
| Adaptive RAG | Ollama `qwen3:4b` router → `qwen3:8b` | ✅ |
| Agentic RAG | Claude Agent SDK (Pro) preferred | ⚠️ functional with `qwen3:8b` tool calling, weaker autonomous planning |

## Layer 4 — Compound systems & workflows

| Entity | Engine | Stack coverage |
|---|---|---|
| Compound AI System | N/A — umbrella | ✅ |
| Prompt Chaining | Ollama — `qwen3:8b` | ✅ |
| Routing | Ollama — `qwen3:4b` | ✅ |
| Parallelization | Claude API (true concurrency) | ⚠️ **correction:** the *pattern* (sample-and-vote, sectioning) runs fine locally — you just lose the wall-clock speed benefit since one 6GB GPU serializes instead of running concurrently |
| Orchestrator-Workers | Claude Agent SDK (Pro) as lead | ⚠️ hand-rolled with `qwen3:8b` for both lead and workers — no separate specialized worker model unless you pull more |
| Evaluator-Optimizer | Claude (Pro) as evaluator | ⚠️ same-model self-critique (`qwen3:8b` grading `qwen3:8b`) is weaker than a separate stronger evaluator |

## Layer 5 — Agents

| Entity | Engine | Stack coverage |
|---|---|---|
| AI Agent | Claude Agent SDK (Pro) preferred | ✅ `qwen3:8b` + tool calling covers this directly |
| ReAct Agent | Claude Agent SDK (Pro) preferred | ✅ this is literally the pattern you've been hand-building |
| Planning Agent | Claude (Pro) preferred | ⚠️ weaker upfront planning depth |
| Tool-using Agent | Ollama — `qwen3:8b` | ✅ |
| Reflection / Self-critique Agent | Claude (Pro) preferred | ⚠️ same self-grading caveat as above |

## Layer 6 — Multi-agent systems

| Entity | Engine | Stack coverage |
|---|---|---|
| Single-Agent System | Ollama — `qwen3:8b` | ✅ |
| Multi-Agent System (MAS) | Claude Agent SDK (Pro, native subagents) | ⚠️ **correction:** doable via multiple `qwen3:8b` calls with different system prompts, but sequential not concurrent — only one model fits in your 6GB VRAM at a time |
| Orchestrator / Supervisor pattern | Claude Agent SDK (Pro, built-in) | ⚠️ same sequential constraint as MAS |
| Agentic AI | N/A — paradigm label | N/A |

## Layer 9 — Cross-cutting

| Entity | Engine | Stack coverage |
|---|---|---|
| MCP | Claude Code (native support) | ⚠️ **correction:** MCP is an open protocol — implementable with Ollama, but you'd hand-roll the client; no built-in Ollama support |
| A2A | N/A — not at your scale yet | ❌ not implemented, not needed yet |
| Related protocols (ACP, ANP) | N/A — watch, don't adopt | N/A |
| Human-in-the-loop (HITL) | N/A — design choice | ✅ trivial to add to any hand-rolled loop |
| Agent / orchestration frameworks | Claude Agent SDK, or **OpenCode** | ✅ OpenCode is open-source and works directly with Ollama — worth highlighting given your goal |

## Layer 10 — Product categories

| Entity | Engine | Stack coverage |
|---|---|---|
| Chatbot / Conversational AI | Ollama — `qwen3:8b` | ✅ |
| Copilot | Ollama `qwen3:8b` + OpenCode | ✅ |
| AI Assistant | Ollama — `qwen3:8b` | ✅ |
| Vertical / Domain agent | Claude Agent SDK (Pro) preferred | ⚠️ MAS constraint underneath applies |

---

## Summary

- **Genuinely uncoverable with current stack (❌):** only two — **Fine-tuning/Adapted Models** (hardware) and **A2A** (not implemented, not yet needed). Everything else is at least ⚠️ partially buildable today.
- **Where Claude is doing real work, not just convenience:** anything needing strong multi-step planning, self-evaluation, or graph/nuanced reasoning — GraphRAG, Multi-hop RAG, Self-RAG, Agentic RAG, Planning/Reflection agents. Local models get you a working version, just a weaker one.
- **Hardware, not model choice, is the real ceiling on Layer 6** — MAS and orchestrator patterns are conceptually fine locally, they just can't run concurrently on one 6GB GPU.

## Is anything missing from the taxonomy itself?

A few AI-engineering-relevant system types aren't explicit entities in the source doc — worth knowing even though I haven't added them to your reference file (that's a maintained working doc with its own version history, not mine to edit unprompted):

- **Evaluation/benchmarking systems** (LLM-as-judge harnesses, eval pipelines) — touched by "Evaluator-Optimizer" as a workflow pattern, but not called out as its own system category
- **Fine-tuning/training pipelines as systems** (not just "fine-tuned model" as a Layer-0 artifact) — the pipeline itself (data prep → train → eval loop) isn't a listed entity
- **Model serving/inference infrastructure** — Ollama itself is an instance of this, but "local/self-hosted inference server" isn't named anywhere in the taxonomy
- **Observability/cost-tracking systems** — logging, tracing, token-spend monitoring for AI systems in production

Want me to flag these back to you as candidate additions if you ever revise the source taxonomy, or leave it as-is?
