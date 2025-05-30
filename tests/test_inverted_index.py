import os
import unittest
from webcrawler_project.utils.trie import Trie
from webcrawler_project.index.direct_index import build_direct_index
from webcrawler_project.index.inverted_index import build_inverted_index

class TestInvertedIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = "test_docs"
        os.makedirs(cls.test_dir, exist_ok=True)
        with open(os.path.join(cls.test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
            f.write("Python is great and webcrawler is awesome.")
        with open(os.path.join(cls.test_dir, "doc2.txt"), "w", encoding="utf-8") as f:
            f.write("Webcrawler is a python tool.")

    @classmethod
    def tearDownClass(cls):
        for fname in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, fname))
        os.rmdir(cls.test_dir)

    def test_build_inverted_index(self):
        stopwords = Trie()
        exceptions = Trie()
        for w in ["the", "is", "and", "a", "to", "in"]:
            stopwords.insert(w)
        for w in ["python", "webcrawler"]:
            exceptions.insert(w)

        direct_index = build_direct_index(self.test_dir, stopwords, exceptions)
        inverted_index = build_inverted_index(direct_index)

        # verifica daca contine postings pentru cuvintele cheie
        self.assertIn("python", inverted_index)
        self.assertIn("webcrawler", inverted_index)
        self.assertIn("great", inverted_index)
        self.assertIn("awesom", inverted_index)
        self.assertIn("tool", inverted_index)

        # postings pentru "python"
        self.assertEqual(inverted_index["python"]["postings"]["doc1.txt"], 1)
        self.assertEqual(inverted_index["python"]["postings"]["doc2.txt"], 1)

        # postings pentru "webcrawler"
        self.assertEqual(inverted_index["webcrawler"]["postings"]["doc1.txt"], 1)
        self.assertEqual(inverted_index["webcrawler"]["postings"]["doc2.txt"], 1)

        # postings pentru "great"
        self.assertEqual(inverted_index["great"]["postings"]["doc1.txt"], 1)
        self.assertNotIn("doc2.txt", inverted_index["great"]["postings"])

        # idf
        self.assertIn("idf", inverted_index["python"])
        self.assertIsInstance(inverted_index["python"]["idf"], float)

if __name__ == "__main__":
    unittest.main()