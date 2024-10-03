from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    def __init__(self, words: list[str]):
        self.words = words

    @abstractmethod
    def search(self, word: str):
        pass
