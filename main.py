import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def chat_with_llm(prompt, model="openai/gpt-4o-mini"):
    """
    Send a chat message to OpenRouter API and get the response.
    
    Args:
        prompt (str): The user's message
        model (str): The model to use (default: gpt-3.5-turbo)
    
    Returns:
        str: The model's response
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def main():
    # Example usage
    prompt = "cuanto es 2 + 2"
    response = chat_with_llm(prompt)
    
    if response:
        print("\nUser:", prompt)
        print("\nAssistant:", response)
    else:
        print("Failed to get response from the API")

if __name__ == "__main__":
    main()