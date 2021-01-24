from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import Generator, Optional, Tuple, TypeVar

from adt.cons import Cons
from adt.tree import Tree

T = TypeVar('T')


@dataclass(frozen=True)
class BaseContext:
    pass


@dataclass(frozen=True)
class ConsContext(BaseContext):
    node: T


@dataclass(frozen=True)
class TreeContext(BaseContext):
    root: T
    left: Tuple[Tree, ...]
    right: Tuple[Tree, ...]

    def __str__(self):
        left_str = '\n'.join(map(repr, self.left))
        right_str = '\n'.join(map(repr, self.right))
        return '\n'.join((
            f'root: {repr(self.root)}',
            f'left: {left_str}',
            f'right: {right_str}',
        ))

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class BaseContexts:
    rec: BaseContexts

    @property
    def context(self):
        raise NotImplementedError

    @property
    def depth(self):
        def helper(rec, acc):
            if not rec:
                return acc
            return helper(rec.rec, acc + 1)

        if not self:
            return 0
        return helper(self.rec, 1)

    def _str(self):
        if not self:
            return repr(self)
        return repr(self.context) + '\n->\n' + type(self)._str(self.rec)

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class ConsContexts(BaseContexts, ConsContext):
    rec: ConsContexts = None

    @property
    def context(self):
        return ConsContext(self.node)

    def __str__(self):
        return 'Cons contexts:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class TreeContexts(BaseContexts, TreeContext):
    rec: TreeContexts = None

    @property
    def context(self):
        return TreeContext(self.root, self.left, self.right)

    def __str__(self):
        return 'Tree contexts:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()


class BaseZipper:
    @property
    def _body(self):
        raise NotImplementedError

    @property
    def _contexts(self) -> BaseContexts:
        raise NotImplementedError

    @property
    def depth(self) -> int:
        return self._contexts.depth

    @property
    def top(self) -> bool:
        return self._contexts is None

    @property
    def bottom(self) -> bool:
        raise NotImplementedError

    def go_up(self):
        raise NotImplementedError

    def go_down(self):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join((
            f'body: {repr(self._body)}',
            f'contexts: {repr(self._contexts)}',
        ))


@dataclass(frozen=True)
class ZipperCons(BaseZipper):
    cons: Cons
    contexts: ConsContexts

    @property
    def _body(self) -> Cons:
        return self.cons

    @property
    def _contexts(self) -> ConsContexts:
        return self.contexts

    @property
    def bottom(self):
        if not self.cons.cdr:
            return True
        return False

    @classmethod
    def from_cons(cls, cons: Cons):
        return cls(cons=cons, contexts=None)

    def go_up(self) -> ZipperCons:
        if self.top:
            return self
        return type(self)(
            type(self.cons)(self.contexts.node, self.cons),
            self.contexts.rec,
        )

    def go_down(self) -> ZipperCons:
        if self.bottom:
            return self
        return type(self)(
            self.cons.cdr,
            ConsContexts(self.cons.car, self.contexts),
        )

    def go_up_most(self) -> ZipperCons:
        if self.top:
            return self
        return self.go_up().go_up_most()

    def go_down_most(self) -> ZipperCons:
        if self.bottom:
            return self
        return self.go_down().go_down_most()

    def __len__(self):
        return self.go_down_most().depth + 1

    def get_item_int(self, item: int, reverse=False):
        if item == 0:
            return self.cons.car
        if item < 0 and not reverse:
            return self.go_down_most().get_item_int(item + 1, True)
        if item > 0 and not reverse:
            if item == 0:
                return self.go_up_most().cons.car
            if self.bottom:
                raise IndexError("Index out of range")
            return self.go_down().get_item_int(item - 1)
        if self.bottom:
            raise IndexError("Index out of range")
        return self.go_up().get_item_int(item + 1, reverse)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return type(self.cons).constr(
                (self.get_item_int(i)
                 for i in range(*item.indices(self.__len__()))))
        if isinstance(item, int):
            return self.get_item_int(item)
        raise TypeError("Invalid argument type")

    def __add__(self, other) -> ZipperCons:
        if isinstance(other, ZipperCons):
            left = self.go_down_most()
            right = other.go_up_most()
            return type(self)(
                cons=Cons(car=left.cons.car, cdr=right.cons),
                contexts=left.contexts,
            )
        if isinstance(other, Cons):
            left = self.go_down_most()
            return type(self)(
                cons=Cons(car=left.cons.car, cdr=other),
                contexts=left.contexts,
            )
        raise TypeError("Invalid argument type")


@dataclass(frozen=True)
class ZipperTree(BaseZipper):
    tree: Tree
    contexts: TreeContexts

    @classmethod
    def from_tree(cls, tree: Tree):
        return cls(tree=tree, contexts=None)

    @property
    def _body(self) -> Tree:
        return self.tree

    @property
    def _contexts(self) -> TreeContexts:
        return self.contexts

    def __str__(self):
        return 'Tree with Zipper:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()

    @property
    def bottom(self) -> bool:
        if not self.tree.children:
            return True
        return False

    def go_up(self) -> ZipperTree:
        if self.top:
            return self
        return type(self)(
            type(self.tree)(
                self.contexts.root,
                (
                    *self.contexts.left,
                    self.tree,
                    *self.contexts.right,
                ),
            ),
            self.contexts.rec,
        )

    def go_down(self, idx=0) -> ZipperTree:
        if self.bottom:
            return self
        if idx < 0:
            idx_ = len(self.tree.children) + idx
        else:
            idx_ = idx
        subtree = self.tree.children[idx_]
        return type(self)(
            subtree,
            TreeContexts(
                self.tree.root,
                self.tree.children[:idx_],
                self.tree.children[idx_ + 1:],
                self.contexts,
            ),
        )

    def go_up_most(self) -> ZipperTree:
        if self.top:
            return self
        return self.go_up().go_up_most()

    @property
    def left_most(self) -> bool:
        if not self.contexts:
            return True
        return not self.contexts.left

    @property
    def right_most(self) -> bool:
        if not self.contexts:
            return True
        return not self.contexts.right

    def go_left(self) -> ZipperTree:
        if self.left_most:
            return self
        tr = self.contexts.left[-1]
        left = self.contexts.left[:-1]
        right = (self.tree, *self.contexts.right)
        return (type(self))(tr,
                            TreeContexts(
                                self.contexts.root,
                                left,
                                right,
                                self.contexts.rec,
                            ))

    def go_right(self) -> ZipperTree:
        if self.right_most:
            return self
        tr = self.contexts.right[0]
        left = (*self.contexts.left, self.tree)
        right = self.contexts.right[1:]
        return (type(self))(tr,
                            TreeContexts(
                                self.contexts.root,
                                left,
                                right,
                                self.contexts.rec,
                            ))

    def go_down_most(self, left=True) -> ZipperTree:
        """go local bottom
        """
        if self.bottom and ((left and self.left_most) or
                            (not left and self.right_most)):
            return self
        if self.bottom and left:
            return self.go_left().go_down_most(left=left)
        if self.bottom and not left:
            return self.go_right().go_down_most(left=left)
        if left:
            idx = 0
        else:
            idx = -1
        return self.go_down(idx=idx).go_down_most(left=left)

    def go_bottomleft(self) -> ZipperTree:
        """go global bottom-left
        """
        return self.go_up_most().go_down_most(left=True)

    def go_bottomright(self) -> ZipperTree:
        """go global bottom-right
        """
        return self.go_up_most().go_down_most(left=False)

    def dfs_pre(self) -> Generator[ZipperTree]:
        """pre-order deep first search

        0. start from top
        1. if bottom-right most, all finished
        2. if right most and bottom most (not bottom-right most,
           meaning parent tree finished), repeat until succeed:
           **go for parent's right siblings**
        3. if right most but not bottom most, go down-left
        4. if bottom most but not right most, go for right siblings
        :return: ZTree generator
        """
        tr = self.go_up_most()
        bottomright = tr.go_bottomright()
        while True:
            yield tr
            if tr == bottomright:
                break
            if tr.bottom and tr.right_most:
                while True:
                    # print('up')
                    tr = tr.go_up()
                    if not tr.right_most:
                        tr = tr.go_right()
                        break
            elif tr.bottom and not tr.right_most:
                tr = tr.go_right()
                # print('right')
            else:
                tr = tr.go_down(idx=0)
                # print('down left')

    def dfs_post(self) -> Generator[ZipperTree]:
        """post-order deep first search

        0. start from bottom-left most
        1. if top, all finished
        2. if right most, go up
        3. if bottom most and not right most, go right
        4. if bottom most but not right most, go for right siblings
        5. if not bottom most and not right most:
           go to the bottom-left of its right sibling
        :return: ZTree generator
        """
        tr = self.go_bottomleft()
        top = tr.go_up_most()
        while True:
            yield tr
            if tr == top:
                break
            if tr.right_most:
                tr = tr.go_up()
            elif tr.bottom:
                tr = tr.go_right()
            else:
                tr = tr.go_right().go_down_most(left=True)

    def child_iter(self) -> Generator[Optional[ZipperTree], ...]:
        """iterate over its children

        :return:
        """
        if self.bottom:
            yield
        else:
            tr = self.go_down(idx=0)
            while True:
                yield tr
                if tr.right_most:
                    break
                tr = tr.go_right()

    @staticmethod
    def __mul_child_iter(
        itr: Generator[Optional[ZipperTree], ...]
    ) -> Generator[Optional[ZipperTree], ...]:
        return filter(lambda x: x is not None,
                      chain(*(zt.child_iter() for zt in itr)))

    def bfs(self) -> Generator[Optional[ZipperTree], ...]:
        def helper(tp: Tuple[Optional[ZipperTree], ...],
                   rec: Generator[Optional[ZipperTree], ...]):
            tp_ = tuple(ZipperTree.__mul_child_iter(iter(tp)))
            if not tp_:
                return rec
            return helper(tp_, chain(rec, tp_))

        return helper((self, ), iter((self, )))
