# -*- coding: utf-8 -*-
"""Remove Duplicates from Sorted Array

Given a sorted array nums, remove the duplicates in-place such that each
element appear only once and return the new length.

Do not allocate extra space for another array, you must do this by modifying
the input array in-place with O(1) extra memory.

Example 1:

Given nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums
being 1 and 2 respectively.

It doesn't matter what you leave beyond the returned length. Example 2:

Given nums = [0,0,1,1,1,2,2,3,3,4],

Your function should return length = 5, with the first five elements of nums
being modified to 0, 1, 2, 3, and 4 respectively.

It doesn't matter what values are set beyond the returned length. Clarification:

Confused why the returned value is an integer but your answer is an array?

Note that the input array is passed in by reference, which means modification
to the input array will be known to the caller as well.

Internally you can think of this:

```
// nums is passed in by reference. (i.e., without making a copy)
int len = removeDuplicates(nums);

// any modification to nums in your function would be known by the caller.
// using the length returned by your function, it prints the first len elements.
for (int i = 0; i < len; i++) {
    print(nums[i]);
}
```

"""

from typing import Tuple, List


def remove_dup(arr: List[int]) -> Tuple[int, List[int]]:
    """

    :param arr: sorted array
    :return: tuple of length and deduped arrray
    """
    def helper(l: List[int], length: int,
               rec: List[int]) -> Tuple[int, List[int]]:
        if not l:
            return length, rec
        elif not rec:
            return helper(l[1:], length + 1, rec + [l[0]])
        elif rec[-1] != l[0]:
            return helper(l[1:], length + 1, rec + [l[0]])
        else:
            return helper(l[1:], length, rec)

    return helper(arr, 0, [])


if __name__ == '__main__':
    in1 = [1, 1, 2]
    in2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    in3 = []
    in4 = [1, 1, 1]
    exp1 = (2, [1, 2])
    exp2 = (5, [0, 1, 2, 3, 4])
    exp3 = (0, [])
    exp4 = (1, [1])

    assert exp1 == remove_dup(in1)
    assert exp2 == remove_dup(in2)
    assert exp3 == remove_dup(in3)
    assert exp4 == remove_dup(in4)
