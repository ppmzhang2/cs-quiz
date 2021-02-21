# -*- coding: utf-8 -*-
"""Min-stack

Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.

"""

from functools import reduce
from collections import deque
from math import inf


class MinStack(object):
    __slots__ = ['__stack', '__aux']

    def __init__(self):
        self.__stack: deque = deque()
        self.__aux: deque = deque()

    def get_min(self):
        try:
            return self.__aux[-1]
        except IndexError:
            return inf

    def push(self, e: int):
        if e <= self.get_min():
            self.__aux.append(e)
        self.__stack.append(e)

    def pop(self):
        e = self.__stack.pop()
        if e == self.get_min():
            self.__aux.pop()
        return e

    def __str__(self):
        return 'MinStack(' + reduce(lambda x, y: str(x) + ', ' + str(y),
                                    self.__stack) + ')'

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    in1 = (-3, -4, -1, 5, -4, -20)
    exp1_str = 'MinStack(-3, -4, -1, 5, -4, -20)'
    exp1_min1 = -20
    exp1_min2 = -4
    exp1_pop1 = -20

    ms = MinStack()
    list(map(lambda x: ms.push(x), in1))
    assert str(ms) == exp1_str
    assert ms.get_min() == exp1_min1
    assert ms.pop() == exp1_pop1
    assert ms.get_min() == exp1_min2
