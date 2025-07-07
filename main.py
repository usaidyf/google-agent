import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

function_name_maps = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(fn_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {fn_call_part.name}({fn_call_part.args})")
    else:
        print(f" - Calling function: {fn_call_part.name}")

    if fn_call_part.name not in function_name_maps:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_call_part.name,
                    response={"error": f"Unknown function: {fn_call_part.name}"},
                )
            ],
        )

    fn_call_result = function_name_maps[fn_call_part.name](
        "./calculator", **fn_call_part.args
    )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fn_call_part.name,
                response={"result": fn_call_result},
            )
        ],
    )


def main():
    if len(sys.argv) < 2:
        print("Please provide a second argument")
        sys.exit(1)

    is_verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        is_verbose = True

    print("Hello from google-agent!")

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if is_verbose:
        print(f"User prompt: {user_prompt}")


    # Main Agent loop
    i = 1
    while True:
        if i >= 20:
            break
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls is not None:
            for fn_call_part in response.function_calls:
                fn_call_result = call_function(fn_call_part, is_verbose)
                messages.append(fn_call_result)
                try:
                    if is_verbose:
                        print(
                            f"-> {fn_call_result.parts[0].function_response.response}"
                        )
                except Exception as e:
                    raise Exception(
                        f"Function call result has an unexpected structure {e}"
                    )
        else:
            print(response.text)
            break

        i += 1

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
