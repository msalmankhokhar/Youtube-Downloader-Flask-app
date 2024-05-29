import webview
from app import app

window = webview.create_window('V Downloader', app)

if __name__ == '__main__':
    webview.start()