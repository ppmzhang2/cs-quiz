"""Partition List
Given the head of a linked list and a value x, partition it such that all nodes
less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two
partitions.

Example 1:

Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]

Example 2:

Input: head = [2,1], x = 2
Output: [1,2]

Constraints:

* The number of nodes in the tree is in the range [0, 200].
* -100 <= Node.val <= 100
* -200 <= x <= 200
"""
from collections import defaultdict
from enum import Enum
from typing import Sequence


class Compare(Enum):
    LT = 1
    GE = 2


class PartitionList:
    __slots = ['_dd', '_seq', '_pivot']

    def __init__(self, seq: Sequence[int], pivot: int):
        self._dd = defaultdict(list)
        self._seq = seq
        self._pivot = pivot

    def add_one(self, num: int):
        if num >= self._pivot:
            self._dd[Compare.GE].append(num)
        else:
            self._dd[Compare.LT].append(num)

    def solution(self):
        list(map(self.add_one, self._seq))
        return (
            *self._dd[Compare.LT],
            *self._dd[Compare.GE],
        )


if __name__ == '__main__':
    ipt_1_1 = [1, 4, 3, 2, 5, 2]
    ipt_1_2 = 3
    exp_1 = (1, 2, 2, 4, 3, 5)
    ipt_2_1 = [2, 1]
    ipt_2_2 = 2
    exp_2 = (1, 2)

    assert PartitionList(ipt_1_1, ipt_1_2).solution() == exp_1
    assert PartitionList(ipt_2_1, ipt_2_2).solution() == exp_2
