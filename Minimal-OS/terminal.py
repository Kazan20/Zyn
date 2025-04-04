import tkinter as tk

class Terminal:
    def __init__(self, master):
        self.terminal = tk.Text(master, bg="black", fg="white", insertbackground="white")
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal.insert(tk.END, "Welcome to My OS Terminal\n")
        self.terminal.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.get_command()
        self.terminal.insert(tk.END, f"\nExecuting: {command}\n")
        # Add command handling logic here

    def get_command(self):
        return self.terminal.get("end-2c linestart", "end-1c")

if __name__ == "__main__":
    root = tk.Tk()
    terminal = Terminal(root)
    root.mainloop()
