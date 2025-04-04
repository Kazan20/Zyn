#include "window_manager.h"
#include <iostream>
#include <map>
#include <conio.h>  // For _getch() to handle input

void WindowManager::addWindow(const std::string& title, Window* window) {
    windows[title] = window;
    if (currentWindow.empty()) {
        currentWindow = title;  // Set the first added window as the current one
    }
}

void WindowManager::run() {
    while (true) {
        renderWindows();
        handleInput();  // Process input for the current window

        // Break the loop if all windows are closed
        bool allClosed = true;
        for (std::map<std::string, Window*>::iterator it = windows.begin(); it != windows.end(); ++it) {
            if (!it->second->isClosed()) {
                allClosed = false;
                break;
            }
        }
        if (allClosed) break;
    }
}

void WindowManager::renderWindows() {
    system("cls");  // Clear the screen (Windows-specific)
    for (std::map<std::string, Window*>::iterator it = windows.begin(); it != windows.end(); ++it) {
        if (!it->second->isClosed()) {
            it->second->render();  // Render each window that's not closed
        }
    }
    std::cout << "Current Window: " << currentWindow << "\n";
    std::cout << "Press Tab to switch windows, or enter a choice for the current window.\n";
}

void WindowManager::handleInput() {
    char key = _getch();  // Get a single keypress from the user

    if (key == '\t') {  // Tab key switches between windows
        std::map<std::string, Window*>::iterator it = windows.find(currentWindow);
        do {
            if (++it == windows.end()) {
                it = windows.begin();  // Wrap around to the first window
            }
        } while (it->second->isClosed());  // Skip closed windows

        currentWindow = it->first;  // Set the new active window
    } else {
        int choice = key - '0';  // Convert the character to an integer (0-9)
        if (choice >= 1 && choice <= 3) {
            windows[currentWindow]->handleInput(choice);  // Handle the choice for the current window
        }
    }
}
