# tests/test_edge_cases.py
import unittest
import os
from token_itemize.utils import process_file

class TestEdgeCases(unittest.TestCase):
    def test_nonexistent_file(self):
        with self.assertRaises(Exception):
            process_file("nonexistent_file.txt", verbose=False)
    
    def test_unsupported_file(self):
        # Create a dummy file with an unsupported extension.
        file_name = "dummy.unsupported"
        with open(file_name, "w") as f:
            f.write("dummy content")
        with self.assertRaises(ValueError):
            process_file(file_name, verbose=False)
        os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
