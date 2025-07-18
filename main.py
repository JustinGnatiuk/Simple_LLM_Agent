# Simple LLM agent
# Usage: "python main.py "user prompt" [--verbose]"
#
# Justin Gnatiuk


# External libraries
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Local imports
from prompts import system_prompt
from functions.call_function import call_function, available_functions
from config import MAX_ITERS

# Load environment file and store gemini api key in variable
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Establish connection to gemini genai client
client = genai.Client(api_key=api_key)

def main():

    # set verbose boolean flag & store prompt arguments
    verbose = "--verbose" in sys.argv[-1]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # if no arguments/prompt given
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # extract full text prompt from command line arguments
    user_prompt = " ".join(args)
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # message list for agent prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    iters = 0
    # generate agent responses until a final text response is reached
    while True:

        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations reached: {MAX_ITERS}")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final Response:")
                print(final_response)
                break

        except Exception as e:
            print(f'Error Analyzing prompt: {e}')

# Function to call gemini API and generate responses
# Call tool functions that it recommends with each response
# Return final text response once no more function calls are recommended 
def generate_content(client, messages, verbose):

    # make API call with list of agent messages
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Add candidate responses to list of messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # If no function calls are recommended in response, return final response
    if not response.function_calls:
        return response.text
    
    # Loop over each function recommendation and call function.
    # function is a genai library function_call object and is passed into 
    # locally defined "call_function"
    function_responses = []
    for func in response.function_calls:
        
        function_call_result = call_function(func, verbose)
        

        # raise exception if function response is empty
        if not function_call_result.parts[0].function_response.response:
            raise Exception(f"Error: function {func.name} gave no response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        # add function call result to list of function_responses
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # add function responses to messages list
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()
