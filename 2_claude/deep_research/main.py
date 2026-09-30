from anthropic import AsyncAnthropic
from typing import Any
from dotenv import load_dotenv
import asyncio
import os
from pydantic import BaseModel, Field
from datetime import date
from claude_agent_sdk import client, query, ClaudeAgentOptions, AssistantMessage, ResultMessage

# Load environment variables from .env file
load_dotenv(override=True)
ANTHROPIC_API_KEY2= os.environ.get("ANTHROPIC_API_KEY2")
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
# USE_EMAIL = True # Set to True to enable email sending, False to disable
HOW_MANY_SEARCHES = 3
CURRENT_DATE = date.today().isoformat()
model = "claude-haiku-4-5-20251001"

client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY2)

# Prompts
planner_prompt = f"""You are a search planner. You will be given a research query. \
Your task is to write web search queries that together best answer it. You do not run the searches.
- Output only: exactly {HOW_MANY_SEARCHES} search queries.
- Each query: 3–10 words, specific, covering a different angle (no near-duplicates).
- Today is {CURRENT_DATE}; include the year when recency matters.
- If the query is vague, cover its most likely interpretations.
- No intro, no outro."""

researcher_prompt = f"""You are a web researcher. Today is {CURRENT_DATE}. You will be given a search term and a reason for searching. \
Your task is to perform a web search and return the most relevant information."""

# Web search plan schema
class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search matters for the topic")
    query: str = Field(description="The search term to use")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]

# Async agent functions
async def plan_searches(args) -> WebSearchPlan:
    """ Generate a web search plan based on the user's topic and the cap of queries to generate."""
    response = await client.messages.parse( #type: ignore
        model=model,
        system=planner_prompt,
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": args["topic"],
            }
        ],
        output_format=WebSearchPlan,
    )
    return response.parsed_output

async def perform_search(item: WebSearchItem) -> Any:
    async for message in query(
        prompt=f"Search term: {item.query}\nReason for searching: {item.reason}",
        options=ClaudeAgentOptions(
            system_prompt=researcher_prompt,
            allowed_tools=["WebFetch", "WebSearch"],
        )
    ):
        if isinstance(message, AssistantMessage): # AssistantMessage can contain multiple blocks (thoughts, tool calls, etc.)
            for block in message.content:
                if hasattr(block, "text"):
                    print("Thought:", block.text) # Claude's reasoning
                elif hasattr(block, "name"):
                    print("Tool call:", block.name) # Claude's tool call
        elif isinstance(message, ResultMessage): # ResultMessage is the result of a tool call
            return message

async def main() -> None:
    user_input = input("Enter a topic for research: ")
    result = await plan_searches({"topic": user_input})
    print(result)
    await asyncio.gather(*(perform_search(search) for search in result.searches))

asyncio.run(main())

# The agent is a fixed-control flow pipeline, not agent decide.
# search_planner → web_researcher (parallel) → report_drafter → send_email