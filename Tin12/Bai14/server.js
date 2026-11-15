/**
 * BACKEND NODE.JS - BÀI 14: ĐỊNH DẠNG VĂN BẢN BẰNG CSS (TIN HỌC 12 • THTH-DHSP)
 * Hệ thống thu thập bài nộp, kiểm tra trực tuyến & bảng điều khiển Giáo viên Realtime
 * Chạy độc lập: node server.js (Port 3017) hoặc qua Tin12/hub_server.js (Port 3020)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { execSync } = require('child_process');

const PORT = process.env.PORT || 3017;
const CURRENT_DIR = __dirname;
const ROOT_DIR = CURRENT_DIR;
const DATA_FILE = path.join(CURRENT_DIR, 'data', 'submissions.json');
const SHEETS_DIR = path.join(CURRENT_DIR, 'data', 'sheets');
const HD3_DIR = path.join(CURRENT_DIR, 'data', 'submissions_hd3');
const HD3_DATA_FILE = path.join(CURRENT_DIR, 'data', 'submissions_hd3.json');

fs.mkdirSync(path.dirname(DATA_FILE), { recursive: true });
fs.mkdirSync(SHEETS_DIR, { recursive: true });
fs.mkdirSync(HD3_DIR, { recursive: true });
if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, '[]', 'utf8');
if (!fs.existsSync(HD3_DATA_FILE)) fs.writeFileSync(HD3_DATA_FILE, '[]', 'utf8');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.json': 'application/json; charset=utf-8',
  '.zip': 'application/zip',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
};

const TEACHER_PASSWORDS = ['darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4'];

function readJson(filePath) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); }
  catch (e) { return []; }
}
function writeJson(filePath, data) {
  try { fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8'); return true; }
  catch (e) { return false; }
}
function normalizeVN(str) {
  if (!str) return 'HocSinh';
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_').replace(/_+/g, '_');
}
function isTeacher(req) {
  return (req.headers.cookie || '').includes('thth_teacher=1');
}
function cleanApiPath(p) {
  const prefix = '/api/bai14';
  if (p.startsWith(prefix + '/')) return '/api/' + p.slice(prefix.length + 1);
  if (p === prefix) return '/api';
  return p;
}

const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  const cleanPath = cleanApiPath(reqUrl.pathname);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  if (req.method === 'POST' && cleanPath === '/api/auth/login') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { email, password } = JSON.parse(body || '{}');
        if (TEACHER_PASSWORDS.includes(String(password || '').trim())) {
          res.setHeader('Set-Cookie', 'thth_teacher=1; Path=/; SameSite=Lax');
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ authenticated: true, email, name: 'Nguyễn Lê Minh Ngọc' }));
        } else {
          res.writeHead(401, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ authenticated: false, error: 'Sai mật khẩu' }));
        }
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/submit') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const sub = JSON.parse(body);
        const list = readJson(DATA_FILE);
        list.unshift(sub);
        writeJson(DATA_FILE, list);
        const safeClass = normalizeVN(sub.className || '12A');
        const safeName = normalizeVN(sub.studentName || 'HocSinh');
        const wsId = sub.worksheetId || 'phieubaitap';
        const fn = `${wsId}_${safeClass}_${safeName}_${Date.now()}.json`;
        fs.writeFileSync(path.join(SHEETS_DIR, fn), JSON.stringify(sub, null, 2), 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ status: 'ok', total: list.length, id: sub.id }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/submissions') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(readJson(DATA_FILE)));
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/reset') {
    writeJson(DATA_FILE, []);
    try {
      for (const f of fs.readdirSync(SHEETS_DIR)) {
        fs.unlinkSync(path.join(SHEETS_DIR, f));
      }
    } catch (e) {}
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'reset_ok' }));
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/submit-hd3') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const sub = JSON.parse(body);
        const safeClass = normalizeVN(sub.className || '12A');
        const safeMach = normalizeVN(sub.studentNumber || 'May00');
        const safeName = normalizeVN(sub.studentName || 'HocSinh');
        const filename = `${safeClass}_${safeMach}_${safeName}_Chia_de_tri.html`;
        sub.filename = filename;
        fs.writeFileSync(path.join(HD3_DIR, filename), sub.code || '', 'utf8');
        const list = readJson(HD3_DATA_FILE);
        list.unshift(sub);
        writeJson(HD3_DATA_FILE, list);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ status: 'ok', filename, total: list.length }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/submissions-hd3') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(readJson(HD3_DATA_FILE)));
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/reset-hd3') {
    writeJson(HD3_DATA_FILE, []);
    try {
      for (const f of fs.readdirSync(HD3_DIR)) {
        if (f.endsWith('.html')) fs.unlinkSync(path.join(HD3_DIR, f));
      }
    } catch (e) {}
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'reset_hd3_ok' }));
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/submissions-hd3-zip') {
    try {
      execSync('python3 create_submissions_zip.py', { cwd: CURRENT_DIR });
      const zipPath = path.join(CURRENT_DIR, 'Bai14_HD3_TatCaBaiLam_THTH_DHSP.zip');
      if (fs.existsSync(zipPath)) {
        const data = fs.readFileSync(zipPath);
        res.writeHead(200, {
          'Content-Type': 'application/zip',
          'Content-Disposition': 'attachment; filename="Bai14_HD3_TatCaBaiLam_THTH_DHSP.zip"',
        });
        res.end(data);
        return;
      }
    } catch (e) {}
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Zip build failed' }));
    return;
  }

  // Serve saved HTML files for viewing
  const hd3SubPrefix = '/submissions_hd3_bai14/';
  if (req.method === 'GET' && reqUrl.pathname.startsWith(hd3SubPrefix)) {
    const fname = path.basename(reqUrl.pathname);
    const fpath = path.join(HD3_DIR, fname);
    if (fs.existsSync(fpath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(fpath));
      return;
    }
  }

  // Static files with teacher protection for DOCX/PPTX
  let relPath = reqUrl.pathname === '/' ? '/index.html' : reqUrl.pathname;
  relPath = decodeURIComponent(relPath).replace(/^\/+/, '');
  const fullPath = path.resolve(ROOT_DIR, relPath);
  if (!fullPath.startsWith(ROOT_DIR)) {
    res.writeHead(403); res.end('Forbidden'); return;
  }
  const ext = path.extname(fullPath).toLowerCase();
  if ((ext === '.docx' || ext === '.pptx' || path.basename(fullPath).includes('KHBD') || path.basename(fullPath).includes('_TrinhChieu')) && !isTeacher(req)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 Forbidden - Chỉ Giáo viên được phép truy cập giáo án và bài trình chiếu.');
    return;
  }
  if (fs.existsSync(fullPath) && fs.statSync(fullPath).isFile()) {
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    fs.createReadStream(fullPath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found');
  }
});

server.listen(PORT, () => {
  console.log(`Bài 14: Định dạng văn bản bằng CSS Server listening on http://localhost:${PORT}`);
});
