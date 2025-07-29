# token_itemize/cache.py
import os
import json
import hashlib
import time

CACHE_DIR = ".cache"

def get_cache_path():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    return os.path.join(CACHE_DIR, "cache.json")

def load_cache():
    cache_file = get_cache_path()
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    cache_file = get_cache_path()
    with open(cache_file, "w") as f:
        json.dump(cache, f)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception:
        return None

def get_cached_token_count(file_path):
    cache = load_cache()
    file_hash = get_file_hash(file_path)
    if file_hash and file_hash in cache:
        entry = cache[file_hash]
        # Compare modification times (allowing a small difference)
        if abs(entry.get("mtime", 0) - os.path.getmtime(file_path)) < 1:
            return entry.get("tokens")
    return None

def set_cached_token_count(file_path, tokens):
    cache = load_cache()
    file_hash = get_file_hash(file_path)
    if file_hash:
        cache[file_hash] = {
            "tokens": tokens,
            "mtime": os.path.getmtime(file_path),
            "timestamp": time.time()
        }
        save_cache(cache)
