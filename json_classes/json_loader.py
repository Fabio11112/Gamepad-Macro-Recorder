import json
from input_classes.input_type import Type
from input_classes.input import Input

class JsonLoader:

    def __init__(self, filename: str):
        self.record = []
        self.filename = filename
        self.inputs = None


    def load(self):
        with open(self.filename) as f:
            self.inputs = json.load(f)

        inputs = []
        for input in self.inputs:
            inputs.append(Input(input))

        self.inputs = inputs

    def getInputs(self)-> list[object]:
        return self.inputs

        

