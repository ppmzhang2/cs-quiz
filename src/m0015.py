# -*- coding: utf-8 -*-
"""three-sum
Given an array nums of n integers, are there elements a, b, c in nums such that
a + b + c = 0? Find all unique triplets in the array which gives the sum of
zero.

Note: The solution set must not contain duplicate triplets.

Example:

Given array nums = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
"""
from functools import reduce
from typing import List, Tuple


class ThreeSum(object):
    @staticmethod
    def _sum(seq: List[int], target: int, acc: Tuple[List, ...]):
        if len(seq) <= 1:
            return acc
        left = seq[0]
        right = seq[-1]
        if left + right == target:
            return ThreeSum._sum(
                seq[1:], target, acc + (tuple(sorted(
                    (left, right, -target))), ))
        elif left + right > target:
            return ThreeSum._sum(seq[:-1], target, acc)
        elif left + right < target:
            return ThreeSum._sum(seq[1:], target, acc)

    @staticmethod
    def split(arr: List[int], idx: int):
        return arr[:idx] + arr[idx + 1:], arr[idx], ()

    @staticmethod
    def solution(arr: List[int]):
        return set(
            reduce(
                lambda x, y: x + y,
                (map(lambda x: ThreeSum._sum(*ThreeSum.split(sorted(arr), x)),
                     range(len(arr))))))


if __name__ == '__main__':
    input_1 = [-1, 0, 1, 2, -1, -4]
    input_2 = [-1, -2, 1, 3, 6, 0, -3]

    exp_1 = {(-1, 0, 1), (-1, -1, 2)}
    exp_2 = {(-1, 0, 1), (-2, 1, 1), (-3, -3, 6), (-3, 0, 3), (-2, -1, 3),
             (-3, 1, 2)}
    three_sum = ThreeSum()

    assert three_sum.solution(input_1) == exp_1
    assert three_sum.solution(input_2) == exp_2
