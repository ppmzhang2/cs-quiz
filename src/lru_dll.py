from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional


@unique
class NodeState(Enum):
    ORPHAN = 0
    HEAD = 1
    TAIL = 2
    MIDDLE = 3


@dataclass
class Node:
    value: Any
    head: Optional[Node] = None
    tail: Optional[Node] = None

    @property
    def state(self) -> NodeState:
        if not self.head and not self.tail:
            return NodeState.ORPHAN
        if not self.head:
            return NodeState.HEAD
        if not self.tail:
            return NodeState.TAIL
        return NodeState.MIDDLE

    @property
    def head_value(self):
        if self.state in (NodeState.ORPHAN, NodeState.HEAD):
            return None
        return self.head.value

    @property
    def tail_value(self):
        if self.state in (NodeState.ORPHAN, NodeState.TAIL):
            return None
        return self.tail.value

    def __repr__(self):
        return '%s <-> %s <-> %s' % (
            self.head_value,
            self.value,
            self.tail_value,
        )

    def __str__(self):
        return self.__repr__()


class DoublyLinkedList:
    def __init__(self):
        self._pervyy: Optional[Node] = None
        self._posledniy: Optional[Node] = None
        self.count = 0

    def __iter__(self):
        node = self._pervyy
        while True:
            if not node:
                break
            yield node
            node = node.tail

    def __repr__(self):
        return ' <==> '.join((str(i) for i in self))

    def __str__(self):
        return self.__repr__()

    def _init(self, value) -> Node:
        new_node = Node(value)
        self._pervyy = new_node
        self._posledniy = new_node
        return self._pervyy

    def _add_to_head(self, value) -> Node:
        old_head = self._pervyy
        new_head = Node(value)
        old_head.head, new_head.tail = new_head, old_head
        self._pervyy = new_head
        return self._pervyy

    def _add_to_tail(self, value) -> Node:
        old_tail = self._posledniy
        new_tail = Node(value)
        old_tail.tail, new_tail.head = new_tail, old_tail
        self._posledniy = new_tail
        return self._posledniy

    def append(self, value, last=False) -> Node:
        if self.count == 0:
            node = self._init(value)
        elif last:
            node = self._add_to_tail(value)
        else:
            node = self._add_to_head(value)
        self.count += 1
        return node

    def _pop_orphan(self):
        value = self._pervyy.value
        self._pervyy = None
        self._posledniy = None
        return value

    def _pop_head(self):
        old_head = self._pervyy
        new_head = old_head.tail
        new_head.head = None
        self._pervyy = new_head
        return old_head.value

    def _pop_tail(self):
        old_tail = self._posledniy
        new_tail = old_tail.head
        new_tail.tail = None
        self._posledniy = new_tail
        return old_tail.value

    def pop(self, last=False):
        if self.count == 0:
            raise IndexError('cannot pop empty list')
        if self.count == 1:
            value = self._pop_orphan()
        elif last:
            value = self._pop_tail()
        else:
            value = self._pop_head()
        self.count -= 1
        return value


class LRUCache:
    def __init__(self, limit: int):
        self._limit = limit
        self._dict = {}
        self._cache = DoublyLinkedList()

    def set(self, key, value):
        self._dict[key] = self._cache.append(value)
        if self._cache.count > self._limit:
            self._cache.pop(last=True)

    def get(self, key):
        node = self._dict.get(key)
        if node is None:
            return None
        if node.state in (NodeState.HEAD, NodeState.ORPHAN):
            return node.value
        if node.state == NodeState.TAIL:
            self._cache.pop(last=True)
        else:
            head = node.head
            tail = node.tail
            head.tail, tail.head = tail, head
        self._cache.count -= 1
        self.set(key, node.value)
        return node.value

    def __repr__(self):
        return self._cache.__repr__()

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    # dll = DoublyLinkedList()

    # dll.append(101)
    # dll.append(102)
    # dll.append(103)
    # print(dll)
    # dll.pop()
    # print(dll)
    # dll.pop()
    # print(dll)
    # dll.pop()
    # print(dll)

    lru = LRUCache(5)

    lru.set('c', 'ccc')
    lru.set('b', 'bbb')
    lru.set('a', 'aaa')
    lru.set(3, 333)
    lru.set(2, 222)
    lru.set(1, 111)

    print(lru)
    print(lru.get(3))
    print(lru)
    print(lru.get(2))
    print(lru)
