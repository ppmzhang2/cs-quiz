"""Reverse Linked List II
TAG: linked-list

Reverse a linked list from position m to n. Do it in one-pass.

Note: 1 ≤ m ≤ n ≤ length of list.

Example:

Input: 1->2->3->4->5->NULL, m = 2, n = 4
Output: 1->4->3->2->5->NULL

RELATED: 0206
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Tuple, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class LinkedList:
    value: T
    tail: Optional[LinkedList]

    @classmethod
    def from_seq(cls, seq: Sequence[T]):
        def helper(seq_: Sequence[T], acc: Optional[LinkedList]):
            if not seq_:
                return acc
            return helper(seq_[:-1], LinkedList(seq_[-1], acc))

        return helper(seq, None)

    def __iter__(self):
        v = self.value
        t = self.tail
        while True:
            yield v
            if not t:
                break
            v, t = t.value, t.tail

    def __repr__(self):
        return '[' + ', '.join((*map(str, iter(self)), 'None')) + ']'

    def __str__(self):
        return self.__repr__()

    def __reversed__(self):
        def helper(
            ll: Optional[LinkedList],
            acc: Optional[LinkedList],
        ) -> Optional[LinkedList]:
            if not ll:
                return acc
            return helper(ll.tail, LinkedList(ll.value, acc))

        return helper(self, None)


@dataclass(frozen=True)
class ZipperLList:
    seq: LinkedList
    zipper: Optional[LinkedList]

    @classmethod
    def from_linked_list(cls, ll: LinkedList):
        return ZipperLList(ll, None)

    @property
    def top(self):
        return self.zipper is None

    @property
    def bottom(self):
        return self.seq is None

    def go_up(self):
        if self.top:
            raise IndexError('cannot go up anymore')
        return type(self)(
            LinkedList(self.zipper.value, self.seq),
            self.zipper.tail,
        )

    def go_down(self):
        if self.bottom:
            raise IndexError('cannot go down anymore')
        return type(self)(
            self.seq.tail,
            LinkedList(self.seq.value, self.zipper),
        )

    def go_up_most(self):
        if self.top:
            return self
        return self.go_up().go_up_most()

    def go_down_most(self):
        if self.bottom:
            return self
        return self.go_down().go_down_most()

    def split(
        self,
        idx: int,
    ) -> Tuple[Optional[ZipperLList], Optional[ZipperLList]]:
        def helper(zl: ZipperLList, idx: int):
            if idx <= 0:
                return (
                    ZipperLList.from_linked_list(reversed(zl.zipper)),
                    ZipperLList.from_linked_list(zl.seq),
                )
            return helper(zl.go_down(), idx - 1)

        return helper(self, idx)

    def append(self, element: T) -> ZipperLList:
        zl = self.go_down_most()
        return ZipperLList(
            LinkedList(element, None),
            zl.zipper,
        )

    def chain(self, appendee: ZipperLList) -> ZipperLList:
        self_bottom = self.go_down_most()
        appendee_top = appendee.go_up_most()
        return ZipperLList(
            appendee_top.seq,
            self_bottom.zipper,
        )


class Status(Enum):
    DOING = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    prefix: Optional[ZipperLList]
    body: Optional[ZipperLList]
    suffix: Optional[ZipperLList]
    acc: Optional[ZipperLList]

    @property
    def status(self):
        if not self.body.seq:
            return Status.DONE
        return Status.DOING


class ReverseList:
    @staticmethod
    def split_three(
        zl: ZipperLList,
        idx1: int,
        idx2: int,
    ) -> Tuple[ZipperLList, ZipperLList, ZipperLList]:
        prefix, remaining = zl.split(idx1)
        body, suffix = remaining.split(idx2 - idx1)
        return prefix, body, suffix

    @staticmethod
    def transform(fsm: FSM) -> FSM:
        assert fsm.status == Status.DOING
        value = fsm.body.seq.value
        return FSM(
            fsm.prefix,
            ZipperLList.from_linked_list(fsm.body.seq.tail),
            fsm.suffix,
            ZipperLList.from_linked_list(LinkedList(value, fsm.acc.seq)),
        )

    def looper(self, fsm: FSM) -> FSM:
        if fsm.status == Status.DONE:
            return fsm
        return self.looper(self.transform(fsm))

    def solution(self, seq: LinkedList, m: int, n: int) -> LinkedList:
        prefix, body, suffix = self.split_three(
            ZipperLList.from_linked_list(seq), m, n)
        fsm = FSM(prefix, body, suffix, ZipperLList.from_linked_list(None))
        res = self.looper(fsm)
        return res.prefix.chain(res.acc).chain(res.suffix).go_up_most().seq


if __name__ == '__main__':
    ipt_1_1 = LinkedList.from_seq([2, 4, 6, 0, 1])
    ipt_1_2 = 2
    ipt_1_3 = 4
    exp_1 = LinkedList.from_seq([2, 4, 0, 6, 1])

    rl = ReverseList()

    assert rl.solution(ipt_1_1, 2, 4) == exp_1
