"""Integer Break
TAG: dynamic-programming, math

Given a positive integer n, break it into the sum of at least two positive
integers and maximize the product of those integers. Return the maximum product
you can get.

Example 1:
Input: 2
Output: 1
Explanation: 2 = 1 + 1, 1 × 1 = 1.

Example 2:
Input: 10
Output: 36
Explanation: 10 = 3 + 3 + 4, 3 × 3 × 4 = 36.
Note: You may assume that n is not less than 2 and not larger than 58.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Tuple


@unique
class State(Enum):
    DOING = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    remainders: Tuple[int, ...]
    ones: int
    twos: int
    threes: int

    @staticmethod
    def cut(n: int) -> Tuple[int, int]:
        if n >= 4:
            addend = n // 2
            return addend, n - addend
        raise ValueError('invalid input')

    @staticmethod
    def naive(n: int):
        if n in (1, 2, 3):
            return n
        raise ValueError('invalid input')

    @property
    def state(self) -> State:
        if not self.remainders:
            return State.DONE
        return State.DOING

    @property
    def result(self) -> int:
        return (self.naive(1)**self.ones * self.naive(2)**self.twos *
                self.naive(3)**self.threes)

    def transform(self) -> FSM:
        assert self.state == State.DOING
        remainder = self.remainders[0]
        if remainder == 1:
            return (type(self))(
                self.remainders[1:],
                self.ones + 1,
                self.twos,
                self.threes,
            )
        if remainder == 2:
            return (type(self))(
                self.remainders[1:],
                self.ones,
                self.twos + 1,
                self.threes,
            )
        if remainder == 3:
            return (type(self))(
                self.remainders[1:],
                self.ones,
                self.twos,
                self.threes + 1,
            )
        return (type(self))(
            (*self.cut(remainder), *self.remainders[1:]),
            self.ones,
            self.twos,
            self.threes,
        )


class IntegerBreak:
    @classmethod
    def looper(cls, fsm: FSM) -> FSM:
        while True:
            if fsm.state == State.DONE:
                return fsm
            fsm = fsm.transform()

    def solution(self, n: int):
        if n == 1:
            return 1
        if n == 2:
            return 1
        fsm = FSM((n, ), 0, 0, 0)
        final = self.looper(fsm)
        return final.result


if __name__ == '__main__':
    ipt_1 = 2
    exp_1 = 1
    ipt_2 = 10
    exp_2 = 36

    ib = IntegerBreak()

    assert exp_1 == ib.solution(ipt_1)
    assert exp_2 == ib.solution(ipt_2)
