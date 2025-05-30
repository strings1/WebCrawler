import os
import unittest
from webcrawler_project.utils.trie import Trie
from webcrawler_project.index.direct_index import build_direct_index
from webcrawler_project.index.inverted_index import build_inverted_index
from webcrawler_project.search.vectorial_search import vectorial_search

class TestVectorialSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = "test_docs"
        os.makedirs(cls.test_dir, exist_ok=True)
        with open(os.path.join(cls.test_dir, "doc1.txt"), "w", encoding="utf-8") as f:
            f.write("Python is great and webcrawler is awesome.")
        with open(os.path.join(cls.test_dir, "doc2.txt"), "w", encoding="utf-8") as f:
            f.write("Webcrawler is a python tool.")
        with open(os.path.join(cls.test_dir, "doc3.txt"), "w", encoding="utf-8") as f:
            f.write("Java is also a programming language.")

    @classmethod
    def tearDownClass(cls):
        for fname in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, fname))
        os.rmdir(cls.test_dir)

    def setUp(self):
        self.stopwords = Trie()
        self.exceptions = Trie()
        for w in ["the", "is", "and", "a", "to", "in"]:
            self.stopwords.insert(w)
        for w in ["python", "webcrawler"]:
            self.exceptions.insert(w)
        self.direct_index = build_direct_index(self.test_dir, self.stopwords, self.exceptions)
        self.inverted_index = build_inverted_index(self.direct_index)

    def test_vectorial_search_python_webcrawler(self):
        query = "python webcrawler"
        results = vectorial_search(query, self.inverted_index, self.stopwords, self.exceptions)
        result_docs = [doc for doc, score in results]
        # print("\n\n")
        # print(self.direct_index)
        # print("\n\n")
        # print(self.inverted_index)

        self.assertIn("doc1.txt", result_docs)
        self.assertIn("doc2.txt", result_docs)
        self.assertNotIn("doc3.txt", result_docs)
        for doc, score in results:
            self.assertGreater(score, 0.0)

    def test_vectorial_search_java(self):
        query = "java"
        results = vectorial_search(query, self.inverted_index, self.stopwords, self.exceptions)
        result_docs = [doc for doc, score in results]
        self.assertEqual(result_docs, ["doc3.txt"])

    def test_vectorial_search_no_match(self):
        query = "banana"
        results = vectorial_search(query, self.inverted_index, self.stopwords, self.exceptions)
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()