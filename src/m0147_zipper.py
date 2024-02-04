"""Insertion Sort List with Zipper."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class LinkedList:
    car: int
    cdr: Optional[LinkedList]

    @staticmethod
    def from_list(seq: Sequence[int]):
        def helper(seq: tuple[int, ...], acc: Optional[LinkedList]):
            while True:
                if not seq:
                    return acc
                seq, acc = seq[1:], LinkedList(seq[0], acc)

        return helper(tuple(reversed(seq)), None)

    def __iter__(self):
        ll = self
        while True:
            if ll is None:
                break
            yield ll.car
            ll = ll.cdr

    def __str__(self):
        return ' -> '.join(str(i) for i in self)

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class ZippedLinkedList:
    llist: Optional[LinkedList]
    contexts: Optional[LinkedList]

    @staticmethod
    def from_linked_list(ll: LinkedList):
        return ZippedLinkedList(ll, None)

    @property
    def top(self) -> bool:
        return self.contexts is None

    @property
    def bottom(self) -> bool:
        return self.llist is None

    def go_up(self) -> ZippedLinkedList:
        if self.top:
            return self
        new_car = self.contexts.car
        new_contexts = self.contexts.cdr
        new_llist = LinkedList(new_car, self.llist)
        return (type(self))(new_llist, new_contexts)

    def go_down(self) -> ZippedLinkedList:
        if self.bottom:
            return self
        new_context = self.llist.car
        new_contexts = LinkedList(new_context, self.contexts)
        new_llist = self.llist.cdr
        return (type(self))(new_llist, new_contexts)

    def go_top(self) -> ZippedLinkedList:
        zll = self
        while True:
            if zll.top:
                return zll
            zll = zll.go_up()

    def go_bottom(self) -> ZippedLinkedList:
        zll = self
        while True:
            if zll.bottom:
                return zll
            zll = zll.go_down()

    def insert(self, num: int) -> ZippedLinkedList:
        new_llist = LinkedList(num, self.llist)
        return (type(self))(new_llist, self.contexts)

    @property
    def value(self) -> int:
        if self.bottom:
            return None
        return self.llist.car


@dataclass(frozen=True)
class FSM:
    llist: Optional[LinkedList]
    zlist: ZippedLinkedList

    @property
    def done(self) -> bool:
        return self.llist is None

    def transform(self) -> FSM:
        new_element = self.llist.car
        new_llist = self.llist.cdr
        zlist = self.zlist.go_top()
        while True:
            if (zlist.value is None or new_element < zlist.value
                    or zlist.bottom):
                zlist = zlist.insert(new_element)
                break
            zlist = zlist.go_down()
        return FSM(new_llist, zlist.go_top())


class InsertionSortList:
    @staticmethod
    def looper(fsm: FSM):
        fsm_ = fsm
        while True:
            if fsm_.done:
                return fsm_.zlist.llist
            fsm_ = fsm_.transform()

    def solution(self, llist: LinkedList):
        fsm = FSM(llist, ZippedLinkedList(None, None))
        return self.looper(fsm)


if __name__ == '__main__':
    ipt_1 = LinkedList.from_list([2, 4, 6, 0, 1])
    exp_1 = LinkedList.from_list([0, 1, 2, 4, 6])
    ipt_2 = LinkedList.from_list([2, 4, 6, 0, 1, 9, 5, 3, 8, 7])
    exp_2 = LinkedList.from_list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    isl = InsertionSortList()

    assert isl.solution(ipt_1) == exp_1
    assert isl.solution(ipt_2) == exp_2
