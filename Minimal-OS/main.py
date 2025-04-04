import tkinter as tk
from tkinter import PhotoImage
import webview

class WindowManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My OS Desktop")
        self.root.geometry("800x600")
        self.windows = []

    def create_window(self, title="New Window", content_class=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x300")
        if content_class:
            content_class(window)
        self.windows.append(window)

    def run(self):
        self.root.mainloop()


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

class Browser:
    def __init__(self, url="https://www.google.com"):
        self.url = url

    def open(self):
        webview.create_window("My OS Browser", self.url)
        webview.start()

if __name__ == "__main__":
    browser = Browser()



class MyOS:
    def __init__(self):
        self.wm = WindowManager()
        self.create_desktop()

    def create_desktop(self):
        # Add app icons to the desktop
        desktop_frame = tk.Frame(self.wm.root)
        desktop_frame.pack(expand=True, fill=tk.BOTH)

        # Load images for the icons (replace with actual paths)
        terminal_icon = PhotoImage(file="terminal_icon.png")
        browser_icon = PhotoImage(file="browser_icon.png")

        # Create buttons for the apps
        terminal_button = tk.Button(desktop_frame, image=terminal_icon, text="Terminal",
                                    compound=tk.TOP, command=self.launch_terminal)
        terminal_button.image = terminal_icon  # Keep a reference to avoid garbage collection
        terminal_button.grid(row=0, column=0, padx=20, pady=20)

        browser_button = tk.Button(desktop_frame, image=browser_icon, text="Browser",
                                   compound=tk.TOP, command=self.launch_browser)
        browser_button.image = browser_icon  # Keep a reference to avoid garbage collection
        browser_button.grid(row=0, column=1, padx=20, pady=20)

    def launch_terminal(self):
        self.wm.create_window("Terminal", Terminal)

    def launch_browser(self):
        self.wm.create_window("Browser", Browser)

    def run(self):
        self.wm.run()


if __name__ == "__main__":
    os = MyOS()
    os.run()
