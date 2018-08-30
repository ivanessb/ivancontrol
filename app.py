#see: https://gist.github.com/bsingr/a5ef6834524e82270154a9a72950c842 (http-json-echo.py)
#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
StoredData = 'Empty'
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        global StoredData
        if data["HTTP POST Request from"] == "IFTTT":
            StoredData = data
            self.wfile.write(json.dumps({
                'Response': 'Received'
                }).encode())
        if data["HTTP POST Request from"] == "STM32":
            self.wfile.write(json.dumps({
                'Stored data': StoredData
                }).encode())
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()
