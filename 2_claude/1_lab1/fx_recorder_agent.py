from claude_agent_sdk import (
    tool, create_sdk_mcp_server, query, ClaudeAgentOptions,
    AssistantMessage, ResultMessage,
)
from dotenv import load_dotenv
from datetime import datetime, timezone
import httpx
import asyncio
import csv
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]

CSV_PATH = os.path.join(os.path.dirname(__file__), "fx_rates.csv")

@tool("fetch_cop_usd_rate", "Fetch the current COP/USD exchange rate", {})
async def fetch_cop_usd_rate(args):
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://open.er-api.com/v6/latest/USD", timeout=10)
    data = resp.json()
    rate = data["rates"]["COP"]
    return {"content": [{"type": "text", "text": f"1 USD = {rate} COP"}]}

@tool("record_rate", "Append a timestamped exchange rate to the CSV log", {"rate": float})
async def record_rate(args):
    is_new = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "usd_to_cop"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), args["rate"]])
    return {"content": [{"type": "text", "text": f"Recorded {args['rate']} to {CSV_PATH}"}]}

server = create_sdk_mcp_server(
    name="fx-tools",
    version="1.0.0",
    tools=[fetch_cop_usd_rate, record_rate])

options = ClaudeAgentOptions(
    mcp_servers={"fx-tools": server},
    allowed_tools=["mcp__fx-tools__fetch_cop_usd_rate", "mcp__fx-tools__record_rate"],
    permission_mode="acceptEdits",
)

async def main():
    prompt = "Fetch the current COP/USD exchange rate and record it in the CSV log."
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
