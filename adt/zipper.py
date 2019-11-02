# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple, NamedTuple, Any, Optional, Generator
from itertools import chain
from adt.tree import Tree


class Zipper(NamedTuple):
    matl: Any
    upper: Zipper


class TreeZp(Zipper):
    def __new__(cls,
                upper_node: Any,
                left_siblings=(),
                right_siblings=(),
                upper: TreeZp = ()):
        matl: Tuple = tuple((upper_node, left_siblings, right_siblings))
        self = super().__new__(cls, matl=matl, upper=upper)
        self.upper_node = upper_node
        self.left_siblings = left_siblings
        self.right_siblings = right_siblings
        return self


class ZTree(NamedTuple):
    tree: Tree
    zipper: TreeZp = TreeZp(upper_node=None,
                            left_siblings=(),
                            right_siblings=(),
                            upper=())

    @property
    def top_most(self) -> bool:
        return self.zipper == TreeZp(upper_node=None,
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

    def go_up(self) -> ZTree:
        if self.top_most:
            return self
        else:
            children = self.zipper.left_siblings + (
                self.tree, ) + self.zipper.right_siblings
            return (type(self))(tree=Tree(node=self.zipper.upper_node,
                                          children=children),
                                zipper=self.zipper.upper)

    def go_down(self, left=True) -> ZTree:
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
                                zipper=TreeZp(upper_node=self.tree.node,
                                              left_siblings=left_sibling,
                                              right_siblings=right_sibling,
                                              upper=self.zipper))

    def go_left(self) -> ZTree:
        if self.left_most:
            return self
        else:
            tr = self.zipper.left_siblings[-1]
            left_siblings = self.zipper.left_siblings[:-1]
            right_siblings = (self.tree, ) + self.zipper.right_siblings
            return (type(self))(tree=tr,
                                zipper=TreeZp(
                                    upper_node=self.zipper.upper_node,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings,
                                    upper=self.zipper.upper))

    def go_right(self) -> ZTree:
        if self.right_most:
            return self
        else:
            tr = self.zipper.right_siblings[0]
            left_siblings = self.zipper.left_siblings + (self.tree, )
            right_siblings = self.zipper.right_siblings[1:]
            return (type(self))(tree=tr,
                                zipper=TreeZp(
                                    upper_node=self.zipper.upper_node,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings,
                                    upper=self.zipper.upper))

    def go_top(self) -> ZTree:
        if self.top_most:
            return self
        else:
            return self.go_up().go_top()

    def go_bottom(self, left=True) -> ZTree:
        if self.bottom_most and ((left and self.left_most) or
                                 (not left and self.right_most)):
            return self
        else:
            return self.go_down(left=left).go_bottom(left=left)

    def go_bottomleft(self) -> ZTree:
        return self.go_top().go_bottom(left=True)

    def go_bottomright(self) -> ZTree:
        return self.go_top().go_bottom(left=False)

    def dfs_pre(self) -> Generator[ZTree]:
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

    def dfs_post(self) -> Generator[ZTree]:
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

    def child_iter(self) -> Generator[Optional[ZTree], ...]:
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
    def __mul_child_iter(itr: Generator[Optional[ZTree], ...]
                         ) -> Generator[Optional[ZTree], ...]:
        return filter(lambda x: x is not None,
                      chain(*(zt.child_iter() for zt in itr)))

    def bfs(self) -> Generator[Optional[ZTree], ...]:
        def helper(tp: Tuple[Optional[ZTree], ...],
                   rec: Generator[Optional[ZTree], ...]):
            tp_ = tuple(ZTree.__mul_child_iter(iter(tp)))
            if not tp_:
                return rec
            else:
                return helper(tp_, chain(rec, tp_))

        return helper((self, ), iter((self, )))
