from typing import Tuple


class TwoSumSorted:
    @staticmethod
    def solution(arr: Tuple[int, ...], target: int):
        def helper(arr_: Tuple[int, ...], target_: int, idx_beg: int,
                   idx_end: int, rec: Tuple[Tuple[int, int], ...]):
            if idx_beg >= idx_end:
                return rec
            if arr[idx_beg] + arr[idx_end] < target:
                return helper(arr_, target_, idx_beg + 1, idx_end, rec)
            if arr[idx_beg] + arr[idx_end] > target:
                return helper(arr_, target_, idx_beg, idx_end - 1, rec)
            return helper(arr_, target_, idx_beg + 1, idx_end - 1,
                          rec + ((idx_beg, idx_end), ))

        return helper(arr, target, 0, len(arr) - 1, ())


if __name__ == '__main__':
    in1_1 = (2, 7, 11, 15)
    in1_2 = 9
    in2_1 = (1, 2, 4, 5, 7, 8)
    in2_2 = 9
    exp1 = ((0, 1), )
    exp2 = ((0, 5), (1, 4), (2, 3))

    assert TwoSumSorted.solution(in1_1, in1_2) == exp1
    assert TwoSumSorted.solution(in2_1, in2_2) == exp2
