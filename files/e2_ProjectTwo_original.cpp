#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;
//struct to hold course data
struct Course {
    string courseId;
    string title;
    vector<string> prereq;

    Course() {
        courseId = "";
        title = "";
    }
};
//struct for nodes
struct Node {
    Course course;
    Node *left;
    Node *right;

    Node() {
        left = nullptr;
        right = nullptr;
    }

    Node(Course aCourse) : Node() {
        course = aCourse;
    }
};
//bst class 
class BinarySearchTree {

private:
    Node* root;

    void addNode(Node* node, Course course);
    void inOrder(Node* node);
    void postOrder(Node* node);
    void preOrder(Node* node);
    void destroyTree(Node* node);

public:
    BinarySearchTree();
    virtual ~BinarySearchTree();
    void InOrder();
    void PostOrder();
    void PreOrder();
    void Insert(Course course);
    Course Search(string courseId);
};
//method loading courses
void loadCrs(string filePath, BinarySearchTree* bst) {
    ifstream file(filePath);
    if (!file.is_open()) {
        cout << "Error" << endl;
        return;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string item;

        Course course;

        if (getline(ss, item, ',')) {
            course.courseId = item;
        }
        if (getline(ss, item, ',')) {
            course.title = item;
        }
        while (getline(ss, item, ',')) {
            if (!item.empty()) {
                course.prereq.push_back(item);
            }
        }

        if (!course.courseId.empty() && !course.title.empty()) {
            bst->Insert(course);
        }
    }
    file.close();
}

/**
 * Default constructor
 */
BinarySearchTree::BinarySearchTree() {
    root = nullptr;
}

/**
 * Destructor
 */
BinarySearchTree::~BinarySearchTree() {
    destroyTree(root);  
}
//recursive deletion of bst 
void BinarySearchTree::destroyTree(Node* node) {
    if (node == nullptr) {
        return;
    }
    else{
        destroyTree(node->left);
        destroyTree(node->right);
        delete node;
    }
}

void BinarySearchTree::InOrder() {
    inOrder(root);
}

void BinarySearchTree::PostOrder() {
    postOrder(root);
}

void BinarySearchTree::PreOrder() {
    preOrder(root);
}

void BinarySearchTree::Insert(Course course) {
    if (root == nullptr) {
        root = new Node(course);
    }

    else {
        addNode(root, course);
    }

}

Course BinarySearchTree::Search(string courseId) {
    Node* currNode = root;
    while (currNode != nullptr){
        if (currNode->course.courseId == courseId){
            return currNode->course;
        }
        else if (currNode->course.courseId > courseId) {
            currNode = currNode->left;
        }
        else if (currNode->course.courseId < courseId) {
            currNode = currNode->right;
        }
    }
        
        
    Course course;
    return course;
}

void BinarySearchTree::addNode(Node* node, Course course) {
    if (node->course.courseId > course.courseId) {
        if (node->left == nullptr){
            node->left = new Node(course);
        }
        else {
            addNode(node->left, course);
        }
    }

    else{
        if (node->right == nullptr){
            node->right = new Node(course);
        }

        else {
            addNode(node->right, course);
        }
    }
}
void BinarySearchTree::inOrder(Node* node) {
      if (node != nullptr){
        inOrder(node->left);
        displayCourse(node->course);
        inOrder(node->right);
      }
}
void BinarySearchTree::postOrder(Node* node) {
    if (node != nullptr){
    postOrder(node->left);
    postOrder(node->right);
    displayCourse(node->course);
    }

}

void BinarySearchTree::preOrder(Node* node) {
    if (node != nullptr){
    displayCourse(node->course);
    preOrder(node->left);
    preOrder(node->right);
    }    
}

void displayCourse(Course course) {
    cout << course.courseId << ": " << course.title << endl;

    if (!course.prereq.empty()) {
        cout << endl << "Prerequisites: ";
        for (size_t i = 0; i < course.prereq.size(); ++i) {
            cout << course.prereq[i];
            if (i < course.prereq.size() - 1) {
                cout << ", ";
            }
        }
    }
    cout << endl;
}


int main() {
    BinarySearchTree* bst = new BinarySearchTree();
    string fileName;
    int choice = 0;

    while (choice != 9) {
        cout << "Menu: " << endl;
        cout << "1. Load Course Data" << endl;
        cout << "2. Print Course List" << endl;
        cout << "3. Print Course Information" << endl;
        cout << "9. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;

        switch(choice) {
            case 1:
                cout << "Enter file name: ";
                cin >> fileName;
                loadCrs(fileName, bst);
                break;
            case 2:
                bst->InOrder();
                break;
            case 3: {
                cout << "Enter Course ID: ";
                string courseId;
                cin >> courseId;
                Course course = bst->Search(courseId);
                if (!course.courseId.empty()) {
                    displayCourse(course);
                }
                else {
                    cout << "Course " << courseId << " not found." <<endl;
                }
                break;
            }
            default:
                cout << "Invalid choice" << endl;
                break;

        }
    }

    delete bst;
    return 0;
}