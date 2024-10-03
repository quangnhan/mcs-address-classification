from .base import SearchStrategy

class ExactMatchStrategy(SearchStrategy):
    def __init__(self, words: list[str]):
        super().__init__(words)

    def search(self, word):
        for _word in self.words:
            if _word == word:
                return _word
        return ""
