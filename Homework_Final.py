from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

taska_file = 'tasks.txt'
TASKS = []
NEXT_ID = 1

class TaskHandler(BaseHTTPRequestHandler):
    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except:
            return None
        
    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_empty (self, status = 200):
        self.send_response(status)
        self.end_headers()

    def _error(self, status, msg):
        self._send_json({"error": msg}, status=status)

    def _save_tasks(self):
        with open(taska_file, 'w', encoding='utf-8') as file_write:
            json.dump(TASKS, file_write, ensure_ascii=False)


    def do_POST(self):
        parsed = urlparse(self.path)
        parts = [part for part in parsed.path.split('/') if part]
        if parsed.path == '/tasks':
            self.create_task()
        elif len(parts) == 3 and parts[0] == 'tasks' and parts[2] == 'complete':
            self.complete_task(parts[1])
        else:
            self._error(404, "Not found")

    def do_GET(self):        
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "":
            self.send_response(200)
            # self.send_header("Content-Type", "text")
            self.end_headers()

        elif parsed.path == "/tasks":
            self.list_tasks()
        else:
            self._error(404, "Not found")


    def create_task(self):
        global NEXT_ID 
        data = self._read_json_body()
        if not data or "title" not in data or "priority" not in data:
            return self._error(400, "Field 'title' or 'priority' is required")

        priority = data['priority']
        if priority not in ('low', 'normal', 'high'):
            return self._error(400, "'Priority' must be 'low', 'normal' or 'high'")
        
        task = {
            'title': data['title'],
            'priority': priority,
            'isDone': False,
            'id': NEXT_ID
        }
        TASKS.append(task)
        NEXT_ID += 1
        self._save_tasks()
        self._send_json(task, 201)

    def list_tasks(self):
        self._send_json(TASKS)

    def complete_task(self, task_id):
        try:
            task_id = int(task_id)
        except:
            return self._error(400, "Task id must be integer")
        for task in TASKS:
            if task["id"] == task_id:
                task['isDone'] = True
                self._save_tasks()
                return self._send_empty()
        self._send_empty(404)


def loadtasks():
    global TASKS, NEXT_ID
    if os.path.exists(taska_file):
        with open(taska_file, 'r', encoding='utf-8') as file_read:
            TASKS = json.load(file_read)
        if TASKS:
            NEXT_ID = 1 + max(task['id'] for task in TASKS)


def run(host="127.0.0.1", port=8000):
    loadtasks()
    print(f"Serving on http://{host}:{port}")
    print(f"Loaded {len(TASKS)} tasks from {taska_file}")
    server = HTTPServer((host, port), TaskHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.server_close()

if __name__ == "__main__":
    run()
