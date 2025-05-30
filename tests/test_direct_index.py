import os
import unittest
from webcrawler_project.utils.trie import Trie
from webcrawler_project.index.direct_index import build_direct_index

class TestDirectIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = "test_docs"
        os.makedirs(cls.test_dir, exist_ok=True)
        with open(os.path.join(cls.test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
            f.write("Python is great in 2024. Python and webcrawler!")
        with open(os.path.join(cls.test_dir, "doc2.txt"), "w", encoding="utf-8") as f:
            f.write("Webcrawler is a tool to crawl the web in 2024.")

    @classmethod
    def tearDownClass(cls):
        for fname in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, fname))
        os.rmdir(cls.test_dir)

    def test_build_direct_index(self):
        stopwords = Trie()
        exceptions = Trie()
        for word in ["the", "is", "and", "a", "to", "in"]:
            stopwords.insert(word)
        for word in ["python", "webcrawler"]:
            exceptions.insert(word)

        index = build_direct_index(self.test_dir, stopwords, exceptions)

        self.assertIn("doc1.txt", index)
        self.assertEqual(index["doc1.txt"]["python"], 2)
        self.assertEqual(index["doc1.txt"]["webcrawler"], 1)
        self.assertEqual(index["doc1.txt"]["great"], 1)

        self.assertIn("doc2.txt", index)
        self.assertEqual(index["doc2.txt"]["webcrawler"], 1)
        self.assertEqual(index["doc2.txt"]["tool"], 1)
        self.assertEqual(index["doc2.txt"]["crawl"], 1)
        self.assertNotIn("is", index["doc2.txt"])  # stopword

if __name__ == "__main__":
    unittest.main()