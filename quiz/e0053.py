# -*- coding: utf-8 -*-
"""Maximum Sum Subarray

Given an integer array nums, find the contiguous subarray (containing at least
one number) which has the largest sum and return its sum.

Example:

Input: [-2,1,-3,4,-1,2,1,-5,4],
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.
Follow up:

If you have figured out the O(n) solution, try coding another solution using
the divide and conquer approach, which is more subtle.

"""

from typing import Union, List, Tuple


class DP(object):
    """
    Dynamic Programming
    """
    @staticmethod
    def maxsum_endidx_tuple(arr: Union[List, Tuple]):
        """

        :param arr:
        :return: tuple of maximum sum ending at every index
        """
        def helper(arr_: Union[List, Tuple], rec: Tuple) -> Tuple:
            if not arr_:
                return rec
            if not rec:
                curmax = arr_[0]
            else:
                curmax = max(rec[-1] + arr_[0], arr_[0])
            return helper(arr_[1:], rec + (curmax, ))

        return helper(arr, ())

    @staticmethod
    def maxsum_subarr(arr: Union[List, Tuple]) -> int:
        return max(DP.maxsum_endidx_tuple(arr))


class PS(object):
    """
    Prefix Sum
    """
    @staticmethod
    def prefix_sum(arr: Union[List, Tuple]) -> Tuple[int, ...]:
        def helper(arr_: Union[List, Tuple], rec: Tuple[int, ...]):
            if not arr_:
                return rec
            if not rec:
                return helper(arr_[1:], (arr_[0], ))
            else:
                return helper(arr_[1:], rec + (rec[-1] + arr_[0], ))

        return helper(arr, ())

    @staticmethod
    def maxsum_subarr(arr: Union[List, Tuple]) -> int:
        arr_ps = PS.prefix_sum(arr)
        return max(arr_ps) - min(arr_ps)


if __name__ == '__main__':
    in1 = (-2, 1, -3, 4, -1, 2, 1, -5, 4)
    exp1 = 6

    print(DP.maxsum_endidx_tuple(in1))
    assert DP.maxsum_subarr(in1) == exp1

    print(PS.prefix_sum(in1))
    assert PS.maxsum_subarr(in1) == exp1
