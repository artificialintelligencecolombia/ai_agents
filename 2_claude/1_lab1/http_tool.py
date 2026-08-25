from claude_agent_sdk import (
    tool, create_sdk_mcp_server, query, ClaudeAgentOptions,
    AssistantMessage, ResultMessage,
)
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import httpx
import asyncio
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

MAX_CHARS = 8000  # cap extracted text so we don't blow the context window

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())[:MAX_CHARS]

@tool("http_get", "Fetch a URL and return its cleaned, readable text content", {"url": str})
async def http_get(args):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(args["url"], timeout=10)
    text = extract_text(resp.text)
    return {"content": [{"type": "text", "text": f"Status {resp.status_code}\n\n{text}"}]}

server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[http_get])

options = ClaudeAgentOptions(
    mcp_servers={"my-tools": server},
    allowed_tools=["mcp__my-tools__http_get", "WebFetch"],
    permission_mode="acceptEdits",
)

URL = "https://www.anthropic.com/news"
QUESTION = "What are the main announcements on this page?"

async def main():
    prompt = f"Fetch {URL}, then answer based only on that content: {QUESTION}"
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
