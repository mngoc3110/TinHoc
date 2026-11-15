# -*- coding: utf-8 -*-
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

COLOR_PRIMARY = RGBColor(30, 58, 138)
COLOR_ROYAL = RGBColor(37, 99, 235)
COLOR_EMERALD = RGBColor(16, 185, 129)
COLOR_DARK_GREEN = RGBColor(21, 128, 61)
COLOR_AMBER = RGBColor(217, 119, 6)
COLOR_RED = RGBColor(220, 38, 38)
COLOR_PURPLE = RGBColor(147, 51, 234)
COLOR_SLATE_900 = RGBColor(15, 23, 42)
COLOR_TEXT_TITLE = RGBColor(15, 23, 42)
COLOR_TEXT_BODY = RGBColor(30, 41, 59)
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)
COLOR_BG_MAIN = RGBColor(248, 250, 252)
COLOR_CARD_BORDER = RGBColor(203, 213, 225)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CODE_BG = RGBColor(15, 23, 42)
COLOR_CODE_TEXT = RGBColor(226, 232, 240)

COLOR_MAP = {
    "blue": COLOR_ROYAL,
    "navy": COLOR_PRIMARY,
    "green": COLOR_EMERALD,
    "emerald": COLOR_EMERALD,
    "amber": COLOR_AMBER,
    "red": COLOR_RED,
    "purple": COLOR_PURPLE,
}


def set_bg(slide, color=COLOR_BG_MAIN):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_card(slide, left, top, width, height, bg=COLOR_WHITE, border=COLOR_CARD_BORDER, bw=1.2):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    s.adjustments[0] = 0.03
    s.fill.solid()
    s.fill.fore_color.rgb = bg
    if border:
        s.line.color.rgb = border
        s.line.width = Pt(bw)
    else:
        s.line.fill.background()
    return s


def add_header(slide, badge_text, title_text, subtitle_text="", theme="blue"):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_MAP.get(theme, COLOR_ROYAL)
    bar.line.fill.background()

    hcard = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.08), Inches(13.333), Inches(1.38))
    hcard.fill.solid()
    hcard.fill.fore_color.rgb = COLOR_WHITE
    hcard.line.color.rgb = RGBColor(226, 232, 240)
    hcard.line.width = Pt(1)

    badge_bg = RGBColor(239, 246, 255)
    badge_fg = COLOR_ROYAL
    if theme == "green" or theme == "emerald":
        badge_bg, badge_fg = RGBColor(236, 253, 245), COLOR_DARK_GREEN
    elif theme == "amber":
        badge_bg, badge_fg = RGBColor(255, 251, 235), COLOR_AMBER
    elif theme == "purple":
        badge_bg, badge_fg = RGBColor(245, 243, 255), COLOR_PURPLE
    elif theme == "red":
        badge_bg, badge_fg = RGBColor(254, 242, 242), COLOR_RED

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(0.22), Inches(3.25), Inches(0.36))
    badge.adjustments[0] = 0.25
    badge.fill.solid()
    badge.fill.fore_color.rgb = badge_bg
    badge.line.color.rgb = badge_fg
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.margin_left = tf_b.margin_right = Pt(6)
    pb = tf_b.paragraphs[0]
    pb.text = badge_text
    pb.font.name = FONT_HEADING
    pb.font.size = Pt(11.5)
    pb.font.bold = True
    pb.font.color.rgb = badge_fg
    pb.alignment = PP_ALIGN.CENTER

    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.60), Inches(12.0), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_HEADING
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    if subtitle_text:
        tb2 = slide.shapes.add_textbox(Inches(4.05), Inches(0.24), Inches(8.6), Inches(0.36))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = subtitle_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.alignment = PP_ALIGN.RIGHT


def add_footer(slide, num, total, lesson_short):
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(7.05), Inches(12.03), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = f"Tin học 12 • {lesson_short} • THTH-DHSP • GV: Nguyễn Lê Minh Ngọc        Trang {num}/{total}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_MUTED


def add_code_panel(slide, left, top, width, height, code_str, filename="index.html"):
    add_card(slide, left, top, width, height, bg=COLOR_CODE_BG, border=RGBColor(51, 65, 85), bw=1.5)
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.42))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = RGBColor(30, 41, 59)
    hdr.line.fill.background()

    for idx, clr in enumerate((RGBColor(239, 68, 68), RGBColor(245, 158, 11), RGBColor(34, 197, 94))):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.16 + idx * 0.22), top + Inches(0.14), Inches(0.13), Inches(0.13))
        dot.fill.solid()
        dot.fill.fore_color.rgb = clr
        dot.line.fill.background()

    th = slide.shapes.add_textbox(left + Inches(0.9), top + Inches(0.06), width - Inches(1.1), Inches(0.32))
    ph = th.text_frame.paragraphs[0]
    ph.text = f"📄 {filename}"
    ph.font.name = FONT_CODE
    ph.font.size = Pt(12)
    ph.font.color.rgb = RGBColor(148, 163, 184)

    tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.52), width - Inches(0.44), height - Inches(0.62))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = code_str.strip().splitlines()
    fsize = Pt(14) if len(lines) <= 10 else (Pt(13) if len(lines) <= 14 else Pt(11.5))
    for idx, line in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = FONT_CODE
        p.font.size = fsize
        p.font.color.rgb = RGBColor(125, 211, 252) if "<" in line and ">" in line else COLOR_CODE_TEXT


def add_bullets_box(slide, left, top, width, height, heading, bullets, heading_color=COLOR_PRIMARY, body_size=15.5):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = heading
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = heading_color
    p0.space_after = Pt(8)

    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.name = FONT_BODY
        p.font.size = Pt(body_size)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_before = Pt(5)
        p.space_after = Pt(4)


def add_picture_fitted(slide, img_path, left, top, max_w, max_h):
    if not os.path.exists(img_path):
        return
    from PIL import Image
    with Image.open(img_path) as im:
        iw, ih = im.size
    ratio = iw / max(ih, 1)
    box_ratio = max_w / max(max_h, 1)
    if ratio > box_ratio:
        w = max_w
        h = w / ratio
    else:
        h = max_h
        w = h * ratio
    x = left + (max_w - w) / 2
    y = top + (max_h - h) / 2
    slide.shapes.add_picture(img_path, x, y, w, h)


def build_from_slides_data(slides_data, lesson_short, assets_dir, out_pptx):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides_data)

    for idx, sd in enumerate(slides_data, start=1):
        sl = prs.slides.add_slide(blank)
        kind = sd["kind"]

        if kind == "cover":
            set_bg(sl, COLOR_SLATE_900)
            bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.14))
            bar.fill.solid(); bar.fill.fore_color.rgb = COLOR_ROYAL; bar.line.fill.background()

            pill = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(1.1), Inches(6.2), Inches(0.5))
            pill.fill.solid(); pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
            pill.line.color.rgb = RGBColor(96, 165, 250); pill.line.width = Pt(1.2)
            pp = pill.text_frame.paragraphs[0]
            pp.text = sd["pill"]
            pp.font.name = FONT_HEADING; pp.font.size = Pt(14); pp.font.bold = True; pp.font.color.rgb = RGBColor(191, 219, 254)
            pp.alignment = PP_ALIGN.CENTER

            tb = sl.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.6), Inches(1.9))
            tf = tb.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.text = sd["title"]
            p.font.name = FONT_HEADING; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = COLOR_WHITE

            p2 = tf.add_paragraph(); p2.text = "\n" + sd["subtitle"]
            p2.font.name = FONT_BODY; p2.font.size = Pt(18); p2.font.color.rgb = RGBColor(203, 213, 225)

            meta = slide_meta = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.35), Inches(11.6), Inches(1.25))
            meta.fill.solid(); meta.fill.fore_color.rgb = RGBColor(30, 41, 59)
            meta.line.color.rgb = RGBColor(71, 85, 105); meta.line.width = Pt(1)
            mtf = meta.text_frame; mtf.word_wrap = True
            mp = mtf.paragraphs[0]
            mp.text = f"  Trường: THTH-DHSP   •   Giáo viên: Nguyễn Lê Minh Ngọc   •   {sd['meta']}"
            mp.font.name = FONT_HEADING; mp.font.size = Pt(16); mp.font.bold = True; mp.font.color.rgb = RGBColor(147, 197, 253)
            mp2 = mtf.add_paragraph()
            mp2.text = f"  Học liệu trực tuyến: {sd['url']}"
            mp2.font.name = FONT_BODY; mp2.font.size = Pt(14); mp2.font.color.rgb = RGBColor(226, 232, 240)

        elif kind == "objectives":
            set_bg(sl)
            add_header(sl, sd.get("badge", "MỤC TIÊU BÀI HỌC"), sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            cards = sd["cards"][:4]
            cw, ch = Inches(5.85), Inches(2.35)
            coords = [(Inches(0.65), Inches(1.72)), (Inches(6.83), Inches(1.72)),
                      (Inches(0.65), Inches(4.32)), (Inches(6.83), Inches(4.32))]
            for (x, y), c in zip(coords, cards):
                col = COLOR_MAP.get(c.get("color", "blue"), COLOR_ROYAL)
                add_card(sl, x, y, cw, ch, border=col, bw=1.8)
                add_bullets_box(sl, x + Inches(0.25), y + Inches(0.18), cw - Inches(0.5), ch - Inches(0.32),
                                c["heading"], c["bullets"], heading_color=col, body_size=15)

        elif kind == "roadmap":
            set_bg(sl)
            add_header(sl, "TIẾN TRÌNH BÀI DẠY", sd["title"], sd.get("sub", "Tổ chức theo mô hình 4 hoạt động Công văn 5512"), "purple")
            add_footer(sl, idx, total, lesson_short)
            rows = sd["rows"]
            row_h = Inches(min(1.02, 4.9 / max(len(rows), 1)))
            for r_i, r in enumerate(rows):
                y = Inches(1.75) + r_i * (row_h + Inches(0.12))
                col = COLOR_MAP.get(r.get("color", "blue"), COLOR_ROYAL)
                add_card(sl, Inches(0.65), y, Inches(12.03), row_h, border=col, bw=1.5)
                pill = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), y + Inches(0.16), Inches(3.05), row_h - Inches(0.32))
                pill.fill.solid(); pill.fill.fore_color.rgb = col; pill.line.fill.background()
                ptf = pill.text_frame; ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
                pp = ptf.paragraphs[0]; pp.text = r["stage"]
                pp.font.name = FONT_HEADING; pp.font.size = Pt(14); pp.font.bold = True; pp.font.color.rgb = COLOR_WHITE; pp.alignment = PP_ALIGN.CENTER

                tb = sl.shapes.add_textbox(Inches(4.15), y + Inches(0.14), Inches(8.3), row_h - Inches(0.28))
                tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = tf.paragraphs[0]; p.text = r["desc"]
                p.font.name = FONT_BODY; p.font.size = Pt(15.5); p.font.color.rgb = COLOR_TEXT_BODY

        elif kind == "section":
            set_bg(sl, RGBColor(238, 242, 255))
            col = COLOR_MAP.get(sd.get("theme", "blue"), COLOR_ROYAL)
            bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
            bar.fill.solid(); bar.fill.fore_color.rgb = col; bar.line.fill.background()
            add_footer(sl, idx, total, lesson_short)

            add_card(sl, Inches(1.1), Inches(1.05), Inches(11.13), Inches(5.35), border=col, bw=2.2)
            tag = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.4), Inches(1.4), Inches(4.5), Inches(0.46))
            tag.fill.solid(); tag.fill.fore_color.rgb = RGBColor(239, 246, 255); tag.line.color.rgb = col
            pt = tag.text_frame.paragraphs[0]; pt.text = sd["tag"]
            pt.font.name = FONT_HEADING; pt.font.size = Pt(14); pt.font.bold = True; pt.font.color.rgb = col; pt.alignment = PP_ALIGN.CENTER

            tb = sl.shapes.add_textbox(Inches(1.6), Inches(2.05), Inches(10.1), Inches(1.6))
            tf = tb.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.text = sd["title"]
            p.font.name = FONT_HEADING; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.alignment = PP_ALIGN.CENTER
            p2 = tf.add_paragraph(); p2.text = "\n" + sd.get("subtitle", "")
            p2.font.name = FONT_BODY; p2.font.size = Pt(16.5); p2.font.color.rgb = COLOR_TEXT_MUTED; p2.alignment = PP_ALIGN.CENTER

            pills = sd.get("pills", [])[:3]
            for pi, (ptitle, pdesc, pcol_name) in enumerate(pills):
                cx = Inches(1.55) + pi * Inches(3.52)
                pcol = COLOR_MAP.get(pcol_name, COLOR_ROYAL)
                add_card(sl, cx, Inches(3.9), Inches(3.22), Inches(2.15), border=pcol, bw=1.5)
                ptag = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.22), Inches(4.08), Inches(2.78), Inches(0.44))
                ptag.fill.solid(); ptag.fill.fore_color.rgb = pcol; ptag.line.fill.background()
                pp = ptag.text_frame.paragraphs[0]; pp.text = ptitle
                pp.font.name = FONT_HEADING; pp.font.size = Pt(14); pp.font.bold = True; pp.font.color.rgb = COLOR_WHITE; pp.alignment = PP_ALIGN.CENTER
                tbd = sl.shapes.add_textbox(cx + Inches(0.2), Inches(4.65), Inches(2.82), Inches(1.25))
                tfd = tbd.text_frame; tfd.word_wrap = True
                pd = tfd.paragraphs[0]; pd.text = pdesc
                pd.font.name = FONT_BODY; pd.font.size = Pt(14.5); pd.font.color.rgb = COLOR_TEXT_BODY; pd.alignment = PP_ALIGN.CENTER

        elif kind == "two_col":
            set_bg(sl)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            for ci, col_data in enumerate((sd["left"], sd["right"])):
                x = Inches(0.65) if ci == 0 else Inches(6.8)
                c = COLOR_MAP.get(col_data.get("color", "blue"), COLOR_ROYAL)
                add_card(sl, x, Inches(1.72), Inches(5.88), Inches(5.1), border=c, bw=1.8)
                add_bullets_box(sl, x + Inches(0.28), Inches(1.92), Inches(5.32), Inches(4.7),
                                col_data["heading"], col_data["bullets"], heading_color=c, body_size=15.5)

        elif kind == "three_col":
            set_bg(sl)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            for ci, col_data in enumerate(sd["cols"][:3]):
                x = Inches(0.65) + ci * Inches(4.11)
                c = COLOR_MAP.get(col_data.get("color", "blue"), COLOR_ROYAL)
                add_card(sl, x, Inches(1.75), Inches(3.81), Inches(5.05), border=c, bw=1.8)
                hdr = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), Inches(1.95), Inches(3.41), Inches(0.62))
                hdr.fill.solid(); hdr.fill.fore_color.rgb = c; hdr.line.fill.background()
                htf = hdr.text_frame; htf.vertical_anchor = MSO_ANCHOR.MIDDLE; htf.word_wrap = True
                hp = htf.paragraphs[0]; hp.text = col_data["heading"]
                hp.font.name = FONT_HEADING; hp.font.size = Pt(15); hp.font.bold = True; hp.font.color.rgb = COLOR_WHITE; hp.alignment = PP_ALIGN.CENTER

                add_bullets_box(sl, x + Inches(0.24), Inches(2.75), Inches(3.33), Inches(3.85),
                                col_data.get("subhead", ""), col_data["bullets"], heading_color=c, body_size=15)

        elif kind == "code_result":
            set_bg(sl)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            add_code_panel(sl, Inches(0.65), Inches(1.72), Inches(6.25), Inches(5.1), sd["code"], sd.get("filename", "index.html"))

            add_card(sl, Inches(7.1), Inches(1.72), Inches(5.58), Inches(5.1), border=COLOR_EMERALD, bw=1.8)
            add_bullets_box(sl, Inches(7.35), Inches(1.9), Inches(5.08), Inches(2.4),
                            sd.get("right_heading", "👁️ KẾT QUẢ & LƯU Ý:"),
                            sd["notes"], heading_color=COLOR_DARK_GREEN, body_size=15)
            if sd.get("image"):
                add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(7.3), Inches(4.25), Inches(5.18), Inches(2.4))

        elif kind == "image_focus":
            set_bg(sl)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            add_card(sl, Inches(0.65), Inches(1.72), Inches(5.15), Inches(5.1), border=COLOR_ROYAL, bw=1.8)
            add_bullets_box(sl, Inches(0.9), Inches(1.92), Inches(4.65), Inches(4.7),
                            sd["heading"], sd["bullets"], heading_color=COLOR_PRIMARY, body_size=15.5)

            add_card(sl, Inches(6.02), Inches(1.72), Inches(6.66), Inches(5.1), border=COLOR_CARD_BORDER, bw=1.5)
            add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(6.22), Inches(1.9), Inches(6.26), Inches(4.25))
            if sd.get("caption"):
                tb = sl.shapes.add_textbox(Inches(6.2), Inches(6.28), Inches(6.3), Inches(0.45))
                p = tb.text_frame.paragraphs[0]; p.text = sd["caption"]
                p.font.name = FONT_BODY; p.font.size = Pt(13.5); p.font.italic = True; p.font.color.rgb = COLOR_TEXT_MUTED; p.alignment = PP_ALIGN.CENTER

        elif kind == "quiz":
            set_bg(sl)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", "Trả lời nhanh & giải thích"), "amber")
            add_footer(sl, idx, total, lesson_short)
            add_card(sl, Inches(0.65), Inches(1.72), Inches(12.03), Inches(1.65), border=COLOR_AMBER, bw=1.8)
            add_bullets_box(sl, Inches(0.9), Inches(1.85), Inches(11.53), Inches(1.4),
                            "❓ CÂU HỎI / TÌNH HUỐNG:", [sd["question"]], heading_color=COLOR_AMBER, body_size=16.5)

            add_card(sl, Inches(0.65), Inches(3.58), Inches(5.85), Inches(3.25), border=COLOR_ROYAL, bw=1.5)
            add_bullets_box(sl, Inches(0.9), Inches(3.72), Inches(5.35), Inches(2.95),
                            "📌 CÁC PHƯƠNG ÁN / Ý XÉT:", sd["options"], heading_color=COLOR_PRIMARY, body_size=15)

            add_card(sl, Inches(6.8), Inches(3.58), Inches(5.88), Inches(3.25), border=COLOR_EMERALD, bw=1.8)
            add_bullets_box(sl, Inches(7.05), Inches(3.72), Inches(5.38), Inches(2.95),
                            "✅ ĐÁP ÁN & GIẢI THÍCH:", sd["answer"], heading_color=COLOR_DARK_GREEN, body_size=15)

        elif kind == "thank_you":
            set_bg(sl, COLOR_SLATE_900)
            bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.14))
            bar.fill.solid(); bar.fill.fore_color.rgb = COLOR_EMERALD; bar.line.fill.background()

            tb = sl.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(1.2))
            tf = tb.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.text = sd["title"]
            p.font.name = FONT_HEADING; p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

            add_card(sl, Inches(1.0), Inches(2.35), Inches(11.33), Inches(2.85), bg=RGBColor(30, 41, 59), border=COLOR_EMERALD, bw=1.8)
            tbm = sl.shapes.add_textbox(Inches(1.35), Inches(2.55), Inches(10.6), Inches(2.5))
            tfm = tbm.text_frame; tfm.word_wrap = True
            pm0 = tfm.paragraphs[0]; pm0.text = "📌 GHI NHỚ TRỌNG TÂM & DẶN DÒ:"
            pm0.font.name = FONT_HEADING; pm0.font.size = Pt(18); pm0.font.bold = True; pm0.font.color.rgb = RGBColor(110, 231, 183)
            for point in sd["takeaways"]:
                pm = tfm.add_paragraph(); pm.text = f"• {point}"
                pm.font.name = FONT_BODY; pm.font.size = Pt(15.5); pm.font.color.rgb = RGBColor(241, 245, 249); pm.space_before = Pt(6)

            tb_end = sl.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.1))
            tfe = tb_end.text_frame
            pe = tfe.paragraphs[0]; pe.text = "TRÂN TRỌNG CẢM ƠN CÁC EM ĐÃ THAM GIA TIẾT HỌC!"
            pe.font.name = FONT_HEADING; pe.font.size = Pt(20); pe.font.bold = True; pe.font.color.rgb = RGBColor(147, 197, 253); pe.alignment = PP_ALIGN.CENTER
            pe2 = tfe.add_paragraph(); pe2.text = "THTH-DHSP • Giáo viên: Nguyễn Lê Minh Ngọc"
            pe2.font.name = FONT_BODY; pe2.font.size = Pt(15); pe2.font.color.rgb = RGBColor(203, 213, 225); pe2.alignment = PP_ALIGN.CENTER

    prs.save(out_pptx)
    print(f"Generated PPTX: {out_pptx} ({total} slides)")

SLIDES_DATA = [
  {
    "kind": "cover",
    "pill": "TIN HỌC 12 • KẾT NỐI TRI THỨC • CHỦ ĐỀ F",
    "title": "BÀI 10: TẠO LIÊN KẾT",
    "subtitle": "Siêu văn bản, đường dẫn tuyệt đối/tương đối và kĩ thuật tạo liên kết đa tệp HTML",
    "meta": "Tiết 19–20 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/Bai10/index.html"
  },
  {
    "kind": "objectives",
    "title": "I. MỤC TIÊU BÀI HỌC (CV 5512 & NLS)",
    "sub": "Chuẩn SGK Kết nối tri thức & Khung Năng lực số 3.4.NC1.a",
    "cards": [
      {
        "heading": "1. Năng lực Tin học (1)–(3)",
        "color": "blue",
        "bullets": [
          "(1) Hiểu siêu văn bản, siêu liên kết, vai trò đường dẫn.",
          "(2) Tạo liên kết bằng thẻ <a>, href, id/# và <img>.",
          "(3) Chọn đúng URL tuyệt đối vs tương đối (Hình 10.1)."
        ]
      },
      {
        "heading": "2. Năng lực số 3.4.NC1.a",
        "color": "emerald",
        "bullets": [
          "Thiết kế & phát triển nội dung số đa trang HTML.",
          "Tổ chức website từ >= 2 tệp HTML liên kết logic.",
          "Quản lí tài nguyên chuẩn theo cấu trúc thư mục."
        ]
      },
      {
        "heading": "3. Năng lực chung (4)–(6)",
        "color": "amber",
        "bullets": [
          "(4) Tự học, tự thực hành & kiểm thử trên Sandbox.",
          "(5) Giao tiếp & hợp tác cặp đôi hiệu quả.",
          "(6) Giải quyết lỗi đường dẫn 404 / ổ đĩa máy cá nhân."
        ]
      },
      {
        "heading": "4. Phẩm chất (7)",
        "color": "purple",
        "bullets": [
          "(7) Chăm chỉ: thực hiện nghiêm túc các nhiệm vụ.",
          "Cẩn thận khi đặt tên tệp không dấu, viết đúng cú pháp.",
          "Trung thực trong tự đánh giá tiêu chí và nộp bài."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "TIẾN TRÌNH TỔ CHỨC 4 HOẠT ĐỘNG",
    "rows": [
      {
        "stage": "HĐ 1: Khởi động (5')",
        "color": "blue",
        "desc": "Câu hỏi mở đầu SGK tr.57: Trang web khác sách, báo giấy ở điểm nào? So sánh CLB.html."
      },
      {
        "stage": "HĐ 2.1: Khám phá 1 (15')",
        "color": "emerald",
        "desc": "Mục 1 SGK (tr.57–58): Siêu văn bản, thẻ <a>, đường dẫn tuyệt đối & đường dẫn tương đối."
      },
      {
        "stage": "HĐ 2.2: Khám phá 2 (20')",
        "color": "amber",
        "desc": "Mục 2 SGK (tr.58–60): Liên kết ngoài, cùng website (Hình 10.1), neo #id, ảnh & Phiếu BT."
      },
      {
        "stage": "HĐ 3: Luyện tập (35')",
        "color": "purple",
        "desc": "Mục 3 SGK (tr.61): Tạo >= 2 tệp HTML trên web (CLB.html, thong_tin.html...), bấm liên kết thật."
      },
      {
        "stage": "HĐ 4: Infographic (15')",
        "color": "red",
        "desc": "AntV Infographic Studio (4 chế độ), Flashcard 3D & giải đáp Luyện tập 1–2, Vận dụng tr.61."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG (TR.57)",
    "title": "TỪ SÁCH BÁO GIẤY ĐẾN SIÊU VĂN BẢN",
    "subtitle": "Điều gì tạo nên khả năng 'nhảy cóc' diệu kì giữa các trang web trên Internet?",
    "theme": "blue",
    "pills": [
      [
        "Đọc sách giấy",
        "Đọc tuần tự từ trang đầu tới trang cuối, tìm mục bằng tay.",
        "slate"
      ],
      [
        "Đọc trang web",
        "Nhấp vào chữ/ảnh liên kết để mở ngay trang mới hoặc đoạn mới.",
        "blue"
      ],
      [
        "Bí mật HTML",
        "Cặp thẻ <a> kết hợp thuộc tính href định địa chỉ trang đích.",
        "emerald"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "KHỞI ĐỘNG • SGK TR.57",
    "title": "SO SÁNH TRANG CLB TRƯỚC VÀ SAU KHI GẮN LIÊN KẾT",
    "left": {
      "heading": "Chưa tạo liên kết",
      "color": "amber",
      "bullets": [
        "Mọi tiêu đề CLB Thể thao, CLB Nghệ thuật chỉ là chữ tĩnh.",
        "Muốn xem trang thong_tin.html phải mở thủ công từng tệp.",
        "Không thể bấm để chuyển nhanh tới website Trường hay sách điện tử."
      ]
    },
    "right": {
      "heading": "Đã gắn siêu liên kết <a href>",
      "color": "emerald",
      "bullets": [
        "Các mục điều hướng tự đổi màu và gạch chân, có con trỏ hình bàn tay.",
        "Nhấp vào tên CLB tự động mở ngay trang thong_tin.html.",
        "Kết nối nhiều trang đơn lẻ thành một website hoàn chỉnh."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.1 • KHÁM PHÁ 1 (MỤC 1 SGK)",
    "title": "1. SIÊU VĂN BẢN VÀ ĐƯỜNG DẪN",
    "subtitle": "Khám phá bản chất Hypertext, cú pháp thẻ <a> và hai loại đường dẫn (tr.57–58)",
    "theme": "emerald",
    "pills": [
      [
        "Hoạt động 1",
        "Phân biệt tệp .docx có liên kết và tệp .txt thuần túy.",
        "blue"
      ],
      [
        "Thẻ <a href>",
        "<a href=\"URL\">Nội dung hiển thị</a>.",
        "emerald"
      ],
      [
        "Đường dẫn",
        "Đường dẫn tuyệt đối vs Đường dẫn tương đối.",
        "purple"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "KHÁM PHÁ 1 • HOẠT ĐỘNG 1 (TR.57)",
    "title": "THẢO LUẬN CẶP ĐÔI: TỆP .DOCX CÓ LIÊN KẾT VS TỆP .TXT",
    "question": "Khi đọc một văn bản định dạng .docx có chứa đường link và một tệp văn bản thuần túy .txt chứa cùng địa chỉ web đó, em thấy có điểm gì khác biệt?",
    "options": [
      "Tệp .txt chỉ lưu các kí tự chữ đơn thuần.",
      "Tệp .docx cho phép chèn hình ảnh, định dạng chữ và siêu liên kết.",
      "Trong Word (.docx), liên kết có màu xanh, gạch chân và nhấp mở được trình duyệt."
    ],
    "answer": [
      ".docx mang đặc điểm của siêu văn bản: chứa text + đa phương tiện + liên kết bấm được.",
      ".txt là văn bản thuần: URL chỉ là chữ chết, phải copy dán mới mở được.",
      "Web HTML chính là siêu văn bản tiêu chuẩn hóa trên trình duyệt!"
    ]
  },
  {
    "kind": "two_col",
    "badge": "KHÁM PHÁ 1 • KIẾN THỨC MỤC 1 (TR.57–58)",
    "title": "SIÊU VĂN BẢN, SIÊU LIÊN KẾT VÀ CÚ PHÁP THẺ <a>",
    "left": {
      "heading": "Khái niệm cốt lõi",
      "color": "blue",
      "bullets": [
        "Siêu văn bản (Hypertext): văn bản tích hợp text, ảnh, âm thanh, video và các liên kết tới phần tử khác.",
        "Siêu liên kết (Hyperlink): tham chiếu giúp người dùng di chuyển tới vị trí khác trong cùng trang hoặc sang trang web khác khi nhấp chuột.",
        "Thẻ tạo liên kết: <a> (Anchor) là thẻ đôi, có thuộc tính bắt buộc href."
      ]
    },
    "right": {
      "heading": "Cú pháp & Lưu ý thẻ <a>",
      "color": "emerald",
      "bullets": [
        "Cú pháp chuẩn: <a href=\"URL\">Nội dung siêu liên kết</a>",
        "Giá trị của href là địa chỉ URL đích (đặt trong ngoặc kép).",
        "Nội dung giữa <a> và </a> có thể là chữ hoặc hình ảnh <img>.",
        "Ví dụ: <a href=\"https://www.nxbgd.vn/\">Trang NXB Giáo dục</a>"
      ]
    }
  },
  {
    "kind": "two_col",
    "badge": "KHÁM PHÁ 1 • GHI NHỚ SGK TR.58",
    "title": "PHÂN BIỆT ĐƯỜNG DẪN TUYỆT ĐỐI VÀ ĐƯỜNG DẪN TƯƠNG ĐỐI",
    "left": {
      "heading": "Đường dẫn Tuyệt đối (Absolute URL)",
      "color": "amber",
      "bullets": [
        "Ghi đầy đủ giao thức (http:// hoặc https://) và tên miền + đường dẫn tài nguyên.",
        "Ví dụ: https://www.nxbgd.vn/ hoặc https://hanhtrangso.nxbgd.vn/",
        "Dùng khi liên kết tới trang web NGOÀI website hiện tại.",
        "Không nên dùng đường dẫn ổ đĩa máy cá nhân (D:\\bai_tap\\bt1.html) vì sẽ hỏng khi chuyển máy!"
      ]
    },
    "right": {
      "heading": "Đường dẫn Tương đối (Relative URL)",
      "color": "blue",
      "bullets": [
        "Không có giao thức hay tên miền; xác định tương đối so với thư mục chứa tệp HTML hiện tại.",
        "Ví dụ: thong_tin.html, BT/bai_tap_1.html, ../index.html",
        "Ưu tiên dùng khi liên kết giữa các tệp trong CÙNG website.",
        "Giúp website vẫn chạy bình thường khi copy toàn bộ thư mục sang máy khác hoặc tải lên host."
      ]
    }
  },
  {
    "kind": "quiz",
    "badge": "KHÁM PHÁ 1 • CÂU HỎI CUỐI MỤC 1 (TR.58)",
    "title": "PHÂN LOẠI CÁC ĐƯỜNG DẪN SAU ĐÂY",
    "question": "Các đường dẫn sau là đường dẫn tuyệt đối hay tương đối? Đường dẫn nào nên tránh dùng khi thiết kế website?",
    "options": [
      "a) http://hocmai.vn/khoahoc",
      "b) bai_tap/bai_tap_1.html",
      "c) D:\\TinHoc12\\index.html"
    ],
    "answer": [
      "a) Tuyệt đối (trên Internet) – dùng hợp lệ khi trỏ sang trang ngoài.",
      "b) Tương đối – trỏ vào thư mục con bai_tap, rất chuẩn cho liên kết nội bộ.",
      "c) Tuyệt đối trên ổ đĩa máy cá nhân – TRÁNH DÙNG vì hỏng link ở máy khác!"
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • KHÁM PHÁ 2 (MỤC 2 SGK)",
    "title": "2. CÁC CÁCH TẠO LIÊN KẾT TỚI MỘT TRANG WEB",
    "subtitle": "Hoạt động 2 & Mục 2a, 2b (SGK tr.58–60): Liên kết ngoài, cùng website, neo #id và hình ảnh",
    "theme": "purple",
    "pills": [
      [
        "2a) Trang web khác",
        "Dùng đường dẫn tuyệt đối http:// hoặc https://.",
        "blue"
      ],
      [
        "2b) Cùng website",
        "Dựa theo sơ đồ Hình 10.1: cùng cấp, thư mục con, ../.",
        "emerald"
      ],
      [
        "Neo #id & Ảnh <img>",
        "Chuyển vị trí cụ thể trên trang & lồng <img> trong <a>.",
        "amber"
      ]
    ]
  },
  {
    "kind": "code_result",
    "badge": "KHÁM PHÁ 2 • MỤC 2a (TR.59)",
    "title": "LIÊN KẾT TỚI MỘT TRANG WEB KHÁC TRÊN INTERNET",
    "filename": "index.html",
    "code": "<!DOCTYPE html>\n<html>\n<body>\n  <h2>Học liệu trực tuyến</h2>\n  <p>Truy cập bộ sách điện tử kết nối tri thức:</p>\n  <a href=\"https://hanhtrangso.nxbgd.vn/sach-dien-tu?book_active=0\">\n    Mở Hành trang số NXB Giáo dục\n  </a>\n</body>\n</html>",
    "notes": [
      "Hoạt động 2 (tr.58): Khi lướt web ta gặp 4 dạng liên kết chính: sang trang ngoài, sang trang cùng web, cuộn tại chỗ và bấm vào hình ảnh.",
      "Với trang web bên ngoài, bắt buộc dùng đường dẫn tuyệt đối có https:// hoặc http://.",
      "Nếu quên https://, trình duyệt sẽ tưởng là tên tệp tương đối trong máy và báo lỗi 404!"
    ]
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (HÌNH 10.1 TR.59)",
    "title": "LIÊN KẾT TRONG CÙNG WEBSITE: SƠ ĐỒ CÂY THƯ MỤC",
    "heading": "Xác định vị trí từ trang đang đứng",
    "bullets": [
      "Từ gốc (index.html) tới tệp cùng thư mục: chỉ cần ghi tên tệp, vd: href=\"thong_tin.html\".",
      "Từ gốc đi XUỐNG thư mục con: ghi tên thư mục + / + tên tệp.",
      "Ví dụ: href=\"bai_tap/bai_tap_1.html\" hoặc href=\"bai_tap/on_tap/bai_tap_on_tap.html\".",
      "Lưu ý phân cách thư mục trên web luôn dùng dấu gạch chéo xuôi / (không dùng \\)."
    ],
    "image": "sgk_hinh10_1.png",
    "caption": "Hình 10.1a: Sơ đồ thư mục website (SGK Tin học 12, tr.59)"
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.59)",
    "title": "ĐI NGƯỢC LÊN THƯ MỤC CHA BẰNG KÍ HIỆU ../",
    "heading": "Khi tệp nguồn nằm trong thư mục con",
    "bullets": [
      "Giả sử đang đứng ở tệp bai_tap/bai_tap_1.html (nằm sâu 1 cấp).",
      "Muốn liên kết quay về index.html ở thư mục cha: viết href=\"../index.html\".",
      "Kí hiệu ../ có nghĩa là đi lùi lên 1 cấp thư mục cha.",
      "Từ bai_tap/on_tap/bai_tap_on_tap.html (sâu 2 cấp) về gốc: viết ../../index.html."
    ],
    "image": "sgk_hinh10_1_sub.png",
    "caption": "Hình 10.1b: Liên kết ngược lên thư mục cha bằng ../"
  },
  {
    "kind": "code_result",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.59–60)",
    "title": "LIÊN KẾT TỚI MỘT VỊ TRÍ CỤ THỂ TRÊN TRANG (ID & #)",
    "filename": "thong_tin.html",
    "code": "<!-- Đánh dấu vị trí đích bằng id -->\n<h2 id=\"Thong_tin\">Thông tin chi tiết CLB</h2>\n<p>Lịch sinh hoạt: Chiều thứ Sáu hằng tuần...</p>\n\n<!-- Liên kết ngay trong cùng trang -->\n<a href=\"#Thong_tin\">Đi tới mục Thông tin</a>\n\n<!-- Hoặc từ index.html trỏ sang đúng đoạn này -->\n<a href=\"thong_tin.html#Thong_tin\">Xem mục Thông tin</a>",
    "notes": [
      "Bước 1: Đặt thuộc tính id=\"Ten_vi_tri\" ở thẻ HTML nơi muốn nhảy tới (không dấu cách, phân biệt hoa/thường).",
      "Bước 2: Dùng href=\"#Ten_vi_tri\" nếu nhảy trong cùng một trang web.",
      "Bước 3: Ghép ten_tep.html#Ten_vi_tri nếu nhảy từ trang khác tới đúng mục đó!"
    ]
  },
  {
    "kind": "code_result",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.60)",
    "title": "SỬ DỤNG HÌNH ẢNH LÀM SIÊU LIÊN KẾT",
    "filename": "index.html",
    "code": "<p>Nhấp vào biểu tượng để xem thông tin:</p>\n<a href=\"thong_tin.html\">\n  <img src=\"images/sun.png\" alt=\"Xem thông tin\">\n</a>\n\n<!-- Có thể kết hợp neo id trên liên kết ảnh -->\n<a href=\"CLB.html#CLBTT\">\n  <img src=\"images/the_thao.png\" alt=\"CLB Thể thao\">\n</a>",
    "notes": [
      "Nguyên tắc cực kì đơn giản: Đặt thẻ <img> vào giữa thẻ mở <a> và thẻ đóng </a> thay cho phần chữ.",
      "Khi di chuột vào hình ảnh, con trỏ đổi thành hình bàn tay và bấm vào sẽ chuyển trang.",
      "Nhớ luôn thêm thuộc tính alt để trình duyệt mô tả ảnh nếu ảnh chưa kịp tải."
    ]
  },
  {
    "kind": "quiz",
    "badge": "KHÁM PHÁ 2 • CÂU HỎI CUỐI MỤC 2 (TR.60)",
    "title": "VIẾT MÃ DANH SÁCH <ul> LIÊN KẾT THEO HÌNH 10.1",
    "question": "Hãy viết đoạn mã HTML đặt trong tệp index.html để tạo danh sách không có thứ tự gồm 2 mục liên kết tới trang bai_tap_1.html (trong thư mục bai_tap/) và bai_tap_on_tap.html (trong bai_tap/on_tap/).",
    "options": [
      "Tệp nguồn: index.html nằm ở thư mục gốc.",
      "Đích 1: bai_tap_1.html nằm trong bai_tap/.",
      "Đích 2: bai_tap_on_tap.html nằm trong bai_tap/on_tap/."
    ],
    "answer": [
      "<ul>",
      "  <li><a href=\"bai_tap/bai_tap_1.html\">Bài tập 1</a></li>",
      "  <li><a href=\"bai_tap/on_tap/bai_tap_on_tap.html\">Bài tập ôn tập</a></li>",
      "</ul>"
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • LUYỆN TẬP (MỤC 3 SGK TR.61)",
    "title": "THỰC HÀNH TẠO WEBSITE NHIỀU TỆP HTML",
    "subtitle": "Tạo ít nhất 2 tệp HTML trên Phòng Luyện tập (CLB.html, thong_tin.html & tệp tự tạo thêm)",
    "theme": "emerald",
    "pills": [
      [
        "Bước 1: Tạo >= 2 tệp",
        "Soạn cả CLB.html và thong_tin.html (hoặc thêm tệp mới).",
        "blue"
      ],
      [
        "Bước 2: Gắn liên kết",
        "Nối CLB.html <-> thong_tin.html#CLBTT và URL https://.",
        "emerald"
      ],
      [
        "Bước 3: Chấm 8 tiêu chí",
        "Bấm link trên Trình duyệt ảo bên phải kiểm tra rồi nộp!",
        "purple"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HOẠT ĐỘNG 3 • NHIỆM VỤ SGK TR.61",
    "title": "XÂY DỰNG BỘ TRANG CLB.HTML & THONG_TIN.HTML",
    "heading": "Tại sao cần từ 2 tệp HTML trở lên?",
    "bullets": [
      "Nếu chỉ có 1 tệp CLB.html đơn lẻ thì liên kết nội bộ <a href=\"thong_tin.html\"> sẽ báo lỗi 404!",
      "Trên hd3.html đã có sẵn 2 tab CLB.html & thong_tin.html và nút '+ Tạo thêm tệp .html'.",
      "HS có thể tạo thêm tệp cùng cấp (lich_su_CLB.html) hoặc thư mục con (bai_tap/bt1.html).",
      "Khi bấm link trong Trình duyệt ảo, web sẽ chuyển trang thật như trình duyệt máy tính!"
    ],
    "image": "sgk_hinh10_2.png",
    "caption": "Hình 10.2: Trang CLB.html liên kết sang thong_tin.html (SGK tr.61)"
  },
  {
    "kind": "code_result",
    "badge": "HOẠT ĐỘNG 3 • CODE MẪU ĐỐI CHIẾU",
    "title": "MẪU LIÊN KẾT HAI CHIỀU CLB.HTML <-> THONG_TIN.HTML",
    "filename": "CLB.html  <-->  thong_tin.html",
    "code": "<!-- Trong tệp CLB.html -->\n<ul>\n  <li><a href=\"thong_tin.html#CLBTT\">Xem CLB Thể thao</a></li>\n  <li><a href=\"thong_tin.html\">Xem trang Thông tin chung</a></li>\n  <li><a href=\"https://hanhtrangso.nxbgd.vn/\">Hành trang số</a></li>\n</ul>\n\n<!-- Trong tệp thong_tin.html -->\n<h2 id=\"CLBTT\">Câu lạc bộ Thể thao</h2>\n<p>Bóng đá, Bóng rổ, Cầu lông...</p>\n<a href=\"CLB.html\">← Quay về trang CLB.html</a>",
    "notes": [
      "Tránh đặt id có dấu tiếng Việt hoặc khoảng trắng (nên dùng id=\"CLBTT\" hoặc id=\"lich_su\").",
      "Đặt tên tệp không dấu, khớp chữ hoa/thường: CLB.html khác clb.html trên máy chủ Linux!",
      "Trong bài học hôm nay, học sinh hoàn toàn tập trung vào href, id/# và cấu trúc đa tệp chuẩn SGK."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 4 • INFOGRAPHIC & VẬN DỤNG (TR.61)",
    "title": "TỔNG KẾT ANTV INFOGRAPHIC & GIẢI BÀI TẬP SGK",
    "subtitle": "Hệ thống hóa 4 trụ cột kiến thức và luyện tập thiết kế hệ thống hồ sơ CLB nhiều tệp",
    "theme": "purple",
    "pills": [
      [
        "AntV Studio",
        "4 chế độ: Lộ trình, 4 Trụ cột, So sánh, Mindmap.",
        "purple"
      ],
      [
        "Flashcards 3D",
        "4 thẻ lật tự kiểm tra lỗi dễ mắc về đường dẫn.",
        "blue"
      ],
      [
        "SGK tr.61",
        "Luyện tập 1, Luyện tập 2 & Vận dụng (Hồ sơ CLB).",
        "emerald"
      ]
    ]
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • TỔNG KẾT NHANH",
    "title": "3 ĐIỀU CẦN NHỚ NHẤT CỦA BÀI 10: TẠO LIÊN KẾT",
    "cols": [
      {
        "heading": "1. Cú pháp <a href>",
        "color": "blue",
        "subhead": "Thẻ đôi tạo liên kết",
        "bullets": [
          "<a href=\"URL\">Chữ/Ảnh</a>",
          "Tuyệt đối: có https:// cho web ngoài.",
          "Tương đối: dùng cho các tệp trong cùng web."
        ]
      },
      {
        "heading": "2. Điều hướng Thư mục",
        "color": "emerald",
        "subhead": "Quy tắc Hình 10.1",
        "bullets": [
          "Cùng cấp: ten_tep.html",
          "Thư mục con: thu_muc/tep.html",
          "Thư mục cha: ../tep.html"
        ]
      },
      {
        "heading": "3. Neo & Hình ảnh",
        "color": "amber",
        "subhead": "Liên kết nâng cao",
        "bullets": [
          "Cùng trang: id=\"ten\" + #ten.",
          "Khác trang + vị trí: tep.html#ten.",
          "Ảnh link: bọc <img> trong <a>."
        ]
      }
    ]
  },
  {
    "kind": "quiz",
    "badge": "HOẠT ĐỘNG 4 • VẬN DỤNG SGK TR.61",
    "title": "BÀI TẬP VẬN DỤNG: HỒ SƠ CÁ NHÂN THÀNH VIÊN CLB",
    "question": "Hãy thiết kế website giới thiệu hồ sơ cá nhân của các thành viên trong câu lạc bộ (mỗi bạn là một tệp HTML riêng), sau đó tạo liên kết từ trang danh sách thành viên tới từng trang hồ sơ.",
    "options": [
      "Trang danh sách: thanh_vien.html (hoặc CLB.html).",
      "Thư mục hồ sơ con: ho_so/Nguyen_Van_An.html, ho_so/Tran_Binh.html.",
      "Yêu cầu: Bấm tên bạn nào mở đúng tệp hồ sơ của bạn đó và có nút quay về."
    ],
    "answer": [
      "Trong thanh_vien.html: <a href=\"ho_so/Nguyen_Van_An.html\">Nguyễn Văn An</a>.",
      "Trong ho_so/Nguyen_Van_An.html: <a href=\"../thanh_vien.html\">← Về danh sách</a>.",
      "HS thực hành tạo ngay nhiều tệp trên Phòng Luyện tập hd3.html!"
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 10: TẠO LIÊN KẾT (TIN HỌC 12)",
    "takeaways": [
      "Thẻ <a> dùng thuộc tính href để nối siêu văn bản tới URL ngoài (tuyệt đối) hoặc tệp nội bộ (tương đối).",
      "Muốn liên kết hoạt động thật giữa các trang thì dự án phải có từ 2 tệp HTML trở lên và đặt tên chuẩn không dấu.",
      "Thực hành thành thạo mô hình đa tệp trên hd3.html và ôn tập kĩ Luyện tập 1, 2, Vận dụng tr.61 trên hd4.html."
    ]
  }
]
LESSON_SHORT = "Bài 10: Tạo liên kết"
OUT_PPTX_NAME = "Bai10_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
