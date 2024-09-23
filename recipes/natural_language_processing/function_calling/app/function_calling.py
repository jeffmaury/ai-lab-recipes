import json
import streamlit as st
import instructor
from openai.types.chat import ChatCompletion


def get_current_weather(location):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({
            "location": "Tokyo",
            "temperature": "10",
        })
    elif "san francisco" in location.lower():
        return json.dumps(
            {
                "location": "San Francisco",
                "temperature": "72",
            }
        )
    elif "paris" in location.lower():
        return json.dumps({
            "location": "Paris",
            "temperature": "22",
        })
    else:
        return json.dumps({
            "location": location,
            "temperature": "unknown"
        })

# Define how the tools get used
tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]


def function_calling_submit(client, input: str, model: str) -> ChatCompletion:
    # Step 1: send the conversation and available functions to the model
    messages = [
        {
            "role": "user",
            "content": input,
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
            )
            st.info(f'model called `{function_name}` with {function_args}')

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response


def function_calling_form(openai_client, model: str):
    with st.form('function-calling-form'):
        st.subheader('python function')
        code = '''
            def get_current_weather(location):
                """Get the current weather in a given location"""
                if "tokyo" in location.lower():
                    return json.dumps({
                        "location": "Tokyo",
                        "temperature": "10",
                    })
                elif "san francisco" in location.lower():
                    return json.dumps(
                        {
                            "location": "San Francisco",
                            "temperature": "72",
                        }
                    )
                elif "paris" in location.lower():
                    return json.dumps({
                        "location": "Paris",
                        "temperature": "22",
                    })
                else:
                    return json.dumps({
                        "location": location,
                        "temperature": "unknown"
                    })
        '''
        st.code(code, language="python")

        text = st.text_area('Enter text:',
                            'What\'s the weather like in San Francisco, Tokyo, and Paris?')
        submitted = st.form_submit_button('Submit')
        if submitted:
            classification = function_calling_submit(openai_client, text, model)
            st.markdown(classification.choices[0].message.content)