# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple, NamedTuple, Any, Optional, Generator
from itertools import chain
from adt.tree import Tree


class Context(NamedTuple):
    parent_node: Any
    parent_ctx: Context = ()
    left_siblings: Tuple[Optional[Tree], ...] = ()
    right_siblings: Tuple[Optional[Tree], ...] = ()


class ZTree(NamedTuple):
    tree: Tree
    context: Context = Context(parent_node=None,
                               parent_ctx=(),
                               left_siblings=(),
                               right_siblings=())

    @property
    def top_most(self) -> bool:
        return self.context == Context(parent_node=None,
                                       parent_ctx=(),
                                       left_siblings=(),
                                       right_siblings=())

    @property
    def left_most(self) -> bool:
        return self.context.left_siblings == ()

    @property
    def right_most(self) -> bool:
        return self.context.right_siblings == ()

    @property
    def bottom_most(self) -> bool:
        return self.tree.children == ()

    def go_up(self) -> ZTree:
        if self.top_most:
            return self
        else:
            children = self.context.left_siblings + (
                self.tree, ) + self.context.right_siblings
            return (type(self))(tree=Tree(node=self.context.parent_node,
                                          children=children),
                                context=self.context.parent_ctx)

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
                                context=Context(parent_node=self.tree.node,
                                                parent_ctx=self.context,
                                                left_siblings=left_sibling,
                                                right_siblings=right_sibling))

    def go_left(self) -> ZTree:
        if self.left_most:
            return self
        else:
            tr = self.context.left_siblings[-1]
            left_siblings = self.context.left_siblings[:-1]
            right_siblings = (self.tree, ) + self.context.right_siblings
            return (type(self))(tree=tr,
                                context=Context(
                                    parent_node=self.context.parent_node,
                                    parent_ctx=self.context.parent_ctx,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings))

    def go_right(self) -> ZTree:
        if self.right_most:
            return self
        else:
            tr = self.context.right_siblings[0]
            left_siblings = self.context.left_siblings + (self.tree, )
            right_siblings = self.context.right_siblings[1:]
            return (type(self))(tree=tr,
                                context=Context(
                                    parent_node=self.context.parent_node,
                                    parent_ctx=self.context.parent_ctx,
                                    left_siblings=left_siblings,
                                    right_siblings=right_siblings))

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
