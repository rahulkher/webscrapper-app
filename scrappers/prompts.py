import openai
# from dotenv import load_dotenv
import os
import json
import requests
from scrappers.checklicense import check_license_premium, check_license_standard


@check_license_premium
def generate_twitter_prompts_openai(theme, model="gpt-3.5-turbo-instruct", num_prompts=5):
    """
    Generates Twitter-specific search prompts based on a given theme.

    :param theme: The user-provided theme to base search prompts on.
    :param num_prompts: The number of prompts to generate.
    :return: A list of generated Twitter search queries.
    """

    try:
        # Load environment variables from .env file
        # load_dotenv()

        # Retrieve the OpenAI API key from environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')
        prompt_text = f"Create {num_prompts} search queries for Twitter related to the theme: '{theme}'. Focus on keywords, hashtags, and phrases typical for Twitter."

        response = openai.Completion.create(
            engine=model,  # or the latest available version
            prompt=prompt_text,
            temperature=0.7,
            max_tokens=150,
            n=num_prompts,
            stop=None
        )

       # Creating a result dictionary with prompts as separate key-value pairs
        result = {"theme": theme}
        for idx, choice in enumerate(response.choices, start=1):
            key = f"prompt_{idx}"
            result[key] = choice['text'].strip()

        # Convert the result dictionary to a JSON string
        json_result = json.dumps(result, indent=4)
        return json_result

    except Exception as e:
        print(f"An error occurred: {e}")
        # Returning an error message as JSON
        return json.dumps({"error": str(e)})


@check_license_standard
# Function to generate prompts using the Hugging Face API
def generate_prompts_huggingface(theme, model="gpt2", num_prompts=1):
    """
    Generates prompts using the Hugging Face API.

    :param theme: Theme to base the prompts on.
    :param model: The model ID from Hugging Face to use for generation.
    :param num_prompts: Number of prompts to generate.
    :return: A list of generated prompts.
    """
    # Retrieve the Hugging Face API key
    # load_dotenv()
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    # Set up the API URL
    api_url = f"https://api-inference.huggingface.co/models/{model}"

    # Prepare headers and payload for the request
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": theme,
        "parameters": {"max_length": 50, "num_return_sequences": num_prompts},
    }

    # Make the request to the Hugging Face API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Extract the generated texts from the response
        generated_texts = response.json()

        # Structuring the result as separate key-value pairs
        result = {}
        for idx, text in enumerate(generated_texts, start=1):
            prompt_key = f"prompt_{idx}"
            result[prompt_key] = text['generated_text'].strip()

        return json.dumps(result, indent=4)
    else:
        print(f"Failed to generate prompts: {response.text}")
        return json.dumps({"error": response.json()['error']})

def main_openai():
    theme = input("Enter a theme to generate Twitter search queries: ")
    json_prompts = generate_twitter_prompts_openai(theme, num_prompts=5)
    print("\nGenerated Twitter Search Queries (JSON):")
    print(json_prompts)

def main_hf():
    theme = input("Enter a theme to generate Twitter search queries: ")
    prompts_json = generate_prompts_huggingface(theme, model="gpt2", num_prompts=5)
    print("Generated Prompts (JSON):")
    print(prompts_json)

if __name__ == "__main__":
    main_hf()