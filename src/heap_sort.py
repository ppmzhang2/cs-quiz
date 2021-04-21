from __future__ import annotations

from dataclasses import dataclass
from typing import List, NoReturn, Optional, Tuple


@dataclass
class Heap:
    arr: List[int]

    @property
    def length(self) -> int:
        return len(self.arr)

    @property
    def last_index(self) -> int:
        return self.length - 1

    @staticmethod
    def left_index(idx: int) -> int:
        return idx * 2 + 1

    @staticmethod
    def right_index(idx: int) -> int:
        return idx * 2 + 2

    @staticmethod
    def parent_index(idx: int) -> int:
        return (idx - 1) // 2

    @property
    def last_non_leaf_node_index(self) -> int:
        return self.parent_index(self.last_index)

    def get(self, idx: int) -> Optional[int]:
        try:
            return self.arr[idx]
        except IndexError:
            return None

    def swap(self, i: int, j: int) -> NoReturn:
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def swap_pop(self) -> NoReturn:
        self.swap(0, self.last_index)
        value, self.arr = self.arr[-1], self.arr[:-1]
        return value

    def heapify_from(self, idx: int) -> NoReturn:
        parent = self.get(idx)
        left_index = self.left_index(idx)
        right_index = self.right_index(idx)
        left = self.get(left_index)
        right = self.get(right_index)
        # dealing None
        if left is None and right is None:
            return None
        if right is None and left > parent:
            self.swap(idx, left_index)
            return self.heapify_from(left_index)
        if right is None:
            return None
        # left and right not None
        if left >= right > parent or left > parent >= right:
            self.swap(idx, left_index)
            return self.heapify_from(left_index)
        if right >= left > parent or right > parent >= left:
            self.swap(idx, right_index)
            return self.heapify_from(right_index)
        return None

    def heapify(self) -> NoReturn:
        for idx in range(self.last_non_leaf_node_index, -1, -1):
            self.heapify_from(idx)


@dataclass
class FSM:
    heap: Heap
    res: Tuple[int, ...]

    @property
    def done(self) -> bool:
        if not self.heap.arr:
            return True
        return False

    def sort(self):
        value = self.heap.swap_pop()
        self.res = (*self.res, value)
        self.heap.heapify_from(0)


class HeapSort:
    @staticmethod
    def solution(seq: List[int]):
        acc = ()
        heap = Heap(seq)
        heap.heapify()
        while True:
            if not heap.arr:
                return acc
            value = heap.swap_pop()
            heap.heapify_from(0)
            acc = (value, *acc)


if __name__ == '__main__':
    ipt_1 = [2, 4, 6, 0, 1, 9, 3, 8, 5, 7]
    exp_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    # heap = Heap(list(ipt_1))
    # heap.heapify()
    # print(heap.arr)

    hs = HeapSort()
    assert exp_1 == hs.solution(ipt_1)
