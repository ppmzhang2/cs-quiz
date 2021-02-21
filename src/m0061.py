"""Rotate List
Given the head of a linked list, rotate the list to the right by k places.

Example 1:
Input: head = [1,2,3,4,5], k = 2
Output: [4,5,1,2,3]

Example 2:
Input: head = [0,1,2], k = 4
Output: [2,0,1]

Constraints:
* The number of nodes in the list is in the range [0, 500].
* -100 <= Node.val <= 100
* 0 <= k <= 2 * 10^9
"""
from __future__ import annotations

from typing import NamedTuple, Sequence


class FSM(NamedTuple):
    seq: Sequence[int]
    raw_steps: int

    @property
    def period(self) -> int:
        return len(self.seq)

    @property
    def steps(self) -> int:
        periods = self.raw_steps // self.period
        return self.raw_steps - periods * self.period

    @property
    def status(self) -> int:
        if self.steps == 0:
            return 1
        return 0

    def standardize(self) -> FSM:
        if not self.seq:
            return FSM(self.seq, 0)
        return FSM(self.seq, self.steps)

    def transform(self) -> FSM:
        assert self.status != 1
        return FSM((self.seq[-1], *self.seq[:-1]), self.raw_steps - 1)


class RotateList:
    @classmethod
    def looper(cls, fsm: FSM) -> FSM:
        if fsm.status == 1:
            return fsm
        return cls.looper(fsm.transform())

    def solution(self, nums: Sequence[int], k: int) -> Sequence[int]:
        fsm = FSM(nums, k).standardize()
        return self.looper(fsm).seq


if __name__ == '__main__':
    ipt_1_1 = [1, 2, 3, 4, 5]
    ipt_1_2 = 2
    exp_1 = (4, 5, 1, 2, 3)
    ipt_2_1 = [0, 1, 2]
    ipt_2_2 = 4
    exp_2 = (2, 0, 1)
    ipt_3_1 = [1, 2, 3, 4, 5]
    ipt_3_2 = 2 + 5 * 10**5
    exp_3 = (4, 5, 1, 2, 3)

    rl = RotateList()
    assert rl.solution(ipt_1_1, ipt_1_2) == exp_1
    assert rl.solution(ipt_2_1, ipt_2_2) == exp_2
    assert rl.solution(ipt_3_1, ipt_3_2) == exp_3

    # print(FSM(ipt_1_1, ipt_1_2).steps)
    # print(FSM(ipt_2_1, ipt_2_2).steps)
    # print(FSM(ipt_2_1, ipt_2_2).standardize().transform())
