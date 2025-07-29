# tests/test_video_tokenizer.py
import unittest
import os
from token_itemize.tokenizers.video_tokenizer import count_video_tokens
from token_itemize.tokenizers.image_tokenizer import count_image_tokens

class TestVideoTokenizer(unittest.TestCase):
    def setUp(self):
        self.test_video = "test.mp4"
        
    def test_basic_functionality(self):
        tokens, details = count_video_tokens(
            file_path=self.test_video,
            verbose=True
        )
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)
        self.assertIn("Processed", details)
    
    def test_frame_interval(self):
        tokens_normal, _ = count_video_tokens(
            file_path=self.test_video,
            frame_interval=1.0
        )
        
        tokens_half, _ = count_video_tokens(
            file_path=self.test_video,
            frame_interval=0.5
        )
        
        self.assertGreater(tokens_half, tokens_normal)
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            count_video_tokens("nonexistent.mp4")
            
        with self.assertRaises(ImportError):
            # Simulate missing OpenCV
            original_cv2 = count_video_tokens.__globals__["cv2"]
            count_video_tokens.__globals__["cv2"] = None
            try:
                count_video_tokens(self.test_video)
            finally:
                count_video_tokens.__globals__["cv2"] = original_cv2

if __name__ == '__main__':
    unittest.main()