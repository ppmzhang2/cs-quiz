# -*- coding: utf-8 -*-
"""Majority Element

Given an array of size n, find the majority element. The majority element is
the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always
exist in the array.

Example 1:

Input: [3,2,3]
Output: 3
Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2

"""

from collections import defaultdict
from typing import Tuple


class HM(object):
    """
    hash-map implemented
    """
    __slots__ = ['__arr', '__tot', '__cnt']

    @staticmethod
    def __count(arr):
        cnt: defaultdict = defaultdict(int)

        def helper(x):
            cnt[x] += 1

        list(map(helper, arr))
        return cnt

    def __init__(self, arr: Tuple):
        self.__arr = arr
        self.__tot = len(self.__arr)
        self.__cnt: defaultdict = HM.__count(self.__arr)

    def mode(self):
        tp = max(self.__cnt.items(), key=lambda x: x[1])
        return {'element': tp[0], 'count': tp[1]}

    def majority(self):
        md = self.mode()
        if 2 * md['count'] >= self.__tot:
            return md['element']
        else:
            return None


if __name__ == '__main__':
    in1: Tuple[int, ...] = (2, 2, 1, 1, 1, 2, 2)
    exp1 = 2
    in2: Tuple[int, ...] = (2, 3, 5, 7, 11, 13, 7)
    exp2 = None

    assert exp1 == HM(in1).majority()
    assert exp2 == HM(in2).majority()
