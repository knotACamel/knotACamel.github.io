#include "AVLTree.h"

#include <algorithm>

AVLTree::AVLTree() : root_(nullptr), size_(0) {}

AVLTree::~AVLTree() {
    destroy(root_);
}

void AVLTree::destroy(Node* node) {
    if (node == nullptr) {
        return;
    }
    destroy(node->left);
    destroy(node->right);
    delete node;
}

// -1 for an empty subtree
int AVLTree::heightOf(const Node* node) {
    return node == nullptr ? -1 : node->height;
}

void AVLTree::updateHeight(Node* node) {
    node->height = 1 + std::max(heightOf(node->left), heightOf(node->right));
}

int AVLTree::balanceOf(const Node* node) {
    return node == nullptr ? 0 : heightOf(node->left) - heightOf(node->right);
}

AVLTree::Node* AVLTree::rotateRight(Node* node) {
    Node* newRoot = node->left;
    node->left = newRoot->right;
    newRoot->right = node;

    // The demoted node must be updated first, or the new root reads a stale height.
    updateHeight(node);
    updateHeight(newRoot);

    return newRoot;
}

AVLTree::Node* AVLTree::rotateLeft(Node* node) {
    Node* newRoot = node->right;
    node->right = newRoot->left;
    newRoot->left = node;

    updateHeight(node);
    updateHeight(newRoot);

    return newRoot;
}

AVLTree::Node* AVLTree::rebalance(Node* node) {
    const int balance = balanceOf(node);

    // Left heavy. Straighten a right leaning child first, then rotate.
    if (balance > 1) {
        if (balanceOf(node->left) < 0) {
            node->left = rotateLeft(node->left);
        }
        return rotateRight(node);
    }

    // Right heavy, mirrored.
    if (balance < -1) {
        if (balanceOf(node->right) > 0) {
            node->right = rotateRight(node->right);
        }
        return rotateLeft(node);
    }

    return node;
}

bool AVLTree::insert(const Course& course) {
    bool inserted = false;
    // Returning the subtree root is what lets a rotation change the parent's
    // pointer. The original addNode returned void and could not do this.
    root_ = insert(root_, course, inserted);
    return inserted;
}

AVLTree::Node* AVLTree::insert(Node* node, const Course& course, bool& inserted) {
    if (node == nullptr) {
        inserted = true;
        ++size_;
        return new Node{course, nullptr, nullptr, 0};
    }

    const int cmp = course.courseId.compare(node->course.courseId);

    if (cmp < 0) {
        node->left = insert(node->left, course, inserted);
    } else if (cmp > 0) {
        node->right = insert(node->right, course, inserted);
    } else {
        inserted = false;  // duplicate, tree unchanged
        return node;
    }

    updateHeight(node);
    return rebalance(node);
}

Course AVLTree::search(const std::string& courseId) const {
    const Node* current = root_;
    while (current != nullptr) {
        const int cmp = courseId.compare(current->course.courseId);
        if (cmp == 0) {
            return current->course;
        }
        current = cmp < 0 ? current->left : current->right;
    }
    return Course();
}

void AVLTree::inOrder(const std::function<void(const Course&)>& visit) const {
    inOrder(root_, visit);
}

void AVLTree::inOrder(const Node* node, const std::function<void(const Course&)>& visit) const {
    if (node == nullptr) {
        return;
    }
    inOrder(node->left, visit);
    visit(node->course);
    inOrder(node->right, visit);
}

int AVLTree::height() const {
    return heightOf(root_);
}

int AVLTree::size() const {
    return size_;
}

bool AVLTree::validate() const {
    int height = 0;
    int count = 0;
    if (!validate(root_, height, count)) {
        return false;
    }
    if (count != size_) {
        return false;
    }

    // A rotation that rewires the wrong pointer can still leave heights
    // consistent, so the key order is checked separately.
    bool ordered = true;
    bool first = true;
    std::string previous;
    inOrder([&](const Course& course) {
        if (!first && !(previous < course.courseId)) {
            ordered = false;
        }
        previous = course.courseId;
        first = false;
    });
    return ordered;
}

bool AVLTree::validate(const Node* node, int& height, int& count) const {
    if (node == nullptr) {
        height = -1;
        count = 0;
        return true;
    }

    int leftHeight = 0;
    int rightHeight = 0;
    int leftCount = 0;
    int rightCount = 0;

    if (!validate(node->left, leftHeight, leftCount)) {
        return false;
    }
    if (!validate(node->right, rightHeight, rightCount)) {
        return false;
    }

    height = 1 + std::max(leftHeight, rightHeight);
    count = leftCount + rightCount + 1;

    if (node->height != height) {
        return false;
    }
    const int balance = leftHeight - rightHeight;
    return balance >= -1 && balance <= 1;
}
