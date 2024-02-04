"""Add Two Numbers

You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order and each of their nodes contain a single
digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the
number 0 itself.

Example

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.

"""

from __future__ import annotations
from collections import defaultdict
from functools import reduce
from itertools import zip_longest
from typing import Iterator, Optional, Set, Iterable, NamedTuple
from adt.cons import Cons


class Num(Cons):
    class SparseNum(NamedTuple):
        idx: int
        value: int

    def __new__(cls, car: int, cdr: int = None):
        return super(Num, cls).__new__(cls, car=car, cdr=cdr)

    @staticmethod
    def __sum_iter(it: Iterator[int]) -> int:
        return reduce(lambda x1, x2: x1 + x2,
                      map(lambda x: x[1] * 10**x[0], enumerate(it)))

    def sum(self) -> int:
        return Num.__sum_iter(self.traversal())

    @classmethod
    def constr_sparse(cls, s: Set[Optional[SparseNum]]):
        if not s:
            return None
        max_idx = max(s, key=lambda x: x.idx).idx
        dd = defaultdict(int)
        for sn in s:
            dd[sn.idx] = sn.value
        return cls.constr((dd[i] for i in range(max_idx + 1)))

    def add(self, num: Num):
        sums = tuple(x1 + x2 for x1, x2 in zip_longest(
            self.traversal(), num.traversal(), fillvalue=0))

        def helper(it: Iterable[int]):
            def _carry(itr):
                return (0 if x < 10 else 1 for x in itr)

            def _add(itr):
                return (x if x < 10 else x - 10 for x in itr)

            carries = set(
                map(lambda x: Num.SparseNum(idx=x[0], value=x[1]),
                    filter(lambda i: i[1] == 1, enumerate(_carry(it), 1))))
            if not carries:
                return (type(self)).constr(_add(it))
            else:
                num_carry = (type(self)).constr_sparse(carries)
                return helper([
                    x1 + x2 for x1, x2 in zip_longest(
                        _add(it), num_carry.traversal(), fillvalue=0)
                ])

        return helper(sums)


if __name__ == '__main__':
    n1 = Num(2, Num(4, Num(3)))
    n2 = Num(5, Num(6, Num(4)))
    assert n1.add(n2).sum() == 807
