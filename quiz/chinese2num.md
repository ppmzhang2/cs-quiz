# Chinese String to Number

Convert a sequence of Chinese characters into a number

## Explanation

The numerical Chinese characters use six units and ten digits:

- units
  - GE ("个"): 1
  - SHI ("十"): 10
  - BAI ("百"): 100
  - QIAN ("千"): 1,000
  - WAN ("万"): 10,000
  - YI ("亿"): 100,000,000
- digits
  - "零": 0
  - "一": 1
  - "二": 2
  - "三": 3
  - "四": 4
  - "五": 5
  - "六": 6
  - "七": 7
  - "八": 8
  - "九": 9

The character string for "5,372,654,839" is "五十三亿七千二百六十五万四千八百三十九", which can be dismantled into three addends:

- "五十三亿" (5,300,000,000)
- "七千二百六十五万" (72,650,000)
- "四千八百三十九" (4,839)

Each addend includes a series of digits with descending units, as well as a trailing unit:

- "五十三亿" (5,300,000,000)
  - "五十三"
  - "亿"
- "七千二百六十五万" (72,650,000)
  - "七千二百六十五"
  - "万"
- "四千八百三十九" (4,839)
  - "四千八百三十九"
  - "个"

Each of the first element of one group includes several pairs of numbers and units:

- "五十三亿" (5,300,000,000)
  - "五十三"
    - "五十"
    - "三个"
  - "亿"
- "七千二百六十五万" (72,650,000)
  - "七千二百六十五"
    - "七千"
    - "二百"
    - "六十"
    - "五个"
  - "万"
- "四千八百三十九" (4,839)
  - "四千八百三十九"
    - "四千"
    - "八百"
    - "三十"
    - "九个"
  - "个"

Thus a Chinese number can be expressed with the following three structures:

1. the most elementary structure with a digit and a unit, e.g. `(7, QIAN)`
2. a sequence of the elementary structures, and its value is the sum, e.g. `[(7, QIAN), (2, BAI), (6, SHI), (5, GE)]`
3. the second structure and a unit, e.g. `([(7, QIAN), (2, BAI), (6, SHI), (5, GE)], WAN)`

## Source Code

- [FSM](../src/chinese2num.py)
