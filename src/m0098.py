from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple


@unique
class Position(IntEnum):
    ROOT = 0
    LEFT = 1
    RIGHT = 2


@unique
class State(IntEnum):
    DOING = 0
    DONE = 1
    INVALID = 2


@dataclass(frozen=True)
class FSM:
    position: Position
    root: Optional[int]
    remaining: Tuple[int, ...]

    @staticmethod
    def split(
            seq: Tuple[int,
                       ...]) -> Tuple[int, Tuple[int, ...], Tuple[int, ...]]:
        root = seq[0]
        seq_ = seq[1:]
        assert len(seq_) % 2 == 0
        length = len(seq_) // 2

        return root, seq_[:length], seq_[length:]

    @property
    def invalid(self) -> bool:
        if self.position == Position.ROOT:
            return False
        if self.position == Position.LEFT:
            seq = filter(lambda n: n is not None and n > self.root,
                         self.remaining)
        else:
            seq = filter(lambda n: n is not None and n < self.root,
                         self.remaining)
        if len(tuple(seq)) >= 1:
            return True
        return False

    @property
    def state(self) -> State:
        if not self.remaining:
            return State.DONE
        if len(self.remaining) % 2 == 0:
            return State.INVALID
        if self.invalid:
            return State.INVALID
        return State.DOING

    def explode(self) -> Tuple[FSM, FSM]:
        assert self.state == State.DOING
        root, left, right = self.split(self.remaining)
        return FSM(Position.LEFT, root, left), FSM(Position.RIGHT, root, right)


class ValidateBinarySearchTree:
    @classmethod
    def looper(cls, inputs: Tuple[FSM, ...]) -> Optional[FSM]:
        if not inputs:
            return None
        fsm = inputs[0]
        if fsm.state == State.INVALID:
            return fsm
        if fsm.state == State.DONE:
            return cls.looper(inputs[1:])
        return cls.looper((*fsm.explode(), *inputs[1:]))

    def solution(self, seq: Tuple[int, ...]):
        fsm = FSM(Position.ROOT, None, seq)
        res = self.looper((fsm, ))
        if not res:
            return True
        return False


if __name__ == '__main__':
    ipt_1 = (2, 1, 3)
    exp_1 = True
    ipt_2 = (5, 1, None, None, 4, 3, 6)
    exp_2 = False

    # print(FSM.split(ipt_1))
    # print(FSM.split(ipt_2))

    vbst = ValidateBinarySearchTree()
    assert exp_1 == vbst.solution(ipt_1)
    assert exp_2 == vbst.solution(ipt_2)
