from dotenv import load_dotenv
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from typing import Any 
import resend
import os
import asyncio

load_dotenv(override=True)
resend.api_key = os.environ["RESEND_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
email_list = os.environ.get("EMAIL_LIST", "").split(",")  # Get the email list from environment variable

@tool("send_email", "Send emails to a list of emails", {"to": str, "subject": str, "message": str})
async def send_email_tool(args) -> dict[str: Any]:
    try:
        await asyncio.to_thread(resend.Emails.send, {
                "from": "hola@mail.aicolombia.io",
                "to": args["to"],
                "reply_to": email_list[0],
                "subject": args["subject"],
                "html": args["message"],
            })
        return {"content": [{"type": "text", "text": f"Sent to {args['to']}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Failed to send email to {args['to']}: {str(e)}"}],
                "is_error": True}   

server = create_sdk_mcp_server(
    name="tools",
    version="1.0.0",
    tools=[send_email_tool])

options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__send_email"],
    permission_mode="bypassPermissions",
)
async def main():
    prompt = f"Send exactly one email to the users of {', '.join(email_list)} with a unique greeting message"
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