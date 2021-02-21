"""combination sum ii
Given a collection of candidate numbers (candidates) and a target number
(target), find all unique combinations in candidates where the candidate
numbers sum to target.

Each number in candidates may only be used once in the combination.

Note: The solution set must not contain duplicate combinations.

Example 1:
* Input: candidates = [10,1,2,7,6,1,5], target = 8
* Output:
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]

Example 2:
* Input: candidates = [2,5,2,1,2], target = 5
* Output:
[
[1,2,2],
[5]
]


Constraints:

1 <= candidates.length <= 100
1 <= candidates[i] <= 50
1 <= target <= 30
"""
from typing import NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    candidates: Tuple[int]
    target: int
    addends: Tuple[int]

    @staticmethod
    def _qualifier(asc_seq: Sequence[int], target: int) -> Tuple[int, ...]:
        def helper(asc_seq: Sequence[int], target: int,
                   acc: Tuple[int, ...]) -> Tuple[int, ...]:
            if not asc_seq:
                return acc
            smallest = asc_seq[0]
            if smallest <= target:
                return helper(asc_seq[1:], target, (*acc, smallest))
            return acc

        return helper(asc_seq, target, ())

    def qualifier(self):
        return Middleware(
            self._qualifier(sorted(self.candidates), self.target),
            self.target,
            self.addends,
        )

    @property
    def status(self):
        if self.target == 0:
            return 1
        if not self.candidates:
            return -1
        return 0


class CombSum2:
    @staticmethod
    def mapper(mw: Middleware) -> Tuple[Middleware, ...]:
        seq: Tuple[Middleware, ...] = tuple(
            Middleware(
                (*mw.candidates[:idx], *mw.candidates[idx + 1:]),
                mw.target - elem,
                (*mw.addends, elem),
            ) for idx, elem in enumerate(mw.candidates))
        return tuple(mw_.qualifier() for mw_ in seq)

    def looper(
        self,
        inputs: Sequence[Middleware],
        outputs: Sequence[Middleware],
    ) -> Sequence[Middleware]:
        if not inputs:
            return outputs
        mw: Middleware = inputs[0]
        if mw.status == 0:
            return self.looper((*inputs[1:], *self.mapper(mw)), outputs)
        if mw.status == 1:
            return self.looper(inputs[1:], (*outputs, mw))
        return self.looper(inputs[1:], outputs)

    def solution(self, nums: Sequence[int],
                 target: int) -> Tuple[Tuple[int, ...], ...]:
        mw = Middleware(nums, target, ()).qualifier()
        mw_seq = self.looper((mw, ), ())
        return tuple(sorted(set(tuple(sorted(mw_.addends)) for mw_ in mw_seq)))


if __name__ == '__main__':
    ipt_1_1 = [10, 1, 2, 7, 6, 1, 5]
    ipt_1_2 = 8
    exp_1 = (
        (1, 1, 6),
        (1, 2, 5),
        (1, 7),
        (2, 6),
    )
    ipt_2_1 = [2, 5, 2, 1, 2]
    ipt_2_2 = 5
    exp_2 = (
        (1, 2, 2),
        (5, ),
    )

    cs = CombSum2()

    assert Middleware(ipt_1_1, ipt_1_2, ()).qualifier() == Middleware(
        (1, 1, 2, 5, 6, 7),
        8,
        (),
    )
    assert Middleware(ipt_2_1, ipt_2_2, ()).qualifier() == Middleware(
        (1, 2, 2, 2, 5),
        5,
        (),
    )

    assert cs.solution(ipt_1_1, ipt_1_2) == exp_1
    assert cs.solution(ipt_2_1, ipt_2_2) == exp_2
