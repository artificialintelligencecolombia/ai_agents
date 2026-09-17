from dotenv import load_dotenv
from typing import Any
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions, AssistantMessage, ResultMessage
from anthropic import AsyncAnthropic
import asyncio
import os

# Environment variables
load_dotenv(override=True)
#resend.api_key = os.environ["RESEND_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
email_list = os.environ.get("EMAIL_LIST", "").split(",")  # Get the email list from environment variable
model = "claude-haiku-4-5-20251001"

# Prompts
system_prompt1 = "You are a sales agent working for AI Colombia, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

system_prompt2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

system_prompt3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

@tool("agent1", "Craft professional cold emails", {"topic": str}) # type: ignore
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
    
server = create_sdk_mcp_server(
    name="tools",
    version="1.0.0",
    tools=[agent1_tool])

options = ClaudeAgentOptions(
    system_prompt="You are an email writer. Call your agent1 tool to craft professional cold emails.",
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__agent1"],
    permission_mode="bypassPermissions",
)
async def main():
    prompt = f"Craft an email"
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