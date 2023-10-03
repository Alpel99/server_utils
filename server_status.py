import json, psutil, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from shutdown_query import checkAll, reslist

# Specify the IP address and port for the server to listen on
host = "0.0.0.0"
port = 8080

# Create a custom request handler class that inherits from BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        checkAll()
        # Create a JSON object
        # data = {"message": "Hello, this is your JSON response!"}

        res_uptime = subprocess.run(['/usr/bin/uptime'], capture_output=True)
        r = str(res_uptime.stdout, 'UTF-8').strip()
        # r = "16:20:00 up 30 min,  1 user,  load average: 0.01, 0.02, 0.02"
        splits = r.split(',', 2)
        data = {}
        data["uptime"] = splits[0]
        data["users"] = splits[1].strip()
        data["load"] = splits[2].split(':')[1].strip()
        data["reslist"] = reslist
        data["cpu_percent"] = psutil.cpu_percent()
        data["ram_percent"] = psutil.virtual_memory().percent
        
        # Convert the JSON object to a JSON-encoded string
        json_str = json.dumps(data)

        # Send the response headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Write the JSON-encoded string to the response
        self.wfile.write(json_str.encode("utf-8"))

# Create an instance of the HTTP server with your custom request handler
httpd = HTTPServer((host, port), MyHandler)

if __name__ == "__main__":
    try:
        print(f"Server listening on {host}:{port}")
        # Start the server
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        httpd.server_close()
