# token_itemize/tokenizers/text_tokenizer.py
import os
import tiktoken  # You can further configure this if needed

def count_text_tokens(text, verbose=False):
    try:
        # For demonstration, a simple whitespace tokenizer is used.
        tokens = text.split()
        if verbose:
            print(f"Text tokenization: {len(tokens)} tokens")
        return len(tokens), "Simple whitespace tokenization"
    except Exception as e:
        raise ValueError(f"Error tokenizing text: {str(e)}")

def count_text_file_tokens(file_path, verbose=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    try:
        # Open with errors="replace" to handle files with minor encoding issues.
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return count_text_tokens(text, verbose=verbose)
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")
