import json
from input_classes.input_type import Type
from input_classes.input import Input

class JsonRecorder:

    def __init__(self, filename: str):
        self.record = []
        self.filename = filename
        self.json = None

    def append(self, input: Input):
        self.record.append(input.to_dict())
        print(f"{input.to_dict()}\n")

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.record, f, indent=4)
