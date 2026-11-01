/**
 * TIN HỌC 12 - HOẠT ĐỘNG 3: LUYỆN TẬP (30 PHÚT)
 * Logic Lập Trình Thực Hành, Live Preview & Quản Lý Nộp Bài
 * THTH-DHSP
 */

// --- NỘI DUNG VĂN BẢN KHỞI TẠO CHO HỌC SINH (CHƯA CÓ ĐÁP ÁN) ---
    // --- NỘI DUNG VĂN BẢN KHỞI TẠO CHO HỌC SINH (CHƯA CÓ ĐÁP ÁN) ---
    // Học sinh tự gõ toàn bộ cấu trúc chuẩn HTML5 cho Bài 1 & Bài 3
    const INITIAL_TEXTS = {
      // Để trống hoàn toàn để học sinh tự gõ cấu trúc HTML5 từ đầu
      bai1: '',
      bai2: '',
      bai3: ''
    };

    // VĂN BẢN MẪU THÔ ĐỂ HỌC SINH SAO CHÉP KHI CẦN (TIỆN LỢI, TRÁNH PHẢI GÕ LẠI NHIỀU CHỮ TIẾNG VIỆT)
    const SAMPLE_TEXTS = {
      bai1: `Biện luận số nghiệm của phương trình bậc 2

Bài toán: Xác định số nghiệm của phương trình ax2 + bx + c = 0 (a != 0)

Cách làm:
B1: Xác định hệ số a, b và c
B2: Tính delta = b2 - 4ac
B3: Kết luận
+ Nếu delta < 0: Phương trình vô nghiệm
+ Nếu delta = 0: Phương trình có nghiệm duy nhất
+ Nếu delta > 0: Phương trình có hai nghiệm phân biệt`,

      bai3: `INTERNET TỐC ĐỘ CAO

Dịch vụ Internet tốc độ cao là dịch vụ Internet cáp quang chất lượng cao, ổn định, giá cả hợp lí.

Các tính năng nổi bật:
Tốc độ siêu cao từ 150 MBps trở lên
Lắp đặt nhanh chóng trong 24 h
Phù hợp với cá nhân/Hộ gia đình
Tặng Modem 2 băng tần
Miễn phí lắp đặt
Hỗ trợ 24/7`
    };

    // HÀM SAO CHÉP VĂN BẢN MẪU VÀO CLIPBOARD
    function copySampleText(ex) {
      const text = SAMPLE_TEXTS[ex];
      if (!text) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          showToast(`Đã sao chép văn bản mẫu Bài ${ex === 'bai1' ? '1' : '3'} vào bộ nhớ tạm!`);
        }).catch(() => {
          fallbackCopyText(text, ex);
        });
      } else {
        fallbackCopyText(text, ex);
      }
    }

    function fallbackCopyText(text, ex) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        showToast(`Đã sao chép văn bản mẫu Bài ${ex === 'bai1' ? '1' : '3'} vào bộ nhớ tạm!`);
      } catch (err) {
        alert('Không thể tự động sao chép. Em hãy copy trực tiếp từ khung mẫu nhé!');
      }
      document.body.removeChild(ta);
    }

    let studentMode = 'single'; // 'single' hoặc 'pair'
    let currentExercise = 'bai1'; // 'bai1', 'bai2', 'bai3'
    let cachedHd3Submissions = [];

    // --- HIỂN THỊ THÔNG BÁO TOAST ---
    function showToast(msg) {
      const toast = document.getElementById('toast-msg');
      if (!toast) return;
      toast.textContent = msg;
      toast.style.display = 'block';
      setTimeout(() => {
        toast.style.display = 'none';
      }, 3000);
    }

    // --- QUẢN LÝ ĐỒNG HỒ ĐẾM GIỜ (TIMER 30 PHÚT) ---
    let timerSeconds = 30 * 60;
    let timerInterval = null;
    let isTimerRunning = false;

    function initTimer() {
      const display = document.getElementById('timer-display');
      const toggleBtn = document.getElementById('timer-toggle');
      const resetBtn = document.getElementById('timer-reset');
      const presetSelect = document.getElementById('timer-preset');

      if (!display) return;

      function updateTimerDisplay() {
        const mins = Math.floor(timerSeconds / 60);
        const secs = timerSeconds % 60;
        display.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        if (timerSeconds <= 60 && timerSeconds > 0) {
          display.style.color = '#dc2626';
          display.style.fontWeight = 'bold';
        } else {
          display.style.color = '';
          display.style.fontWeight = '';
        }
      }

      function startTimer() {
        if (isTimerRunning) return;
        isTimerRunning = true;
        if (toggleBtn) toggleBtn.innerHTML = '⏸ Dừng';
        timerInterval = setInterval(() => {
          if (timerSeconds > 0) {
            timerSeconds--;
            updateTimerDisplay();
          } else {
            clearInterval(timerInterval);
            isTimerRunning = false;
            if (toggleBtn) toggleBtn.innerHTML = '▶ Bắt đầu';
            showToast('⏰ Hết thời gian Hoạt động 3!');
          }
        }, 1000);
      }

      function pauseTimer() {
        isTimerRunning = false;
        clearInterval(timerInterval);
        if (toggleBtn) toggleBtn.innerHTML = '▶ Bắt đầu';
      }

      function resetTimer() {
        pauseTimer();
        const mins = parseInt(presetSelect?.value || '30', 10);
        timerSeconds = mins * 60;
        updateTimerDisplay();
      }

      toggleBtn?.addEventListener('click', () => {
        if (isTimerRunning) pauseTimer();
        else startTimer();
      });

      resetBtn?.addEventListener('click', resetTimer);

      presetSelect?.addEventListener('change', (e) => {
        const mins = parseInt(e.target.value, 10);
        timerSeconds = mins * 60;
        resetTimer();
      });

      updateTimerDisplay();
    }

    // --- QUẢN LÝ CHẾ ĐỘ TOÀN MÀN HÌNH / TRÌNH CHIẾU ---
    function initFullscreen() {
      const fsBtn = document.getElementById('btn-fullscreen');
      if (!fsBtn) return;

      fsBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().then(() => {
            fsBtn.innerHTML = '✕ Thu nhỏ';
            showToast('📺 Chế độ trình chiếu toàn màn hình');
          }).catch(err => console.warn(err));
        } else {
          document.exitFullscreen().then(() => {
            fsBtn.innerHTML = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg> Trình chiếu';
          });
        }
      });

      document.addEventListener('fullscreenchange', () => {
        if (!document.fullscreenElement) {
          fsBtn.innerHTML = '<svg class="icon-svg" viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg> Trình chiếu';
        }
      });
    }

    // --- HỖ TRỢ PHÍM TAB TRONG TRÌNH SOẠN THẢO (CODE EDITOR) ---
    function setupEditorKeyboard(textareaId) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
          e.preventDefault();
          const start = this.selectionStart;
          const end = this.selectionEnd;
          const value = this.value;

          // Chèn 2 dấu cách thụt lề
          this.value = value.substring(0, start) + '  ' + value.substring(end);
          this.selectionStart = this.selectionEnd = start + 2;

          const ex = textareaId.replace('code-', '');
          updateLivePreview(ex);
        }
      });
    }

    // ==============================================================
    // --- BẢO MẬT & XÁC THỰC QUYỀN GIÁO VIÊN (TEACHER AUTH) ---
    // ==============================================================
    const TEACHER_EMAIL = 'darber3110@gmail.com';

    function isTeacherAuthenticated() {
      try {
        const sess = sessionStorage.getItem('thth_teacher_auth') || localStorage.getItem('thth_teacher_auth');
        if (!sess) return false;
        const data = JSON.parse(sess);
        return data && data.authenticated && data.email && data.email.toLowerCase() === TEACHER_EMAIL.toLowerCase();
      } catch (e) {
        return false;
      }
    }

    function openTeacherLoginModal() {
      const modal = document.getElementById('teacher-auth-modal');
      const emailInput = document.getElementById('teacher-email-input');
      const alertBox = document.getElementById('teacher-auth-alert');
      if (alertBox) alertBox.style.display = 'none';
      if (emailInput && !emailInput.value) {
        emailInput.value = '';
      }
      modal?.classList.add('active');
      setTimeout(() => emailInput?.focus(), 150);
    }

    function closeTeacherLoginModal() {
      const modal = document.getElementById('teacher-auth-modal');
      modal?.classList.remove('active');
      const alertBox = document.getElementById('teacher-auth-alert');
      if (alertBox) alertBox.style.display = 'none';
    }

    function togglePasswordVisibility(inputId, btn) {
      const inp = document.getElementById(inputId);
      if (!inp) return;
      if (inp.type === 'password') {
        inp.type = 'text';
        if (btn) btn.textContent = '🙈 Ẩn mật khẩu';
      } else {
        inp.type = 'password';
        if (btn) btn.textContent = '👁️ Hiện mật khẩu';
      }
    }

    async function handleTeacherLogin(e) {
      if (e) e.preventDefault();
      const emailInput = document.getElementById('teacher-email-input');
      const pwdInput = document.getElementById('teacher-pwd-input');
      const rememberInput = document.getElementById('teacher-remember-me');
      const alertBox = document.getElementById('teacher-auth-alert');
      const submitBtn = document.querySelector('#teacher-login-form button[type="submit"]');

      const email = (emailInput?.value || '').trim().toLowerCase();
      const pwd = (pwdInput?.value || '').trim();

      if (!alertBox) return;

      if (!email || !pwd) {
        alertBox.style.display = 'block';
        alertBox.style.background = '#fef2f2';
        alertBox.style.color = '#991b1b';
        alertBox.style.border = '1px solid #fecaca';
        alertBox.innerHTML = '<strong>Vui lòng nhập đầy đủ Email và Mật khẩu!</strong>';
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Đang kiểm tra...';
      }

      let isAuthenticated = false;
      let teacherName = 'Thầy/Cô';

      // 1. XÁC THỰC TRỰC TIẾP QUA MINDA API (/api/auth/login)
      try {
        const formBody = new URLSearchParams();
        formBody.append('username', email);
        formBody.append('password', pwd);

        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formBody
        });

        if (res.ok) {
          const data = await res.json();
          if (data.role === 'teacher' || data.role === 'admin' || email === TEACHER_EMAIL.toLowerCase()) {
            isAuthenticated = true;
            teacherName = data.full_name || 'Giáo viên';
          }
        }
      } catch (err) {
        console.warn('API Minda không phản hồi, dùng xác thực dự phòng.');
      }

      // 2. DỰ PHÒNG NẾU OFFLINE HOẶC MÁY CỤC BỘ
      if (!isAuthenticated) {
        const customPwd = localStorage.getItem('thth_teacher_pwd');
        const validPwds = ['darber3110', '3110', '0902937006', '123456', 'admin', 'SfAUwbUtH3Bj1ouP2nM4'];
        if (customPwd) validPwds.push(customPwd);

        if (email === TEACHER_EMAIL.toLowerCase() && validPwds.includes(pwd)) {
          isAuthenticated = true;
          teacherName = 'Nguyễn Lê Minh Ngọc';
        }
      }

      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🔓 Đăng Nhập Vào Bảng Giáo Viên';
      }

      if (!isAuthenticated) {
        alertBox.style.display = 'block';
        alertBox.style.background = '#fef2f2';
        alertBox.style.color = '#991b1b';
        alertBox.style.border = '1px solid #fecaca';
        alertBox.innerHTML = `<strong>❌ Thông tin đăng nhập chưa chính xác!</strong><br>Vui lòng kiểm tra lại Email hoặc Mật khẩu tài khoản Giáo viên.`;
        pwdInput?.focus();
        return;
      }

      // 3. ĐĂNG NHẬP THÀNH CÔNG
      const authData = {
        email: email,
        name: teacherName,
        authenticated: true,
        loginAt: new Date().toISOString()
      };

      sessionStorage.setItem('thth_teacher_auth', JSON.stringify(authData));
      if (rememberInput && rememberInput.checked) {
        localStorage.setItem('thth_teacher_auth', JSON.stringify(authData));
      } else {
        localStorage.removeItem('thth_teacher_auth');
      }

      closeTeacherLoginModal();
      activateTeacherView();
      showToast(`Chào mừng ${teacherName} đã đăng nhập thành công!`);
    }

    function teacherLogout() {
      if (confirm('Thầy/Cô có chắc chắn muốn đăng xuất khỏi Bảng quản lý giáo viên?')) {
        sessionStorage.removeItem('thth_teacher_auth');
        localStorage.removeItem('thth_teacher_auth');
        activateStudentView();
        showToast('Đã đăng xuất tài khoản giáo viên!');
      }
    }

    function changeTeacherPassword() {
      const currentPwd = prompt(`[ĐỔI MẬT KHẨU GIÁO VIÊN]\nTài khoản: ${TEACHER_EMAIL}\nNhập mật khẩu mới cho tài khoản:`);
      if (currentPwd && currentPwd.trim().length >= 4) {
        localStorage.setItem('thth_teacher_pwd', currentPwd.trim());
        showToast('Đã cập nhật mật khẩu mới cho giáo viên thành công!');
      } else if (currentPwd !== null) {
        alert('Mật khẩu cần tối thiểu 4 ký tự!');
      }
    }

    function updateTeacherAuthUI() {
      const isAuth = isTeacherAuthenticated();
      const lockBadge = document.getElementById('teacher-lock-badge');
      const authStatus = document.getElementById('teacher-auth-status');
      const emailDisplay = document.getElementById('teacher-auth-email-display');

      if (isAuth) {
        if (lockBadge) {
          lockBadge.textContent = '✓ Đã xác thực';
          lockBadge.style.background = '#dcfce7';
          lockBadge.style.color = '#15803d';
          lockBadge.style.borderColor = '#bbf7d0';
        }
        if (authStatus) {
          authStatus.style.display = 'inline-flex';
        }
        if (emailDisplay) {
          emailDisplay.textContent = TEACHER_EMAIL;
        }
      } else {
        if (lockBadge) {
          lockBadge.textContent = '🔒 Cần đăng nhập';
          lockBadge.style.background = '#fef2f2';
          lockBadge.style.color = '#dc2626';
          lockBadge.style.borderColor = '#fecaca';
        }
        if (authStatus) {
          authStatus.style.display = 'none';
        }
      }
    }

    // --- CHUYỂN CHẾ ĐỘ XEM CHÍNH (HỌC SINH vs GIÁO VIÊN) ---
    function switchMainView(view) {
      if (view === 'teacher') {
        if (!isTeacherAuthenticated()) {
          openTeacherLoginModal();
          return;
        }
        activateTeacherView();
      } else {
        activateStudentView();
      }
    }

    function activateTeacherView() {
      const studentBtn = document.getElementById('btn-view-student');
      const teacherBtn = document.getElementById('btn-view-teacher');
      const studentCont = document.getElementById('view-student-container');
      const teacherCont = document.getElementById('view-teacher-container');

      studentBtn?.classList.remove('active');
      teacherBtn?.classList.add('active');
      if (studentCont) studentCont.style.display = 'none';
      teacherCont?.classList.add('active');

      updateTeacherAuthUI();
      loadHd3Submissions();
    }

    function activateStudentView() {
      const studentBtn = document.getElementById('btn-view-student');
      const teacherBtn = document.getElementById('btn-view-teacher');
      const studentCont = document.getElementById('view-student-container');
      const teacherCont = document.getElementById('view-teacher-container');

      teacherBtn?.classList.remove('active');
      studentBtn?.classList.add('active');
      teacherCont?.classList.remove('active');
      if (studentCont) studentCont.style.display = 'block';

      updateTeacherAuthUI();
    }

    // --- CHỌN HÌNH THỨC: CÁ NHÂN vs THEO CẶP ---
    function setStudentMode(mode) {
      studentMode = mode;
      const tab1 = document.getElementById('tab-mode-single');
      const tab2 = document.getElementById('tab-mode-pair');
      const box1 = document.getElementById('form-single-box');
      const box2 = document.getElementById('form-pair-box');

      if (mode === 'pair') {
        tab1.classList.remove('active');
        tab2.classList.add('active');
        box1.style.display = 'none';
        box2.style.display = 'block';
      } else {
        tab2.classList.remove('active');
        tab1.classList.add('active');
        box2.style.display = 'none';
        box1.style.display = 'block';
      }
      saveDraftInfo();
    }

    // --- CHUYỂN ĐỔI BÀI TẬP (BÀI 1, BÀI 2, BÀI 3) ---
    function switchExercise(ex) {
      currentExercise = ex;
      ['bai1', 'bai2', 'bai3'].forEach(id => {
        const btn = document.getElementById(`tab-btn-${id}`);
        const panel = document.getElementById(`panel-${id}`);
        if (id === ex) {
          btn?.classList.add('active');
          panel?.classList.add('active');
          updateLivePreview(id);
        } else {
          btn?.classList.remove('active');
          panel?.classList.remove('active');
        }
      });
    }

    // --- HÀM TẠO NỘI DUNG PREVIEW THÔNG MINH CHO TỪNG BÀI ---
    function getPreviewHtml(code) {
      if (!code || !code.trim()) {
        return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      padding: 40px 20px;
      margin: 0;
      color: #94a3b8;
      text-align: center;
      font-size: 0.95rem;
      background: #f8fafc;
    }
  <\/style>
<\/head>
<body>
  <div style="max-width: 450px; margin: 0 auto; border: 2px dashed #cbd5e1; border-radius: 8px; padding: 24px;">
    <div style="font-size: 1.8rem; margin-bottom: 8px;">🌐</div>
    <div style="font-weight: 600; color: #64748b; margin-bottom: 4px;">Chưa có mã HTML</div>
    <div style="font-size: 0.85rem; color: #94a3b8;">Em hãy tự gõ mã hoặc bấm nút [📄 Khung HTML5] để bắt đầu. Kết quả hiển thị trang web sẽ xuất hiện tại đây theo thời gian thực!</div>
  </div>
<\/body>
<\/html>`;
      }

      const lower = code.toLowerCase();
      // Nếu học sinh đã gõ cấu trúc hoàn chỉnh <!DOCTYPE> hoặc <html>
      if (lower.includes('<!doctype') || lower.includes('<html')) {
        return code;
      }

      // Nếu là đoạn mã nhỏ (fragment) như thẻ <p>, <h2>... (Bài 2 hoặc đang gõ dở)
      return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: 'Times New Roman', serif;
      padding: 16px 20px;
      margin: 0;
      line-height: 1.6;
      color: #0f172a;
      background: #ffffff;
    }
  <\/style>
<\/head>
<body>
  ${code}
<\/body>
<\/html>`;
    }

    // --- CẬP NHẬT PREVIEW CÁCH LY QUA IFRAME & TỰ ĐỘNG CHẤM TIÊU CHÍ ---
    function updateLivePreview(ex) {
      const textarea = document.getElementById(`code-${ex}`);
      const iframe = document.getElementById(`preview-frame-${ex}`);
      if (!textarea || !iframe) return;

      const code = textarea.value;
      iframe.srcdoc = getPreviewHtml(code);

      // Cập nhật trạng thái badge và đánh giá tiêu chí
      evaluateExerciseCriteria(ex, code);

      // Lưu nháp tự động
      try {
        localStorage.setItem(`bai8_hd3_draft_${ex}`, code);
      } catch (e) {}
    }

    // --- ĐÁNH GIÁ TIÊU CHÍ TỰ ĐỘNG (REALTIME CHECKLIST) ---
    function evaluateExerciseCriteria(ex, code) {
      const badge = document.getElementById(`status-badge-${ex}`);
      const lower = code.toLowerCase();

      if (ex === 'bai1') {
        const hasStruct = (/<html/i.test(code) && /<head/i.test(code) && /<body/i.test(code)) || (/<html/i.test(code) && /<body/i.test(code));
        const hasH = /<h[1-3][^>]*>.*<\/h[1-3]>/is.test(code);
        const hasRed = /color\s*:\s*(red|#f|#e|#d|rgb\(255)/i.test(code);
        const hasSup = /<sup[^>]*>.*<\/sup>/is.test(code);
        const hasSub = /<sub[^>]*>.*<\/sub>/is.test(code);
        const hasEm = /<(em|i)[^>]*>.*<\/(em|i)>/is.test(code);
        const hasWrap = /<p[^>]*>|<br\s*\/?>/i.test(code);

        setCritItem('crit-b1-struct', hasStruct);
        setCritItem('crit-b1-h', hasH);
        setCritItem('crit-b1-red', hasRed);
        setCritItem('crit-b1-sup', hasSup);
        setCritItem('crit-b1-sub', hasSub);
        setCritItem('crit-b1-em', hasEm);
        setCritItem('crit-b1-wrap', hasWrap);

        const score = [hasStruct, hasH, hasRed, hasSup, hasSub, hasEm, hasWrap].filter(Boolean).length;
        const scoreTag = document.getElementById('score-tag-bai1');
        if (scoreTag) {
          scoreTag.textContent = `${score}/7 tiêu chí đạt`;
          scoreTag.style.background = score >= 5 ? '#dcfce7' : '#e2e8f0';
          scoreTag.style.color = score >= 5 ? '#15803d' : '#475569';
        }

        if (badge) {
          if (score >= 5) {
            badge.textContent = '✓ Hoàn thành';
            badge.style.background = '#dcfce7'; badge.style.color = '#15803d';
          } else if (score > 0) {
            badge.textContent = 'Đang làm';
            badge.style.background = '#fef3c7'; badge.style.color = '#b45309';
          } else {
            badge.textContent = 'Chưa làm';
            badge.style.background = '#e2e8f0'; badge.style.color = '#475569';
          }
        }
      } else if (ex === 'bai2') {
        const hasStrong = /<strong[^>]*>.*<\/strong>/is.test(code);
        const hasEm = /<em[^>]*>.*<\/em>/is.test(code);
        const hasB = /<(b|i|mark)[^>]*>.*<\/(b|i|mark)>/is.test(code);

        setCritItem('crit-b2-strong', hasStrong);
        setCritItem('crit-b2-em', hasEm);
        setCritItem('crit-b2-b', hasB);

        const score = [hasStrong, hasEm, hasB].filter(Boolean).length;
        const scoreTag = document.getElementById('score-tag-bai2');
        if (scoreTag) {
          scoreTag.textContent = `${score}/3 tiêu chí đạt`;
          scoreTag.style.background = score >= 2 ? '#dcfce7' : '#e2e8f0';
          scoreTag.style.color = score >= 2 ? '#15803d' : '#475569';
        }

        if (badge) {
          if (score >= 2) {
            badge.textContent = '✓ Hoàn thành';
            badge.style.background = '#dcfce7'; badge.style.color = '#15803d';
          } else if (score > 0) {
            badge.textContent = 'Đang làm';
            badge.style.background = '#fef3c7'; badge.style.color = '#b45309';
          } else {
            badge.textContent = 'Chưa làm';
            badge.style.background = '#e2e8f0'; badge.style.color = '#475569';
          }
        }
      } else if (ex === 'bai3') {
        const hasStruct = (/<html/i.test(code) && /<head/i.test(code) && /<body/i.test(code)) || (/<html/i.test(code) && /<body/i.test(code));
        const hasTitle = /<h[1-2][^>]*>.*internet.*<\/h[1-2]>/is.test(code);
        const hasDesc = /<(em|i)[^>]*>.*<\/(em|i)>/is.test(code);
        const hasSub = /<h3[^>]*>|<strong[^>]*>/is.test(code);
        const hasList = /<(ul|ol|li)[^>]*>|<br\s*\/?>/is.test(code);

        setCritItem('crit-b3-struct', hasStruct);
        setCritItem('crit-b3-title', hasTitle);
        setCritItem('crit-b3-desc', hasDesc);
        setCritItem('crit-b3-sub', hasSub);
        setCritItem('crit-b3-list', hasList);

        const score = [hasStruct, hasTitle, hasDesc, hasSub, hasList].filter(Boolean).length;
        const scoreTag = document.getElementById('score-tag-bai3');
        if (scoreTag) {
          scoreTag.textContent = `${score}/5 tiêu chí đạt`;
          scoreTag.style.background = score >= 4 ? '#dcfce7' : '#e2e8f0';
          scoreTag.style.color = score >= 4 ? '#15803d' : '#475569';
        }

        if (badge) {
          if (score >= 4) {
            badge.textContent = '✓ Hoàn thành';
            badge.style.background = '#dcfce7'; badge.style.color = '#15803d';
          } else if (score > 0) {
            badge.textContent = 'Đang làm';
            badge.style.background = '#fef3c7'; badge.style.color = '#b45309';
          } else {
            badge.textContent = 'Chưa làm';
            badge.style.background = '#e2e8f0'; badge.style.color = '#475569';
          }
        }
      }
    }

    function setCritItem(id, passed) {
      const el = document.getElementById(id);
      if (!el) return;
      if (passed) {
        el.classList.add('passed');
        el.querySelector('.check-icon').textContent = '✓';
      } else {
        el.classList.remove('passed');
        el.querySelector('.check-icon').textContent = '○';
      }
    }

    // --- KHÔI PHỤC VĂN BẢN GỐC (RESET CODE VỀ TRẠNG THÁI CHƯA LÀM) ---
    function restoreInitialText(ex) {
      if (confirm(`Em có muốn khôi phục lại văn bản thô ban đầu của Bài tập ${ex === 'bai1' ? '1' : ex === 'bai2' ? '2' : '3'} không?`)) {
        const textarea = document.getElementById(`code-${ex}`);
        if (textarea) {
          textarea.value = INITIAL_TEXTS[ex] || '';
          updateLivePreview(ex);
          showToast(`Đã khôi phục văn bản ban đầu của ${ex.toUpperCase()}!`);
        }
      }
    }

    // --- CHÈN NHANH CÁC THẺ HTML (SNIPPETS THÔNG MINH) ---
    function insertHtmlSkeleton(textareaId, title) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const currentVal = textarea.value.trim();
      if (currentVal.length > 0 && !confirm('Thao tác này sẽ chèn khung cấu trúc HTML5 chuẩn. Em có muốn tiếp tục không?')) {
        return;
      }

      const skeleton = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>${title || 'Trang web của em'}<\/title>
<\/head>
<body>
  ${currentVal ? currentVal : '  <!-- Viết nội dung trang web tại đây -->'}
<\/body>
<\/html>`;

      textarea.value = skeleton;
      textarea.focus();
      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
      showToast('Đã chèn khung cấu trúc HTML5 chuẩn!');
    }

    function insertTag(textareaId, tag) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const selected = text.substring(start, end);

      const openTag = `<${tag}>`;
      const closeTag = `</${tag}>`;

      if (selected.length > 0) {
        // Bao bọc đoạn văn bản đang bôi đen
        const replacement = openTag + selected + closeTag;
        textarea.value = text.substring(0, start) + replacement + text.substring(end);
        textarea.focus();
        textarea.selectionStart = start + openTag.length;
        textarea.selectionEnd = start + openTag.length + selected.length;
      } else {
        // Chèn cặp thẻ và đặt con trỏ ở giữa
        const replacement = openTag + closeTag;
        textarea.value = text.substring(0, start) + replacement + text.substring(end);
        textarea.focus();
        textarea.selectionStart = start + openTag.length;
        textarea.selectionEnd = start + openTag.length;
      }

      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
    }

    function insertVoidTag(textareaId, tag) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const start = textarea.selectionStart;
      const text = textarea.value;
      const replacement = `<${tag}>\n`;

      textarea.value = text.substring(0, start) + replacement + text.substring(start);
      textarea.focus();
      textarea.selectionStart = textarea.selectionEnd = start + replacement.length;

      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
    }

    function insertSnippet(textareaId, openTag, closeTag) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const selected = text.substring(start, end) || 'Nội dung';

      const replacement = openTag + selected + closeTag;
      textarea.value = text.substring(0, start) + replacement + text.substring(end);
      textarea.focus();
      textarea.selectionStart = start + openTag.length;
      textarea.selectionEnd = start + openTag.length + selected.length;

      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
    }

    function insertStyledTag(textareaId, tag, style) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const selected = text.substring(start, end) || 'Nội dung';

      const openTag = style ? `<${tag} style="${style}">` : `<${tag}>`;
      const closeTag = `</${tag}>`;

      const replacement = openTag + selected + closeTag;
      textarea.value = text.substring(0, start) + replacement + text.substring(end);
      textarea.focus();
      textarea.selectionStart = start + openTag.length;
      textarea.selectionEnd = start + openTag.length + selected.length;

      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
    }

    function insertListSnippet(textareaId) {
      const textarea = document.getElementById(textareaId);
      if (!textarea) return;

      const start = textarea.selectionStart;
      const text = textarea.value;
      const snippet = `<ul>\n  <li>Tốc độ siêu cao từ 150 MBps trở lên</li>\n  <li>Lắp đặt nhanh chóng trong 24 h</li>\n  <li>Phù hợp với cá nhân/Hộ gia đình</li>\n  <li>Tặng Modem 2 băng tần</li>\n  <li>Miễn phí lắp đặt</li>\n  <li>Hỗ trợ 24/7</li>\n</ul>\n`;

      textarea.value = text.substring(0, start) + snippet + text.substring(start);
      textarea.focus();
      textarea.selectionStart = textarea.selectionEnd = start + snippet.length;

      const ex = textareaId.replace('code-', '');
      updateLivePreview(ex);
    }

    // --- LẤY THÔNG TIN HỌC SINH ---
    function getStudentInfo() {
      if (studentMode === 'pair') {
        const name1 = document.getElementById('pair-name-1')?.value.trim() || '';
        const stt1 = document.getElementById('pair-stt-1')?.value.trim() || '';
        const name2 = document.getElementById('pair-name-2')?.value.trim() || '';
        const stt2 = document.getElementById('pair-stt-2')?.value.trim() || '';
        const className = document.getElementById('pair-class-select')?.value || '';
        const machine = document.getElementById('pair-machine-input')?.value.trim() || 'N/A';

        let combinedName = '';
        if (name1 && name2) combinedName = `${name1} & ${name2}`;
        else combinedName = name1 || name2 || 'Nhóm học sinh';

        return {
          isPair: true,
          studentName: combinedName,
          student1: { name: name1, stt: stt1 },
          student2: { name: name2, stt: stt2 },
          className: className,
          studentNumber: machine
        };
      } else {
        const name = document.getElementById('student-name-input')?.value.trim() || '';
        const className = document.getElementById('student-class-select')?.value || '';
        const machine = document.getElementById('student-machine-input')?.value.trim() || 'N/A';

        return {
          isPair: false,
          studentName: name,
          className: className,
          studentNumber: machine
        };
      }
    }

    function saveDraftInfo() {
      try {
        const info = getStudentInfo();
        localStorage.setItem('bai8_hd3_student_info', JSON.stringify({ mode: studentMode, info }));
      } catch (e) {}
    }

    function loadDrafts() {
      try {
        // Tải thông tin học sinh
        const saved = JSON.parse(localStorage.getItem('bai8_hd3_student_info') || '{}');
        if (saved.mode) {
          setStudentMode(saved.mode);
        }
        if (saved.info) {
          if (saved.mode === 'pair') {
            if (document.getElementById('pair-name-1')) document.getElementById('pair-name-1').value = saved.info.student1?.name || '';
            if (document.getElementById('pair-stt-1')) document.getElementById('pair-stt-1').value = saved.info.student1?.stt || '';
            if (document.getElementById('pair-name-2')) document.getElementById('pair-name-2').value = saved.info.student2?.name || '';
            if (document.getElementById('pair-stt-2')) document.getElementById('pair-stt-2').value = saved.info.student2?.stt || '';
            if (document.getElementById('pair-class-select')) document.getElementById('pair-class-select').value = saved.info.className || '';
            if (document.getElementById('pair-machine-input')) document.getElementById('pair-machine-input').value = saved.info.studentNumber || '';
          } else {
            if (document.getElementById('student-name-input')) document.getElementById('student-name-input').value = saved.info.studentName || '';
            if (document.getElementById('student-class-select')) document.getElementById('student-class-select').value = saved.info.className || '';
            if (document.getElementById('student-machine-input')) document.getElementById('student-machine-input').value = saved.info.studentNumber || '';
          }
        }

        // Tải nháp code (nếu chưa có nháp, nạp văn bản ban đầu)
        ['bai1', 'bai2', 'bai3'].forEach(id => {
          let draftCode = localStorage.getItem(`bai8_hd3_draft_${id}`);
          const ta = document.getElementById(`code-${id}`);
          if (ta) {
            // Tự động làm sạch nếu nháp là bài giải mẫu cũ của phiên bản trước
            if (draftCode && (draftCode.includes('<strong style="color: red;">Bài toán:</strong>') || draftCode.includes('Thẻ <strong>strong</strong>') || draftCode.includes('INTERNET TỐC ĐỘ CAO</h2>'))) {
              draftCode = null;
              try { localStorage.removeItem(`bai8_hd3_draft_${id}`); } catch (e) {}
            }
            // Nếu nháp là văn bản thô cũ trước khi đổi sang để học sinh tự gõ cấu trúc
            if ((id === 'bai1' || id === 'bai3') && draftCode && !draftCode.includes('<') && !draftCode.includes('>')) {
              draftCode = null;
              try { localStorage.removeItem(`bai8_hd3_draft_${id}`); } catch (e) {}
            }

            if (draftCode !== null) {
              ta.value = draftCode;
            } else {
              ta.value = INITIAL_TEXTS[id] || '';
            }
          }
          updateLivePreview(id);
        });
      } catch (e) {}
    }

    // Chuẩn hóa chuỗi an toàn cho tên thư mục và tên tệp không dấu
    function sanitize(str) {
      if (!str) return 'HocSinh';
      return str
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/đ/g, 'd').replace(/Đ/g, 'D')
        .replace(/[^a-zA-Z0-9_-]/g, '_')
        .replace(/_+/g, '_')
        .trim();
    }

    // --- TẢI TỪNG TỆP HTML VỀ MÁY TÍNH HỌC SINH ---
    function downloadSingleHtml(ex, notify = true) {
      const textarea = document.getElementById(`code-${ex}`);
      const code = textarea ? textarea.value : '';
      const info = getStudentInfo();

      const safeClass = (info.className || '12A').replace(/[^a-zA-Z0-9]/g, '');
      const safeMachine = (info.studentNumber && info.studentNumber !== 'N/A') ? info.studentNumber.replace(/[^a-zA-Z0-9]/g, '') : '';
      const safeName = (info.studentName || 'HocSinh').replace(/[^a-zA-Z0-9_\u00C0-\u1EF9]/g, '_');
      const machinePart = safeMachine ? `_${safeMachine}` : '';
      const filename = `${safeClass}${machinePart}_${safeName}_${ex.toUpperCase()}.html`;

      const exTitles = {
        bai1: 'Bài 1: Phương trình bậc 2',
        bai2: 'Bài 2: Làm nổi bật ý chính',
        bai3: 'Bài 3: Internet tốc độ cao'
      };

      let fullHtml = code;
      if (!code.includes('<!DOCTYPE') && !code.includes('<html')) {
        fullHtml = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${exTitles[ex]} - ${info.studentName || 'Học sinh'} (${info.className || 'Tin 12'})<\/title>
  <style>
    body {
      font-family: 'Times New Roman', serif;
      padding: 24px;
      line-height: 1.6;
      color: #0f172a;
      max-width: 800px;
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
  <\/style>
<\/head>
<body>
  <div class="student-badge-header">
    <strong>🏫 THTH - DHSP - TIN HỌC 12</strong><br>
    <strong>Học sinh:</strong> ${info.studentName || 'Học sinh'} &nbsp;|&nbsp; 
    <strong>Lớp:</strong> ${info.className || 'Tin 12'} &nbsp;|&nbsp; 
    <strong>Số máy:</strong> ${info.studentNumber || 'N/A'}
  </div>
  ${code || '<p style="color:#94a3b8; font-style:italic;">(Chưa có nội dung)</p>'}
<\/body>
<\/html>`;
      }

      const blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      if (notify) {
        showToast(`Đã tải tệp ${filename} về máy!`);
      }
    }

    // --- TẢI VỀ MÁY CẢ 3 TỆP HTML CỦA HỌC SINH ---
    function downloadAllHtml() {
      const exercises = ['bai1', 'bai2', 'bai3'];
      exercises.forEach((ex, idx) => {
        setTimeout(() => {
          downloadSingleHtml(ex, false);
        }, idx * 300);
      });
      setTimeout(() => {
        showToast('Đã tải thành công cả 3 tệp HTML về máy tính của em!');
      }, 1000);
    }

    // --- TẢI FILE HTML TỪ TRONG CỬA SỔ XEM CHI TIẾT (WORK MODAL) ---
    function downloadCurrentModalHtml() {
      if (!currentModalStudent || !currentModalEx) return;
      const ex = currentModalEx;
      const fileObj = currentModalStudent.files ? currentModalStudent.files[ex] : null;
      const code = fileObj ? fileObj.code : (currentModalStudent[`${ex}Html`] || '');
      const safeClass = (currentModalStudent.className || '12A').replace(/[^a-zA-Z0-9]/g, '');
      const safeMachine = (currentModalStudent.studentNumber && currentModalStudent.studentNumber !== 'N/A') ? currentModalStudent.studentNumber.replace(/[^a-zA-Z0-9]/g, '') : '';
      const safeName = (currentModalStudent.studentName || 'HocSinh').replace(/[^a-zA-Z0-9_\u00C0-\u1EF9]/g, '_');
      const filename = fileObj?.filename || `${safeClass}_${safeMachine}_${safeName}_${ex.toUpperCase()}.html`;

      const exTitles = {
        bai1: 'Bài 1: Phương trình bậc 2',
        bai2: 'Bài 2: Làm nổi bật ý chính',
        bai3: 'Bài 3: Internet tốc độ cao'
      };

      const fullHtml = wrapInFullHtml(`${exTitles[ex]} - ${currentModalStudent.studentName}`, code);
      const blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      showToast(`Đã tải tệp ${filename} về máy!`);
    }

    // --- TẢI FILE HTML CỦA HỌC SINH TỪ BẢNG GIÁO VIÊN ---
    function downloadStudentWork(idx, ex, notify = true) {
      const sub = cachedHd3Submissions[idx];
      if (!sub) return;
      const fileObj = sub.files ? sub.files[ex] : null;
      const code = fileObj ? fileObj.code : (sub[`${ex}Html`] || '');
      const safeClass = (sub.className || '12A').replace(/[^a-zA-Z0-9]/g, '');
      const safeMachine = (sub.studentNumber && sub.studentNumber !== 'N/A') ? sub.studentNumber.replace(/[^a-zA-Z0-9]/g, '') : '';
      const safeName = (sub.studentName || 'HocSinh').replace(/[^a-zA-Z0-9_\u00C0-\u1EF9]/g, '_');
      const filename = fileObj?.filename || `${safeClass}_${safeMachine}_${safeName}_${ex.toUpperCase()}.html`;

      const exTitles = {
        bai1: 'Bài 1: Phương trình bậc 2',
        bai2: 'Bài 2: Làm nổi bật ý chính',
        bai3: 'Bài 3: Internet tốc độ cao'
      };

      const fullHtml = wrapInFullHtml(`${exTitles[ex]} - ${sub.studentName}`, code);
      const blob = new Blob([fullHtml], { type: 'text/html;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      if (notify) {
        showToast(`Đã tải tệp ${filename} về máy!`);
      }
    }

    // --- TẢI TRỌN BỘ BÀI LÀM CỦA 1 HỌC SINH (NÉN THÀNH 1 FILE ZIP) ---
    function downloadStudentAllWork(idx) {
      const sub = cachedHd3Submissions[idx];
      if (!sub) return;

      const safeClass = sanitize(sub.className || '12A');
      const safeMachine = sanitize(sub.studentNumber || '00');
      const safeName = sanitize(sub.studentName || 'HocSinh');
      const zipName = `${safeClass}_${safeMachine}_${safeName}.zip`;

      const files = sub.files || {};
      const b1 = wrapInFullHtml(`Bài 1: Phương trình bậc 2 - ${sub.studentName}`, files.bai1?.code || '');
      const b2 = wrapInFullHtml(`Bài 2: Nhấn mạnh văn bản - ${sub.studentName}`, files.bai2?.code || '');
      const b3 = wrapInFullHtml(`Bài 3: Tờ rơi Internet - ${sub.studentName}`, files.bai3?.code || '');

      const studentInfo = [
        "TRƯỜNG THTH - DHSP • BÀI 8: ĐỊNH DẠNG VĂN BẢN",
        "PHIẾU THÔNG TIN BÀI LÀM HỌC SINH (HĐ 3: LUYỆN TẬP)",
        "--------------------------------------------------",
        `Họ và tên:        ${sub.studentName}`,
        `Lớp:              ${sub.className}`,
        `Số máy / STT:     ${sub.studentNumber || 'N/A'}`,
        `Thời gian nộp:    ${sub.submittedAt || ''}`,
        `Mã biên nhận:     ${sub.id || ''}`,
        "--------------------------------------------------",
        "DANH SÁCH 3 TỆP HTML ĐÍNH KÈM:",
        "1. Bai1.html - Bài toán biện luận phương trình bậc 2",
        "2. Bai2.html - Sử dụng thẻ nhấn mạnh strong, em, b, i, mark, u",
        "3. Bai3.html - Tờ rơi giới thiệu dịch vụ Internet tốc độ cao",
        "--------------------------------------------------"
      ].join("\n");

      if (typeof JSZip !== 'undefined') {
        const zip = new JSZip();
        zip.file("Bai1.html", b1);
        zip.file("Bai2.html", b2);
        zip.file("Bai3.html", b3);
        zip.file("ThongTin_BaiLam.txt", studentInfo);

        zip.generateAsync({ type: "blob" }).then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = zipName;
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
          showToast(`Đã tải 1 tệp ZIP (${zipName}) gồm 3 bài làm của học sinh!`);
        });
      } else {
        // Fallback tải lần lượt 3 file
        ['bai1', 'bai2', 'bai3'].forEach((ex, i) => {
          setTimeout(() => downloadStudentWork(idx, ex, false), i * 300);
        });
        setTimeout(() => showToast('Đã tải 3 file HTML của học sinh này!'), 1000);
      }
    }

    // --- TẢI TẤT CẢ FILE CỦA CẢ LỚP: NÉN THÀNH 1 FILE ZIP DUY NHẤT CHỨA TỪNG THƯ MỤC HỌC SINH ---
    async function downloadAllClassSubmissionsZipFolders() {
      if (!cachedHd3Submissions || cachedHd3Submissions.length === 0) {
        alert('Chưa có bài nộp nào trong danh sách để tải!');
        return;
      }
      if (!confirm(`Thầy/Cô có muốn tải về 1 TỆP ZIP DUY NHẤT chứa thư mục riêng biệt của ${cachedHd3Submissions.length} học sinh không?\n(Mỗi học sinh 1 thư mục riêng gồm Bai1.html, Bai2.html, Bai3.html và phiếu thông tin)`)) {
        return;
      }

      showToast('⏳ Đang gom nhóm và đóng gói tệp ZIP theo từng học sinh...');

      // 1. Thử gọi API backend (Server Node.js / Python đã hỗ trợ nén ZIP)
      try {
        const res = await fetch('/api/submissions-hd3-zip');
        if (res.ok) {
          const blob = await res.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `Bai8_HD3_TatCaBaiLam_THTH_DHSP_${new Date().toISOString().slice(0, 10)}.zip`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
          showToast('🎉 Đã tải xong 1 file ZIP duy nhất chứa các thư mục bài làm!');
          return;
        }
      } catch (e) {
        console.warn('API nén phía máy chủ không sẵn sàng, chuyển sang nén bằng JSZip trên trình duyệt:', e);
      }

      // 2. Chế độ Fallback / Offline: Nén trực tiếp bằng JSZip trên trình duyệt
      const createClientZip = () => {
        if (typeof JSZip === 'undefined') {
          alert('Không tìm thấy thư viện JSZip. Vui lòng kiểm tra kết nối mạng!');
          return;
        }

        const zip = new JSZip();
        let overviewLines = [
          "============================================================",
          "TRƯỜNG THTH - DHSP • BÀI 8: ĐỊNH DẠNG VĂN BẢN",
          "BẢNG TỔNG HỢP NỘP BÀI THỰC HÀNH HOẠT ĐỘNG 3 (30 PHÚT)",
          `Thời điểm xuất file: ${new Date().toLocaleString('vi-VN')}`,
          `Tổng số bài nộp: ${cachedHd3Submissions.length} học sinh`,
          "============================================================",
          "",
          "STT  | HỌ VÀ TÊN                 | LỚP    | SỐ MÁY  | THỜI GIAN NỘP      | THƯ MỤC LƯU TRỮ",
          "-----------------------------------------------------------------------------------------------"
        ];

        const seenFolders = new Set();
        cachedHd3Submissions.forEach((sub, sIdx) => {
          const name = sub.studentName || 'Học sinh';
          const cls = sub.className || '12A';
          const stt = String(sub.studentNumber || sIdx + 1).padStart(2, '0');
          const timeStr = sub.submittedAt || '';

          let baseFolder = `${sanitize(cls)}_${stt}_${sanitize(name)}`;
          let folderName = baseFolder;
          let dup = 1;
          while (seenFolders.has(folderName)) {
            dup++;
            folderName = `${baseFolder}_${dup}`;
          }
          seenFolders.add(folderName);

          overviewLines.push(`${String(sIdx + 1).padEnd(4)} | ${name.padEnd(25)} | ${cls.padEnd(6)} | ${stt.padEnd(7)} | ${timeStr.padEnd(18)} | ${folderName}/`);

          const studentFolder = zip.folder(folderName);
          const files = sub.files || {};
          const b1 = wrapInFullHtml(`Bài 1: Phương trình bậc 2 - ${name}`, files.bai1?.code || '');
          const b2 = wrapInFullHtml(`Bài 2: Nhấn mạnh văn bản - ${name}`, files.bai2?.code || '');
          const b3 = wrapInFullHtml(`Bài 3: Tờ rơi Internet - ${name}`, files.bai3?.code || '');

          studentFolder.file("Bai1.html", b1);
          studentFolder.file("Bai2.html", b2);
          studentFolder.file("Bai3.html", b3);

          const studentInfo = [
            "TRƯỜNG THTH - DHSP • BÀI 8: ĐỊNH DẠNG VĂN BẢN",
            "PHIẾU THÔNG TIN BÀI LÀM HỌC SINH (HĐ 3: LUYỆN TẬP)",
            "--------------------------------------------------",
            `Họ và tên:        ${name}`,
            `Lớp:              ${cls}`,
            `Số máy / STT:     ${stt}`,
            `Thời gian nộp:    ${timeStr}`,
            `Mã biên nhận:     ${sub.id || ''}`,
            "--------------------------------------------------",
            "DANH SÁCH 3 TỆP HTML ĐÍNH KÈM:",
            "1. Bai1.html - Bài toán biện luận phương trình bậc 2",
            "2. Bai2.html - Sử dụng thẻ nhấn mạnh strong, em, b, i, mark, u",
            "3. Bai3.html - Tờ rơi giới thiệu dịch vụ Internet tốc độ cao",
            "--------------------------------------------------"
          ].join("\n");
          studentFolder.file("ThongTin_BaiLam.txt", studentInfo);
        });

        zip.file("00_TONG_KET_LOP_HOC.txt", overviewLines.join("\n"));

        zip.generateAsync({ type: "blob", compression: "DEFLATE" }).then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `Bai8_HD3_TatCaBaiLam_THTH_DHSP_${new Date().toISOString().slice(0, 10)}.zip`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
          showToast('🎉 Đã tải xong 1 file ZIP duy nhất chứa các thư mục bài làm!');
        });
      };

      if (typeof JSZip !== 'undefined') {
        createClientZip();
      } else {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';
        script.onload = createClientZip;
        script.onerror = () => alert('Không thể nạp thư viện tạo ZIP.');
        document.head.appendChild(script);
      }
    }

    // Giữ alias downloadAllClassSubmissions trỏ vào hàm nén ZIP mới
    function downloadAllClassSubmissions() {
      downloadAllClassSubmissionsZipFolders();
    }

    // --- NỘP BÀI LÊN MÁY CHỦ (POST /api/submit-hd3) ---
    function submitHd3Practice() {
      const info = getStudentInfo();
      if (!info.studentName) {
        alert('Vui lòng nhập họ và tên học sinh trước khi nộp bài!');
        if (studentMode === 'pair') document.getElementById('pair-name-1')?.focus();
        else document.getElementById('student-name-input')?.focus();
        return;
      }
      if (!info.className) {
        alert('Vui lòng chọn lớp học của em!');
        if (studentMode === 'pair') document.getElementById('pair-class-select')?.focus();
        else document.getElementById('student-class-select')?.focus();
        return;
      }

      const codeBai1 = document.getElementById('code-bai1')?.value || '';
      const codeBai2 = document.getElementById('code-bai2')?.value || '';
      const codeBai3 = document.getElementById('code-bai3')?.value || '';

      const payload = {
        studentName: info.studentName,
        className: info.className,
        studentNumber: info.studentNumber,
        isPair: info.isPair,
        student1: info.student1,
        student2: info.student2,
        bai1Html: codeBai1,
        bai2Html: codeBai2,
        bai3Html: codeBai3,
        submittedAt: new Date().toLocaleTimeString('vi-VN') + ' - ' + new Date().toLocaleDateString('vi-VN')
      };

      // Gửi lên server
      fetch('/api/submit-hd3', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(res => res.json())
      .then(resData => {
        if (resData.success) {
          handleSubmissionSuccess(resData.data);
        } else {
          fallbackLocalSubmit(payload);
        }
      })
      .catch(() => {
        fallbackLocalSubmit(payload);
      });
    }

    function fallbackLocalSubmit(payload) {
      const id = 'HD3-' + Math.floor(1000 + Math.random() * 9000);
      const safeClass = (payload.className || '12A').replace(/[^a-zA-Z0-9]/g, '');
      const safeName = (payload.studentName || 'HocSinh').replace(/[^a-zA-Z0-9_\u00C0-\u1EF9]/g, '_');
      const prefix = `${safeClass}_${payload.studentNumber || '00'}_${safeName}`;

      const record = {
        id: id,
        activity: 'hd3',
        ...payload,
        timestamp: Date.now(),
        files: {
          bai1: { filename: `${prefix}_Bai1.html`, url: '#', code: payload.bai1Html },
          bai2: { filename: `${prefix}_Bai2.html`, url: '#', code: payload.bai2Html },
          bai3: { filename: `${prefix}_Bai3.html`, url: '#', code: payload.bai3Html }
        }
      };

      try {
        const list = JSON.parse(localStorage.getItem('bai8_hd3_submissions') || '[]');
        list.unshift(record);
        localStorage.setItem('bai8_hd3_submissions', JSON.stringify(list));
      } catch (e) {}

      handleSubmissionSuccess(record);
    }

    function wrapInFullHtml(title, code) {
      if (code && (code.includes('<!DOCTYPE') || code.includes('<html'))) return code;
      return `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}<\/title>
  <style>
    body {
      font-family: 'Times New Roman', serif;
      padding: 24px;
      line-height: 1.6;
      color: #0f172a;
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
    }
  <\/style>
<\/head>
<body>
  ${code || ''}
<\/body>
<\/html>`;
    }

    function handleSubmissionSuccess(record) {
      // Phát tín hiệu qua BroadcastChannel
      try {
        const bc = new BroadcastChannel('bai8_hd3_channel');
        bc.postMessage({ type: 'NEW_SUBMISSION', data: record });
      } catch (e) {}

      // Lấy link xem trực tiếp cho từng bài (dùng blob nếu offline)
      const getFileUrl = (ex, fallbackCode) => {
        if (record.files && record.files[ex] && record.files[ex].url && record.files[ex].url !== '#') {
          return record.files[ex].url;
        }
        const blob = new Blob([wrapInFullHtml(`Bài tập ${ex.toUpperCase()}`, fallbackCode || '')], { type: 'text/html;charset=utf-8' });
        return URL.createObjectURL(blob);
      };

      const b1Url = getFileUrl('bai1', record.bai1Html);
      const b2Url = getFileUrl('bai2', record.bai2Html);
      const b3Url = getFileUrl('bai3', record.bai3Html);

      const b1Name = record.files?.bai1?.filename || 'Bai1.html';
      const b2Name = record.files?.bai2?.filename || 'Bai2.html';
      const b3Name = record.files?.bai3?.filename || 'Bai3.html';

      // Hiện biên nhận modal
      const content = document.getElementById('receipt-content');
      content.innerHTML = `
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #64748b; font-size: 0.85rem;">Mã biên nhận:</span>
            <strong style="color: #2563eb; font-size: 1.1rem; font-family: monospace;">${record.id}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #64748b; font-size: 0.85rem;">Học sinh nộp:</span>
            <strong>${record.studentName}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #64748b; font-size: 0.85rem;">Lớp / Số máy:</span>
            <span><strong>${record.className}</strong> (Máy: ${record.studentNumber})</span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: #64748b; font-size: 0.85rem;">Thời gian nộp:</span>
            <span>${record.submittedAt}</span>
          </div>
        </div>

        <div style="font-weight: 700; color: #1e3a8a; font-size: 0.92rem; margin-bottom: 0.5rem;">
          📁 CÁC TỆP HTML ĐÃ LƯU THÀNH CÔNG VÀ SẴN SÀNG TẢI VỀ:
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.88rem;">
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 0.6rem 0.85rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">
            <span>📄 <strong>${b1Name}</strong></span>
            <div style="display: flex; gap: 0.4rem;">
              <a href="${b1Url}" target="_blank" style="background: #eff6ff; color: #2563eb; font-weight: 700; text-decoration: none; padding: 0.25rem 0.6rem; border-radius: 4px; border: 1px solid #bfdbfe;">Xem web →</a>
              <button type="button" onclick="downloadSingleHtml('bai1')" style="background: #f1f5f9; color: #1e293b; font-weight: 700; border: 1px solid #cbd5e1; padding: 0.25rem 0.6rem; border-radius: 4px; cursor: pointer;">💾 Tải về</button>
            </div>
          </div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 0.6rem 0.85rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">
            <span>📄 <strong>${b2Name}</strong></span>
            <div style="display: flex; gap: 0.4rem;">
              <a href="${b2Url}" target="_blank" style="background: #ecfdf5; color: #047857; font-weight: 700; text-decoration: none; padding: 0.25rem 0.6rem; border-radius: 4px; border: 1px solid #a7f3d0;">Xem web →</a>
              <button type="button" onclick="downloadSingleHtml('bai2')" style="background: #f1f5f9; color: #1e293b; font-weight: 700; border: 1px solid #cbd5e1; padding: 0.25rem 0.6rem; border-radius: 4px; cursor: pointer;">💾 Tải về</button>
            </div>
          </div>
          <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 0.6rem 0.85rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">
            <span>📄 <strong>${b3Name}</strong></span>
            <div style="display: flex; gap: 0.4rem;">
              <a href="${b3Url}" target="_blank" style="background: #fffbeb; color: #b45309; font-weight: 700; text-decoration: none; padding: 0.25rem 0.6rem; border-radius: 4px; border: 1px solid #fde68a;">Xem web →</a>
              <button type="button" onclick="downloadSingleHtml('bai3')" style="background: #f1f5f9; color: #1e293b; font-weight: 700; border: 1px solid #cbd5e1; padding: 0.25rem 0.6rem; border-radius: 4px; cursor: pointer;">💾 Tải về</button>
            </div>
          </div>
        </div>

        <div style="margin-top: 1rem;">
          <button type="button" class="btn btn-primary" onclick="downloadAllHtml()" style="width: 100%; padding: 0.75rem; font-size: 0.95rem; font-weight: 700; background: #2563eb; justify-content: center; box-shadow: 0 4px 6px -1px rgba(37,99,235,0.25);">
            📥 TẢI VỀ MÁY CẢ 3 FILE .HTML
          </button>
        </div>
      `;

      document.getElementById('receipt-modal').classList.add('active');

      // Tự động tải cả 3 tệp HTML về máy học sinh ngay khi nộp thành công!
      setTimeout(() => {
        downloadAllHtml();
      }, 500);
    }

    function closeReceiptModal() {
      document.getElementById('receipt-modal').classList.remove('active');
    }

    // --- QUẢN LÝ BẢNG THEO DÕI CỦA GIÁO VIÊN ---
    function loadHd3Submissions() {
      if (!isTeacherAuthenticated()) {
        const tbody = document.getElementById('hd3-submissions-tbody');
        if (tbody) {
          tbody.innerHTML = `
            <tr>
              <td colspan="9" style="text-align: center; padding: 3rem 1.5rem; color: #dc2626;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.35rem;">BẢNG THEO DÕI ĐANG BỊ KHÓA</div>
                <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 1.25rem;">Học sinh không có quyền truy cập. Vui lòng đăng nhập đúng tài khoản <strong>darber3110@gmail.com</strong> để xem kết quả.</div>
                <button type="button" class="btn btn-primary" onclick="openTeacherLoginModal()" style="font-size: 0.9rem; padding: 0.5rem 1rem;">🔑 Đăng Nhập Giáo Viên</button>
              </td>
            </tr>
          `;
        }
        return;
      }

      let localList = [];
      try {
        localList = JSON.parse(localStorage.getItem('bai8_hd3_submissions') || '[]');
      } catch (e) {}

      fetch('/api/submissions-hd3')
        .then(res => res.json())
        .then(serverData => {
          if (Array.isArray(serverData)) {
            renderHd3Table(serverData);
          } else {
            renderHd3Table(localList);
          }
        })
        .catch(() => {
          renderHd3Table(localList);
        });
    }

    function renderHd3Table(list) {
      cachedHd3Submissions = list || [];
      const tbody = document.getElementById('hd3-submissions-tbody');
      if (!tbody) return;

      const countEl = document.getElementById('stat-count-hd3');
      const filesEl = document.getElementById('stat-files-hd3');
      const latestEl = document.getElementById('stat-latest-hd3');

      if (!list || list.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align: center; padding: 2.5rem; color: #94a3b8;">
              <div style="font-size: 2rem; margin-bottom: 0.5rem;">📭</div>
              Chưa có bài nộp nào cho Hoạt động 3. Khi học sinh bấm <strong>"NỘP BÀI NGAY"</strong>, kết quả sẽ tự động xuất hiện tại đây theo thời gian thực!
            </td>
          </tr>
        `;
        if (countEl) countEl.textContent = '0';
        if (filesEl) filesEl.textContent = '0';
        if (latestEl) latestEl.textContent = 'Chưa có';
        return;
      }

      if (countEl) countEl.textContent = list.length;
      if (filesEl) filesEl.textContent = (list.length * 3);
      if (latestEl) latestEl.textContent = list[0].studentName + ' (' + (list[0].className || '') + ')';

      let html = '';
      list.forEach((sub, idx) => {
        const modeBadge = sub.isPair 
          ? '<span style="background: #eff6ff; color: #1d4ed8; font-size: 0.72rem; font-weight: 800; padding: 0.15rem 0.45rem; border-radius: 4px; margin-right: 0.35rem;">Cặp</span>'
          : '<span style="background: #f1f5f9; color: #475569; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; margin-right: 0.35rem;">Cá nhân</span>';

        html += `
          <tr>
            <td style="text-align: center; font-weight: 700; color: #64748b;">${idx + 1}</td>
            <td>
              <div style="font-weight: 700; color: #0f172a;">${modeBadge}${sub.studentName}</div>
            </td>
            <td style="text-align: center;"><span style="background: #eff6ff; color: #1e40af; font-weight: 800; font-size: 0.8rem; padding: 0.2rem 0.5rem; border-radius: 4px;">${sub.className || 'N/A'}</span></td>
            <td style="text-align: center; font-family: monospace; font-size: 0.88rem;">${sub.studentNumber || 'N/A'}</td>
            <td style="font-size: 0.82rem; color: #475569;">${sub.submittedAt || ''}</td>

            <!-- BÀI 1 -->
            <td style="text-align: center;">
              <div style="display: inline-flex; gap: 0.3rem;">
                <button type="button" class="btn btn-secondary btn-sm" onclick="viewStudentWork(${idx}, 'bai1')" style="font-size: 0.76rem; padding: 0.2rem 0.5rem; color: #1d4ed8; border-color: #bfdbfe; background: #eff6ff;" title="Xem trang web">
                  🌐 Xem
                </button>
                <button type="button" class="btn btn-secondary btn-sm" onclick="downloadStudentWork(${idx}, 'bai1')" style="font-size: 0.76rem; padding: 0.2rem 0.45rem; color: #1e40af; border-color: #bfdbfe; background: #ffffff;" title="Tải file Bai1.html về máy">
                  💾
                </button>
              </div>
            </td>

            <!-- BÀI 2 -->
            <td style="text-align: center;">
              <div style="display: inline-flex; gap: 0.3rem;">
                <button type="button" class="btn btn-secondary btn-sm" onclick="viewStudentWork(${idx}, 'bai2')" style="font-size: 0.76rem; padding: 0.2rem 0.5rem; color: #047857; border-color: #a7f3d0; background: #ecfdf5;" title="Xem trang web">
                  🌐 Xem
                </button>
                <button type="button" class="btn btn-secondary btn-sm" onclick="downloadStudentWork(${idx}, 'bai2')" style="font-size: 0.76rem; padding: 0.2rem 0.45rem; color: #047857; border-color: #a7f3d0; background: #ffffff;" title="Tải file Bai2.html về máy">
                  💾
                </button>
              </div>
            </td>

            <!-- BÀI 3 -->
            <td style="text-align: center;">
              <div style="display: inline-flex; gap: 0.3rem;">
                <button type="button" class="btn btn-secondary btn-sm" onclick="viewStudentWork(${idx}, 'bai3')" style="font-size: 0.76rem; padding: 0.2rem 0.5rem; color: #b45309; border-color: #fde68a; background: #fffbeb;" title="Xem trang web">
                  🌐 Xem
                </button>
                <button type="button" class="btn btn-secondary btn-sm" onclick="downloadStudentWork(${idx}, 'bai3')" style="font-size: 0.76rem; padding: 0.2rem 0.45rem; color: #b45309; border-color: #fde68a; background: #ffffff;" title="Tải file Bai3.html về máy">
                  💾
                </button>
              </div>
            </td>

            <td style="text-align: center;">
              <div style="display: inline-flex; gap: 0.4rem; align-items: center; justify-content: center;">
                <span style="font-family: monospace; font-size: 0.8rem; font-weight: 700; color: #64748b;">${sub.id}</span>
                <button type="button" class="btn btn-secondary btn-sm" onclick="downloadStudentAllWork(${idx})" style="font-size: 0.72rem; padding: 0.2rem 0.45rem; color: #2563eb; border-color: #bfdbfe; background: #eff6ff; font-weight: 700;" title="Tải 1 tệp ZIP chứa trọn bộ bài làm của học sinh này">
                  🗜️ Tải ZIP (3 bài)
                </button>
              </div>
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    // --- MODAL XEM SẢN PHẨM CỦA HỌC SINH (ISOLATED IFRAME) ---
    let currentModalStudent = null;
    let currentModalEx = 'bai1';

    function viewStudentWork(idx, ex) {
      const sub = cachedHd3Submissions[idx];
      if (!sub) return;

      currentModalStudent = sub;
      switchModalExercise(ex || 'bai1');
      switchModalTab('preview');
      document.getElementById('work-modal').classList.add('active');
    }

    function switchModalExercise(ex) {
      if (!currentModalStudent) return;
      currentModalEx = ex;

      // Cập nhật trạng thái tab bài tập bên trong modal
      ['bai1', 'bai2', 'bai3'].forEach(id => {
        const btn = document.getElementById(`modal-btn-ex-${id}`);
        if (btn) {
          if (id === ex) {
            btn.style.background = '#ffffff';
            btn.style.color = '#1e40af';
            btn.style.borderColor = '#3b82f6';
            btn.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
          } else {
            btn.style.background = '#f8fafc';
            btn.style.color = '#475569';
            btn.style.borderColor = '#cbd5e1';
            btn.style.boxShadow = 'none';
          }
        }
      });

      const fileObj = currentModalStudent.files ? currentModalStudent.files[ex] : null;
      const code = fileObj ? fileObj.code : (currentModalStudent[`${ex}Html`] || '');
      const exTitles = {
        bai1: 'Bài tập 1: Phương trình bậc 2 (Hình 8.3)',
        bai2: 'Bài tập 2: Nổi bật ý chính câu văn',
        bai3: 'Bài tập 3: Tờ rơi Internet tốc độ cao'
      };

      document.getElementById('modal-title').textContent = `${exTitles[ex]} • ${currentModalStudent.studentName}`;
      document.getElementById('modal-subtitle').textContent = `Lớp: ${currentModalStudent.className} | Số máy: ${currentModalStudent.studentNumber} | Mã biên nhận: ${currentModalStudent.id}`;

      const linkEl = document.getElementById('modal-direct-link');
      if (fileObj && fileObj.url && fileObj.url !== '#') {
        linkEl.href = fileObj.url;
      } else {
        const blob = new Blob([wrapInFullHtml(exTitles[ex], code)], { type: 'text/html;charset=utf-8' });
        linkEl.href = URL.createObjectURL(blob);
      }

      // Render vào iframe cách ly an toàn
      const modalIframe = document.getElementById('modal-iframe-preview');
      modalIframe.srcdoc = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: 'Times New Roman', serif;
      padding: 20px;
      margin: 0;
      line-height: 1.6;
      color: #0f172a;
      background: #ffffff;
    }
  <\/style>
<\/head>
<body>
  ${code || '<p style="color:#94a3b8; font-style:italic;">(Học sinh chưa có nội dung cho bài này)</p>'}
<\/body>
<\/html>`;

      document.getElementById('modal-code-text').textContent = code || '(Chưa có mã nguồn)';
    }

    function switchModalTab(tab) {
      const tabPrev = document.getElementById('modal-tab-preview');
      const tabCode = document.getElementById('modal-tab-code');
      const iframePrev = document.getElementById('modal-iframe-preview');
      const bodyCode = document.getElementById('modal-body-code');

      if (tab === 'code') {
        tabPrev.classList.remove('active');
        tabCode.classList.add('active');
        iframePrev.style.display = 'none';
        bodyCode.style.display = 'block';
      } else {
        tabCode.classList.remove('active');
        tabPrev.classList.add('active');
        bodyCode.style.display = 'none';
        iframePrev.style.display = 'block';
      }
    }

    function copyModalCode() {
      const code = document.getElementById('modal-code-text').textContent;
      navigator.clipboard.writeText(code).then(() => {
        showToast('✓ Đã sao chép mã nguồn HTML!');
      }).catch(() => {
        prompt('Sao chép mã nguồn:', code);
      });
    }

    function closeWorkModal() {
      document.getElementById('work-modal').classList.remove('active');
    }

    // --- SAO CHÉP CHO GOOGLE SHEETS & CSV ---
    function copyHd3ForGoogleSheets() {
      if (!cachedHd3Submissions || cachedHd3Submissions.length === 0) {
        alert('Chưa có dữ liệu bài nộp để sao chép.');
        return;
      }

      let tsv = ['STT', 'Họ và tên', 'Hình thức', 'Lớp', 'Số máy', 'Thời gian nộp', 'File Bài 1', 'File Bài 2', 'File Bài 3', 'Mã biên nhận'].join('\t') + '\n';
      cachedHd3Submissions.forEach((s, idx) => {
        tsv += [
          idx + 1,
          s.studentName,
          s.isPair ? 'Làm theo cặp (2 bạn)' : 'Cá nhân',
          s.className,
          s.studentNumber,
          s.submittedAt,
          s.files?.bai1?.filename || '',
          s.files?.bai2?.filename || '',
          s.files?.bai3?.filename || '',
          s.id
        ].join('\t') + '\n';
      });

      navigator.clipboard.writeText(tsv).then(() => {
        alert('✅ ĐÃ SAO CHÉP BẢNG DANH SÁCH HOẠT ĐỘNG 3!\n\nThầy/Cô hãy mở Google Sheets và nhấn Ctrl + V (hoặc Cmd + V) để dán bảng dữ liệu vào trang tính.');
      }).catch(() => {
        prompt('Sao chép dữ liệu bên dưới để dán vào Google Sheets:', tsv);
      });
    }

    function exportHd3CSV() {
      if (!cachedHd3Submissions || cachedHd3Submissions.length === 0) {
        alert('Chưa có dữ liệu để xuất file.');
        return;
      }

      let csv = '\uFEFF"STT","Họ và tên","Hình thức","Lớp","Số máy","Thời gian nộp","File Bài 1","File Bài 2","File Bài 3","Mã biên nhận"\n';
      cachedHd3Submissions.forEach((s, idx) => {
        csv += `"${idx + 1}","${s.studentName}","${s.isPair ? 'Cặp' : 'Cá nhân'}","${s.className}","${s.studentNumber}","${s.submittedAt}","${s.files?.bai1?.filename || ''}","${s.files?.bai2?.filename || ''}","${s.files?.bai3?.filename || ''}","${s.id}"\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `DanhSach_NopBai_HD3_LuyenTap_Bai8_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    // --- TẠO BÀI NỘP MẪU ĐỂ GIÁO VIÊN KIỂM TRA HIỂN THỊ ---
    function generateSampleHd3Data() {
      const sampleNames = ['Trần Minh Quang', 'Nguyễn Thị Thuỳ Dung', 'Lê Hoàng Nam & Đỗ Đức Huy', 'Phạm Quỳnh Anh'];
      const randomName = sampleNames[Math.floor(Math.random() * sampleNames.length)];
      const randomClass = '12A' + Math.floor(1 + Math.random() * 4);
      const isPair = randomName.includes('&');

      const mockData = {
        id: 'HD3-' + Math.floor(1000 + Math.random() * 9000),
        activity: 'hd3',
        studentName: randomName,
        isPair: isPair,
        className: randomClass,
        studentNumber: 'Máy ' + Math.floor(1 + Math.random() * 30),
        submittedAt: new Date().toLocaleTimeString('vi-VN') + ' - ' + new Date().toLocaleDateString('vi-VN'),
        timestamp: Date.now(),
        files: {
          bai1: {
            filename: `${randomClass}_May08_${randomName.replace(/[^a-zA-Z0-9]/g, '_')}_Bai1.html`,
            url: '#',
            code: `<h2>Biện luận số nghiệm của phương trình bậc 2</h2>
<p><strong style="color: red;">Bài toán:</strong> Xác định số nghiệm của phương trình ax<sup>2</sup> + bx + c = 0 (a != 0)</p>
<p><strong style="color: red;">Cách làm:</strong></p>
<p><strong>B<sub>1</sub>:</strong> Xác định hệ số a, b và c</p>
<p><strong>B<sub>2</sub>:</strong> Tính delta = b<sup>2</sup> - 4ac</p>
<p><strong>B<sub>3</sub>:</strong> Kết luận</p>
<p style="margin-left: 20px;">
  <em>+ Nếu delta &lt; 0: Phương trình vô nghiệm</em><br>
  <em>+ Nếu delta = 0: Phương trình có nghiệm duy nhất</em><br>
  <em>+ Nếu delta &gt; 0: Phương trình có hai nghiệm phân biệt</em>
</p>`
          },
          bai2: {
            filename: `${randomClass}_May08_${randomName.replace(/[^a-zA-Z0-9]/g, '_')}_Bai2.html`,
            url: '#',
            code: `<p>Thẻ <strong>strong</strong> và thẻ <strong>em</strong> được sử dụng để <em>nhấn mạnh vào nội dung trong phần tử</em>. Thẻ <b>b</b> chỉ có tác dụng in đậm văn bản</p>`
          },
          bai3: {
            filename: `${randomClass}_May08_${randomName.replace(/[^a-zA-Z0-9]/g, '_')}_Bai3.html`,
            url: '#',
            code: `<h2 style="color: blue;">INTERNET TỐC ĐỘ CAO</h2>
<p><em>Dịch vụ Internet tốc độ cao là dịch vụ Internet cáp quang chất lượng cao, ổn định, giá cả hợp lí.</em></p>
<h3>Các tính năng nổi bật:</h3>
<ul>
  <li>Tốc độ siêu cao từ 150 MBps trở lên</li>
  <li>Lắp đặt nhanh chóng trong 24 h</li>
  <li>Phù hợp với cá nhân/Hộ gia đình</li>
  <li>Tặng Modem 2 băng tần</li>
  <li>Miễn phí lắp đặt</li>
  <li>Hỗ trợ 24/7</li>
</ul>`
          }
        }
      };

      try {
        const list = JSON.parse(localStorage.getItem('bai8_hd3_submissions') || '[]');
        list.unshift(mockData);
        localStorage.setItem('bai8_hd3_submissions', JSON.stringify(list));
      } catch (e) {}

      loadHd3Submissions();
      showToast(`✓ Đã thêm bài nộp mẫu của: ${randomName}`);
    }

    function clearHd3Submissions() {
      if (confirm('Thầy/Cô có chắc chắn muốn xóa toàn bộ danh sách nộp bài Hoạt động 3 không?')) {
        localStorage.removeItem('bai8_hd3_submissions');
        renderHd3Table([]);
        showToast('Đã xóa danh sách bài nộp Hoạt động 3');
      }
    }

    // Modal QR Zoom
    function openQrModal() {
      document.getElementById('qr-zoom-modal').classList.add('active');
    }
    function closeQrModal() {
      document.getElementById('qr-zoom-modal').classList.remove('active');
    }

    // --- TỰ ĐỘNG KHỞI CHẠY KHI TẢI TRANG ---
    document.addEventListener('DOMContentLoaded', () => {
      // Khởi tạo phím Tab cho các editor
      setupEditorKeyboard('code-bai1');
      setupEditorKeyboard('code-bai2');
      setupEditorKeyboard('code-bai3');

      // Khởi tạo Timer và Fullscreen
      initTimer();
      initFullscreen();

      // Nạp nháp và thiết lập ban đầu
      loadDrafts();

      // Cập nhật trạng thái xác thực giáo viên
      updateTeacherAuthUI();

      // Chỉ tải danh sách nộp bài nếu giáo viên đã xác thực trước đó
      if (isTeacherAuthenticated()) {
        loadHd3Submissions();
      }

      // Tự động làm mới dữ liệu định kỳ chỉ khi giáo viên đang đăng nhập
      setInterval(() => {
        if (isTeacherAuthenticated()) {
          loadHd3Submissions();
        }
      }, 4000);

      // Lắng nghe BroadcastChannel
      try {
        const bc = new BroadcastChannel('bai8_hd3_channel');
        bc.onmessage = (ev) => {
          if (ev.data && ev.data.type === 'NEW_SUBMISSION' && isTeacherAuthenticated()) {
            loadHd3Submissions();
          }
        };
      } catch (e) {}
    });
