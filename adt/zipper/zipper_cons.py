from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from adt.cons import Cons
from adt.zipper.base_zipper import BaseContext, BaseContexts, BaseZipper

T = TypeVar('T')


@dataclass(frozen=True)
class ConsContext(BaseContext):
    node: T


@dataclass(frozen=True)
class ConsContexts(BaseContexts, ConsContext):
    rec: ConsContexts = None

    @property
    def context(self):
        return ConsContext(self.node)

    def __str__(self):
        return 'Cons contexts:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class ZipperCons(BaseZipper):
    cons: Cons
    contexts: ConsContexts

    @property
    def _body(self) -> Cons:
        return self.cons

    @property
    def _contexts(self) -> ConsContexts:
        return self.contexts

    @property
    def bottom(self):
        if not self.cons.cdr:
            return True
        return False

    @classmethod
    def from_cons(cls, cons: Cons):
        return cls(cons=cons, contexts=None)

    def go_up(self) -> ZipperCons:
        if self.top:
            return self
        return type(self)(
            type(self.cons)(self.contexts.node, self.cons),
            self.contexts.rec,
        )

    def go_down(self, *args, **kwargs) -> ZipperCons:
        if self.bottom:
            return self
        return type(self)(
            self.cons.cdr,
            ConsContexts(self.cons.car, self.contexts),
        )

    def go_down_most(self, *args, **kwargs) -> ZipperCons:
        if self.bottom:
            return self
        return self.go_down().go_down_most()

    def __len__(self):
        return self.go_down_most().depth + 1

    def get_item_int(self, item: int, reverse=False):
        if item == 0:
            return self.cons.car
        if item < 0 and not reverse:
            return self.go_down_most().get_item_int(item + 1, True)
        if item > 0 and not reverse:
            if item == 0:
                return self.go_up_most().cons.car
            if self.bottom:
                raise IndexError("Index out of range")
            return self.go_down().get_item_int(item - 1)
        if self.bottom:
            raise IndexError("Index out of range")
        return self.go_up().get_item_int(item + 1, reverse)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return type(self.cons).constr(
                (self.get_item_int(i)
                 for i in range(*item.indices(self.__len__()))))
        if isinstance(item, int):
            return self.get_item_int(item)
        raise TypeError("Invalid argument type")

    def __add__(self, other) -> ZipperCons:
        if isinstance(other, ZipperCons):
            left = self.go_down_most()
            right = other.go_up_most()
            return type(self)(
                cons=Cons(car=left.cons.car, cdr=right.cons),
                contexts=left.contexts,
            )
        if isinstance(other, Cons):
            left = self.go_down_most()
            return type(self)(
                cons=Cons(car=left.cons.car, cdr=other),
                contexts=left.contexts,
            )
        raise TypeError("Invalid argument type")
