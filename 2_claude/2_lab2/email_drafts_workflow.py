from dotenv import load_dotenv
import os
import asyncio
from anthropic import AsyncAnthropic


load_dotenv(override=True)
# resend.api_key = os.environ["RESEND_API_KEY"]
#os.environ["ANTHROPIC_API_KEY"] = os.environ["ANTHROPIC_API_KEY2"]
api_key = os.environ["ANTHROPIC_API_KEY2"]

model = "claude-haiku-4-5-20251001"

system_prompt1 = "You are a sales agent working for AI Colombia, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

system_prompt2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

system_prompt3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

messages=[{
    "role": "user",
    "content": "Write a short email",
    }]

'''
async marks a function as one that can pause and wait 
for something slow (like a network call) without 
freezing everything else.
'''
async def write_email(system_prompt):
    client = AsyncAnthropic(api_key=api_key) 
    message = await client.messages.create( # 
        model=model,
        system=system_prompt,
        max_tokens=1000,
        messages=messages,
        )
    for block in message.content:
        if block.type == "text":
            print(block.text)


'''
This is orchestration, not an agent: the sequence (call all 3,
always, in parallel, then stop) is fixed by this Python code.
No LLM decides which sub-agent to call, when, or how many times -
that decision-making is what would make it an agent instead.
'''
async def main():
    await asyncio.gather( # future object that will hold the results of the concurrent tasks
        write_email(system_prompt1), # concurrent tasks
        write_email(system_prompt2),
        write_email(system_prompt3),
    )

asyncio.run(main())

'''
await is the actual "pause here" instruction — it says 
"wait for this slow thing to finish, then continue."
'''

# You can only use await inside a function marked async def. 
# That's the whole rule.