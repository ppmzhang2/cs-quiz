"""maximum-product-subarray
TAG: dynamic-programming

Given an integer array nums, find the contiguous subarray within an array
(containing at least one number) which has the largest product.

Example 1:
Input: [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

Example 2:
Input: [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Tuple


@unique
class Status(Enum):
    DOING = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    value: int
    remainings: Tuple[int, ...]
    candidates: Tuple[int, ...]

    @property
    def status(self):
        if not self.remainings:
            return Status.DONE
        return Status.DOING

    @property
    def next_value(self):
        if self.status == Status.DONE:
            return None
        return self.value * self.remainings[0]

    @property
    def max_value(self):
        return max((self.value, *self.candidates))

    def transform(self) -> FSM:
        assert self.status == Status.DOING
        if self.next_value >= self.value:
            return (type(self))(
                self.next_value,
                self.remainings[1:],
                self.candidates,
            )
        return (type(self))(
            self.next_value,
            self.remainings[1:],
            (*self.candidates, self.value),
        )


class MaxProductSubarray:
    @classmethod
    def explode(cls, nums: Tuple[int, ...]) -> Tuple[Tuple[int, ...], ...]:
        return tuple(nums[idx:] for idx in range(len(nums)))

    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[int, ...],
    ) -> Tuple[int, ...]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.status == Status.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm.max_value))
        return cls.looper((fsm.transform(), *inputs[1:]), outputs)

    def solution(self, nums: Tuple[int, ...]):
        seq_nums = self.explode(nums)
        seq_fsms = tuple(FSM(nums_[0], nums_[1:], ()) for nums_ in seq_nums)
        return max(self.looper(seq_fsms, ()))


if __name__ == '__main__':
    ipt_1 = (2, 3, -2, 4)
    exp_1 = 6
    ipt_2 = (-2, 0, -1)
    exp_2 = 0
    ipt_3 = (-1, -2, -3, -4, -5, -6, -7)
    exp_3 = 5040

    mps = MaxProductSubarray()

    assert mps.solution(ipt_1) == exp_1
    assert mps.solution(ipt_2) == exp_2
    assert mps.solution(ipt_3) == exp_3
