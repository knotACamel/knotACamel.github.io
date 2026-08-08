#ifndef AVL_TREE_H
#define AVL_TREE_H

#include <functional>
#include <string>
#include <vector>

// One course record.
struct Course {
    std::string courseId;
    std::string title;
    std::vector<std::string> prereq;

    // A default constructed Course is the "not found" result.
    bool empty() const { return courseId.empty(); }
};

// Self balancing search tree keyed on courseId. Replaces the unbalanced
// binary search tree in the original artifact.
class AVLTree {
public:
    AVLTree();
    ~AVLTree();

    AVLTree(const AVLTree&) = delete;
    AVLTree& operator=(const AVLTree&) = delete;

    // Returns false if courseId is already present.
    bool insert(const Course& course);

    // Returns an empty Course when courseId is absent.
    Course search(const std::string& courseId) const;

    // Keys come out in ascending order.
    void inOrder(const std::function<void(const Course&)>& visit) const;

    int height() const;
    int size() const;

    // Confirms stored heights match their children
    bool validate() const;

private:
    struct Node {
        Course course;
        Node* left = nullptr;
        Node* right = nullptr;
        int height = 0;
    };

    Node* root_;
    int size_;

    static int heightOf(const Node* node);
    static void updateHeight(Node* node);
    static int balanceOf(const Node* node);

    Node* rotateRight(Node* node);
    Node* rotateLeft(Node* node);
    Node* rebalance(Node* node);

    Node* insert(Node* node, const Course& course, bool& inserted);
    void destroy(Node* node);
    void inOrder(const Node* node, const std::function<void(const Course&)>& visit) const;
    bool validate(const Node* node, int& height, int& count) const;
};

#endif
