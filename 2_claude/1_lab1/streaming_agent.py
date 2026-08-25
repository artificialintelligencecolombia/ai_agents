from claude_agent_sdk import query, ClaudeAgentOptions, StreamEvent
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

async def main():
    async for message in query(
        prompt="Tell me a short joke.",
        options=ClaudeAgentOptions(include_partial_messages=True),
    ):
        if isinstance(message, StreamEvent):
            delta = message.event.get("delta", {})
            if delta.get("type") == "text_delta":
                print(delta["text"], end="", flush=True)

asyncio.run(main())
