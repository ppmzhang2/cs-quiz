# Su Doku

Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept.

Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares.

The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

board:

```
[[5, 3, 0, | 0, 7, 0, | 0, 0, 0],
 [6, 0, 0, | 1, 9, 5, | 0, 0, 0],
 [0, 9, 8, | 0, 0, 0, | 0, 6, 0],
-----------|----------|----------
 [8, 0, 0, | 0, 6, 0, | 0, 0, 3],
 [4, 0, 0, | 8, 0, 3, | 0, 0, 1],
 [7, 0, 0, | 0, 2, 0, | 0, 0, 6],
-----------|----------|----------
 [0, 6, 0, | 0, 0, 0, | 2, 8, 0],
 [0, 0, 0, | 4, 1, 9, | 0, 0, 5],
 [0, 0, 0, | 0, 8, 0, | 0, 7, 9]]
```

solution:

```
[[5, 3, 4, | 6, 7, 8, | 9, 1, 2],
 [6, 7, 2, | 1, 9, 5, | 3, 4, 8],
 [1, 9, 8, | 3, 4, 2, | 5, 6, 7],
-----------|----------|----------
 [8, 5, 9, | 7, 6, 1, | 4, 2, 3],
 [4, 2, 6, | 8, 5, 3, | 7, 9, 1],
 [7, 1, 3, | 9, 2, 4, | 8, 5, 6],
-----------|----------|----------
 [9, 6, 1, | 5, 3, 7, | 2, 8, 4],
 [2, 8, 7, | 4, 1, 9, | 6, 3, 5],
 [3, 4, 5, | 2, 8, 6, | 1, 7, 9]]
```

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, [sudoku.txt](https://projecteuler.net/project/resources/p096_sudoku.txt), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.

## Solution

- [python FSM solution](../src/euler0096.py)
