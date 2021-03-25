from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Tuple


@dataclass(frozen=True)
class Point:
    office: bool
    school: bool
    store: bool

    @staticmethod
    def from_tuple(tp: Tuple[bool, bool, bool]) -> Point:
        return Point(*tp)


@unique
class State(Enum):
    INIT = 0
    MOVING = 1
    SEARCHING = 2
    DONE = 3
    INVALID = 4


@unique
class Action(Enum):
    MOVE = 1
    STAY = 2


@dataclass(frozen=True)
class FSM:  #pylint: disable=too-many-instance-attributes
    to_office: int
    to_school: int
    to_store: int
    no_office: bool
    no_school: bool
    no_store: bool
    actions: Tuple[Action, ...]
    points: Tuple[Point, ...]

    @property
    def state(self):
        if not self.actions:
            return State.INIT
        if ((not self.no_office) and (not self.no_school)
                and (not self.no_store)):
            return State.DONE
        if not self.points:
            return State.INVALID
        action = self.actions[-1]
        if action == Action.MOVE:
            return State.MOVING
        return State.SEARCHING

    @property
    def distance(self):
        return max(self.to_office, self.to_school, self.to_store)

    def move(self) -> FSM:
        def helper(to_place: int, no_place: bool, has_place: bool):
            if has_place:
                return 0, False
            to_place_ = 0 if no_place else to_place + 1
            return to_place_, no_place

        assert self.state in (State.INIT, State.MOVING)
        point = self.points[0]

        to_office, no_office = helper(
            self.to_office,
            self.no_office,
            point.office,
        )
        to_school, no_school = helper(
            self.to_school,
            self.no_school,
            point.school,
        )
        to_store, no_store = helper(
            self.to_store,
            self.no_store,
            point.store,
        )
        return FSM(
            to_office,
            to_school,
            to_store,
            no_office,
            no_school,
            no_store,
            (*self.actions, Action.MOVE),
            self.points[1:],
        )

    def search(self) -> FSM:
        assert self.state in (State.MOVING, State.SEARCHING)
        point = self.points[0]

        def helper(
            to_place: int,
            no_place: bool,
            has_place: bool,
        ) -> Tuple[int, bool]:
            if not no_place:
                return to_place, no_place
            if has_place:
                return to_place + 1, False
            return to_place + 1, True

        to_office, no_office = helper(
            self.to_office,
            self.no_office,
            point.office,
        )
        to_school, no_school = helper(
            self.to_school,
            self.no_school,
            point.school,
        )
        to_store, no_store = helper(
            self.to_store,
            self.no_store,
            point.store,
        )
        return FSM(
            to_office,
            to_school,
            to_store,
            no_office,
            no_school,
            no_store,
            (*self.actions, Action.STAY),
            self.points[1:],
        )


class FindAppartment:
    @classmethod
    def looper(cls, inputs: Tuple[FSM, ...], outputs: Tuple[FSM, ...]):
        if not inputs:
            return outputs

        fsm = inputs[0]

        if fsm.state == State.INVALID:
            return cls.looper(inputs[1:], outputs)
        if fsm.state == State.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        if fsm.state == State.INIT:
            return cls.looper((fsm.move(), *inputs[1:]), outputs)
        if fsm.state == State.SEARCHING:
            return cls.looper((fsm.search(), *inputs[1:]), outputs)
        return cls.looper((fsm.move(), fsm.search(), *inputs[1:]), outputs)

    def solution(self, seq: Tuple[Tuple[bool, bool, bool], ...]):
        points = tuple(Point.from_tuple(tp) for tp in seq)
        fsm = FSM(0, 0, 0, True, True, True, (), points)
        res = self.looper((fsm, ), ())
        best = min(res, key=lambda x: x.distance)
        return best


if __name__ == '__main__':
    ipt_1 = (
        (True, False, False),
        (False, True, False),
        (False, False, True),
    )
    ipt_2 = (
        (False, True, False),
        (True, False, False),
        (True, True, False),
        (False, True, False),
        (False, True, True),
    )

    f = FindAppartment()
    print(f.solution(ipt_1))
    print(f.solution(ipt_2))
