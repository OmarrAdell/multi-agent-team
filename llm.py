import os
import time
from google import genai
from google.genai import errors, types
from tracing import log

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-lite-latest"

def _generate(contents, config, retries=4):
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model=MODEL, contents=contents, config=config
            )
        except errors.ServerError:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"Server busy, retrying in {wait}s...")
            time.sleep(wait)

def ask(prompt, system=None):
    config = types.GenerateContentConfig(system_instruction=system)
    return _generate(prompt, config).text

def ask_with_tools(prompt, system, tools, max_steps=6, name="agent"):
    registry = {fn.__name__: fn for fn in tools}
    config = types.GenerateContentConfig(
        system_instruction=system,
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(max_steps):
        response = _generate(contents, config)
        calls = response.function_calls
        if not calls:
            return response.text

        contents.append(response.candidates[0].content)
        results = []
        for call in calls:
            print(f"  tool call: {call.name}({dict(call.args)})")
            log(name, "tool_call", f"{call.name}({dict(call.args)})")
            output = registry[call.name](**call.args)
            results.append(
                types.Part.from_function_response(
                    name=call.name, response={"result": output}
                )
            )
        contents.append(types.Content(role="user", parts=results))

    return "Stopped: reached the maximum number of steps."