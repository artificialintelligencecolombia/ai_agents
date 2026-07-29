# Recipe Builder Agent

## Overview

A from-scratch implementation of an Anthropic tool-use agent loop: given a chef system prompt and a message about available ingredients, Claude calls tools to build up a recipe.

**Notebook:** `5_extra_recipe_builder.ipynb`

"Canonical" here means **correct per the Anthropic Messages API tool-use contract** — not a copy of any other notebook's structure. The checklist below is derived directly from Anthropic's docs, not from a sibling project.

## Anthropic tool-use contract (what "correct" means)

Reference: [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls), [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)

| Requirement | Rule |
|---|---|
| Loop exit | Stop when `response.stop_reason != "tool_use"` |
| Message history | `messages` is a single persistent list, mutated across turns — never rebuilt from scratch each iteration |
| Assistant turn | `response.content` (may contain `text` + `tool_use` blocks) appended with `role: "assistant"` — `tool_use` blocks are only valid inside assistant messages |
| Tool dispatch | Resolve `tool_use.name` → callable, call it with `tool_use.input` unpacked as kwargs |
| `tool_result` shape | `{"type": "tool_result", "tool_use_id": <id>, "content": <string or content blocks>}` |
| `tool_result` placement | Wrapped in one `role: "user"` message; `tool_result` blocks must come **before** any other text in that message's content array |
| `tool_result` ordering | Must immediately follow the corresponding assistant `tool_use` message — no messages in between |

## Current implementation status

| Requirement | Status |
|---|---|
| Loop exit on `stop_reason` | ✅ implemented (`else: break`) |
| Tool dispatch (`globals().get(name)`) | ✅ implemented — generic, works for any number of tools |
| `tool_result` dict shape | ✅ correct (`type`, `tool_use_id`, `content` as string) |
| Persistent `messages` list | ❌ not implemented — rebuilt identically every loop pass |
| Assistant turn appended to `messages` | ❌ not implemented |
| `tool_result` turn appended to `messages` | ❌ not implemented — `tool_results` is computed and discarded |

**Net effect of the two ❌ items:** the loop can detect a tool call and execute it, but Claude is never told the result, so it cannot use it or continue reasoning. The dispatch and exit-condition work done so far has no way to feed back into the conversation yet.

## Next step

Move `messages = [...]` above the `while` loop (built once). Inside the loop, after computing `tool_results`, append:
1. The assistant's turn: `role: "assistant"`, `content: response.content`.
2. The tool outcome: `role: "user"`, `content: tool_results`.

Then re-call `claude.messages.create(messages=messages, ...)` using the updated list, not a hardcoded prompt.

## Key lessons learned

- `globals().get(tool_name)` resolves a tool's string name to its callable — the mechanism that makes dispatch generic across any number of tools. Resolving and calling are two separate steps: `globals().get(tool_name)` returns the function; `(**tool_input)` calls it.
- A `tool_result`'s `content` must satisfy the API's string/content-block requirement — a Python object like a list needs converting (e.g. `str(result)`) first.
- Mutable global state (e.g. an ingredients list) persists across Jupyter cell re-runs. Resetting it must happen once per run, not inside the tool function — putting the reset inside the tool discards accumulation instead of fixing duplication.
- `while True` with no `break` is an infinite loop regardless of what happens inside it — the exit condition must be checked and acted on every iteration.
