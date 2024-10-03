from .base import Database

class ProvinceDB(Database):
    def __init__(self):
        super().__init__()
        self.file_path = "./data/list_province.txt"