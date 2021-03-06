"""Next Permutation
TAG: untagged

Implement next permutation, which rearranges numbers into the lexicographically
next greater permutation of numbers.

If such arrangement is not possible, it must rearrange it as the lowest possible
order (ie, sorted in ascending order).

The replacement must be in-place and use only constant extra memory.

Here are some examples. Inputs are in the left-hand column and its corresponding
outputs are in the right-hand column.

1,2,3 → 1,3,2
3,2,1 → 1,2,3
1,1,5 → 1,5,1
"""
from __future__ import annotations

from typing import List


class Desc(object):
    @staticmethod
    def bisection_search(desc_seq: List[int], target: int):
        idx_start = 0
        idx_end = len(desc_seq) - 1
        while True:
            idx = (idx_end - idx_start) // 2
            if desc_seq[idx] > target:
                break
            idx_end = idx

        return idx

    @staticmethod
    def solution(seq: List[int]):
        length = len(seq)
        if length <= 1:
            return seq

        idx1, idx2 = length - 2, length - 1
        while True:
            if idx1 < 0:
                return list(reversed(seq))
            elif seq[idx1] < seq[idx2]:
                idx = Desc.bisection_search(seq[idx2:], seq[idx1]) + idx2
                seq[idx1], seq[idx] = seq[idx], seq[idx1]
                return seq
            idx1, idx2 = idx1 - 1, idx2 - 1


if __name__ == '__main__':
    input_1 = [3, 5, 4, 6, 2, 1]
    exp_1 = [3, 5, 6, 4, 2, 1]
    assert Desc.solution(input_1) == exp_1
