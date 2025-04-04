#ifndef WINDOW_MANAGER_H
#define WINDOW_MANAGER_H

#include <vector>
#include <string>
#include <map>
#include "window.h"

class WindowManager {
public:
    void addWindow(const std::string& title, Window* window);
    void run();  // Main loop to manage windows and handle input

private:
    std::map<std::string, Window*> windows;
    std::string currentWindow;  // Track the currently active window

    void renderWindows();  // Render all windows
    void handleInput();    // Handle user input for the current window
};

#endif // WINDOW_MANAGER_H
