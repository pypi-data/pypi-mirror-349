# tests/test_api_client.py
import unittest
from token_itemize.api.api_client import APIClient

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json
    def raise_for_status(self):
        pass

class DummySession:
    def post(self, url, json, headers, timeout):
        # Return a dummy response with token counts.
        return DummyResponse({"input_tokens": 100, "output_tokens": 50, "results": []})

class TestAPIClient(unittest.TestCase):
    def test_api_client_fallback(self):
        # Monkey-patch requests.post to use our dummy response.
        import requests
        original_post = requests.post
        requests.post = DummySession().post

        client = APIClient(endpoint="http://dummy", model="dummy-model", verbose=False)
        result = client.count_tokens(files=["dummy_file.txt"], prompt="Test prompt")
        self.assertIn("input_tokens", result)
        self.assertEqual(result["input_tokens"], 100)
        
        requests.post = original_post

if __name__ == '__main__':
    unittest.main()
