from pathlib import Path


def load_file_content(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()


# Load API_PROMPT
api_prompt_path = Path(__file__).parent.parent.parent / "prompts" / "datalab-api-prompt.md"
API_PROMPT = load_file_content(api_prompt_path)

# Load SYSTEM_PROMPT
system_prompt_path = Path(__file__).parent.parent.parent / "prompts" / "system-prompt.md"
SYSTEM_PROMPT = load_file_content(system_prompt_path)

if __name__ == "__main__":
    print(SYSTEM_PROMPT)
    print(API_PROMPT)
