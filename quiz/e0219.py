# -*- coding: utf-8 -*-
"""Contains Duplicate ii

Given an array of integers and an integer k, find out whether there are two
distinct indices i and j in the array such that nums[i] = nums[j] and the
absolute difference between i and j is at most k.

Example 1:

Input: nums = [1,2,3,1], k = 3
Output: true
Example 2:

Input: nums = [1,0,1,1], k = 1
Output: true
Example 3:

Input: nums = [1,2,3,1,2,3], k = 2
Output: false

"""

from __future__ import annotations
from collections import defaultdict
from collections.abc import Sequence


class CountKDict(object):
    """
    K-element default dict to count the occurance
    """
    __slots__ = ['__dd', '__maxlen']

    def __init__(self, k: int):
        self.__dd = defaultdict(int)
        self.__maxlen = k

    def __check_len(self):
        keys: list = list(self.__dd.keys())
        if len(keys) > self.__maxlen:
            del self.__dd[keys[0]]

    def add(self, key):
        self.__dd[key] += 1
        self.__check_len()

    def count(self, key):
        return self.__dd[key]

    def __str__(self):
        return self.__dd.__str__()

    def __repr__(self):
        return self.__str__()


def solution(seq: Sequence[int, ...], k: int) -> bool:
    kd = CountKDict(k)
    for key in seq:
        kd.add(key)
        if kd.count(key) > 1:
            return True
    return False


if __name__ == '__main__':
    in1_1 = [1, 2, 3, 1]
    in2_1 = [1, 0, 1, 1]
    in3_1 = [1, 2, 3, 1, 2, 3]
    in1_2 = 3
    in2_2 = 1
    in3_2 = 2
    exp1 = True
    exp2 = True
    exp3 = False

    assert solution(in1_1, in1_2) is exp1
    assert solution(in2_1, in2_2) is exp2
    assert solution(in3_1, in3_2) is exp3
