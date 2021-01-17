"""permutations
Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]

Example 3:
Input: nums = [1]
Output: [[1]]

Constraints:

1 <= nums.length <= 6
-10 <= nums[i] <= 10
All the integers of nums are unique.
"""
from typing import NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    perm: Tuple[int, ...]
    addend_seq: Tuple[int, ...]


class Permutation:
    @staticmethod
    def add_one_num(seq: Sequence[int],
                    addend: int) -> Tuple[Tuple[int, ...], ...]:
        if not seq:
            return ((addend, ), )
        return (
            *((*seq[:idx], addend, *seq[idx:]) for idx, _ in enumerate(seq)),
            (*seq, addend),
        )

    @staticmethod
    def mw_status(mw: Middleware) -> int:
        if not mw.addend_seq:
            return 1
        return 0

    def looper(self, input_seq: Sequence[Middleware],
               output_seq: Sequence[Middleware]) -> Sequence[Middleware]:
        if not input_seq:
            return output_seq
        mw = input_seq[0]
        if self.mw_status(mw) == 1:
            return self.looper(input_seq[1:], (*output_seq, mw))
        perm_seq = self.add_one_num(mw.perm, mw.addend_seq[0])
        mw_seq = tuple(
            Middleware(perm, mw.addend_seq[1:]) for perm in perm_seq)
        return self.looper((*input_seq[1:], *mw_seq), output_seq)

    def solution(self, nums: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
        mw = Middleware((), tuple(nums))
        mw_seq = self.looper((mw, ), ())
        return tuple(sorted(mw_.perm for mw_ in mw_seq))


if __name__ == '__main__':
    ipt_1 = [1, 2, 3]
    exp_1 = (
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    )
    ipt_2 = [0, 1]
    exp_2 = ((0, 1), (1, 0))
    ipt_3 = [1]
    exp_3 = ((1, ), )

    pm = Permutation()

    assert pm.add_one_num([1, 2, 3], 4) == (
        (4, 1, 2, 3),
        (1, 4, 2, 3),
        (1, 2, 4, 3),
        (1, 2, 3, 4),
    )
    assert pm.add_one_num([1, 2], 3) == (
        (3, 1, 2),
        (1, 3, 2),
        (1, 2, 3),
    )
    assert pm.add_one_num([1], 2) == (
        (2, 1),
        (1, 2),
    )
    assert pm.solution(ipt_1) == exp_1
    assert pm.solution(ipt_2) == exp_2
    assert pm.solution(ipt_3) == exp_3
