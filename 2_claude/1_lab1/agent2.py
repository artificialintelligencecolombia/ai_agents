from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock
from dotenv import load_dotenv
import asyncio
import os

# Import API creds
load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

MAX_OUTPUT_TOKNS = 199

# Simple query
async def main():
    async for message in query(
            prompt="Create one simple txt file with 3 fundamentals for success as entrepreneur. Each item is one phrase.",
            options=ClaudeAgentOptions(
                system_prompt="You are an ai assistant. MAX_OUTPUT TOKENS. Answer with deterministim and conciseness: {MAX_OUTPUT_TOKNS}.\
                    Do you have tools enabled?Y/N",
                max_turns= 6,
                # tools=[],
                allowed_tools=["Read", "Write", "Bash"],  # Auto-approve these tools
                permission_mode='acceptEdits'  # auto-accept file edits
            )    
        ):
        if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text)  # Claude's reasoning
                    else:
                        #print(type(block).__name__, block)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  

asyncio.run(main())