from collections.abc import Iterator
from input.input import Input


class InputIterator(Iterator):

    def __init__(self, collection: list[Input]):
        self._position = -1
        self._collection = collection
        self._length = len(collection)

    def hasNext(self) -> bool:
        return self._position + 1 < self._length
    
    def __next__(self) -> Input:
        return self.next()

    def next(self) -> Input:
        if(not self.hasNext()):
            raise StopIteration("There are no more elements in the iterator")
        
        self._position = self._position + 1
        return self._collection[self._position]
        