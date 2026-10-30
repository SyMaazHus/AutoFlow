import os, json, requests
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"

def groq_folder_match(fileNames: list[str], folders: list[str]) -> dict[str, str | None] | None:
    if not fileNames or not folders:
        return {}

    body = {
        "model": GROQ_MODEL,
        "temperature": 0,                          # 0 = least random, so the same input gives the same answer
        "reasoning_effort": "low",                 # gpt-oss 'thinks' first; low keeps it fast.
        "response_format": {"type": "json_object"},   # forces valid JSON back
        "messages": [
            # 'system' message = the rules the model must follow
            {"role": "system", "content":
                'You sort files into the user\'s existing folders. '
                'Folder names may be abbreviations or short forms (for example "ML" means machine learning, '
                '"CS" means computer science). File names may contain typos. '
                'Pick the folder whose subject best matches the file, even if the name is not an exact match. '
                'Use null only if no folder is a reasonable fit. '
                'Reply only with JSON: {"matches": {"<file name>": "<exact folder name>" or null}},'},
            # 'user' message = the actual question
            {"role": "user", "content":
                f"Folders: {json.dumps(folders)}\nFiles: {json.dumps(fileNames)}"},
        ],
    }

    try:
        # request from groq URL server with the auth headers and message
        r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {GROQ_KEY}"}, json=body, timeout=30)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        raw = json.loads(content).get("matches", {})

        # Return the results, checking if folder exists (groq / real directory)
        return {n : (raw.get(n) if raw.get(n) in folders else None) for n in fileNames}
        
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print("[Groq] failed: ", e)
        return {}

if __name__ == "__main__":
    print(groq_folder_match(["Neural networks revision.pdf", "cw1.pdf", "holiday.png"], ["Lectures", "ML", "Coursework"]))