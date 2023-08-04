from itertools import chain
from typing import Any, Union, Sequence, Iterable, List, Callable, Tuple


class funclist(list):
    """A wrapped implementation of the regular Python list
    inspired by Rust Vectors."""

    def __init__(self, *items: Union[Iterable, Sequence]):
        if len(items) == 1 and hasattr(items, '__iter__'):
            super().__init__(item for item in items[0])
        else:
            super().__init__(items)

    def append(self, item: Any) -> List:
        super().append(item)
        return self
    
    def remove(self, item) -> List:
        super().remove(item)
        return self

    def extend(self, iterable) -> List:
        super().extend(iterable)
        return self

    def pop(self, item) -> List:
        super().pop(item)
        return self

    def sort(self) -> List:
        super().sort()
        return self

    def insert(self, idx, item) -> List:
        super().insert(idx, item)
        return self

    def reverse(self) -> List:
        super().reverse()
        return self
    
    def select(self, idx: Sequence) -> List:
        self._check_where_indices(idx)
        return funclist(map(self.__getitem__, idx))
      
    def filter(self, f: Callable):
        return funclist(filter(f, self)) 
    
    def flatten(self) -> List:
        self._check_not_1d()
        return funclist(chain(*self))
    
    def enumerate(self) -> List[Tuple]:
        return funclist(
            (i, item) for i, item in zip(range(len(self)), self)
        )

    def windows(self, window_size: int) -> List[List]:
        return funclist(
            [tuple(self[i:i+window_size]) for i in range(len(self) - window_size + 1)]
        )

    def map(self, f: Callable):
        return funclist(map(f, self))
    
    def dedupe(self):
        return funclist(set(self))
    
    def _check_where_indices(self, indices: Sequence):
        try:
            assert max(indices) <= len(self) and min(indices) >= 0
        except AssertionError as e:
            e.args = e.args + ("Indices are out of bounds.",)
            raise e
    
    def _check_not_1d(self):
        try:
            assert all(isinstance(l, list) for l in self)
        except AssertionError as e:
            e.args = e.args + ("Can't flatten a 1d list.")
            raise e