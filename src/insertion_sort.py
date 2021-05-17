from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum, unique


@unique
class State(IntEnum):
    DONE = 0
    DOING = 1


@dataclass(frozen=True)
class FSM:
    seq: tuple[int, ...]
    acc: tuple[int, ...]
    search: str

    @property
    def state(self) -> State:
        if not self.seq:
            return State.DONE
        return State.DOING

    @staticmethod
    def binary_search(array: tuple[int, ...], target: int) -> int:
        """return an index to cut the input sequence into two arrays s.t.:
        1. each element of the first array is less than or equal to the target
        2. each element of the second array is greater than the target

        :param array: sorted ascending array to search
        :param target: target integer
        :return: cut index, -1 if all elements of the input array is greater
            than the input target
        """
        idx_min = -1
        idx_max = len(array)
        while True:
            if idx_max - idx_min <= 1:
                return idx_min
            idx_mid = (idx_max + idx_min) // 2
            if target <= array[idx_mid]:
                idx_max = idx_mid
            else:
                idx_min = idx_mid

    @staticmethod
    def traversal_search(array: tuple[int, ...], target: int) -> int:
        """same function as `binary_search` but using traversal
        """
        def helper(idx: int):
            while True:
                try:
                    pivot = array[idx]
                    if pivot >= target:
                        return idx - 1
                    idx += 1
                except IndexError:
                    return idx - 1

        return helper(0)

    @property
    def search_func(self) -> Callable[[tuple[int, ...], int], int]:
        if self.search == 'binary':
            return self.binary_search
        return self.traversal_search

    def transform(self) -> FSM:
        assert self.state == State.DOING
        num = self.seq[0]
        cut = self.search_func(self.acc, num) + 1
        new_acc = (*self.acc[:cut], num, *self.acc[cut:])
        return (type(self))(self.seq[1:], new_acc, self.search)


class InsertionSort:
    @staticmethod
    def looper(fsm: FSM) -> tuple[int, ...]:
        fsm_ = fsm
        while True:
            if fsm_.state == State.DONE:
                return fsm_.acc
            fsm_ = fsm_.transform()

    def solution(self, seq: tuple[int, ...], binary: bool = True):
        search = 'binary' if binary else 'traversal'
        fsm = FSM(seq, (), search)
        return self.looper(fsm)


if __name__ == '__main__':
    ipt_1 = (2, 4, 6, 0, 1, 9, 3, 8, 5, 7)
    exp_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    assert FSM.binary_search(exp_1, 5.5) == 5
    assert FSM.binary_search(exp_1, -1) == -1
    assert FSM.binary_search(exp_1, 0) == -1
    assert FSM.binary_search(exp_1, 0.1) == 0
    assert FSM.binary_search(exp_1, 8.5) == 8
    assert FSM.binary_search(exp_1, 9) == 8
    assert FSM.binary_search(exp_1, 100) == 9
    assert FSM.traversal_search(exp_1, 5.5) == 5
    assert FSM.traversal_search(exp_1, -1) == -1
    assert FSM.traversal_search(exp_1, 0) == -1
    assert FSM.traversal_search(exp_1, 0.1) == 0
    assert FSM.traversal_search(exp_1, 8.5) == 8
    assert FSM.traversal_search(exp_1, 9) == 8
    assert FSM.traversal_search(exp_1, 100) == 9

    sort = InsertionSort()
    assert sort.solution(ipt_1) == exp_1
