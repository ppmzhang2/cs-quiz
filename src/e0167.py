# -*- coding: utf-8 -*-
"""Two Sum ii: Input Array is Sorted

Given an array of integers that is already sorted in ascending order, find two
numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they
add up to the target, where index1 must be less than index2.

Note:

Your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution and you may
not use the same element twice.
Example:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore index1 = 1, index2 = 2.

"""

from typing import Tuple


class TwoSumSorted(object):
    @staticmethod
    def solution(arr: Tuple[int, ...], target: int):
        def helper(arr_: Tuple[int, ...], target_: int, idx_beg: int,
                   idx_end: int, rec: Tuple[Tuple[int, int], ...]):
            if idx_beg >= idx_end:
                return rec
            elif arr[idx_beg] + arr[idx_end] < target:
                return helper(arr_, target_, idx_beg + 1, idx_end, rec)
            elif arr[idx_beg] + arr[idx_end] > target:
                return helper(arr_, target_, idx_beg, idx_end - 1, rec)
            else:
                return helper(arr_, target_, idx_beg + 1, idx_end - 1,
                              rec + ((idx_beg, idx_end), ))

        return helper(arr, target, 0, len(arr) - 1, ())


if __name__ == '__main__':
    in1_1 = (2, 7, 11, 15)
    in1_2 = 9
    in2_1 = (1, 2, 4, 5, 7, 8)
    in2_2 = 9
    exp1 = ((0, 1), )
    exp2 = ((0, 5), (1, 4), (2, 3))

    assert TwoSumSorted.solution(in1_1, in1_2) == exp1
    assert TwoSumSorted.solution(in2_1, in2_2) == exp2
