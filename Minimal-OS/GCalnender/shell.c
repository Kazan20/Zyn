#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>

// Function to list files in the current directory
void ls() {
    struct dirent *entry;
    DIR *dp = opendir(".");

    if (dp == NULL) {
        perror("opendir");
        return;
    }

    while ((entry = readdir(dp))) {
        printf("%s\n", entry->d_name);
    }

    closedir(dp);
}

// Function to change the current working directory
void cs(const char *path) {
    if (chdir(path) != 0) {
        perror("chdir");
    }
}

int main() {
    char command[256];
    char *cmd;
    char *arg;

    while (1) {
        printf("chroot> ");
        if (fgets(command, sizeof(command), stdin) == NULL) {
            perror("fgets");
            continue;
        }

        // Remove newline character from the end of the command
        command[strcspn(command, "\n")] = 0;

        // Parse the command
        cmd = strtok(command, " ");
        arg = strtok(NULL, " ");

        if (cmd != NULL) {
            if (strcmp(cmd, "cs") == 0 && arg != NULL) {
                cs(arg);
            } else if (strcmp(cmd, "ls") == 0) {
                ls();
            } else {
                printf("Unknown command: %s\n", cmd);
            }
        }
    }

    return 0;
}
