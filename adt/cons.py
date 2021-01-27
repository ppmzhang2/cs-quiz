from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Sequence, TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True)
class Cons(Generic[T]):
    """
    Immutable Linked List
    """
    car: T
    cdr: Cons[T] = None

    def traversal(self) -> Sequence[T]:
        rec = self
        while rec is not None:
            yield rec.car
            rec = rec.cdr

    @classmethod
    def constr_reverse(cls, it: Sequence[T]):
        return reduce(lambda x1, x2: cls(x2, x1), it, None)

    def __reversed__(self):
        return (type(self)).constr_reverse(self.traversal())

    @classmethod
    def constr(cls, it: Sequence[T]):
        return cls.constr_reverse(it).__reversed__()
