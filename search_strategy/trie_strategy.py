from .base import SearchStrategy

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

class TrieStrategy(SearchStrategy):
    def __init__(self, words: list[str]):
        super().__init__(words)

        # Create tree
        self.trie = Trie()
        for _word in self.words:
            self.trie.insert(_word)

    def search(self, word):
        if self.trie.search(word):
            return word
        return ""
