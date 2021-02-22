"""pow-x-n
TAG: math

Implement pow(x, n), which calculates x raised to the power n (i.e. xn).

Example 1:
Input: x = 2.00000, n = 10
Output: 1024.00000

Example 2:
Input: x = 2.10000, n = 3
Output: 9.26100

Example 3:
Input: x = 2.00000, n = -2
Output: 0.25000
Explanation: 2^(-2) = 1/2^2 = 1/4 = 0.25

Constraints:
* -100.0 < x < 100.0
* -2^31 <= n <= 2^31-1
* -10^4 <= x^n <= 10^4
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Sequence, Tuple


@unique
class Status(Enum):
    INIT = 0
    DISASSEMBLE = 1
    ASSEMBLE = 2
    DONE = 3


@dataclass(frozen=True)
class FSM:
    base: float
    new_base: float
    negative: bool
    factor: int
    powers: Sequence[int]

    @staticmethod
    def naive_pow(base: float, power: int) -> float:
        if power == 2:
            return base * base
        if power == 1:
            return base
        if power == 0:
            return 1
        raise ValueError('power number not supported')

    @staticmethod
    def parameterize(n: int) -> Tuple[int, int]:
        factor = n // 2
        remainer = n - 2 * factor
        return factor, remainer

    @property
    def status(self) -> Status:
        if self.factor > 1 and not self.powers:
            return Status.INIT
        if self.factor > 1:
            return Status.DISASSEMBLE
        if self.factor == 1 and len(self.powers) >= 1:
            return Status.ASSEMBLE
        return Status.DONE

    def disassemble(self) -> FSM:
        assert self.status in (Status.INIT, Status.DISASSEMBLE)
        new_factor, new_power = self.parameterize(self.factor)
        return FSM(
            self.base,
            self.new_base,
            self.negative,
            new_factor,
            (new_power, *self.powers),
        )

    def assemble(self) -> FSM:
        assert self.status == Status.ASSEMBLE
        power = self.powers[0]
        new_base = (self.naive_pow(self.new_base, 2) *
                    self.naive_pow(self.base, power))
        return FSM(
            self.base,
            new_base,
            self.negative,
            self.factor,
            self.powers[1:],
        )


class Pow:
    def looper(self, mw: FSM) -> FSM:
        if mw.status == Status.DONE:
            return mw
        if mw.status in (Status.INIT, Status.DISASSEMBLE):
            return self.looper(mw.disassemble())
        if mw.status == Status.ASSEMBLE:
            return self.looper(mw.assemble())
        raise ValueError('Unexpected middleware')

    def solution(self, x: float, n: int):
        mw = FSM(x, x, n < 0, abs(n), ())
        mw_ = self.looper(mw)
        if mw_.negative:
            return 1 / mw_.new_base
        return mw_.new_base


if __name__ == '__main__':
    ipt_1_1 = 2.0
    ipt_1_2 = 10
    exp_1 = 1024
    ipt_2_1 = 2.1
    ipt_2_2 = 3
    exp_2 = 9.261
    ipt_3_1 = 2.0
    ipt_3_2 = -2
    exp_3 = 0.25

    p = Pow()
    assert abs(p.solution(ipt_1_1, ipt_1_2) - exp_1) <= 0.01
    assert abs(p.solution(ipt_2_1, ipt_2_2) - exp_2) <= 0.01
    assert abs(p.solution(ipt_3_1, ipt_3_2) - exp_3) <= 0.01
