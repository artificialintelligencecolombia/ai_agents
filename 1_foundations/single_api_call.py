import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY2"),
)

message = client.messages.create(
    max_tokens=128,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-opus-5",
)

for block in message.content:
    if block.type == "text":
        print(block.text)