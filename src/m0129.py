from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class Tree:
    node: int
    subs: Tuple[Tree, ...] = ()

    @property
    def leaf(self) -> bool:
        if not self.subs:
            return True
        return False


@unique
class State(IntEnum):
    DOING = 0
    DONE = 1


@dataclass(frozen=True)
class FSM:
    seq: Tuple[int, ...]
    tree: Optional[Tree]

    @property
    def state(self) -> State:
        if self.tree is None:
            return State.DONE
        return State.DOING

    @property
    def num(self) -> int:
        if not self.seq:
            return 0
        return int(''.join((str(i) for i in self.seq)))

    def explode(self) -> Tuple[FSM, ...]:
        assert self.state == State.DOING
        if self.tree.leaf:
            return (FSM((*self.seq, self.tree.node), None), )
        return tuple(
            (FSM((*self.seq, self.tree.node), tr) for tr in self.tree.subs))


class SumRootToLeaf:
    @classmethod
    def looper(cls, inputs: Sequence[FSM],
               outputs: Sequence[int]) -> Sequence[int]:
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.state == State.DONE:
                inputs, outputs = inputs[1:], (*outputs, fsm.num)
            else:
                inputs = (*inputs[1:], *fsm.explode())

    def solution(self, tree: Tree):
        fsm = FSM((), tree)
        fsm_seq = self.looper((fsm, ), ())
        return sum(fsm_seq)


if __name__ == '__main__':
    ipt_1 = Tree(1, (Tree(2), Tree(3)))
    exp_1 = 25
    ipt_2 = Tree(4, (Tree(9, (Tree(5), Tree(1))), Tree(0)))
    exp_2 = 1026

    srtl = SumRootToLeaf()
    assert exp_1 == srtl.solution(ipt_1)
    assert exp_2 == srtl.solution(ipt_2)
