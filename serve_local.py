import http.server
import socketserver
import webbrowser
import argparse
from pathlib import Path


def serve(port: int = 8000, open_browser: bool = True):
    root = Path('.').resolve()
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/index.html"
        print(f"Serving {root} at {url}")
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serve the current directory over HTTP')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on')
    parser.add_argument('--no-open', action='store_true', help="Don't open the browser automatically")
    args = parser.parse_args()
    serve(args.port, not args.no_open)
