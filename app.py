import glob
import os
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

WORKING_DIR = sys.argv[1]


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, Path:", self.path)

        now = datetime.now()
        day_dir = now.strftime("%Y%m" + os.sep + "%d" + os.sep + "%H")

        list_of_files = glob.glob(WORKING_DIR + day_dir + '**\*.jpg', recursive=True)
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        self.send_response(200)
        self.send_header('Content-type', 'image/jpg')
        self.end_headers()
        with open(latest_file, 'rb') as file:
            self.wfile.write(file.read())


def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    port = 8090
    print("Starting server at port %d" % port)
    print("Working dir %s" % WORKING_DIR)
    server_thread(port)
