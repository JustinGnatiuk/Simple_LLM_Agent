import os
import sys
from dotenv import load_dotenv
from google import genai

# load environment file and store gemini api key in variable
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# establish connection to gemini genai client
client = genai.Client(api_key=api_key)

def main():

    # verify prompt was given
    if len(sys.argv) < 2:
        print("Please provide a text prompt.")
        sys.exit(1)
    else:

        # extract text prompt from command line arguments
        prompt = sys.argv[1]

        # make API call with prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=prompt
        )

        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)


if __name__ == "__main__":
    main()
