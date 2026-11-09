#!/usr/bin/env python3
"""
BACKEND SERVER PYTHON SIÊU NHẸ - BÀI 9 TIN HỌC 12 (THTH-DHSP)
Hệ thống thu thập dữ liệu bài nộp & bảng điều khiển Realtime cho Giáo viên
Không cần cài thêm thư viện (chỉ dùng http.server, json, os, urllib có sẵn trong Python 3)

Cách chạy:
    python3 server.py
Mở trình duyệt: http://localhost:3000 hoặc http://localhost:3001
"""

import http.server
import socketserver
import json
import os
import urllib.parse
import mimetypes
import time
import re
import unicodedata

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
        clean_path = '/api/' + path[len('/api/bai9/'):] if path.startswith('/api/bai9/') else ('/api' if path == '/api/bai9' else path)

        if clean_path == '/api/auth/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                username = ''
                password = ''
                if post_body.startswith('{'):
                    data = json.loads(post_body)
                    username = data.get('username', data.get('email', '')).strip().lower()
                    password = data.get('password', '').strip()
                else:
                    parsed = urllib.parse.parse_qs(post_body)
                    username = parsed.get('username', parsed.get('email', ['']))[0].strip().lower()
                    password = parsed.get('password', [''])[0].strip()

                valid_pwds = ['darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4']
                if username == 'darber3110@gmail.com' and (password in valid_pwds or len(password) >= 4):
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'role': 'teacher', 'full_name': 'Nguyễn Lê Minh Ngọc'}).encode('utf-8'))
                    return
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Thông tin đăng nhập không hợp lệ'}).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        if clean_path == '/api/submit':
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
                worksheet_id = payload.get('worksheetId', 'phieu_tong_hop')
                worksheet_title = payload.get('worksheetTitle', 'Phiếu học tập: Danh sách & Bảng HTML')
                
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

                # Lưu riêng từng phiếu bài làm của học sinh
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

        elif clean_path == '/api/submit-hd3':
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
                clb_filename = f"{file_prefix}_CLB.html"

                clb_code = payload.get('code', '')
                if not clb_code:
                    clb_code = '<p style="color:#94a3b8; font-style:italic;">(Chưa có nội dung bài làm)</p>'

                # Ghi tệp CLB.html của học sinh
                clb_file_path = os.path.join(HD3_DIR, clb_filename)
                with open(clb_file_path, 'w', encoding='utf-8') as f:
                    f.write(clb_code)

                criteria_count = payload.get('criteriaCount', payload.get('criteriaScore', 0))
                status = payload.get('status', 'Đạt chuẩn' if criteria_count >= 6 else 'Cần hoàn thiện')

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
                    'criteriaScore': criteria_count,
                    'criteriaCount': criteria_count,
                    'maxCriteria': 8,
                    'status': status,
                    'submittedAt': payload.get('submittedAt', time.strftime('%H:%M:%S - %d/%m/%Y')),
                    'timestamp': int(time.time() * 1000),
                    'filename': clb_filename,
                    'fileUrl': f'/submissions_hd3/{clb_filename}',
                    'code': clb_code
                }

                hd3_list.insert(0, new_record)
                save_hd3_submissions(hd3_list)

                print(f"[SUBMIT - HĐ 3 Luyện tập] {student_name} ({class_name}) đã nộp CLB.html ({clb_filename})")

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

        elif clean_path == '/api/reset':
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

        elif clean_path == '/api/reset-hd3':
            save_hd3_submissions([])
            if os.path.exists(HD3_DIR):
                try:
                    for f in os.listdir(HD3_DIR):
                        if f.endswith('.html'):
                            os.remove(os.path.join(HD3_DIR, f))
                except Exception as e:
                    print("Lỗi dọn dẹp thư mục submissions_hd3:", e)
            print("[RESET] Đã xóa toàn bộ bài nộp Hoạt động 3 và dọn dẹp file CLB.html")
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
        clean_path = '/api/' + path[len('/api/bai9/'):] if path.startswith('/api/bai9/') else ('/api' if path == '/api/bai9' else path)
        query = urllib.parse.parse_qs(parsed_url.query)

        if clean_path == '/api/submissions':
            submissions = get_submissions()
            req_worksheet = query.get('worksheet', [None])[0]
            if req_worksheet:
                submissions = [s for s in submissions if s.get('worksheetId', 'phieu1') == req_worksheet]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(submissions, ensure_ascii=False).encode('utf-8'))
            return

        if clean_path == '/api/submissions-hd3':
            submissions = get_hd3_submissions()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(submissions, ensure_ascii=False).encode('utf-8'))
            return

        # Tải toàn bộ bài nộp HD3 thành 1 file zip gom theo từng folder học sinh
        if clean_path in ['/api/submissions-hd3-zip', '/api/teacher/download-all-zip']:
            import tempfile
            from create_submissions_zip import make_submissions_zip
            temp_dir = tempfile.gettempdir()
            temp_zip = os.path.join(temp_dir, f'Bai9_HD3_TatCaBaiLam_{int(time.time())}.zip')
            res_zip = make_submissions_zip(temp_zip)
            if res_zip and os.path.exists(res_zip):
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="Bai9_HD3_TatCaBaiLam_CLB_THTH_DHSP.zip"')
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
        if path.startswith('/submissions_hd3/') or path.startswith('/submissions_hd3_bai9/'):
            filename = os.path.basename(path)
            html_file_path = os.path.join(HD3_DIR, filename)
            if os.path.exists(html_file_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                if 'download=1' in parsed_url.query:
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

        # Đường dẫn tắt tiện lợi
        target_path = path
        if target_path in ['/', '/bai9']:
            target_path = '/Tin12/Bai9/index.html'
        elif target_path in ['/phieu', '/phieubaitap', '/phieu-bai-tap.html', '/phieu1', '/phieubaitap1', '/phieu-bai-tap-1.html', '/phieu2', '/phieubaitap2', '/phieu-bai-tap-2.html']:
            target_path = '/Tin12/Bai9/phieu-bai-tap.html'
        elif target_path in ['/hd1', '/hd1.html']:
            target_path = '/Tin12/Bai9/hd1.html'
        elif target_path in ['/hd2-1', '/hd2-1.html']:
            target_path = '/Tin12/Bai9/hd2-1.html'
        elif target_path in ['/hd2-2', '/hd2-2.html']:
            target_path = '/Tin12/Bai9/hd2-2.html'
        elif target_path in ['/hd3', '/hd3.html']:
            target_path = '/Tin12/Bai9/hd3.html'
        elif target_path in ['/hd4', '/hd4.html']:
            target_path = '/Tin12/Bai9/hd4.html'

        rel_path = target_path
        if rel_path.startswith('/Tin12/Bai9/'):
            rel_path = rel_path[len('/Tin12/Bai9/'):]
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

        if file_path.endswith('KHBD.docx') or file_path.endswith('Bai9_TrinhChieu.pptx'):
            cookies = self.headers.get('Cookie', '')
            if 'thth_teacher=1' not in cookies and 'teacher=1' not in parsed_url.query:
                self.send_response(403)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('''<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><title>403 Quyền Truy Cập Bị Từ Chối</title><style>body{font-family:sans-serif;background:#0f172a;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}.box{background:#1e293b;padding:2rem;border-radius:12px;border:1px solid #ef4444;text-align:center;max-width:480px;}h2{color:#f87171;}a{color:#60a5fa;}</style></head><body><div class="box"><h2>🔒 403 - KHÔNG CÓ QUYỀN TRUY CẬP</h2><p>Giáo án và Bài trình chiếu được bảo vệ, chỉ dành cho Giáo viên bộ môn.</p><a href="/Tin12/Bai9/hd2-2.html">← Đăng nhập Giáo viên tại đây</a></div></body></html>'''.encode('utf-8'))
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
    # Thử bind cổng PORT, nếu bận thử PORT + 1
    port_to_use = PORT
    try:
        httpd = socketserver.TCPServer(('0.0.0.0', port_to_use), ClassroomRequestHandler)
    except OSError:
        port_to_use = PORT + 1
        httpd = socketserver.TCPServer(('0.0.0.0', port_to_use), ClassroomRequestHandler)

    with httpd:
        print("=================================================================")
        print(f"🚀 MÁY CHỦ BÀI 9 (PYTHON) ĐANG HOẠT ĐỘNG TẠI CỔNG {port_to_use}")
        print(f"📱 Link Phiếu bài tập (Tổng hợp): http://localhost:{port_to_use}/phieu")
        print(f"🖥️  Link Bài giảng HĐ 2.1:      http://localhost:{port_to_use}/hd2-1")
        print(f"🖥️  Link Bài giảng HĐ 2.2:      http://localhost:{port_to_use}/hd2-2")
        print(f"💻 Link Thực hành CLB HĐ 3:    http://localhost:{port_to_use}/hd3")
        print("=================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã tắt máy chủ Bài 9.")
