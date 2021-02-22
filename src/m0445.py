"""Add Two Numbers II
TAG: linked-list

You are given two non-empty linked lists representing two non-negative
integers. The most significant digit comes first and each of their nodes
contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the
number 0 itself.

Follow up:

What if you cannot modify the input lists? In other words, reversing the lists
is not allowed.

Example:

* Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
* Output: 7 -> 8 -> 0 -> 7
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class Cons:
    car: int
    cdr: Optional[Cons]

    @classmethod
    def from_seq(cls, seq: Sequence[int]) -> Optional[Cons]:
        def helper(seq: Sequence[int], acc: Optional[Cons]) -> Optional[Cons]:
            while True:
                if not seq:
                    return acc
                seq, acc = seq[1:], cls(seq[0], acc)

        return helper(tuple(reversed(seq)), None)

    @classmethod
    def from_int(cls, num: int) -> Optional[Cons]:
        seq_int = [int(c) for c in tuple(str(num))]
        return cls.from_seq(seq_int)

    @property
    def integer(self) -> int:
        def helper(cons: Cons, acc: int) -> int:
            while True:
                if not cons:
                    return acc
                cons, acc = cons.cdr, acc * 10 + cons.car

        return helper(self, 0)

    def add(self, cons: Cons) -> Cons:
        integer = self.integer + cons.integer
        return self.from_int(integer)


if __name__ == '__main__':
    ipt_1_1 = 7243
    ipt_1_2 = 564
    exp_1 = 7807

    # print(Cons.from_seq([2, 4, 6, 0, 1]))
    # print(Cons.from_int(24601))
    # print(Cons.from_seq([2, 4, 6, 0, 1]).integer)

    cons_1 = Cons.from_int(ipt_1_1)
    cons_2 = Cons.from_int(ipt_1_2)
    assert exp_1 == cons_1.add(cons_2).integer
