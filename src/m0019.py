# -*- coding: utf-8 -*-
"""Remove Nth Node from End of List
TAG: linked-list

Given a linked list, remove the n-th node from the end of list and return its
head.

Example:

Given linked list: 1->2->3->4->5, and n = 2.

After removing the second node from the end, the linked list becomes 1->2->3->5.

Note: Given n will always be valid.

Follow up: Could you do this in one pass?
"""
from __future__ import annotations

from typing import Any


class LinkedList(object):
    __slots__ = ['head', 'tail']

    def __init__(self, head: Any, tail: LinkedList):
        self.head = head
        self.tail = tail

    def __str__(self):
        return self.head.__str__() + ' -> ' + self.tail.__str__()

    def __repr__(self):
        return self.__str__()

    def _get_item_int(self, idx: int):
        def helper(seq: LinkedList, idx_):
            while idx_ > 0:
                try:
                    seq, idx_ = seq.tail, idx_ - 1
                except AttributeError:
                    raise IndexError('Index out of range')
            return seq

        if idx >= 0:
            return helper(self, idx)
        else:
            raise ValueError('negative value not supported')

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._get_item_int(item)
        else:
            raise TypeError('Invalid argument type')

    def solution(self, n: int):
        def helper(seq: LinkedList, pre_seq: LinkedList) -> LinkedList:
            while pre_seq is not None:
                try:
                    seq, pre_seq = seq.tail, pre_seq.tail
                except AttributeError:
                    raise IndexError('Index out of range')
            return seq

        last_n = helper(self, self[n + 1])
        last_n.tail = last_n.tail.tail
        return self


if __name__ == '__main__':
    input_1_1 = LinkedList(
        1, LinkedList(2, LinkedList(3, LinkedList(4, LinkedList(5, None)))))
    input_1_2 = 2
    exp_1 = LinkedList(1, LinkedList(2, LinkedList(3, LinkedList(5, None))))

    assert input_1_1.solution(input_1_2).__eq__(exp_1)
