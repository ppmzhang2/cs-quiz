# -*- coding: utf-8 -*-

from functools import reduce
from collections import deque
from typing import Iterable, Optional, Any


class EmptyStackException(Exception):
    pass


class Stack(object):
    __slots__ = ['__stack']

    def __init__(self, arr: Iterable[Optional[Any]] = ()):
        self.__stack: deque = deque(arr)

    def __len__(self):
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
        else:
            return False

    def __empty_exception(self):
        if self.empty():
            raise EmptyStackException('Stack is empty!')

    def push(self, e: int):
        self.__stack.append(e)

    def peak(self):
        self.__empty_exception()
        return self.__stack[-1]

    def pop(self):
        self.__empty_exception()
        e = self.__stack.pop()
        return e

    def __str__(self):
        if self.empty():
            return 'Stack([])'
        else:
            return 'Stack([' + reduce(lambda x, y: x + ', ' + y,
                                      map(str, self.__stack)) + '])'

    def __repr__(self):
        return self.__str__()
