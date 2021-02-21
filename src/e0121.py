# -*- coding: utf-8 -*-
"""Best Time to Buy and Sell Stock

Say you have an array for which the ith element is the price of a given stock
on day i.

If you were only permitted to complete at most one transaction (i.e., buy one
and sell one share of the stock), design an algorithm to find the maximum
profit.

Note that you cannot sell a stock before you buy one.

Example 1:

Input: [7,1,5,3,6,4]
Output: 5
Explanation:
    Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
    Not 7-1 = 6, as selling price needs to be larger than buying price.
Example 2:

Input: [7,6,4,3,1]
Output: 0
Explanation: In this case, no transaction is done, i.e. max profit = 0.

"""

from __future__ import annotations
from typing import Tuple
from functools import reduce


class DP(object):
    @staticmethod
    def __max_profit_buy_at(arr: Tuple, buy: int) -> int:
        sell = reduce(lambda x, y: max(x, y), arr[buy + 1:], arr[buy])
        return sell - arr[buy]

    @staticmethod
    def solution(arr: Tuple) -> int:
        tp = (DP.__max_profit_buy_at(arr, i) for i in range(len(arr)))
        return max(tp)


class Ex(object):
    """
    based on extreme
    """
    @staticmethod
    def __if_minima(arr: Tuple[int, ...], idx: int) -> bool:
        if idx >= len(arr) - 1:
            return False
        elif idx == 0:
            if arr[idx] < arr[idx + 1]:
                return True
            else:
                return False
        elif arr[idx - 1] > arr[idx] < arr[idx + 1]:
            return True
        else:
            return False

    @staticmethod
    def __if_extreme(arr: Tuple[int, ...], idx: int) -> bool:
        if idx >= len(arr):
            return False
        elif idx == len(arr) - 1:
            if arr[idx] > arr[idx - 1]:
                return True
            else:
                return False
        elif idx == 0:
            if arr[idx] < arr[idx + 1]:
                return True
            else:
                return False
        elif arr[idx - 1] > arr[idx] < arr[idx + 1]:
            return True
        elif arr[idx - 1] < arr[idx] > arr[idx + 1]:
            return True
        else:
            return False


if __name__ == '__main__':
    in1 = (6, 4, 2, 5, 3, 7, 1, 4)
    exp1 = 5
    in2 = (7, 6, 4, 3, 1)
    exp2 = 0

    assert exp1 == DP.solution(in1)
    assert exp2 == DP.solution(in2)
