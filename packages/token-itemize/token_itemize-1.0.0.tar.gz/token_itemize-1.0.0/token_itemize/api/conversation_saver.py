# token_itemize/api/conversation_saver.py
import os
from datetime import datetime

def save_conversation_markdown(conversation, filename=None):
    """
    Save the conversation as a Markdown transcript.
    The conversation dictionary should contain:
      - provider: API provider used
      - prompt: text prompt sent (including any file contents)
      - files: list of file paths that were sent
      - response: the AI response text
      - input_tokens: count of input tokens
      - output_tokens: count of output tokens
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Conversation Transcript\n\n")
        f.write("## Provider\n")
        f.write(f"{conversation.get('provider','')}\n\n")
        f.write("## Prompt and Files Sent\n")
        prompt = conversation.get("prompt", "")
        files = conversation.get("files", [])
        if files:
            f.write("### Files:\n")
            for file in files:
                f.write(f"- {file}\n")
            f.write("\n")
        f.write("### Prompt:\n")
        f.write(f"{prompt}\n\n")
        f.write("## AI Response\n")
        f.write(conversation.get("response", "") + "\n\n")
        f.write("## Token Usage\n")
        input_tokens = conversation.get("input_tokens", 0)
        output_tokens = conversation.get("output_tokens", 0)
        f.write(f"- Input Tokens: {input_tokens}\n")
        f.write(f"- Output Tokens: {output_tokens}\n")
    return filename
