import unittest
from webcrawler_project.utils.trie import Trie

class TestTrie(unittest.TestCase):
    def test_insert_and_search(self):
        trie = Trie()
        words = ["cat", "dog", "apple", "Cat", "DOG"]
        for word in words:
            trie.insert(word)
        # Test words that should be found (case-insensitive)
        self.assertTrue(trie.search("cat"))
        self.assertTrue(trie.search("dog"))
        self.assertTrue(trie.search("apple"))
        self.assertTrue(trie.search("CAT"))
        self.assertTrue(trie.search("Dog"))
        
        # Test words that should not be found
        self.assertFalse(trie.search("ca"))
        self.assertFalse(trie.search("caterpillar"))
        self.assertFalse(trie.search("appl"))
        self.assertFalse(trie.search(""))

    def test_empty_insert(self):
        trie = Trie()
        trie.insert("")
        self.assertFalse(trie.search(""))

    def test_prefix_not_word(self):
        trie = Trie()
        trie.insert("test")
        self.assertFalse(trie.search("tes"))
        self.assertTrue(trie.search("test"))

if __name__ == "__main__":
    unittest.main()