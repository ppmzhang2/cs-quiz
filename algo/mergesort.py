from typing import Tuple


class MergeSort(object):
    @staticmethod
    def __merge(arr1: Tuple[int, ...], arr2: Tuple[int, ...]):
        def helper(arr1_: Tuple[int, ...], arr2_: Tuple[int, ...],
                   rec: Tuple[int, ...]):
            if not arr1_ and not arr2_:
                return rec
            elif not arr1_:
                return rec + arr2_
            elif not arr2_:
                return rec + arr1_
            else:
                if arr1_[0] >= arr2_[0]:
                    return helper(arr1_, arr2_[1:], rec + (arr2_[0], ))
                else:
                    return helper(arr1_[1:], arr2_, rec + (arr1_[0], ))

        return helper(arr1, arr2, ())

    @staticmethod
    def sort(arr: Tuple[int, ...]):
        if len(arr) <= 1:
            return arr
        else:
            idx = len(arr) // 2
            left = arr[:idx]
            right = arr[idx:]
            return MergeSort.__merge(MergeSort.sort(left),
                                     MergeSort.sort(right))


if __name__ == '__main__':
    in1 = (2, 4, 6, 0, 1, 9, 3, 8, 5, 7)
    exp1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    assert MergeSort.sort(in1) == exp1
