#ifndef WINDOW_H
#define WINDOW_H

#include <string>

class Window {
public:
    enum State { VISIBLE, HIDDEN, EXPANDED, CLOSED };

    Window(const std::string& title);

    virtual void render() const;
    void handleInput(int choice);
    bool isClosed() const;

    const std::string& getTitle() const;

private:
    std::string title;
    State state;
};

#endif // WINDOW_H
