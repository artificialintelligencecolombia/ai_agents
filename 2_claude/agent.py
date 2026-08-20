# Import libraries
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from dotenv import load_dotenv
import asyncio
import os

# Import API creds
load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt="Give me 5 finance and budgeting tips based on the most recent 2026 expert articles. Search the web first and cite your sources.",
        options=ClaudeAgentOptions(
            allowed_tools=[ "WebSearch"],  # Auto-approve these tools
            permission_mode="acceptEdits",  # Auto-approve file edits
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())