#include "window.h"
#include <iostream>

Window::Window(const std::string& title) : title(title), state(VISIBLE) {}

void Window::render() const {
    if (state == CLOSED) return;

    std::cout << "=====================================\n";
    std::cout << "| " << title << (state == EXPANDED ? " [EXPANDED]" : "") << "\n";
    std::cout << "=====================================\n";
    if (state == HIDDEN) {
        std::cout << "| [Window is hidden]\n";
    } else {
        std::cout << "| 1. Hide Window\n";
        std::cout << "| 2. Expand Window\n";
        std::cout << "| 3. Close Window\n";
    }
    std::cout << "=====================================\n";
}

void Window::handleInput(int choice) {
    switch (choice) {
        case 1: state = HIDDEN; break;
        case 2: state = EXPANDED; break;
        case 3: state = CLOSED; break;
        default: break;
    }
}

bool Window::isClosed() const {
    return state == CLOSED;
}

const std::string& Window::getTitle() const {
    return title;
}
