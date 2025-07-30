"""
webtask HTTP Server
"""

import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class WebTaskHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for webtask"""
    def __init__(self, *args, **kwargs):
        static_dir = Path(__file__).parent / "static"
        super().__init__(*args, directory=str(static_dir), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        pass


class webtaskServer:
    """webtask server wrapper"""
    def __init__(self, host="localhost", port=8000, open_browser=True):
        self.host = host
        self.port = port
        self.open_browser = open_browser
        self.server = None

    def run(self):
        try:
            self.server = HTTPServer((self.host, self.port), WebTaskHandler)
            url = f"http://{self.host}:{self.port}"
            print(f"🚀 Starting webtask server at {url}")
            print("📊 webtask is running! Press Ctrl+C to stop.")
            if self.open_browser:
                threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            self.server.serve_forever()
        except OSError as e:
            if hasattr(e, 'errno') and e.errno in (48, 98):
                print(f"❌ Port {self.port} is already in use. Try a different port with --port")
            else:
                raise
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self.server:
            print("\n🛑 Stopping webtask server...")
            self.server.shutdown()
            self.server.server_close()