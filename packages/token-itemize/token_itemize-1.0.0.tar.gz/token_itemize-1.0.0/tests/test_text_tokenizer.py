# tests/test_text_tokenizer.py
import unittest
from token_itemize.tokenizers.text_tokenizer import count_text_tokens

class TestTextTokenizer(unittest.TestCase):
    def test_token_count(self):
        text = "Hello world! This is a test."
        tokens, details = count_text_tokens(text, verbose=False)
        # With a simple whitespace split, we expect 6 tokens.
        self.assertEqual(tokens, 6)

if __name__ == '__main__':
    unittest.main()
