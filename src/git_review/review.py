import subprocess
import json
import urllib.request
import sys

# Config
TARGET_BRANCH = "main"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"  # Change this to whatever model you use locally

# Edit these guidelines to match your exact coding style and preferences
PERSONAL_GUIDELINES = """
- Strict Formatting Rule: Do not include ANY emojis anywhere in your output.
- Group your analysis strictly into the four required sections defined below.
- After finding an issue, identify which section it best fits. Only allocate it to that section. It is not allowed to be put into multiple sections.

1. BUGS and typos
List 100% certain, clear, and non-negotiable coding mistakes and typos here. Group them by line numbers using short, direct sentences. They must be immediately noticeable. Do not discuss syntax style, naming preferences, or wording in this section.

2. CAUTION AREAS
Identify line numbers where the user must be careful due to potential vulnerabilities, subtle edge cases, or risky implementations. Do not discuss style, naming, wording, or typos in this section.

3. WORDING AND Grammar
List any typos, grammatical issues, unclear documentation strings, poorly phrased console logs, or variable names that should be updated to improve clarity.

4. CODE SMELL AND CONSOLIDATION
Highlight redundant imports, obsolete logic, bloated functions, and blocks of code that can be easily shrunken, refactored, or simplified.
"""


def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff", f"origin/{TARGET_BRANCH}"],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(
                ["git", "diff", f"{TARGET_BRANCH}"],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            print("❌ Error: Could not generate git diff.")
            sys.exit(1)


def query_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'), headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get('response', 'Error: No response text returned from Ollama.')
    except Exception as e:
        return (
            f"Error connecting to local Ollama instance: {str(e)}\n"
            f"Please verify Ollama is active by running `ollama list` in your terminal."
        )


def main():
    print("Performing Automated PR Review")
    diff = get_git_diff().strip()

    if not diff:
        print("Current Branch matches target branch")
        return

    full_prompt = f"""You are a strict, objective senior software engineer reviewing my pull request.
    Review the following git diff according to these explicit workflow guidelines: {PERSONAL_GUIDELINES}
    
    CRITICAL: Absolutely no emojis allowed in your output.
    
    Here is the Git Diff to review: {diff}
    Provide your structured, highly technical review now:"""

    print(f"Review being done using {OLLAMA_MODEL}...")
    review_output = query_ollama(full_prompt)

    print("\n" + "=" * 50 + "\n AI REVIEW OUTPUT \n" + "=" * 50)
    print(review_output)

if __name__ == "__main__":
    main()