# token_itemize/tokenizers/video_tokenizer.py
import os
import math
import logging
from typing import Tuple, Optional, Any

try:
    import cv2
except ImportError:
    cv2 = None  # type: ignore

from token_itemize.tokenizers.image_tokenizer import count_image_tokens
import tempfile
import numpy as np

logger = logging.getLogger(__name__)

def count_video_tokens(
    file_path: str,
    verbose: bool = False,
    frame_interval: float = 1.0,
    patch_size: int = 16
) -> Tuple[int, str]:
    """
    Process a video file by extracting frames at a fixed interval and tokenizing each frame as an image.
    
    Args:
        file_path (str): Path to the video file.
        verbose (bool): Enable detailed logging. Defaults to False.
        frame_interval (float): Time between consecutive frames in seconds. Defaults to 1.0.
        patch_size (int): Size of image patches for tokenization. Defaults to 16.
        
    Returns:
        Tuple[int, str]: Total tokens and details string.
        
    Raises:
        ValueError: If video file cannot be opened or processing fails.
        ImportError: If OpenCV dependency missing.
    """
    # Ensure OpenCV is available
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is required for video tokenization.")
        
    try:
        # Initialize video capture
        cap = cv2.VideoCapture(file_path)
        
        # Verify video file opens successfully
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {file_path}")
            
        # Extract video metadata
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Display video properties in verbose mode
        if verbose:
            logger.info(f"Video {os.path.basename(file_path)}: {total_frames} frames at {fps:.2f} FPS, duration {duration:.2f}s")
            
        tokens_total = 0
        frame_count = 0
        current_time = 0.0
        
        # Process frames at defined intervals
        while True:
            # Set frame position
            cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
            ret, frame = cap.read()
            
            # End of video reached
            if not ret:
                break
            
            # Convert to RGB for consistent image handling
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create temporary file for frame processing
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp_path = tmp.name
                
                # Save frame to temp file
                cv2.imwrite(tmp_path, frame_rgb)
                
                # Process frame for tokens
                tokens, details = count_image_tokens(tmp_path, verbose=verbose, patch_size=patch_size)
                
                if isinstance(tokens, int):
                    tokens_total += tokens
                else:  # if implementation returns tuple
                    tokens_total += tokens[0] if isinstance(tokens, tuple) else tokens
                    
                frame_count += 1
            
            current_time += frame_interval
            
            # Terminate when end of video reached
            if current_time * 1000 > cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break
        
        cap.release()
        
        # Construct response details
        details = (
            f"Frames Sampled: {frame_count} at {frame_interval:.2f}s intervals, "
            f"Total Image Patches: {tokens_total}, Model Patch Size: {patch_size}"
        )
        
        # Verbose output
        if verbose:
            logger.info(f"Video {os.path.basename(file_path)}: {details}")
            
        return tokens_total, details
        
    except Exception as e:
        # Ensure resource release on error
        if 'cap' in locals() and cap.isOpened():
            cap.release()
            
        logger.error(f"Video processing failed: {str(e)}")
        raise ValueError(f"Video Processing Error: {str(e)}")