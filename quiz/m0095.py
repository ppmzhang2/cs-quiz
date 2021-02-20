"""Unique Binary Search Trees II
TAG: dynamic-programming

Given an integer n, return all the structurally unique BST's (binary search
trees), which has exactly n nodes of unique values from 1 to n. Return the
answer in any order.

Example 1:
Input: n = 3

 1    1        2        3     3
  \    \      / \      /     /
   3    2    1   3    2     1
  /      \           /       \
 2        3         1         2

Output: [[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]

Example 2:
Input: n = 1
Output: [[1]]

Constraints:
* 1 <= n <= 8
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional, Tuple


@unique
class TreeStatus(Enum):
    UNFACTORED = 1
    FULL_TREE = 2
    LEFT_TREE = 3
    RIGHT_TREE = 4
    LEAF = 5
    INVALID = 6


@dataclass(frozen=True)
class Tree:
    root: Tuple[int, ...]
    left: Optional[Tree]
    right: Optional[Tree]

    @property
    def width(self):
        return len(self.root)

    @property
    def status(self):
        if (self.width >= 2 and (self.left and self.right)):
            return TreeStatus.INVALID
        if self.width >= 2:
            return TreeStatus.UNFACTORED
        if not self.left and not self.right:
            return TreeStatus.LEAF
        if not self.left:
            return TreeStatus.RIGHT_TREE
        if not self.right:
            return TreeStatus.LEFT_TREE
        return TreeStatus.FULL_TREE

    def transform(self, idx) -> Tree:
        assert 0 <= idx < self.width
        assert self.status == TreeStatus.UNFACTORED
        root = (self.root[idx], )
        left = self.root[:idx]
        right = self.root[idx + 1:]
        return (type(self))(
            root,
            None if not left else (type(self))(left, None, None),
            None if not right else (type(self))(right, None, None),
        )

    def explode(self) -> Tuple[Tree, ...]:
        assert self.status == TreeStatus.UNFACTORED
        return tuple(self.transform(idx) for idx in range(self.width))


@unique
class Status(Enum):
    EMPTY = 0
    UNFACTORED = 1
    TREE = 2
    LEAF = 3
    DONE = 4
    INVALID = 5


@dataclass(frozen=True)
class FSM:
    inputs: Tuple[Optional[Tree], ...]
    outputs: Tuple[Optional[int], ...]

    @property
    def status(self):
        if not self.inputs:
            return Status.DONE
        tree = self.inputs[0]
        if not tree:
            return Status.EMPTY
        if tree.status == TreeStatus.INVALID:
            return Status.INVALID
        if tree.status == TreeStatus.UNFACTORED:
            return Status.UNFACTORED
        if tree.status == TreeStatus.LEAF:
            return Status.LEAF
        return Status.TREE

    def explode(self) -> Tuple[FSM, ...]:
        assert self.status == Status.UNFACTORED
        tree = self.inputs[0]
        remaining = self.inputs[1:]
        seq_tree = tree.explode()
        return tuple(
            (type(self))((tr, *remaining), self.outputs) for tr in seq_tree)

    def transform(self) -> FSM:
        assert self.status in (Status.EMPTY, Status.TREE, Status.LEAF)
        tree = self.inputs[0]
        remaining = self.inputs[1:]
        if self.status == Status.EMPTY:
            return (type(self))(remaining, (*self.outputs, tree))
        if self.status == Status.LEAF:
            return (type(self))(remaining, (*self.outputs, tree.root[0]))
        return (type(self))((
            *(tree.left, tree.right, Tree(tree.root, None, None)),
            *remaining,
        ), self.outputs)


class UniqueBST:
    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[FSM, ...],
    ) -> Tuple[FSM, ...]:
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.status == Status.INVALID:
                inputs = inputs[1:]
            elif fsm.status == Status.DONE:
                inputs, outputs = inputs[1:], (*outputs, fsm)
            elif fsm.status == Status.UNFACTORED:
                inputs = (*fsm.explode(), *inputs[1:])
            else:
                inputs = (fsm.transform(), *inputs[1:])

    def solution(self, n: int):
        tree = Tree(tuple(range(n)), None, None)
        fsm = FSM((tree, ), ())
        fsm_seq = self.looper((fsm, ), ())
        paths = [fsm_.outputs for fsm_ in fsm_seq]
        return len(paths)


if __name__ == '__main__':
    # Catalan numbers
    ipt_1 = 1
    exp_1 = 1
    ipt_2 = 2
    exp_2 = 2
    ipt_3 = 3
    exp_3 = 5
    ipt_4 = 4
    exp_4 = 14
    ipt_5 = 5
    exp_5 = 42
    ipt_6 = 6
    exp_6 = 132
    ipt_7 = 7
    exp_7 = 429
    ipt_8 = 8
    exp_8 = 1430

    bst = UniqueBST()

    assert bst.solution(ipt_1) == exp_1
    assert bst.solution(ipt_2) == exp_2
    assert bst.solution(ipt_3) == exp_3
    assert bst.solution(ipt_4) == exp_4
    assert bst.solution(ipt_5) == exp_5
    assert bst.solution(ipt_6) == exp_6
    assert bst.solution(ipt_7) == exp_7
    assert bst.solution(ipt_8) == exp_8
