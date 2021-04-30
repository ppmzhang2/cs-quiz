from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from functools import reduce
from typing import Tuple

T = Tuple[int, ...]


class SortedTuple(T):
    def __new__(cls, *args, **kwargs):
        ordered = kwargs.get('ordered', False)
        if not ordered:
            return super().__new__(cls, sorted(args))
        return super().__new__(cls, args)

    def split(self, idx: int) -> Tuple[int, SortedTuple]:
        seq = (*self.__getitem__(slice(0, idx)),
               *self.__getitem__(slice(idx + 1, None)))
        return self.__getitem__(idx), SortedTuple(*seq, ordered=True)

    def binary_search(self, val: int) -> int:
        left_idx = 0
        right_idx = self.__len__() - 1
        while True:
            idx = (right_idx + left_idx) // 2
            if self.__getitem__(idx) == val:
                return idx
            if right_idx - left_idx <= 1:
                if (abs(self.__getitem__(right_idx) - val) >=
                        abs(self.__getitem__(left_idx) - val)):
                    return left_idx
                return right_idx
            if self.__getitem__(idx) > val:
                right_idx = idx
            else:
                left_idx = idx


@unique
class State(IntEnum):
    INIT = 0
    ONE_LEFT = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    seq: SortedTuple
    target: int
    values: Tuple[int, ...]

    @property
    def state(self):
        if len(self.values) == 0:
            return State.INIT
        if len(self.values) == 1:
            return State.ONE_LEFT
        return State.DONE

    @property
    def total(self) -> int:
        return sum(self.values)

    @property
    def diff(self) -> int:
        return self.total - self.target

    @property
    def pair(self) -> Tuple[int, int]:
        return tuple(sorted(self.values))

    def explode(self) -> Tuple[FSM, ...]:
        tuples = tuple(self.seq.split(idx) for idx, _ in enumerate(self.seq))
        return tuple((type(self))(
            SortedTuple(*seq),
            self.target,
            (value, ),
        ) for value, seq in tuples)

    def complete(self) -> FSM:
        second = self.seq[self.seq.binary_search(self.target - self.values[0])]
        return (type(self))(self.seq, self.target, (*self.values, second))


class TwoSum:
    @staticmethod
    def looper(
        inputs: Tuple[FSM, ...],
        outputs: Tuple[FSM, ...],
    ) -> Tuple[FSM, ...]:
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.state == State.DONE:
                inputs, outputs = inputs[1:], (*outputs, fsm)
            elif fsm.state == State.INIT:
                inputs = (*fsm.explode(), *inputs[1:])
            else:
                inputs = (fsm.complete(), *inputs[1:])

    @staticmethod
    def reducer(x: FSM, y: FSM) -> FSM:
        if abs(x.diff) <= abs(y.diff):
            return x
        return y

    def solution(self, seq: Tuple[int, ...], target: int):
        fsm = FSM(SortedTuple(*seq), target, ())
        seq_fsm = self.looper((fsm, ), ())
        return reduce(self.reducer, seq_fsm).pair


if __name__ == '__main__':
    ipt_1_1 = (2, 4, 6, 0, 1, 3, 7, 8, 9)
    ipt_1_2 = 14
    exp_1 = (6, 8)
    ipt_2_1 = (1, 2, 7, 3, 10)
    ipt_2_2 = 14
    exp_2 = (3, 10)
    ipt_3_1 = (1, 2, 7, 3, 10)
    ipt_3_2 = -1
    exp_3 = (1, 2)

    # st = SortedTuple(*ipt_1_1)
    # assert st.binary_search(-10) == 0
    # assert st.binary_search(5) == 4
    # assert st.binary_search(100) == 8

    # print(st.split(2))
    # print(st.split(3))

    ts = TwoSum()

    assert exp_1 == ts.solution(ipt_1_1, ipt_1_2)
    assert exp_2 == ts.solution(ipt_2_1, ipt_2_2)
    assert exp_3 == ts.solution(ipt_3_1, ipt_3_2)
