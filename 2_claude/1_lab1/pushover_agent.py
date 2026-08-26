from claude_agent_sdk import (
    tool, create_sdk_mcp_server, query, ClaudeAgentOptions,
    AssistantMessage, ResultMessage,
)
from dotenv import load_dotenv
from typing import Any
import asyncio
import httpx
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
pushover_user = os.environ["PUSHOVER_USER"]
pushover_token = os.environ["PUSHOVER_API_TOKEN"] 
pushover_url = "https://api.pushover.net/1/messages.json"

@tool("send_push", "Send a message to the user", {"message": str})
async def push_message(args: dict[str, Any]) -> None:
    """Sends a given message to the user as a notification"""
    message = args["message"]
    async with httpx.AsyncClient() as client:
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        resp = await client.post(pushover_url, data=payload, timeout=10)
    data = resp.json()
    print(data)
    return {"content": [{"type": "text", "text": f"Message sent to user"}]}

server = create_sdk_mcp_server(
    name="fx-tools",
    version="1.0.0",
    tools=[push_message])

options = ClaudeAgentOptions(
    mcp_servers={"fx-tools": server},
    allowed_tools=["mcp__fx-tools__push_message"],
    permission_mode="bypassPermissions",
)

async def main():
    prompt = "Send a message to the user"
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}({block.input})")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())