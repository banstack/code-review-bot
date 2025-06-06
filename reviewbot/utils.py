# reviewbot/utils.py

def get_diff():
    # In real setup, parse `git diff` or PR files
    return "def hello(name):\n    print('Hello ' + name)"

def fake_llm_review(diff):
    if "print" in diff:
        return "Consider using logging instead of print for better production code quality."
    return "No issues found."
