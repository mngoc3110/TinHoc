/**
 * BACKEND SERVER SIÊU NHẸ - BÀI 8 TIN HỌC 12 (THTH-DHSP)
 * Hỗ trợ tiếp nhận bài nộp Phiếu học tập số 1 và phục vụ trang web lớp học.
 * Sử dụng thuần các module chuẩn của Node.js (http, fs, path) - KHÔNG CẦN CÀI NPM PACKAGE!
 * 
 * Cách chạy:
 *   node server.js
 * Sau đó mở trình duyệt: http://localhost:3000
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const BASE_DIR = path.resolve(__dirname, '../../'); // Thư mục gốc THTH-DHSP
const DATA_FILE = path.join(__dirname, 'data', 'submissions.json');
const SHEETS_DIR = path.join(__dirname, 'data', 'sheets');
const HD3_DIR = path.join(__dirname, 'data', 'submissions_hd3');
const HD3_DATA_FILE = path.join(__dirname, 'data', 'submissions_hd3.json');

// Khởi tạo thư mục và file lưu trữ bài nộp nếu chưa có
function initStorage() {
  const dataDir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  if (!fs.existsSync(SHEETS_DIR)) {
    fs.mkdirSync(SHEETS_DIR, { recursive: true });
  }
  if (!fs.existsSync(HD3_DIR)) {
    fs.mkdirSync(HD3_DIR, { recursive: true });
  }
  if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, JSON.stringify([], null, 2), 'utf8');
  }
  if (!fs.existsSync(HD3_DATA_FILE)) {
    fs.writeFileSync(HD3_DATA_FILE, JSON.stringify([], null, 2), 'utf8');
  }
}

initStorage();

// Đọc danh sách bài nộp từ JSON (Phiếu 1 & 2)
function getSubmissions() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw || '[]');
  } catch (err) {
    console.error('Lỗi khi đọc file submissions.json:', err);
    return [];
  }
}

// Lưu danh sách bài nộp vào JSON (Phiếu 1 & 2)
function saveSubmissions(list) {
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(list, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Lỗi khi ghi file submissions.json:', err);
    return false;
  }
}

// Đọc danh sách bài nộp Hoạt động 3
function getHd3Submissions() {
  try {
    const raw = fs.readFileSync(HD3_DATA_FILE, 'utf8');
    return JSON.parse(raw || '[]');
  } catch (err) {
    console.error('Lỗi khi đọc file submissions_hd3.json:', err);
    return [];
  }
}

// Lưu danh sách bài nộp Hoạt động 3
function saveHd3Submissions(list) {
  try {
    fs.writeFileSync(HD3_DATA_FILE, JSON.stringify(list, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Lỗi khi ghi file submissions_hd3.json:', err);
    return false;
  }
}

// Chuẩn hóa tên file không dấu tiếng Việt
function sanitizeFilename(str) {
  if (!str) return 'HocSinh';
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_')
    .replace(/_+/g, '_');
}

// Bảng ánh xạ MIME types
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
  '.pdf': 'application/pdf'
};

const server = http.createServer((req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  // --- API ENDPOINT: NỘP BÀI HỌC SINH (POST /api/submit) ---
  if (pathname === '/api/submit' && req.method === 'POST') {
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
        const newRecord = {
          id: payload.id || 'MD-' + Math.floor(1000 + Math.random() * 9000),
          worksheetId: payload.worksheetId || 'phieu1',
          worksheetTitle: payload.worksheetTitle || (payload.worksheetId === 'phieu2' ? 'Phiếu bài tập số 2' : 'Phiếu bài tập số 1'),
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

        // Lưu riêng từng phiếu bài làm của học sinh thành một file độc lập
        try {
          const singleSheetFile = path.join(SHEETS_DIR, `${newRecord.id}.json`);
          fs.writeFileSync(singleSheetFile, JSON.stringify(newRecord, null, 2), 'utf8');
        } catch (e) {
          console.warn('Lỗi lưu single sheet file:', e);
        }

        console.log(`[SUBMIT - ${newRecord.worksheetTitle}] ${newRecord.studentName} (${newRecord.className}) nộp bài đạt ${newRecord.score} điểm. Đã lưu phiếu: ${newRecord.id}.json`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, data: newRecord }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Lỗi xử lý JSON' }));
      }
    });
    return;
  }

  // --- API ENDPOINT: LẤY DANH SÁCH BÀI NỘP (GET /api/submissions) ---
  if (pathname === '/api/submissions' && req.method === 'GET') {
    let list = getSubmissions();
    const reqWorksheet = parsedUrl.query.worksheet;
    if (reqWorksheet) {
      list = list.filter(item => (item.worksheetId || 'phieu1') === reqWorksheet);
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(list));
    return;
  }

  // --- API ENDPOINT: XÓA DỮ LIỆU BÀI NỘP (POST /api/reset) ---
  if (pathname === '/api/reset' && req.method === 'POST') {
    saveSubmissions([]);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: true, message: 'Đã xóa dữ liệu bài nộp' }));
    return;
  }

  // --- API ENDPOINT: NỘP BÀI HOẠT ĐỘNG 3 (POST /api/submit-hd3) ---
  // Lưu mã nguồn học sinh thành từng file HTML độc lập trên đĩa!
  if (pathname === '/api/submit-hd3' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        if (!payload.studentName || !payload.className) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: 'Thiếu họ tên học sinh hoặc lớp học' }));
          return;
        }

        const id = 'HD3-' + Math.floor(1000 + Math.random() * 9000);
        const safeClass = sanitizeFilename(payload.className);
        const safeMachine = sanitizeFilename(payload.studentNumber || 'May00');
        const safeName = sanitizeFilename(payload.studentName);
        const filePrefix = `${safeClass}_${safeMachine}_${safeName}`;

        const wrapHtml = (title, code) => {
          if (!code) code = '<p style="color:#94a3b8; font-style:italic;">(Chưa có nội dung bài làm)</p>';
          if (code.includes('<!DOCTYPE') || code.includes('<html')) {
            return code;
          }
          return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} - ${payload.studentName} (${payload.className})</title>
  <style>
    body {
      font-family: 'Times New Roman', serif;
      padding: 24px;
      line-height: 1.6;
      color: #0f172a;
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
    }
    .student-badge-header {
      background: #f1f5f9;
      border-left: 4px solid #2563eb;
      padding: 10px 16px;
      border-radius: 6px;
      margin-bottom: 24px;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: 0.9rem;
      color: #334155;
    }
  </style>
</head>
<body>
  <div class="student-badge-header">
    <strong>🏫 THTH - DHSP - TIN HỌC 12</strong><br>
    <strong>Học sinh:</strong> ${payload.studentName} &nbsp;|&nbsp; 
    <strong>Lớp:</strong> ${payload.className} &nbsp;|&nbsp; 
    <strong>Máy:</strong> ${payload.studentNumber || 'N/A'} &nbsp;|&nbsp;
    <strong>Nộp lúc:</strong> ${payload.submittedAt}
  </div>
  ${code}
</body>
</html>`;
        };

        const bai1File = `${filePrefix}_Bai1.html`;
        const bai2File = `${filePrefix}_Bai2.html`;
        const bai3File = `${filePrefix}_Bai3.html`;

        fs.writeFileSync(path.join(HD3_DIR, bai1File), wrapHtml('Bài 1: Phương trình bậc 2', payload.bai1Html), 'utf8');
        fs.writeFileSync(path.join(HD3_DIR, bai2File), wrapHtml('Bài 2: Làm nổi bật ý chính', payload.bai2Html), 'utf8');
        fs.writeFileSync(path.join(HD3_DIR, bai3File), wrapHtml('Bài 3: Internet tốc độ cao', payload.bai3Html), 'utf8');

        const list = getHd3Submissions();
        const newRecord = {
          id: id,
          activity: 'hd3',
          studentName: payload.studentName,
          isPair: payload.isPair || false,
          student1: payload.student1 || null,
          student2: payload.student2 || null,
          className: payload.className,
          studentNumber: payload.studentNumber || 'N/A',
          submittedAt: payload.submittedAt || new Date().toLocaleString('vi-VN'),
          timestamp: Date.now(),
          files: {
            bai1: { filename: bai1File, url: `/submissions_hd3/${bai1File}`, code: payload.bai1Html || '' },
            bai2: { filename: bai2File, url: `/submissions_hd3/${bai2File}`, code: payload.bai2Html || '' },
            bai3: { filename: bai3File, url: `/submissions_hd3/${bai3File}`, code: payload.bai3Html || '' }
          }
        };

        list.unshift(newRecord);
        saveHd3Submissions(list);

        console.log(`[SUBMIT - HĐ 3 Luyện tập] ${newRecord.studentName} (${newRecord.className}) đã nộp bài. Đã lưu 3 file HTML: ${bai1File}, ${bai2File}, ${bai3File}`);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, data: newRecord }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Lỗi ghi file HTML bài làm: ' + err.message }));
      }
    });
    return;
  }

  // --- API ENDPOINT: LẤY DANH SÁCH BÀI NỘP HOẠT ĐỘNG 3 (GET /api/submissions-hd3) ---
  if (pathname === '/api/submissions-hd3' && req.method === 'GET') {
    const list = getHd3Submissions();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(list));
    return;
  }



  // --- API ENDPOINT: TẢI TOÀN BỘ BÀI NỘP HĐ 3 THÀNH 1 FILE ZIP GOM THEO TỪNG THƯ MỤC HỌC SINH (GET /api/submissions-hd3-zip) ---
  if ((pathname === '/api/submissions-hd3-zip' || pathname === '/api/teacher/download-all-zip') && req.method === 'GET') {
    const { execFile } = require('child_process');
    const pyScript = path.join(__dirname, 'create_submissions_zip.py');
    const tempZip = path.join(__dirname, 'data', `Bai8_HD3_TatCaBaiLam_${Date.now()}.zip`);

    execFile('python3', [pyScript, tempZip], (err, stdout, stderr) => {
      if (err || !fs.existsSync(tempZip)) {
        console.error('Lỗi khi nén file zip:', err || stderr);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Không thể tạo file nén ZIP: ' + (err ? err.message : stderr) }));
        return;
      }

      const stat = fs.statSync(tempZip);
      const downloadFilename = `Bai8_HD3_TatCaBaiLam_THTH_DHSP.zip`;
      res.writeHead(200, {
        'Content-Type': 'application/zip',
        'Content-Length': stat.size,
        'Content-Disposition': `attachment; filename="${downloadFilename}"`
      });

      const stream = fs.createReadStream(tempZip);
      stream.pipe(res);
      stream.on('end', () => {
        setTimeout(() => {
          try { if (fs.existsSync(tempZip)) fs.unlinkSync(tempZip); } catch(e) {}
        }, 1000);
      });
    });
    return;
  }

  // --- PHỤC VỤ TRỰC TIẾP TỪNG TỆP HTML BÀI LÀM CỦA HỌC SINH (GET /submissions_hd3/*) ---
  if (pathname.startsWith('/submissions_hd3/')) {
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



  // --- BẢO VỆ TÀI LIỆU KẾ HOẠCH BÀI DẠY VÀ SLIDE BÀI GIẢNG (CHỈ GIÁO VIÊN MỚI ĐƯỢC TẢI) ---
  if (pathname.endsWith('Bai8.docx') || pathname.endsWith('pptx.pdf')) {
    const cookies = req.headers['cookie'] || '';
    const authHeader = req.headers['authorization'] || '';
    const query = parsedUrl.query || {};
    const isTeacher = cookies.includes('thth_teacher=1') || 
                      cookies.includes('access_token') || 
                      authHeader.startsWith('Bearer ') || 
                      query.teacher === '1';

    if (!isTeacher) {
      res.writeHead(403, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>403 Quyền Truy Cập Bị Từ Chối | THTH - DHSP</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #f8fafc; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .box { background: #1e293b; padding: 2.5rem; border-radius: 16px; border: 1.5px solid #ef4444; text-align: center; max-width: 520px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
    h2 { color: #f87171; margin-top: 0; font-size: 1.4rem; }
    p { color: #94a3b8; line-height: 1.6; font-size: 0.95rem; }
    a { display: inline-block; background: #2563eb; color: #fff; padding: 0.75rem 1.4rem; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 1.25rem; }
  </style>
</head>
<body>
  <div class="box">
    <h2>🔒 QUYỀN TRUY CẬP BỊ TỪ CHỐI (403)</h2>
    <p>Kế hoạch bài dạy (Giáo án) và Slide bài giảng được bảo mật, chỉ dành riêng cho Giáo viên Trường THTH - DHSP.</p>
    <a href="/Tin12/Bai8/index.html">← Về trang chủ Bài 8 để Đăng nhập Giáo viên</a>
  </div>
</body>
</html>`);
      return;
    }
  }

  // --- CÁC ĐƯỜNG DẪN VIẾT TẮT TIỆN LỢI CHO HỌC SINH & GIÁO VIÊN ---
  let targetPath = pathname;
  if (targetPath === '/' || targetPath === '/bai8') {
    targetPath = '/Tin12/Bai8/hd2.html';
  } else if (targetPath === '/phieu1' || targetPath === '/phieubaitap1' || targetPath === '/phieu-bai-tap-1.html') {
    targetPath = '/Tin12/Bai8/phieu-bai-tap-1.html';
  } else if (targetPath === '/phieu2' || targetPath === '/phieubaitap2' || targetPath === '/phieu-bai-tap-2.html') {
    targetPath = '/Tin12/Bai8/phieu-bai-tap-2.html';
  } else if (targetPath === '/hd1' || targetPath === '/hd1.html') {
    targetPath = '/Tin12/Bai8/hd1.html';
  } else if (targetPath === '/hd2' || targetPath === '/hd2.html') {
    targetPath = '/Tin12/Bai8/hd2.html';
  } else if (targetPath === '/hd3' || targetPath === '/hd3.html') {
    targetPath = '/Tin12/Bai8/hd3.html';
  } else if (targetPath === '/hd4' || targetPath === '/hd4.html') {
    targetPath = '/Tin12/Bai8/hd4.html';
  }

  // Phục vụ Static Files:
  // 1. Tìm trong thư mục Bai8 hiện tại (__dirname)
  const relPath = targetPath.replace(/^\/Tin12\/Bai8\/?/, '').replace(/^\//, '');
  let filePath = path.join(__dirname, relPath);

  // 2. Nếu không có trong Bai8, tìm trong thư mục gốc BASE_DIR
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(BASE_DIR, targetPath);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }
  }

  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Không tìm thấy trang: ' + pathname);
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Lỗi đọc file: ' + err.message);
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`=======================================================`);
  console.log(`🚀 MÁY CHỦ BÀI 8 (TIN HỌC 12) ĐANG HOẠT ĐỘNG!`);
  console.log(`🌐 Cổng: ${PORT}`);
  console.log(`📱 Link Phiếu bài tập số 1:  http://localhost:${PORT}/phieu1`);
  console.log(`📱 Link Phiếu bài tập số 2:  http://localhost:${PORT}/phieu2`);
  console.log(`🖥️  Link Bài giảng HĐ 2:      http://localhost:${PORT}/hd2`);
  console.log(`📂 Dữ liệu bài nộp lưu tại:  ${DATA_FILE}`);
  console.log(`=======================================================`);
});

