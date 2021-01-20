"""Word Search
Given an m x n board and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where
"adjacent" cells are horizontally or vertically neighboring. The same letter
cell may not be used more than once.

Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],
word = "ABCB"
Output: false

Constraints:
* m == board.length
* n = board[i].length
* 1 <= m, n <= 200
* 1 <= word.length <= 103
* board and word consists only of lowercase and uppercase English letters.
"""
from typing import NamedTuple

if __name__ == '__main__':
    ipt_1_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_1_2 = "ABCCED"
    ipt_2_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_2_1 = "SEE"
    ipt_3_1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    ipt_3_1 = "ABCB"
