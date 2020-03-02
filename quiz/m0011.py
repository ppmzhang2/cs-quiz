# -*- coding: utf-8 -*-
"""Container with Most Water

Given n non-negative integers a1, a2, ..., an , where each represents a point at
coordinate (i, ai). n vertical lines are drawn such that the two endpoints of
line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis
forms a container, such that the container contains the most water.

Note: You may not slant the container and n is at least 2.

"""

from functools import reduce
from typing import Tuple


class Container(object):
    @staticmethod
    def __volume_by_two_indexes(arr: Tuple[int, ...], idx_beg: int,
                                idx_end: int):
        """volume by providing two indexes

        :param arr: height array
        :param idx_beg: starting index
        :param idx_end: ending index
        :return:
        """
        return (idx_end - idx_beg) * min(arr[idx_beg], arr[idx_end])

    @staticmethod
    def __max_volume_with_fixed_end(arr: Tuple[int, ...], idx_end: int):
        return max(Container.__volume_by_two_indexes(arr, i, idx_end)
                   for i in range(0, idx_end))

    @staticmethod
    def solution(arr: Tuple[int, ...]):
        return max(Container.__max_volume_with_fixed_end(arr, i)
                   for i in range(1, len(arr)))


if __name__ == '__main__':
    in1 = (2, 4, 6, 1, 5)
    in2 = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    exp1 = 12
    exp2 = 49

    assert Container.solution(in1) == exp1
    assert Container.solution(in2) == exp2
