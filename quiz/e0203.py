# -*- coding: utf-8 -*-
"""Remove Linked List Elements

Remove all elements from a linked list of integers that have value val.

Example:

Input:  1->2->6->3->4->5->6, val = 6
Output: 1->2->3->4->5

"""

from __future__ import annotations
from collections.abc import Sequence
from functools import reduce
from itertools import chain
from typing import Iterator, NamedTuple, Union


class LL(NamedTuple):
    head: int
    tail: Union[LL, None] = None

    def __iter__(self):
        h = self.head
        t = self.tail
        while True:
            yield h
            if not t:
                break
            h, t = t.head, t.tail

    def __repr__(self):
        return reduce(lambda s1, s2: s1 + ' -> ' + s2,
                      chain(map(str, self.__iter__()), iter(('None', ))))

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def compose(seq: Sequence[int, ...]) -> LL:
        def helper(sq: Iterator[int, ...], rec: Union[LL, None]) -> LL:
            rec_ = rec
            for i in sq:
                rec_ = LL(head=i, tail=rec_)
            return rec_

        return helper(reversed(seq), None)

    def solution(self, val):
        it = iter(self)
        return LL.compose(list(filter(lambda x: x != val, it)))


if __name__ == '__main__':
    ll1 = LL(head=1,
             tail=LL(head=2,
                     tail=LL(head=6,
                             tail=LL(head=3,
                                     tail=LL(head=4,
                                             tail=LL(head=5,
                                                     tail=LL(head=6)))))))
    exp1_str = '1 -> 2 -> 3 -> 4 -> 5 -> None'

    assert exp1_str == str(ll1.solution(6))
