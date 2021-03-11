from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Sequence, Tuple


@unique
class BTreeStruc(IntEnum):
    NULL = 0
    LEAF = 1
    NO_LEFT_SUB = 2
    NO_RIGHT_SUB = 3
    COMPLETE = 4
    MASS = 5


@dataclass(frozen=True)
class BTree:
    root: Optional[int] = None
    pre_seq: Optional[Tuple[Optional[int], ...]] = None
    left: Optional[BTree] = None
    right: Optional[BTree] = None

    @staticmethod
    def split(seq: Sequence[int]) -> Tuple[int, Sequence[int], Sequence[int]]:
        root = seq[0]
        seq_ = seq[1:]
        assert len(seq_) % 2 == 0
        length = len(seq_) // 2

        return root, seq_[:length], seq_[length:]

    @property
    def struc(self) -> BTreeStruc:
        if (not self.root and not self.pre_seq and not self.left
                and not self.right):
            return BTreeStruc.NULL
        if not self.root and not self.left and not self.right:
            return BTreeStruc.MASS
        if not self.left and not self.right:
            return BTreeStruc.LEAF
        if not self.right:
            return BTreeStruc.NO_RIGHT_SUB
        if not self.left:
            return BTreeStruc.NO_LEFT_SUB
        return BTreeStruc.COMPLETE

    def clean(self) -> BTree:
        if self.struc != BTreeStruc.MASS:
            return self
        root, left_pre, right_pre = self.split(self.pre_seq)
        left = None if not left_pre else (type(self))(pre_seq=left_pre)
        right = None if not right_pre else (type(self))(pre_seq=right_pre)
        return (type(self))(root=root, left=left, right=right)


@unique
class Position(IntEnum):
    LEFT_ORPHAN = 1
    RIGHT_ORPHAN = 2
    LEFT = 3
    RIGHT = 4
    TOP = 5


# whether: 1. has sibling, 2. left tree
position_mapping = {
    (True, True): Position.LEFT,
    (False, True): Position.LEFT_ORPHAN,
    (True, False): Position.RIGHT,
    (False, False): Position.RIGHT_ORPHAN,
}


@dataclass(frozen=True)
class Contexts:
    left: bool
    root: int
    tree: Optional[BTree]
    rec: Optional[Contexts]

    @property
    def position(self) -> Position:
        try:
            return position_mapping[(bool(self.tree), self.left)]
        except KeyError as exc:
            raise ValueError('invalid contexts') from exc


@unique
class State(IntEnum):
    MASS = 0
    L_ORPHAN_LEAF = 1
    R_ORPHAN_LEAF = 2
    L_BRANCH_LEAF = 3
    R_BRANCH_LEAF = 4
    TOP_LEAF = 5
    L_ORPHAN_COMPLETE = 6
    R_ORPHAN_COMPLETE = 7
    L_BRANCH_COMPLETE = 8
    R_BRANCH_COMPLETE = 9
    TOP_COMPLETE = 10
    L_ORPHAN_NORIGHT = 11
    R_ORPHAN_NORIGHT = 12
    L_BRANCH_NORIGHT = 13
    R_BRANCH_NORIGHT = 14
    TOP_NORIGHT = 15
    L_ORPHAN_NOLEFT = 16
    R_ORPHAN_NOLEFT = 17
    L_BRANCH_NOLEFT = 18
    R_BRANCH_NOLEFT = 19
    TOP_NOLEFT = 20
    NULLABLE = 21
    NULL = 22


zipper_state_mapping = {
    (BTreeStruc.LEAF, Position.LEFT_ORPHAN): State.L_ORPHAN_LEAF,
    (BTreeStruc.LEAF, Position.RIGHT_ORPHAN): State.R_ORPHAN_LEAF,
    (BTreeStruc.LEAF, Position.LEFT): State.L_BRANCH_LEAF,
    (BTreeStruc.LEAF, Position.RIGHT): State.R_BRANCH_LEAF,
    (BTreeStruc.COMPLETE, Position.LEFT_ORPHAN): State.L_ORPHAN_COMPLETE,
    (BTreeStruc.COMPLETE, Position.RIGHT_ORPHAN): State.R_ORPHAN_COMPLETE,
    (BTreeStruc.COMPLETE, Position.LEFT): State.L_BRANCH_COMPLETE,
    (BTreeStruc.COMPLETE, Position.RIGHT): State.R_BRANCH_COMPLETE,
    (BTreeStruc.NO_RIGHT_SUB, Position.LEFT_ORPHAN): State.L_ORPHAN_NORIGHT,
    (BTreeStruc.NO_RIGHT_SUB, Position.RIGHT_ORPHAN): State.R_ORPHAN_NORIGHT,
    (BTreeStruc.NO_RIGHT_SUB, Position.LEFT): State.L_BRANCH_NORIGHT,
    (BTreeStruc.NO_RIGHT_SUB, Position.RIGHT): State.R_BRANCH_NORIGHT,
    (BTreeStruc.NO_LEFT_SUB, Position.LEFT_ORPHAN): State.L_ORPHAN_NOLEFT,
    (BTreeStruc.NO_LEFT_SUB, Position.RIGHT_ORPHAN): State.R_ORPHAN_NOLEFT,
    (BTreeStruc.NO_LEFT_SUB, Position.LEFT): State.L_BRANCH_NOLEFT,
    (BTreeStruc.NO_LEFT_SUB, Position.RIGHT): State.R_BRANCH_NOLEFT,
    (BTreeStruc.LEAF, Position.TOP): State.TOP_LEAF,
    (BTreeStruc.NO_RIGHT_SUB, Position.TOP): State.TOP_NORIGHT,
    (BTreeStruc.NO_LEFT_SUB, Position.TOP): State.TOP_NOLEFT,
    (BTreeStruc.COMPLETE, Position.TOP): State.TOP_COMPLETE,
}

_top = {
    State.TOP_LEAF,
    State.TOP_NORIGHT,
    State.TOP_NOLEFT,
    State.TOP_COMPLETE,
}.__contains__

_is_lhs = {
    State.L_BRANCH_LEAF,
    State.L_BRANCH_NORIGHT,
    State.L_BRANCH_NOLEFT,
    State.L_BRANCH_COMPLETE,
    State.L_ORPHAN_LEAF,
    State.L_ORPHAN_NORIGHT,
    State.L_ORPHAN_NOLEFT,
    State.L_ORPHAN_COMPLETE,
}.__contains__

_is_rhs = {
    State.R_BRANCH_LEAF,
    State.R_BRANCH_NORIGHT,
    State.R_BRANCH_NOLEFT,
    State.R_BRANCH_COMPLETE,
    State.R_ORPHAN_LEAF,
    State.R_ORPHAN_NORIGHT,
    State.R_ORPHAN_NOLEFT,
    State.R_ORPHAN_COMPLETE,
}.__contains__

_has_left_subtree = {
    State.TOP_COMPLETE,
    State.L_BRANCH_COMPLETE,
    State.R_BRANCH_COMPLETE,
    State.L_ORPHAN_COMPLETE,
    State.R_ORPHAN_COMPLETE,
    State.TOP_NORIGHT,
    State.L_BRANCH_NORIGHT,
    State.R_BRANCH_NORIGHT,
    State.L_ORPHAN_NORIGHT,
    State.R_ORPHAN_NORIGHT,
}.__contains__

_has_right_subtree = {
    State.TOP_COMPLETE,
    State.L_BRANCH_COMPLETE,
    State.R_BRANCH_COMPLETE,
    State.L_ORPHAN_COMPLETE,
    State.R_ORPHAN_COMPLETE,
    State.TOP_NOLEFT,
    State.L_BRANCH_NOLEFT,
    State.R_BRANCH_NOLEFT,
    State.L_ORPHAN_NOLEFT,
    State.R_ORPHAN_NOLEFT,
}.__contains__

_orphan = {
    State.L_ORPHAN_LEAF,
    State.L_ORPHAN_NORIGHT,
    State.L_ORPHAN_NOLEFT,
    State.L_ORPHAN_COMPLETE,
    State.R_ORPHAN_LEAF,
    State.R_ORPHAN_NORIGHT,
    State.R_ORPHAN_NOLEFT,
    State.R_ORPHAN_COMPLETE,
}.__contains__


@dataclass(frozen=True)
class Zipper:
    btree: Optional[BTree]
    contexts: Optional[Contexts]

    @classmethod
    def from_btree(cls, btree: BTree) -> Zipper:
        return cls(btree, None)

    @property
    def state(self) -> State:
        if not self.btree:
            return State.NULL
        if self.btree.struc == BTreeStruc.NULL:
            return State.NULLABLE
        if self.btree.struc == BTreeStruc.MASS:
            return State.MASS

        if not self.contexts:
            position = Position.TOP
        else:
            position = self.contexts.position
        try:
            return zipper_state_mapping[(self.btree.struc, position)]
        except KeyError as exc:
            raise ValueError('invalid zipper') from exc

    def clean(self) -> Zipper:
        if self.state == State.NULLABLE:
            return (type(self))(None, self.contexts)
        if self.state == State.NULL:
            return self.go_up()
        if self.state == State.MASS:
            return (type(self))(self.btree.clean(), self.contexts)
        return self

    @property
    def top(self) -> bool:
        return _top(self.state)

    @property
    def lhs(self) -> bool:
        return _is_lhs(self.state)

    @property
    def rhs(self) -> bool:
        return _is_rhs(self.state)

    @property
    def has_left_subtree(self) -> bool:
        return _has_left_subtree(self.state)

    @property
    def has_right_subtree(self) -> bool:
        return _has_right_subtree(self.state)

    @property
    def orphan(self) -> bool:
        return _orphan(self.state)

    def go_up(self) -> Zipper:
        assert self.state != State.MASS

        if self.top:
            return self
        if self.lhs:
            btree = BTree(
                root=self.contexts.root,
                left=self.btree,
                right=self.contexts.tree,
            )
        else:
            btree = BTree(
                root=self.contexts.root,
                left=self.contexts.tree,
                right=self.btree,
            )
        return (type(self))(btree, self.contexts.rec)

    def go_down_left(self) -> Zipper:
        assert self.state != State.MASS

        if not self.has_left_subtree:
            return self

        btree = self.btree.left
        root = self.btree.root
        sibling = self.btree.right
        return (type(self))(
            btree,
            Contexts(True, root, sibling, self.contexts),
        )

    def go_down_right(self) -> Zipper:
        assert self.state != State.MASS

        if not self.has_right_subtree:
            return self

        btree = self.btree.right
        root = self.btree.root
        sibling = self.btree.left
        return (type(self))(
            btree,
            Contexts(True, root, sibling, self.contexts),
        )

    def go_right(self) -> Zipper:
        assert self.state != State.MASS

        if self.top or self.orphan:
            return self
        return (type(self))(
            self.contexts.tree,
            Contexts(False, self.contexts.root, self.btree, self.contexts.rec),
        )


@unique
class Action(IntEnum):
    CLEAN = 0
    UP = 1
    DOWN_LEFT = 2
    DOWN_RIGHT = 3
    RIGHT = 4


@dataclass(frozen=True)
class FSM:
    zipper: Zipper
    actions: Tuple[Action, ...]

    @property
    def last_action(self) -> Action:
        if not self.actions:
            return None
        return self.actions[-1]

    @property
    def finished(self) -> bool:
        if self.zipper.top and self.last_action == Action.UP:
            return True
        return False

    def transform(self):
        assert not self.finished

        # unclean zipper
        if self.zipper.state in (State.MASS, State.NULLABLE, State.NULL):
            return (type(self))(
                self.zipper.clean(),
                (*self.actions, Action.CLEAN),
            )
        # cases to go up
        if self.zipper.state in (
                State.L_ORPHAN_LEAF,
                State.R_BRANCH_LEAF,
                State.R_ORPHAN_LEAF,
        ):
            return (type(self))(
                self.zipper.go_up(),
                (*self.actions, Action.UP),
            )
        if self.zipper.state in (
                State.L_ORPHAN_NORIGHT,
                State.L_ORPHAN_NOLEFT,
                State.L_ORPHAN_COMPLETE,
                State.R_BRANCH_NORIGHT,
                State.R_BRANCH_NOLEFT,
                State.R_BRANCH_COMPLETE,
                State.R_ORPHAN_NORIGHT,
                State.R_ORPHAN_NOLEFT,
                State.R_ORPHAN_COMPLETE,
        ) and self.last_action == Action.UP:
            return (type(self))(
                self.zipper.go_up(),
                (*self.actions, Action.UP),
            )
        # cases to go right
        if self.zipper.state == State.L_BRANCH_LEAF:
            return (type(self))(
                self.zipper.go_right(),
                (*self.actions, Action.RIGHT),
            )
        if self.zipper.state in (
                State.L_BRANCH_NORIGHT,
                State.L_BRANCH_NOLEFT,
                State.L_BRANCH_COMPLETE,
        ) and self.last_action == Action.UP:
            return (type(self))(
                self.zipper.go_right(),
                (*self.actions, Action.RIGHT),
            )
        # go down-left otherwise
        return (type(self))(
            self.zipper.go_down_left(),
            (*self.actions, Action.DOWN_LEFT),
        )


class ValidateBinarySearchTree:
    @classmethod
    def looper(cls, fsm: FSM) -> FSM:
        if fsm.finished:
            return fsm
        return cls.looper(fsm.transform())

    def solution(self, seq: Tuple[int, ...]):
        bt = BTree(pre_seq=seq)
        zipper = Zipper.from_btree(bt)
        fsm = FSM(zipper, ())
        return self.looper(fsm).zipper


if __name__ == '__main__':
    ipt_1 = (2, 1, 3)
    ipt_2 = (5, 1, None, None, 4, 3, 6)

    vbst = ValidateBinarySearchTree()
    print(vbst.solution(ipt_1))
    print(vbst.solution(ipt_2))
