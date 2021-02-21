# -*- coding: utf-8 -*-
"""Intersection of Two Arrays
Given two arrays, write a function to compute their intersection.

Example 1:

Input: nums1 = [1,2,2,1], nums2 = [2,2]
Output: [2]
Example 2:

Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
Output: [9,4]
Note:

Each element in the result must be unique.
The result can be in any order.

"""
from typing import Tuple
from collections import defaultdict


def solution(arr1: Tuple[int], arr2: Tuple[int]):
    hm = defaultdict(int)
    for i in arr1:
        hm[i] = 1
    for i in arr2:
        hm[i] += 1
    return {k for k, v in hm.items() if v > 1}


if __name__ == '__main__':
    in1_1 = (1, 2, 2, 1)
    in1_2 = (2, 2)
    in2_1 = (4, 9, 5)
    in2_2 = (9, 4, 9, 8, 4)
    exp1 = {2}
    exp2 = {9, 4}

    assert solution(in1_1, in1_2) == exp1
    assert solution(in2_1, in2_2) == exp2
