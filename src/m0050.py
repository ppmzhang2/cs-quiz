"""pow-x-n
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
from typing import NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    base: float
    new_base: float
    negative: bool
    facter: int
    remainers: Sequence[int]

    @property
    def status(self) -> int:
        if self.facter > 1 and not self.remainers:
            return 0
        if self.facter > 1:
            return 1
        if self.facter == 1 and len(self.remainers) >= 1:
            return 2
        return 3


class Pow:
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
        facter = n // 2
        remainer = n - 2 * facter
        return facter, remainer

    def disassemble(self, mw: Middleware) -> Middleware:
        assert mw.status <= 1
        new_facter, new_remainer = self.parameterize(mw.facter)
        return Middleware(
            mw.base,
            mw.new_base,
            mw.negative,
            new_facter,
            (new_remainer, *mw.remainers),
        )

    def assemble(self, mw: Middleware) -> Middleware:
        assert mw.status >= 2
        remainer = mw.remainers[0]
        new_base = (self.naive_pow(mw.new_base, 2) *
                    self.naive_pow(mw.base, remainer))
        return Middleware(
            mw.base,
            new_base,
            mw.negative,
            mw.facter,
            mw.remainers[1:],
        )

    def looper(self, mw: Middleware) -> Middleware:
        if mw.status == 3:
            return mw
        if mw.status <= 1:
            return self.looper(self.disassemble(mw))
        if mw.status >= 2:
            return self.looper(self.assemble(mw))
        raise ValueError('Unexpected middleware')

    def solution(self, x: float, n: int):
        mw = Middleware(x, x, n < 0, abs(n), ())
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
