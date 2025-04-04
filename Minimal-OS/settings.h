#ifndef SETTINGS_H
#define SETTINGS_H

#include "window.h"

class Settings : public Window {
public:
    Settings();
    void render() const override;
};

#endif // SETTINGS_H
