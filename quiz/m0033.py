"""search in rotated-sorted array
https://leetcode-cn.com/problems/search-in-rotated-sorted-array/

You are given an integer array nums sorted in ascending order (with distinct
values), and an integer target.

Suppose that nums is rotated at some pivot unknown to you beforehand (i.e.,
[0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).

If target is found in the array return its index, otherwise, return -1.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1

Constraints:

1 <= nums.length <= 5000
-10^4 <= nums[i] <= 10^4
All values of nums are unique.
nums is guaranteed to be rotated at some pivot.
-10^4 <= target <= 10^4
"""

from typing import Sequence, Tuple


class Dichotomy:
    @staticmethod
    def split(seq: Sequence[int],
              idx: int) -> Tuple[Sequence[int], Sequence[int]]:
        if len(seq) <= 1:
            raise IndexError('must be longer than 1')
        return seq[:idx], seq[idx:]

    @staticmethod
    def not_ascending_order(seq: Sequence[int]) -> bool:
        if len(seq) <= 1:
            return True
        return seq[0] > seq[-1]

    @staticmethod
    def binary_search(asc_seq: Sequence[int], target: int) -> int:
        seq_ = asc_seq
        idx_base = 0
        while True:
            length = len(seq_)
            if length == 0:
                return -1
            idx = length // 2
            if seq_[idx] == target:
                return idx_base + idx
            if idx == 0:
                return -1
            if seq_[idx] > target:
                seq_ = seq_[:idx]
            else:
                seq_ = seq_[idx:]
                idx_base += idx

    def solution(self, nums: Sequence[int], target: int) -> int:
        def search_in_sub_seq(asc_seq: Sequence[int], target: int,
                              index_base: int) -> int:
            res = self.binary_search(asc_seq, target)
            if res == -1:
                return res
            return res + index_base

        def helper(seq: Sequence[int], target: int, index_base: int) -> int:
            if len(seq) <= 1 and seq[0] == target:
                return index_base
            if len(seq) <= 1 and seq[0] != target:
                return -1
            seq_ = seq
            while True:
                idx = len(seq_) // 2
                seq_left, seq_right = self.split(seq_, idx)
                if self.not_ascending_order(seq_right):
                    res = search_in_sub_seq(seq_left, target, index_base)
                    if res != -1:
                        return res
                    return helper(seq_right, target, index_base + idx)
                res = search_in_sub_seq(seq_right, target, idx + index_base)
                if res != -1:
                    return res
                return helper(seq_left, target, index_base)

        return helper(nums, target, 0)


if __name__ == '__main__':
    input_1_1 = [4, 5, 6, 7, 0, 1, 2]
    input_1_2 = 0
    input_2_1 = [4, 5, 6, 7, 0, 1, 2]
    input_2_2 = 4
    input_3_1 = [4, 5, 6, 7, 0, 1, 2]
    input_3_2 = 3

    dich = Dichotomy()

    assert dich.binary_search([2, 3, 5, 7, 11, 13], 2) == 0
    assert dich.binary_search([2, 3, 5, 7, 11, 13], 3) == 1
    assert dich.binary_search([2, 3, 5, 7, 11, 13], 5) == 2
    assert dich.binary_search([2], 2) == 0
    assert dich.binary_search([2], 3) == -1
    assert dich.binary_search([], 1) == -1

    print(dich.solution(input_1_1, input_1_2))
    print(dich.solution(input_2_1, input_2_2))
    print(dich.solution(input_3_1, input_3_2))
