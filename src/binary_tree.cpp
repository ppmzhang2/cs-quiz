#include <functional>
#include <iostream>
#include <queue>

template <typename T> class BinaryTree {

  public:
    struct Node {
        T data;
        Node *left;
        Node *right;
    };

    Node *root;

  private:
    // Recursively delete all nodes in the tree, starting from the given node.
    void clear(Node *);

  public:
    // Constructor for the BinaryTree class.
    BinaryTree();

    // Destructor for the BinaryTree class.
    //
    // - Call the `clear` method to recursively delete all nodes in the tree,
    //   starting from the root.
    // - Ensure all dynamically allocated memory is properly freed, preventing
    //   memory leaks.
    // - Directly using `delete` on the root without a recursive cleanup
    //   mechanism would only free the memory allocated for the root node
    ~BinaryTree();

    void Traverse(const char &, const std::function<void(const T &)> &) const;
};

template <typename T> BinaryTree<T>::BinaryTree() { root = nullptr; }

template <typename T> BinaryTree<T>::~BinaryTree() { clear(root); }

template <typename T> void BinaryTree<T>::clear(Node *node) {
    if (node != nullptr) {
        clear(node->left);
        clear(node->right);
        delete node;
    }
}

template <typename T>
static inline void
traverse_preorder(const typename BinaryTree<T>::Node *node,
                  const std::function<void(const T &)> &func) {
    if (node != nullptr) {
        func(node->data);
        traverse_preorder(node->left, func);
        traverse_preorder(node->right, func);
    }
}

template <typename T>
static inline void
traverse_inorder(const typename BinaryTree<T>::Node *node,
                 const std::function<void(const T &)> &func) {
    if (node != nullptr) {
        traverse_inorder(node->left, func);
        func(node->data);
        traverse_inorder(node->right, func);
    }
}

template <typename T>
static inline void
traverse_postorder(const typename BinaryTree<T>::Node *node,
                   const std::function<void(const T &)> &func) {
    if (node != nullptr) {
        traverse_postorder(node->left, func);
        traverse_postorder(node->right, func);
        func(node->data);
    }
}

template <typename T>
static inline void
traverse_levelorder(const typename BinaryTree<T>::Node *node,
                    const std::function<void(const T &)> &func) {
    std::queue<const typename BinaryTree<T>::Node *> queue;
    if (node == nullptr) {
        return;
    }
    // add the root node to the queue
    queue.push(node);
    // consume the queue
    while (!queue.empty()) {
        const typename BinaryTree<T>::Node *current = queue.front();
        func(current->data);
        queue.pop();
        if (current->left != nullptr) {
            queue.push(current->left);
        }
        if (current->right != nullptr) {
            queue.push(current->right);
        }
    }
}

template <typename T>
void BinaryTree<T>::Traverse(const char &method,
                             const std::function<void(const T &)> &func) const {
    switch (method) {
    case 'P': // Pre-order
        return traverse_preorder(root, func);
    case 'I': // In-order
        return traverse_inorder(root, func);
    case 'O': // Post-order
        return traverse_postorder(root, func);
    case 'L': // Level-order
        return traverse_levelorder(root, func);
    default:
        std::cerr << "Invalid traversal method specified." << std::endl;
        exit(1);
    }
}

int main() {
    BinaryTree<int> tree;

    BinaryTree<int>::Node *node_0 = new BinaryTree<int>::Node;
    BinaryTree<int>::Node *node_1 = new BinaryTree<int>::Node;
    BinaryTree<int>::Node *node_2 = new BinaryTree<int>::Node;
    BinaryTree<int>::Node *node_3 = new BinaryTree<int>::Node;
    BinaryTree<int>::Node *node_4 = new BinaryTree<int>::Node;
    BinaryTree<int>::Node *node_5 = new BinaryTree<int>::Node;

    node_0->data = 0;
    node_1->data = 1;
    node_2->data = 2;
    node_3->data = 3;
    node_4->data = 4;
    node_5->data = 5;

    node_0->left = node_1;
    node_0->right = node_2;
    node_1->left = node_3;
    node_2->left = node_4;
    node_2->right = node_5;

    tree.root = node_0;

    tree.Traverse('P', [](const int &data) { std::cout << data << ' '; });
    std::cout << std::endl;
    tree.Traverse('L', [](const int &data) { std::cout << data << ' '; });
    std::cout << std::endl;
}
