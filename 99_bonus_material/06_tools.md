# Tools

It consists into giving LLMs new abilities.

User request → LLM receives conversation + list of available tools → LLM decides a tool is needed and outputs a structured call (tool name + arguments) → application code (not the LLM) executes the tool with those arguments → code captures the tool's result → result is appended to the conversation as a tool-result message → LLM is called again with that result included → LLM generates the final natural-language response (or requests another tool call, looping back to the execution step)

## Tool Calling diagram

User ──> Software ──> LLM
             ↑           │
             │           │ "call tool X with args Y"
             │           ▼
             │        Software ──> Tool (executes)
             │           │
             │           ▼
             └──── result back to LLM ──> final answer ──> User