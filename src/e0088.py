# -*- coding: utf-8 -*-
"""Merge Sorted Array

Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as
one sorted array.

Note:

The number of elements initialized in nums1 and nums2 are m and n respectively.
You may assume that nums1 has enough space (size that is greater or equal to
m + n) to hold additional elements from nums2.
Example:

Input:
nums1 = [1,2,3,0,0,0], m = 3
nums2 = [2,5,6],       n = 3

Output: [1,2,2,3,5,6]

"""

from typing import Tuple


class TR(object):
    """
    tail recursion
    """
    @staticmethod
    def solution(arr1: Tuple[int, ...], arr2: Tuple[int, ...]):
        def helper(arr1_: Tuple[int, ...], arr2_: Tuple[int, ...],
                   rec: Tuple[int, ...]):
            if not arr1_ and not arr2_:
                return rec
            elif not arr1_:
                return rec + arr2_
            elif not arr2_:
                return rec + arr1_
            else:
                if arr1_[0] >= arr2_[0]:
                    return helper(arr1_, arr2_[1:], rec + (arr2_[0], ))
                else:
                    return helper(arr1_[1:], arr2_, rec + (arr1_[0], ))

        return helper(arr1, arr2, ())


if __name__ == '__main__':
    in1_1 = (1, 2, 3)
    in1_2 = (2, 5, 6)
    print(TR.solution(in1_1, in1_2))
