import json
from input_type import Type
from input import Input

class JsonLoader:

    def __init__(self, filename: str):
        self.record = []
        self.filename = filename
        self.json = None

        with open(filename, "r") as f:
            self.json = json.load(filename)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.record, f, indent=4)
