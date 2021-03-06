"""Binary Tree Inorder Traversal
TAG: hash-table, stack

Given the root of a binary tree, return the in-order traversal of its nodes'
values.

Example 1:
    1
     \
      2
     /
    3
Input: root = [1,null,2,3]
Output: [1,3,2]

Example 2:
Input: root = []
Output: []

Example 3:
Input: root = [1]
Output: [1]

Example 4:
    1
   /
  2
Input: root = [1,2]
Output: [2,1]

Example 5:
    1
     \
      2
Input: root = [1,null,2]
Output: [1,2]

Constraints:
* The number of nodes in the tree is in the range [0, 100].
* -100 <= Node.val <= 100
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Tuple, TypeVar

T = TypeVar('T')


@dataclass
class BinaryTree:
    root: T
    left: Optional[BinaryTree] = None
    right: Optional[BinaryTree] = None

    @property
    def is_leaf(self):
        return not self.left and not self.right

    @classmethod
    def dfs_helper(
        cls,
        inputs: Sequence[BinaryTree],
        outputs: Optional[Optional[T]],
        explode: Callable[[BinaryTree], Sequence[BinaryTree]],
    ) -> Tuple[Optional[T]]:
        if not inputs:
            return outputs
        bt = inputs[0]
        if not bt:
            return cls.dfs_helper(inputs[1:], (*outputs, bt), explode)
        if bt.is_leaf:
            return cls.dfs_helper(inputs[1:], (*outputs, bt.root), explode)
        return cls.dfs_helper((*explode(bt), *inputs[1:]), outputs, explode)

    def _in_order_explode(self) -> Tuple[Optional[T]]:
        assert not self.is_leaf
        return (self.left, type(self)(self.root, None, None), self.right)

    def in_order_traversal(self):
        return self.dfs_helper((self, ), (), type(self)._in_order_explode)

    def _pre_order_explode(self) -> Tuple[Optional[T]]:
        assert not self.is_leaf
        return (type(self)(self.root, None, None), self.left, self.right)

    def pre_order_traversal(self):
        return self.dfs_helper((self, ), (), type(self)._pre_order_explode)

    def solution(self) -> Tuple[T]:
        return tuple(filter(lambda x: x is not None,
                            self.in_order_traversal()))


if __name__ == '__main__':
    ipt_1 = BinaryTree(
        1,
        None,
        BinaryTree(2, BinaryTree(3), None),
    )
    exp_1 = (1, 3, 2)
    ipt_2 = BinaryTree(None, None, None)
    exp_2 = ()
    ipt_3 = BinaryTree(1, None, None)
    exp_3 = (1, )
    ipt_4 = BinaryTree(1, BinaryTree(2), None)
    exp_4 = (2, 1)
    ipt_5 = BinaryTree(1, None, BinaryTree(2))
    exp_5 = (1, 2)

    assert ipt_1.solution() == exp_1
    assert ipt_2.solution() == exp_2
    assert ipt_3.solution() == exp_3
    assert ipt_4.solution() == exp_4
    assert ipt_5.solution() == exp_5
