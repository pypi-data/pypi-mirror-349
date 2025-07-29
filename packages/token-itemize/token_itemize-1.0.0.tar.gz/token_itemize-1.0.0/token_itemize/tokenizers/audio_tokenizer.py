# token_itemize/tokenizers/audio_tokenizer.py
import os
import wave
import contextlib
import math

def count_audio_tokens(file_path, verbose=False, window_duration=0.96):
    """
    Process a .wav file and count tokens based on spectrogram windows.
    window_duration: duration in seconds of each window (similar to Whisper)
    """
    try:
        with contextlib.closing(wave.open(file_path, 'r')) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            # Calculate number of windows (tokens)
            tokens = math.ceil(duration / window_duration)
            details = f"Audio duration: {duration:.2f}s, window duration: {window_duration}s, {tokens} tokens"
            if verbose:
                print(f"Audio {file_path}: {details}")
            return tokens, details
    except wave.Error:
        raise ValueError("Only .wav files are supported for audio tokenization in this implementation.")
    except Exception as e:
        raise ValueError(f"Error processing audio {file_path}: {str(e)}")
