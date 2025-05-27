class TrieNode:
    """
    TrieNode represents a single node in the Trie structure.
    Each node contains an array of children nodes and a boolean flag
    indicating if it marks the end of a word.
    """
    def __init__(self):
        # 27 - 26 litere mici + 1 pentru '{'
        # de ce `{` pentru ca 'z' + 1 = '{' in ASCII :) [Lab 4]
        # nu tine cont de numere
        self.children = [None] * 27 
        self.is_end = False

class Trie:
    """
    Trie is a data structure that allows for efficient storage and retrieval of strings.
    It supports insertion and search operations.
    """
    def __init__(self):
        self.root = TrieNode()

    def _char_to_index(self, ch):
        """
        Convert a character to an index in the children array.
        Args:
            ch (str): The character to convert.
        Returns:
            int: The index corresponding to the character.
        """
        return ord(ch) - ord('a') if ch.isalpha() else 26  # '{' va fi pe 26

    def insert(self, word):
        """
        Insert a word into the Trie.
        Args:
            word (str): The word to insert.
        """
        if not word:
            return #TODO: Throw an exception for empty words and handle it
        
        word = word.lower() + '{'
        node = self.root
        
        for ch in word:
            idx = self._char_to_index(ch)
            if not node.children[idx]:
                node.children[idx] = TrieNode()
            node = node.children[idx]

        node.is_end = True

    def search(self, word):
        """
        Search for a word in the Trie.
        Args:
            word (str): The word to search for.
        Returns:
            bool: True if the word exists in the Trie, False otherwise.
        """
        word = word.lower() + '{'
        node = self.root
        for ch in word:
            idx = self._char_to_index(ch)
            if not node.children[idx]:
                return False
            node = node.children[idx]
        return node.is_end
