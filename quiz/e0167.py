# -*- coding: utf-8 -*-
"""Two Sum ii: Input Array is Sorted

Given an array of integers that is already sorted in ascending order, find two
numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they
add up to the target, where index1 must be less than index2.

Note:

Your returned answers (both index1 and index2) are not zero-based.
You may assume that each input would have exactly one solution and you may
not use the same element twice.
Example:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore index1 = 1, index2 = 2.

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
