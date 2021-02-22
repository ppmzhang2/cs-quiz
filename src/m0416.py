"""Partition Equal Subset Sum
TAG: dynamic-programming

Given a non-empty array nums containing only positive integers, find if the
array can be partitioned into two subsets such that the sum of elements in both
subsets is equal.

Example 1:

* Input: nums = [1,5,11,5]
* Output: true
* Explanation: The array can be partitioned as [1, 5, 5] and [11].

Example 2:

* Input: nums = [1,2,3,5]
* Output: false
* Explanation: The array cannot be partitioned into equal sum subsets.

Constraints:

* 1 <= nums.length <= 200
* 1 <= nums[i] <= 100
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Sequence, Tuple


@unique
class State(Enum):
    DOING = 1
    DONE = 2
    INVALID = 3


@dataclass(frozen=True)
class FSM:
    target: int
    seq: Tuple[int, ...]

    @staticmethod
    def all_cuts(
        seq: Sequence[int], ) -> Tuple[Tuple[int, Tuple[int, ...]], ...]:
        return tuple((
            seq[idx],
            seq[idx + 1:],
        ) for idx in range(len(seq)))

    @property
    def state(self):
        if self.target == 0:
            return State.DONE
        if self.target < 0 or not self.seq:
            return State.INVALID
        return State.DOING

    def explode(self) -> Tuple[FSM, ...]:
        assert self.state == State.DOING
        all_cuts = self.all_cuts(self.seq)
        return tuple(FSM(self.target - tp[0], tp[1]) for tp in all_cuts)


class PartitionEqualSubsetSum:
    @classmethod
    def looper(cls, inputs: Tuple[FSM, ...], outputs: Tuple[FSM, ...]):
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.state == State.INVALID:
                inputs = inputs[1:]
            elif fsm.state == State.DONE:
                inputs = inputs[1:]
                outputs = (*outputs, fsm)
            else:
                inputs = (*fsm.explode(), *inputs[1:])

    def solution(self, nums):
        nums_ = tuple(sorted(nums))
        sum_ = sum(nums_)
        target = sum_ // 2
        if target * 2 != sum_:
            print('target is not an integer')
            return False
        fsm = FSM(target, nums_)
        res = self.looper((fsm, ), ())
        if not res:
            print('no solution available')
            return False
        print(f'solution: {res}')
        return True


if __name__ == '__main__':
    ipt_1 = [1, 5, 11, 5]
    exp_1 = True
    ipt_2 = [1, 5, 3, 2]
    exp_2 = False
    ipt_3 = [1, 8, 3, 2]
    exp_3 = False
    # print(FSM.all_cuts((1, 5, 6, 11)))

    pess = PartitionEqualSubsetSum()

    assert exp_1 == pess.solution(ipt_1)
    assert exp_2 == pess.solution(ipt_2)
    assert exp_3 == pess.solution(ipt_3)
