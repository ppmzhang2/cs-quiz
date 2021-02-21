# -*- coding: utf-8 -*-
"""House Robber

You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed, the only constraint stopping
you from robbing each of them is that adjacent houses have security system
connected and it will automatically contact the police if two adjacent houses
were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each
house, determine the maximum amount of money you can rob tonight without
alerting the police.

Example 1:

Input: [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
    Total amount you can rob = 1 + 3 = 4.
Example 2:

Input: [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house
    5 (money = 1). Total amount you can rob = 2 + 9 + 1 = 12.

"""

from typing import Tuple, Iterator


class DP(object):
    """
    dynamic programming
    """
    @staticmethod
    def __gen_house_rob(arr: Tuple[int, ...]) -> Iterator[int]:
        """maximum income including ith house
        S(i) = max(S(i - 2) + a(i), S(i - 3) + a(i))

        :param arr:
        :return:
        """
        res0 = arr[0]
        res1 = arr[1]
        res2 = arr[0] + arr[2]
        arr = arr + (0, 0)
        for idx in range(len(arr) - 3):
            yield res0
            res0, res1, res2 = res1, res2, max(res0 + arr[idx + 3],
                                               res1 + arr[idx + 3])

    @staticmethod
    def solution(arr: Tuple[int, ...]):
        return max(DP.__gen_house_rob(arr))


if __name__ == '__main__':
    in1 = (1, 2, 3, 1)
    in2 = (2, 7, 9, 3, 1)
    in3 = (7, 3, 60, 1, 1, 50, 10, 12, 0)
    exp1 = 4
    exp2 = 11
    exp3 = 129

    assert exp1 == DP.solution(in1)
    assert exp2 == DP.solution(in2)
    assert exp3 == DP.solution(in3)
