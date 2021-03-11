from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple


@unique
class TreeState(IntEnum):
    MASS = 1
    CLEAN = 2


@dataclass(frozen=True)
class BTree:
    root: Optional[int] = None
    left: Optional[BTree] = None
    right: Optional[BTree] = None
    pre_order: Optional[Tuple[int, ...]] = None
    in_order: Optional[Tuple[int, ...]] = None

    @staticmethod
    def to_clean(
        pre_order: Tuple[int, ...],
        in_order: Tuple[int, ...],
    ) -> Tuple[int, Tuple[int, ...], Tuple[int, ...], Tuple[int, ...], Tuple[
            int, ...]]:
        root = pre_order[0]
        pre_order_ = pre_order[1:]
        root_idx = in_order.index(root)
        left_in_order = in_order[:root_idx]
        right_in_order = in_order[root_idx + 1:]
        left_len = len(left_in_order)
        left_pre_order = pre_order_[:left_len]
        right_pre_order = pre_order_[left_len:]
        return (
            root,
            left_pre_order,
            left_in_order,
            right_pre_order,
            right_in_order,
        )

    def clean_tree(self) -> BTree:
        assert self.state == TreeState.MASS
        (root, left_pre_order, left_in_order, right_pre_order,
         right_in_order) = self.to_clean(self.pre_order, self.in_order)
        if not left_pre_order:
            left = None
        else:
            left = (type(self))(pre_order=left_pre_order,
                                in_order=left_in_order)
        if not right_pre_order:
            right = None
        else:
            right = (type(self))(pre_order=right_pre_order,
                                 in_order=right_in_order)
        return (type(self))(root=root, left=left, right=right)

    @property
    def state(self):
        if not self.root:
            return TreeState.MASS
        if not self.pre_order:
            return TreeState.CLEAN

        raise ValueError('invalid input')


@dataclass(frozen=True)
class Contexts:
    left: bool
    root: int
    tree: BTree[int]
    rec: Optional[Contexts]


@dataclass(frozen=True)
class ZipBTree:
    btree: BTree
    contexts: Optional[Contexts]

    @classmethod
    def from_btree(cls, bt: BTree) -> ZipBTree:
        return cls(bt, None)

    def cleaned(self) -> ZipBTree:
        if self.btree.state == TreeState.CLEAN:
            return self
        bt = self.btree.clean_tree()
        return (type(self))(bt, self.contexts)

    @property
    def top(self) -> bool:
        return not self.contexts

    @property
    def left_most(self) -> bool:
        if not self.contexts:
            return True
        return self.contexts.left

    @property
    def right_most(self) -> bool:
        if not self.contexts:
            return True
        return not self.contexts.left

    @property
    def leaf(self) -> bool:
        return not self.btree.left and not self.btree.right

    @property
    def no_sibling(self) -> bool:
        return not self.contexts.tree

    def go_up(self) -> ZipBTree:
        if self.top:
            return self
        if self.contexts.left:
            btree = BTree(self.contexts.root, self.btree, self.contexts.tree)
        else:
            btree = BTree(self.contexts.root, self.contexts.tree, self.btree)
        return (type(self))(btree, self.contexts.rec)

    def go_down_left(self) -> ZipBTree:
        if not self.btree.left:
            return self
        root = self.btree.root
        left = True
        tree = self.btree.right
        return ZipBTree(
            self.btree.left,
            Contexts(left, root, tree, self.contexts),
        )

    def go_down_right(self) -> ZipBTree:
        if not self.btree.right:
            return self
        root = self.btree.root
        left = False
        tree = self.btree.left
        return ZipBTree(
            self.btree.right,
            Contexts(left, root, tree, self.contexts),
        )

    def go_sibling(self) -> ZipBTree:
        if self.no_sibling:
            return self
        left = not self.contexts.left
        return ZipBTree(
            self.contexts.tree,
            Contexts(left, self.contexts.root, self.btree, self.contexts.rec),
        )

    def go_left_clean(self) -> ZipBTree:
        return self.go_down_left().cleaned()

    def go_right_clean(self) -> ZipBTree:
        return self.go_down_right().cleaned()

    def go_sibling_clean(self) -> ZipBTree:
        return self.go_sibling().cleaned()


@unique
class Position(IntEnum):
    TOP = 1
    SINGLE_TREE = 2
    LEFT_TREE = 3
    RIGHT_TREE = 4
    SINGLE_LEAF = 5
    LEFT_LEAF = 6
    RIGHT_LEAF = 7
    OTHER = 8


@unique
class Action(IntEnum):
    UP = 1
    LEFT = 2
    RIGHT = 3
    SIBLING = 4


@unique
class State(IntEnum):
    DOING = 1
    DONE = 2


@dataclass(frozen=True)
class FSM:
    zipper: ZipBTree
    actions: Tuple[Action, ...]

    @property
    def position(self):  # pylint: disable=too-many-return-statements
        if self.zipper.top:
            return Position.TOP
        if self.zipper.leaf and not self.zipper.contexts.tree:
            return Position.SINGLE_LEAF
        if self.zipper.leaf and self.zipper.left_most:
            return Position.LEFT_LEAF
        if self.zipper.leaf and self.zipper.right_most:
            return Position.RIGHT_LEAF
        if not self.zipper.leaf and not self.zipper.contexts.tree:
            return Position.SINGLE_TREE
        if not self.zipper.leaf and self.zipper.left_most:
            return Position.LEFT_TREE
        if not self.zipper.leaf and self.zipper.right_most:
            return Position.RIGHT_TREE

        raise ValueError('invalid value')

    @property
    def last_action(self) -> Action:
        if not self.actions:
            return None
        return self.actions[-1]

    @property
    def state(self) -> State:
        if self.position == Position.TOP and self.last_action == Action.UP:
            return State.DONE
        return State.DOING

    def transform(self) -> FSM:
        '''build tree via pre-order traversal
        '''
        assert self.state == State.DOING
        if self.position in (
                Position.RIGHT_LEAF,
                Position.SINGLE_LEAF,
        ):
            return FSM(
                self.zipper.go_up(),
                (*self.actions, Action.UP),
            )
        if self.position == Position.LEFT_TREE and self.last_action == Action.UP:
            return FSM(
                self.zipper.go_sibling_clean(),
                (*self.actions, Action.SIBLING),
            )
        if self.position in (
                Position.RIGHT_TREE,
                Position.SINGLE_TREE,
        ) and self.last_action == Action.UP:
            return FSM(
                self.zipper.go_up(),
                (*self.actions, Action.UP),
            )
        if self.position == Position.LEFT_LEAF:
            return FSM(
                self.zipper.go_sibling_clean(),
                (*self.actions, Action.SIBLING),
            )
        return FSM(
            self.zipper.go_left_clean(),
            (*self.actions, Action.LEFT),
        )


class PreInOrder:
    @staticmethod
    def solution(
        pre_order: Tuple[int, ...],
        in_order: Tuple[int, ...],
    ) -> BTree:
        bt = BTree(pre_order=pre_order, in_order=in_order)
        zipper = ZipBTree.from_btree(bt)
        fsm = FSM(zipper, ())
        while True:
            if fsm.state == State.DONE:
                return fsm.zipper.btree
            fsm = fsm.transform()


if __name__ == '__main__':
    ipt_1_1 = (3, 9, 20, 15, 7)
    ipt_1_2 = (9, 3, 15, 20, 7)

    ipt_2_1 = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    ipt_2_2 = (4, 3, 2, 1, 6, 5, 8, 7, 9)

    # print(BTree.to_clean(ipt_1_1, ipt_1_2))
    # print(BTree.to_clean((20, 15, 7), (15, 20, 7)))
    # print(BTree.to_clean((1, ), (1, )))

    btree_1 = BTree(pre_order=ipt_1_1, in_order=ipt_1_2)
    zbt_1 = ZipBTree.from_btree(btree_1)

    # print(zbt_1.cleaned())
    # print(zbt_1.cleaned().go_left().cleaned().go_up().go_right().cleaned().
    #       go_up())

    pio = PreInOrder()
    print(pio.solution(ipt_1_1, ipt_1_2))
    print(pio.solution(ipt_2_1, ipt_2_2))
