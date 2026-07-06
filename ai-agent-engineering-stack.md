# The AI Agent Engineering Stack

A comprehensive, categorized map of the technologies, frameworks, platforms, and products that make up the current AI agent landscape (mid-2026).

---

## 1. Foundation Models
The reasoning core every agent is built on.

- **Claude** (Opus, Sonnet, Haiku) – Anthropic
- **GPT-5.x / o-series** – OpenAI
- **Gemini 3** – Google DeepMind
- **Llama 4** – Meta (open-weight)
- **Mistral Large / Mixtral** – Mistral AI (open-weight)
- **DeepSeek V3/R1** – DeepSeek (open-weight, strong reasoning)
- **Grok** – xAI

---

## 2. Frameworks (Code-First Orchestration)
Libraries and SDKs developers use to build custom agents and multi-agent systems.

### General-purpose
- **LangGraph** – Graph-based framework for durable, stateful, multi-step agent workflows
- **LangChain** – Modular chains/components for LLM app development
- **CrewAI** – Role-based multi-agent orchestration framework
- **Microsoft Agent Framework** – Unified successor to Semantic Kernel + AutoGen; native MCP support, A2A (beta)
- **LlamaIndex Workflows** – Agentic workflows built on LlamaIndex's data/RAG foundation
- **Pydantic AI** – Type-safe agent framework for Python/FastAPI teams
- **Haystack Agents** (deepset) – Pipeline-based agent orchestration, evolved from RAG
- **AutoGen / AG2** – Multi-agent conversation framework (legacy AutoGen v0.2 fork, still used in research)
- **Rasa** – Open-source framework for private, self-hosted conversational agents
- **FastAgency** – Lightweight framework for deploying multi-agent workflows to production
- **Semantic Kernel** – Microsoft's earlier agent SDK (superseded by Microsoft Agent Framework)

### Vendor-native SDKs
- **OpenAI Agents SDK / Responses API** – OpenAI's toolkit for building and orchestrating agents
- **Google ADK (Agent Development Kit)** – Open-source, code-first framework (Python, Java, Go, Kotlin); powers Vertex AI Agent Builder
- **Claude Agent SDK** – Anthropic's SDK (renamed from Claude Code SDK) with hierarchical subagent spawning

---

## 3. Builders (No-Code / Low-Code)
Visual or drag-and-drop tools for building agents without heavy engineering.

### General agent/workflow builders
- **n8n** – Visual workflow automation with AI agent nodes, self-hostable
- **Dify** – Open-source visual builder for LLM apps and agents
- **Make** – Visual automation platform with AI agent capabilities
- **Zapier Agents** – Agent builder integrated into Zapier's automation ecosystem
- **Lindy** – No-code platform for business-automation agents
- **Gumloop** – Visual automation builder for AI-powered workflows
- **AutoGPT** – Open-source autonomous agent builder with visual workflows
- **OpenAI Agent Builder** – OpenAI's no-code agent creation platform
- **CrewAI Studio** – No-code interface layered on the CrewAI framework

### Voice-specific builders
- **ElevenLabs** – Voice generation, cloning, and conversational agent platform
- **Vapi** – Developer platform for building real-time voice AI agents
- **Synthflow** – No-code voice agent builder for business calling

---

## 4. Runtimes (Managed Execution & Scaling)
Where agents are deployed, scaled, and governed in production.

- **AWS Bedrock AgentCore** – Amazon's dedicated managed runtime for production agents
- **Vertex AI Agent Engine** – Google's managed agent runtime (now part of the rebranded Gemini Enterprise Agent Platform); handles sessions, memory, observability, governance
- **Microsoft Agent Framework Runtime / Azure AI Foundry** – Runtime with task-adherence guardrails, PII protection, and prompt-injection defense
- **Generic compute** (agent-agnostic, used to self-host agents): AWS Lambda, Cloud Run, GKE/Kubernetes, Azure Container Apps

---

## 5. Products (End-User Agentic Applications)
Finished, user-facing agent products — not frameworks you build with, but tools you use directly.

### Anthropic
- **Claude Code** – CLI-based agentic coding tool
- **Claude Cowork** – Agentic desktop app for non-coding knowledge work (files, docs, spreadsheets)
- **Claude in Chrome** – Browser automation agent
- **Claude in Excel / PowerPoint** – Spreadsheet and slides agents

### Other vendors
- **ChatGPT Agent** – OpenAI's task-executing agent
- **Devin AI** – Autonomous AI software engineer
- **Perplexity Computer** – Multi-model orchestration agent
- **Manus** – Autonomous task-execution agent
- **Google Antigravity** – Agent-first development platform

### Enterprise platforms
- **Salesforce Agentforce 360** – Enterprise agent platform for CRM workflows
- **Microsoft Copilot Studio / Microsoft 365 Agents** – Enterprise agent builder integrated with Microsoft 365
- **AWS Bedrock Agents** (build layer, distinct from AgentCore runtime)
- **Vertex AI Agent Builder** – Google's enterprise agent build suite (ADK + Agent Studio + Agent Garden + Agent Engine)

> **Note on unverified/miscategorized items:** "OpenClay" is not an Anthropic product — it refers to unrelated small third-party open-source projects and is not a comparable "product" to Claude Code. "Claude Design" is not confirmed in Anthropic's own documentation as of this writing; treat as unverified until officially announced.

---

## 6. Protocols (Interoperability Layer)
Standards enabling agents to talk to tools, data, and each other.

- **MCP (Model Context Protocol)** – Standard for connecting agents to external tools and data sources
- **A2A (Agent2Agent)** – Emerging protocol for direct agent-to-agent communication (beta support in Microsoft Agent Framework, Google ADK)

---

## 7. Voice & Multimodal Infrastructure
Speech and real-time conversational infrastructure for voice agents.

- **ElevenLabs** – Voice generation/cloning, strong for studio-grade content
- **Cartesia** – Low-latency (~90ms) TTS with a dedicated voice-agent platform ("Line")
- **Deepgram** – Combined STT+TTS API optimized for real-time agents
- **Inworld AI** – Top-ranked TTS/STT for real-time interactive AI
- **PlayHT** – TTS with strong multilingual/telephony support
- **Twilio Voice** – Programmable telephony infrastructure
- **Amazon Lex** – AWS conversational interface builder with NLU
- **Chatterbox / Kokoro** – Open-source TTS models (self-hostable)

---

## 8. Memory, RAG & Data Layer
How agents store, retrieve, and ground knowledge.

- **Vector databases**: Pinecone, Weaviate, Qdrant, Chroma, Milvus
- **Memory services**: Vertex AI Memory Bank, Zep, Mem0
- **Retrieval frameworks**: LlamaIndex (core), Haystack (core), LangChain retrievers

---

## 9. Observability, Evaluation & Guardrails
Monitoring, testing, and safety layers for agents in production.

- **LangSmith** – Tracing and evaluation for LangChain/LangGraph agents
- **Arize** – ML/LLM observability platform
- **Braintrust** – Evaluation and experimentation platform for LLM apps
- **Azure AI Foundry guardrails** – Task-adherence checks, PII protection, prompt-injection defense
- **Cloud-native observability**: Google Cloud Trace/Monitoring/Logging, AWS CloudWatch (for agents deployed on respective clouds)

---

## Summary Table

| Layer | Purpose | Examples |
|---|---|---|
| Foundation Models | Reasoning core | Claude, GPT-5.x, Gemini 3, Llama 4 |
| Frameworks | Code-first orchestration | LangGraph, CrewAI, Google ADK, MS Agent Framework |
| Builders | No-code creation | n8n, Dify, Lindy, OpenAI Agent Builder |
| Runtimes | Managed execution at scale | Bedrock AgentCore, Vertex AI Agent Engine |
| Products | End-user agentic apps | Claude Code, Claude Cowork, ChatGPT Agent, Devin |
| Protocols | Interoperability | MCP, A2A |
| Voice Infra | Speech & real-time conversation | ElevenLabs, Cartesia, Deepgram |
| Memory/RAG | Knowledge storage & retrieval | Pinecone, Weaviate, Mem0 |
| Observability | Monitoring & guardrails | LangSmith, Arize, Braintrust |

---

*Compiled mid-2026. This landscape moves fast — verify vendor-specific details (pricing, GA status, naming) against official docs before treating any entry as final.*
