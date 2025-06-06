import os
import requests
import json

def get_pr_number():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        raise Exception("GITHUB_EVENT_PATH not set")

    with open(event_path, 'r') as f:
        event = json.load(f)
    
    return event["pull_request"]["number"]

def get_diff():
    repo = os.environ.get("GITHUB_REPOSITORY")  # e.g. "owner/repo"
    pr_number = get_pr_number()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise Exception("Missing GITHUB_TOKEN environment variable.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    diffs = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        response.raise_for_status()
        files = response.json()
        if not files:
            break

        for f in files:
            patch = f.get("patch")
            if patch:
                diffs.append(f"File: {f['filename']}\n{patch}")

        page += 1

    return "\n\n".join(diffs)

def post_pr_comment(body: str):
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")
    pr_number = get_pr_number()

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "body": body
    }

    response = requests.post(url, headers=headers, json=payload)
    print("GitHub API response:", response.status_code, response.text)
    response.raise_for_status()
