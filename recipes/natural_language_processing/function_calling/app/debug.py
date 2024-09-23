import json
import openai

BASE_URL = "http://0.0.0.0:8000/v1"
API_KEY = "sk-xxx"
MODEL_ID = "/home/axel7083/Documents/models/functionary-small-v2.5.Q4_0.gguf"

def get_current_weather(location):
    return json.dumps({"location": location, "temperature": "37° celsius"})

client = openai.OpenAI(base_url=BASE_URL, api_key=API_KEY)

messages = [
    {"role": "user", "content": "what's the weather like in Hanoi?"}
]
tools = [ # For functionary-7b-v2 we use "tools"; for functionary-7b-v1.4 we use "functions" = [{"name": "get_current_weather", "description":..., "parameters": ....}]
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA",
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model=MODEL_ID,
    messages=messages,
    tools=tools,
)

print(response)
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if not tool_calls:
    exit(1)

available_functions = {
            "get_current_weather": get_current_weather,
        }

messages.append(response_message)

for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    function_response = function_to_call(
        location=function_args.get("location"),
    )
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )  # extend conversation with function response
second_response = client.chat.completions.create(
    model=MODEL_ID,
    messages=messages,
    tools=tools,
)