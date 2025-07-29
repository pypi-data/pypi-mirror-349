# token_itemize/utils.py
import os
import re
from token_itemize.cache import get_cached_token_count, set_cached_token_count
from token_itemize.tokenizers import text_tokenizer, image_tokenizer, audio_tokenizer, video_tokenizer

def collect_files(file_list, folder_list, exclude_pattern=None, verbose=False, use_gitignore=False):
    files = set()
    if file_list:
        for f in file_list:
            if os.path.isfile(f):
                files.add(os.path.abspath(f))
            elif verbose:
                print(f"Warning: {f} is not a file.")
    if folder_list:
        for folder in folder_list:
            if os.path.isdir(folder):
                for root, _, filenames in os.walk(folder):
                    for filename in filenames:
                        full_path = os.path.join(root, filename)
                        files.add(os.path.abspath(full_path))
            elif verbose:
                print(f"Warning: {folder} is not a directory.")
    if exclude_pattern:
        pattern = re.compile(exclude_pattern)
        files = {f for f in files if not pattern.search(f)}
    
    if use_gitignore:
        gitignore_path = os.path.join(os.getcwd(), ".gitignore")
        if os.path.exists(gitignore_path):
            try:
                import pathspec
                with open(gitignore_path, "r") as f:
                    lines = f.read().splitlines()
                spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
                files = {f for f in files if not spec.match_file(os.path.relpath(f, os.getcwd()))}
                if verbose:
                    print("Applied .gitignore filtering.")
            except Exception as e:
                if verbose:
                    print(f"Error applying .gitignore filtering: {e}")
    return list(files)

def process_file(file_path, verbose=False):
    # Check if result is cached.
    cached = get_cached_token_count(file_path)
    if cached is not None:
        if verbose:
            print(f"Cache hit for {file_path}: {cached} tokens")
        return cached, "Cached result"

    ext = os.path.splitext(file_path)[1].lower()
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
    audio_extensions = ['.wav', '.mp3', '.flac', '.aac', '.ogg']
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    if ext in image_extensions:
        tokens, details = image_tokenizer.count_image_tokens(file_path, verbose=verbose)
    elif ext in audio_extensions:
        tokens, details = audio_tokenizer.count_audio_tokens(file_path, verbose=verbose)
    elif ext in video_extensions:
        tokens, details = video_tokenizer.count_video_tokens(file_path, verbose=verbose)
    else:
        # For any other file type (e.g., .ini, .json, .yaml, .js, .bat, .sh, .sql, .html, .css, etc.),
        # treat it as a text file.
        tokens, details = text_tokenizer.count_text_file_tokens(file_path, verbose=verbose)
    
    set_cached_token_count(file_path, tokens)
    return tokens, details
