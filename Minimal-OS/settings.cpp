#include "settings.h"
#include <iostream>

Settings::Settings() : Window("Settings") {}

void Settings::render() const {
    Window::render();  // Call the base class render method
    if (!isClosed()) {
        std::cout << "| Settings Panel\n";
        std::cout << "| 1. Change display settings\n";
        std::cout << "| 2. Change system settings\n";
        std::cout << "| 3. Network settings\n";
    }
}
