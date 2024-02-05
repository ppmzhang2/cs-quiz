"""binary-tree-zigzag-level-order-traversal

Given a binary tree, return the zigzag level order traversal of its nodes'
values. (ie, from left to right, then right to left for the next level and
alternate between).

For example:
Given binary tree [3,9,20,null,null,15,7],
    3
   / \
  9  20
    /  \
   15   7
return its zigzag level order traversal as:
[
  [3],
  [20,9],
  [15,7]
]
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple


@unique
class State(IntEnum):
    TREE = 1
    LEAF = 2


@dataclass(frozen=True)
class BTree:
    root: int
    left: Optional[BTree] = None
    right: Optional[BTree] = None

    def explode(self, desc: bool) -> Tuple[BTree, ...]:
        if not self.left and not self.right:
            return ()
        if not self.left:
            return (self.right, )
        if not self.right:
            return (self.left, )
        if desc:
            return (self.right, self.left)
        return (self.left, self.right)


@dataclass(frozen=True)
class BTreePlus:
    tree: BTree
    level: int
    desc: bool

    def explode(self) -> Tuple[BTreePlus, ...]:
        seq_tree = self.tree.explode(self.desc)
        level = self.level + 1
        desc = (not self.desc)
        return tuple((type(self))(tr, level, desc) for tr in seq_tree)

    @property
    def state(self):
        if not self.tree.left and not self.tree.right:
            return State.LEAF
        return State.TREE


@dataclass(frozen=True)
class Node:
    value: int
    level: int


class ZigzagLevelOrderTraverse:
    @classmethod
    def looper(
        cls,
        inputs: Tuple[BTreePlus, ...],
        outputs: Tuple[Node, ...],
    ) -> Tuple[Node, ...]:
        if not inputs:
            return outputs
        bt = inputs[0]
        if bt.state == State.LEAF:
            return cls.looper(
                inputs[1:],
                (*outputs, Node(bt.tree.root, bt.level)),
            )
        return cls.looper(
            (*inputs[1:], *bt.explode()),
            (*outputs, Node(bt.tree.root, bt.level)),
        )

    def solution(self, btree: BTree):
        bt = BTreePlus(btree, 0, True)
        seq_node = self.looper((bt, ), ())
        res_seq = []
        level_seq = []
        level = 0
        for node in seq_node:
            if node.level != level:
                res_seq.append(level_seq)
                level += 1
                level_seq = []
            level_seq.append(node.value)
        res_seq.append(level_seq)

        return res_seq


if __name__ == '__main__':
    ipt_1 = BTree(3, BTree(9), BTree(20, BTree(15), BTree(7)))
    exp_1 = [[3], [20, 9], [15, 7]]

    zlot = ZigzagLevelOrderTraverse()
    assert exp_1 == zlot.solution(ipt_1)
