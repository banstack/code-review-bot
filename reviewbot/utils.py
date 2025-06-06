import os
import requests

def get_diff():
    repo = os.environ.get("GITHUB_REPOSITORY")  # e.g. "owner/repo"
    ref = os.environ.get("GITHUB_REF")          # e.g. "refs/pull/123/merge"

    if not repo or not ref:
        raise Exception("Missing GitHub repository or ref environment variables.")

    # Extract PR number safely:
    parts = ref.split("/")
    if len(parts) >= 3 and parts[-3] == "pull":
        pr_number = parts[-2]
    else:
        raise Exception(f"Unexpected GITHUB_REF format: {ref}")

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
                diffs.append(patch)

        page += 1

    return "\n".join(diffs)
