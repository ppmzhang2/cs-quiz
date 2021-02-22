"""Permutation Sequence
TAG: math

The set [1, 2, 3, ..., n] contains a total of n! unique permutations.

By listing and labeling all of the permutations in order, we get the following
sequence for n = 3:

* "123"
* "132"
* "213"
* "231"
* "312"
* "321"

Given n and k, return the kth permutation sequence.

Example 1:
Input: n = 3, k = 3
Output: "213"

Example 2:
Input: n = 4, k = 9
Output: "2314"

Example 3:
Input: n = 3, k = 1
Output: "123"
"""
from __future__ import annotations

from functools import reduce
from typing import NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    nums: Sequence[int]
    perm: Tuple[int, ...]

    @property
    def status(self):
        if not self.nums:
            return 2
        if not self.perm:
            return 0
        return 1

    def explode(self) -> Sequence[Middleware]:
        assert self.status <= 1
        num = self.nums[0]
        all_perms_but_one = tuple((
            *self.perm[:idx],
            num,
            *self.perm[idx:],
        ) for idx, _ in enumerate(self.perm))
        all_perms = (*all_perms_but_one, (*self.perm, num))
        return tuple(Middleware(self.nums[1:], perm_) for perm_ in all_perms)


class Permutation:
    @classmethod
    def looper(cls, inputs: Sequence[Middleware],
               outputs: Sequence[Middleware]):
        if not inputs:
            return outputs
        mw = inputs[0]
        if mw.status == 2:
            return cls.looper(inputs[1:], (*outputs, mw))
        return cls.looper((*inputs[1:], *mw.explode()), outputs)

    def all_perms(self, nums: Sequence[int]):
        mws = self.looper((Middleware(nums, ()), ), ())
        return tuple(sorted(mw_.perm for mw_ in mws))

    def solution(self, n: int, idx: int):
        nums = range(1, n + 1)
        perms = self.all_perms(nums)
        return reduce(lambda x, y: x + y, map(str, perms[idx - 1]))


if __name__ == '__main__':
    ipt_1_1 = 3
    ipt_1_2 = 3
    exp_1 = '213'
    ipt_2_1 = 4
    ipt_2_2 = 9
    exp_2 = '2314'
    ipt_3_1 = 3
    ipt_3_2 = 1
    exp_3 = '123'

    p = Permutation()
    # print(p.all_perms([1, 2, 3]))
    assert p.solution(ipt_1_1, ipt_1_2) == exp_1
    assert p.solution(ipt_2_1, ipt_2_2) == exp_2
    assert p.solution(ipt_3_1, ipt_3_2) == exp_3
