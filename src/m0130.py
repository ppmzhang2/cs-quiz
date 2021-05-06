"""Surrounded Regions
Given a 2D board containing 'X' and 'O' (the letter O), capture all regions
surrounded by 'X'.

A region is captured by flipping all 'O's into 'X's in that surrounded region.

Example:

X X X X
X O O X
X X O X
X O X X

After running your function, the board should be:

X X X X
X X X X
X X X X
X O X X

Explanation:

Surrounded regions shouldn’t be on the border, which means that any 'O' on the
border of the board are not flipped to 'X'. Any 'O' that is not on the border
and it is not connected to an 'O' on the border will be flipped to 'X'. Two
cells are connected if they are adjacent cells connected horizontally or
vertically.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from functools import reduce
from typing import Optional, Tuple

import numpy as np


@dataclass(frozen=True)
class Segment:
    """line segment (i.e. adjacent dots)
    """
    lower: int
    upper: int

    def distance(self, seg: Segment) -> int:
        new_upper = min(self.upper, seg.upper)
        new_lower = max(self.lower, seg.lower)
        if new_upper >= new_lower:
            return 0
        return new_lower - new_upper

    def adjacent(self, seg: Segment) -> bool:
        if self.distance(seg) == 0:
            return True
        return False

    def union(self, seg: Segment) -> Optional[Segment]:
        if self.distance(seg) >= 2:
            return None
        new_upper = max(self.upper, seg.upper)
        new_lower = min(self.lower, seg.lower)
        return (type(self))(new_lower, new_upper)


@dataclass(frozen=True)
class SegmentGroup:
    position: int
    segments: Tuple[Segment, ...]
    y: bool = False

    @property
    def empty(self) -> bool:
        return not self.segments

    def adjacent(self, seg: Segment) -> bool:
        return reduce(lambda x, y: x or y,
                      tuple(seg.adjacent(s) for s in self.segments))

    def move(self, sg: SegmentGroup) -> Optional[SegmentGroup]:
        if abs(self.position - sg.position) >= 2:
            return None
        bools = tuple(self.adjacent(s) for s in sg.segments)
        return SegmentGroup(
            sg.position,
            tuple(s for b, s in zip(bools, sg.segments) if b),
            self.y,
        )

    @property
    def points(self):
        if not self.y:
            return tuple((self.position, j) for seg in self.segments
                         for j in range(seg.lower, seg.upper + 1))
        return tuple((j, self.position) for seg in self.segments
                     for j in range(seg.lower, seg.upper + 1))


@unique
class State(IntEnum):
    DOING = 0
    MERGED_NOT_COPIED = 1
    COPIED_NOT_FINISHED = 2
    DONE = 3


@dataclass(frozen=True)
class FSM:
    """
    the first element of the `ordered_groups` should be on border
    """
    ordered_groups: Tuple[Optional[SegmentGroup], ...]
    acc: Tuple[SegmentGroup, ...]

    @property
    def length(self) -> int:
        return len(self.ordered_groups)

    @property
    def state(self) -> State:
        if self.length <= 1:
            return State.DONE
        sg = self.ordered_groups[0]
        if not sg or sg.empty:
            return State.DONE
        return State.DOING

    @property
    def points(self) -> Tuple[Tuple[int, int], ...]:
        return tuple(p for sg in self.acc for p in sg.points)

    def transform(self) -> FSM:
        assert self.state == State.DOING
        sg1 = self.ordered_groups[0]
        sg2 = self.ordered_groups[1]
        new_sg = sg1.move(sg2)
        new_groups = (new_sg, *self.ordered_groups[2:])
        if not new_sg or new_sg.empty:
            acc = self.acc
        else:
            acc = (*self.acc, new_sg)
        return (type(self))(new_groups, acc)


class SurroundedRegion:
    __slots__ = ('array', )

    def __init__(self, array: np.array):
        self.array = array

    @staticmethod
    def merge_segments(segments: Tuple[Segment, ...]) -> Tuple[Segment, ...]:
        """
        Examples:
            >>> merge_segments((Segment(1, 2), Segment(2, 3), Segment(5, 7)))
            >>> (Segment(1, 3), Segment(5, 7))
        """
        def helper(
            segments_: Tuple[Segment, ...],
            acc: Tuple[Segment, ...],
        ) -> Tuple[Segment, ...]:
            if not segments_:
                return acc
            seg1 = segments_[0]
            if len(segments_) == 1:
                return (*acc, seg1)
            seg2 = segments_[1]
            new_seg = seg1.union(seg2)
            if not new_seg:
                return helper(segments_[1:], (*acc, seg1))
            return helper((new_seg, *segments_[2:]), acc)

        return helper(segments, ())

    @classmethod
    def to_segment_group(
        cls,
        position: int,
        array: np.array,
        y: bool = False,
    ) -> SegmentGroup:
        indexes = (array == 0).nonzero()[0]
        segments = tuple(Segment(i, i) for i in indexes)
        merged_segments = cls.merge_segments(segments)
        return SegmentGroup(position, merged_segments, y)

    @property
    def shape(self) -> Tuple[int, int]:
        return self.array.shape

    @property
    def x_length(self) -> int:
        return self.shape[0]

    @property
    def y_length(self) -> int:
        return self.shape[1]

    def segment_group(
        self,
        y: bool = False,
        desc: bool = False,
    ) -> Tuple[SegmentGroup, ...]:
        if not y:
            sgs = tuple(
                self.to_segment_group(i, self.array[i, :], y)
                for i in range(self.x_length))
        else:
            sgs = tuple(
                self.to_segment_group(i, self.array[:, i], y)
                for i in range(self.y_length))
        if desc:
            return sgs[::-1]
        return sgs

    @staticmethod
    def looper(fsm: FSM) -> Tuple[Tuple[int, int], ...]:
        fsm_ = fsm
        while True:
            if fsm_.state == State.DONE:
                return fsm_.points
            fsm_ = fsm_.transform()

    def zeros(self):
        def helper(
            y: bool = False,
            desc: bool = False,
        ) -> Tuple[Tuple[int, int], ...]:
            sgs = self.segment_group(y, desc)
            fsm = FSM(sgs, (sgs[0], ))
            return self.looper(fsm)

        bools = ((False, False), (False, True), (True, False), (True, True))
        seq_points = tuple(helper(y, d) for y, d in bools)
        return tuple(sorted({p for tp in seq_points for p in tp}))

    def solution(self):
        zero_points = self.zeros()
        mat = np.ones(self.shape, np.int8)
        for p in zero_points:
            mat[p[0], p[1]] = 0
        return mat


if __name__ == '__main__':
    ipt_1 = np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [1, 0, 1, 1],
    ])
    exp_1 = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 0, 1, 1],
    ])
    ipt_2 = np.array([
        [1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ])
    exp_2 = np.array([
        [1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ])

    # segment = Segment(3, 7)
    # assert segment.union(Segment(4, 6)) == Segment(3, 7)
    # assert segment.union(Segment(1, 1)) is None
    # assert segment.union(Segment(1, 2)) == Segment(1, 7)
    # assert segment.union(Segment(1, 3)) == Segment(1, 7)
    # assert segment.union(Segment(7, 8)) == Segment(3, 8)

    # segment_group = SegmentGroup(1, (Segment(0, 3), Segment(6, 8)))
    # assert segment_group.adjacent(Segment(4, 5)) is False
    # assert segment_group.adjacent(Segment(9, 10)) is False
    # assert segment_group.adjacent(Segment(2, 5)) is True
    # assert segment_group.adjacent(Segment(1, 9)) is True

    assert ((SurroundedRegion(ipt_1).solution() - exp_1) == 0).all()
    assert ((SurroundedRegion(ipt_2).solution() - exp_2) == 0).all()
