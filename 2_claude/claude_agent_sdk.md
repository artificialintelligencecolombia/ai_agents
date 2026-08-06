# Anthropic Python SDK

- Provides access to antrophic's REST API from python apps
- It supports:

1. synchronous and asynchronous requests
2. streaming
3. Integratons (Amazon  Bedrock, Claude on AWS, Google cloud, etc)

https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python

## Terminology

- **Agent**: a script, an app composed of an LLM with system prompt and tools, that can be used to perform tasks.

## Agentic AI steps

1. Create an instance of the `Agent` class, providing a system prompt and tools.
2. Use `with trace()` to trace the agent's execution.
3. Call the `agent.run()` method to execute the agent and get the result. 

## Coding agents

1. Invest time in the prompts, be precise about the task and the expected output. Demand conciseness
2. Start simple with the task for the agent, and then iterate to make it more complex.
3. Work incrementally, test constantly, validate success criteria
4. Challenge it, demand evidence, ask for reasoning, ask for multiple solutions, ask for pros and cons, ask for a final recommendation.

## Claude SDK

An Agent SDK is a code-first orchestration library — a vendor-native toolkit developers use to programmatically build and run agents (define tools, manage the reasoning/tool-call loop, handle multi-step execution), as opposed to a no-code builder, a managed runtime, or an end-user product.

SDK agents exist for developers who need agent behavior as a component inside something bigger they're shipping.

https://code.claude.com/docs/en/agent-sdk/overview

## Claude API vs Claude Agent SDK

https://www.mindstudio.ai/blog/what-is-claude-agent-sdk-vs-claude-api