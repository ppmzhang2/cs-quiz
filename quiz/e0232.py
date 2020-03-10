# -*- coding: utf-8 -*-
"""Implement Queue Using Stacks
Implement the following operations of a queue using stacks.

push(x) -- Push element x to the back of queue.
pop() -- Removes the element from in front of queue.
peek() -- Get the front element.
empty() -- Return whether the queue is empty.
Example:

MyQueue queue = new MyQueue();

queue.push(1);
queue.push(2);
queue.peek();  // returns 1
queue.pop();   // returns 1
queue.empty(); // returns false
Notes:

You must use only standard operations of a stack -- which means only push to
top, peek/pop from top, size, and is empty operations are valid.

Depending on your language, stack may not be supported natively. You may
simulate a stack by using a list or deque (double-ended queue), as long as
you use only standard operations of a stack.

You may assume that all operations are valid (for example, no pop or peek
operations will be called on an empty queue).

"""

from typing import Iterable, Optional, Any
from adt.stack import Stack


class Queue(object):
    __slots__ = ['__main_stk', '__aux_stk']

    def __init__(self, itr: Iterable[Optional[Any]] = ()):
        self.__main_stk = Stack()
        self.__aux_stk = Stack()
        list(map(lambda x: Queue.push(self, x), itr))

    def push(self, e: Any):
        self.__aux_stk = Stack(iter(self.__main_stk))
        self.__aux_stk.push(e)
        self.__main_stk = Stack(iter(self.__aux_stk))

    def peak(self) -> Any:
        return self.__main_stk.peak()

    def pop(self) -> Any:
        self.__main_stk.pop()

    def empty(self) -> bool:
        return self.__main_stk.empty()

    def __str__(self):
        return 'Queue' + str(self.__main_stk)[5:]

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    qu = Queue(iter((1, )))
    print(qu)
    qu.push(111)
    print(qu)
    qu.pop()
    print(qu)
    qu.push(222)
    print(qu)
