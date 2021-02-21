# -*- coding: utf-8 -*-
"""Move Zeroes
Given an array nums, write a function to move all 0's to the end of it while
maintaining the relative order of the non-zero elements.

Example:

Input: [5,7,0,1,0,3,12]
Output: [5,7,1,3,12,0,0]
Note:

You must do this in-place without making a copy of the array.
Minimize the total number of operations.

"""
from typing import Optional, Tuple


class Rc(object):
    """
    recursive solution
    """
    @staticmethod
    def solution(arr: Tuple[Optional[int]]):
        def helper(arr_: Tuple[Optional[int]], prefix: Tuple[Optional[int]],
                   nzero: int):
            if not arr_:
                return prefix + (0, ) * nzero
            elem = arr_[0]
            if elem == 0:
                return helper(arr_[1:], prefix, nzero + 1)
            else:
                return helper(arr_[1:], prefix + (elem, ), nzero)

        return helper(arr, (), 0)


if __name__ == '__main__':
    in1 = [5, 7, 0, 1, 0, 3, 12]
    exp1 = (5, 7, 1, 3, 12, 0, 0)
    assert Rc.solution(in1) == exp1
