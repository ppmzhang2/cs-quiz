# Tree

- Vanilla Tree
  - A collection of special values (a.k.a. nodes) that points to others
  - refer to [linked list](./linkedlist.md)
- Zipper Tree
  - a node and its context
  - context: a collection of "breadcrumbs" that leads to the node
    - why: a node itself can only go to any of its children; its breadcrumbs
      enable path to parent and siblings
    - structure: each node has its own breadcrumbs, resulting the context
      to be a list or a recursive struct
  - zipper concept can also be applied to other structures e.g. linked list

## Quizzes

- [E0104: maximum-depth-of-binary-tree](../src/e0104.py)
- [E0226: invert-binary-tree](../src/e0226.py)
- [M0094: Binary-Tree-Inorder-Traversal](../src/m0094.py)
- [M0095: Unique-Binary-Search-Trees-II](../src/m0095.py)
- [M0096: Unique-Binary-Search-Trees](../src/m0096.py)
- [M0098: Validate-Binary-Search-Tree](./m0098.md)
- [M0102: Binary-Tree-Level-Order-Traversal](../src/m0102.py)
- [M0103: Binary-Tree-Zigzag-Level-Order-Traversal](../src/m0103.py)
- [M0105: Construct Binary Tree from Pre-order and In-order Traversal](./m0105.md)
- [M0113: Path-Sum-II](./m0113.md)
- [M0144: Binary-Tree-Preorder-Traversal](./m0144.md)
- [M0199: Binary-Tree-Right-Side-View](../src/m0199.py)
- [M0236: Lowest Common Ancestor of a Binary Tree](../src/m0236.py)
- [M0513: Find Bottom Left Tree Value (91)](../src/m0513.py)
- [M0987: Vertical Order Traversal of a Binary Tree (91)](../src/m0987.py)
- [M1104: Path In Zigzag Labelled Binary Tree](../src/m1104.py)
- [M1261: Find Elements in a Contaminated Binary Tree](../src/m1261.py)
