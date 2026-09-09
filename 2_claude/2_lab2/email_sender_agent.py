from dotenv import load_dotenv
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from typing import Dict
import resend
import os
import asyncio

load_dotenv(override=True)
resend.api_key = os.environ["RESEND_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

# Create a function to send emails using the Resend API
def send_email(email_list: list) -> None:
    for r in email_list:
        r = resend.Emails.send({
            "from": "hola@mail.aicolombia.io",
            "to": ["damarias991@gmail.com"],
            "reply_to": "damarias991@gmail.com",
            "subject": "test",
            "html": "<p>hello</p>",
        })
        print(r)
@tool("send_email", "Send emails to a list of emails", {"email_list": list})
async def send_email_tool(args) -> dict:
    send_email(args["email_list"])
    return {"content": [{"type": "text", "text": "Sent"}]}

server = create_sdk_mcp_server(
    name="fx-tools",
    version="1.0.0",
    tools=[send_email_tool])

options = ClaudeAgentOptions(
    mcp_servers={"fx-tools": server},
    allowed_tools=["mcp__fx-tools__send_email_tool"],
    permission_mode="bypassPermissions",
)
async def main():
    prompt = "Send a email to the user damarias..."
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text) # type: ignore
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}({block.input})") # type: ignore
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())