import requests
import json
import os

def get_gemini_response(prompt, api_key, model="gemini-2.0-flash"):
    """
    Sends a prompt to the Gemini API and returns the generated content.

    Args:
        prompt: The text prompt to send to the API.
        api_key: Your Gemini API key.
        model: The Gemini model to use.

    Returns:
        The generated text response from the API, or None if an error occurred.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing API response: {e}")
        if 'response' in locals(): #check if response exist, to avoid error when response is not created.
            print(response.text) #Print the raw response to help debugging
        return None

def chatbot():
    """
    A simple chatbot that interacts with the Gemini API.
    """
    api_key = os.environ.get("GEMINI_API_KEY")  # Get API key from environment variable
    if not api_key:
        api_key = input("Enter your Gemini API key: ")  # If not in env, ask the user.
        print("Warning: Storing API keys directly in code is insecure. Please consider using environment variables.")

    print("Welcome to the Gemini Chatbot! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = get_gemini_response(user_input, api_key)

        if response:
            print("Gemini:", response)
        else:
            print("Gemini: Sorry, I couldn't generate a response.")

if __name__ == "__main__":
    chatbot()
