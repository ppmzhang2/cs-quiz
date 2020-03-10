# -*- coding: utf-8 -*-
"""Reverse Linked List

Reverse a singly linked list.

Example:

Input: 1->2->3->4->5->NULL Output: 5->4->3->2->1->NULL Follow up:

A linked list can be reversed either iteratively or recursively. Could you
implement both?

"""

from __future__ import annotations
from collections.abc import Sequence
from functools import reduce
from itertools import chain
from typing import Iterator, NamedTuple, Union


class LList(NamedTuple):
    head: int
    tail: Union[LList, None] = None

    def __iter__(self):
        h = self.head
        t = self.tail
        while True:
            yield h
            if not t:
                break
            h, t = t.head, t.tail

    def __reversed__(self):
        for elem in reversed(tuple(self.__iter__())):
            yield elem

    def __repr__(self):
        return reduce(lambda s1, s2: s1 + ' -> ' + s2,
                      chain(map(str, self.__iter__()), iter(('None', ))))

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def __reverse_compose(it: Iterator[int, ...],
                          rec: Union[LList, None]) -> LList:
        rec_ = rec
        for i in it:
            rec_ = LList(head=i, tail=rec_)
        return rec_

    @staticmethod
    def compose(seq: Sequence[int, ...]) -> LList:
        return LList.__reverse_compose(reversed(seq), None)

    def reverse(self):
        return LList.__reverse_compose(self.__iter__(), None)


if __name__ == '__main__':
    ll1 = LList(head=1,
                tail=LList(head=2,
                           tail=LList(
                               head=6,
                               tail=LList(
                                   head=3,
                                   tail=LList(
                                       head=4,
                                       tail=LList(head=5,
                                                  tail=LList(head=6)))))))
    exp1_rev = '6 -> 5 -> 4 -> 3 -> 6 -> 2 -> 1 -> None'

    assert exp1_rev == str(ll1.reverse())
