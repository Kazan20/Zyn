import socket
import tkinter as tk
from PIL import Image, ImageTk
import io
import pickle
import threading
import struct

class ViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deck PC Viewer")
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(('localhost', 9999))
            self.receive_images()
        except Exception as e:
            print(f"Client Error: {e}")
            self.root.quit()

    def receive_images(self):
        def receive():
            while True:
                try:
                    # Receive length of the data first
                    data_length = self._recvall(4)
                    if not data_length:
                        break
                    data_length = struct.unpack('I', data_length)[0]

                    # Receive the actual data
                    screenshot_bytes = self._recvall(data_length)
                    if not screenshot_bytes:
                        break

                    screenshot = pickle.loads(screenshot_bytes)
                    img = ImageTk.PhotoImage(image=screenshot)
                    self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
                    self.root.update_idletasks()
                except Exception as e:
                    print(f"Receiving Error: {e}")
                    self.socket.close()
                    break

        threading.Thread(target=receive).start()

    def _recvall(self, length):
        data = b''
        while len(data) < length:
            packet = self.socket.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data

if __name__ == "__main__":
    root = tk.Tk()
    app = ViewerApp(root)
    root.mainloop()
