"""Unique Paths
A robot is located at the top-left corner of a m x n grid (marked 'Start' in
the diagram below).

The robot can only move either down or right at any point in time. The robot is
trying to reach the bottom-right corner of the grid (marked 'Finish' in the
diagram below).

How many possible unique paths are there?

Example 1:
Input: m = 3, n = 7
Output: 28

Example 2:
* Input: m = 3, n = 2
* Output: 3
* Explanation: From the top-left corner, there are a total of 3 ways to reach
  the bottom-right corner:
  1. Right -> Down -> Down
  2. Down -> Down -> Right
  3. Down -> Right -> Down

Example 3:
Input: m = 7, n = 3
Output: 28

Example 4:
Input: m = 3, n = 3
Output: 6

Constraints:
* 1 <= m, n <= 100
* It's guaranteed that the answer will be less than or equal to 2 * 10^9.
"""
from __future__ import annotations

from enum import Enum, unique
from typing import NamedTuple, Sequence, Tuple


@unique
class Move(Enum):
    RIGHT = 1
    DOWN = 2


@unique
class Status(Enum):
    DIAGONAL = 1
    RIGHT = 2
    BOTTOM = 3
    DONE = 4


class FSM(NamedTuple):
    x: int
    y: int
    history: Tuple[Move, ...]

    @property
    def status(self) -> Status:
        if self.x == 1 and self.y == 1:
            return Status.DONE
        if self.x == 1:
            return Status.RIGHT
        if self.y == 1:
            return Status.BOTTOM
        if self.x > 1 and self.y > 1:
            return Status.DIAGONAL
        raise ValueError('invalid status')

    def explode(self) -> Tuple[FSM, FSM]:
        assert self.status == Status.DIAGONAL
        return (
            FSM(self.x - 1, self.y, (*self.history, Move.RIGHT)),
            FSM(self.x, self.y - 1, (*self.history, Move.DOWN)),
        )

    def one_way_trip(self) -> FSM:
        assert self.status in (Status.RIGHT, Status.BOTTOM)
        if self.status == Status.RIGHT:
            return FSM(
                self.x,
                1,
                (*self.history, *[Move.DOWN for _ in range(self.y - 1)]),
            )
        return FSM(
            1,
            self.y,
            (*self.history, *[Move.DOWN for _ in range(self.x - 1)]),
        )


class UniquePath:
    @classmethod
    def looper(cls, inputs: Sequence[FSM],
               outputs: Sequence[FSM]) -> Sequence[FSM]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.status == Status.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        if fsm.status == Status.DIAGONAL:
            return cls.looper((*inputs[1:], *fsm.explode()), outputs)
        return cls.looper((*inputs[1:], fsm.one_way_trip()), outputs)

    def solution(self, m: int, n: int) -> int:
        fsm = FSM(m, n, ())
        fsm_seq = self.looper([fsm], ())
        return len([fsm_.history for fsm_ in fsm_seq])


if __name__ == '__main__':
    ipt_1_1 = 3
    ipt_1_2 = 7
    exp_1 = 28
    ipt_2_1 = 3
    ipt_2_2 = 2
    exp_2 = 3
    ipt_3_1 = 7
    ipt_3_2 = 3
    exp_3 = 28
    ipt_4_1 = 3
    ipt_4_2 = 3
    exp_4 = 6

    up = UniquePath()
    print(up.solution(ipt_1_1, ipt_1_2))
