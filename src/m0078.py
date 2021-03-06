"""Subsets
TAG: back-tracking

Given an integer array nums of unique elements, return all possible subsets
(the power set).

The solution set must not contain duplicate subsets. Return the solution in any
order.

Example 1:
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Example 2:
Input: nums = [0]
Output: [[],[0]]

Constraints:
* 1 <= nums.length <= 10
* -10 <= nums[i] <= 10
* All the numbers of nums are unique.
"""
from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Sequence, Tuple


class Status(Enum):
    DOING = 0
    DONE = 1


class FSM(NamedTuple):
    subsets: Sequence[Sequence[int]]
    elements: Sequence[int]

    @property
    def status(self):
        if not self.elements:
            return Status.DONE
        return Status.DOING

    def transform(self) -> FSM:
        assert self.status == Status.DOING
        element = self.elements[0]
        additional_sets = tuple(
            (*subset, element) for _, subset in enumerate(self.subsets))
        return FSM((*self.subsets, *additional_sets), self.elements[1:])


class Subsets:
    @classmethod
    def looper(cls, fsm: FSM) -> FSM:
        if fsm.status == Status.DONE:
            return fsm
        return cls.looper(fsm.transform())

    def solution(self, nums: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
        fsm = FSM((), ), nums)
        return tuple(sorted(self.looper(fsm).subsets))


if __name__ == '__main__':
    ipt_1 = [1, 2]
    exp_1 = (
        (),
        (1, ),
        (1, 2),
        (2, ),
    )
    ipt_2 = [1, 2, 3]
    exp_2 = (
        (),
        (1, ),
        (1, 2),
        (1, 2, 3),
        (1, 3),
        (2, ),
        (2, 3),
        (3, ),
    )

    s = Subsets()

    assert s.solution(ipt_1) == exp_1
    assert s.solution(ipt_2) == exp_2
