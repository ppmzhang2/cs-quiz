"""Set Matrix Zeroes
TAG: untagged

Given an m x n matrix. If an element is 0, set its entire row and column to 0.
Do it in-place.

Follow up:
* A straight forward solution using O(mn) space is probably a bad idea.
* A simple improvement uses O(m + n) space, but still not the best solution.
* Could you devise a constant space solution?

Example 1:
Input: = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]
Output: [
    [1, 0, 1],
    [0, 0, 0],
    [1, 0, 1],
]

Example 2:
Input: [
    [0, 1, 2, 0],
    [3, 4, 5, 2],
    [1, 3, 1, 5],
]
Output: [
    [0, 0, 0, 0],
    [0, 4, 5, 0],
    [0, 3, 1, 0],
]

Constraints:
* m == matrix.length
* n == matrix[0].length
* 1 <= m, n <= 200
* -2^31 <= matrix[i][j] <= 2^31 - 1
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Cell:
    x: int
    y: int
    value: int


@dataclass
class Matrix:
    rows: Sequence[int]
    columns: Sequence[int]
    cells: Sequence[Cell]

    @classmethod
    def from_array(cls, array: Sequence[Sequence[int]]) -> Matrix:
        cells = []
        rows = []
        columns = []
        for row_id, seq in enumerate(array):
            for col_id, value in enumerate(seq):
                cells.append(Cell(row_id, col_id, value))
                if value == 0:
                    rows.append(row_id)
                    columns.append(col_id)

        return cls(rows, columns, cells)

    def zeronize(self) -> Sequence[Cell]:
        seq = []
        for cell in self.cells:
            if cell.x in self.rows or cell.y in self.columns:
                seq.append(Cell(cell.x, cell.y, 0))
            else:
                seq.append(cell)

        return seq


class SetMatrixZeroes:
    @staticmethod
    def to_array(cells: Sequence[Cell]):
        rows = max(cell.x for cell in cells) + 1
        cols = max(cell.y for cell in cells) + 1

        array = []
        row = []
        for _ in range(rows):
            for _ in range(cols):
                row.append(0)
            array.append(row)
            row = []

        for cell in cells:
            array[cell.x][cell.y] = cell.value

        return array

    def solution(self, array: Sequence[Sequence[int]]):
        matrix = Matrix.from_array(array)
        cells = matrix.zeronize()
        return self.to_array(cells)


if __name__ == '__main__':
    ipt_1 = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    exp_1 = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1],
    ]
    ipt_2 = [
        [0, 1, 2, 0],
        [3, 4, 5, 2],
        [1, 3, 1, 5],
    ]
    exp_2 = [
        [0, 0, 0, 0],
        [0, 4, 5, 0],
        [0, 3, 1, 0],
    ]

    # matrix = Matrix.from_array(ipt_1)
    # print(matrix.zeronize())
    # print(Matrix.to_array(matrix.zeronize()))
    smz = SetMatrixZeroes()
    assert smz.solution(ipt_1) == exp_1
    assert smz.solution(ipt_2) == exp_2
