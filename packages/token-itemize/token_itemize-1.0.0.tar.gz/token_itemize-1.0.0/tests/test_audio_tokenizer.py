import unittest
import os
import wave
import contextlib
import numpy as np
from token_itemize.tokenizers.audio_tokenizer import count_audio_tokens
from unittest.mock import patch

class TestAudioTokenizer(unittest.TestCase):
    def setUp(self):
        self.test_file = "test.wav"
        # Create a valid dummy WAV file for testing
        with wave.open(self.test_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            frames = np.zeros(44100, dtype=np.int16)  # 1 second of silence
            wf.writeframes(frames.tobytes())

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_basic_functionality(self):
        tokens, details = count_audio_tokens(self.test_file)
        self.assertIsInstance(tokens, int)
        self.assertEqual(tokens, 2)  # 1 second audio / 0.96s window = 2 tokens
        self.assertIn("Audio duration", details)

    def test_different_window_duration(self):
        tokens, _ = count_audio_tokens(self.test_file, window_duration=0.5)
        self.assertEqual(tokens, 2)  # 1 second / 0.5s = 2 windows

    def test_invalid_file_format(self):
        with self.assertRaises(ValueError) as cm:
            count_audio_tokens("invalid.mp3")
        self.assertIn(".wav files are supported", str(cm.exception))

    def test_nonexistent_file(self):
        with self.assertRaises(ValueError) as cm:
            count_audio_tokens("nonexistent.wav")
        self.assertIn("Error processing audio", str(cm.exception))

    @patch('wave.open')
    def test_wave_error_handling(self, mock_wave_open):
        mock_wave_open.side_effect = wave.Error("Invalid wave file")
        with self.assertRaises(ValueError) as cm:
            count_audio_tokens(self.test_file)
        self.assertIn("Only .wav files are supported", str(cm.exception))