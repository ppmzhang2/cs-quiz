"""Best Time to Buy and Sell Stock with Cooldown
TAG: dynamic-programming

Say you have an array for which the ith element is the price of a given stock
on day i.

Design an algorithm to find the maximum profit. You may complete as many
transactions as you like (ie, buy one and sell one share of the stock multiple
times) with the following restrictions:

You may not engage in multiple transactions at the same time (ie, you must sell
the stock before you buy again).

After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1
day)

Example:
Input: [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Sequence, Tuple


@unique
class Action(Enum):
    IDLE = 0
    BUY = 1
    SELL = 2


@unique
class Status(Enum):
    DOING = 1
    DONE = 2
    INVALID = 3


@dataclass(frozen=True)
class FSM:
    prices: Tuple[int, ...]
    stocks: int
    profit: int
    actions: Tuple[Action, ...]

    @property
    def status(self) -> Status:
        if self.stocks < 0:
            return Status.INVALID
        if not self.prices:
            return Status.DONE
        return Status.DOING

    @property
    def last_action(self) -> Action:
        if not self.actions:
            return Action.IDLE
        return self.actions[-1]

    def idle(self) -> FSM:
        assert self.status == Status.DOING
        return FSM(
            self.prices[1:],
            self.stocks,
            self.profit,
            (*self.actions, Action.IDLE),
        )

    def buy(self) -> FSM:
        assert self.status == Status.DOING
        price = self.prices[0]
        return FSM(
            self.prices[1:],
            self.stocks + 1,
            self.profit - price,
            (*self.actions, Action.BUY),
        )

    def sell(self) -> FSM:
        assert self.status == Status.DOING
        price = self.prices[0]
        return FSM(
            self.prices[1:],
            self.stocks - 1,
            self.profit + price,
            (*self.actions, Action.SELL),
        )

    def explode(self) -> Tuple[FSM, ...]:
        assert self.status == Status.DOING
        if self.last_action == Action.IDLE and self.stocks >= 1:
            return (
                self.idle(),
                self.buy(),
                self.sell(),
            )
        if self.last_action == Action.IDLE:
            return (
                self.idle(),
                self.buy(),
            )
        if self.last_action == Action.BUY:
            return (
                self.idle(),
                self.sell(),
            )
        if self.last_action == Action.SELL:
            return (self.idle(), )

        raise ValueError('invalid value')


class SellStocks:
    @classmethod
    def looper(cls, inputs: Sequence[FSM],
               outputs: Sequence[FSM]) -> Sequence[FSM]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.status == Status.INVALID:
            return cls.looper(inputs[1:], outputs)
        if fsm.status == Status.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        return cls.looper((*fsm.explode(), *inputs[1:]), outputs)

    def solution(self, prices: Sequence[int]) -> int:
        fsm = FSM(prices, 0, 0, ())
        return max(self.looper((fsm, ), ()), key=lambda x: x.profit)


if __name__ == '__main__':
    ipt_1 = [1, 2, 3, 0, 2]
    exp_1 = 3

    s = SellStocks()
    print(s.solution(ipt_1))
