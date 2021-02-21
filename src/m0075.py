"""Sort Colors
Given an array nums with n objects colored red, white, or blue, sort them
in-place so that objects of the same color are adjacent, with the colors in the
order red, white, and blue.

Here, we will use the integers 0, 1, and 2 to represent the color red, white,
and blue respectively.

Follow up:
* Could you solve this problem without using the library's sort function?
* TBD: Could you come up with a one-pass algorithm using only O(1) constant
  space?

Example 1:
Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Example 2:
Input: nums = [2,0,1]
Output: [0,1,2]

Example 3:
Input: nums = [0]
Output: [0]

Example 4:
Input: nums = [1]
Output: [1]

Constraints:

* n == nums.length
* 1 <= n <= 300
* nums[i] is 0, 1, or 2.
"""
from collections import defaultdict
from enum import Enum
from typing import Tuple


class Color(Enum):
    RED = 0
    WHITE = 1
    BLUE = 2


class SortColor:
    __slots__ = ['_dd']

    def __init__(self):
        self._dd = defaultdict(int)

    def add_color(self, color: Color):
        self._dd[color] += 1

    def solution(self, nums: int) -> Tuple[int, ...]:
        colors = [Color(i) for i in nums]
        list(map(self.add_color, colors))
        return (
            *[0] * self._dd[Color.RED],
            *[1] * self._dd[Color.WHITE],
            *[2] * self._dd[Color.BLUE],
        )


if __name__ == '__main__':
    ipt_1 = [2, 0, 2, 1, 1, 0, 0]
    exp_1 = (0, 0, 0, 1, 1, 2, 2)

    sc = SortColor()
    assert sc.solution(ipt_1) == exp_1
