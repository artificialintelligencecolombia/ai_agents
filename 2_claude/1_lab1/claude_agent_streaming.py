# Import libraries
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

async def main():
    async for message in query(
        prompt="Give 5 product ideas for creating a business model as AI Engineer.",
        options=ClaudeAgentOptions(
            allowed_tools=["WebFetch", "WebSearch"],
            permission_mode="acceptEdits",  # Auto-approve these tools
        )
    ):
        if isinstance(message, AssistantMessage): # AssistantMessage can contain multiple blocks (thoughts, tool calls, etc.)
            # print("Assistant message:", message.blocks)
            for block in message.content:
                if hasattr(block, "text"):
                    print("Thought:", block.text) # Claude's reasoning
                elif hasattr(block, "name"):
                    print("Tool call:", block.name) # Claude's tool call
        elif isinstance(message, ResultMessage): # ResultMessage is the result of a tool call
            Console().print(message)
            # print("Result:", message.content) # Result of the tool call

asyncio.run(main())