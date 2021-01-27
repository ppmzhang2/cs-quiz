from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generic, Sequence, Tuple, TypeVar

T = TypeVar('T')


class BaseTree(Generic[T]):
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
        stack: Tuple[BaseTree[T], ...],
        acc: Tuple[T, ...],
        cb: Callable[[BaseTree[T]], Sequence[BaseTree[T]]],
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
            if not stack:
                return acc

            tree = stack[0]
            stack = stack[1:]
            if tree.is_leaf:
                acc = (*acc, tree.root)
            else:
                stack = (*cb(tree), *stack)

    @staticmethod
    def _bfs(tp: Tuple[BaseTree[T], ...]) -> Tuple[BaseTree[T], ...]:
        return reduce(
            lambda x, y: x + tuple(
                filter(lambda tr: tr is not None, y.subtrees)), tp, ())

    def bfs(self) -> Tuple[T, ...]:
        """Breadth-first search

        :return:
        """
        def helper(
            tp: Tuple[BaseTree[T], ...],
            rec: Tuple[T, ...],
        ) -> Tuple[T, ...]:
            if not tp:
                return rec
            rec_ = rec + tuple(i.root for i in tp)
            return helper(type(self)._bfs(tp), rec_)

        return helper((self, ), ())

    def dfs_pre(self) -> Tuple[T, ...]:
        def callback(tree: BaseTree[T]) -> Tuple[BaseTree[T], ...]:
            return (type(self)(node=tree.root), *tree.subtrees)

        return self._dfs_helper((self, ), (), callback)

    def dfs_post(self) -> Tuple[T, ...]:
        def callback(tree: BaseTree[T]) -> Tuple[BaseTree[T], ...]:
            return (*tree.subtrees, type(self)(node=tree.root))

        return self._dfs_helper((self, ), (), callback)

    def depth(self) -> int:
        """check binary tree depth with depth-first search

        :return: tree depth
        """
        def helper(tp: Tuple[BaseTree[T], ...], rec: int) -> int:
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
class Tree(BaseTree[T]):
    node: T
    children: Tuple[Tree[T], ...] = ()

    @property
    def root(self) -> T:
        return self.node

    @property
    def subtrees(self) -> Tuple[Tree[T], ...]:
        return self.children

    def __str__(self):
        return 'tree:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class BTree(BaseTree[T]):
    """
    Immutable Binary Tree
    """
    node: T
    left: BTree[T] = None
    right: BTree[T] = None

    @property
    def root(self) -> T:
        return self.node

    @property
    def subtrees(self) -> Tuple[BTree[T], ...]:
        return tuple(filter(lambda x: x is not None, (self.left, self.right)))

    def dfs_in(self) -> Tuple[T, ...]:
        def callback(tree: BTree[T]) -> Tuple[BTree[T], ...]:
            return filter(lambda t: t is not None,
                          (tree.left, type(self)(node=tree.node), tree.right))

        return self._dfs_helper((self, ), (), callback)

    def __str__(self):
        return 'binary tree:\n' + super().__str__()

    def __repr__(self):
        return self.__str__()
