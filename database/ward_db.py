from .base import Database

class WardDB(Database):
    def __init__(self):
        super().__init__()
        self.file_path = "./data/list_ward.txt"