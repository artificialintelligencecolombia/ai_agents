from dotenv import load_dotenv
from typing import Any
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions, AssistantMessage, ResultMessage
from anthropic import AsyncAnthropic
import resend
import asyncio
import os

# Environment variables
load_dotenv(override=True)
#resend.api_key = os.environ["RESEND_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
email_list = os.environ.get("EMAIL_LIST", "").split(",")  # Get the email list from environment variable
model = "claude-haiku-4-5-20251001"
linkedin_url = os.environ.get("LINKEDIN_URL")  # Get the LinkedIn URL from environment variable
sender_name = "AI COLOMBIA"

# Prompts
system_prompt1 = "You write professional, warm outreach emails for someone reaching out to make a genuine personal connection."

system_prompt2 = "You write witty, engaging outreach emails for someone reaching out to make a genuine personal connection, likely to get a response."

system_prompt3 = "You write concise, to the point outreach emails for someone reaching out to make a genuine personal connection."

@tool("agent1", "Craft professional cold emails", {"topic": str, "sender_name": str, "linkedin_url": str}) # type: ignore
async def agent1_tool(args) -> dict[str, Any]:
    try:
        client = AsyncAnthropic() 
        message = await client.messages.create( # 
            model=model,
            system=system_prompt1,
            max_tokens=200,
            messages=[{"role": "user", "content": args["topic"]}],
            )
        text = "".join(block.text for block in message.content if block.type == "text")
        return {"content": [{"type": "text", "text": text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Failed to craft email: {str(e)}"}],
                "is_error": True}

@tool("agent2", "Craft friendly, engaging emails", {"topic": str, "sender_name": str, "linkedin_url": str}) # type: ignore
async def agent2_tool(args) -> dict[str, Any]:
    try:
        client = AsyncAnthropic() 
        message = await client.messages.create( # 
            model=model,
            system=system_prompt2,
            max_tokens=200,
            messages=[{"role": "user", "content": args["topic"]}],
            )
        text = "".join(block.text for block in message.content if block.type == "text")
        return {"content": [{"type": "text", "text": text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Failed to craft email: {str(e)}"}],
                "is_error": True}

@tool("agent3", "Craft short, simple emails", {"topic": str, "sender_name": str, "linkedin_url": str}) # type: ignore
async def agent3_tool(args) -> dict[str, Any]:
    try:
        client = AsyncAnthropic() 
        message = await client.messages.create( # 
            model=model,
            system=system_prompt3,
            max_tokens=200,
            messages=[{"role": "user", "content": args["topic"]}],
            )
        text = "".join(block.text for block in message.content if block.type == "text")
        return {"content": [{"type": "text", "text": text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Failed to craft email: {str(e)}"}],
                "is_error": True}

@tool("send_email", "Send email to a list of emails", {"to": str, "subject": str, "message": str})
async def send_email_tool(args) -> dict[str, Any]:
    try:
        await asyncio.to_thread(resend.Emails.send, {
                "from": "hola@mail.aicolombia.io",
                "to": args["to"],
                "reply_to": email_list[0],
                "subject": args["subject"],
                "html": args["message"].replace("\n", "<br>"),
            })
        return {"content": [{"type": "text", "text": f"Sent to {args['to']}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Failed to send email to {args['to']}: {str(e)}"}],
                "is_error": True} 

server = create_sdk_mcp_server(
    name="tools",
    version="1.0.0",
    tools=[agent1_tool, agent2_tool, agent3_tool, send_email_tool])

options = ClaudeAgentOptions(
    system_prompt=F"You are an email writer. Call your agent1, agent2, and agent3 tools to craft professional, friendly and short emails. \
        When calling the agent tools, pass sender_name: {sender_name} and linkedin_url: {linkedin_url} as arguments. \
        Select the best email draft and send it to {email_list[0]}.",
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__agent1", "mcp__tools__agent2", "mcp__tools__agent3", "mcp__tools__send_email"],
    permission_mode="bypassPermissions",
)
async def main():
    prompt = f"Craft an email inviting to connect on Linkedin with a unique greeting message. Send the best candidate email to the user"
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