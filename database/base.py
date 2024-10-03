from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self):
        self.file_path = ""
        self.location_mapping = {}

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            # Read all lines at once
            locations = file.readlines()

        for location in locations:
            # Preprocessing db
            origin_location = location.strip()
            converted_location = origin_location.lower()

            # Add to mapping
            self.location_mapping[converted_location] = origin_location