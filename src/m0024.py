"""Swap Nodes in Pairs

Given a linked list, swap every two adjacent nodes and return its head.

You may not modify the values in the list's nodes, only nodes itself may be
changed.

Example:

Given 1->2->3->4, you should return the list as 2->1->4->3.
"""
from __future__ import annotations

from typing import Any, Optional


class LinkedList(object):
    __slots__ = ['head', 'tail']

    def __init__(self, head: Any, tail: Optional[LinkedList] = None):
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

    @property
    def is_last(self):
        return self.tail is None

    def set_head(self, value):
        self.head = value

    def set_tail(self, value):
        self.tail = value

    def solution(self):
        if self.is_last:
            pass
        else:
            head1 = self.head
            head2 = self.tail.head
            self.set_head(head2)
            self.tail.set_head(head1)
            if self.tail.is_last:
                pass
            else:
                return self.tail.tail.solution()

    def __eq__(self, other: LinkedList):
        if self.head.__eq__(other.head):
            if self.is_last and other.is_last:
                return True
            else:
                try:
                    return self.tail.__eq__(other.tail)
                except AttributeError:
                    return False
        else:
            return False


if __name__ == '__main__':
    input_1 = LinkedList(1, LinkedList(2, LinkedList(3, LinkedList(4, None))))
    exp_1 = LinkedList(2, LinkedList(1, LinkedList(4, LinkedList(3, None))))

    input_1.solution()
    assert input_1 == exp_1
