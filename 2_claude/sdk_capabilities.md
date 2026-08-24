# Claude Agent SDK — Capabilities & Framework

## Beyond basic tools
- Orchestration: subagents (`Agent`/`Task`), `Workflow`
- Persistence: `resume`/`continue_conversation`, CLAUDE.md memory
- Integration: external MCP servers, hooks (Pre/PostToolUse, Stop)
- Control: `task_budget`, `max_budget_usd`, `max_turns`, `permission_mode`
- Observability: `get_context_usage()`, OTEL tracing
- Output: `include_partial_messages`, `structured_output`

## Domains (fundamentals)
- **API** — interface a program calls to use another program's logic
- **HTTP** — request/response protocol most APIs run over
- **cURL** — CLI tool sending raw HTTP requests
- **JSON** — data format for API payloads and tool schemas
- **MCP** — protocol connecting AI apps to external tools/data ("USB-C for AI")

## Details
- **SDK** — a library that wraps an API/CLI with ergonomic code
- **JSON-RPC** — wire format MCP servers use (SDK↔CLI itself uses plain stdio, not this)
- **stdio/subprocess** — how `claude_agent_sdk` talks to the `claude` CLI process

## Meta layers
- **Agent loop** — call model → get tool_use → run tool → return result → repeat
- **Context window** — the token space a model reasons within; `task_budget` bounds it

## Confirms
`@tool` wraps any Python function (HTTP/cURL call, SDK client, CLI wrapper) into an MCP tool, run in-process via `create_sdk_mcp_server()`.
