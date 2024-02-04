"""Reverse Linked List."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class LinkedList:
    value: T
    tail: Optional[LinkedList]

    @staticmethod
    def from_seq(seq: Sequence[T]):
        def helper(seq_: Sequence[T], acc: Optional[LinkedList]):
            if not seq_:
                return acc
            return helper(seq_[1:], LinkedList(seq_[0], acc))

        return helper(list(reversed(seq)), None)

    def __iter__(self):
        v = self.value
        t = self.tail
        while True:
            yield v
            if not t:
                break
            v, t = t.value, t.tail

    def __repr__(self):
        return ' -> '.join((*map(str, self.__iter__()), 'None'))

    def __str__(self):
        return self.__repr__()


class Status(Enum):
    DOING = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    body: Optional[LinkedList]
    acc: Optional[LinkedList]

    @property
    def status(self):
        if not self.body:
            return Status.DONE
        return Status.DOING


class ReverseList:
    @staticmethod
    def transform(fsm: FSM) -> FSM:
        assert fsm.status == Status.DOING
        value = fsm.body.value
        return FSM(fsm.body.tail, LinkedList(value, fsm.acc))

    def looper(self, fsm: FSM) -> FSM:
        if fsm.status == Status.DONE:
            return fsm
        return self.looper(self.transform(fsm))

    def solution(self, seq: LinkedList) -> LinkedList:
        fsm = FSM(seq, None)
        return self.looper(fsm).acc


if __name__ == '__main__':
    ipt_1 = LinkedList(1, LinkedList(2, LinkedList(3, None)))
    exp_1 = LinkedList.from_seq([3, 2, 1])
    ipt_2 = LinkedList.from_seq([2, 4, 6, 0, 1])
    exp_2 = LinkedList.from_seq([1, 0, 6, 4, 2])

    r = ReverseList()
    assert r.solution(ipt_1) == exp_1
    assert r.solution(ipt_2) == exp_2
