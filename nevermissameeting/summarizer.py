import requests
import os

# Claude API key should be stored in environment variables for safety
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

SYSTEM_PROMPT = """
You are a helpful assistant that summarizes meeting notes clearly and concisely. Extract key points, action items, and decisions.
"""

def summarize_text(text, model="claude-3-haiku-20240307"):
    data = {
        "model": model,
        "max_tokens": 1024,
        "temperature": 0.5,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(CLAUDE_API_URL, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()["content"][0]["text"]

if __name__ == "__main__":
    sample = """
    Alice discussed project deadlines. Bob will update the Jira board. The next review is scheduled for next Friday.
    """
    print(summarize_text(sample))
