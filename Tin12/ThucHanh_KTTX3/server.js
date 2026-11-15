/**
 * BACKEND NODE.JS - THỰC HÀNH TỔNG HỢP HTML & KTTX3 (TIN HỌC 12 • THTH-DHSP)
 * Hệ thống thu thập bài nộp, kiểm tra trực tuyến & bảng điều khiển Giáo viên Realtime
 * Chạy độc lập: node server.js (Port 3014) hoặc qua Tin12/hub_server.js (Port 3020)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const crypto = require('crypto');
const { execSync } = require('child_process');

const PORT = process.env.PORT || 3014;
const CURRENT_DIR = __dirname;
const ROOT_DIR = CURRENT_DIR;
const SLUG = 'kttx3';
const AUTH_SECRET = process.env.TIN12_AUTH_SECRET || 'thth-dhsp-tin12-exam-gate-2026-secret-k9x2m';
const TEACHER_EMAIL = 'darber3110@gmail.com';
const EXPECTED_TEACHER_SIG = crypto.createHmac('sha256', AUTH_SECRET).update('teacher:' + TEACHER_EMAIL).digest('hex');
const EXAM_BANKS_FILE = path.join(CURRENT_DIR, '..', 'exam_banks.private.json');
const EXAM_STATE_FILE = path.join(CURRENT_DIR, '..', 'data', 'exam_state.private.json');
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

function readJson(filePath, fallback = []) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); }
  catch (e) { return fallback; }
}
function writeJson(filePath, data) {
  try {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (e) { return false; }
}
function loadExamBanks() {
  return readJson(EXAM_BANKS_FILE, {});
}
function defaultExamState() {
  return { isOpen: false, openUntil: null, closedAt: null, allowReview: false, updatedAt: null };
}
function loadAllExamStates() {
  const raw = readJson(EXAM_STATE_FILE, {});
  return (raw && typeof raw === 'object' && !Array.isArray(raw)) ? raw : {};
}
function getEffectiveExamState(key) {
  const states = loadAllExamStates();
  const st = { ...defaultExamState(), ...(states[key] || {}) };
  if (st.isOpen && st.openUntil && Date.now() > st.openUntil) {
    st.isOpen = false;
    st.closedAt = st.openUntil;
    st.openUntil = null;
    st.updatedAt = new Date().toISOString();
    states[key] = st;
    writeJson(EXAM_STATE_FILE, states);
  }
  return { st, states };
}
function sanitizeQuestions(questions) {
  return (questions || []).map(q => {
    const clean = { id: q.id, type: q.type, points: q.points, prompt: q.prompt };
    if (q.code) clean.code = q.code;
    if (q.type === 'tf') {
      clean.statements = (q.statements || []).map(s => ({ text: s.text }));
    } else if (q.options) {
      clean.options = q.options;
    }
    return clean;
  });
}
function buildReviewPayload(questions, results) {
  const resMap = results || {};
  const review = {};
  (questions || []).forEach(q => {
    const r = resMap[q.id] || {};
    if (q.type === 'tf') {
      const okMap = r.okMap || {};
      const ua = r.userAnswer || {};
      const letters = ['a', 'b', 'c', 'd'];
      const stList = letters.map((letter, si) => {
        const corBool = !!(q.statements && q.statements[si] && q.statements[si].correct);
        const corStr = corBool ? 'Đúng' : 'Sai';
        const hit = typeof okMap[letter] === 'boolean' ? okMap[letter] : (ua[letter] === corStr);
        return { letter, correct: corBool, ok: hit };
      });
      review[q.id] = {
        type: 'tf',
        score: Number(r.score || 0),
        correctCnt: Number(r.correctCnt || stList.filter(x => x.ok).length),
        explain: q.explain || '',
        statements: stList,
      };
    } else {
      review[q.id] = {
        type: 'mcq',
        correct: q.correct,
        ok: typeof r.isCorrect === 'boolean' ? r.isCorrect : (r.userAnswer === q.correct),
        userVal: r.userAnswer || '',
        score: Number(r.score || 0),
        explain: q.explain || '',
      };
    }
  });
  return review;
}
function normalizeVN(str) {
  if (!str) return 'HocSinh';
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_').replace(/_+/g, '_');
}
function parseCookies(req) {
  const out = {};
  String(req.headers.cookie || '').split(';').forEach(part => {
    const idx = part.indexOf('=');
    if (idx > 0) {
      const k = part.slice(0, idx).trim();
      try { out[k] = decodeURIComponent(part.slice(idx + 1).trim()); }
      catch (e) { out[k] = part.slice(idx + 1).trim(); }
    }
  });
  return out;
}
function isVerifiedTeacher(req) {
  const cookies = parseCookies(req);
  const hdrToken = String(req.headers['x-teacher-token'] || '').trim();
  return cookies.thth_teacher_sig === EXPECTED_TEACHER_SIG || hdrToken === EXPECTED_TEACHER_SIG;
}
function isTeacher(req) {
  return isVerifiedTeacher(req);
}
function sendJson(res, status, payload, extraHeaders = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extraHeaders });
  res.end(JSON.stringify(payload));
}
function cleanApiPath(p) {
  const prefix = '/api/kttx3';
  if (p.startsWith(prefix + '/')) return '/api/' + p.slice(prefix.length + 1);
  if (p === prefix) return '/api';
  return p;
}

const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  const cleanPath = cleanApiPath(reqUrl.pathname);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Teacher-Token');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  if (req.method === 'POST' && cleanPath === '/api/auth/login') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const { email, password } = JSON.parse(body || '{}');
        const cleanEmail = String(email || '').trim().toLowerCase();
        if (TEACHER_PASSWORDS.includes(String(password || '').trim()) && (!cleanEmail || cleanEmail === TEACHER_EMAIL)) {
          res.setHeader('Set-Cookie', [
            'thth_teacher=1; Path=/; SameSite=Lax',
            `thth_teacher_sig=${EXPECTED_TEACHER_SIG}; Path=/; HttpOnly; SameSite=Lax`,
          ]);
          sendJson(res, 200, {
            authenticated: true,
            role: 'teacher',
            email: TEACHER_EMAIL,
            name: 'Nguyễn Lê Minh Ngọc',
            full_name: 'Nguyễn Lê Minh Ngọc',
            token: EXPECTED_TEACHER_SIG,
          });
        } else {
          sendJson(res, 401, { authenticated: false, error: 'Sai email hoặc mật khẩu giáo viên' });
        }
      } catch (e) {
        sendJson(res, 400, { error: e.message });
      }
    });
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/auth/logout') {
    res.setHeader('Set-Cookie', [
      'thth_teacher=; Max-Age=0; Path=/; SameSite=Lax',
      'thth_teacher_sig=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax',
    ]);
    sendJson(res, 200, { authenticated: false });
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/exam/status') {
    const banks = loadExamBanks();
    const showAll = reqUrl.query && reqUrl.query.all === '1';
    const now = Date.now();
    const exams = {};
    Object.keys(banks).forEach(k => {
      const b = banks[k];
      if (!showAll && b.slug !== SLUG) return;
      const { st } = getEffectiveExamState(k);
      const remSec = (st.isOpen && st.openUntil) ? Math.max(0, Math.ceil((st.openUntil - now) / 1000)) : null;
      exams[k] = {
        key: k, slug: b.slug, folder: b.folder, worksheetId: b.worksheetId, file: b.file,
        title: b.title, minutes: b.minutes, isOpen: !!st.isOpen, openUntil: st.openUntil,
        remainingOpenSec: remSec, allowReview: !!st.allowReview, updatedAt: st.updatedAt,
      };
    });
    sendJson(res, 200, { isTeacher: isVerifiedTeacher(req), serverNow: now, exams });
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/exam') {
    const banks = loadExamBanks();
    const examId = String((reqUrl.query && reqUrl.query.examId) || 'phieubaitap').trim();
    const key = `${SLUG}:${examId}`;
    const bank = banks[key];
    if (!bank) { sendJson(res, 404, { error: 'Exam not found' }); return; }
    const teacher = isVerifiedTeacher(req);
    const { st } = getEffectiveExamState(key);
    if (!st.isOpen && !teacher) {
      sendJson(res, 403, {
        locked: true, isOpen: false, isTeacher: false, key,
        title: bank.title, badge: bank.badge, desc: bank.desc, minutes: bank.minutes,
        allowReview: !!st.allowReview,
        message: 'Đề kiểm tra đang khóa. Giáo viên sẽ mở đề đúng giờ kiểm tra trên lớp.',
      });
      return;
    }
    const now = Date.now();
    const remSec = (st.isOpen && st.openUntil) ? Math.max(0, Math.ceil((st.openUntil - now) / 1000)) : null;
    sendJson(res, 200, {
      locked: false, isOpen: !!st.isOpen, openUntil: st.openUntil, remainingOpenSec: remSec,
      allowReview: !!st.allowReview, isTeacher: teacher, key, title: bank.title, badge: bank.badge,
      desc: bank.desc, minutes: bank.minutes, questions: sanitizeQuestions(bank.questions),
      ...(teacher ? { teacherQuestions: bank.questions } : {}),
    });
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/exam/control') {
    if (!isVerifiedTeacher(req)) {
      sendJson(res, 401, { error: 'Phiên Giáo viên chưa xác thực bảo mật. Vui lòng đăng nhập lại.' });
      return;
    }
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const banks = loadExamBanks();
        const examId = String(payload.examId || 'phieubaitap').trim();
        const key = `${SLUG}:${examId}`;
        if (!banks[key]) { sendJson(res, 404, { error: 'Exam not found' }); return; }
        const action = String(payload.action || '').trim();
        const { st, states } = getEffectiveExamState(key);
        if (action === 'open') {
          const mins = Number(payload.durationMinutes || 0);
          st.isOpen = true;
          st.openUntil = mins > 0 ? Date.now() + mins * 60000 : null;
          st.closedAt = null;
          st.allowReview = Boolean(payload.allowReview);
          st.updatedAt = new Date().toISOString();
        } else if (action === 'close') {
          st.isOpen = false;
          st.openUntil = null;
          st.closedAt = Date.now();
          if (typeof payload.allowReview === 'boolean') st.allowReview = payload.allowReview;
          st.updatedAt = new Date().toISOString();
        } else if (action === 'set_review') {
          st.allowReview = Boolean(payload.allowReview);
          st.updatedAt = new Date().toISOString();
        } else {
          sendJson(res, 400, { error: 'Invalid control action' });
          return;
        }
        states[key] = st;
        writeJson(EXAM_STATE_FILE, states);
        const now = Date.now();
        const remSec = (st.isOpen && st.openUntil) ? Math.max(0, Math.ceil((st.openUntil - now) / 1000)) : null;
        sendJson(res, 200, { key, isOpen: !!st.isOpen, openUntil: st.openUntil, remainingOpenSec: remSec, allowReview: !!st.allowReview, updatedAt: st.updatedAt, serverNow: now });
      } catch (e) { sendJson(res, 400, { error: e.message }); }
    });
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/exam/submit') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const banks = loadExamBanks();
        const examId = String(payload.examId || 'phieubaitap').trim();
        const key = `${SLUG}:${examId}`;
        const bank = banks[key];
        if (!bank) { sendJson(res, 404, { error: 'Exam not found' }); return; }
        const teacher = isVerifiedTeacher(req);
        const { st } = getEffectiveExamState(key);
        const graceActive = !!(st.closedAt && (Date.now() - st.closedAt <= 120000));
        if (!st.isOpen && !graceActive && !teacher) {
          sendJson(res, 403, { error: 'Đề kiểm tra đang khóa, không nhận bài nộp ngoài giờ kiểm tra!' });
          return;
        }
        let totalScore = 0, maxScore = 0;
        const cleanAnswers = {}, results = {};
        const inAns = (payload.answers && typeof payload.answers === 'object') ? payload.answers : {};
        for (const q of bank.questions) {
          const maxQ = Number(q.points || 1.0);
          maxScore += maxQ;
          if (q.type === 'tf') {
            const rawUserTF = (inAns[q.id] && typeof inAns[q.id] === 'object') ? inAns[q.id] : {};
            const userTF = {}, okMap = {};
            let correctCnt = 0;
            ['a', 'b', 'c', 'd'].forEach((letter, si) => {
              const val = String(rawUserTF[letter] || '');
              userTF[letter] = val;
              const stItem = (q.statements || [])[si] || {};
              const target = stItem.correct ? 'Đúng' : 'Sai';
              const hit = val === target;
              okMap[letter] = hit;
              if (hit) correctCnt++;
            });
            const ratio = correctCnt === 4 ? 1.0 : (correctCnt === 3 ? 0.5 : (correctCnt === 2 ? 0.25 : (correctCnt === 1 ? 0.1 : 0.0)));
            const qScore = +(maxQ * ratio).toFixed(2);
            totalScore += qScore;
            cleanAnswers[q.id] = userTF;
            results[q.id] = { userAnswer: userTF, score: qScore, correctCnt, okMap };
          } else {
            const val = String(inAns[q.id] || '');
            const ok = val === q.correct;
            const qScore = ok ? maxQ : 0;
            totalScore += qScore;
            cleanAnswers[q.id] = val;
            results[q.id] = { userAnswer: val, correctAnswer: q.correct, isCorrect: ok, score: qScore };
          }
        }
        const norm10 = maxScore > 0 ? +(totalScore / maxScore * 10).toFixed(2) : 0;
        const now = new Date();
        const sub = {
          id: 'EX-' + crypto.randomBytes(3).toString('hex').toUpperCase(),
          worksheetId: examId,
          isPair: Boolean(payload.isPair),
          studentName: String(payload.studentName || 'Học sinh').trim() || 'Học sinh',
          className: String(payload.className || '12A1').trim() || '12A1',
          studentNumber: String(payload.studentNumber || 'Máy HS').trim() || 'Máy HS',
          score: norm10,
          submittedAt: now.toLocaleTimeString('vi-VN') + ' - ' + now.toLocaleDateString('vi-VN'),
          answers: cleanAnswers,
          results,
        };
        const list = readJson(DATA_FILE, []);
        list.unshift(sub);
        writeJson(DATA_FILE, list);
        const safeClass = normalizeVN(sub.className || '12A');
        const safeName = normalizeVN(sub.studentName || 'HocSinh');
        const wsId = normalizeVN(examId);
        const fn = `${wsId}_${safeClass}_${safeName}_${Date.now()}.json`;
        fs.writeFileSync(path.join(SHEETS_DIR, fn), JSON.stringify(sub, null, 2), 'utf8');
        sendJson(res, 200, {
          status: 'ok', id: sub.id, score: norm10,
          totalScore: +totalScore.toFixed(2), maxScore: +maxScore.toFixed(2),
          allowReview: !!st.allowReview,
          review: st.allowReview ? buildReviewPayload(bank.questions, results) : null,
        });
      } catch (e) { sendJson(res, 400, { error: e.message }); }
    });
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/exam/review') {
    const banks = loadExamBanks();
    const examId = String((reqUrl.query && reqUrl.query.examId) || 'phieubaitap').trim();
    const subId = String((reqUrl.query && reqUrl.query.subId) || '').trim();
    const key = `${SLUG}:${examId}`;
    const bank = banks[key];
    if (!bank) { sendJson(res, 404, { error: 'Exam not found' }); return; }
    const { st } = getEffectiveExamState(key);
    if (!st.allowReview && !isVerifiedTeacher(req)) {
      sendJson(res, 403, { allowReview: false, message: 'Giáo viên chưa bật chế độ xem đáp án chi tiết.' });
      return;
    }
    const list = readJson(DATA_FILE, []);
    const sub = list.find(item => item.id === subId);
    if (!sub) { sendJson(res, 404, { error: 'Không tìm thấy bài nộp.' }); return; }
    sendJson(res, 200, { allowReview: true, review: buildReviewPayload(bank.questions, sub.results || {}) });
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/submit') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const sub = JSON.parse(body);
        const banks = loadExamBanks();
        if (banks[`${SLUG}:${sub.worksheetId || ''}`]) {
          sendJson(res, 403, { error: 'Đề kiểm tra bắt buộc nộp qua /api/exam/submit' });
          return;
        }
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
    let list = readJson(DATA_FILE);
    const ws = reqUrl.query && reqUrl.query.worksheet;
    if (ws) list = list.filter(item => item.worksheetId === ws || (!item.worksheetId && ws === 'phieu1'));
    if (!isVerifiedTeacher(req)) {
      list = list.map(s => ({
        id: s.id, worksheetId: s.worksheetId, isPair: s.isPair,
        studentName: s.studentName, className: s.className, studentNumber: s.studentNumber,
        score: s.score, submittedAt: s.submittedAt,
      }));
    }
    sendJson(res, 200, list);
    return;
  }

  if (req.method === 'POST' && cleanPath === '/api/reset') {
    if (!isVerifiedTeacher(req)) { sendJson(res, 401, { error: 'Chỉ Giáo viên được phép xóa danh sách điểm.' }); return; }
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

  const sanitizeRelHtmlPath = (relPath) => {
    const parts = String(relPath || '').replace(/\\/g, '/').split('/').filter(Boolean);
    const safeParts = [];
    for (const seg of parts) {
      if (seg === '.' || seg === '..') continue;
      const cleaned = seg.replace(/[^a-zA-Z0-9._-]/g, '_');
      if (cleaned && cleaned !== '.' && cleaned !== '..') safeParts.push(cleaned);
    }
    if (!safeParts.length) return '';
    let last = safeParts[safeParts.length - 1];
    if (!/\.(html?|htm)$/i.test(last)) last += '.html';
    safeParts[safeParts.length - 1] = last;
    return safeParts.join('/');
  };

  if (req.method === 'POST' && cleanPath === '/api/submit-hd3') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const sub = JSON.parse(body);
        const safeClass = normalizeVN(sub.className || '12A');
        const safeMach = normalizeVN(sub.studentNumber || 'May00');
        const safeName = normalizeVN(sub.studentName || 'HocSinh');
        const folderName = `${safeClass}_${safeMach}_${safeName}`;
        const filename = `${folderName}_Website_CLB.html`;
        sub.filename = filename;
        fs.writeFileSync(path.join(HD3_DIR, filename), sub.code || '', 'utf8');
        if (sub.files && typeof sub.files === 'object' && !Array.isArray(sub.files)) {
          const studentDir = path.join(HD3_DIR, folderName);
          fs.mkdirSync(studentDir, { recursive: true });
          const savedFiles = {};
          for (const [rawRel, content] of Object.entries(sub.files)) {
            const safeRel = sanitizeRelHtmlPath(rawRel);
            if (!safeRel) continue;
            const destPath = path.join(studentDir, safeRel);
            fs.mkdirSync(path.dirname(destPath), { recursive: true });
            fs.writeFileSync(destPath, String(content || ''), 'utf8');
            savedFiles[safeRel] = String(content || '');
          }
          sub.files = savedFiles;
          sub.folderName = folderName;
        }
        const list = readJson(HD3_DATA_FILE);
        list.unshift(sub);
        writeJson(HD3_DATA_FILE, list);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ status: 'ok', filename, folderName, total: list.length }));
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
    if (!isVerifiedTeacher(req)) { sendJson(res, 401, { error: 'Chỉ Giáo viên được phép xóa bài thực hành.' }); return; }
    writeJson(HD3_DATA_FILE, []);
    try {
      for (const entry of fs.readdirSync(HD3_DIR, { withFileTypes: true })) {
        const full = path.join(HD3_DIR, entry.name);
        if (entry.isDirectory()) {
          fs.rmSync(full, { recursive: true, force: true });
        } else if (entry.name.endsWith('.html')) {
          fs.unlinkSync(full);
        }
      }
    } catch (e) {}
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'reset_hd3_ok' }));
    return;
  }

  if (req.method === 'GET' && cleanPath === '/api/submissions-hd3-zip') {
    try {
      execSync('python3 create_submissions_zip.py', { cwd: CURRENT_DIR });
      const zipPath = path.join(CURRENT_DIR, 'ThucHanh_KTTX3_HD3_TatCaBaiLam_THTH_DHSP.zip');
      if (fs.existsSync(zipPath)) {
        const data = fs.readFileSync(zipPath);
        res.writeHead(200, {
          'Content-Type': 'application/zip',
          'Content-Disposition': 'attachment; filename="ThucHanh_KTTX3_HD3_TatCaBaiLam_THTH_DHSP.zip"',
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
  const hd3SubPrefix = '/submissions_hd3_kttx3/';
  if (req.method === 'GET' && reqUrl.pathname.startsWith(hd3SubPrefix)) {
    const fname = path.basename(reqUrl.pathname);
    const fpath = path.join(HD3_DIR, fname);
    if (fs.existsSync(fpath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(fpath));
      return;
    }
  }

  // Static files with teacher & private data protection
  let relPath = reqUrl.pathname === '/' ? '/index.html' : reqUrl.pathname;
  relPath = decodeURIComponent(relPath).replace(/^\/+/, '');
  if (relPath.includes('.private.') || relPath === 'data' || relPath.startsWith('data/') || relPath.includes('/data/')) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 Forbidden');
    return;
  }
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
  console.log(`Thực hành tổng hợp HTML & KTTX3 Server listening on http://localhost:${PORT}`);
});
