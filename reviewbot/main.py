import os
import requests
from reviewbot.utils import get_diff

def review_with_groq(diff):
    api_key = os.environ.get("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a senior software engineer doing code reviews."},
            {"role": "user", "content": f"Please review this code diff:\n\n{diff}"}
        ],
        "temperature": 0.3,
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def main():
    diff = get_diff()
    review = review_with_groq(diff)
    print("::notice file=test_module/hello.py,line=1::" + review.replace("\n", " "))

if __name__ == "__main__":
    main()
