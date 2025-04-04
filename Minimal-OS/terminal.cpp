#include "terminal.h"
#include <iostream>

Terminal::Terminal() : Window("Terminal") {}

void Terminal::render() const {
    Window::render();  // Call the base class render method
    if (!isClosed()) {
        std::cout << "| This is a basic terminal.\n";
        std::cout << "| You can execute commands here.\n";
    }
}
