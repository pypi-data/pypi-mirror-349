from __future__ import annotations
import functools
import itertools
import more_itertools
from pprint import pprint
from typing import IO, Callable, Iterable, Iterator, Literal, TypeVar, Any

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

class Pipeline(Iterable[T]):
    """Fluent wrapper around a list.
    
    >>> (Pipeline(range(10))
    ... .filter(lambda x: x % 2 == 0)
    ... .map(lambda x: x * x)
    ... .sum())                      
    120
    """

    def __init__(self, iterable: Iterable[T]) -> None:
        """
        >>> Pipeline([x for x in range(5)]).to_list()
        [0, 1, 2, 3, 4]
        """
        self._data = list(iterable)

    def map(self, fn: Callable[[T], U]) -> Pipeline[U]:
        """
        >>> Pipeline([1, 2, 3]).map(lambda x: x * 2).to_list()
        [2, 4, 6]
        """
        return Pipeline(map(fn, self._data))

    def filter(self, pred: Callable[[T], bool]) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).to_list()
        [2, 4]
        """
        return Pipeline(filter(pred, self._data))

    def zip(self, other: Iterable[U]) -> Pipeline[tuple[T, U]]:
        """
        >>> Pipeline([1, 2]).zip([10, 20]).to_list()
        [(1, 10), (2, 20)]
        """
        return Pipeline(zip(self._data, other, strict=True))

    def zip_longest(self, other: Iterable[U], fillvalue: V) -> Pipeline[tuple[T | V, U | V]]:
        """
        >>> Pipeline([1, 2]).zip_longest([10, 20, 30], fillvalue=None).to_list()
        [(1, 10), (2, 20), (None, 30)]
        
        >>> Pipeline([1, 2, 3]).zip_longest([10, 20], fillvalue=0).to_list()
        [(1, 10), (2, 20), (3, 0)]
        """
        return Pipeline(itertools.zip_longest(self._data, other, fillvalue=fillvalue))

    def zip_with(self, fn: Callable[[T, U], V], other: Iterable[U]) -> Pipeline[V]:
        """
        >>> Pipeline([1, 2]).zip_with(lambda a, b: a + b, [10, 20]).to_list()
        [11, 22]
        """
        return Pipeline(fn(a, b) for a, b in zip(self._data, other, strict=True))

    def zip_tuples_with(self, fn: Callable[[T, U], V]) -> Pipeline[V]:
        """
        >>> Pipeline([(1, 2), (3, 4)]).zip_tuples_with(lambda a, b: a + b).to_list()
        [3, 7]
        """
        if not all(isinstance(item, tuple) and len(item) == 2 for item in self._data):
            raise ValueError("zip_tuples_with requires an iterable of tuples with 2 elements")
        return Pipeline(itertools.starmap(fn, self._data)) # type: ignore

    def sort(self, key: Callable[[T], Any] | None = None, reverse: bool = False) -> Pipeline[T]:
        """
        >>> Pipeline([3, 1, 2]).sort().to_list()
        [1, 2, 3]
        
        >>> Pipeline([3, 1, 2]).sort(reverse=True).to_list()
        [3, 2, 1]
        """
        return Pipeline(sorted(self._data, key=key, reverse=reverse))  # type: ignore

    def unique(self) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 2, 3]).unique().to_list()
        [1, 2, 3]
        """
        return Pipeline(dict.fromkeys(self._data))
    
    def slice(self, start: int = 0, end: int | None = None, step: int = 1) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3, 4, 5]).slice(1, 4).to_list()
        [2, 3, 4]
        """
        if end is None:
            end = len(self._data)
        return Pipeline(self._data[start:end:step])

    def take(self, n: int) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3, 4]).take(2).to_list()
        [1, 2]
        """
        return Pipeline(self._data[:n])
    
    def drop(self, n: int) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3, 4]).drop(2).to_list()
        [3, 4]
        """
        return Pipeline(self._data[n:])

    def enumerate(self, start: int = 0) -> Pipeline[tuple[int, T]]:
        """
        >>> Pipeline(['a', 'b']).enumerate().to_list()
        [(0, 'a'), (1, 'b')]
        """
        return Pipeline(enumerate(self._data, start))

    def batch(self, n: int, strict: bool = False, pipelines: bool = True) -> Pipeline[Iterable[T]]:
        """
        >>> Pipeline(range(1, 6)).batch(2)
        Pipeline([Pipeline([1, 2]), Pipeline([3, 4]), Pipeline([5])])
        
        >>> Pipeline(range(1, 6)).batch(2, pipelines=False)
        Pipeline([[1, 2], [3, 4], [5]])
        """
        if pipelines:
            return Pipeline([Pipeline(batch) for batch 
                             in more_itertools.chunked(self._data, n, strict=strict)])
        else:
            return Pipeline(more_itertools.chunked(self._data, n, strict=strict))
    
    def batch_fill(self, n: int, 
                   fillvalue: U,
                   incomplete: Literal['fill', 'ignore', 'strict'] = 'fill',
                   pipelines: bool = True) -> Pipeline[Iterable[T | U]]:
        """
        >>> Pipeline(range(1, 6)).batch_fill(2, fillvalue=0)
        Pipeline([Pipeline([1, 2]), Pipeline([3, 4]), Pipeline([5, 0])])
        
        >>> Pipeline(range(1, 6)).batch_fill(2, fillvalue=0, pipelines=False)
        Pipeline([[1, 2], [3, 4], [5, 0]])
        """
        if pipelines:
            return Pipeline([Pipeline(row) for row 
                    in more_itertools.grouper(self._data, n, 
                                              incomplete=incomplete, 
                                              fillvalue=fillvalue)])
        else:
            return Pipeline([list(row) for row 
                    in more_itertools.grouper(self._data, n, 
                                            incomplete=incomplete, 
                                            fillvalue=fillvalue)])

    def flatten(self: Pipeline[Iterable[T]]) -> Pipeline[T]:
        """
        >>> Pipeline([[1, 2], [3, 4]]).flatten().to_list()
        [1, 2, 3, 4]
        """
        if not all(isinstance(item, Iterable) for item in self._data):
            raise ValueError("flatten requires an iterable of iterables")
        return Pipeline(itertools.chain.from_iterable(self._data))

    def for_each(self, fn: Callable[[T], None]) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3]).for_each(print).to_list()
        1
        2
        3
        [1, 2, 3]
        """
        for item in self._data:
            fn(item)
        return self

    def print(self, label: str = "", 
              label_only: bool = False,
              end: str | None = "\n",
              file: IO[str] | None = None,
              flush: bool = False) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3]).print("Numbers: ", end="\\n\\n")
        Numbers: Pipeline([1, 2, 3])
        <BLANKLINE>
        Pipeline([1, 2, 3])
        
        >>> Pipeline([1, 2, 3]).print("Numbers:", label_only=True)
        Numbers:
        Pipeline([1, 2, 3])
        """
        if label_only:
            print(label, end=end, file=file, flush=flush)
        else:
            print(f"{label}{self}", end=end, file=file, flush=flush)
        return self

    def pprint(self, label: str = "", 
               stream: IO[str] | None = None, 
               indent: int = 1, width: int = 80, 
               depth: int | None = None, 
               compact: bool = False, 
               sort_dicts: bool = True, 
               underscore_numbers: bool = False) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3]).pprint("Numbers:")
        Numbers:
        [1, 2, 3]
        Pipeline([1, 2, 3])
        """
        if label:
            print(label)
        pprint(self._data, stream=stream, indent=indent, width=width,
               depth=depth, compact=compact, sort_dicts=sort_dicts,
               underscore_numbers=underscore_numbers)
        return self

    # === Terminal methods ===

    def to_list(self) -> list[T]:
        """
        >>> Pipeline([1, 2, 3]).to_list()
        [1, 2, 3]
        """
        return self._data.copy()

    def first(self) -> T:
        """
        >>> Pipeline([1, 2, 3]).first()
        1
        """
        if not self._data:
            raise IndexError("Pipeline is empty")
        return self._data[0]
    
    def last(self) -> T:
        """
        >>> Pipeline([1, 2, 3]).last()
        3
        """
        if not self._data:
            raise IndexError("Pipeline is empty")
        return self._data[-1]

    def reduce(self, fn: Callable[[V, T], V], initial: V) -> V:
        """
        >>> Pipeline([104, 101, 108, 108, 111]).reduce(lambda acc, x: acc + chr(x), "")     
        'hello'
        """
        return functools.reduce(fn, self._data, initial)

    def reduce_non_empty(self, fn: Callable[[T, T], T]) -> T:
        """
        >>> Pipeline([1, 2, 3]).reduce_non_empty(lambda acc, x: acc + x)
        6
        """
        if not self._data:
            raise ValueError("Pipeline is empty")
        return functools.reduce(fn, self._data)

    def len(self) -> int:
        """
        >>> Pipeline([1, 2, 3]).len()
        3
        """
        return len(self._data)
    
    def min(self) -> T:
        """
        >>> Pipeline([3, 1, 2]).min()
        1
        """
        return min(self._data)  # type: ignore
    
    def max(self) -> T:
        """
        >>> Pipeline([3, 1, 2]).max()
        3
        """
        return max(self._data)  # type: ignore
    
    def sum(self) -> T:
        """
        >>> Pipeline([1, 2, 3]).sum()
        6
        """
        return sum(self._data)  # type: ignore
    
    def any(self) -> bool:
        """
        >>> Pipeline([False, False, True]).any()
        True
        
        >>> Pipeline([False, False, False]).any()
        False
        """
        return any(self._data)
    
    def all(self) -> bool:
        """
        >>> Pipeline([True, True, True]).all()
        True
        
        >>> Pipeline([True, False, True]).all()
        False
        """
        return all(self._data)
    
    def contains(self, item: T) -> bool:
        """
        >>> Pipeline([1, 2, 3]).contains(2)
        True
        
        >>> Pipeline([1, 2, 3]).contains(4)
        False
        """
        return item in self._data

    # === Wrapped list methods ===

    def append(self, item: T) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2]).append(3).to_list()
        [1, 2, 3]
        """
        return Pipeline(self._data + [item])

    def extend(self, items: Iterable[T]) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2]).extend([3, 4]).to_list()
        [1, 2, 3, 4]
        """
        return Pipeline(self._data + list(items))
    
    def insert(self, index: int, item: T) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 4]).insert(2, 3).to_list()
        [1, 2, 3, 4]
        """
        self._data.insert(index, item)
        return Pipeline(self._data)
    
    def remove(self, item: T) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3]).remove(2).to_list()
        [1, 3]
        """
        self._data.remove(item)
        return Pipeline(self._data)
    
    def index(self, item: T) -> int:
        """
        >>> Pipeline(['a', 'b', 'c']).index('b')
        1
        """
        return self._data.index(item)
    
    def count(self, item: T) -> int:
        """
        >>> Pipeline([1, 2, 2, 3]).count(2)
        2
        """
        return self._data.count(item)
    
    def reverse(self) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2, 3]).reverse().to_list()
        [3, 2, 1]
        """
        return Pipeline(reversed(self._data))

    # === Dunder methods ===

    def __eq__(self, other: object) -> bool:
        """
        >>> Pipeline([1, 2, 3]) == Pipeline([1, 2, 3])
        True
        
        >>> Pipeline([1, 2]) == Pipeline([2, 1])
        False
        """
        if not isinstance(other, Pipeline):
            return False
        return self._data == other._data 

    def __str__(self) -> str:
        """
        >>> str(Pipeline([1, 2, 3]))
        'Pipeline([1, 2, 3])'
        """
        return f"Pipeline({self._data})"

    def __repr__(self) -> str:
        """
        >>> Pipeline([1, 2, 3])
        Pipeline([1, 2, 3])
        """
        return str(self)

    def __iter__(self) -> Iterator[T]:
        """
        >>> list(Pipeline([1, 2, 3]))
        [1, 2, 3]
        """
        return iter(self._data)

    def __len__(self) -> int:
        """
        >>> len(Pipeline([1, 2, 3]))
        3
        """
        return len(self._data)
    
    def __getitem__(self, index: int) -> T:
        """
        >>> Pipeline([1, 2, 3])[1]
        2
        """
        return self._data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """
        >>> p = Pipeline([1, 2, 3])
        >>> p[1] = 4
        >>> p.to_list()
        [1, 4, 3]
        """
        self._data[index] = value
        
    def __delitem__(self, index: int) -> None:
        """
        >>> p = Pipeline([1, 2, 3])
        >>> del p[1]
        >>> p.to_list()
        [1, 3]
        """
        del self._data[index]
        
    def __contains__(self, item: T) -> bool:
        """
        >>> 2 in Pipeline([1, 2, 3])
        True
        
        >>> 4 in Pipeline([1, 2, 3])
        False
        """
        return item in self._data
    
    def __reversed__(self) -> Iterator[T]:
        """
        >>> list(reversed(Pipeline([1, 2, 3])))
        [3, 2, 1]
        """
        return reversed(self._data)
    
    def __add__(self, other: Iterable[T]) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2]) + Pipeline([3, 4])
        Pipeline([1, 2, 3, 4])
        """
        return Pipeline(self._data + list(other))
    
    def __mul__(self, n: int) -> Pipeline[T]:
        """
        >>> Pipeline([1, 2]) * 2
        Pipeline([1, 2, 1, 2])
        """
        return Pipeline(self._data * n)

        

if __name__ == "__main__":
    # Interpreter usage: 
    # from importlib import reload; import oa_utils.pipeline; reload(oa_utils.pipeline); from oa_utils.pipeline import Pipeline
    import doctest
    doctest.testmod()
    