"""rotate image
TAG: array, math

You are given an n x n 2D matrix representing an image, rotate the image by 90
degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input
2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Example 1:
input =
[
  [1,2,3],
  [4,5,6],
  [7,8,9]
],
output =
[
  [7,4,1],
  [8,5,2],
  [9,6,3]
]

Example 1:
input =
[
  [ 5, 1, 9,11],
  [ 2, 4, 8,10],
  [13, 3, 6, 7],
  [15,14,12,16]
],
output =
[
  [15,13, 2, 5],
  [14, 3, 4, 1],
  [12, 6, 8, 9],
  [16, 7,10,11]
]
"""
from typing import List, NamedTuple, Sequence, Tuple

import numpy as np


class Middleware(NamedTuple):
    x: int
    y: int
    value: int


class Rotate:
    MATRIX = np.matrix([[0, 1], [-1, 0]])

    @staticmethod
    def size(arrays: Sequence[Sequence[int]]) -> int:
        return len(arrays)

    @staticmethod
    def ingest(arrays: Sequence[Sequence[int]]) -> Tuple[Middleware, ...]:
        seq = ()
        for i, array in enumerate(arrays):
            for j, num in enumerate(array):
                mw = Middleware(i, j, num)
                seq = (*seq, mw)

        return seq

    def transform(self, mw: Middleware, intercept: int) -> Middleware:
        vec = np.transpose(np.matrix([mw.x, mw.y]))
        rotated_vec = self.MATRIX * vec
        new_vec = rotated_vec + np.transpose(np.matrix([0, intercept]))
        return Middleware(new_vec[0, 0], new_vec[1, 0], mw.value)

    @staticmethod
    def producer(
        mws: Tuple[Middleware, ...],
        size: int,
    ) -> List[List[int]]:
        arrays = [[0 for _ in range(size)] for _ in range(size)]
        for mw in mws:
            arrays[mw.x][mw.y] = mw.value

        return arrays

    def solution(self,
                 arrays: Sequence[Sequence[int]]) -> Sequence[Sequence[int]]:
        size_ = self.size(arrays)
        mw_seq = self.ingest(arrays)
        new_mw_seq = tuple(self.transform(mw, size_ - 1) for mw in mw_seq)
        return self.producer(new_mw_seq, size_)


if __name__ == '__main__':
    ipt_1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    opt_1 = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3],
    ]

    ipt_2 = [
        [5, 1, 9, 11],
        [2, 4, 8, 10],
        [13, 3, 6, 7],
        [15, 14, 12, 16],
    ]
    opt_2 = [
        [15, 13, 2, 5],
        [14, 3, 4, 1],
        [12, 6, 8, 9],
        [16, 7, 10, 11],
    ]

    rotate = Rotate()

    # assert rotate.transform(Middleware(0, 0, 1), 2) == Middleware(0, 2, 1)
    # assert rotate.transform(Middleware(0, 1, 2), 2) == Middleware(1, 2, 2)
    # assert rotate.transform(Middleware(1, 1, 5), 2) == Middleware(1, 1, 5)
    # assert rotate.transform(Middleware(1, 0, 4), 2) == Middleware(0, 1, 4)

    assert rotate.solution(ipt_1) == opt_1
    assert rotate.solution(ipt_2) == opt_2
