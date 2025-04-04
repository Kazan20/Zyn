class Shell:
    def __init__(self):
        self.commands = {
            "echo": self.echo,
            "exit": self.exit_shell,
            # Add more commands here
        }

    def execute(self, command):
        cmd_parts = command.split()
        if cmd_parts[0] in self.commands:
            return self.commands[cmd_parts[0]](cmd_parts[1:])
        else:
            return f"Command '{cmd_parts[0]}' not found."

    def echo(self, args):
        return " ".join(args)

    def exit_shell(self, args):
        return "Exiting shell..."

if __name__ == "__main__":
    shell = Shell()
    while True:
        command = input(">>> ")
        output = shell.execute(command)
        print(output)
        if output == "Exiting shell...":
            break
