/**
 * TIN HỌC 12 - BÀI 7: HTML VÀ CẤU TRÚC TRANG WEB
 * JavaScript Tương Tác: Cây Thông Tin DOM & Kéo Thả Cấu Trúc HTML
 * (UI UX Pro Max Standards - Clean, Resilient, Anti-bug)
 * Giáo viên: Nguyễn Lê Minh Ngọc
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initTeachingTimer();
  initFullscreen();
  initCopyButtons();
  initImageModals();
  initLivePlaygrounds();
  initDomTreeInspector();
  initDragAndDropAssembler();
  initCriteriaValidator();
  initInteractiveQuizzes();
  initFlashcards();
  initDesktopSidebarScrollspy();
});

/* ==========================================================================
   CODE REPOSITORY (Tránh lỗi Live Server tự ý chèn script vào textarea)
   ========================================================================== */
const HTML_SAMPLES = {
  chuan7dong: `<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Trang web thử nghiệm</title>
</head>
<body>
    <h1 style="color: #1d4ed8;">Trang web và HTML</h1>
    <p>Đây là dòng đầu tiên</p>
    <hr>
    <p><em>Đây là dòng cuối cùng</em></p>
</body>
</html>`,

  tieude_doanvan: `<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Thử nghiệm các cấp tiêu đề</title>
</head>
<body>
    <h1>Tiêu đề cấp lớn nhất H1</h1>
    <h2>Tiêu đề cấp hai H2</h2>
    <h3>Tiêu đề cấp ba H3</h3>
    <hr>
    <p>Đoạn văn thứ nhất có chữ <b>in đậm</b> và <i>in nghiêng</i>.</p>
    <p style="color: #059669;">Đoạn văn thứ hai có màu xanh lá cây.</p>
</body>
</html>`,

  gioithieu_mau: `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Giới thiệu - Nguyễn Văn An</title>
</head>
<body>

    <h1>NGUYỄN VĂN AN</h1>
    <h3>Lớp: 12A1</h3>
    <h3>Trường: THPT Thực hành – ĐH Sư phạm</h3>

    <p>Xin chào mọi người! Đây là trang web đầu tiên của mình được tạo bằng ngôn ngữ HTML.</p>

</body>
</html>`
};

/* ==========================================================================
   1. NAVBAR ACTIVE STATE
   ========================================================================== */
function initNavbar() {
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

/* ==========================================================================
   2. TEACHING TIMER (Đồng hồ đếm giờ giáo viên)
   ========================================================================== */
function initTeachingTimer() {
  const timerDisplay = document.getElementById('timer-display');
  const timerToggleBtn = document.getElementById('timer-toggle');
  const timerResetBtn = document.getElementById('timer-reset');
  const timerPresetSelect = document.getElementById('timer-preset');
  
  if (!timerDisplay) return;

  let totalSeconds = (parseInt(timerPresetSelect?.value, 10) || 5) * 60;
  let remainingSeconds = totalSeconds;
  let timerInterval = null;
  let isRunning = false;

  function updateDisplay() {
    const mins = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    timerDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    
    if (remainingSeconds <= 60 && remainingSeconds > 0) {
      timerDisplay.style.color = '#dc2626';
      timerDisplay.style.fontWeight = 'bold';
    } else {
      timerDisplay.style.color = '';
      timerDisplay.style.fontWeight = '';
    }
  }

  function startTimer() {
    if (isRunning) return;
    isRunning = true;
    if (timerToggleBtn) timerToggleBtn.innerHTML = '⏸ Dừng';
    
    timerInterval = setInterval(() => {
      if (remainingSeconds > 0) {
        remainingSeconds--;
        updateDisplay();
      } else {
        pauseTimer();
        showToast('⏰ Hết thời gian cho hoạt động này!');
      }
    }, 1000);
  }

  function pauseTimer() {
    isRunning = false;
    clearInterval(timerInterval);
    if (timerToggleBtn) timerToggleBtn.innerHTML = '▶ Bắt đầu';
  }

  function resetTimer() {
    pauseTimer();
    if (timerPresetSelect) {
      remainingSeconds = parseInt(timerPresetSelect.value, 10) * 60;
    } else {
      remainingSeconds = totalSeconds;
    }
    updateDisplay();
  }

  timerToggleBtn?.addEventListener('click', () => {
    if (isRunning) pauseTimer();
    else startTimer();
  });

  timerResetBtn?.addEventListener('click', resetTimer);

  timerPresetSelect?.addEventListener('change', (e) => {
    totalSeconds = parseInt(e.target.value, 10) * 60;
    resetTimer();
  });

  updateDisplay();
}

/* ==========================================================================
   3. FULLSCREEN MODE
   ========================================================================== */
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
        fsBtn.innerHTML = '📺 Chiếu';
      });
    }
  });

  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement) {
      fsBtn.innerHTML = '📺 Chiếu';
    }
  });
}

/* ==========================================================================
   4. COPY BUTTONS & TOAST
   ========================================================================== */
function initCopyButtons() {
  document.querySelectorAll('.btn-copy').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      let textToCopy = '';
      
      if (targetId) {
        const targetElem = document.getElementById(targetId);
        if (targetElem) textToCopy = targetElem.innerText || targetElem.value;
      } else {
        const codeElem = btn.closest('.code-window')?.querySelector('code');
        if (codeElem) textToCopy = codeElem.innerText;
      }

      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          const original = btn.innerHTML;
          btn.innerHTML = '✓ Đã chép!';
          showToast('📋 Đã sao chép mã nguồn vào bộ nhớ tạm');
          setTimeout(() => btn.innerHTML = original, 2000);
        });
      }
    });
  });
}

function showToast(message) {
  let toast = document.getElementById('site-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'site-toast';
    toast.className = 'toast-notice';
    document.body.appendChild(toast);
  }
  toast.innerHTML = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2600);
}

/* ==========================================================================
   5. NATIVE IMAGE MODAL ZOOM
   ========================================================================== */
function initImageModals() {
  const modal = document.getElementById('image-zoom-modal');
  const modalImg = document.getElementById('modal-zoom-img');
  const modalCaption = document.getElementById('modal-zoom-caption');
  const closeBtn = document.getElementById('modal-close-btn');
  if (!modal || !modalImg) return;

  document.querySelectorAll('.figure-img-wrap img, .zoomable-img').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      modalImg.src = img.src;
      modalImg.alt = img.alt || 'Hình ảnh bài dạy';
      if (modalCaption) {
        const cap = img.closest('figure')?.querySelector('figcaption');
        modalCaption.textContent = cap ? cap.textContent : (img.alt || '');
      }
      modal.showModal();
    });
  });

  closeBtn?.addEventListener('click', () => modal.close());

  modal.addEventListener('click', (e) => {
    const rect = modal.getBoundingClientRect();
    if (
      e.clientX < rect.left || e.clientX > rect.right ||
      e.clientY < rect.top || e.clientY > rect.bottom
    ) {
      modal.close();
    }
  });
}

/* ==========================================================================
   6. LIVE HTML PLAYGROUND (Khắc phục triệt để lỗi Live Server Injection)
   ========================================================================== */
function initLivePlaygrounds() {
  document.querySelectorAll('.playground-box').forEach(box => {
    const textarea = box.querySelector('.code-textarea');
    const iframe = box.querySelector('.preview-frame');
    const btnRun = box.querySelector('.btn-run-code');
    const btnReset = box.querySelector('.btn-reset-code');
    const sampleBtns = box.querySelectorAll('.btn-load-sample');

    if (!textarea || !iframe) return;

    // Gán mã mẫu mặc định ban đầu bằng JS (chỉ khi không có thuộc tính data-no-preload)
    const isNoPreload = textarea.getAttribute('data-no-preload') === 'true';
    const initialKey = textarea.getAttribute('data-sample-key');
    if (!isNoPreload && initialKey && !textarea.value.trim() && HTML_SAMPLES[initialKey]) {
      textarea.value = HTML_SAMPLES[initialKey];
    }

    function renderCode() {
      let raw = textarea.value;

      // Làm sạch tự động nếu có script Live Server vô tình bị dán vào
      raw = raw.replace(/<!-- Code injected by live-server -->[\s\S]*?<\/script>/gi, '')
               .replace(/<script[\s\S]*?WebSocket[\s\S]*?<\/script>/gi, '')
               .replace(/<script[\s\S]*?_cacheOverride[\s\S]*?<\/script>/gi, '');

      const doc = iframe.contentDocument || iframe.contentWindow.document;
      doc.open();
      doc.write(raw);
      doc.close();
    }

    let debounceTimer;
    textarea.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(renderCode, 300);
    });

    btnRun?.addEventListener('click', renderCode);

    btnReset?.addEventListener('click', () => {
      if (isNoPreload) {
        textarea.value = '';
      } else {
        textarea.value = (initialKey && HTML_SAMPLES[initialKey]) ? HTML_SAMPLES[initialKey] : HTML_SAMPLES.chuan7dong;
      }
      renderCode();
      textarea.dispatchEvent(new Event('input'));
      showToast('↺ Đã làm mới khung soạn thảo');
    });

    sampleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-sample-key');
        if (key && HTML_SAMPLES[key]) {
          textarea.value = HTML_SAMPLES[key];
          renderCode();
          showToast('📥 Đã nạp mã mẫu');
        }
      });
    });

    // Render ban đầu
    renderCode();
  });
}

/* ==========================================================================
   7. INTERACTIVE DOM TREE INSPECTOR (Tương tác với Cây thông tin trang web)
   ========================================================================== */
const DOM_NODE_DATA = {
  html: {
    tag: '<html>',
    name: 'Phần tử Gốc (Root Element)',
    type: 'Thẻ cấu trúc gốc',
    parent: 'Không có (Cấp cao nhất của cây DOM)',
    children: '<head> và <body>',
    desc: 'Bao bọc toàn bộ mã nguồn của trang web. Mọi phần tử khác đều là con cháu nằm bên trong <html>.'
  },
  head: {
    tag: '<head>',
    name: 'Phần Đầu Trang Web (Header/Metadata)',
    type: 'Vùng thông tin cấu hình',
    parent: '<html>',
    children: '<meta>, <title>, <style>, <script>',
    desc: 'Chứa các thông tin bổ sung, siêu dữ liệu (metadata) của trang web. Nội dung trong <head> KHÔNG hiển thị trên trang trắng của trình duyệt.'
  },
  meta: {
    tag: '<meta charset="UTF-8">',
    name: 'Khai báo Bảng mã Ký tự (Charset)',
    type: 'Thẻ đơn (Void Element)',
    parent: '<head>',
    children: 'Không có',
    desc: 'Xác định bảng mã UTF-8 chuẩn quốc tế, giúp trang web hiển thị đúng tiếng Việt có dấu mà không bị lỗi font chữ.'
  },
  title: {
    tag: '<title>',
    name: 'Tiêu đề Trang Web (Document Title)',
    type: 'Thẻ văn bản tiêu đề tab',
    parent: '<head>',
    children: 'Văn bản thuần túy (Plain text)',
    desc: 'Quy định tên hiển thị trên thanh tiêu đề/tab của trình duyệt web và xuất hiện trong kết quả tìm kiếm Google.'
  },
  body: {
    tag: '<body>',
    name: 'Thân Trang Web (Body Document)',
    type: 'Vùng nội dung hiển thị',
    parent: '<html>',
    children: '<h1>, <p>, <hr>, <div>, <img>, ...',
    desc: 'Chứa TẤT CẢ nội dung hiển thị trực quan mà người xem có thể nhìn thấy trên cửa sổ trình duyệt.'
  },
  h1: {
    tag: '<h1>',
    name: 'Tiêu đề Cấp 1 (Heading 1)',
    type: 'Thẻ khối (Block-level)',
    parent: '<body>',
    children: 'Văn bản tiêu đề',
    desc: 'Tiêu đề quan trọng nhất, lớn nhất của trang web. Mặc định chữ to, in đậm và tự động xuống dòng sau thẻ.'
  },
  p1: {
    tag: '<p>',
    name: 'Đoạn Văn Bản Thứ Nhất (Paragraph)',
    type: 'Thẻ khối (Block-level)',
    parent: '<body>',
    children: 'Văn bản đoạn văn',
    desc: 'Định nghĩa một đoạn văn bản hoàn chỉnh. Trình duyệt tự động chèn khoảng cách trước và sau đoạn văn.'
  },
  hr: {
    tag: '<hr>',
    name: 'Đường Kẻ Ngang Phân Cách (Horizontal Rule)',
    type: 'Thẻ đơn (Không cần thẻ đóng)',
    parent: '<body>',
    children: 'Không có',
    desc: 'Vẽ một đường kẻ ngang trên màn hình dùng để phân tách các phần nội dung theo chủ đề.'
  },
  p2: {
    tag: '<p>',
    name: 'Đoạn Văn Bản Thứ Hai (Chứa thẻ lồng)',
    type: 'Thẻ khối (Block-level)',
    parent: '<body>',
    children: 'Thẻ <em> (In nghiêng)',
    desc: 'Minh họa việc lồng một thẻ trang trí con (<em>) vào bên trong một thẻ văn bản cha (<p>).'
  },
  em: {
    tag: '<em>',
    name: 'Nhấn mạnh In Nghiêng (Emphasis)',
    type: 'Thẻ nội dòng (Inline)',
    parent: '<p>',
    children: 'Văn bản được nhấn mạnh',
    desc: 'Làm nổi bật nội dung văn bản bằng cách hiển thị chữ in nghiêng (italic).'
  }
};

function initDomTreeInspector() {
  const treeButtons = document.querySelectorAll('.tree-btn');
  const inspectTag = document.getElementById('inspect-tag-name');
  const inspectTitle = document.getElementById('inspect-title');
  const inspectType = document.getElementById('inspect-type');
  const inspectParent = document.getElementById('inspect-parent');
  const inspectChildren = document.getElementById('inspect-children');
  const inspectDesc = document.getElementById('inspect-desc');
  const inspectCodePreview = document.getElementById('inspect-code-preview');

  if (!treeButtons.length || !inspectTag) return;

  function selectNode(nodeKey) {
    const data = DOM_NODE_DATA[nodeKey];
    if (!data) return;

    // Highlight active button
    treeButtons.forEach(btn => {
      if (btn.getAttribute('data-node') === nodeKey) {
        btn.classList.add('selected');
      } else {
        btn.classList.remove('selected');
      }
    });

    // Update Inspector details
    inspectTag.textContent = data.tag;
    inspectTitle.textContent = data.name;
    inspectType.textContent = data.type;
    inspectParent.textContent = data.parent;
    inspectChildren.textContent = data.children;
    inspectDesc.textContent = data.desc;

    // Highlight corresponding line in code preview
    if (inspectCodePreview) {
      inspectCodePreview.querySelectorAll('.code-line').forEach(line => {
        if (line.getAttribute('data-for-node') === nodeKey) {
          line.style.background = 'rgba(29, 78, 216, 0.25)';
          line.style.fontWeight = 'bold';
        } else {
          line.style.background = '';
          line.style.fontWeight = '';
        }
      });
    }
  }

  treeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const nodeKey = btn.getAttribute('data-node');
      selectNode(nodeKey);
    });
  });

  // Select <html> by default
  selectNode('html');
}

/* ==========================================================================
   8. INTERACTIVE DRAG & DROP HTML STRUCTURE ASSEMBLER (Kéo Thả Cấu Trúc HTML)
   ========================================================================== */
function initDragAndDropAssembler() {
  const workshop = document.getElementById('dnd-assembler-workshop');
  if (!workshop) return;

  const tagItems = workshop.querySelectorAll('.dnd-tag-item');
  const dropzones = workshop.querySelectorAll('.dnd-dropzone');
  const previewFrame = document.getElementById('dnd-live-preview');
  const btnReset = document.getElementById('btn-dnd-reset');
  const btnAutoSolve = document.getElementById('btn-dnd-autosolve');
  const statusMessage = document.getElementById('dnd-status-msg');

  let draggedTagData = null;

  // Hỗ trợ Drag & Drop HTML5
  tagItems.forEach(item => {
    item.addEventListener('dragstart', (e) => {
      draggedTagData = {
        tag: item.getAttribute('data-tag'),
        label: item.getAttribute('data-label'),
        validZone: item.getAttribute('data-valid-zone'),
        codeHtml: item.getAttribute('data-html')
      };
      e.dataTransfer.setData('text/plain', item.getAttribute('data-tag'));
      item.style.opacity = '0.5';
    });

    item.addEventListener('dragend', () => {
      item.style.opacity = '1';
    });

    // Hỗ trợ Click-to-add (cho máy tính bảng, màn hình cảm ứng)
    item.addEventListener('click', () => {
      const targetZoneId = item.getAttribute('data-valid-zone');
      const targetZone = document.getElementById(`dropzone-${targetZoneId}`);
      if (targetZone) {
        addTagToZone(targetZone, {
          tag: item.getAttribute('data-tag'),
          label: item.getAttribute('data-label'),
          codeHtml: item.getAttribute('data-html')
        });
      }
    });
  });

  dropzones.forEach(zone => {
    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('drag-over');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('drag-over');
    });

    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('drag-over');

      if (!draggedTagData) return;

      const expectedZone = draggedTagData.validZone;
      const currentZoneId = zone.getAttribute('data-zone-id');

      if (expectedZone !== currentZoneId) {
        zone.classList.add('has-error');
        showToast(`⚠️ Thẻ ${draggedTagData.tag} không thuộc vùng này! Hãy xem lại vị trí cha-con.`);
        setTimeout(() => zone.classList.remove('has-error'), 1000);
        return;
      }

      addTagToZone(zone, draggedTagData);
    });
  });

  function addTagToZone(zone, tagData) {
    // Check if tag already in this zone to prevent duplicates for single tags like title or doctype
    const existing = zone.querySelector(`[data-placed-tag="${tagData.tag}"]`);
    if (existing && (tagData.tag === '<!DOCTYPE html>' || tagData.tag === '<title>' || tagData.tag === '<meta>')) {
      showToast(`ℹ️ Thẻ ${tagData.tag} đã có trong vùng này.`);
      return;
    }

    const tagCard = document.createElement('div');
    tagCard.className = 'dnd-placed-tag';
    tagCard.setAttribute('data-placed-tag', tagData.tag);
    tagCard.setAttribute('data-html-chunk', tagData.codeHtml);
    tagCard.style.cssText = `
      display: flex; align-items: center; justify-content: space-between;
      padding: 0.4rem 0.65rem; background: #ffffff; border: 1px solid #10b981;
      border-radius: 6px; font-family: var(--font-mono); font-size: 0.82rem;
      margin-bottom: 0.25rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    `;
    tagCard.innerHTML = `
      <span style="color: #059669; font-weight: 600;">✓ ${tagData.tag}</span>
      <button type="button" class="btn-remove-tag" style="background:none; border:none; color:#ef4444; cursor:pointer; font-size:0.9rem;" title="Xóa thẻ này">✕</button>
    `;

    tagCard.querySelector('.btn-remove-tag').addEventListener('click', () => {
      tagCard.remove();
      compileAndPreview();
    });

    zone.appendChild(tagCard);
    compileAndPreview();
    showToast(`✓ Đã ghép thẻ ${tagData.tag}`);
  }

  function compileAndPreview() {
    const rootTags = workshop.querySelectorAll('#dropzone-root .dnd-placed-tag');
    const headTags = workshop.querySelectorAll('#dropzone-head .dnd-placed-tag');
    const bodyTags = workshop.querySelectorAll('#dropzone-body .dnd-placed-tag');

    let hasDocType = Array.from(rootTags).some(el => el.getAttribute('data-placed-tag') === '<!DOCTYPE html>');
    let headHtml = Array.from(headTags).map(el => el.getAttribute('data-html-chunk')).join('\n    ');
    let bodyHtml = Array.from(bodyTags).map(el => el.getAttribute('data-html-chunk')).join('\n    ');

    let fullHtml = `${hasDocType ? '<!DOCTYPE html>\n' : ''}<html lang="vi">\n<head>\n    ${headHtml}\n</head>\n<body>\n    ${bodyHtml}\n</body>\n</html>`;

    if (previewFrame) {
      const doc = previewFrame.contentDocument || previewFrame.contentWindow.document;
      doc.open();
      doc.write(fullHtml);
      doc.close();
    }

    // Update status
    const totalPlaced = rootTags.length + headTags.length + bodyTags.length;
    if (statusMessage) {
      if (totalPlaced >= 6 && hasDocType) {
        statusMessage.textContent = '🎉 Tuyệt vời! Cấu trúc trang web đã hoàn chỉnh và hợp lệ!';
        statusMessage.style.color = '#059669';
      } else {
        statusMessage.textContent = `Đã ghép ${totalPlaced} thẻ. Kéo thêm thẻ vào <head> và <body>.`;
        statusMessage.style.color = '#64748b';
      }
    }
  }

  btnReset?.addEventListener('click', () => {
    dropzones.forEach(z => {
      z.querySelectorAll('.dnd-placed-tag').forEach(t => t.remove());
    });
    compileAndPreview();
    showToast('↺ Đã làm mới khung kéo thả');
  });

  btnAutoSolve?.addEventListener('click', () => {
    btnReset.click();
    // Auto populate correctly
    const rootZone = document.getElementById('dropzone-root');
    const headZone = document.getElementById('dropzone-head');
    const bodyZone = document.getElementById('dropzone-body');

    if (rootZone && headZone && bodyZone) {
      addTagToZone(rootZone, { tag: '<!DOCTYPE html>', codeHtml: '' });
      addTagToZone(headZone, { tag: '<meta>', codeHtml: '<meta charset="UTF-8">' });
      addTagToZone(headZone, { tag: '<title>', codeHtml: '<title>Trang web mẫu</title>' });
      addTagToZone(bodyZone, { tag: '<h1>', codeHtml: '<h1>Trang web và HTML</h1>' });
      addTagToZone(bodyZone, { tag: '<p>', codeHtml: '<p>Đây là dòng đầu tiên</p>' });
      addTagToZone(bodyZone, { tag: '<hr>', codeHtml: '<hr>' });
      addTagToZone(bodyZone, { tag: '<em>', codeHtml: '<p><em>Đây là dòng cuối cùng</em></p>' });
      showToast('⚡ Đã tự động lắp ráp cấu trúc chuẩn!');
    }
  });

  // Ban đầu
  compileAndPreview();
}

/* ==========================================================================
   9. CRITERIA VALIDATOR FOR ACTIVITY 3 (Thực hành gioithieu.html)
   ========================================================================== */
function initCriteriaValidator() {
  const studentCodeArea = document.getElementById('student-code-input');
  const btnValidate = document.getElementById('btn-validate-code');
  if (!studentCodeArea) return;

  // Học sinh tự tay lập trình, không đưa code mẫu sẵn
  studentCodeArea.value = '';

  const criteria = {
    doctype: { id: 'chk-doctype', test: (c) => /<!DOCTYPE\s+html>/i.test(c) },
    htmlTag: { id: 'chk-html', test: (c) => /<html[\s>]/i.test(c) && /<\/html>/i.test(c) },
    headBody: { id: 'chk-head-body', test: (c) => /<head[\s>]/i.test(c) && /<\/head>/i.test(c) && /<body[\s>]/i.test(c) && /<\/body>/i.test(c) },
    metaUtf8: { id: 'chk-meta', test: (c) => /<meta\s+charset\s*=\s*["']?utf-8["']?/i.test(c) },
    titleTag: { id: 'chk-title', test: (c) => /<title>[\s\S]+<\/title>/i.test(c) },
    h1Tag: { id: 'chk-h1', test: (c) => /<h1>[\s\S]+<\/h1>/i.test(c) },
    headingSub: { id: 'chk-subheading', test: (c) => /<h[23]>[\s\S]+<\/h[23]>/i.test(c) },
    paragraph: { id: 'chk-p', test: (c) => /<p>[\s\S]+<\/p>/i.test(c) }
  };

  function validate() {
    const code = studentCodeArea.value;
    let passedCount = 0;
    const totalCount = Object.keys(criteria).length;

    for (const key in criteria) {
      const item = criteria[key];
      const chkElem = document.getElementById(item.id);
      if (chkElem) {
        const isPassed = item.test(code);
        chkElem.checked = isPassed;
        const itemWrap = chkElem.closest('.checklist-item');
        if (itemWrap) {
          if (isPassed) {
            itemWrap.style.borderColor = '#10b981';
            itemWrap.style.background = '#ecfdf5';
          } else {
            itemWrap.style.borderColor = '';
            itemWrap.style.background = '';
          }
        }
        if (isPassed) passedCount++;
      }
    }

    const scoreDisplay = document.getElementById('criteria-score-display');
    if (scoreDisplay) {
      scoreDisplay.textContent = `${passedCount}/${totalCount} tiêu chí đạt`;
      scoreDisplay.style.background = passedCount === totalCount ? '#ecfdf5' : '#eff6ff';
      scoreDisplay.style.color = passedCount === totalCount ? '#059669' : '#1d4ed8';
    }
  }

  studentCodeArea.addEventListener('input', validate);
  btnValidate?.addEventListener('click', () => {
    validate();
    showToast('🔍 Đã phân tích tiêu chí bài làm!');
  });

  validate();
}

/* ==========================================================================
   10. INTERACTIVE QUIZZES
   ========================================================================== */
function initInteractiveQuizzes() {
  document.querySelectorAll('.quiz-card').forEach(card => {
    const buttons = card.querySelectorAll('.quiz-btn');
    const feedback = card.querySelector('.quiz-feedback');

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const isCorrect = btn.getAttribute('data-correct') === 'true';
        
        buttons.forEach(b => {
          b.disabled = true;
          if (b.getAttribute('data-correct') === 'true') {
            b.classList.add('correct');
          }
        });

        if (isCorrect) {
          btn.classList.add('correct');
          if (feedback) {
            feedback.innerHTML = `<strong>Chính xác! 🎉</strong> ` + (btn.getAttribute('data-explain') || 'Bạn đã chọn đúng đáp án.');
            feedback.className = 'quiz-feedback show correct-fb';
          }
        } else {
          btn.classList.add('incorrect');
          if (feedback) {
            feedback.innerHTML = `<strong>Chưa chính xác! 💡</strong> ` + (btn.getAttribute('data-explain') || 'Hãy xem lại lý thuyết nhé.');
            feedback.className = 'quiz-feedback show incorrect-fb';
          }
        }

        // Cập nhật điểm ôn tập nếu có bảng tổng kết
        updateReviewScore();
      });
    });
  });
}

function updateReviewScore() {
  const totalQuestions = document.querySelectorAll('.quiz-card').length;
  const answeredCorrect = document.querySelectorAll('.quiz-btn.correct:disabled').length;
  const scoreBadge = document.getElementById('review-score-badge');
  if (scoreBadge && totalQuestions > 0) {
    scoreBadge.textContent = `${answeredCorrect}/${totalQuestions} câu đúng`;
  }
}

/* ==========================================================================
   11. INTERACTIVE FLASHCARDS (Lật thẻ ôn tập)
   ========================================================================== */
function initFlashcards() {
  const flashcards = document.querySelectorAll('.flashcard');
  flashcards.forEach(card => {
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'button');
    card.setAttribute('aria-label', 'Nhấp để lật thẻ');

    const toggleFlip = () => {
      card.classList.toggle('flipped');
    };

    card.addEventListener('click', toggleFlip);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleFlip();
      }
    });
  });
}

/* ==========================================================================
   12. DESKTOP SIDEBAR SCROLLSPY
   ========================================================================== */
function initDesktopSidebarScrollspy() {
  const sidebarLinks = document.querySelectorAll('.sidebar-item-link');
  if (!sidebarLinks.length) return;

  const sections = [];
  sidebarLinks.forEach(link => {
    const targetId = link.getAttribute('href');
    if (targetId && targetId.startsWith('#')) {
      const section = document.querySelector(targetId);
      if (section) {
        sections.push({ id: targetId, link: link, element: section });
      }
    }
  });

  if (!sections.length) return;

  function onScroll() {
    const scrollPos = window.scrollY + 140;
    let currentSection = sections[0];

    for (let i = 0; i < sections.length; i++) {
      if (sections[i].element.offsetTop <= scrollPos) {
        currentSection = sections[i];
      }
    }

    sections.forEach(s => s.link.classList.remove('active'));
    if (currentSection) {
      currentSection.link.classList.add('active');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

