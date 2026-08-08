#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "AVLTree.h"

namespace {

// Strips leading and trailing whitespace
std::string trim(const std::string& text) {
    const std::string blanks = " \t\r\n";
    const std::size_t first = text.find_first_not_of(blanks);
    if (first == std::string::npos) {
        return "";
    }
    const std::size_t last = text.find_last_not_of(blanks);
    return text.substr(first, last - first + 1);
}

// Parses one CSV row: courseId,title[,prereq...]
// Returns an empty Course if the row has no id or no title.
Course parseRow(const std::string& line) {
    std::stringstream row(line);
    std::string field;
    Course course;

    if (std::getline(row, field, ',')) {
        course.courseId = trim(field);
    }
    if (std::getline(row, field, ',')) {
        course.title = trim(field);
    }
    while (std::getline(row, field, ',')) {
        const std::string prereq = trim(field);
        if (!prereq.empty()) {
            course.prereq.push_back(prereq);
        }
    }

    if (course.courseId.empty() || course.title.empty()) {
        return Course();
    }
    return course;
}

bool loadCourses(const std::string& path, AVLTree& tree) {
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cout << "Could not open '" << path
                  << "'. Check the name and the working directory.\n";
        return false;
    }

    int read = 0;
    int loaded = 0;
    int skipped = 0;
    int duplicates = 0;
    std::string line;

    while (std::getline(file, line)) {
        ++read;
        if (trim(line).empty()) {
            ++skipped;
            continue;
        }

        const Course course = parseRow(line);
        if (course.empty()) {
            ++skipped;
            continue;
        }

        // Duplicate policy: first record is kept
        if (tree.insert(course)) {
            ++loaded;
        } else {
            ++duplicates;
        }
    }

    std::cout << "Loaded " << loaded << " of " << read << " rows.\n";
    if (skipped > 0) {
        std::cout << "  " << skipped << " blank or malformed row(s) skipped.\n";
    }
    if (duplicates > 0) {
        std::cout << "  " << duplicates << " duplicate id(s) rejected.\n";
    }
    return loaded > 0;
}

void displayCourse(const Course& course) {
    std::cout << course.courseId << ": " << course.title << "\n";
    if (!course.prereq.empty()) {
        std::cout << "  Prerequisites: ";
        for (std::size_t i = 0; i < course.prereq.size(); ++i) {
            std::cout << (i == 0 ? "" : ", ") << course.prereq[i];
        }
        std::cout << "\n";
    }
}

void printMenu() {
    std::cout << "\nABCU Course Advising\n"
              << "  1. Load course data\n"
              << "  2. Print course list\n"
              << "  3. Print course information\n"
              << "  9. Exit\n"
              << "Enter choice: ";
}

// Reads a whole line so a non-numeric entry cannot leave cin in a failed state
bool readChoice(int& choice) {
    std::string line;
    if (!std::getline(std::cin, line)) {
        return false;
    }
    std::istringstream parser(line);
    if (!(parser >> choice)) {
        choice = -1;
    }
    return true;
}

bool readLine(const std::string& prompt, std::string& value) {
    std::cout << prompt;
    return static_cast<bool>(std::getline(std::cin, value));
}

void handleLoad(AVLTree*& catalog) {
    std::string path;
    if (!readLine("Enter file name: ", path)) {
        return;
    }

    // Loading into a fresh tree keeps a failed load from leaving a half
    // populated catalog behind.
    AVLTree* loading = new AVLTree();
    if (!loadCourses(trim(path), *loading)) {
        delete loading;
        std::cout << "Catalog unchanged.\n";
        return;
    }

    delete catalog;
    catalog = loading;

    std::cout << "Catalog ready: " << catalog->size() << " courses, tree height "
              << catalog->height() << ".\n";
}

void handleList(const AVLTree* catalog) {
    if (catalog == nullptr) {
        std::cout << "Load course data first (option 1).\n";
        return;
    }
    catalog->inOrder(displayCourse);
}

void handleFind(const AVLTree* catalog) {
    if (catalog == nullptr) {
        std::cout << "Load course data first (option 1).\n";
        return;
    }

    std::string courseId;
    if (!readLine("Enter course ID: ", courseId)) {
        return;
    }

    const Course course = catalog->search(trim(courseId));
    if (course.empty()) {
        std::cout << "Course " << courseId << " not found.\n";
        return;
    }
    displayCourse(course);
}

}

int main() {
    AVLTree* catalog = nullptr;
    int choice = 0;

    while (true) {
        printMenu();
        if (!readChoice(choice)) {
            break; 
        }

        if (choice == 9) {
            std::cout << "Goodbye.\n";
            break;
        }

        switch (choice) {
            case 1:
                handleLoad(catalog);
                break;
            case 2:
                handleList(catalog);
                break;
            case 3:
                handleFind(catalog);
                break;
            default:
                std::cout << choice << " is not a valid option.\n";
                break;
        }
    }

    delete catalog;
    return 0;
}
