from collections import deque
from functools import reduce
from typing import Optional, Sequence, TypeVar

T = TypeVar('T')


class EmptyStackException(Exception):
    pass


class Stack:
    __slots__ = ['__stack']

    def __init__(self, arr: Sequence[Optional[T]] = ()):
        self.__stack: deque = deque(arr)

    def __len__(self) -> int:
        return len(self.__stack)

    def __iter__(self):
        while True:
            try:
                e = self.pop()
                yield e
            except EmptyStackException:
                break

    def empty(self) -> bool:
        if self.__len__() == 0:
            return True
        return False

    def __empty_exception(self):
        if self.empty():
            raise EmptyStackException('Stack is empty!')

    def push(self, e):
        self.__stack.append(e)

    def peak(self) -> T:
        self.__empty_exception()
        return self.__stack[-1]

    def pop(self) -> T:
        self.__empty_exception()
        e = self.__stack.pop()
        return e

    def __str__(self):
        if self.empty():
            return 'Stack([])'
        return 'Stack([' + reduce(lambda x, y: x + ', ' + y,
                                  map(str, self.__stack)) + '])'

    def __repr__(self):
        return self.__str__()
