import tkinter as tk

class WindowManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My OS Desktop")
        self.windows = []

    def create_window(self, title="New Window", content_class=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("400x300")
        if content_class:
            content_class(window)  # Instantiate the class and pass the window as its master
        self.windows.append(window)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    wm = WindowManager()
    wm.create_window("Welcome to My OS")
    wm.run()
