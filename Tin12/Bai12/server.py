#!/usr/bin/env python3
"""
BACKEND PYTHON SERVER - Bài 12: Tạo biểu mẫu (Tin học 12 • THTH-DHSP)
Chạy: python3 server.py (mặc định Port 3012)
"""
import http.server
import socketserver
import json
import os
import urllib.parse
import re
import unicodedata
import subprocess

PORT = int(os.environ.get('PORT', 3012))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CURRENT_DIR, 'data', 'submissions.json')
SHEETS_DIR = os.path.join(CURRENT_DIR, 'data', 'sheets')
HD3_DIR = os.path.join(CURRENT_DIR, 'data', 'submissions_hd3')
HD3_DATA_FILE = os.path.join(CURRENT_DIR, 'data', 'submissions_hd3.json')

os.makedirs(SHEETS_DIR, exist_ok=True)
os.makedirs(HD3_DIR, exist_ok=True)
for fp in (DATA_FILE, HD3_DATA_FILE):
    if not os.path.exists(fp):
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump([], f)

TEACHER_PASSWORDS = {'darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4'}


def read_json(fp):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def write_json(fp, data):
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clean_name(text):
    if not text:
        return 'HocSinh'
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    return re.sub(r'_+', '_', text)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def _clean_path(self):
        p = urllib.parse.urlparse(self.path).path
        pref = '/api/bai12'
        if p.startswith(pref + '/'):
            return '/api/' + p[len(pref) + 1:]
        if p == pref:
            return '/api'
        return p

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        cp = self._clean_path()
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length else '{}'
        data = json.loads(body)

        if cp == '/api/auth/login':
            if str(data.get('password', '')).strip() in TEACHER_PASSWORDS:
                self.send_response(200)
                self.send_header('Set-Cookie', 'thth_teacher=1; Path=/; SameSite=Lax')
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'authenticated': True, 'name': 'Nguyễn Lê Minh Ngọc'}).encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'{"authenticated": false}')
            return

        if cp == '/api/submit':
            lst = read_json(DATA_FILE)
            lst.insert(0, data)
            write_json(DATA_FILE, lst)
            fn = f"{data.get('worksheetId','phieu')}_{clean_name(data.get('className','12A'))}_{clean_name(data.get('studentName'))}.json"
            with open(os.path.join(SHEETS_DIR, fn), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'total': len(lst)}).encode('utf-8'))
            return

        if cp == '/api/reset':
            write_json(DATA_FILE, [])
            for f in os.listdir(SHEETS_DIR):
                os.remove(os.path.join(SHEETS_DIR, f))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"reset_ok"}')
            return

        if cp == '/api/submit-hd3':
            fn = f"{clean_name(data.get('className','12A'))}_{clean_name(data.get('studentNumber','May00'))}_{clean_name(data.get('studentName'))}_dang_ki_thi.html"
            data['filename'] = fn
            with open(os.path.join(HD3_DIR, fn), 'w', encoding='utf-8') as f:
                f.write(data.get('code', ''))
            lst = read_json(HD3_DATA_FILE)
            lst.insert(0, data)
            write_json(HD3_DATA_FILE, lst)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'filename': fn}).encode('utf-8'))
            return

        if cp == '/api/reset-hd3':
            write_json(HD3_DATA_FILE, [])
            for f in os.listdir(HD3_DIR):
                if f.endswith('.html'):
                    os.remove(os.path.join(HD3_DIR, f))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"reset_hd3_ok"}')
            return

        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        cp = self._clean_path()
        if cp == '/api/submissions':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(read_json(DATA_FILE), ensure_ascii=False).encode('utf-8'))
            return
        if cp == '/api/submissions-hd3':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(read_json(HD3_DATA_FILE), ensure_ascii=False).encode('utf-8'))
            return
        if cp == '/api/submissions-hd3-zip':
            subprocess.run(['python3', 'create_submissions_zip.py'], cwd=CURRENT_DIR, check=False)
            zp = os.path.join(CURRENT_DIR, 'Bai12_HD3_TatCaBaiLam_THTH_DHSP.zip')
            if os.path.exists(zp):
                with open(zp, 'rb') as f:
                    raw = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="Bai12_HD3_TatCaBaiLam_THTH_DHSP.zip"')
                self.end_headers()
                self.wfile.write(raw)
                return
        if '.private.' in cp or cp.startswith('/data/') or '/data/' in cp:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'403 Forbidden')
            return
        if cp.endswith('.docx') or cp.endswith('.pptx'):
            if 'thth_teacher=1' not in self.headers.get('Cookie', ''):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'403 Forbidden')
                return
        super().do_GET()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'Bài 12: Tạo biểu mẫu Python server on http://localhost:{PORT}')
        httpd.serve_forever()
