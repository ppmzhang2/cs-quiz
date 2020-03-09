# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple, NamedTuple, Any, Optional, Generator
from itertools import chain

from adt.cons import Cons
from adt.tree import Tree


class Zipper(NamedTuple):
    material: Any
    upper: Zipper


class TreeZipper(Zipper):
    def __new__(cls,
                upper_node: Any,
                left_siblings=(),
                right_siblings=(),
                upper: TreeZipper = ()):
        material: Tuple = tuple((upper_node, left_siblings, right_siblings))
        self = super().__new__(cls, material=material, upper=upper)
        self.upper_node = upper_node
        self.left_siblings = left_siblings
        self.right_siblings = right_siblings
        return self


class ZipperTree(NamedTuple):
    tree: Tree
    zipper: TreeZipper = TreeZipper(upper_node=None,
                                    left_siblings=(),
                                    right_siblings=(),
                                    upper=())

    @property
    def top_most(self) -> bool:
        return self.zipper == TreeZipper(upper_node=None,
                                         left_siblings=(),
                                         right_siblings=(),
                                         upper=())

    @property
    def left_most(self) -> bool:
        return self.zipper.left_siblings == ()

    @property
    def right_most(self) -> bool:
        return self.zipper.right_siblings == ()

    @property
    def bottom_most(self) -> bool:
        return self.tree.children == ()

    def go_up(self) -> ZipperTree:
        if self.top_most:
            return self
        else:
            children = self.zipper.left_siblings + (
                self.tree, ) + self.zipper.right_siblings
            return (type(self))(tree=Tree(node=self.zipper.upper_node,
                                          children=children),
                                zipper=self.zipper.upper)

    def go_down(self, left=True) -> ZipperTree:
        if self.bottom_most:
            return self
        else:
            if left:
                tr = self.tree.children[0]
                left_sibling = ()
                right_sibling = self.tree.children[1:]
            else:
                tr = self.tree.children[-1]
                left_sibling = self.tree.children[:-1]
                right_sibling = ()
            return (type(self))(tree=tr,
                                zipper=TreeZipper(upper_node=self.tree.node,
                                                  left_siblings=left_sibling,
                                                  right_siblings=right_sibling,
                                                  upper=self.zipper))

    def go_left(self) -> ZipperTree:
        if self.left_most:
            return self
        else:
            tr = self.zipper.left_siblings[-1]
            left_siblings = self.zipper.left_siblings[:-1]
            right_siblings = (self.tree, ) + self.zipper.right_siblings
            return (type(self))(tree=tr,
                                zipper=TreeZipper(
                                    upper_node=self.zipper.upper_node,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings,
                                    upper=self.zipper.upper))

    def go_right(self) -> ZipperTree:
        if self.right_most:
            return self
        else:
            tr = self.zipper.right_siblings[0]
            left_siblings = self.zipper.left_siblings + (self.tree, )
            right_siblings = self.zipper.right_siblings[1:]
            return (type(self))(tree=tr,
                                zipper=TreeZipper(
                                    upper_node=self.zipper.upper_node,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings,
                                    upper=self.zipper.upper))

    def go_top(self) -> ZipperTree:
        if self.top_most:
            return self
        else:
            return self.go_up().go_top()

    def go_bottom(self, left=True) -> ZipperTree:
        if self.bottom_most and ((left and self.left_most) or
                                 (not left and self.right_most)):
            return self
        else:
            return self.go_down(left=left).go_bottom(left=left)

    def go_bottomleft(self) -> ZipperTree:
        return self.go_top().go_bottom(left=True)

    def go_bottomright(self) -> ZipperTree:
        return self.go_top().go_bottom(left=False)

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
        tr = self.go_top()
        bottomright = tr.go_bottomright()
        while True:
            yield tr
            if tr == bottomright:
                break
            elif tr.bottom_most and tr.right_most:
                while True:
                    tr = tr.go_up()
                    if not tr.right_most:
                        tr = tr.go_right()
                        break
            elif tr.bottom_most and not tr.right_most:
                tr = tr.go_right()
            else:
                tr = tr.go_down(left=True)

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
        top = tr.go_top()
        while True:
            yield tr
            if tr == top:
                break
            elif tr.right_most:
                tr = tr.go_up()
            elif tr.bottom_most:
                tr = tr.go_right()
            else:
                tr = tr.go_right().go_bottom(left=True)

    def child_iter(self) -> Generator[Optional[ZipperTree], ...]:
        """iterate over its children

        :return:
        """
        if self.bottom_most:
            yield
        else:
            tr = self.go_down(left=True)
            while True:
                yield tr
                if tr.right_most:
                    break
                else:
                    tr = tr.go_right()

    @staticmethod
    def __mul_child_iter(itr: Generator[Optional[ZipperTree], ...]
                         ) -> Generator[Optional[ZipperTree], ...]:
        return filter(lambda x: x is not None,
                      chain(*(zt.child_iter() for zt in itr)))

    def bfs(self) -> Generator[Optional[ZipperTree], ...]:
        def helper(tp: Tuple[Optional[ZipperTree], ...],
                   rec: Generator[Optional[ZipperTree], ...]):
            tp_ = tuple(ZipperTree.__mul_child_iter(iter(tp)))
            if not tp_:
                return rec
            else:
                return helper(tp_, chain(rec, tp_))

        return helper((self, ), iter((self, )))


class ConsZipper(Zipper):
    def __new__(cls, material: Any = None, upper: ConsZipper = None):
        self = super().__new__(cls, material=material, upper=upper)
        return self


class ZipperCons(NamedTuple):
    cons: Cons
    zipper: ConsZipper
    index: int = 0

    @classmethod
    def from_cons(cls, cons: Cons):
        return cls(cons=cons,
                   zipper=ConsZipper(material=None, upper=None),
                   index=0)

    @property
    def left_most(self):
        if self.index == 0:
            return True
        else:
            return False

    @property
    def right_most(self):
        if self.cons.cdr is None:
            return True
        else:
            return False

    def go_right(self):
        if self.right_most:
            return self
        else:
            return type(self)(cons=self.cons.cdr,
                              zipper=ConsZipper(material=self.cons.car,
                                                upper=self.zipper),
                              index=self.index + 1)

    def go_left(self):
        if self.left_most:
            return self
        else:
            return type(self)(cons=Cons(car=self.zipper.material,
                                        cdr=self.cons),
                              zipper=self.zipper.upper,
                              index=self.index - 1)

    def go_right_most(self):
        if self.right_most:
            return self
        else:
            return self.go_right().go_right_most()

    def go_left_most(self):
        if self.left_most:
            return self
        else:
            return self.go_left().go_left_most()

    def __len__(self):
        return self.go_right_most().index + 1
