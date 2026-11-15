/**
 * HUB SERVER HỢP NHẤT — TIN HỌC 12 (THTH-DHSP)
 * Phục vụ toàn bộ portal Tin12/index.html và tất cả bài học Bai7..Bai15, ThucHanh_KTTX3, OnTap_HK1
 * Khởi chạy: node hub_server.js (mặc định Port 3020)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const PORT = process.env.PORT || 3020;
const HUB_ROOT = __dirname;
const AUTH_SECRET = process.env.TIN12_AUTH_SECRET || 'thth-dhsp-tin12-exam-gate-2026-secret-k9x2m';
const TEACHER_EMAIL = 'darber3110@gmail.com';
const EXPECTED_TEACHER_SIG = crypto.createHmac('sha256', AUTH_SECRET).update('teacher:' + TEACHER_EMAIL).digest('hex');

const EXAM_BANKS_FILE = path.join(HUB_ROOT, 'exam_banks.private.json');
const EXAM_STATE_FILE = path.join(HUB_ROOT, 'data', 'exam_state.private.json');

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

function readJson(filePath, fallback = []) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); }
  catch (e) { return fallback; }
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
    const clean = {
      id: q.id,
      type: q.type,
      points: q.points,
      prompt: q.prompt,
    };
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
  return String(str)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D')
    .replace(/[^a-zA-Z0-9_-]/g, '_')
    .replace(/_+/g, '_');
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
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extraHeaders });
  res.end(JSON.stringify(payload));
}

const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  const rawPathname = decodeURIComponent(reqUrl.pathname || '/');
  const pathname = stripBasePrefix(rawPathname);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Teacher-Token');
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
          const email = String(payload.email || payload.username || '').trim().toLowerCase();
          if (TEACHER_PASSWORDS.includes(password) && (!email || email === TEACHER_EMAIL)) {
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
            sendJson(res, 401, { authenticated: false, success: false, error: 'Sai email hoặc mật khẩu giáo viên' });
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

    // --- EXAM GATING ENDPOINTS ---
    if (req.method === 'GET' && cleanPath === '/api/exam/status') {
      const banks = loadExamBanks();
      const showAll = reqUrl.query && reqUrl.query.all === '1';
      const now = Date.now();
      const exams = {};
      Object.keys(banks).forEach(k => {
        const b = banks[k];
        if (!showAll && b.slug !== slug) return;
        const { st } = getEffectiveExamState(k);
        const remSec = (st.isOpen && st.openUntil) ? Math.max(0, Math.ceil((st.openUntil - now) / 1000)) : null;
        exams[k] = {
          key: k,
          slug: b.slug,
          folder: b.folder,
          worksheetId: b.worksheetId,
          file: b.file,
          title: b.title,
          minutes: b.minutes,
          isOpen: !!st.isOpen,
          openUntil: st.openUntil,
          remainingOpenSec: remSec,
          allowReview: !!st.allowReview,
          updatedAt: st.updatedAt,
        };
      });
      sendJson(res, 200, {
        isTeacher: isVerifiedTeacher(req),
        serverNow: now,
        exams,
      });
      return;
    }

    if (req.method === 'GET' && cleanPath === '/api/exam') {
      const banks = loadExamBanks();
      const examId = String((reqUrl.query && reqUrl.query.examId) || 'phieubaitap').trim();
      const key = `${slug}:${examId}`;
      const bank = banks[key];
      if (!bank) {
        sendJson(res, 404, { error: 'Exam not found' });
        return;
      }
      const teacher = isVerifiedTeacher(req);
      const { st } = getEffectiveExamState(key);
      if (!st.isOpen && !teacher) {
        sendJson(res, 403, {
          locked: true,
          isOpen: false,
          isTeacher: false,
          key,
          title: bank.title,
          badge: bank.badge,
          desc: bank.desc,
          minutes: bank.minutes,
          allowReview: !!st.allowReview,
          message: 'Đề kiểm tra đang khóa. Giáo viên sẽ mở đề đúng giờ kiểm tra trên lớp.',
        });
        return;
      }
      const now = Date.now();
      const remSec = (st.isOpen && st.openUntil) ? Math.max(0, Math.ceil((st.openUntil - now) / 1000)) : null;
      sendJson(res, 200, {
        locked: false,
        isOpen: !!st.isOpen,
        openUntil: st.openUntil,
        remainingOpenSec: remSec,
        allowReview: !!st.allowReview,
        isTeacher: teacher,
        key,
        title: bank.title,
        badge: bank.badge,
        desc: bank.desc,
        minutes: bank.minutes,
        questions: sanitizeQuestions(bank.questions),
        ...(teacher ? { teacherQuestions: bank.questions } : {}),
      });
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/exam/control') {
      if (!isVerifiedTeacher(req)) {
        sendJson(res, 401, { error: 'Phiên Giáo viên chưa xác thực bảo mật. Vui lòng đăng nhập lại mật khẩu Giáo viên.' });
        return;
      }
      readBody(req, body => {
        try {
          const payload = JSON.parse(body || '{}');
          const banks = loadExamBanks();
          const examId = String(payload.examId || 'phieubaitap').trim();
          const key = `${slug}:${examId}`;
          if (!banks[key]) {
            sendJson(res, 404, { error: 'Exam not found' });
            return;
          }
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
          sendJson(res, 200, {
            key,
            isOpen: !!st.isOpen,
            openUntil: st.openUntil,
            remainingOpenSec: remSec,
            allowReview: !!st.allowReview,
            updatedAt: st.updatedAt,
            serverNow: now,
          });
        } catch (e) {
          sendJson(res, 400, { error: e.message });
        }
      });
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/exam/submit') {
      readBody(req, body => {
        try {
          const payload = JSON.parse(body || '{}');
          const banks = loadExamBanks();
          const examId = String(payload.examId || 'phieubaitap').trim();
          const key = `${slug}:${examId}`;
          const bank = banks[key];
          if (!bank) {
            sendJson(res, 404, { error: 'Exam not found' });
            return;
          }
          const teacher = isVerifiedTeacher(req);
          const { st } = getEffectiveExamState(key);
          const graceActive = !!(st.closedAt && (Date.now() - st.closedAt <= 120000));
          if (!st.isOpen && !graceActive && !teacher) {
            sendJson(res, 403, { error: 'Đề kiểm tra đang khóa, không nhận bài nộp ngoài giờ kiểm tra!' });
            return;
          }

          let totalScore = 0;
          let maxScore = 0;
          const cleanAnswers = {};
          const results = {};
          const inAns = (payload.answers && typeof payload.answers === 'object') ? payload.answers : {};

          for (const q of bank.questions) {
            const maxQ = Number(q.points || 1.0);
            maxScore += maxQ;
            if (q.type === 'tf') {
              const rawUserTF = (inAns[q.id] && typeof inAns[q.id] === 'object') ? inAns[q.id] : {};
              const userTF = {};
              const okMap = {};
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

          const list = readJson(paths.dataFile, []);
          list.unshift(sub);
          writeJson(paths.dataFile, list);
          const safeClass = normalizeVN(sub.className || '12A');
          const safeName = normalizeVN(sub.studentName || 'HocSinh');
          const wsId = normalizeVN(examId);
          const fn = `${wsId}_${safeClass}_${safeName}_${Date.now()}.json`;
          fs.writeFileSync(path.join(paths.sheetsDir, fn), JSON.stringify(sub, null, 2), 'utf8');

          sendJson(res, 200, {
            status: 'ok',
            id: sub.id,
            score: norm10,
            totalScore: +totalScore.toFixed(2),
            maxScore: +maxScore.toFixed(2),
            allowReview: !!st.allowReview,
            review: st.allowReview ? buildReviewPayload(bank.questions, results) : null,
          });
        } catch (e) {
          sendJson(res, 400, { error: e.message });
        }
      });
      return;
    }

    if (req.method === 'GET' && cleanPath === '/api/exam/review') {
      const banks = loadExamBanks();
      const examId = String((reqUrl.query && reqUrl.query.examId) || 'phieubaitap').trim();
      const subId = String((reqUrl.query && reqUrl.query.subId) || '').trim();
      const key = `${slug}:${examId}`;
      const bank = banks[key];
      if (!bank) {
        sendJson(res, 404, { error: 'Exam not found' });
        return;
      }
      const { st } = getEffectiveExamState(key);
      if (!st.allowReview && !isVerifiedTeacher(req)) {
        sendJson(res, 403, { allowReview: false, message: 'Giáo viên chưa bật chế độ xem đáp án chi tiết.' });
        return;
      }
      const list = readJson(paths.dataFile, []);
      const sub = list.find(item => item.id === subId);
      if (!sub) {
        sendJson(res, 404, { error: 'Không tìm thấy bài nộp.' });
        return;
      }
      sendJson(res, 200, {
        allowReview: true,
        review: buildReviewPayload(bank.questions, sub.results || {}),
      });
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/submit') {
      readBody(req, body => {
        try {
          const sub = JSON.parse(body);
          const banks = loadExamBanks();
          if (banks[`${slug}:${sub.worksheetId || ''}`]) {
            sendJson(res, 403, { error: 'Đề kiểm tra bắt buộc nộp qua /api/exam/submit' });
            return;
          }
          const list = readJson(paths.dataFile, []);
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
      let list = readJson(paths.dataFile, []);
      const ws = reqUrl.query && reqUrl.query.worksheet;
      if (ws) {
        list = list.filter(item => item.worksheetId === ws || (!item.worksheetId && ws === 'phieu1'));
      }
      if (!isVerifiedTeacher(req)) {
        list = list.map(s => ({
          id: s.id,
          worksheetId: s.worksheetId,
          isPair: s.isPair,
          studentName: s.studentName,
          className: s.className,
          studentNumber: s.studentNumber,
          score: s.score,
          submittedAt: s.submittedAt,
        }));
      }
      sendJson(res, 200, list);
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/reset') {
      if (!isVerifiedTeacher(req)) {
        sendJson(res, 401, { error: 'Chỉ Giáo viên được phép xóa danh sách điểm.' });
        return;
      }
      const ws = reqUrl.query && reqUrl.query.worksheet;
      if (ws) {
        const list = readJson(paths.dataFile, []).filter(item => item.worksheetId !== ws);
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
          const list = readJson(paths.hd3DataFile, []);
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
      sendJson(res, 200, readJson(paths.hd3DataFile, []));
      return;
    }

    if (req.method === 'POST' && cleanPath === '/api/reset-hd3') {
      if (!isVerifiedTeacher(req)) {
        sendJson(res, 401, { error: 'Chỉ Giáo viên được phép xóa bài thực hành.' });
        return;
      }
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

  // --- STATIC FILES WITH TEACHER & PRIVATE DATA PROTECTION ---
  let relPath = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  if (relPath.includes('.private.') || relPath === 'data' || relPath.startsWith('data/') || relPath.includes('/data/')) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 Forbidden');
    return;
  }

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
  if ((ext === '.docx' || ext === '.pptx' || base.includes('KHBD') || base.includes('_TrinhChieu')) && !isVerifiedTeacher(req)) {
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
