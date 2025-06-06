import os
import requests
from reviewbot.utils import get_diff, post_pr_comment, get_pr_number

llm_prompt = "Please reviiew thsi code diff, list improvements and potential optimizations in bullet points";

def review_with_groq(diff):
    api_key = os.environ.get("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "You are a senior software engineer doing code reviews."},
            {"role": "user", "content": f"{llm_prompt} given the following diff{diff}"}
        ],
        "temperature": 0.3,
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    print("Raw Groq response:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    diff = get_diff()
    review = review_with_groq(diff)
    post_pr_comment(review)

if __name__ == "__main__":
    main()
