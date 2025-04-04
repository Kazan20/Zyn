#include "window_manager.h"
#include "terminal.h"
#include "settings.h"

int main() {
    WindowManager windowManager;

    Terminal terminal;
    Settings settings;

    windowManager.addWindow("Terminal", &terminal);
    windowManager.addWindow("Settings", &settings);

    windowManager.run();
    return 0;
}
