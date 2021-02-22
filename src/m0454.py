"""4Sum II
TAG: hash-table

Given four lists A, B, C, D of integer values, compute how many tuples
(i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] is zero.

To make problem a bit easier, all A, B, C, D have same length of N where
0 ≤ N ≤ 500. All integers are in the range of -228 to 228 - 1 and the result is
guaranteed to be at most 231 - 1.

Example:

Input:

* A = [ 1, 2]
* B = [-2,-1]
* C = [-1, 2]
* D = [ 0, 2]

Output: 2

Explanation:

The two tuples are:

1. (0, 0, 0, 1) -> A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> A[1] + B[1] + C[0] + D[0] = 2 + (-1) + (-1) + 0 = 0
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Sequence, Tuple


@unique
class State(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    DONE = 5
    INVALID = 6


@dataclass(frozen=True)
class SumTuple:
    a: int
    b: int
    c: int
    d: int

    @property
    def result(self):
        return self.a + self.b + self.c + self.d


@dataclass(frozen=True)
class FSM:
    seq_array: Tuple[Tuple[int, ...], ...]
    tup: SumTuple

    @property
    def state(self) -> State:
        if not self.seq_array and self.tup.result == 0:
            return State.DONE
        if not self.seq_array:
            return State.INVALID
        if len(self.seq_array) == 4:
            return State.A
        if len(self.seq_array) == 3:
            return State.B
        if len(self.seq_array) == 2:
            return State.C
        if len(self.seq_array) == 1:
            return State.D

        raise ValueError('invalid input')

    def explode(self) -> Tuple[FSM, ...]:
        assert self.state in (State.A, State.B, State.C, State.D)
        active_array = self.seq_array[0]
        remainder_seq = self.seq_array[1:]
        if self.state == State.A:
            return tuple(
                FSM(
                    remainder_seq,
                    SumTuple(num, 0, 0, 0),
                ) for num in active_array)
        if self.state == State.B:
            return tuple(
                FSM(
                    remainder_seq,
                    SumTuple(self.tup.a, num, 0, 0),
                ) for num in active_array)
        if self.state == State.C:
            return tuple(
                FSM(
                    remainder_seq,
                    SumTuple(self.tup.a, self.tup.b, num, 0),
                ) for num in active_array)
        return tuple(
            FSM(
                remainder_seq,
                SumTuple(self.tup.a, self.tup.b, self.tup.c, num),
            ) for num in active_array)


class FourSum2:
    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[FSM, ...],
    ) -> Tuple[FSM, ...]:
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

    def solution(
        self,
        a: Sequence[int],
        b: Sequence[int],
        c: Sequence[int],
        d: Sequence[int],
    ) -> int:
        fsm = FSM((a, b, c, d), SumTuple(0, 0, 0, 0))
        res = self.looper((fsm, ), ())
        return res


if __name__ == '__main__':
    ipt_1_1 = [1, 2]
    ipt_1_2 = [-2, -1]
    ipt_1_3 = [-1, 2]
    ipt_1_4 = [0, 2]
    exp_1 = 2

    fs = FourSum2()
    print(fs.solution(ipt_1_1, ipt_1_2, ipt_1_3, ipt_1_4))
