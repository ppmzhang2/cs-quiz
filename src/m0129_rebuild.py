from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple


@dataclass
class BTree:
    node: int
    left: Optional[BTree] = None
    right: Optional[BTree] = None


@unique
class State(IntEnum):
    FETCHING = 1
    PATCHING = 2
    DONE = 3


@dataclass(frozen=True)
class FSM:
    base: Optional[BTree]
    layer: int
    seq_to_fetch: Tuple[Optional[int], ...]
    seq_to_patch: Tuple[Optional[int], ...]
    trees: Tuple[BTree, ...]

    @property
    def state(self) -> State:
        if not self.seq_to_fetch and not self.seq_to_patch:
            return State.DONE
        if not self.seq_to_patch:
            return State.FETCHING
        return State.PATCHING

    @property
    def n_tree(self) -> int:
        """how many sub-trees to patch
        """
        return len(self.trees)

    @property
    def n_fetch(self) -> int:
        """how many integers to fetch from the source sequence
        """
        nones = len(list(filter(lambda x: x is None, self.seq_to_patch)))
        return 2**self.layer - 2 * nones

    def fetch(self) -> FSM:
        return FSM(
            self.base,
            self.layer,
            self.seq_to_fetch[self.n_fetch:],
            self.seq_to_fetch[:self.n_fetch],
            self.trees,
        )

    def new(self) -> FSM:
        node = self.seq_to_patch[0]
        remains_to_patch = self.seq_to_patch[1:]
        base = BTree(node)
        return FSM(
            base,
            self.layer + 1,
            self.seq_to_fetch,
            remains_to_patch,
            (base, ),
        )

    def add(self) -> FSM:
        left_node, right_node = (*self.seq_to_patch, None, None)[:2]
        tree = self.trees[0]
        remains_to_patch = self.seq_to_patch[2:]
        # update number of layers
        if not remains_to_patch:
            layer = self.layer + 1
        else:
            layer = self.layer
        # update tree if necessary
        if left_node is None and right_node is None:
            seq_tree = self.trees[1:]
        elif right_node is None:
            tree.left = BTree(left_node)
            seq_tree = (*self.trees[1:], tree.left)
        elif left_node is None:
            tree.right = BTree(right_node)
            seq_tree = (*self.trees[1:], tree.right)
        else:
            tree.left, tree.right = BTree(left_node), BTree(right_node)
            seq_tree = (*self.trees[1:], tree.left, tree.right)
        return FSM(
            self.base,
            layer,
            self.seq_to_fetch,
            remains_to_patch,
            seq_tree,
        )

    def patch(self) -> FSM:
        if self.n_tree == 0:
            return self.new()
        return self.add()


class Rebuild:
    @classmethod
    def looper(cls, fsm: FSM) -> FSM:
        fsm_ = fsm
        while True:
            if fsm_.state == State.DONE:
                return fsm_
            if fsm_.state == State.FETCHING:
                fsm_ = fsm_.fetch()
            if fsm_.state == State.PATCHING:
                fsm_ = fsm_.patch()

    def solution(self, seq):
        fsm = FSM(None, 0, seq, (), ())
        return self.looper(fsm).base


if __name__ == '__main__':
    ipt_1 = (5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1)
    ipt_2 = (4, 9, 0, 5, 1)

    rb = Rebuild()
    print(rb.solution(ipt_1))
    print(rb.solution(ipt_2))
