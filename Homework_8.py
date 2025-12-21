from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json


TOKEN = "OAuth _"   #Вместо _ должен быть ваш токен

def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def get_uploaded_file():
    response = get(f"https://cloud-api.yandex.net/v1/disk/resources?path=Backup",   #На вашем диске должна быть создана папка Backup
                   headers={"Authorization": TOKEN})
    data = response.json()

    if "_embedded" not in data:
        return set()
    
    return {item["name"] for item in data["_embedded"]["items"]}


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        uploaded_files = get_uploaded_file()

        def fname2html(fname):
            style = ""
            if fname in uploaded_files:
                style = "style='background-color: rgba(0, 200, 0, 0.25);'"

            return f"""
                <li {style}
                    onclick="fetch('/upload', {{'method': 'POST', 'headers': {{'Content-Type': 'text/plain'}},'body': '{fname}'}})">
                    {fname}
                </li>
            """

        files_html = "".join(
            fname2html(fname) for fname in os.listdir("pdfs"))  #В одной папке с этим файлом должна быть папка pdfs, в которой файлы .pdf
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"""
            <html>
                <body>
                    <ul>
                        {files_html}
                    </ul>
                </body>
            </html>
        """.encode("utf-8"))

    def do_POST(self):
        if self.path != "/upload":
            self.send_response(404)
            self.end_headers()
            return
        
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"Backup/{fname}"
        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                   headers={"Authorization": TOKEN})
        upload_url = resp.json()['href']

        with open(local_path, 'rb') as f:
            put(upload_url, files={'file': (fname, f)})

        self.send_response(200)
        self.end_headers()


run(handler_class=HttpGetHandler)