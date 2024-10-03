from .base import Database

class DistrcitDB(Database):
    def __init__(self):
        super().__init__()
        self.file_path = "./data/list_district.txt"