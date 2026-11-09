#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator for Bai9_TrinhChieu.pptx
Tích hợp toàn bộ 16 hình ảnh thiết kế từ KHBD.docx
Giáo viên: Nguyễn Lê Minh Ngọc
Trường THPT Thực hành - Đại học Sư phạm TP.HCM
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ----------------- HẰNG SỐ MÀU SẮC & GIAO DIỆN -----------------
COLOR_PRIMARY = RGBColor(30, 58, 138)       # #1E3A8A Navy Blue
COLOR_ROYAL = RGBColor(37, 99, 235)         # #2563EB Royal Blue
COLOR_SKY = RGBColor(2, 132, 199)           # #0284C7 Sky Blue
COLOR_EMERALD = RGBColor(5, 150, 105)       # #059669 Emerald Green
COLOR_DARK_GREEN = RGBColor(6, 95, 70)      # #065F46 Dark Green
COLOR_AMBER = RGBColor(217, 119, 6)         # #D97706 Amber
COLOR_RED = RGBColor(220, 38, 38)           # #DC2626 Red
COLOR_PURPLE = RGBColor(124, 58, 237)       # #7C3AED Purple

COLOR_BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC Canvas background
COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF Card background
COLOR_CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0 Subtle border
COLOR_DIVIDER = RGBColor(203, 213, 225)     # #CBD5E1 Divider line

COLOR_TEXT_TITLE = RGBColor(15, 23, 42)     # #0F172A Dark title
COLOR_TEXT_BODY = RGBColor(51, 65, 85)      # #334155 Body text
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B Secondary text

# Code editor theme
COLOR_CODE_BG = RGBColor(15, 23, 42)        # #0F172A
COLOR_CODE_BAR = RGBColor(30, 41, 59)       # #1E293B
COLOR_CODE_TEXT = RGBColor(241, 245, 249)   # #F1F5F9
COLOR_CODE_VAL = RGBColor(74, 222, 128)     # #4ADE80 Green
COLOR_CODE_COMMENT = RGBColor(148, 163, 184)# #94A3B8

FONT_HEADING = 'Arial'
FONT_BODY = 'Arial'
FONT_CODE = 'Consolas'

BASE_DIR = '/Users/minhngoc/Desktop/THTH-DHSP/Tin12/Bai9'
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
WORD_IMG_DIR = os.path.join(ASSETS_DIR, 'word_images')
OUTPUT_PPTX = os.path.join(BASE_DIR, 'Bai9_TrinhChieu.pptx')

# ----------------- HÀM TRỢ GIÚP DỰNG SLIDE -----------------

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, color=COLOR_BG_LIGHT):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, badge_text, title_text, subtitle_text=None, badge_theme='blue'):
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.07))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_PRIMARY
    top_bar.line.fill.background()

    badge_bg = RGBColor(239, 246, 255)
    badge_border = RGBColor(191, 219, 254)
    badge_txt_color = COLOR_ROYAL

    if badge_theme == 'green':
        badge_bg = RGBColor(236, 253, 245)
        badge_border = RGBColor(167, 243, 208)
        badge_txt_color = COLOR_EMERALD
    elif badge_theme == 'amber':
        badge_bg = RGBColor(254, 243, 199)
        badge_border = RGBColor(253, 230, 138)
        badge_txt_color = COLOR_AMBER
    elif badge_theme == 'purple':
        badge_bg = RGBColor(245, 243, 255)
        badge_border = RGBColor(221, 214, 254)
        badge_txt_color = COLOR_PURPLE

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(0.24), Inches(2.9), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = badge_bg
    badge.line.color.rgb = badge_border
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = badge_text.upper()
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = badge_txt_color
    p_b.alignment = PP_ALIGN.CENTER

    title_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.68), Inches(12.0), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_TITLE

    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.65), Inches(1.22), Inches(12.0), Inches(0.35))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(14)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(1.60), Inches(12.03), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_DIVIDER
    div.line.fill.background()

def add_footer(slide, slide_num=None):
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(7.0), Inches(12.03), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_CARD_BORDER
    div.line.fill.background()

    box_l = slide.shapes.add_textbox(Inches(0.65), Inches(7.05), Inches(8.5), Inches(0.35))
    tf_l = box_l.text_frame
    p_l = tf_l.paragraphs[0]
    p_l.text = "Tin học 12 Thống nhất • Bài 9: Tạo danh sách, bảng • GV: Nguyễn Lê Minh Ngọc"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(11)
    p_l.font.color.rgb = COLOR_TEXT_MUTED

    box_r = slide.shapes.add_textbox(Inches(8.5), Inches(7.05), Inches(4.18), Inches(0.35))
    tf_r = box_r.text_frame
    p_r = tf_r.paragraphs[0]
    p_r.text = "Trường THPT Thực hành ĐH Sư phạm"
    if slide_num:
        p_r.text += f" • {slide_num}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(11)
    p_r.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_code_editor(slide, left, top, width, height, filename, code_text, font_size=15):
    card = add_card(slide, left, top, width, height, bg_color=COLOR_CODE_BG, border_color=COLOR_PRIMARY, border_width=1.5)
    
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.44))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_CODE_BAR
    bar.line.fill.background()

    c_red = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.15), top + Inches(0.14), Inches(0.15), Inches(0.15))
    c_red.fill.solid(); c_red.fill.fore_color.rgb = RGBColor(239, 68, 68); c_red.line.fill.background()
    c_yellow = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.36), top + Inches(0.14), Inches(0.15), Inches(0.15))
    c_yellow.fill.solid(); c_yellow.fill.fore_color.rgb = RGBColor(245, 158, 11); c_yellow.line.fill.background()
    c_green = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.57), top + Inches(0.14), Inches(0.15), Inches(0.15))
    c_green.fill.solid(); c_green.fill.fore_color.rgb = RGBColor(16, 185, 129); c_green.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.85), top + Inches(0.06), width - Inches(0.95), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = f"📄 {filename}"
    p.font.name = FONT_CODE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(203, 213, 225)

    code_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.50), width - Inches(0.4), height - Inches(0.58))
    tf_c = code_box.text_frame
    tf_c.word_wrap = True
    lines = code_text.strip().split('\n')
    for i, line in enumerate(lines):
        p_c = tf_c.paragraphs[0] if i == 0 else tf_c.add_paragraph()
        p_c.text = line
        p_c.font.name = FONT_CODE
        p_c.font.size = Pt(font_size)
        if line.strip().startswith('<!--') or line.strip().startswith('//'):
            p_c.font.color.rgb = COLOR_CODE_COMMENT
            p_c.font.italic = True
        elif '<' in line or '>' in line:
            p_c.font.color.rgb = COLOR_CODE_TEXT
        else:
            p_c.font.color.rgb = COLOR_CODE_VAL
    return card

def add_browser_preview(slide, left, top, width, height, title, content_lines, font_size=15):
    card = add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.44))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(238, 242, 255)
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.06), width - Inches(0.4), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = f"🌐 Trình duyệt hiển thị: {title}"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    body_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.52), width - Inches(0.5), height - Inches(0.58))
    tf_b = body_box.text_frame
    tf_b.word_wrap = True
    for i, line in enumerate(content_lines):
        p_b = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p_b.text = line
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(font_size)
        p_b.font.color.rgb = COLOR_TEXT_BODY
        if line.startswith('•') or line.startswith('1.') or line.startswith('2.'):
            p_b.font.bold = False
        elif line.endswith(':') or 'Hóa đơn' in line or 'BẢNG' in line or 'Danh sách' in line:
            p_b.font.bold = True
            p_b.font.color.rgb = COLOR_PRIMARY
    return card

def add_callout(slide, left, top, width, height, title, text, theme='tip'):
    bg = RGBColor(239, 246, 255)
    border = COLOR_ROYAL
    icon = "💡 LƯU Ý SƯ PHẠM:"
    title_color = COLOR_PRIMARY

    if theme == 'warning':
        bg = RGBColor(254, 242, 242)
        border = COLOR_RED
        icon = "⚠️ LỖI CẦN TRÁNH:"
        title_color = COLOR_RED
    elif theme == 'green':
        bg = RGBColor(236, 253, 245)
        border = COLOR_EMERALD
        icon = "✅ CHUẨN W3C:"
        title_color = COLOR_DARK_GREEN

    card = add_card(slide, left, top, width, height, bg_color=bg, border_color=border, border_width=1.5)
    accent = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.1), height)
    accent.fill.solid()
    accent.fill.fore_color.rgb = border
    accent.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), width - Inches(0.35), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = f"{icon} {title}"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = title_color

    p2 = tf.add_paragraph()
    p2.text = text
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_TEXT_BODY
    return card

# ----------------- XÂY DỰNG 28 SLIDES VỚI HÌNH WORD -----------------

def build_all_slides():
    prs = create_presentation()
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: BÌA BÀI HỌC (Chỉ để tên GV: Nguyễn Lê Minh Ngọc)
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_background(s1, RGBColor(241, 245, 249))

    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY; top_bar.line.fill.background()

    # Hero card lớn bên trái
    add_card(s1, Inches(0.8), Inches(0.7), Inches(7.4), Inches(6.1), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=2)
    
    b_tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(1.1), Inches(6.7), Inches(0.46))
    b_tag.fill.solid(); b_tag.fill.fore_color.rgb = RGBColor(238, 242, 255)
    b_tag.line.color.rgb = RGBColor(199, 210, 254); b_tag.line.width = Pt(1)
    tf = b_tag.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.text = "TRƯỜNG THPT THỰC HÀNH - ĐẠI HỌC SƯ PHẠM TP.HCM • TIN HỌC 12"
    p.font.name = FONT_HEADING; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    t_box = s1.shapes.add_textbox(Inches(1.15), Inches(1.85), Inches(6.7), Inches(2.2))
    tf_t = t_box.text_frame; tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]; p1.text = "CHỦ ĐỀ 4: TẠO TRANG WEB"
    p1.font.name = FONT_HEADING; p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = COLOR_ROYAL
    
    p2 = tf_t.add_paragraph(); p2.text = "BÀI 9: TẠO DANH SÁCH, BẢNG"
    p2.font.name = FONT_HEADING; p2.font.size = Pt(32); p2.font.bold = True; p2.font.color.rgb = COLOR_PRIMARY
    
    p3 = tf_t.add_paragraph(); p3.text = "Khám phá các thẻ Danh sách HTML5 & Thiết lập Bảng dữ liệu"
    p3.font.name = FONT_BODY; p3.font.size = Pt(15); p3.font.color.rgb = COLOR_TEXT_MUTED

    div_s1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.15), Inches(4.3), Inches(6.7), Inches(0.02))
    div_s1.fill.solid(); div_s1.fill.fore_color.rgb = COLOR_DIVIDER; div_s1.line.fill.background()

    # THÔNG TIN GIÁO VIÊN: CHỈ ĐỂ TÊN NGUYỄN LÊ MINH NGỌC
    gv_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(4.7), Inches(6.7), Inches(1.5))
    gv_card.fill.solid(); gv_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    gv_card.line.color.rgb = COLOR_ROYAL; gv_card.line.width = Pt(1.5)
    tf_gv = gv_card.text_frame; tf_gv.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_gv1 = tf_gv.paragraphs[0]
    p_gv1.text = "👨‍🏫 GIÁO VIÊN HƯỚNG DẪN:"
    p_gv1.font.name = FONT_HEADING; p_gv1.font.size = Pt(13); p_gv1.font.bold = True; p_gv1.font.color.rgb = COLOR_PRIMARY
    p_gv1.alignment = PP_ALIGN.CENTER

    p_gv2 = tf_gv.add_paragraph()
    p_gv2.text = "Nguyễn Lê Minh Ngọc"
    p_gv2.font.name = FONT_HEADING; p_gv2.font.size = Pt(22); p_gv2.font.bold = True; p_gv2.font.color.rgb = COLOR_ROYAL
    p_gv2.alignment = PP_ALIGN.CENTER

    # Bên phải: Code editor & Preview
    add_code_editor(s1, Inches(8.5), Inches(0.7), Inches(4.1), Inches(3.3), "demo_bai9.html",
"""<!DOCTYPE html>
<html>
<body>
  <h3>Danh sách món ăn</h3>
  <ul>
    <li>Thịt xiên nướng</li>
    <li>Trà đào cam sả</li>
  </ul>
</body>
</html>""", font_size=15)

    add_browser_preview(s1, Inches(8.5), Inches(4.25), Inches(4.1), Inches(2.55), "demo_bai9.html", [
        "Danh sách món ăn:",
        "• Thịt xiên nướng",
        "• Trà đào cam sả",
        "",
        "➔ Bố cục chuẩn W3C, thoáng đẹp!"
    ], font_size=15)

    # =========================================================================
    # SLIDE 2: MỤC TIÊU BÀI HỌC
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_slide_background(s2)
    add_header(s2, "MỤC TIÊU BÀI HỌC", "3 CHUẨN KIẾN THỨC & NĂNG LỰC CỐT LÕI", "Yêu cầu cần đạt theo Chương trình GDPT 2018")
    add_footer(s2, 2)

    card_w = Inches(3.8)
    card_h = Inches(5.0)
    top_pos = Inches(1.8)

    # Cột 1: Năng lực Tin học
    add_card(s2, Inches(0.65), top_pos, card_w, card_h, border_color=COLOR_ROYAL, border_width=2)
    h1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), top_pos + Inches(0.2), Inches(3.4), Inches(0.55))
    h1.fill.solid(); h1.fill.fore_color.rgb = RGBColor(238, 242, 255); h1.line.fill.background()
    p = h1.text_frame.paragraphs[0]; p.text = "💻 NĂNG LỰC TIN HỌC"
    p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    tb1 = s2.shapes.add_textbox(Inches(0.85), top_pos + Inches(0.95), Inches(3.4), Inches(3.8))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    pts1 = [
        "1. Hiểu ý nghĩa danh sách và bảng trong trình bày web.",
        "2. Sử dụng thành thạo các thẻ: <ol>, <ul>, <dl>, <table>.",
        "3. Lựa chọn dạng cấu trúc tối ưu cho từng loại dữ liệu."
    ]
    for pt in pts1:
        p_pt = tf1.add_paragraph()
        p_pt.text = f"\n{pt}"
        p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(16); p_pt.font.color.rgb = COLOR_TEXT_BODY

    # Cột 2: Năng lực chung
    add_card(s2, Inches(4.75), top_pos, card_w, card_h, border_color=COLOR_EMERALD, border_width=2)
    h2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.95), top_pos + Inches(0.2), Inches(3.4), Inches(0.55))
    h2.fill.solid(); h2.fill.fore_color.rgb = RGBColor(236, 253, 245); h2.line.fill.background()
    p = h2.text_frame.paragraphs[0]; p.text = "🤝 NĂNG LỰC CHUNG"
    p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD
    p.alignment = PP_ALIGN.CENTER

    tb2 = s2.shapes.add_textbox(Inches(4.95), top_pos + Inches(0.95), Inches(3.4), Inches(3.8))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    pts2 = [
        "1. Tự chủ & Tự học: Khám phá cú pháp thẻ mới.",
        "2. Giao tiếp & Hợp tác: Lập trình cặp đôi trang web CLB.html.",
        "3. Giải quyết vấn đề: Xử lý kỹ thuật gộp ô phức tạp."
    ]
    for pt in pts2:
        p_pt = tf2.add_paragraph()
        p_pt.text = f"\n{pt}"
        p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(16); p_pt.font.color.rgb = COLOR_TEXT_BODY

    # Cột 3: Phẩm chất
    add_card(s2, Inches(8.85), top_pos, card_w, card_h, border_color=COLOR_AMBER, border_width=2)
    h3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.05), top_pos + Inches(0.2), Inches(3.4), Inches(0.55))
    h3.fill.solid(); h3.fill.fore_color.rgb = RGBColor(254, 243, 199); h3.line.fill.background()
    p = h3.text_frame.paragraphs[0]; p.text = "⭐ PHẨM CHẤT CHỦ YẾU"
    p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_AMBER
    p.alignment = PP_ALIGN.CENTER

    tb3 = s2.shapes.add_textbox(Inches(9.05), top_pos + Inches(0.95), Inches(3.4), Inches(3.8))
    tf3 = tb3.text_frame; tf3.word_wrap = True
    pts3 = [
        "1. Chăm chỉ: Gõ mã chính xác từng thẻ đóng.",
        "2. Trách nhiệm: Hoàn thành bài nộp đúng thời hạn.",
        "3. Thẩm mỹ: Thiết kế trang web sáng sủa, đẹp mắt."
    ]
    for pt in pts3:
        p_pt = tf3.add_paragraph()
        p_pt.text = f"\n{pt}"
        p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(16); p_pt.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 3: TIẾN TRÌNH 2 TIẾT HỌC
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_slide_background(s3)
    add_header(s3, "TIẾN TRÌNH BÀI DẠY", "LỘ TRÌNH 2 TIẾT HỌC (90 PHÚT)", "Tiến trình sư phạm từ Khám phá đến Lập trình thực hành")
    add_footer(s3, 3)

    steps = [
        ("HĐ 1: KHỞI ĐỘNG (10')", "So sánh 2 cách tạo thực đơn món ăn trên web", COLOR_PRIMARY),
        ("HĐ 2.1: KHÁM PHÁ 1 (20')", "Danh sách có thứ tự <ol>, không thứ tự <ul>, danh sách mô tả <dl>", COLOR_ROYAL),
        ("HĐ 2.2: KHÁM PHÁ 2 (20')", "Thiết lập bảng <table>, thuộc tính viền border và gộp ô", COLOR_SKY),
        ("ĐÁNH GIÁ CHẶNG (5')", "Kiểm tra nhanh 5 câu trắc nghiệm để mở khóa Thực hành", COLOR_AMBER),
        ("HĐ 3: THỰC HÀNH (30')", "Lập trình cặp đôi dự án CLB.html: Danh sách & Bảng lịch CLB", COLOR_EMERALD),
        ("HĐ 4 & 5: VẬN DỤNG (5')", "Tổng kết Infographic Cheat Sheet & Nhiệm vụ về nhà", COLOR_PURPLE)
    ]

    y_start = Inches(1.8)
    box_h = Inches(0.75)
    gap = Inches(0.12)
    for i, (title, desc, color) in enumerate(steps):
        cur_y = y_start + i * (box_h + gap)
        card = add_card(s3, Inches(0.65), cur_y, Inches(12.03), box_h, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        nb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cur_y + Inches(0.12), Inches(2.8), Inches(0.5))
        nb.fill.solid(); nb.fill.fore_color.rgb = color; nb.line.fill.background()
        p = nb.text_frame.paragraphs[0]; p.text = title
        p.font.name = FONT_HEADING; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = s3.shapes.add_textbox(Inches(3.75), cur_y + Inches(0.12), Inches(8.8), Inches(0.5))
        tf = tb.text_frame; tf.word_wrap = True
        p_desc = tf.paragraphs[0]; p_desc.text = desc
        p_desc.font.name = FONT_BODY; p_desc.font.size = Pt(15); p_desc.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 4: HĐ 1 - TÌNH HUỐNG DẪN NHẬP
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_slide_background(s4)
    add_header(s4, "HĐ 1: KHỞI ĐỘNG (10')", "TÌNH HUỐNG DẪN NHẬP: HỘI CHỢ ẨM THỰC 12E", "Mục tiêu: Đặt vấn đề và khơi gợi nhu cầu tổ chức dữ liệu dạng danh sách & bảng", badge_theme='blue')
    add_footer(s4, 4)

    add_card(s4, Inches(0.65), Inches(1.8), Inches(5.8), Inches(4.9), border_color=COLOR_ROYAL, border_width=1.5)
    tb_s4 = s4.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_s4 = tb_s4.text_frame; tf_s4.word_wrap = True

    p = tf_s4.paragraphs[0]; p.text = "🎪 ĐẶT VẤN ĐỀ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    p1 = tf_s4.add_paragraph()
    p1.text = "\n• Lớp 12E tham gia Hội chợ ẩm thực trường."
    p1.font.name = FONT_BODY; p1.font.size = Pt(16); p1.font.color.rgb = COLOR_TEXT_BODY

    p2 = tf_s4.add_paragraph()
    p2.text = "• Cần đăng thực đơn kèm giá tiền lên trang web của lớp."
    p2.font.name = FONT_BODY; p2.font.size = Pt(16); p2.font.color.rgb = COLOR_TEXT_BODY

    p3 = tf_s4.add_paragraph()
    p3.text = "\n❓ CÂU HỎI THẢO LUẬN:\nLàm sao để trình bày danh sách rõ ràng, đẹp mắt và tiện quản lý nhất?"
    p3.font.name = FONT_HEADING; p3.font.size = Pt(17); p3.font.bold = True; p3.font.color.rgb = COLOR_AMBER

    p_illus_vi_sao = os.path.join(ASSETS_DIR, 'illus_vi_sao_can_ds_bang.png')
    if os.path.exists(p_illus_vi_sao):
        add_card(s4, Inches(6.65), Inches(1.8), Inches(6.03), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        s4.shapes.add_picture(p_illus_vi_sao, Inches(6.8), Inches(1.95), Inches(5.73), Inches(4.6))

    # =========================================================================
    # SLIDE 5: HĐ 1 - ĐỐI SÁNH TRỰC QUAN 2 CÁCH TẠO DANH SÁCH (Dán Image1 & Image2 từ Word)
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_slide_background(s5)
    add_header(s5, "HĐ 1: KHỞI ĐỘNG (10')", "ĐỐI SÁNH TRỰC QUAN: 2 CÁCH TẠO DANH SÁCH", "Hình ảnh thực tế trích xuất từ Kế hoạch bài dạy KHBD.docx", badge_theme='blue')
    add_footer(s5, 5)

    # Khung 1: Cách 1 (Dán image1.png từ file Word)
    add_card(s5, Inches(0.65), Inches(1.8), Inches(12.03), Inches(2.35), bg_color=COLOR_WHITE, border_color=COLOR_RED, border_width=1.5)
    tb_h1 = s5.shapes.add_textbox(Inches(0.85), Inches(1.9), Inches(11.63), Inches(0.4))
    p = tb_h1.text_frame.paragraphs[0]; p.text = "❌ CÁCH 1: TẠO DANH SÁCH THỦ CÔNG (GÕ TAY TRONG THẺ <P>)"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_RED
    
    img1_p = os.path.join(WORD_IMG_DIR, 'image1.png')
    if os.path.exists(img1_p):
        s5.shapes.add_picture(img1_p, Inches(0.85), Inches(2.35), Inches(11.63), Inches(1.65))

    # Khung 2: Cách 2 (Dán image2.png từ file Word)
    add_card(s5, Inches(0.65), Inches(4.35), Inches(12.03), Inches(2.45), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    tb_h2 = s5.shapes.add_textbox(Inches(0.85), Inches(4.45), Inches(11.63), Inches(0.4))
    p = tb_h2.text_frame.paragraphs[0]; p.text = "✅ CÁCH 2: TẠO DANH SÁCH CHUẨN BẰNG HTML (<OL>, <UL> VÀ <LI>)"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN

    img2_p = os.path.join(WORD_IMG_DIR, 'image2.png')
    if os.path.exists(img2_p):
        s5.shapes.add_picture(img2_p, Inches(0.85), Inches(4.90), Inches(11.63), Inches(1.65))

    # =========================================================================
    # SLIDE 6: HĐ 1 - 3 LỢI ÍCH VƯỢT TRỘI
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_slide_background(s6)
    add_header(s6, "HĐ 1: KHỞI ĐỘNG (10')", "3 LỢI ÍCH VƯỢT TRỘI CỦA DANH SÁCH & BẢNG TRONG HTML", "Chốt kiến thức dẫn nhập trước khi bước vào phần Khám phá", badge_theme='blue')
    add_footer(s6, 6)

    b_w = Inches(3.8)
    b_h = Inches(4.9)
    y_pos = Inches(1.8)

    benefits = [
        ("⏱️ TIẾT KIỆM THỜI GIAN", "Tự động hóa quản lý", [
            "Tự động đánh số thứ tự 1, 2, 3...",
            "Thêm hoặc xóa mục không cần sửa tay.",
            "Tránh 100% lỗi nhầm số thứ tự."
        ], COLOR_ROYAL),
        ("🎯 CHUẨN W3C SEMANTIC", "Tối ưu hóa trình duyệt", [
            "Trình duyệt hiểu đúng cấu trúc dữ liệu.",
            "Tối ưu SEO cho công cụ tìm kiếm.",
            "Dễ dàng định dạng kiểu dáng CSS."
        ], COLOR_EMERALD),
        ("👁️ THẨM MỸ THỊ GIÁC", "Trải nghiệm người đọc", [
            "Người dùng nắm bắt ý chính trong 3s.",
            "Thụt lề và khoảng cách dòng chuẩn.",
            "Giao diện khoa học và chuyên nghiệp."
        ], COLOR_AMBER)
    ]

    for i, (head, subhead, points, color) in enumerate(benefits):
        cx = Inches(0.65) + i * Inches(4.11)
        add_card(s6, cx, y_pos, b_w, b_h, border_color=color, border_width=2)
        hb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), y_pos + Inches(0.2), Inches(3.4), Inches(0.65))
        hb.fill.solid(); hb.fill.fore_color.rgb = color; hb.line.fill.background()
        tf = hb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.text = head
        p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph(); p2.text = subhead
        p2.font.name = FONT_BODY; p2.font.size = Pt(11); p2.font.color.rgb = RGBColor(241, 245, 249)
        p2.alignment = PP_ALIGN.CENTER

        tb = s6.shapes.add_textbox(cx + Inches(0.25), y_pos + Inches(1.1), Inches(3.3), Inches(3.5))
        tf_b = tb.text_frame; tf_b.word_wrap = True
        for j, pt in enumerate(points):
            p_pt = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p_pt.text = f"\n• {pt}"
            p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(15.5); p_pt.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 7: HĐ 2.1 - HEADER CHUYỂN TIẾP KHÁM PHÁ DANH SÁCH
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    set_slide_background(s7, RGBColor(238, 242, 255))
    top_bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY; top_bar.line.fill.background()
    add_footer(s7, 7)

    add_card(s7, Inches(1.5), Inches(1.2), Inches(10.33), Inches(5.2), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=2)
    
    tag = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.66), Inches(1.6), Inches(4.0), Inches(0.48))
    tag.fill.solid(); tag.fill.fore_color.rgb = RGBColor(238, 242, 255); tag.line.color.rgb = COLOR_ROYAL
    p = tag.text_frame.paragraphs[0]; p.text = "NỘI DUNG TRỌNG TÂM TIẾT 1"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    tb_hd = s7.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.33), Inches(1.5))
    tf_hd = tb_hd.text_frame; tf_hd.word_wrap = True
    p = tf_hd.paragraphs[0]; p.text = "HOẠT ĐỘNG 2.1: KHÁM PHÁ DANH SÁCH HTML"
    p.font.name = FONT_HEADING; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    p2 = tf_hd.add_paragraph(); p2.text = "Khám phá 3 loại danh sách: Có thứ tự (<ol>), Không thứ tự (<ul>) và Danh sách mô tả (<dl>)"
    p2.font.name = FONT_BODY; p2.font.size = Pt(15.5); p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    types = [
        ("<ol>", "DANH SÁCH CÓ THỨ TỰ", "Đánh số 1, 2, 3... hoặc A, B, C...", COLOR_ROYAL),
        ("<ul>", "DANH SÁCH KHÔNG THỨ TỰ", "Dấu chấm tròn, vuông, tròn rỗng...", COLOR_EMERALD),
        ("<dl>", "DANH SÁCH MÔ TẢ", "Thuật ngữ kèm giải thích (Kem, Trà sữa)", COLOR_AMBER)
    ]
    for i, (tag_name, name, desc, color) in enumerate(types):
        cx = Inches(2.0) + i * Inches(3.2)
        box = add_card(s7, cx, Inches(3.9), Inches(2.9), Inches(2.1), border_color=color, border_width=1.5)
        tp = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.6), Inches(4.1), Inches(1.7), Inches(0.42))
        tp.fill.solid(); tp.fill.fore_color.rgb = color; tp.line.fill.background()
        p = tp.text_frame.paragraphs[0]; p.text = tag_name
        p.font.name = FONT_CODE; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb_sub = s7.shapes.add_textbox(cx + Inches(0.15), Inches(4.65), Inches(2.6), Inches(1.3))
        tf_s = tb_sub.text_frame; tf_s.word_wrap = True
        p_s1 = tf_s.paragraphs[0]; p_s1.text = name
        p_s1.font.name = FONT_HEADING; p_s1.font.size = Pt(12); p_s1.font.bold = True; p_s1.font.color.rgb = COLOR_TEXT_TITLE
        p_s1.alignment = PP_ALIGN.CENTER
        p_s2 = tf_s.add_paragraph(); p_s2.text = desc
        p_s2.font.name = FONT_BODY; p_s2.font.size = Pt(11.5); p_s2.font.color.rgb = COLOR_TEXT_MUTED
        p_s2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 8: HĐ 2.1 - DANH SÁCH CÓ THỨ TỰ <OL> (Dán Image3, Image4, Image6 từ Word)
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    set_slide_background(s8)
    add_header(s8, "HĐ 2.1: DANH SÁCH HTML", "1. DANH SÁCH CÓ THỨ TỰ: CẶP THẺ <OL> VÀ <LI>", "Hình ảnh cấu trúc cú pháp, code mẫu và kết quả biên dịch từ KHBD.docx", badge_theme='blue')
    add_footer(s8, 8)

    # Trái: Cấu trúc chung (image3.png)
    add_card(s8, Inches(0.65), Inches(1.8), Inches(4.6), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im3 = s8.shapes.add_textbox(Inches(0.85), Inches(1.9), Inches(4.2), Inches(0.4))
    p = tb_h_im3.text_frame.paragraphs[0]; p.text = "📌 CẤU TRÚC PHÂN CẤP CHUNG:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    img3_p = os.path.join(WORD_IMG_DIR, 'image3.png')
    if os.path.exists(img3_p):
        s8.shapes.add_picture(img3_p, Inches(0.85), Inches(2.4), Inches(4.2), Inches(2.1))

    tb_nt_im3 = s8.shapes.add_textbox(Inches(0.85), Inches(4.7), Inches(4.2), Inches(1.8))
    tf_nt = tb_nt_im3.text_frame; tf_nt.word_wrap = True
    p = tf_nt.paragraphs[0]; p.text = "• <ol>: Thẻ cha bao bọc danh sách có thứ tự."
    p.font.name = FONT_BODY; p.font.size = Pt(14); p.font.color.rgb = COLOR_TEXT_BODY
    p2 = tf_nt.add_paragraph(); p2.text = "• <li>: Thẻ con chứa từng mục cụ thể."
    p2.font.name = FONT_BODY; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_BODY

    # Phải trên: Code mẫu (image4.png)
    add_card(s8, Inches(5.5), Inches(1.8), Inches(7.18), Inches(2.35), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im4 = s8.shapes.add_textbox(Inches(5.7), Inches(1.9), Inches(6.8), Inches(0.35))
    p = tb_h_im4.text_frame.paragraphs[0]; p.text = "💻 CODE MẪU DANH SÁCH CÓ THỨ TỰ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img4_p = os.path.join(WORD_IMG_DIR, 'image4.png')
    if os.path.exists(img4_p):
        s8.shapes.add_picture(img4_p, Inches(5.7), Inches(2.3), Inches(6.8), Inches(1.75))

    # Phải dưới: Kết quả biên dịch (image6.png)
    add_card(s8, Inches(5.5), Inches(4.35), Inches(7.18), Inches(2.35), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    tb_h_im6 = s8.shapes.add_textbox(Inches(5.7), Inches(4.45), Inches(6.8), Inches(0.35))
    p = tb_h_im6.text_frame.paragraphs[0]; p.text = "🌐 BIÊN DỊCH TRÊN TRÌNH DUYỆT:"
    p.font.name = FONT_HEADING; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    img6_p = os.path.join(WORD_IMG_DIR, 'image6.png')
    if os.path.exists(img6_p):
        s8.shapes.add_picture(img6_p, Inches(5.7), Inches(4.85), Inches(6.8), Inches(1.75))

    # =========================================================================
    # SLIDE 9: HĐ 2.1 - THUỘC TÍNH TYPE & START CỦA <OL> (Dán Image8 từ Word)
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    set_slide_background(s9)
    add_header(s9, "HĐ 2.1: DANH SÁCH HTML", "THUỘC TÍNH CỐT LÕI CỦA THẺ <OL>: TYPE & START", "Bảng tra cứu thuộc tính thông dụng từ Kế hoạch bài dạy KHBD.docx", badge_theme='blue')
    add_footer(s9, 9)

    # Dán image8.png lớn ở nửa trên
    add_card(s9, Inches(0.65), Inches(1.8), Inches(12.03), Inches(3.2), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im8 = s9.shapes.add_textbox(Inches(0.85), Inches(1.9), Inches(11.63), Inches(0.35))
    p = tb_h_im8.text_frame.paragraphs[0]; p.text = "📋 BẢNG THUỘC TÍNH THÔNG DỤNG CỦA THẺ <OL>:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img8_p = os.path.join(WORD_IMG_DIR, 'image8.png')
    if os.path.exists(img8_p):
        s9.shapes.add_picture(img8_p, Inches(1.5), Inches(2.3), Inches(10.3), Inches(2.55))

    # Nửa dưới: 2 thẻ tóm tắt to rõ ràng
    add_card(s9, Inches(0.65), Inches(5.15), Inches(5.85), Inches(1.6), bg_color=RGBColor(238, 242, 255), border_color=COLOR_ROYAL, border_width=1.5)
    tb_t1 = s9.shapes.add_textbox(Inches(0.85), Inches(5.25), Inches(5.45), Inches(1.4))
    tf_t1 = tb_t1.text_frame; tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]; p.text = "1. THUỘC TÍNH TYPE (KIỂU ĐÁNH SỐ):"
    p.font.name = FONT_HEADING; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p2 = tf_t1.add_paragraph(); p2.text = "type=\"1\" (Số) • type=\"A\" / \"a\" (Chữ cái) • type=\"I\" / \"i\" (La Mã)"
    p2.font.name = FONT_BODY; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_BODY

    add_card(s9, Inches(6.83), Inches(5.15), Inches(5.85), Inches(1.6), bg_color=RGBColor(236, 253, 245), border_color=COLOR_EMERALD, border_width=1.5)
    tb_t2 = s9.shapes.add_textbox(Inches(7.03), Inches(5.25), Inches(5.45), Inches(1.4))
    tf_t2 = tb_t2.text_frame; tf_t2.word_wrap = True
    p = tf_t2.paragraphs[0]; p.text = "2. THUỘC TÍNH START (SỐ BẮT ĐẦU):"
    p.font.name = FONT_HEADING; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    p2 = tf_t2.add_paragraph(); p2.text = "start=\"số_nguyên\" ➔ Bắt đầu từ số bất kỳ (ví dụ start=\"10\": 10, 11, 12...)"
    p2.font.name = FONT_BODY; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 10: HĐ 2.1 - DANH SÁCH KHÔNG THỨ TỰ <UL> (Dán Image9, Image5, Image7 từ Word)
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    set_slide_background(s10)
    add_header(s10, "HĐ 2.1: DANH SÁCH HTML", "2. DANH SÁCH KHÔNG THỨ TỰ: THẺ <UL>", "Hình ảnh kiểu dấu đầu dòng, code mẫu và kết quả biên dịch từ KHBD.docx", badge_theme='blue')
    add_footer(s10, 10)

    # Top: Kiểu dấu đầu dòng (image9.png)
    add_card(s10, Inches(0.65), Inches(1.8), Inches(12.03), Inches(2.2), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im9 = s10.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.35))
    p = tb_h_im9.text_frame.paragraphs[0]; p.text = "🎨 4 KIỂU DẤU ĐẦU DÒNG (CSS LIST-STYLE-TYPE):"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img9_p = os.path.join(WORD_IMG_DIR, 'image9.png')
    if os.path.exists(img9_p):
        s10.shapes.add_picture(img9_p, Inches(0.85), Inches(2.25), Inches(11.63), Inches(1.65))

    # Bottom Trái: Code mẫu (image5.png)
    add_card(s10, Inches(0.65), Inches(4.2), Inches(5.85), Inches(2.6), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im5 = s10.shapes.add_textbox(Inches(0.85), Inches(4.3), Inches(5.45), Inches(0.35))
    p = tb_h_im5.text_frame.paragraphs[0]; p.text = "💻 CODE MẪU DANH SÁCH KHÔNG THỨ TỰ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img5_p = os.path.join(WORD_IMG_DIR, 'image5.png')
    if os.path.exists(img5_p):
        s10.shapes.add_picture(img5_p, Inches(0.85), Inches(4.7), Inches(5.45), Inches(1.95))

    # Bottom Phải: Kết quả biên dịch (image7.png)
    add_card(s10, Inches(6.83), Inches(4.2), Inches(5.85), Inches(2.6), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    tb_h_im7 = s10.shapes.add_textbox(Inches(7.03), Inches(4.3), Inches(5.45), Inches(0.35))
    p = tb_h_im7.text_frame.paragraphs[0]; p.text = "🌐 BIÊN DỊCH TRÊN TRÌNH DUYỆT:"
    p.font.name = FONT_HEADING; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    img7_p = os.path.join(WORD_IMG_DIR, 'image7.png')
    if os.path.exists(img7_p):
        s10.shapes.add_picture(img7_p, Inches(7.03), Inches(4.7), Inches(5.45), Inches(1.95))

    # =========================================================================
    # SLIDE 11: HĐ 2.1 - DANH SÁCH MÔ TẢ (Dán Image11 & Image10 từ Word)
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    set_slide_background(s11)
    add_header(s11, "HĐ 2.1: DANH SÁCH HTML", "3. DANH SÁCH MÔ TẢ: BỘ BA THẺ <DL>, <DT>, <DD>", "Hình ảnh đoạn mã HTML và kết quả hiển thị tự động thụt lề từ KHBD.docx", badge_theme='amber')
    add_footer(s11, 11)

    # Trái: Đoạn mã HTML (image11.png)
    add_card(s11, Inches(0.65), Inches(1.8), Inches(6.0), Inches(3.6), bg_color=COLOR_WHITE, border_color=COLOR_AMBER, border_width=1.5)
    tb_h_im11 = s11.shapes.add_textbox(Inches(0.85), Inches(1.9), Inches(5.6), Inches(0.35))
    p = tb_h_im11.text_frame.paragraphs[0]; p.text = "💻 ĐOẠN MÃ HTML DANH SÁCH MÔ TẢ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_AMBER
    img11_p = os.path.join(WORD_IMG_DIR, 'image11.png')
    if os.path.exists(img11_p):
        s11.shapes.add_picture(img11_p, Inches(0.85), Inches(2.35), Inches(5.6), Inches(2.9))

    # Phải: Kết quả hiển thị (image10.png)
    add_card(s11, Inches(6.85), Inches(1.8), Inches(5.83), Inches(3.6), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    tb_h_im10 = s11.shapes.add_textbox(Inches(7.05), Inches(1.9), Inches(5.43), Inches(0.35))
    p = tb_h_im10.text_frame.paragraphs[0]; p.text = "🌐 KẾT QUẢ HIỂN THỊ TỰ ĐỘNG THỤT LỀ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    img10_p = os.path.join(WORD_IMG_DIR, 'image10.png')
    if os.path.exists(img10_p):
        s11.shapes.add_picture(img10_p, Inches(7.05), Inches(2.35), Inches(5.43), Inches(2.9))

    # Dưới: Thẻ tóm tắt bộ 3 thẻ
    add_card(s11, Inches(0.65), Inches(5.55), Inches(12.03), Inches(1.25), bg_color=RGBColor(254, 243, 199), border_color=COLOR_AMBER, border_width=1.5)
    tb_b_dl = s11.shapes.add_textbox(Inches(0.85), Inches(5.6), Inches(11.63), Inches(1.1))
    tf_bdl = tb_b_dl.text_frame; tf_bdl.word_wrap = True
    p = tf_bdl.paragraphs[0]
    p.text = "📚 BỘ 3 THẺ: <dl> (thẻ cha bao bọc) • <dt> (tên mục / thuật ngữ) • <dd> (mô tả chi tiết, tự động thụt lề vào trong)"
    p.font.name = FONT_HEADING; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_TEXT_TITLE

    # =========================================================================
    # SLIDE 12: HĐ 2.1 - DANH SÁCH LỒNG NHAU (Dán Image12 từ Word)
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    set_slide_background(s12)
    add_header(s12, "HĐ 2.1: DANH SÁCH HTML", "KỸ THUẬT DANH SÁCH LỒNG NHAU (NESTED LISTS)", "Cách viết chuẩn theo SGK đối chiếu lỗi sai kinh điển từ KHBD.docx", badge_theme='green')
    add_footer(s12, 12)

    # Dán image12.png to rõ ở giữa
    add_card(s12, Inches(0.65), Inches(1.8), Inches(12.03), Inches(3.4), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    tb_h_im12 = s12.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.35))
    p = tb_h_im12.text_frame.paragraphs[0]; p.text = "⚖️ ĐỐI CHIẾU: CÁCH VIẾT CHUẨN SGK >< LỖI SAI KINH ĐIỂN CẦN TRÁNH:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    img12_p = os.path.join(WORD_IMG_DIR, 'image12.png')
    if os.path.exists(img12_p):
        s12.shapes.add_picture(img12_p, Inches(0.85), Inches(2.25), Inches(11.63), Inches(2.8))

    # Dưới: Callout quy tắc vàng
    add_callout(s12, Inches(0.65), Inches(5.35), Inches(12.03), Inches(1.45), "QUY TẮC VÀNG W3C",
                "Danh sách con (<ol> hoặc <ul>) BẮT BUỘC phải nằm trọn vẹn bên trong cặp thẻ <li>...</li> của mục cha. Không được đóng </li> trước khi danh sách con kết thúc!", theme='green')

    # =========================================================================
    # SLIDE 13: HĐ 2.1 - PHIẾU HỌC TẬP SỐ 1 (QR + UI)
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    set_slide_background(s13)
    add_header(s13, "HĐ 2.1: ĐÁNH GIÁ NHANH", "PHIẾU HỌC TẬP SỐ 1: KIỂM TRA NHANH KHÁM PHÁ 1", "Quét mã QR để làm bài trắc nghiệm nhanh 5 phút", badge_theme='amber')
    add_footer(s13, 13)

    add_card(s13, Inches(0.65), Inches(1.8), Inches(4.8), Inches(4.9), border_color=COLOR_ROYAL, border_width=2)
    qr1_path = os.path.join(ASSETS_DIR, 'qr_phieu1.png')
    if os.path.exists(qr1_path):
        s13.shapes.add_picture(qr1_path, Inches(1.4), Inches(2.05), Inches(3.3), Inches(3.3))
    
    link_b = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.5), Inches(4.4), Inches(0.55))
    link_b.fill.solid(); link_b.fill.fore_color.rgb = RGBColor(238, 242, 255)
    link_b.line.color.rgb = COLOR_ROYAL
    p = link_b.text_frame.paragraphs[0]
    p.text = "🔗 minda.io.vn/Tin12/Bai9/phieu-bai-tap-1.html"
    p.font.name = FONT_CODE; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_ROYAL
    p.alignment = PP_ALIGN.CENTER

    p_p1_ui = os.path.join(ASSETS_DIR, 'illus_phieu1_ui.png')
    if os.path.exists(p_p1_ui):
        add_card(s13, Inches(5.65), Inches(1.8), Inches(7.03), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        s13.shapes.add_picture(p_p1_ui, Inches(5.8), Inches(2.2), Inches(6.73), Inches(2.5))
        tb_p1 = s13.shapes.add_textbox(Inches(5.8), Inches(4.9), Inches(6.73), Inches(1.6))
        tf_p1 = tb_p1.text_frame; tf_p1.word_wrap = True
        p = tf_p1.paragraphs[0]; p.text = "🎯 TRỌNG TÂM 3 CÂU HỎI:"
        p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_AMBER
        p2 = tf_p1.add_paragraph(); p2.text = "• Cú pháp đánh số từ 10 (<ol start=\"10\">)"
        p2.font.name = FONT_BODY; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_BODY
        p3 = tf_p1.add_paragraph(); p3.text = "• Thẻ mô tả chi tiết tự thụt lề (<dd>)"
        p3.font.name = FONT_BODY; p3.font.size = Pt(14); p3.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 14: HĐ 2.2 - HEADER CHUYỂN TIẾP THIẾT LẬP BẢNG
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    set_slide_background(s14, RGBColor(238, 242, 255))
    top_bar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY; top_bar.line.fill.background()
    add_footer(s14, 14)

    add_card(s14, Inches(1.5), Inches(1.2), Inches(10.33), Inches(5.2), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=2)
    
    tag2 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.66), Inches(1.6), Inches(4.0), Inches(0.48))
    tag2.fill.solid(); tag2.fill.fore_color.rgb = RGBColor(238, 242, 255); tag2.line.color.rgb = COLOR_ROYAL
    p = tag2.text_frame.paragraphs[0]; p.text = "NỘI DUNG TRỌNG TÂM TIẾT 2"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    tb_h2 = s14.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.33), Inches(1.5))
    tf_h2 = tb_h2.text_frame; tf_h2.word_wrap = True
    p = tf_h2.paragraphs[0]; p.text = "HOẠT ĐỘNG 2.2: THIẾT LẬP BẢNG TRONG HTML"
    p.font.name = FONT_HEADING; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    p2 = tf_h2.add_paragraph(); p2.text = "Hoạt động 2 SGK trang 53: Xử lý bài toán tổ chức dữ liệu dạng hàng và cột"
    p2.font.name = FONT_BODY; p2.font.size = Pt(15.5); p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    tbl_features = [
        ("<table>", "BỘ THẺ CỐT LÕI", "<table>, <tr>, <th> và <td> xây dựng khung lưới hàng - cột", COLOR_ROYAL),
        ("style=\"...\"", "THUỘC TÍNH ĐỊNH DẠNG", "Viền border (solid, dotted), kích thước width/height", COLOR_EMERALD),
        ("colspan/rowspan", "KỸ THUẬT GỘP Ô", "Mở rộng ô theo chiều ngang hoặc dọc cho bảng phức tạp", COLOR_PURPLE)
    ]
    for i, (tag_name, name, desc, color) in enumerate(tbl_features):
        cx = Inches(2.0) + i * Inches(3.2)
        box = add_card(s14, cx, Inches(3.9), Inches(2.9), Inches(2.1), border_color=color, border_width=1.5)
        tp = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.4), Inches(4.1), Inches(2.1), Inches(0.42))
        tp.fill.solid(); tp.fill.fore_color.rgb = color; tp.line.fill.background()
        p = tp.text_frame.paragraphs[0]; p.text = tag_name
        p.font.name = FONT_CODE; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb_sub = s14.shapes.add_textbox(cx + Inches(0.15), Inches(4.65), Inches(2.6), Inches(1.3))
        tf_s = tb_sub.text_frame; tf_s.word_wrap = True
        p_s1 = tf_s.paragraphs[0]; p_s1.text = name
        p_s1.font.name = FONT_HEADING; p_s1.font.size = Pt(12); p_s1.font.bold = True; p_s1.font.color.rgb = COLOR_TEXT_TITLE
        p_s1.alignment = PP_ALIGN.CENTER
        p_s2 = tf_s.add_paragraph(); p_s2.text = desc
        p_s2.font.name = FONT_BODY; p_s2.font.size = Pt(11.5); p_s2.font.color.rgb = COLOR_TEXT_MUTED
        p_s2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 15: HĐ 2.2 - CẤU TRÚC CƠ BẢN CỦA BẢNG (Dán Image13 từ Word)
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    set_slide_background(s15)
    add_header(s15, "HĐ 2.2: THIẾT LẬP BẢNG", "CẤU TRÚC PHÂN CẤP CỦA BẢNG (HÌNH 9.4 SGK)", "Đồ họa chi tiết mã HTML và kết quả mặc định trích xuất từ KHBD.docx", badge_theme='blue')
    add_footer(s15, 15)

    # Dán image13.png lớn sắc nét
    add_card(s15, Inches(0.65), Inches(1.8), Inches(12.03), Inches(4.0), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im13 = s15.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.35))
    p = tb_h_im13.text_frame.paragraphs[0]; p.text = "📊 HÌNH 9.4: CẤU TRÚC HTML CỦA BẢNG & KẾT QUẢ HIỂN THỊ:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img13_p = os.path.join(WORD_IMG_DIR, 'image13.png')
    if os.path.exists(img13_p):
        s15.shapes.add_picture(img13_p, Inches(0.85), Inches(2.25), Inches(11.63), Inches(3.45))

    # Dưới: 4 Thẻ cốt lõi ngắn gọn
    add_card(s15, Inches(0.65), Inches(5.9), Inches(12.03), Inches(0.95), bg_color=RGBColor(238, 242, 255), border_color=COLOR_ROYAL, border_width=1.5)
    tb_b_sub = s15.shapes.add_textbox(Inches(0.85), Inches(5.95), Inches(11.63), Inches(0.8))
    p = tb_b_sub.text_frame.paragraphs[0]
    p.text = "🧱 4 THẺ CỐT LÕI: <table> (bảng) • <tr> (hàng) • <th> (tiêu đề in đậm, căn giữa) • <td> (ô dữ liệu)"
    p.font.name = FONT_HEADING; p.font.size = Pt(14.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 16: HĐ 2.2 - THẺ TIÊU ĐỀ BẢNG <CAPTION>
    # =========================================================================
    s16 = prs.slides.add_slide(blank)
    set_slide_background(s16)
    add_header(s16, "HĐ 2.2: THIẾT LẬP BẢNG", "THẺ TIÊU ĐỀ BẢNG: THẺ <CAPTION>", "Gán nhãn tiêu đề giải thích nội dung cho bảng", badge_theme='blue')
    add_footer(s16, 16)

    add_card(s16, Inches(0.65), Inches(1.8), Inches(6.0), Inches(4.9), border_color=COLOR_ROYAL, border_width=1.5)
    tb_c = s16.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(5.6), Inches(4.5))
    tf_c = tb_c.text_frame; tf_c.word_wrap = True
    p = tf_c.paragraphs[0]; p.text = "🏷️ VỊ TRÍ BẮT BUỘC:"
    p.font.name = FONT_HEADING; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    p_red = tf_c.add_paragraph()
    p_red.text = "\nĐẶT NGAY SAU THẺ <TABLE> VÀ TRƯỚC THẺ <TR> ĐẦU TIÊN!"
    p_red.font.name = FONT_HEADING; p_red.font.size = Pt(16); p_red.font.bold = True; p_red.font.color.rgb = COLOR_RED

    pts_c = [
        "Mỗi bảng chỉ có duy nhất MỘT thẻ <caption>.",
        "Tiêu đề tự động căn giữa phía trên toàn bộ bảng.",
        "Giúp người xem hiểu ngay mục đích bảng dữ liệu."
    ]
    for pt in pts_c:
        p_pt = tf_c.add_paragraph(); p_pt.text = f"\n• {pt}"
        p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(15); p_pt.font.color.rgb = COLOR_TEXT_BODY

    add_code_editor(s16, Inches(6.9), Inches(1.8), Inches(5.78), Inches(2.6), "caption.html",
"""<table>
  <!-- Vị trí bắt buộc -->
  <caption>Hóa đơn hội chợ 12E</caption>
  <tr>
    <th>Món ăn</th>
    <th>Đơn giá</th>
  </tr>
</table>""", font_size=16)

    add_browser_preview(s16, Inches(6.9), Inches(4.6), Inches(5.78), Inches(2.1), "caption.html", [
        "       Hóa đơn hội chợ 12E",
        "┌──────────────────┬──────────────┐",
        "│ Món ăn           │ Đơn giá      │",
        "└──────────────────┴──────────────┘",
        "➔ Tiêu đề tự động căn giữa đẹp mắt!"
    ], font_size=15)

    # =========================================================================
    # SLIDE 17: HĐ 2.2 - CÁC ĐỊNH DẠNG CƠ BẢN CỦA BẢNG (Dán Image14 từ Word)
    # =========================================================================
    s17 = prs.slides.add_slide(blank)
    set_slide_background(s17)
    add_header(s17, "HĐ 2.2: THIẾT LẬP BẢNG", "CÁC ĐỊNH DẠNG CƠ BẢN CỦA BẢNG (HÌNH 9.5 SGK)", "Tiêu đề caption, khung viền border và kích thước width/height từ KHBD.docx", badge_theme='blue')
    add_footer(s17, 17)

    # Dán image14.png to rõ ở giữa
    add_card(s17, Inches(0.65), Inches(1.8), Inches(12.03), Inches(3.5), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=1.5)
    tb_h_im14 = s17.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.35))
    p = tb_h_im14.text_frame.paragraphs[0]; p.text = "🎨 CÁC ĐỊNH DẠNG CƠ BẢN CỦA BẢNG (THEO SGK TRANG 54):"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    img14_p = os.path.join(WORD_IMG_DIR, 'image14.png')
    if os.path.exists(img14_p):
        s17.shapes.add_picture(img14_p, Inches(0.85), Inches(2.25), Inches(11.63), Inches(2.95))

    # Nửa dưới: 3 tóm tắt cốt lõi
    add_card(s17, Inches(0.65), Inches(5.45), Inches(12.03), Inches(1.35), bg_color=RGBColor(238, 242, 255), border_color=COLOR_ROYAL, border_width=1.5)
    tb_b_im14 = s17.shapes.add_textbox(Inches(0.85), Inches(5.5), Inches(11.63), Inches(1.2))
    tf_b14 = tb_b_im14.text_frame; tf_b14.word_wrap = True
    p = tf_b14.paragraphs[0]
    p.text = "1. Tiêu đề: Thẻ <caption> ngay sau <table> • 2. Viền border: độ_dày kiểu_viền màu_viền (solid, dotted, double)"
    p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p2 = tf_b14.add_paragraph()
    p2.text = "3. Kích thước: width và height theo tỉ lệ % hoặc điểm ảnh px (Khuyên dùng % để hiển thị co giãn linh hoạt)."
    p2.font.name = FONT_BODY; p2.font.size = Pt(13.5); p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 18: HĐ 2.2 - KÍCH THƯỚC BẢNG WIDTH VÀ HEIGHT
    # =========================================================================
    s18 = prs.slides.add_slide(blank)
    set_slide_background(s18)
    add_header(s18, "HĐ 2.2: THIẾT LẬP BẢNG", "ĐIỀU CHỈNH KÍCH THƯỚC: WIDTH & HEIGHT (HÌNH 9.5 SGK)", "Kiểm soát độ rộng và chiều cao bảng theo tỷ lệ % hoặc điểm ảnh px", badge_theme='blue')
    add_footer(s18, 18)

    add_card(s18, Inches(0.65), Inches(1.8), Inches(5.5), Inches(4.9), border_color=COLOR_ROYAL, border_width=1.5)
    tb_dim = s18.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_dim = tb_dim.text_frame; tf_dim.word_wrap = True
    p = tf_dim.paragraphs[0]; p.text = "📏 2 ĐƠN VỊ ĐO KÍCH THƯỚC:"
    p.font.name = FONT_HEADING; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    p1 = tf_dim.add_paragraph()
    p1.text = "\n1. Tỉ lệ phần trăm (%):"
    p1.font.name = FONT_HEADING; p1.font.size = Pt(15); p1.font.bold = True; p1.font.color.rgb = COLOR_EMERALD
    p1_d = tf_dim.add_paragraph()
    p1_d.text = "• Co giãn linh hoạt theo màn hình (width: 80%)."
    p1_d.font.name = FONT_BODY; p1_d.font.size = Pt(15); p1_d.font.color.rgb = COLOR_TEXT_BODY

    p2 = tf_dim.add_paragraph()
    p2.text = "\n2. Điểm ảnh (px):"
    p2.font.name = FONT_HEADING; p2.font.size = Pt(15); p2.font.bold = True; p2.font.color.rgb = COLOR_AMBER
    p2_d = tf_dim.add_paragraph()
    p2_d.text = "• Cố định kích thước (height: 400px)."
    p2_d.font.name = FONT_BODY; p2_d.font.size = Pt(15); p2_d.font.color.rgb = COLOR_TEXT_BODY

    add_callout(s18, Inches(0.85), Inches(4.7), Inches(5.1), Inches(1.8), "KHUYẾN CÁO SGK",
                "Khuyên dùng đơn vị % để bảng hiển thị đẹp trên cả điện thoại và máy tính, tránh tràn viền!", theme='warning')

    p_h95 = os.path.join(ASSETS_DIR, 'sgk_hinh9_5.png')
    if os.path.exists(p_h95):
        add_card(s18, Inches(6.35), Inches(1.8), Inches(6.33), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        s18.shapes.add_picture(p_h95, Inches(6.5), Inches(2.6), Inches(6.03), Inches(2.2))
        tb_cap = s18.shapes.add_textbox(Inches(6.5), Inches(5.2), Inches(6.03), Inches(0.8))
        p = tb_cap.text_frame.paragraphs[0]; p.text = "Hình 9.5 SGK: Ví dụ về thuộc tính width và height của bảng"
        p.font.name = FONT_BODY; p.font.size = Pt(13); p.font.italic = True; p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 19: HĐ 2.2 - GỘP CỘT (COLSPAN)
    # =========================================================================
    s19 = prs.slides.add_slide(blank)
    set_slide_background(s19)
    add_header(s19, "HĐ 2.2: KỸ THUẬT GỘP Ô", "GỘP Ô THEO CHIỀU NGANG: THUỘC TÍNH COLSPAN", "Colspan (Column Span): Mở rộng 1 ô chiếm nhiều cột nằm ngang", badge_theme='purple')
    add_footer(s19, 19)

    add_card(s19, Inches(0.65), Inches(1.8), Inches(5.8), Inches(4.9), border_color=COLOR_PURPLE, border_width=1.5)
    tb_col = s19.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(5.4), Inches(4.5))
    tf_col = tb_col.text_frame; tf_col.word_wrap = True

    p = tf_col.paragraphs[0]; p.text = "↔️ BẢN CHẤT COLSPAN:"
    p.font.name = FONT_HEADING; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PURPLE

    p_syn = tf_col.add_paragraph()
    p_syn.text = "\nCú pháp: <th colspan=\"số_cột\">"
    p_syn.font.name = FONT_CODE; p_syn.font.size = Pt(16); p_syn.font.bold = True; p_syn.font.color.rgb = COLOR_PRIMARY

    rules_col = [
        "Mở rộng ô chiếm thêm các cột liền kề bên phải.",
        "Quy tắc cân bằng: Hàng có colspan=\"N\" thì số ô <td> còn lại phải GIẢM ĐI (N - 1) ô!",
        "Tránh thừa ô làm hỏng cấu trúc bảng."
    ]
    for r in rules_col:
        p_r = tf_col.add_paragraph(); p_r.text = f"\n• {r}"
        p_r.font.name = FONT_BODY; p_r.font.size = Pt(15); p_r.font.color.rgb = COLOR_TEXT_BODY

    add_code_editor(s19, Inches(6.65), Inches(1.8), Inches(6.03), Inches(2.7), "colspan.html",
"""<table border="1">
  <tr>
    <th>Họ và tên</th>
    <!-- Gộp 3 cột môn thi -->
    <th colspan="3">Điểm thi các môn</th>
  </tr>
  <tr>
    <td>Nguyễn Văn An</td>
    <td>Toán: 9</td><td>Lí: 8</td><td>Hóa: 9</td>
  </tr>
</table>""", font_size=15)

    add_browser_preview(s19, Inches(6.65), Inches(4.65), Inches(6.03), Inches(2.05), "colspan.html", [
        "┌───────────────┬───────────────────────────────┐",
        "│   Họ và tên   │       Điểm thi các môn        │ (Gộp 3 cột)",
        "├───────────────┼───────────┬───────────┬───────┤",
        "│ Nguyễn Văn An │ Toán: 9   │ Lí: 8     │ Hóa: 9│",
        "└───────────────┴───────────┴───────────┴───────┘"
    ], font_size=15)

    # =========================================================================
    # SLIDE 20: HĐ 2.2 - GỘP HÀNG & CỘT CỦA BẢNG (Dán Image15 từ Word)
    # =========================================================================
    s20 = prs.slides.add_slide(blank)
    set_slide_background(s20)
    add_header(s20, "HĐ 2.2: KỸ THUẬT GỘP Ô", "VÍ DỤ GỘP HÀNG & CỘT CỦA BẢNG (HÌNH 9.6 SGK)", "Đồ họa chi tiết gộp hàng (rowspan) và gộp cột (colspan) từ KHBD.docx", badge_theme='purple')
    add_footer(s20, 20)

    # Dán image15.png lớn ở giữa
    add_card(s20, Inches(0.65), Inches(1.8), Inches(12.03), Inches(4.0), bg_color=COLOR_WHITE, border_color=COLOR_PURPLE, border_width=1.5)
    tb_h_im15 = s20.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.35))
    p = tb_h_im15.text_frame.paragraphs[0]; p.text = "📊 HÌNH 9.6 SGK: VÍ DỤ GỘP HÀNG VÀ CỘT CỦA BẢNG:"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PURPLE
    img15_p = os.path.join(WORD_IMG_DIR, 'image15.png')
    if os.path.exists(img15_p):
        s20.shapes.add_picture(img15_p, Inches(0.85), Inches(2.25), Inches(11.63), Inches(3.45))

    # Nửa dưới: Quy tắc cốt lõi
    add_card(s20, Inches(0.65), Inches(5.9), Inches(12.03), Inches(0.95), bg_color=RGBColor(245, 243, 255), border_color=COLOR_PURPLE, border_width=1.5)
    tb_b_im15 = s20.shapes.add_textbox(Inches(0.85), Inches(5.95), Inches(11.63), Inches(0.8))
    p = tb_b_im15.text_frame.paragraphs[0]
    p.text = "⚡ QUY TẮC ROWSPAN: Thêm rowspan=\"số_hàng\" ở hàng đầu tiên. Ở CÁC HÀNG TIẾP THEO BÊN DƯỚI: BỎ QUA thẻ <th>/<td> tại vị trí tương ứng!"
    p.font.name = FONT_HEADING; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PURPLE

    # =========================================================================
    # SLIDE 21: ĐÁNH GIÁ CHẶNG (QR + UI)
    # =========================================================================
    s21 = prs.slides.add_slide(blank)
    set_slide_background(s21)
    add_header(s21, "ĐÁNH GIÁ CHẶNG (10')", "BÀI KIỂM TRA NHANH: LÀM CHỦ DANH SÁCH & BẢNG HTML", "Vượt qua 5 câu trắc nghiệm để mở khóa bước vào Hoạt động 3 Thực hành!", badge_theme='amber')
    add_footer(s21, 21)

    add_card(s21, Inches(0.65), Inches(1.8), Inches(4.8), Inches(4.9), border_color=COLOR_AMBER, border_width=2)
    qr2_path = os.path.join(ASSETS_DIR, 'qr_phieu2.png')
    if os.path.exists(qr2_path):
        s21.shapes.add_picture(qr2_path, Inches(1.4), Inches(2.05), Inches(3.3), Inches(3.3))

    link_b2 = s21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.5), Inches(4.4), Inches(0.55))
    link_b2.fill.solid(); link_b2.fill.fore_color.rgb = RGBColor(254, 243, 199)
    link_b2.line.color.rgb = COLOR_AMBER
    p = link_b2.text_frame.paragraphs[0]
    p.text = "🔗 minda.io.vn/Tin12/Bai9/phieu-bai-tap-2.html"
    p.font.name = FONT_CODE; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = COLOR_AMBER
    p.alignment = PP_ALIGN.CENTER

    p_dg_ui = os.path.join(ASSETS_DIR, 'illus_danh_gia_chang_ui.png')
    if os.path.exists(p_dg_ui):
        add_card(s21, Inches(5.65), Inches(1.8), Inches(7.03), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        s21.shapes.add_picture(p_dg_ui, Inches(5.8), Inches(2.1), Inches(6.73), Inches(3.2))
        tb_dg = s21.shapes.add_textbox(Inches(5.8), Inches(5.4), Inches(6.73), Inches(1.2))
        tf_dg = tb_dg.text_frame; tf_dg.word_wrap = True
        p = tf_dg.paragraphs[0]; p.text = "🎯 Đạt điểm tối đa: 5/5 điểm để nhận huy hiệu Hoàn thành chặng!"
        p.font.name = FONT_HEADING; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 22: HĐ 3 - GIỚI THIỆU THỰC HÀNH CLB.HTML
    # =========================================================================
    s22 = prs.slides.add_slide(blank)
    set_slide_background(s22, RGBColor(236, 253, 245))
    top_bar = s22.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_EMERALD; top_bar.line.fill.background()
    add_footer(s22, 22)

    add_card(s22, Inches(1.5), Inches(1.2), Inches(10.33), Inches(5.2), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=2)
    
    tag3 = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.41), Inches(1.6), Inches(4.5), Inches(0.48))
    tag3.fill.solid(); tag3.fill.fore_color.rgb = RGBColor(236, 253, 245); tag3.line.color.rgb = COLOR_EMERALD
    p = tag3.text_frame.paragraphs[0]; p.text = "THỰC HÀNH TẠO DANH SÁCH & BẢNG"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    p.alignment = PP_ALIGN.CENTER

    tb_h3 = s22.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.33), Inches(1.5))
    tf_h3 = tb_h3.text_frame; tf_h3.word_wrap = True
    p = tf_h3.paragraphs[0]; p.text = "HOẠT ĐỘNG 3: THỰC HÀNH LẬP TRÌNH (30 PHÚT)"
    p.font.name = FONT_HEADING; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN
    p.alignment = PP_ALIGN.CENTER
    p2 = tf_h3.add_paragraph(); p2.text = "Dự án: Xây dựng trang web giới thiệu Câu lạc bộ trường THPT Thực hành: CLB.html"
    p2.font.name = FONT_BODY; p2.font.size = Pt(15.5); p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    tasks = [
        ("NHIỆM VỤ 1 (15')", "TẠO DANH SÁCH CÂU LẠC BỘ (HÌNH 9.7)", "Lập trình danh sách lồng nhau 3 cấp độ: Thể thao, Nghệ thuật.", COLOR_ROYAL),
        ("NHIỆM VỤ 2 (15')", "LẬP BẢNG LỊCH HOẠT ĐỘNG CLB (HÌNH 9.8)", "Thiết kế bảng 7 hàng, 7 cột; gộp hàng (rowspan) và gộp cột (colspan).", COLOR_EMERALD)
    ]
    for i, (t_time, t_title, t_desc, color) in enumerate(tasks):
        cx = Inches(2.3) + i * Inches(4.5)
        box = add_card(s22, cx, Inches(3.9), Inches(4.2), Inches(2.1), border_color=color, border_width=1.5)
        tp = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.4), Inches(4.1), Inches(3.4), Inches(0.42))
        tp.fill.solid(); tp.fill.fore_color.rgb = color; tp.line.fill.background()
        p = tp.text_frame.paragraphs[0]; p.text = t_time
        p.font.name = FONT_HEADING; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb_sub = s22.shapes.add_textbox(cx + Inches(0.2), Inches(4.65), Inches(3.8), Inches(1.3))
        tf_s = tb_sub.text_frame; tf_s.word_wrap = True
        p_s1 = tf_s.paragraphs[0]; p_s1.text = t_title
        p_s1.font.name = FONT_HEADING; p_s1.font.size = Pt(12); p_s1.font.bold = True; p_s1.font.color.rgb = COLOR_TEXT_TITLE
        p_s1.alignment = PP_ALIGN.CENTER
        p_s2 = tf_s.add_paragraph(); p_s2.text = t_desc
        p_s2.font.name = FONT_BODY; p_s2.font.size = Pt(11.5); p_s2.font.color.rgb = COLOR_TEXT_MUTED
        p_s2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 23: HĐ 3 - THỰC HÀNH TỔNG HỢP (Dán Image16 từ Word)
    # =========================================================================
    s23 = prs.slides.add_slide(blank)
    set_slide_background(s23)
    add_header(s23, "HĐ 3: THỰC HÀNH LẬP TRÌNH", "HƯỚNG DẪN THỰC HÀNH: NHIỆM VỤ 1 & NHIỆM VỤ 2", "Đồ họa tổng hợp đầy đủ từ Kế hoạch bài dạy KHBD.docx", badge_theme='green')
    add_footer(s23, 23)

    # Dán image16.png lớn chiếm gần trọn slide
    add_card(s23, Inches(0.65), Inches(1.8), Inches(12.03), Inches(5.0), bg_color=COLOR_WHITE, border_color=COLOR_EMERALD, border_width=1.5)
    img16_p = os.path.join(WORD_IMG_DIR, 'image16.png')
    if os.path.exists(img16_p):
        s23.shapes.add_picture(img16_p, Inches(1.8), Inches(1.9), Inches(9.73), Inches(4.8))

    # =========================================================================
    # SLIDE 24: HĐ 3 - CHI TIẾT NHIỆM VỤ 2 (LẬP BẢNG LỊCH CLB)
    # =========================================================================
    s24 = prs.slides.add_slide(blank)
    set_slide_background(s24)
    add_header(s24, "HĐ 3: THỰC HÀNH LẬP TRÌNH", "NHIỆM VỤ 2: LẬP BẢNG LỊCH HOẠT ĐỘNG CLB (HÌNH 9.8 SGK)", "Thiết kế bảng 7 hàng, 7 cột & Gộp ô rowspan, colspan", badge_theme='green')
    add_footer(s24, 24)

    add_card(s24, Inches(0.65), Inches(1.8), Inches(6.0), Inches(4.9), border_color=COLOR_EMERALD, border_width=1.5)
    tb_n2 = s24.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(5.6), Inches(4.5))
    tf_n2 = tb_n2.text_frame; tf_n2.word_wrap = True
    p = tf_n2.paragraphs[0]; p.text = "📊 PHÂN TÍCH CẤU TRÚC BẢNG:"
    p.font.name = FONT_HEADING; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN

    specs_n2 = [
        "Quy mô: Đúng 7 hàng và 7 cột.",
        "Tiêu đề: <caption>Lịch hoạt động CLB Thể thao</caption>",
        "Gộp hàng dọc: Bộ môn và GV phụ trách (rowspan=\"2\").",
        "Gộp hàng ngang: Ngày (colspan=\"5\").",
        "Lưu tên tệp: CLB.html"
    ]
    for sp in specs_n2:
        p_sp = tf_n2.add_paragraph()
        p_sp.text = f"\n• {sp}"
        p_sp.font.name = FONT_BODY; p_sp.font.size = Pt(16); p_sp.font.color.rgb = COLOR_TEXT_BODY

    p_h98 = os.path.join(ASSETS_DIR, 'sgk_hinh9_8.png')
    if os.path.exists(p_h98):
        add_card(s24, Inches(6.85), Inches(1.8), Inches(5.83), Inches(4.9), bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        s24.shapes.add_picture(p_h98, Inches(7.0), Inches(2.4), Inches(5.5), Inches(3.6))

    # =========================================================================
    # SLIDE 25: HĐ 3 - TIÊU CHÍ ĐÁNH GIÁ & NỘP BÀI
    # =========================================================================
    s25 = prs.slides.add_slide(blank)
    set_slide_background(s25)
    add_header(s25, "HĐ 3: THỰC HÀNH LẬP TRÌNH", "TIÊU CHÍ ĐÁNH GIÁ SẢN PHẨM & QUY TRÌNH NỘP BÀI", "Thang điểm 10 đánh giá năng lực lập trình và nộp bài trực tuyến", badge_theme='green')
    add_footer(s25, 25)

    add_card(s25, Inches(0.65), Inches(1.8), Inches(7.5), Inches(4.9), border_color=COLOR_EMERALD, border_width=1.5)
    tb_rb = s25.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(7.1), Inches(4.5))
    tf_rb = tb_rb.text_frame; tf_rb.word_wrap = True
    p = tf_rb.paragraphs[0]; p.text = "🎯 THANG ĐIỂM ĐÁNH GIÁ (RUBRIC 10Đ):"
    p.font.name = FONT_HEADING; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN

    rubric_short = [
        ("1. Cấu trúc chuẩn HTML5 (2.0đ):", "Đầy đủ <!DOCTYPE>, <html>, <head>, <body>, mã utf-8."),
        ("2. Danh sách lồng nhau (2.5đ):", "Đủ cụm THỂ THAO & NGHỆ THUẬT, phân cấp 3 cấp W3C."),
        ("3. Cấu trúc bảng & caption (2.5đ):", "Có <caption>, đủ 7 hàng 7 cột, phân biệt đúng <th> và <td>."),
        ("4. Kỹ thuật gộp ô (2.0đ):", "Gộp đúng rowspan=\"2\" và colspan=\"5\", không lệch cột."),
        ("5. Tinh thần hợp tác & Nộp đúng hạn (1.0đ):", "Lưu tên tệp CLB.html và nộp lên hệ thống trước giờ kết thúc.")
    ]
    for r_head, r_desc in rubric_short:
        p_r = tf_rb.add_paragraph()
        p_r.text = f"\n{r_head} "
        p_r.font.name = FONT_HEADING; p_r.font.size = Pt(14); p_r.font.bold = True; p_r.font.color.rgb = COLOR_PRIMARY
        run = p_r.add_run(); run.text = r_desc
        run.font.name = FONT_BODY; run.font.size = Pt(13.5); run.font.color.rgb = COLOR_TEXT_BODY

    add_card(s25, Inches(8.35), Inches(1.8), Inches(4.33), Inches(4.9), bg_color=RGBColor(240, 253, 244), border_color=COLOR_EMERALD, border_width=1.5)
    tb_subm = s25.shapes.add_textbox(Inches(8.55), Inches(2.0), Inches(3.9), Inches(4.5))
    tf_s = tb_subm.text_frame; tf_s.word_wrap = True
    p = tf_s.paragraphs[0]; p.text = "📤 4 BƯỚC NỘP BÀI:"
    p.font.name = FONT_HEADING; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN

    p_sub = [
        "1. Lưu tệp: CLB.html",
        "2. Kiểm tra trên trình duyệt.",
        "3. Vào web: HĐ 3 - Luyện tập.",
        "4. Điền Tên + Số máy và bấm [Nộp bài]."
    ]
    for s_pt in p_sub:
        p_sp = tf_s.add_paragraph(); p_sp.text = f"\n✔ {s_pt}"
        p_sp.font.name = FONT_BODY; p_sp.font.size = Pt(14); p_sp.font.color.rgb = COLOR_TEXT_TITLE

    # =========================================================================
    # SLIDE 26: HĐ 4 - INFOGRAPHIC CHEAT SHEET
    # =========================================================================
    s26 = prs.slides.add_slide(blank)
    set_slide_background(s26)
    add_header(s26, "HĐ 4: TỔNG KẾT KIẾN THỨC", "INFOGRAPHIC CHEAT SHEET BÀI 9", "Toàn bộ cú pháp và thuộc tính cốt lõi cần ghi nhớ", badge_theme='purple')
    add_footer(s26, 26)

    c_w = Inches(5.85)
    c_h = Inches(4.9)

    add_card(s26, Inches(0.65), Inches(1.8), c_w, c_h, border_color=COLOR_ROYAL, border_width=1.5)
    h_ds = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(2.0), Inches(5.45), Inches(0.5))
    h_ds.fill.solid(); h_ds.fill.fore_color.rgb = COLOR_ROYAL; h_ds.line.fill.background()
    p = h_ds.text_frame.paragraphs[0]; p.text = "1. HỆ THỐNG DANH SÁCH (LISTS)"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_cs1 = s26.shapes.add_textbox(Inches(0.85), Inches(2.6), Inches(5.45), Inches(3.9))
    tf_cs1 = tb_cs1.text_frame; tf_cs1.word_wrap = True
    cs1_items = [
        ("<ol>:", "Có thứ tự. type=\"1|A|a|I|i\", start=\"số\""),
        ("<ul>:", "Không thứ tự. list-style-type: disc|circle|square|none"),
        ("<li>:", "Mục con trong danh sách."),
        ("<dl>, <dt>, <dd>:", "Danh sách mô tả thuật ngữ."),
        ("Lồng nhau:", "Đặt danh sách con trong <li> cha.")
    ]
    for hd, dt in cs1_items:
        p_c = tf_cs1.add_paragraph()
        p_c.text = f"\n• {hd} "
        p_c.font.name = FONT_CODE; p_c.font.size = Pt(14); p_c.font.bold = True; p_c.font.color.rgb = COLOR_PRIMARY
        run = p_c.add_run(); run.text = dt
        run.font.name = FONT_BODY; run.font.size = Pt(14); run.font.color.rgb = COLOR_TEXT_BODY

    add_card(s26, Inches(6.83), Inches(1.8), c_w, c_h, border_color=COLOR_EMERALD, border_width=1.5)
    h_tb = s26.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.03), Inches(2.0), Inches(5.45), Inches(0.5))
    h_tb.fill.solid(); h_tb.fill.fore_color.rgb = COLOR_EMERALD; h_tb.line.fill.background()
    p = h_tb.text_frame.paragraphs[0]; p.text = "2. THIẾT LẬP BẢNG (TABLES)"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_cs2 = s26.shapes.add_textbox(Inches(7.03), Inches(2.6), Inches(5.45), Inches(3.9))
    tf_cs2 = tb_cs2.text_frame; tf_cs2.word_wrap = True
    cs2_items = [
        ("<table>, <tr>, <th>, <td>:", "4 thẻ cơ bản xây dựng hàng và cột."),
        ("<caption>:", "Tiêu đề bảng (ngay sau <table>)."),
        ("border:", "Viền: độ_dày kiểu_viền màu_viền."),
        ("width / height:", "Kích thước theo % hoặc px."),
        ("colspan / rowspan:", "colspan gộp cột, rowspan gộp hàng.")
    ]
    for hd, dt in cs2_items:
        p_c = tf_cs2.add_paragraph()
        p_c.text = f"\n• {hd} "
        p_c.font.name = FONT_CODE; p_c.font.size = Pt(14); p_c.font.bold = True; p_c.font.color.rgb = COLOR_DARK_GREEN
        run = p_c.add_run(); run.text = dt
        run.font.name = FONT_BODY; run.font.size = Pt(14); run.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 27: HĐ 5 - VẬN DỤNG & NHIỆM VỤ VỀ NHÀ
    # =========================================================================
    s27 = prs.slides.add_slide(blank)
    set_slide_background(s27)
    add_header(s27, "HĐ 5: VẬN DỤNG & VỀ NHÀ", "NHIỆM VỤ VẬN DỤNG & CHUẨN BỊ BÀI 10", "Củng cố kiến thức và mở rộng dự án trang web CLB", badge_theme='amber')
    add_footer(s27, 27)

    tasks_hw = [
        ("1. HOÀN THIỆN CLB.HTML", [
            "Bổ sung lịch sinh hoạt các môn NGHỆ THUẬT vào bảng.",
            "Tô màu nền cho tiêu đề <th> bằng style=\"background: ...\"."
        ], COLOR_ROYAL),
        ("2. BÀI TẬP SGK TRANG 56", [
            "Làm bài Luyện tập 1 & 2 trang 56 SGK.",
            "Bài tập Vận dụng: Tạo Thời khóa biểu cá nhân bằng bảng HTML."
        ], COLOR_EMERALD),
        ("3. CHUẨN BỊ BÀI 10", [
            "Đọc trước Bài 10: Chèn liên kết <a> và hình ảnh <img>.",
            "Chuẩn bị 2-3 bức ảnh đẹp về lớp để chèn vào web."
        ], COLOR_AMBER)
    ]

    for i, (head, points, color) in enumerate(tasks_hw):
        cx = Inches(0.65) + i * Inches(4.11)
        add_card(s27, cx, Inches(1.8), Inches(3.8), Inches(4.9), border_color=color, border_width=2)
        hb = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), Inches(2.0), Inches(3.4), Inches(0.6))
        hb.fill.solid(); hb.fill.fore_color.rgb = color; hb.line.fill.background()
        tf = hb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.text = head
        p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = s27.shapes.add_textbox(cx + Inches(0.2), Inches(2.8), Inches(3.4), Inches(3.7))
        tf_b = tb.text_frame; tf_b.word_wrap = True
        for j, pt in enumerate(points):
            p_pt = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p_pt.text = f"\n• {pt}"
            p_pt.font.name = FONT_BODY; p_pt.font.size = Pt(16); p_pt.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 28: KẾT THÚC & CẢM ƠN (Chỉ để tên GV: Nguyễn Lê Minh Ngọc)
    # =========================================================================
    s28 = prs.slides.add_slide(blank)
    set_slide_background(s28, RGBColor(241, 245, 249))

    top_bar = s28.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY; top_bar.line.fill.background()

    card_end = add_card(s28, Inches(1.8), Inches(1.0), Inches(9.73), Inches(5.5), bg_color=COLOR_WHITE, border_color=COLOR_ROYAL, border_width=2)

    s_tag = s28.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.86), Inches(1.5), Inches(7.6), Inches(0.48))
    s_tag.fill.solid(); s_tag.fill.fore_color.rgb = RGBColor(238, 242, 255); s_tag.line.color.rgb = COLOR_ROYAL
    p = s_tag.text_frame.paragraphs[0]; p.text = "TRƯỜNG THPT THỰC HÀNH - ĐẠI HỌC SƯ PHẠM TP. HỒ CHÍ MINH"
    p.font.name = FONT_HEADING; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    tb_e = s28.shapes.add_textbox(Inches(2.2), Inches(2.3), Inches(8.93), Inches(2.0))
    tf_e = tb_e.text_frame; tf_e.word_wrap = True

    p = tf_e.paragraphs[0]; p.text = "CẢM ƠN QUÝ THẦY CÔ VÀ CÁC EM HỌC SINH!"
    p.font.name = FONT_HEADING; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_e.add_paragraph()
    p2.text = "Chúc các em luôn đam mê sáng tạo & tự tin làm chủ công nghệ lập trình Web!"
    p2.font.name = FONT_BODY; p2.font.size = Pt(17); p2.font.color.rgb = COLOR_ROYAL
    p2.alignment = PP_ALIGN.CENTER

    # Teacher Badge: CHỈ ĐỂ TÊN NGUYỄN LÊ MINH NGỌC
    tb_gv_end = s28.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.86), Inches(4.3), Inches(5.6), Inches(1.1))
    tb_gv_end.fill.solid(); tb_gv_end.fill.fore_color.rgb = RGBColor(238, 242, 255)
    tb_gv_end.line.color.rgb = COLOR_ROYAL; tb_gv_end.line.width = Pt(1.5)
    tf_ge = tb_gv_end.text_frame; tf_ge.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    p = tf_ge.paragraphs[0]; p.text = "👨‍🏫 GIÁO VIÊN:"
    p.font.name = FONT_HEADING; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_ge.add_paragraph(); p2.text = "Nguyễn Lê Minh Ngọc"
    p2.font.name = FONT_HEADING; p2.font.size = Pt(22); p2.font.bold = True; p2.font.color.rgb = COLOR_ROYAL
    p2.alignment = PP_ALIGN.CENTER

    tb_w = s28.shapes.add_textbox(Inches(2.2), Inches(5.6), Inches(8.93), Inches(0.5))
    p = tb_w.text_frame.paragraphs[0]; p.text = "🌐 Hệ thống học tập trực tuyến: minda.io.vn"
    p.font.name = FONT_CODE; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD
    p.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPTX)
    print(f"✅ Đã cập nhật thành công 28 slides với toàn bộ hình Word tại: {OUTPUT_PPTX}")

if __name__ == '__main__':
    build_all_slides()
