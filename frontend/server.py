#!/usr/bin/env python3
import http.server
import socketserver
import mimetypes

# Adicionar MIME type para módulos JavaScript
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/javascript', '.js')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Servidor rodando na porta {PORT}")
        print(f"Acesse: http://localhost:{PORT}/src/d3.html")
        httpd.serve_forever()