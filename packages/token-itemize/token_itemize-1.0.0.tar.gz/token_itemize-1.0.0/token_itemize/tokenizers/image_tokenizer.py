# token_itemize/tokenizers/image_tokenizer.py
from PIL import Image
import math

def count_image_tokens(file_path, verbose=False, patch_size=16):
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            patches_w = math.ceil(width / patch_size)
            patches_h = math.ceil(height / patch_size)
            total_patches = patches_w * patches_h
            details = f"{patches_w}x{patches_h} patches of size {patch_size}x{patch_size}"
            if verbose:
                print(f"Image {file_path}: {width}x{height} pixels, {details}, {total_patches} tokens")
            return total_patches, details
    except Exception as e:
        raise ValueError(f"Error processing image {file_path}: {str(e)}")
