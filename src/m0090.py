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
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Sequence, Tuple


@unique
class State(IntEnum):
    DOING = 0
    DONE = 1


@dataclass(frozen=True)
class FSM:
    seq: Tuple[int, ...]
    remaining: Tuple[int, ...]

    @property
    def state(self):
        if not self.remaining:
            return State.DONE
        return State.DOING

    def explode(self) -> Tuple[FSM, FSM]:
        assert self.state == State.DOING
        value = self.remaining[0]
        fsm_new = (type(self))((*self.seq, value), self.remaining[1:])
        fsm_old = (type(self))(self.seq, self.remaining[1:])
        return fsm_old, fsm_new


class Subset2:
    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[Tuple[int, ...], ...],
    ) -> Tuple[Tuple[int, ...], ...]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.state == State.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm.seq))
        return cls.looper((*fsm.explode(), *inputs[1:]), outputs)

    def solution(self, seq: Sequence[int]):
        fsm = FSM((), seq)
        raw_seq = self.looper((fsm, ), ())
        unique_seq = set(raw_seq)
        return tuple(sorted(unique_seq))


if __name__ == '__main__':
    ipt_1 = [1, 2, 2]
    exp_1 = (
        (),
        (1, ),
        (1, 2),
        (1, 2, 2),
        (2, ),
        (2, 2),
    )

    subset = Subset2()
    assert subset.solution(ipt_1) == exp_1
