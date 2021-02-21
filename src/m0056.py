"""merge intervals
Given an array of intervals where intervals[i] = [start_i, end_i], merge all
overlapping intervals, and return an array of the non-overlapping intervals
that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
* 1 <= intervals.length <= 10^4
* intervals[i].length == 2
* 0 <= start_i <= end_i <= 10^4
"""
from __future__ import annotations

from typing import NamedTuple, Sequence


class Middleware(NamedTuple):
    start: int
    end: int

    def compare(self, mw: Middleware):
        if mw.end < self.start:
            return -1
        if mw.end >= self.start and mw.end <= self.end:
            return 0
        if mw.start >= self.start and mw.start <= self.end:
            return 0
        if self.end >= mw.start and self.end <= mw.end:
            return 0
        if self.start >= mw.start and self.start <= mw.end:
            return 0
        if mw.start > self.end:
            return 1
        raise ValueError('invalid middleware')

    def merge(self, mw: Middleware):
        assert self.compare(mw) == 0
        return Middleware(min(self.start, mw.start), max(self.end, mw.end))


class MergeIntervals:
    @classmethod
    def merge(cls, inputs: Sequence[Middleware],
              outputs: Sequence[Middleware]):
        if not inputs:
            return outputs
        mw1 = inputs[0]
        if len(inputs) == 1:
            return (*outputs, mw1)
        mw2 = inputs[1]
        if mw1.compare(mw2) == 0:
            return cls.merge((mw1.merge(mw2), *inputs[2:]), outputs)
        return cls.merge(inputs[1:], (*outputs, mw1))

    def solution(self,
                 seq: Sequence[Sequence[int]]) -> Sequence[Sequence[int]]:
        inputs = tuple(
            sorted((Middleware(t[0], t[1]) for t in seq),
                   key=lambda x: x.start))
        mws = self.merge(inputs, ())
        return tuple((mw.start, mw.end) for mw in mws)


if __name__ == '__main__':
    ipt_1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    exp_1 = (
        (1, 6),
        (8, 10),
        (15, 18),
    )
    ipt_2 = [[1, 4], [4, 5]]
    exp_2 = ((1, 5), )

    mi = MergeIntervals()
    assert mi.solution(ipt_1) == exp_1
    assert mi.solution(ipt_2) == exp_2
