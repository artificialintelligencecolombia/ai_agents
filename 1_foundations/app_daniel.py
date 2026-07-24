from dotenv import load_dotenv
from anthropic import Anthropic
import os
from pypdf import PdfReader
import gradio as gr

# Import env vars
load_dotenv(override=True)
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY2')
model_name = "claude-opus-4-6"

# Tools
# Description of requirements, must-to-have inputs, using context engineering
DEFAULT_NAME = "Name not provided"
DEFAULT_NOTES = "not provided"
def record_user_details(email: str, name: str=DEFAULT_NAME, notes: str=DEFAULT_NOTES) -> str:
    if not email:
        raise ValueError("Email required to record user details")
    with open("4_lab4_daniel/user_details.txt", "a", encoding="utf-8") as f:
        user = {
            "email": email,
            "name": name,
            "notes": notes,
        }
        f.write(f"{user}\n")
    return "User details stored"

record_user_details_tool = {
    "name": "record_user_details",
    "description": "Record the details of the user once he/she provides the email and sufficient information to record",
    "input_schema": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# Given context engineering, it detects -> extracts -> append -> unkwnown question
def record_unknown_question(question: str) -> str:
    if not question:
        raise ValueError("Question required to record unknown question")
    with open("4_lab4_daniel/unknown_questions.txt", "a", encoding="utf-8") as f:
        unknow_question = question
        f.write(f"{unknow_question}\n")
    return "Unknown question recorded"

record_unknown_question_tool = {
    "name": "record_unknown_question",
    "description": "Record any question that couldn't be answered as you didn't know the answer despite the context you have",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
    }
}

tools = [record_user_details_tool, record_unknown_question_tool]

# Class definition
class Clone:
    def __init__(self):
        self.antrophic = Anthropic()
        self.name = "Dani"
        self.model_name = ""
        reader = PdfReader("4_lab4_daniel/profile.pdf") # Context injection 1
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("4_lab4_daniel/summary.txt", "r", encoding="utf-8") as f: # Context injection 2
            self.summary = f.read()
    
    def system_prompt(self) -> str:
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
        particularly questions related to {self.name}'s career, background, skills and experience. \
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
        You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
        If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
        If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    # Dispatcher  — canonical, works for 1 or N tools
    def run_tool(self, name: str, tool_input: dict) -> str:
        if name == "record_user_details":
            return record_user_details(email=tool_input["email"],
                                    name=tool_input.get("name", DEFAULT_NAME),
                                    notes=tool_input.get("notes", DEFAULT_NOTES),
                                    ) # type: ignore
        if name == "record_unknown_question":
            return record_unknown_question(question=tool_input["question"])
        raise ValueError(f"Unknown tool: {name}")
    
    # Chat function (Gradio) with tool support
    def chat(self, message, history) -> str | None:
        # Chat logging (history)
        history = [{"role": h["role"], "content": h["content"]} for h in history] # Keep only role, content. Drop Gradio's extra keys
        messages = history + [{"role": "user", "content": message}] # Append the user turn

        while True: # Continuous loop
            response = self.antrophic.messages.create(
                model=model_name,
                messages=messages,
                timeout=59,
                max_tokens=1024,
                system=self.system_prompt(),
                tools=tools, # List of tools
            )
            if response.stop_reason != "tool_use": # Checks whethet Claude is done (not requesting a tool)
                return next(b.text for b in response.content if b.type == "text") # FINISH LOOP: Return the text of the first block

            messages.append({"role": "assistant", "content": response.content}) # Record Claude's turn (text + tool_use blocks) in the conversation

            tool_results = [] # Collect one tool_result per tool_use block below
            for block in response.content:  # Scan every block in Claude's reply (text and tool_use)
                print(block)
                if block.type == 'tool_use':
                    result = self.run_tool(block.name, block.input) # RUN TOOL THROUGH DISPATCHER: block.name, block.input are set by Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})  # Send all tool results back as one user message
    

if __name__ == "__main__":
    clone = Clone()
    gr.ChatInterface(clone.chat, type="messages").launch()
    