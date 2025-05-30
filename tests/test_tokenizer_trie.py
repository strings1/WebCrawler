import unittest
from webcrawler_project.utils.trie import Trie
from webcrawler_project.utils.tokenizer import tokenize

class TestTokenizerWithTrie(unittest.TestCase):
    def test_tokenize_with_stopwords_and_exceptions(self):
        stopwords = Trie()
        exceptions = Trie()
        for word in ['the', 'and', 'is', 'in', 'it', 'was']:
            stopwords.insert(word)
        for word in ['python']:
            exceptions.insert(word)
        text = "Python is great and in 2020 it was very popular."
        tokens = tokenize(text, stopwords, exceptions)
        self.assertEqual(tokens, ['python', 'great', 'veri', 'popular'])

    def test_tokenize_with_only_exceptions_and_no_stopwords(self):
        exceptions = Trie()
        for word in ['nlp', 'python', 'fun']:
            exceptions.insert(word)
        text = "NLP and Python are fun."
        tokens = tokenize(text, Trie(), exceptions)
        self.assertEqual(tokens, ['nlp', 'and', 'python', 'are', 'fun'])

    def test_tokenize_with_only_exceptions_and_and_stopword(self):
        stopwords = Trie()
        stopwords.insert('and')
        exceptions = Trie()
        for word in ['nlp', 'python', 'fun']:
            exceptions.insert(word)
        text = "NLP and Python are fun."
        tokens = tokenize(text, stopwords, exceptions)
        self.assertEqual(tokens, ['nlp', 'python', 'are', 'fun'])

    def test_tokenize_with_no_stopwords_or_exceptions(self):
        text = "Cats and dogs are animals."
        tokens = tokenize(text, Trie(), Trie())
        self.assertEqual(tokens, ['cat', 'and', 'dog', 'are', 'anim'])

if __name__ == "__main__":
    unittest.main()