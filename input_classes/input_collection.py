from collections.abc import Iterable
from input_classes.input import Input
from input_classes.input_iterator import InputIterator

class InputCollection(Iterable):
    def __init__(self, collection: list[Input]):
        self.collection = collection

    def __getitem__(self, index:int)-> Input:
        return self.collection[index]
    
    def __iter__(self) -> InputIterator:
        return InputIterator(self.collection)
    
    def get_iterator(self) -> InputIterator:
        return InputIterator(self.collection)