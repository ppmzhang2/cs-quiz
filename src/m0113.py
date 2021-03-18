"""Path Sum II
Given the root of a binary tree and an integer targetSum, return all
root-to-leaf paths where each path's sum equals targetSum.

A leaf is a node with no children.

Example 1:
Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2],[5,8,4,5]]

Example 2:
Input: root = [1,2,3], targetSum = 5
Output: []

Example 3:
Input: root = [1,2], targetSum = 0
Output: []

Constraints:

* The number of nodes in the tree is in the range [0, 5000].
* -1000 <= Node.val <= 1000
* -1000 <= targetSum <= 1000
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class Point:
    value: Optional[int]
    index: int

    @property
    def none(self) -> bool:
        return not self.value


@unique
class NodeState(IntEnum):
    LEAF = 1
    LEFT_ONLY = 2
    RIGHT_ONLY = 3
    TREE = 4


@dataclass(frozen=True)
class Node:
    root: int
    left: Point
    right: Point

    @property
    def state(self) -> NodeState:
        if self.left.none and self.right.none:
            return NodeState.LEAF
        if self.right.none:
            return NodeState.LEFT_ONLY
        if self.left.none:
            return NodeState.RIGHT_ONLY
        return NodeState.TREE


@unique
class State(IntEnum):
    INIT = 0
    DOING = 1
    DONE = 2
    INVALID = 3


@dataclass(frozen=True)
class FSM:
    seq: Tuple[Optional[Node], ...]
    target: int
    actions: Tuple[Node, ...]

    @property
    def last_action(self) -> Optional[Node]:
        if not self.actions:
            return None
        return self.actions[-1]

    @property
    def state(self) -> State:
        if self.num == self.target:
            return State.DONE
        if not self.actions:
            return State.INIT
        if (self.last_action.state == NodeState.LEAF
                and self.num != self.target):
            return State.INVALID
        return State.DOING

    @property
    def num(self) -> int:
        return sum((node.root for node in self.actions))

    def init(self) -> FSM:
        assert self.state == State.INIT
        node = self.seq[0]
        return FSM(self.seq, self.target, (node, ))

    def explode(self) -> Tuple[FSM, ...]:
        assert self.state == State.DOING
        node = self.last_action
        if node.state == NodeState.LEFT_ONLY:
            new_nodes = (self.seq[node.left.index], )
        elif node.state == NodeState.RIGHT_ONLY:
            new_nodes = (self.seq[node.right.index], )
        elif node.state == NodeState.TREE:
            new_nodes = (self.seq[node.left.index], self.seq[node.right.index])
        return tuple(
            type(self)(self.seq, self.target, (*self.actions, new_node))
            for new_node in new_nodes)


class PathSum2:
    @staticmethod
    def item2node(value: int, idx: int, seq: Sequence[int]) -> Node:
        def helper(seq_: Sequence[int], idx_: int) -> Optional[int]:
            try:
                return seq_[idx_]
            except IndexError:
                return None

        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2

        return Node(
            value,
            Point(helper(seq, left_idx), left_idx),
            Point(helper(seq, right_idx), right_idx),
        )

    @classmethod
    def get_node_seq(cls, seq: Sequence[int]) -> Tuple[Node, ...]:
        """convert an Optional[Integer] sequence into a Optional[Node] sequence
        this is a one-to-one transform and if the value in the source sequence
        is None, the corresponding one is still None
        """
        def valid_index(seq):
            i = 0
            for val in seq:
                yield i
                if val:
                    i += 1

        return tuple(None if not value else cls.item2node(value, idx, seq)
                     for idx, value in zip(valid_index(seq), seq))

    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[FSM, ...],
    ) -> Tuple[FSM, ...]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.state == State.INIT:
            return cls.looper((fsm.init(), *inputs[1:]), outputs)
        if fsm.state == State.INVALID:
            return cls.looper(inputs[1:], outputs)
        if fsm.state == State.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        return cls.looper((*fsm.explode(), *inputs[1:]), outputs)

    def solution(self, seq: Sequence[int], target: int):
        nodes = self.get_node_seq(seq)
        fsm = FSM(nodes, target, ())
        fsm_seq = self.looper((fsm, ), ())
        return tuple(
            tuple(node.root for node in fsm.actions) for fsm in fsm_seq)


if __name__ == '__main__':
    ipt_1_1 = (5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1)
    ipt_1_2 = 22
    exp_1 = ((5, 4, 11, 2), (5, 8, 4, 5))
    ipt_2_1 = (1, 2, 3)
    ipt_2_2 = 5
    exp_2 = ()
    ipt_3_1 = (1, 2)
    ipt_3_2 = 0
    exp_3 = ((), )
    ipt_4_1 = (1, 2, 3, None, None, 4, None, None, 5)
    ipt_4_2 = 13
    exp_4 = ((1, 3, 4, 5), )

    ps = PathSum2()
    # print(ps.get_node_seq(ipt_4_1))

    print(ps.solution(ipt_2_1, ipt_2_2))
    print(ps.solution(ipt_3_1, ipt_3_2))

    assert exp_1 == ps.solution(ipt_1_1, ipt_1_2)
    assert exp_2 == ps.solution(ipt_2_1, ipt_2_2)
    assert exp_3 == ps.solution(ipt_3_1, ipt_3_2)
    assert exp_4 == ps.solution(ipt_4_1, ipt_4_2)
