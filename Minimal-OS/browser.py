import webview

class Browser:
    def __init__(self, url="https://www.google.com"):
        self.url = url

    def open(self):
        webview.create_window("My OS Browser", self.url)
        webview.start()

if __name__ == "__main__":
    browser = Browser()
    browser.open()
