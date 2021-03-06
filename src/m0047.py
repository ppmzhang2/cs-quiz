"""permutations ii
TAG: back-tracking

Given a collection of numbers, nums, that might contain duplicates, return all
possible unique permutations in any order.

Example 1:
Input: nums = [1,1,2]
Output:
[[1,1,2],
 [1,2,1],
 [2,1,1]]

Example 2:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
"""
from typing import NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    elements: Sequence[int]
    perm: Tuple[int, ...]

    @property
    def status(self) -> int:
        if not self.elements:
            return 1
        return 0

    @staticmethod
    def increase_perm(seq: Tuple[int, ...],
                      added: int) -> Tuple[Tuple[int, ...], ...]:
        return (*((
            *seq[:idx],
            added,
            *seq[idx:],
        ) for idx, num in enumerate(seq)), (*seq, added))


class Permutation2:
    @staticmethod
    def transition(mw: Middleware) -> Tuple[Middleware]:
        assert mw.status == 0
        perm_seq = mw.increase_perm(mw.perm, mw.elements[0])
        return tuple(
            Middleware(
                mw.elements[1:],
                perm,
            ) for _, perm in enumerate(perm_seq))

    def looper(
        self,
        inputs: Sequence[Middleware],
        outputs: Sequence[Middleware],
    ) -> Tuple[Middleware, ...]:
        if not inputs:
            return outputs
        mw = inputs[0]
        if mw.status == 0:
            return self.looper((*inputs[1:], *self.transition(mw)), outputs)
        return self.looper(inputs[1:], (*outputs, mw))

    def solution(self, nums: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
        mw_seq = self.looper((Middleware(nums, ()), ), ())
        return tuple(sorted(set(mw.perm for mw in mw_seq)))


if __name__ == '__main__':
    ipt_1 = [1, 1, 2]
    exp_1 = (
        (1, 1, 2),
        (1, 2, 1),
        (2, 1, 1),
    )

    perm = Permutation2()

    middle_ware = Middleware([3], (1, 2))
    assert middle_ware.increase_perm((1, 2), 3) == (
        (3, 1, 2),
        (1, 3, 2),
        (1, 2, 3),
    )
    assert middle_ware.increase_perm((1, 2, 3), 4) == (
        (4, 1, 2, 3),
        (1, 4, 2, 3),
        (1, 2, 4, 3),
        (1, 2, 3, 4),
    )
    assert perm.solution(ipt_1) == exp_1
