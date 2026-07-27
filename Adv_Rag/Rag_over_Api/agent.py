import os
import json
import requests

from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------------
# Load Environment Variables
# ------------------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------------
# Tool Functions
# ------------------------------------
def get_leave():
    print("\n📞 Calling Leave API...")
    return requests.get("http://127.0.0.1:5000/leave").json()


def get_salary():
    print("\n📞 Calling Salary API...")
    return requests.get("http://127.0.0.1:5000/salary").json()


def get_attendance():
    print("\n📞 Calling Attendance API...")
    return requests.get("http://127.0.0.1:5000/attendance").json()


# ------------------------------------
# Tool Definitions
# ------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_leave",
            "description": "Returns employee leave balance.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_salary",
            "description": "Returns employee salary.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_attendance",
            "description": "Returns employee attendance percentage.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# ------------------------------------
# User Question
# ------------------------------------
question = input("\nAsk your question: ")

# ------------------------------------
# Let LLM Decide
# ------------------------------------
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# ------------------------------------
# Tool Calling
# ------------------------------------
if message.tool_calls:

    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name

    print(f"\n🤖 LLM Selected Tool : {tool_name}")

    if tool_name == "get_leave":
        tool_response = get_leave()

    elif tool_name == "get_salary":
        tool_response = get_salary()

    elif tool_name == "get_attendance":
        tool_response = get_attendance()

    else:
        tool_response = {}

    print("\n📦 API Response")
    print(tool_response)

    # Send tool output back to LLM
    final = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": question
            },
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_response)
            }
        ]
    )

    print("\n✅ Final Answer\n")
    print(final.choices[0].message.content)

else:
    print(message.content)