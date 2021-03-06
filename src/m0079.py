"""Word Search
TAG: back-tracking

Given an m x n board and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where
"adjacent" cells are horizontally or vertically neighboring. The same letter
cell may not be used more than once.

Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "ABCB"
Output: false

Constraints:
* m == board.length
* n = board[i].length
* 1 <= m, n <= 200
* 1 <= word.length <= 103
* board and word consists only of lowercase and uppercase English letters.
"""
from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Sequence, Tuple


class Coordinate(NamedTuple):
    x: int
    y: int
    size: Tuple[int, int]

    def adjacent(self) -> Tuple[Coordinate]:
        max_x = self.size[0] - 1
        max_y = self.size[1] - 1
        xs = filter(lambda x: 0 <= x <= max_x, (self.x - 1, self.x + 1))
        ys = filter(lambda y: 0 <= y <= max_y, (self.y - 1, self.y + 1))
        return (
            *(Coordinate(self.x, y, self.size) for y in ys),
            *(Coordinate(x, self.y, self.size) for x in xs),
        )


class ValuedCoordinate(NamedTuple):
    coor: Coordinate
    value: str


class Status(Enum):
    START = 0
    DOING = 1
    DONE = 2


class FSM(NamedTuple):
    matrix: Sequence[Sequence[str]]
    words: Sequence[str]
    trace: Sequence[Coordinate]

    @property
    def status(self):
        if not self.words:
            return Status.DONE
        if not self.trace:
            return Status.START
        return Status.DOING

    @staticmethod
    def matrix_size(matrix: Sequence[Sequence[str]]) -> Tuple[int, int]:
        x = len(matrix)
        assert x > 0
        y = len(matrix[0])
        return (x, y)

    @staticmethod
    def get_value(matrix: Sequence[Sequence[str]], coordinate: Coordinate):
        return matrix[coordinate.x][coordinate.y]

    def all_valued_coord(self) -> Sequence[Coordinate]:
        size_x, size_y = self.matrix_size(self.matrix)
        coords = tuple(
            Coordinate(x, y, (size_x, size_y)) for x in range(size_x)
            for y in range(size_y))
        return tuple(
            ValuedCoordinate(coord, self.get_value(self.matrix, coord))
            for coord in coords)

    def initialize(self) -> Tuple[FSM, ...]:
        assert self.status == Status.START
        char = self.words[0]
        valued_coords = self.all_valued_coord()
        valid_valued_coords = filter(lambda x: x.value == char, valued_coords)
        valid_coordinates = (vc.coor for vc in valid_valued_coords
                             if vc.coor not in self.trace)
        return tuple(
            FSM(self.matrix, self.words[1:], (*self.trace, coor))
            for coor in valid_coordinates)

    def explode(self) -> Tuple[FSM, ...]:
        assert self.status == Status.DOING
        char = self.words[0]
        coordinates = self.trace[-1].adjacent()
        valued_coords = [
            ValuedCoordinate(coor, self.get_value(self.matrix, coor))
            for coor in coordinates
        ]
        valid_seq = tuple(
            filter(lambda x: x.value == char and x.coor not in self.trace,
                   valued_coords))
        valid_coordinates = tuple(tp[0] for tp in valid_seq)
        return tuple(
            FSM(self.matrix, self.words[1:], (*self.trace, coordinate))
            for coordinate in valid_coordinates)


class WordSearch:
    @classmethod
    def looper(cls, inputs: Sequence[FSM],
               outputs: Sequence[FSM]) -> Sequence[FSM]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.status == Status.START:
            return cls.looper((*inputs[1:], *fsm.initialize()), outputs)
        if fsm.status == Status.DOING:
            return cls.looper((*inputs[1:], *fsm.explode()), outputs)
        return cls.looper(inputs[1:], (*outputs, fsm))

    def solution(self, matrix: Sequence[Sequence[str]], word: str):
        fsm_seq = self.looper((FSM(matrix, tuple(word), ()), ), ())
        if not fsm_seq:
            return False
        return True


if __name__ == '__main__':
    ipt_1_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_1_2 = "ABCCED"
    exp_1 = True
    ipt_2_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_2_2 = "SEE"
    exp_2 = True
    ipt_3_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_3_2 = "ABCB"
    exp_3 = False

    ws = WordSearch()

    # print(FSM(ipt_1_1, ('B', 'C'), (Coordinate(0, 0, (3, 4)), )).explode())
    # print(FSM(ipt_1_1, ('Z', 'C'), (Coordinate(0, 0, (3, 4)), )).explode())
    # fsm1, fsm2 = FSM(ipt_1_1, ('A', 'B', 'C', 'C', 'D', 'E'), ()).initialize()
    # print(fsm1)
    # print(fsm2)
    # print(fsm1.explode()[0])
    # print(ws.looper((FSM(ipt_1_1, ('A', 'B'), None), ), ()))
    assert ws.solution(ipt_1_1, ipt_1_2) == exp_1
    assert ws.solution(ipt_2_1, ipt_2_2) == exp_2
    assert ws.solution(ipt_3_1, ipt_3_2) == exp_3
