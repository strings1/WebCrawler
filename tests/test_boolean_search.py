import os
import unittest
from webcrawler_project.utils.trie import Trie
from webcrawler_project.index.direct_index import build_direct_index
from webcrawler_project.index.inverted_index import build_inverted_index
from webcrawler_project.search.boolean_search import boolean_search

class TestBooleanSearch(unittest.TestCase):
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
        stopwords = Trie()
        exceptions = Trie()
        for w in ["the", "is", "and", "a", "to", "in"]:
            stopwords.insert(w)
        for w in ["python", "webcrawler"]:
            exceptions.insert(w)
        self.direct_index = build_direct_index(self.test_dir, stopwords, exceptions)
        self.inverted_index = build_inverted_index(self.direct_index)
        self.all_docs = set(self.direct_index.keys())

    def test_boolean_search_python(self):
        result = boolean_search("python", self.inverted_index, self.all_docs)
        self.assertEqual(result, {"doc1.txt", "doc2.txt"})

    def test_boolean_search_python_and_webcrawler(self):
        result = boolean_search("python AND webcrawler", self.inverted_index, self.all_docs)
        self.assertEqual(result, {"doc1.txt", "doc2.txt"})

    def test_boolean_search_python_or_java(self):
        result = boolean_search("python OR java", self.inverted_index, self.all_docs)
        self.assertEqual(result, {"doc1.txt", "doc2.txt", "doc3.txt"})

    def test_boolean_search_python_and_not_java(self):
        result = boolean_search("python AND NOT java", self.inverted_index, self.all_docs)
        self.assertEqual(result, {"doc1.txt", "doc2.txt"})

if __name__ == "__main__":
    unittest.main()