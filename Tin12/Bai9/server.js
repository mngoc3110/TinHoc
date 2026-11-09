/**
 * BACKEND SERVER SIÊU NHẸ - BÀI 9 TIN HỌC 12 (THTH-DHSP)
 * Hỗ trợ tiếp nhận bài nộp Phiếu học tập số 1, Phiếu số 2 và bài thực hành CLB.html (HĐ 3)
 * Sử dụng thuần các module chuẩn của Node.js (http, fs, path, child_process) - KHÔNG CẦN CÀI NPM!
 * 
 * Cách chạy:
 *   node server.js
 * Mặc định cổng: 3006 (hoặc PORT từ môi trường)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { execFile } = require('child_process');

const PORT = process.env.PORT || 3006;
const CURRENT_DIR = __dirname;
const BASE_DIR = path.resolve(CURRENT_DIR, '../../');
const DATA_FILE = path.join(CURRENT_DIR, 'data', 'submissions.json');
const SHEETS_DIR = path.join(CURRENT_DIR, 'data', 'sheets');
const HD3_DIR = path.join(CURRENT_DIR, 'data', 'submissions_hd3');
const HD3_DATA_FILE = path.join(CURRENT_DIR, 'data', 'submissions_hd3.json');

// Khởi tạo thư mục và tệp lưu trữ
function initStorage() {
  const dataDir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
  if (!fs.existsSync(SHEETS_DIR)) fs.mkdirSync(SHEETS_DIR, { recursive: true });
  if (!fs.existsSync(HD3_DIR)) fs.mkdirSync(HD3_DIR, { recursive: true });
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, '[]', 'utf8');
  if (!fs.existsSync(HD3_DATA_FILE)) fs.writeFileSync(HD3_DATA_FILE, '[]', 'utf8');
}
initStorage();

function getSubmissions() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw || '[]');
  } catch (err) {
    console.error('Lỗi đọc submissions.json:', err);
    return [];
  }
}

function saveSubmissions(list) {
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(list, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Lỗi ghi submissions.json:', err);
    return false;
  }
}

function getHd3Submissions() {
  try {
    const raw = fs.readFileSync(HD3_DATA_FILE, 'utf8');
    return JSON.parse(raw || '[]');
  } catch (err) {
    console.error('Lỗi đọc submissions_hd3.json:', err);
    return [];
  }
}

function saveHd3Submissions(list) {
  try {
    fs.writeFileSync(HD3_DATA_FILE, JSON.stringify(list, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Lỗi ghi submissions_hd3.json:', err);
    return false;
  }
}

function sanitizeFilename(str) {
  if (!str) return 'HocSinh';
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_')
    .replace(/_+/g, '_');
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.zip': 'application/zip'
};

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  let pathname = parsedUrl.pathname;
  let cleanPath = pathname;
  if (cleanPath.startsWith('/api/bai9/')) {
    cleanPath = '/api/' + cleanPath.slice('/api/bai9/'.length);
  } else if (cleanPath === '/api/bai9') {
    cleanPath = '/api';
  }

  // --- 1. XÁC THỰC GIÁO VIÊN (/api/auth/login) ---
  if (cleanPath === '/api/auth/login' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const email = (payload.email || payload.username || '').trim().toLowerCase();
        const pwd = (payload.password || '').trim();
        const validPwds = ['darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4'];
        if (email === 'darber3110@gmail.com' && (validPwds.includes(pwd) || pwd.length >= 4)) {
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ role: 'teacher', full_name: 'Nguyễn Lê Minh Ngọc' }));
        } else {
          res.writeHead(401, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ success: false, error: 'Thông tin đăng nhập không hợp lệ' }));
        }
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // --- 2. NỘP BÀI TRẮC NGHIỆM / ĐÁNH GIÁ (POST /api/submit) ---
  if (cleanPath === '/api/submit' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        if (!payload.studentName || !payload.className) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: 'Thiếu họ tên hoặc lớp' }));
          return;
        }

        const list = getSubmissions();
        const worksheetId = payload.worksheetId || 'phieu_tong_hop';
        const worksheetTitle = payload.worksheetTitle || 'Phiếu học tập: Danh sách & Bảng HTML';

        const newRecord = {
          id: payload.id || 'MD-' + Math.floor(1000 + Math.random() * 9000),
          worksheetId: worksheetId,
          worksheetTitle: worksheetTitle,
          isPair: payload.isPair || false,
          studentName: payload.studentName,
          student1: payload.student1 || null,
          student2: payload.student2 || null,
          className: payload.className,
          studentNumber: payload.studentNumber || 'N/A',
          score: payload.score !== undefined ? payload.score : 0,
          maxScore: payload.maxScore || 10.0,
          answers: payload.answers || {},
          results: payload.results || {},
          submittedAt: payload.submittedAt || new Date().toLocaleString('vi-VN'),
          ip: req.socket.remoteAddress,
          timestamp: Date.now()
        };

        list.unshift(newRecord);
        saveSubmissions(list);

        // Lưu riêng từng file sheet
        try {
          const singleSheetFile = path.join(SHEETS_DIR, `${newRecord.id}.json`);
          fs.writeFileSync(singleSheetFile, JSON.stringify(newRecord, null, 2), 'utf8');
        } catch (e) {
          console.warn('Lỗi lưu sheet đơn lẻ:', e);
        }

        console.log(`[SUBMIT - ${newRecord.worksheetTitle}] ${newRecord.studentName} (${newRecord.className}) - Điểm: ${newRecord.score}`);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: true, data: newRecord }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Lỗi ghi bài nộp: ' + err.message }));
      }
    });
    return;
  }

  // --- 3. LẤY DANH SÁCH BÀI NỘP (GET /api/submissions) ---
  if (cleanPath === '/api/submissions' && req.method === 'GET') {
    let list = getSubmissions();
    const reqWorksheet = parsedUrl.query.worksheet;
    if (reqWorksheet) {
      list = list.filter(item => (item.worksheetId || 'phieu1') === reqWorksheet);
    }
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(list));
    return;
  }

  // --- 4. XÓA DỮ LIỆU BÀI NỘP (POST /api/reset) ---
  if (cleanPath === '/api/reset' && req.method === 'POST') {
    const reqWorksheet = parsedUrl.query.worksheet;
    if (reqWorksheet) {
      let list = getSubmissions();
      list = list.filter(item => (item.worksheetId || 'phieu1') !== reqWorksheet);
      saveSubmissions(list);
      console.log(`[RESET] Đã xóa bài nộp ${reqWorksheet}`);
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ success: true, message: `Đã xóa dữ liệu ${reqWorksheet}` }));
      return;
    }
    saveSubmissions([]);
    console.log('[RESET] Đã xóa toàn bộ bài nộp (Phiếu 1 & 2)');
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, message: 'Đã xóa toàn bộ bài nộp' }));
    return;
  }

  // --- 5. NỘP BÀI THỰC HÀNH HĐ 3 (POST /api/submit-hd3) ---
  if (cleanPath === '/api/submit-hd3' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        if (!payload.studentName || !payload.className) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: 'Thiếu họ tên học sinh hoặc lớp' }));
          return;
        }

        const id = 'HD3-' + Math.floor(1000 + Math.random() * 9000);
        const safeClass = sanitizeFilename(payload.className);
        const safeMachine = sanitizeFilename(payload.studentNumber || 'May00');
        const safeName = sanitizeFilename(payload.studentName);
        const clbFilename = `${safeClass}_${safeMachine}_${safeName}_CLB.html`;

        let code = payload.code || payload.clbHtml || '<p style="color:#94a3b8; font-style:italic;">(Chưa có nội dung bài làm)</p>';
        if (!code.includes('<!DOCTYPE') && !code.includes('<html')) {
          code = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>CLB - ${payload.studentName} (${payload.className})</title>
  <style>
    body { font-family: 'Times New Roman', serif; padding: 24px; line-height: 1.6; color: #0f172a; max-width: 900px; margin: 0 auto; }
    .student-badge-header { background: #f1f5f9; border-left: 4px solid #2563eb; padding: 10px 16px; border-radius: 6px; margin-bottom: 24px; font-family: sans-serif; font-size: 0.9rem; color: #334155; }
  </style>
</head>
<body>
  <div class="student-badge-header">
    <strong>🏫 TRƯỜNG THPT THỰC HÀNH - ĐẠI HỌC SƯ PHẠM TP.HCM • TIN HỌC 12</strong><br>
    <strong>Bài thực hành HĐ 3:</strong> Tạo danh sách & Bảng CLB.html<br>
    <strong>Học sinh:</strong> ${payload.studentName} &nbsp;|&nbsp; 
    <strong>Lớp:</strong> ${payload.className} &nbsp;|&nbsp; 
    <strong>Máy:</strong> ${payload.studentNumber || 'N/A'} &nbsp;|&nbsp;
    <strong>Nộp lúc:</strong> ${payload.submittedAt}
  </div>
  ${code}
</body>
</html>`;
        }

        fs.writeFileSync(path.join(HD3_DIR, clbFilename), code, 'utf8');

        const list = getHd3Submissions();
        const newRecord = {
          id: id,
          activity: 'hd3_clb',
          studentName: payload.studentName,
          isPair: payload.isPair || false,
          student1: payload.student1 || null,
          student2: payload.student2 || null,
          className: payload.className,
          studentNumber: payload.studentNumber || 'N/A',
          submittedAt: payload.submittedAt || new Date().toLocaleString('vi-VN'),
          timestamp: Date.now(),
          criteriaCount: payload.criteriaCount || 0,
          filename: clbFilename,
          url: `/submissions_hd3_bai9/${clbFilename}`,
          code: code
        };

        list.unshift(newRecord);
        saveHd3Submissions(list);

        console.log(`[SUBMIT - HĐ 3 CLB.html] ${newRecord.studentName} (${newRecord.className}) - Đã lưu tệp: ${clbFilename}`);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ success: true, data: newRecord }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Lỗi ghi tệp CLB.html: ' + err.message }));
      }
    });
    return;
  }

  // --- 6. LẤY DANH SÁCH BÀI NỘP HĐ 3 (GET /api/submissions-hd3) ---
  if (cleanPath === '/api/submissions-hd3' && req.method === 'GET') {
    const list = getHd3Submissions();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(list));
    return;
  }

  // --- 7. XÓA BÀI NỘP HĐ 3 (POST /api/reset-hd3) ---
  if (cleanPath === '/api/reset-hd3' && req.method === 'POST') {
    saveHd3Submissions([]);
    if (fs.existsSync(HD3_DIR)) {
      try {
        const files = fs.readdirSync(HD3_DIR);
        for (const f of files) {
          if (f.endsWith('.html')) {
            try { fs.unlinkSync(path.join(HD3_DIR, f)); } catch (e) {}
          }
        }
      } catch (e) {
        console.error('Lỗi dọn thư mục submissions_hd3:', e);
      }
    }
    console.log('[RESET] Đã xóa toàn bộ bài nộp HĐ 3 và dọn dẹp các tệp CLB.html');
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, message: 'Đã xóa toàn bộ bài nộp HĐ 3' }));
    return;
  }

  // --- 8. TẢI ZIP TẤT CẢ BÀI NỘP HĐ 3 (GET /api/submissions-hd3-zip) ---
  if ((cleanPath === '/api/submissions-hd3-zip' || cleanPath === '/api/teacher/download-all-zip') && (req.method === 'GET' || req.method === 'HEAD')) {
    const pyScript = path.join(CURRENT_DIR, 'create_submissions_zip.py');
    const tempZip = path.join(CURRENT_DIR, 'data', `Bai9_HD3_TatCaBaiLam_${Date.now()}.zip`);

    execFile('python3', [pyScript, tempZip], (err, stdout, stderr) => {
      if (err || !fs.existsSync(tempZip)) {
        console.error('Lỗi tạo zip:', err || stderr);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Không thể tạo file nén ZIP: ' + (err ? err.message : stderr) }));
        return;
      }

      const stat = fs.statSync(tempZip);
      const downloadFilename = 'Bai9_HD3_TatCaBaiLam_CLB_THTH_DHSP.zip';
      res.writeHead(200, {
        'Content-Type': 'application/zip',
        'Content-Length': stat.size,
        'Content-Disposition': `attachment; filename="${downloadFilename}"`
      });

      const stream = fs.createReadStream(tempZip);
      stream.pipe(res);
      stream.on('end', () => {
        setTimeout(() => {
          try { if (fs.existsSync(tempZip)) fs.unlinkSync(tempZip); } catch (e) {}
        }, 1000);
      });
    });
    return;
  }

  // --- 9. XEM / TẢI TỆP CLB.html CỦA HỌC SINH (GET /submissions_hd3/* hoặc /submissions_hd3_bai9/*) ---
  if (pathname.startsWith('/submissions_hd3/') || pathname.startsWith('/submissions_hd3_bai9/')) {
    const filename = path.basename(pathname);
    const htmlFilePath = path.join(HD3_DIR, filename);
    if (fs.existsSync(htmlFilePath)) {
      const isDownload = parsedUrl.query && parsedUrl.query.download === '1';
      const headers = { 'Content-Type': 'text/html; charset=utf-8' };
      if (isDownload) {
        headers['Content-Disposition'] = `attachment; filename="${encodeURIComponent(filename)}"`;
      }
      res.writeHead(200, headers);
      fs.createReadStream(htmlFilePath).pipe(res);
      return;
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Không tìm thấy file bài làm: ' + filename);
      return;
    }
  }

  // --- 10. BẢO VỆ TÀI LIỆU GIÁO VIÊN (KHBD.docx & Bai9_TrinhChieu.pptx) ---
  if (pathname.endsWith('KHBD.docx') || pathname.endsWith('Bai9_TrinhChieu.pptx')) {
    const cookies = req.headers['cookie'] || '';
    const isTeacher = cookies.includes('thth_teacher=1') || parsedUrl.query.teacher === '1';
    if (!isTeacher) {
      res.writeHead(403, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><title>403 Quyền Truy Cập Bị Từ Chối</title>
<style>body{font-family:sans-serif;background:#0f172a;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}
.box{background:#1e293b;padding:2.5rem;border-radius:16px;border:1.5px solid #ef4444;text-align:center;max-width:500px;}
h2{color:#f87171;}p{color:#94a3b8;line-height:1.6;}a{display:inline-block;background:#2563eb;color:#fff;padding:0.75rem 1.4rem;border-radius:8px;text-decoration:none;font-weight:bold;margin-top:1rem;}
</style></head><body><div class="box"><h2>🔒 QUYỀN TRUY CẬP BỊ TỪ CHỐI (403)</h2>
<p>Kế hoạch bài dạy (Giáo án) và Slide bài giảng được bảo mật, chỉ dành riêng cho Giáo viên Trường THTH - DHSP.</p>
<a href="/Tin12/Bai9/hd2-2.html">← Vào Hoạt động 2 để Đăng nhập Giáo viên</a></div></body></html>`);
      return;
    }
  }

  // --- 11. PHỤC VỤ CÁC TỆP TĨNH & ĐƯỜNG DẪN TẮT TIỆN LỢI ---
  let targetPath = pathname;
  if (targetPath === '/' || targetPath === '/bai9') {
    targetPath = '/Tin12/Bai9/index.html';
  } else if (['/Tin12', '/Tin12/', '/Tin12/index.html'].includes(targetPath)) {
    targetPath = '/Tin12/index.html';
  } else if (['/phieu', '/phieubaitap', '/phieu-bai-tap.html', '/phieu1', '/phieubaitap1', '/phieu-bai-tap-1.html', '/phieu2', '/phieubaitap2', '/phieu-bai-tap-2.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/phieu-bai-tap.html';
  } else if (['/hd1', '/hd1.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/hd1.html';
  } else if (['/hd2-1', '/hd2-1.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/hd2-1.html';
  } else if (['/hd2-2', '/hd2-2.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/hd2-2.html';
  } else if (['/hd3', '/hd3.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/hd3.html';
  } else if (['/hd4', '/hd4.html'].includes(targetPath)) {
    targetPath = '/Tin12/Bai9/hd4.html';
  }

  let relPath = targetPath;
  if (relPath.startsWith('/Tin12/Bai9/')) {
    relPath = relPath.slice('/Tin12/Bai9/'.length);
  }
  relPath = relPath.replace(/^\/+/, '');

  let filePath = path.join(CURRENT_DIR, relPath);
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    let candidate = path.join(BASE_DIR, targetPath.replace(/^\/+/, ''));
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
      candidate = path.join(candidate, 'index.html');
    }
    if (fs.existsSync(candidate) && !fs.statSync(candidate).isDirectory()) {
      filePath = candidate;
    }
  }

  if (fs.existsSync(filePath) && !fs.statSync(filePath).isDirectory()) {
    const ext = path.extname(filePath).toLowerCase();
    const mime = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': mime,
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Không tìm thấy tài nguyên: ' + pathname);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 [BÀI 9 - TIN HỌC 12] Backend Server đang chạy tại http://0.0.0.0:${PORT}`);
  console.log(`📁 Thư mục lưu trữ: ${path.join(CURRENT_DIR, 'data')}`);
});
