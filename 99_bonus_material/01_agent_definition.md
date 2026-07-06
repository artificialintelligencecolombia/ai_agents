# Agent

An AI Agent is a program where LLM outputs control the workflow

## AI Solution

Any of the following is considered an AI solution:

- Multiple LLM calls
- LLMs with the ability to use tools
- Environment where LLMs interact
- A planner (AI) to coordinate activities
- Autonomy: give some ability to an LLM to control the order of happenning things and what will happen

## Agentic systems

Agentic systems can be distinguished in 2 types:

1. Workflows where LLMs and tools are orchestrated through predefined code paths

2. Agents are systems where LLMs dynamically direct their own processes and tools usage, maintaining control over how they accomplish tasks

## Orchestrating LLMs

It consists in chaining LLMs, so the output of one LLM is the input of another. This can be done in: a linear way or in a more complex way, where the output of one LLM can be used to decide which LLM to call next.

## AI Agents tools

- n8n
- elevenlabs
- OpenAI Agent Builder
- Crew AI Studio