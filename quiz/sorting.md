# Sorting

## Merge Sort

Divide and conquer, sorting by merging from the smallest part after dividing.

1. [with-splitting](../src/merge_sort.py)
2. [without-splitting](../src/merge_sort_fsm.py)

## Quick Sort

Divide and conquer, similar to merge sort but with a top-down method instead of bottom-up: sorting when dividing, and splicing all together finally.

* [fsm](../src/quick_sort.py)

## Heap Sort

1. create a min-max heap `H[0, 1, ..., n-1]`
2. heapify from the last non-leaf node to the top
3. swap top and bottom
4. reduce the heap size and heapify at the top
4. start from step 3

* [heap](../src/heap_sort.py)

## Radix Sort

In each iteration, it distributes elements into buckets according to their radix and re-arrange their order by their radix.

* [radix-sort](../src/radix_sort.py)

## Insertion Sort

1. consuming one input element each repetition and growing a sorted output list
2. at each iteration, removes one element from the input data, finds the location it belongs within the sorted list and inserts it there
3. repeats until no input elements remain

* [insertion-sort](../src/insertion_sort.py)

## Reference

1. https://zhuanlan.zhihu.com/p/95080265
