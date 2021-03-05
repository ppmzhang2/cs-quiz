"""Remove Duplicates from Sorted Array II
Given a sorted array nums, remove the duplicates in-place such that duplicates
appeared at most twice and return the new length.

Do not allocate extra space for another array; you must do this by modifying
the input array in-place with O(1) extra memory.

Clarification:
Confused why the returned value is an integer, but your answer is an array?
Note that the input array is passed in by reference, which means a modification
to the input array will be known to the caller.

Internally you can think of this:

// nums is passed in by reference. (i.e., without making a copy)
int len = removeDuplicates(nums);

// any modification to nums in your function would be known by the caller
// using the length returned by your function, it prints the first len elements
for (int i = 0; i < len; i++) {
    print(nums[i]);
}

Example 1:
Input: nums = [1,1,1,2,2,3]
Output: 5, nums = [1,1,2,2,3]
Explanation: Your function should return length = 5, with the first five
elements of nums being 1, 1, 2, 2 and 3 respectively. It doesn't matter what
you leave beyond the returned length.

Example 2:
Input: nums = [0,0,1,1,1,1,2,3,3]
Output: 7, nums = [0,0,1,1,2,3,3]
Explanation: Your function should return length = 7, with the first seven
elements of nums being modified to 0, 0, 1, 1, 2, 3 and 3 respectively. It
doesn't matter what values are set beyond the returned length.

Constraints:
* 1 <= nums.length <= 3 * 104
* -104 <= nums[i] <= 104
* nums is sorted in ascending order.
"""
from collections import defaultdict
from typing import Sequence


class HashTable:
    __slots__ = ['_dd']

    @staticmethod
    def zero():
        return 0

    def __init__(self):
        self._dd = defaultdict(self.zero)

    def __str__(self):
        return self._dd.__str__()

    def add(self, key: int):
        value = self._dd[key]
        if value in (0, 1):
            self._dd[key] += 1

    @property
    def seq(self):
        items = self._dd.items()
        res = []
        for k, v in items:
            res += [k] * v

        return res

    @property
    def seq_length(self):
        return sum(self._dd.values())


class RemoveDuplicates:
    @staticmethod
    def solution(seq: Sequence):
        ht = HashTable()
        for i in seq:
            ht.add(i)

        return ht.seq


if __name__ == '__main__':
    ipt_1 = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    exp_1 = [0, 0, 1, 1, 2, 3, 3]

    rd = RemoveDuplicates()
    assert exp_1 == rd.solution(ipt_1)
