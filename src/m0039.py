"""combination sum
TAG: array, back-tracking

Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen numbers
sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two
combinations are unique if the frequency of at least one of the chosen numbers
is different.

It is guaranteed that the number of unique combinations that sum up to target
is less than 150 combinations for the given input.

Example 1:
* Input: candidates = [2,3,6,7], target = 7
* Output: [[2,2,3],[7]]
* Explanation:
  2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple
  times.
  7 is a candidate, and 7 = 7.
  These are the only two combinations.

Example 2:
* Input: candidates = [2,3,5], target = 8
* Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
* Input: candidates = [2], target = 1
* Output: []

Example 4:
* Input: candidates = [1], target = 1
* Output: [[1]]

Example 5:
* Input: candidates = [1], target = 2
* Output: [[1,1]]

Constraints:
* 1 <= candidates.length <= 30
* 1 <= candidates[i] <= 200
* All elements of candidates are distinct.
* 1 <= target <= 500
"""
from typing import List, NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    asc_seq: Sequence[int]
    target: int
    acc_seq: Sequence[int]


class CombSum:
    @staticmethod
    def seq_qualifier(asc_seq: Sequence[int], target: int) -> Tuple[int, ...]:
        def helper(
            asc_seq: Sequence[int],
            target: int,
            small_seq: Tuple[int, ...],
        ) -> Tuple[int, ...]:
            if not asc_seq:
                return small_seq
            if asc_seq[0] <= target:
                return helper(
                    asc_seq[1:],
                    target,
                    (*small_seq, asc_seq[0]),
                )
            return small_seq

        return helper(asc_seq, target, ())

    @staticmethod
    def mw_status(mw: Middleware) -> int:
        """status of a middleware
        1: the combination matches the target
        0: need further transform
        -1: combination failed
        """
        if not mw.asc_seq and mw.target == 0:
            return 1
        if not mw.asc_seq:
            return -1
        return 0

    def mapper(self, mw: Middleware) -> List[Middleware]:
        raw_seq: List[Middleware] = [
            Middleware(mw.asc_seq, mw.target - element, (*mw.acc_seq, element))
            for _, element in enumerate(mw.asc_seq)
        ]
        return [
            Middleware(
                self.seq_qualifier(mw_.asc_seq, mw_.target),
                mw_.target,
                mw_.acc_seq,
            ) for mw_ in raw_seq
        ]

    def looper(self, input_seq: Sequence[Middleware],
               output_seq: Sequence[Middleware]) -> Sequence[Middleware]:
        if not input_seq:
            return output_seq
        mw = input_seq[0]
        if self.mw_status(mw) == 0:
            return self.looper((*input_seq[1:], *self.mapper(mw)), output_seq)
        if self.mw_status(mw) == -1:
            return self.looper(input_seq[1:], output_seq)
        return self.looper(input_seq[1:], (*output_seq, mw))

    def solution(self, nums: Sequence[int], target: int):
        mw_seq = self.looper([Middleware(sorted(nums), target, ())], ())
        sorted_set = set(tuple(sorted(mw.acc_seq)) for mw in mw_seq)
        return tuple(sorted(sorted_set))


if __name__ == '__main__':
    ipt_1_1 = [2, 3, 6, 7]
    ipt_1_2 = 7
    exp_1 = ((2, 2, 3), (7, ))
    ipt_2_1 = [2, 3, 5]
    ipt_2_2 = 8
    exp_2 = ((2, 2, 2, 2), (2, 3, 3), (3, 5))

    cs = CombSum()

    assert cs.solution(ipt_1_1, ipt_1_2) == exp_1
    assert cs.solution(ipt_2_1, ipt_2_2) == exp_2
