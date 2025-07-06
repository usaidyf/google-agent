import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) < 2:
        print("Please provide a second argument")
        sys.exit(1)
        
    is_verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
        is_verbose = True

    print("Hello from google-agent!")

    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        
    print(response.text)

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
