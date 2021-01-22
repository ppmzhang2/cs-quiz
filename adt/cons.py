from __future__ import annotations

from functools import reduce
from typing import Any, Iterator, NamedTuple


class Cons(NamedTuple):
    """
    Immutable Linked List
    """
    car: Any
    cdr: Cons = None

    def traversal(self) -> Iterator[Any]:
        rec = self
        while rec is not None:
            yield rec.car
            rec = rec.cdr

    @classmethod
    def constr_reverse(cls, it: Iterator[Any]):
        return reduce(lambda x1, x2: cls(x2, x1), it, None)

    def __reversed__(self):
        return (type(self)).constr_reverse(self.traversal())

    @classmethod
    def constr(cls, it: Iterator[Any]):
        return cls.constr_reverse(it).__reversed__()
