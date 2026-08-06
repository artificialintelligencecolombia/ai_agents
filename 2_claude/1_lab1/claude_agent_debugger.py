# Import libraries
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

async def main():
    # Agent loop: each iteration is one event (a thought, a tool call, a result) as Claude reasons → acts → reasons again, until it decides it's done.
    async for message in query(
        prompt="Review buggy.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],  # Auto-approve these tools
            permission_mode="acceptEdits",  # Auto-approve file edits
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