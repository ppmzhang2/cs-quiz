"""sudoku solution"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from enum import IntEnum, unique

import numpy as np

_X_MAX = _Y_MAX = 8
_COMPLETE_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}


@unique
class State(IntEnum):
    """Sudoku instance's state"""
    INVALID = 0
    DONE = 1
    MOVING = 2
    FILLING = 3


@dataclass
class Sudoku:
    """Sudoku Info"""
    data: np.ndarray
    x: int
    y: int

    @property
    def state(self):
        """state"""
        if self.x > _X_MAX or self.y > _Y_MAX:
            return State.DONE
        if self.cell != 0:
            return State.MOVING
        if self.cell == 0 and not self.possible_values:
            return State.INVALID
        return State.FILLING

    @staticmethod
    def _axis_bound(coor: int) -> tuple[int, int]:
        """coordinate set of the 3*3 group"""
        if coor <= 2:
            return 0, 3
        if coor <= 5:
            return 3, 6
        return 6, 9

    @property
    def _x_bound(self):
        return self._axis_bound(self.x)

    @property
    def _y_bound(self):
        return self._axis_bound(self.y)

    @property
    def cell(self):
        """cell value by x and y"""
        return self.data[self.x, self.y]

    @property
    def row(self):
        """row array"""
        return np.array(self.data[self.x, :], dtype=np.int8)

    @property
    def column(self):
        """column array"""
        return np.array(self.data[:, self.y], dtype=np.int8)

    @property
    def square(self):
        """sub-square array"""
        x1, x2 = self._x_bound
        y1, y2 = self._y_bound
        arr = np.ravel(self.data[x1:x2, y1:y2])
        return np.array(arr, dtype=np.int8)

    @property
    def possible_values(self) -> set:
        """possible values"""
        return (_COMPLETE_SET - set(self.row) - set(self.column) -
                set(self.square))

    @property
    def next_coor(self) -> tuple[int, int]:
        """next coordinates when moving or filling"""
        if self.y == _Y_MAX:
            return self.x + 1, 0
        return self.x, self.y + 1


class FSM:
    """finite state machine"""
    @staticmethod
    def updated_data(sudoku: Sudoku, value: int):
        """updated 9*9 array"""
        data = copy.deepcopy(sudoku.data)
        data[sudoku.x, sudoku.y] = value
        return data

    @staticmethod
    def moved_sudoku(sudoku: Sudoku) -> Sudoku:
        """new Sudoku when the state is `MOVING`"""
        # assert sudoku.state == State.MOVING
        x, y = sudoku.next_coor
        return Sudoku(sudoku.data, x, y)

    @classmethod
    def filled_sudokus(cls, sudoku: Sudoku) -> tuple[Sudoku]:
        """new Sudokus when the state is `FILLING`"""
        # assert sudoku.state == State.FILLING
        x, y = sudoku.next_coor
        return tuple(
            Sudoku(data=cls.updated_data(sudoku, value), x=x, y=y)
            for value in sudoku.possible_values)

    @classmethod
    def transform(cls, inputs: tuple[Sudoku], outputs: tuple[Sudoku]):
        """how to transform Sudoku"""
        while True:
            if not inputs:
                return outputs
            sudoku = inputs[0]
            if sudoku.state == State.INVALID:
                inputs = inputs[1:]
            elif sudoku.state == State.DONE:
                inputs = inputs[1:]
                outputs = (*outputs, sudoku)
            elif sudoku.state == State.MOVING:
                inputs = (cls.moved_sudoku(sudoku), *inputs[1:])
            else:
                inputs = (*cls.filled_sudokus(sudoku), *inputs[1:])

    @classmethod
    def solution(cls, arr):
        """solution to the problem"""
        sudoku = Sudoku(np.array(arr, dtype=np.int8), 0, 0)
        seq_sudoku = cls.transform((sudoku, ), ())
        return tuple(s.data for s in seq_sudoku)


if __name__ == '__main__':
    input_01 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    exp_01 = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    res = FSM.solution(input_01)
    assert (res[0] == np.array(exp_01, dtype=np.int8)).all()
