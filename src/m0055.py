"""Jump Game
Given an array of non-negative integers nums, you are initially positioned at
the first index of the array.

Each element in the array represents your maximum jump length at that position.

Determine if you are able to reach the last index.

Example 1:
Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump
length is 0, which makes it impossible to reach the last index.

Constraints:
* 1 <= nums.length <= 3 * 10^4
* 0 <= nums[i] <= 10^5
"""
from typing import NamedTuple, Sequence, Tuple

import numpy as np


class Middleware(NamedTuple):
    seq: Tuple[int]
    index: int
    acc: Tuple[int]

    @property
    def status(self):
        if self.index >= len(self.seq) - 1:
            return 2
        if self.index == 0 and len(self.acc) == 1:
            return 0
        if self.index > 0 and self.index < len(self.seq) - 1:
            return 1
        raise ValueError('invalid middleware')


class Jump:
    @staticmethod
    def reverse_nums(nums: Sequence[int]) -> Sequence[int]:
        return tuple(reversed(nums))

    @staticmethod
    def transform(mw: Middleware) -> Middleware:
        assert mw.status <= 1
        next_index = mw.index + 1
        max_step_size = mw.seq[next_index]
        if max_step_size == 0:
            steps = -np.inf
        else:
            steps = 1 + min(mw.acc[:max_step_size])
        return Middleware(mw.seq, next_index, (steps, *mw.acc))

    def looper(self, mw: Middleware) -> Middleware:
        if mw.status == 2:
            return mw
        return self.looper(self.transform(mw))

    def solution(self, nums: Sequence[int]) -> int:
        seq = self.reverse_nums(nums)
        mw = self.looper(Middleware(seq, 0, (0, )))
        if mw.acc[0] >= 0:
            return True
        return False


if __name__ == '__main__':
    ipt_1 = [2, 3, 1, 1, 4]
    exp_1 = True
    ipt_2 = [3, 2, 1, 0, 4]
    exp_2 = False

    jump = Jump()
    assert jump.reverse_nums(ipt_1) == (4, 1, 1, 3, 2)
    assert jump.solution(ipt_1) == exp_1
    assert jump.solution(ipt_2) == exp_2
