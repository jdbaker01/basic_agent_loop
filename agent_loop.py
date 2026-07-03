import json
import logging
import sys
from openai import OpenAI

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# Point to LM Studio's local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Set this to whichever model you have loaded in LM Studio
MODEL = "openai/gpt-oss-20b"

# Tools available to the agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a math expression and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Python math expression, e.g. '1234 + 5678'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def invoke_model(tools, conversation):
    return client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        tools=tools,
        tool_choice="auto"
    ).choices[0].message

def is_tool_call(response):
    return bool(response.tool_calls)

def invoke_tool(response):
    tool_call = response.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    logging.info(f"tool call: {tool_call.function.name}({args})")
    result = str(eval(args["expression"]))
    logging.info(f"tool result: {result}")
    return result

def update_conversation(conversation, response, result):
    tool_call = response.tool_calls[0]
    conversation.append(response)
    conversation.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

# The agent loop
def run_agent(user_message):
    conversation = [{"role": "user", "content": user_message}]
    logging.info(f"user: {user_message}")

    while True:
        #observe
        response = invoke_model(tools, conversation)

        #act
        if is_tool_call(response):
            result = invoke_tool(response)
            update_conversation(conversation, response, result)
        else: #end
            logging.info(f"end: {response.content}")
            return response.content


if __name__ == "__main__":
    run_agent("What is 20 multiplied by 250?")
