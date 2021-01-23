from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import Callable, Sequence, Tuple, TypeVar

from adt.stack import Stack

T = TypeVar('T')


class BaseTree:
    """
    base class of a tree
    """
    @property
    def root(self):
        raise NotImplementedError

    @property
    def subtrees(self):
        raise NotImplementedError

    @property
    def is_leaf(self) -> bool:
        return len(self.subtrees) == 0

    @classmethod
    def _dfs_helper(
        cls,
        stack: Stack,
        acc: Tuple[T, ...],
        cb: Callable[[BaseTree], Sequence[BaseTree]],
    ) -> Tuple[T, ...]:
        """depth-first search helper
        depth-first search is like manipulating a stack: get a tree in a stack,
        then pop it out and push into the stack its node value and its children
        (the order is depending on whether this is a pre-order or post-order
        search). Repeat this step until the stack is empty

        :param stack: stack to keep the tree
        :param acc: sequence of the search result
        :param cb: callback function to arrange the node and the children of
          the tree popped out
        """
        while True:
            if stack.empty():
                break

            tree = stack.pop()
            if tree.is_leaf:
                acc = acc + (tree.root, )
            else:
                items = cb(tree)
                for child in items:
                    stack.push(child)

        return acc

    @staticmethod
    def _bfs(tp: Tuple[BaseTree, ...]) -> Tuple[BaseTree, ...]:
        return reduce(
            lambda x, y: x + tuple(
                filter(lambda tr: tr is not None, y.subtrees)), tp, ())

    def bfs(self) -> Tuple[T, ...]:
        """Breadth-first search

        :return:
        """
        def helper(
            tp: Tuple[BaseTree, ...],
            rec: Tuple[T, ...],
        ) -> Tuple[T, ...]:
            if not tp:
                return rec
            rec_ = rec + tuple(i.root for i in tp)
            return helper(type(self)._bfs(tp), rec_)

        return helper((self, ), ())

    def dfs_pre(self) -> Tuple[T, ...]:
        def callback(tree: Tree):
            return chain(reversed(tree.subtrees),
                         (type(self)(node=tree.root), ))

        return self._dfs_helper(Stack((self, )), (), callback)

    def dfs_post(self) -> Tuple[T, ...]:
        def callback(tree: BaseTree):
            return chain((type(self)(node=tree.root), ),
                         reversed(tree.subtrees))

        return self._dfs_helper(Stack((self, )), (), callback)

    def depth(self) -> int:
        """check binary tree depth with depth-first search

        :return: tree depth
        """
        def helper(tp: Tuple[BaseTree, ...], rec: int) -> int:
            if not tp:
                return rec
            return helper(type(self)._bfs(tp), rec + 1)

        return helper((self, ), 0)

    def _str(self, indent: int) -> str:
        if self.is_leaf:
            return '- ' * indent + self.root.__str__() + ' (leaf)'
        return '- ' * indent + self.root.__str__() + '\n' + '\n'.join(
            map(lambda s: type(self)._str(s, indent + 1), self.subtrees))

    def __str__(self):
        return self._str(0)

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class Tree(BaseTree):
    node: T
    children: Tuple[Tree, ...] = ()

    @property
    def root(self) -> T:
        return self.node

    @property
    def subtrees(self) -> Tuple[Tree, ...]:
        return self.children

    def __str__(self):
        return 'tree:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class BTree(BaseTree):
    """
    Immutable Binary Tree
    """
    node: T
    left: BTree = None
    right: BTree = None

    @property
    def root(self) -> T:
        return self.node

    @property
    def subtrees(self) -> Tuple[BTree, ...]:
        return tuple(filter(lambda x: x is not None, (self.left, self.right)))

    def dfs_in(self) -> Tuple[T, ...]:
        def callback(tree: BTree):
            return filter(lambda t: t is not None,
                          (tree.right, type(self)(node=tree.node), tree.left))

        return self._dfs_helper(Stack((self, )), (), callback)

    def __str__(self):
        return 'binary tree:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()
