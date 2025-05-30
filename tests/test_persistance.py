import os
import unittest
from webcrawler_project.storage.persistance import save_json, load_json

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.json"
        self.test_data = {"a": 1, "b": [2, 3], "c": {"d": 4}}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_json(self):
        save_json(self.test_data, self.test_file)
        loaded = load_json(self.test_file)
        self.assertEqual(loaded, self.test_data)

    def test_load_json_file_not_found(self):
        loaded = load_json("nonexistent_file.json")
        self.assertEqual(loaded, {})

    def test_save_json_error(self):
        # Try saving to a directory (should fail and log error)
        os.mkdir("test_dir")
        try:
            save_json(self.test_data, "test_dir")  # Not a file path
            # File should not be created
            self.assertFalse(os.path.isfile("test_dir"))
        finally:
            os.rmdir("test_dir")

    def test_load_json_invalid_json(self):
        # Write invalid JSON
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        loaded = load_json(self.test_file)
        self.assertEqual(loaded, {})

if __name__ == "__main__":
    unittest.main()