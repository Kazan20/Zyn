#ifndef TERMINAL_H
#define TERMINAL_H

#include "window.h"

class Terminal : public Window {
public:
    Terminal();
    void render() const override;
};

#endif // TERMINAL_H
