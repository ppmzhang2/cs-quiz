from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from functools import reduce
from typing import Sequence, Tuple


class QsArray(tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args, **kwargs)

    def split_by_pivot(self, index: int) -> Tuple[QsArray, QsArray, QsArray]:
        pivot = self[index]
        arr = (*self[:index], *self[index + 1:])
        return (
            QsArray(*filter(lambda x: x <= pivot, arr)),
            QsArray(pivot),
            QsArray(*filter(lambda x: x > pivot, arr)),
        )

    def pivot_sort(self) -> Tuple[QsArray, ...]:
        if len(self) <= 1:
            return (self, )
        return self.split_by_pivot(0)


@unique
class State(IntEnum):
    SPLITTING = 1
    ROTATING = 2
    DONE = 3


@dataclass(frozen=True)
class FSM:
    before: Tuple[QsArray, ...]
    after: Tuple[QsArray, ...]
    max_len: int

    @property
    def state(self) -> State:
        if self.before:
            return State.SPLITTING
        if self.max_len <= 1:
            return State.DONE
        return State.ROTATING

    def split(self) -> FSM:
        qs_arr = self.before[0]
        return (type(self))(
            self.before[1:],
            (*self.after, *qs_arr.pivot_sort()),
            max(self.max_len, len(qs_arr)),
        )

    def rotate(self) -> FSM:
        return (type(self))(self.after, (), 0)

    def transform(self) -> FSM:
        if self.state == State.SPLITTING:
            return self.split()
        if self.state == State.ROTATING:
            return self.rotate()
        raise RuntimeError('it is done')

    @property
    def sorted(self) -> QsArray:
        return reduce(lambda x, y: x + y, self.after)


class QuickSort:
    @staticmethod
    def solution(seq: Sequence[int]):
        qs_arr = QsArray(*seq)
        fsm = FSM((qs_arr, ), (), 0)
        while True:
            if fsm.state == State.DONE:
                return fsm.sorted
            fsm = fsm.transform()


if __name__ == '__main__':
    ipt_1 = (2, 4, 6, 0, 1, 9, 3, 8, 5, 7)
    exp_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    # print(QsArray())
    # print(QsArray(1))
    # print(QsArray(1, 2, 3))

    # print(QsArray(*ipt_1).split_by_pivot(0))
    # print(QsArray(*ipt_1).pivot_sort())
    # print(QsArray(1).pivot_sort())
    # print(QsArray().pivot_sort())

    qs = QuickSort()
    assert exp_1 == qs.solution(ipt_1)
