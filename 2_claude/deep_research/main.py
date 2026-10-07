from anthropic import AsyncAnthropic
from typing import Any
from dotenv import load_dotenv
import asyncio
import os
import resend
from pydantic import BaseModel, Field
from datetime import date
from claude_agent_sdk import client, query, ClaudeAgentOptions, AssistantMessage, ResultMessage

# Load environment variables from .env file
load_dotenv(override=True)
ANTHROPIC_API_KEY2= os.environ.get("ANTHROPIC_API_KEY2")
os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
HOW_MANY_SEARCHES = 3
CURRENT_DATE = date.today().isoformat()
EMAIL_LIST = os.environ.get("EMAIL_LIST", "").split(",")
model = "claude-haiku-4-5-20251001"


client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY2)

# Prompts
planner_prompt = f"""You are a search planner. You will be given a research query. \
Your task is to write web search queries that together best answer it. You do not run the searches.
- Output: exactly {HOW_MANY_SEARCHES} search queries.
- Each query: 3–10 words, specific, covering a different angle (no near-duplicates).
- Today is {CURRENT_DATE}; include the year when recency matters.
- If the query is vague, cover its most likely interpretations.
- No intro, no outro."""

researcher_prompt = f"""You are a web researcher. Today is {CURRENT_DATE}. \
You will be given a search term and a reason for searching. \
Your task is to perform a web search and return the most relevant information."""

report_writer_prompt = """You are a report writer. \
    Your task is to write a short, concise one-page report summarizing the findings over a search topic. \
    Read the original topic and its search results carefully to create a cohesive, well-structured report in Markdown format. \
    Draft the title of the report, make it short, descriptive, and attention-grabbing. \
    You will be provided with the original query and the search results. \
    The report must not exceed 250 words.
    Draft the report only, do not include any other text."""

# Output data models
class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search matters for the topic")
    query: str = Field(description="The search term to use")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]

class ReportData(BaseModel):
    title : str = Field(description="The title of the report, short, descriptive, and attention-grabbing.")
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")



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

async def draft_report(query:str, search_results: list[Any]) -> ReportData:
    """ Draft a report based on the original query and the search results."""
    response = await client.messages.parse( #type: ignore
        model=model,
        system=report_writer_prompt,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Original query: {query}\nSearch results: {search_results}",
            }
        ],
        output_format=ReportData,
    )
    return response.parsed_output

async def send_email_tool(report: ReportData) -> dict[str, Any]:
    try:
        await asyncio.to_thread(resend.Emails.send, {
                "from": "hola@mail.aicolombia.io",
                "to": EMAIL_LIST[0], # args["to"],
                "reply_to": EMAIL_LIST[0],
                "subject": report.title,
                "html": report.markdown_report.replace("\n", "<br>"),
            })
        return "Sent email successfully"
    except Exception as e:
        return {"error": str(e)} 

async def main() -> None:
    user_input = input("Enter a topic for research: ")
    result = await plan_searches({"topic": user_input})
    print("SEARCH PLAN:")
    print(result, "\n\n")
    search_results = await asyncio.gather(*(perform_search(search) for search in result.searches))
    print("RESULTS:")
    print(search_results, "\n\n")
    report = await draft_report(user_input, search_results)
    print("REPORT:")
    print(report, "\n\n")
    print (type(report))
    print("EMAILING:")
    email_result = await send_email_tool(report)
    print(email_result)
asyncio.run(main())

# The agent is a fixed-control flow pipeline, not agent decide.
# search_planner → web_researcher (parallel) → report_drafter → send_email