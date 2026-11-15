/**
 * HUB SERVER HỢP NHẤT — TIN HỌC 12 (THTH-DHSP)
 * Phục vụ toàn bộ portal Tin12/index.html và tất cả bài học Bai7..Bai15, ThucHanh_KTTX3, OnTap_HK1
 * Khởi chạy: node hub_server.js (mặc định Port 3020)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { execFileSync } = require('child_process');

const PORT = process.env.PORT || 3020;
const HUB_ROOT = __dirname;

const LESSONS = {
  bai7:     { dir: 'Bai7',           defaultExtFile: 'Bai7.html',        zipName: 'BaiNop_HD3_Bai7.zip' },
  bai8:     { dir: 'Bai8',           defaultExtFile: 'Bai8.html',        zipName: 'BaiNop_HD3_Bai8.zip' },
  bai9:     { dir: 'Bai9',           defaultExtFile: 'CLB.html',         zipName: 'BaiNop_HD3_Bai9.zip' },
  bai10:    { dir: 'Bai10',          defaultExtFile: 'CLB.html',         zipName: 'BaiNop_HD3_Bai10.zip' },
  bai11:    { dir: 'Bai11',          defaultExtFile: 'the_thao.html',    zipName: 'BaiNop_HD3_Bai11.zip' },
  bai12:    { dir: 'Bai12',          defaultExtFile: 'dang_ki_thi.html', zipName: 'BaiNop_HD3_Bai12.zip' },
  kttx3:    { dir: 'ThucHanh_KTTX3', defaultExtFile: 'Website_CLB.html', zipName: 'BaiNop_HD3_KTTX3.zip' },
  ontaphk1: { dir: 'OnTap_HK1',      defaultExtFile: 'OnTap_HK1.html',   zipName: 'BaiNop_HD3_OnTapHK1.zip' },
  bai13:    { dir: 'Bai13',          defaultExtFile: 'Lich_su_CSS.html', zipName: 'BaiNop_HD3_Bai13.zip' },
  bai14:    { dir: 'Bai14',          defaultExtFile: 'Chia_de_tri.html', zipName: 'BaiNop_HD3_Bai14.zip' },
  bai15:    { dir: 'Bai15',          defaultExtFile: 'Loi_ich_CSS.html', zipName: 'BaiNop_HD3_Bai15.zip' },
};

const DIR_TO_SLUG = {
  bai7: 'bai7',
  bai8: 'bai8',
  bai9: 'bai9',
  bai10: 'bai10',
  bai11: 'bai11',
  bai12: 'bai12',
  thuchanh_kttx3: 'kttx3',
  ontap_hk1: 'ontaphk1',
  bai13: 'bai13',
  bai14: 'bai14',
  bai15: 'bai15',
};

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
  '.pdf': 'application/pdf',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
};

const TEACHER_PASSWORDS = ['darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4'];

function getLessonPaths(slug) {
  const cfg = LESSONS[slug] || LESSONS.bai10;
  const lessonDir = path.join(HUB_ROOT, cfg.dir);
  const dataFile = path.join(lessonDir, 'data', 'submissions.json');
  const sheetsDir = path.join(lessonDir, 'data', 'sheets');
  const hd3Dir = path.join(lessonDir, 'data', 'submissions_hd3');
  const hd3DataFile = path.join(lessonDir, 'data', 'submissions_hd3.json');
  return { ...cfg, slug, lessonDir, dataFile, sheetsDir, hd3Dir, hd3DataFile };
}

function ensureLessonDirs(paths) {
  fs.mkdirSync(path.dirname(paths.dataFile), { recursive: true });
  fs.mkdirSync(paths.sheetsDir, { recursive: true });
  fs.mkdirSync(paths.hd3Dir, { recursive: true });
  if (!fs.existsSync(paths.dataFile)) fs.writeFileSync(paths.dataFile, '[]', 'utf8');
  if (!fs.existsSync(paths.hd3DataFile)) fs.writeFileSync(paths.hd3DataFile, '[]', 'utf8');
}

function readJson(filePath) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); }
  catch (e) { return []; }
}

function writeJson(filePath, data) {
  try {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (e) {
    return false;
  }
}

function normalizeVN(str) {
  if (!str) return 'HocSinh';
  return String(str)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_')
    .replace(/_+/g, '_');
}

function isTeacher(req) {
  return (req.headers.cookie || '').includes('thth_teacher=1');
}

function stripBasePrefix(p) {
  if (p === '/Tin12') return '/';
  if (p.startsWith('/Tin12/')) return p.slice('/Tin12'.length);
  return p;
}

function resolveApiRoute(pathname, req) {
  const m = pathname.match(/^\/api\/(bai7|bai8|bai9|bai10|bai11|bai12|kttx3|ontaphk1|bai13|bai14|bai15)(\/.*)?$/);
  if (m) {
    const slug = m[1];
    const cleanPath = m[2] ? '/api' + m[2] : '/api';
    return { slug, cleanPath };
  }
  const ref = String(req.headers.referer || '');
  const refMatch = ref.match(/\/(Bai7|Bai8|Bai9|Bai10|Bai11|Bai12|ThucHanh_KTTX3|OnTap_HK1|Bai13|Bai14|Bai15)\b/i);
  const slug = refMatch ? (DIR_TO_SLUG[refMatch[1].toLowerCase()] || 'bai10') : 'bai8';
  return { slug, cleanPath: pathname };
}

function readBody(req, cb) {
  let body = '';
  req.on('data', chunk => { body += chunk; });
  req.on('end', () => cb(body));
}

function sendJson(res, status, payload, extraHeaders = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', ...extraHeaders });
  res.end(JSON.stringify(payload));
}

const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  const rawPathname = decodeURIComponent(reqUrl.pathname || '/');
  const pathname = stripBasePrefix(rawPathname);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // --- API ROUTES ---
  if (pathname === '/api' || pathname.startsWith('/api/')) {
    const { slug, cleanPath } = resolveApiRoute(pathname, req);
    const paths = getLessonPaths(slug);
    ensureLessonDirs(paths);

    if (req.method === 'POST' && cleanPath === '/api/auth/login') {
      readBody(req, body => {
        try {
          const payload = JSON.parse(body || '{}');
          const password = String(payload.password || '').trim();
          const email = payload.email || payload.username || '';
          if (TEACHER_PASSWORDS.includes(password)) {
            res.setHeader('Set-Cookie', 'thth_teacher=1; Path=/; SameSite=Lax');
            sendJson(res, 200, {
              authenticated: true,
              role: 'teacher',
              email,
              name: 'Nguyễn Lê Minh Ngọc',
              full_name: 'Nguyễn Lê Minh Ngọc',
            });
          } else {
            sendJson(res, 401, { authenticated: false, success: false, error: 'Sai mật khẩu' });
          }
        } catch (e) {
          sendJson(res, 400, { error: e.message });
        }
      });
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/submit') {
      readBody(req, body => {
        try {
          const sub = JSON.parse(body);
          const list = readJson(paths.dataFile);
          list.unshift(sub);
          writeJson(paths.dataFile, list);
          const safeClass = normalizeVN(sub.className || '12A');
          const safeName = normalizeVN(sub.studentName || 'HocSinh');
          const wsId = normalizeVN(sub.worksheetId || 'phieubaitap');
          const fn = `${wsId}_${safeClass}_${safeName}_${Date.now()}.json`;
          fs.writeFileSync(path.join(paths.sheetsDir, fn), JSON.stringify(sub, null, 2), 'utf8');
          sendJson(res, 200, { status: 'ok', total: list.length, id: sub.id, slug });
        } catch (e) {
          sendJson(res, 400, { error: e.message });
        }
      });
      return;
    }

    if (req.method === 'GET' && cleanPath === '/api/submissions') {
      let list = readJson(paths.dataFile);
      const ws = reqUrl.query && reqUrl.query.worksheet;
      if (ws) {
        list = list.filter(item => item.worksheetId === ws || (!item.worksheetId && ws === 'phieu1'));
      }
      sendJson(res, 200, list);
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/reset') {
      const ws = reqUrl.query && reqUrl.query.worksheet;
      if (ws) {
        const list = readJson(paths.dataFile).filter(item => item.worksheetId !== ws);
        writeJson(paths.dataFile, list);
      } else {
        writeJson(paths.dataFile, []);
        try {
          for (const f of fs.readdirSync(paths.sheetsDir)) {
            fs.unlinkSync(path.join(paths.sheetsDir, f));
          }
        } catch (e) {}
      }
      sendJson(res, 200, { status: 'reset_ok', slug });
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/submit-hd3') {
      readBody(req, body => {
        try {
          const sub = JSON.parse(body);
          const safeClass = normalizeVN(sub.className || '12A');
          const safeMach = normalizeVN(sub.studentNumber || 'May00');
          const safeName = normalizeVN(sub.studentName || 'HocSinh');
          const filename = `${safeClass}_${safeMach}_${safeName}_${paths.defaultExtFile}`;
          sub.filename = filename;
          fs.writeFileSync(path.join(paths.hd3Dir, filename), sub.code || '', 'utf8');
          const list = readJson(paths.hd3DataFile);
          list.unshift(sub);
          writeJson(paths.hd3DataFile, list);
          sendJson(res, 200, { status: 'ok', filename, total: list.length, slug });
        } catch (e) {
          sendJson(res, 400, { error: e.message });
        }
      });
      return;
    }

    if (req.method === 'GET' && cleanPath === '/api/submissions-hd3') {
      sendJson(res, 200, readJson(paths.hd3DataFile));
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/reset-hd3') {
      writeJson(paths.hd3DataFile, []);
      try {
        for (const f of fs.readdirSync(paths.hd3Dir)) {
          if (f.endsWith('.html')) fs.unlinkSync(path.join(paths.hd3Dir, f));
        }
      } catch (e) {}
      sendJson(res, 200, { status: 'reset_hd3_ok', slug });
      return;
    }

    if ((req.method === 'GET' || req.method === 'HEAD') && (cleanPath === '/api/submissions-hd3-zip' || cleanPath === '/api/teacher/download-all-zip')) {
      try {
        const zipScript = path.join(paths.lessonDir, 'create_submissions_zip.py');
        if (fs.existsSync(zipScript)) {
          execFileSync('python3', ['create_submissions_zip.py'], { cwd: paths.lessonDir });
        }
        let zipPath = path.join(paths.lessonDir, paths.zipName);
        if (!fs.existsSync(zipPath)) {
          const foundZip = fs.readdirSync(paths.lessonDir).find(f => f.endsWith('.zip'));
          if (foundZip) zipPath = path.join(paths.lessonDir, foundZip);
        }
        if (fs.existsSync(zipPath)) {
          const data = fs.readFileSync(zipPath);
          res.writeHead(200, {
            'Content-Type': 'application/zip',
            'Content-Disposition': `attachment; filename="${path.basename(zipPath)}"`,
          });
          res.end(req.method === 'HEAD' ? undefined : data);
          return;
        }
      } catch (e) {}
      sendJson(res, 500, { error: 'Zip build failed' });
      return;
    }

    sendJson(res, 404, { error: 'Unknown API endpoint' });
    return;
  }

  // --- SERVE SAVED HD3 HTML SUBMISSIONS ---
  const hd3SubMatch = pathname.match(/^(?:\/(?:Bai\d+|ThucHanh_KTTX3|OnTap_HK1))?\/submissions_hd3_([a-z0-9]+)\/(.+)$/);
  if (req.method === 'GET' && hd3SubMatch) {
    const slug = hd3SubMatch[1];
    const paths = getLessonPaths(slug);
    const fname = path.basename(hd3SubMatch[2]);
    const fpath = path.join(paths.hd3Dir, fname);
    if (fs.existsSync(fpath) && fs.statSync(fpath).isFile()) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(fpath));
      return;
    }
  }

  // --- STATIC FILES WITH TEACHER PROTECTION ---
  let relPath = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  let fullPath = path.resolve(HUB_ROOT, relPath);
  if (!fullPath.startsWith(HUB_ROOT)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Forbidden');
    return;
  }
  if (fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory()) {
    fullPath = path.join(fullPath, 'index.html');
  }

  const ext = path.extname(fullPath).toLowerCase();
  const base = path.basename(fullPath);
  if ((ext === '.docx' || ext === '.pptx' || base.includes('KHBD') || base.includes('_TrinhChieu')) && !isTeacher(req)) {
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
  console.log(`Tin12 Hub Server listening on http://localhost:${PORT}`);
});
