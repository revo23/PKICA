#!/usr/bin/env python3
"""Simple HTTPS server using our PKI certificates."""

import http.server
import ssl
import os

PORT = 8443
CERT_FILE = "server/server.cert.pem"
KEY_FILE = "server/server.key.pem"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>PKI Lab - HTTPS Server</title></head>
        <body>
            <h1>🔐 Secure Connection Established!</h1>
            <p>This page is served over HTTPS using:</p>
            <ul>
                <li><strong>Server Certificate:</strong> Issued by MyLab Root CA</li>
                <li><strong>Common Name:</strong> localhost</li>
                <li><strong>Port:</strong> 8443</li>
            </ul>
            <p>Your connection is encrypted with TLS!</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, MyHandler)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_FILE, KEY_FILE)

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"HTTPS server running at https://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    print()
    print("To test with curl (trusting our CA):")
    print(f"  curl --cacert ca/certs/ca.cert.pem https://localhost:{PORT}")
    print()
    print("Or in browser (will show certificate warning since CA is not trusted by OS)")

    httpd.serve_forever()

if __name__ == "__main__":
    main()
