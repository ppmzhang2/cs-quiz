"""Coin Change
TAG: dynamic-programming

You are given coins of different denominations and a total amount of money
amount. Write a function to compute the fewest number of coins that you need to
make up that amount. If that amount of money cannot be made up by any
combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0

Example 4:
Input: coins = [1], amount = 1
Output: 1

Example 5:
Input: coins = [1], amount = 2
Output: 2

Constraints:

* 1 <= coins.length <= 12
* 1 <= coins[i] <= 231 - 1
* 0 <= amount <= 104
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Sequence, Tuple


@unique
class State(Enum):
    DOING = 1
    DONE = 2
    INVALID = 3


@dataclass(frozen=True)
class FSM:
    amount: int
    coins: Tuple[int, ...]
    actions: Tuple[int, ...]

    @property
    def state(self) -> State:
        if self.amount == 0:
            return State.DONE
        if self.amount < 0 or not self.coins:
            return State.INVALID
        return State.DOING

    @property
    def count(self) -> int:
        return len(self.actions)

    def explode(self) -> Tuple[FSM, ...]:
        assert self.state == State.DOING
        seq_actions = [(*self.actions, coin) for coin in self.coins]
        seq_amount = [self.amount - coin for coin in self.coins]
        return tuple((type(self))(
            amount,
            self.coins,
            actions,
        ) for actions, amount in zip(seq_actions, seq_amount))


class CoinChange:
    @classmethod
    def looper(
        cls,
        inputs: Tuple[FSM, ...],
        outputs: Tuple[FSM, ...],
    ) -> Tuple[FSM, ...]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.state == State.INVALID:
            return cls.looper(inputs[1:], outputs)
        if fsm.state == State.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        return cls.looper((*fsm.explode(), *inputs[1:]), outputs)

    def solution(self, coins: Sequence[int], amount: int):
        if not amount:
            print('trivial, no solution needed')
            return 0
        fsm = FSM(amount, coins, ())
        res = self.looper((fsm, ), ())
        if not res:
            print('no solution available')
            return -1
        best = min(res, key=lambda x: x.count)
        print(f'the best solution: {best}')
        return best.count


if __name__ == '__main__':
    ipt_1_1 = [1, 2, 5]
    ipt_1_2 = 11
    exp_1 = 3
    ipt_2_1 = [2]
    ipt_2_2 = 3
    exp_2 = -1
    ipt_3_1 = [1]
    ipt_3_2 = 0
    exp_3 = 0
    ipt_4_1 = [1]
    ipt_4_2 = 1
    exp_4 = 1
    ipt_5_1 = [1]
    ipt_5_2 = 2
    exp_5 = 2

    cc = CoinChange()
    assert exp_1 == cc.solution(ipt_1_1, ipt_1_2)
    assert exp_2 == cc.solution(ipt_2_1, ipt_2_2)
    assert exp_3 == cc.solution(ipt_3_1, ipt_3_2)
    assert exp_4 == cc.solution(ipt_4_1, ipt_4_2)
    assert exp_5 == cc.solution(ipt_5_1, ipt_5_2)
