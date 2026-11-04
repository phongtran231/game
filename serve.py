import mimetypes
mimetypes.add_type("application/wasm", ".wasm")
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ArcadeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Crucial headers required for Nostalgist / RetroArch WASM SharedArrayBuffer
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ArcadeHTTPRequestHandler) as httpd:
        print(f"=======================================================")
        print(f" COIN-OPX Arcade Server running at http://localhost:{PORT}")
        print(f" Press Ctrl+C to stop.")
        print(f"=======================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
