#!/usr/bin/env python3
"""
BACKEND SERVER PYTHON SIÊU NHẸ - BÀI 8 TIN HỌC 12 (THTH-DHSP)
Dùng module chuẩn của Python (http.server, json, os, urllib) - KHÔNG CẦN CÀI THÊM THƯ VIỆN!

Cách chạy:
    python3 server.py
Mở trình duyệt: http://localhost:3000
"""

import http.server
import socketserver
import json
import os
import urllib.parse
import mimetypes
import time

PORT = int(os.environ.get('PORT', 3000))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
DATA_FILE = os.path.join(CURRENT_DIR, 'data', 'submissions.json')
SHEETS_DIR = os.path.join(CURRENT_DIR, 'data', 'sheets')
HD3_DIR = os.path.join(CURRENT_DIR, 'data', 'submissions_hd3')
HD3_DATA_FILE = os.path.join(CURRENT_DIR, 'data', 'submissions_hd3.json')

# Khởi tạo thư mục và file data
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(SHEETS_DIR, exist_ok=True)
os.makedirs(HD3_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
if not os.path.exists(HD3_DATA_FILE):
    with open(HD3_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def get_submissions():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Lỗi đọc submissions.json:", e)
        return []

def save_submissions(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Lỗi ghi submissions.json:", e)
        return False

def get_hd3_submissions():
    try:
        with open(HD3_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Lỗi đọc submissions_hd3.json:", e)
        return []

def save_hd3_submissions(data):
    try:
        with open(HD3_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Lỗi ghi submissions_hd3.json:", e)
        return False

import re
import unicodedata

def sanitize_filename(text):
    if not text:
        return "HocSinh"
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    return re.sub(r'_+', '_', text)

class ClassroomRequestHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/api/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                student_name = payload.get('studentName')
                class_name = payload.get('className')
                if not student_name or not class_name:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Thiếu họ tên hoặc lớp'}).encode('utf-8'))
                    return

                submissions = get_submissions()
                worksheet_id = payload.get('worksheetId', 'phieu1')
                worksheet_title = payload.get('worksheetTitle', 'Phiếu bài tập số 2' if worksheet_id == 'phieu2' else 'Phiếu bài tập số 1')
                new_record = {
                    'id': payload.get('id', 'MD-' + str(int(time.time() * 1000) % 9000 + 1000)),
                    'worksheetId': worksheet_id,
                    'worksheetTitle': worksheet_title,
                    'isPair': payload.get('isPair', False),
                    'studentName': student_name,
                    'student1': payload.get('student1'),
                    'student2': payload.get('student2'),
                    'className': class_name,
                    'studentNumber': payload.get('studentNumber', 'N/A'),
                    'score': payload.get('score', 0),
                    'maxScore': payload.get('maxScore', 10.0),
                    'answers': payload.get('answers', {}),
                    'results': payload.get('results', {}),
                    'submittedAt': payload.get('submittedAt', time.strftime('%H:%M:%S - %d/%m/%Y')),
                    'timestamp': int(time.time() * 1000)
                }
                submissions.insert(0, new_record)
                save_submissions(submissions)

                # Lưu riêng từng phiếu bài làm của học sinh thành một file độc lập
                try:
                    sheet_file = os.path.join(SHEETS_DIR, f"{new_record['id']}.json")
                    with open(sheet_file, 'w', encoding='utf-8') as f:
                        json.dump(new_record, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print("Lỗi lưu file sheet đơn lẻ:", e)

                print(f"[SUBMIT - {worksheet_title}] {student_name} ({class_name}) - Điểm: {new_record['score']} (Đã lưu phiếu {new_record['id']}.json)")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': new_record}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
            return

        elif path == '/api/submit-hd3':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                student_name = payload.get('studentName')
                class_name = payload.get('className')
                if not student_name or not class_name:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Thiếu họ tên hoặc lớp'}).encode('utf-8'))
                    return

                hd3_id = 'HD3-' + str(int(time.time() * 1000) % 9000 + 1000)
                safe_class = sanitize_filename(class_name)
                safe_machine = sanitize_filename(payload.get('studentNumber', 'May00'))
                safe_name = sanitize_filename(student_name)
                file_prefix = f"{safe_class}_{safe_machine}_{safe_name}"

                def wrap_html(title, code):
                    if not code:
                        code = '<p style="color:#94a3b8; font-style:italic;">(Chưa có nội dung bài làm)</p>'
                    if '<!DOCTYPE' in code or '<html' in code:
                        return code
                    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - {student_name} ({class_name})</title>
  <style>
    body {{
      font-family: 'Times New Roman', serif;
      padding: 24px;
      line-height: 1.6;
      color: #0f172a;
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
    }}
    .student-badge-header {{
      background: #f1f5f9;
      border-left: 4px solid #2563eb;
      padding: 10px 16px;
      border-radius: 6px;
      margin-bottom: 24px;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: 0.9rem;
      color: #334155;
    }}
  </style>
</head>
<body>
  <div class="student-badge-header">
    <strong>🏫 THTH - DHSP - TIN HỌC 12</strong><br>
    <strong>Học sinh:</strong> {student_name} &nbsp;|&nbsp; 
    <strong>Lớp:</strong> {class_name} &nbsp;|&nbsp; 
    <strong>Máy:</strong> {payload.get('studentNumber', 'N/A')} &nbsp;|&nbsp;
    <strong>Nộp lúc:</strong> {payload.get('submittedAt', '')}
  </div>
  {code}
</body>
</html>"""

                bai1_file = f"{file_prefix}_Bai1.html"
                bai2_file = f"{file_prefix}_Bai2.html"
                bai3_file = f"{file_prefix}_Bai3.html"

                with open(os.path.join(HD3_DIR, bai1_file), 'w', encoding='utf-8') as f:
                    f.write(wrap_html('Bài 1: Phương trình bậc 2', payload.get('bai1Html', '')))
                with open(os.path.join(HD3_DIR, bai2_file), 'w', encoding='utf-8') as f:
                    f.write(wrap_html('Bài 2: Làm nổi bật ý chính', payload.get('bai2Html', '')))
                with open(os.path.join(HD3_DIR, bai3_file), 'w', encoding='utf-8') as f:
                    f.write(wrap_html('Bài 3: Internet tốc độ cao', payload.get('bai3Html', '')))

                hd3_list = get_hd3_submissions()
                new_record = {
                    'id': hd3_id,
                    'activity': 'hd3',
                    'studentName': student_name,
                    'isPair': payload.get('isPair', False),
                    'student1': payload.get('student1'),
                    'student2': payload.get('student2'),
                    'className': class_name,
                    'studentNumber': payload.get('studentNumber', 'N/A'),
                    'submittedAt': payload.get('submittedAt', time.strftime('%H:%M:%S - %d/%m/%Y')),
                    'timestamp': int(time.time() * 1000),
                    'files': {
                        'bai1': {'filename': bai1_file, 'url': f'/submissions_hd3/{bai1_file}', 'code': payload.get('bai1Html', '')},
                        'bai2': {'filename': bai2_file, 'url': f'/submissions_hd3/{bai2_file}', 'code': payload.get('bai2Html', '')},
                        'bai3': {'filename': bai3_file, 'url': f'/submissions_hd3/{bai3_file}', 'code': payload.get('bai3Html', '')}
                    }
                }

                hd3_list.insert(0, new_record)
                save_hd3_submissions(hd3_list)

                print(f"[SUBMIT - HĐ 3 Luyện tập] {student_name} ({class_name}) đã nộp bài. Đã lưu 3 file HTML: {bai1_file}, {bai2_file}, {bai3_file}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': new_record}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
                return

        elif path == '/api/reset':
            query = urllib.parse.parse_qs(parsed_url.query)
            worksheet = query.get('worksheet', [None])[0]
            if worksheet:
                subs = get_submissions()
                subs = [s for s in subs if s.get('worksheetId', 'phieu1') != worksheet]
                save_submissions(subs)
                print(f"[RESET] Đã xóa bài nộp của {worksheet}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': f'Đã xóa dữ liệu bài nộp {worksheet}'}, ensure_ascii=False).encode('utf-8'))
                return
            else:
                save_submissions([])
                print("[RESET] Đã xóa toàn bộ bài nộp (Phiếu 1 & Phiếu 2)")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'Đã xóa toàn bộ dữ liệu bài nộp'}, ensure_ascii=False).encode('utf-8'))
                return

        elif path == '/api/reset-hd3':
            save_hd3_submissions([])
            if os.path.exists(HD3_DIR):
                try:
                    for f in os.listdir(HD3_DIR):
                        if f.endswith('.html'):
                            os.remove(os.path.join(HD3_DIR, f))
                except Exception as e:
                    print("Lỗi dọn dẹp thư mục submissions_hd3:", e)
            print("[RESET] Đã xóa toàn bộ dữ liệu bài nộp Hoạt động 3 và dọn dẹp file HTML")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Đã xóa dữ liệu bài nộp Hoạt động 3'}, ensure_ascii=False).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        if path == '/api/submissions':
            submissions = get_submissions()
            req_worksheet = query.get('worksheet', [None])[0]
            if req_worksheet:
                submissions = [s for s in submissions if s.get('worksheetId', 'phieu1') == req_worksheet]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(submissions, ensure_ascii=False).encode('utf-8'))
            return

        if path == '/api/submissions-hd3':
            submissions = get_hd3_submissions()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(submissions, ensure_ascii=False).encode('utf-8'))
            return

        # Tải toàn bộ bài nộp HD3 thành 1 file zip gom theo từng folder học sinh
        if path in ['/api/submissions-hd3-zip', '/api/teacher/download-all-zip']:
            import tempfile
            from create_submissions_zip import make_submissions_zip
            temp_dir = tempfile.gettempdir()
            temp_zip = os.path.join(temp_dir, f'Bai8_HD3_TatCaBaiLam_{int(time.time())}.zip')
            res_zip = make_submissions_zip(temp_zip)
            if res_zip and os.path.exists(res_zip):
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="Bai8_HD3_TatCaBaiLam_THTH_DHSP.zip"')
                self.send_header('Content-Length', str(os.path.getsize(res_zip)))
                self.end_headers()
                with open(res_zip, 'rb') as f:
                    self.wfile.write(f.read())
                try:
                    os.remove(res_zip)
                except Exception:
                    pass
                return
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'Lỗi tạo file zip'}).encode('utf-8'))
                return

        # Phục vụ các file HTML bài làm của học sinh
        if path.startswith('/submissions_hd3/'):
            filename = os.path.basename(path)
            html_file_path = os.path.join(HD3_DIR, filename)
            if os.path.exists(html_file_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                if 'download=1' in parsed.query:
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                with open(html_file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f'404 Không tìm thấy file bài làm: {filename}'.encode('utf-8'))
                return

        # Bảo vệ tài liệu Kế hoạch bài dạy và Slide PowerPoint (Chỉ giáo viên mới được tải)
        if path.endswith('Bai8.docx') or path.endswith('pptx.pdf') or path.endswith('Bai8_TrinhChieu.pptx'):
            cookies = self.headers.get('Cookie', '')
            auth = self.headers.get('Authorization', '')
            query = parsed.query
            is_teacher = 'thth_teacher=1' in cookies or 'access_token' in cookies or auth.startswith('Bearer ') or 'teacher=1' in query
            if not is_teacher:
                self.send_response(403)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('<h2>403 Quyền truy cập bị từ chối: Kế hoạch bài dạy và Slide tài liệu chỉ dành riêng cho Giáo viên Trường THTH - DHSP.</h2>'.encode('utf-8'))
                return

        # Đường dẫn tắt
        target_path = path
        if target_path in ['/', '/bai8']:
            target_path = '/Tin12/Bai8/hd2.html'
        elif target_path in ['/phieu1', '/phieubaitap1', '/phieu-bai-tap-1.html']:
            target_path = '/Tin12/Bai8/phieu-bai-tap-1.html'
        elif target_path in ['/phieu2', '/phieubaitap2', '/phieu-bai-tap-2.html']:
            target_path = '/Tin12/Bai8/phieu-bai-tap-2.html'
        elif target_path in ['/hd1', '/hd1.html']:
            target_path = '/Tin12/Bai8/hd1.html'
        elif target_path in ['/hd2', '/hd2.html']:
            target_path = '/Tin12/Bai8/hd2.html'
        elif target_path in ['/hd3', '/hd3.html']:
            target_path = '/Tin12/Bai8/hd3.html'
        elif target_path in ['/hd4', '/hd4.html']:
            target_path = '/Tin12/Bai8/hd4.html'

        rel_path = target_path
        if rel_path.startswith('/Tin12/Bai8/'):
            rel_path = rel_path[len('/Tin12/Bai8/'):]
        rel_path = rel_path.lstrip('/')

        file_path = os.path.join(CURRENT_DIR, rel_path)
        if not (os.path.exists(file_path) and not os.path.isdir(file_path)):
            file_path = os.path.join(BASE_DIR, target_path.lstrip('/'))
            if os.path.isdir(file_path):
                file_path = os.path.join(file_path, 'index.html')

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'404 Không tìm thấy: {path}'.encode('utf-8'))
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        if 'text' in mime_type or 'javascript' in mime_type or 'json' in mime_type:
            mime_type += '; charset=utf-8'

        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f'Lỗi đọc file: {e}'.encode('utf-8'))

if __name__ == '__main__':
    with socketserver.TCPServer(('0.0.0.0', PORT), ClassroomRequestHandler) as httpd:
        print("=======================================================")
        print(f"🚀 MÁY CHỦ BÀI 8 (PYTHON) ĐANG HOẠT ĐỘNG TẠI CỔNG {PORT}")
        print(f"📱 Link Phiếu bài tập số 1:  http://localhost:{PORT}/phieu1")
        print(f"🖥️  Link Bài giảng HĐ 2:      http://localhost:{PORT}/hd2")
        print("=======================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã tắt máy chủ.")

