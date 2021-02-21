"""Subsets II
Given a collection of integers that might contain duplicates, nums, return all
possible subsets (the power set).

Note: The solution set must not contain duplicate subsets.

Example:

Input: [1,2,2]
Output:
[
  [2],
  [1],
  [1,2,2],
  [2,2],
  [1,2],
  []
]
"""
# TODO
from typing import Sequence

if __name__ == '__main__':
    ipt_1 = [1, 2, 2]
    exp_1 = (
        (2, ),
        (1, ),
        (1, 2, 2),
        (2, 2),
        (1, 2),
        (),
    )
