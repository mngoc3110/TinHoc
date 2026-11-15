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
    "subtitle": "Thẻ <a>, Đường dẫn tuyệt đối & tương đối (../), Liên kết neo #id, Liên kết ảnh & Kiểm tra KTTX2 (15p)",
    "meta": "Tuần 11 (Tiết 21–22)",
    "url": "https://minda.io.vn/Tin12/Bai10/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI HỌC & NĂNG LỰC SỐ",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.4.NC1.a",
    "cards": [
      {
        "heading": "1. Cú pháp thẻ liên kết <a>",
        "color": "blue",
        "bullets": [
          "Hiểu bản chất siêu liên kết (Hyperlink).",
          "Viết đúng <a href=\"URL\">Văn bản</a>.",
          "Dùng thuộc tính target=\"_blank\" mở tab mới."
        ]
      },
      {
        "heading": "2. Đường dẫn tuyệt đối & tương đối",
        "color": "emerald",
        "bullets": [
          "Phân biệt URL tuyệt đối (https://...) & tương đối.",
          "Điều hướng đúng thư mục con và cha (../).",
          "Tổ chức liên kết đa trang an toàn, không lỗi."
        ]
      },
      {
        "heading": "3. Liên kết neo (#id) & Hình ảnh",
        "color": "amber",
        "bullets": [
          "Gán định danh id để cuộn tới vị trí cùng trang.",
          "Trỏ tới vị trí thuộc trang khác (page.html#id).",
          "Lồng thẻ <img> vào bên trong thẻ <a>."
        ]
      },
      {
        "heading": "4. Thực hành & Đánh giá KTTX2",
        "color": "purple",
        "bullets": [
          "Nâng cấp dự án CLB.html kết nối thong_tin.html.",
          "Năng lực số: 3.4.NC1.a tổ chức dữ liệu đa trang.",
          "Hoàn thành KTTX2 (15 phút) phủ Bài 7–10."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "TIẾN TRÌNH TỔ CHỨC BÀI HỌC (2 TIẾT)",
    "rows": [
      {
        "stage": "1. Khởi động (5')",
        "color": "blue",
        "desc": "Quan sát CLB.html dạng tĩnh vs trang web đa liên kết; xác định nhu cầu điều hướng nhanh."
      },
      {
        "stage": "2.1. Thẻ <a> & URL (15')",
        "color": "emerald",
        "desc": "Học cú pháp <a href>, thuộc tính target và 4 quy tắc đường dẫn tương đối (SGK tr.57–59)."
      },
      {
        "stage": "2.2. Neo #id & Ảnh (15')",
        "color": "amber",
        "desc": "Thiết lập id + #id, ảnh liên kết và quét QR hoàn thành Phiếu bài tập thống nhất."
      },
      {
        "stage": "3. Thực hành CLB (30')",
        "color": "purple",
        "desc": "Tự gõ mã CLB.html có mục lục #CLBTT, liên kết thong_tin.html và ảnh; nộp lên máy chủ GV."
      },
      {
        "stage": "4. Tổng kết & KTTX2 (25')",
        "color": "red",
        "desc": "Infographic, giải câu hỏi SGK tr.61 và làm bài KTTX2 (15 phút) chuẩn TN THPT 2025."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "ĐIỀU HƯỚNG TRONG WEBSITE",
    "subtitle": "Từ một trang HTML đơn lẻ đến mạng lưới siêu văn bản kết nối",
    "theme": "blue",
    "pills": [
      [
        "Vấn đề trang đơn",
        "Trang CLB.html dài khiến người xem phải cuộn tay thủ công.",
        "amber"
      ],
      [
        "Nhu cầu kết nối",
        "Cần mở sang thong_tin.html hoặc nhảy ngay tới CLB Thể thao.",
        "blue"
      ],
      [
        "Giải pháp HTML5",
        "Sử dụng thẻ <a> kết hợp đường dẫn URL & định danh id.",
        "emerald"
      ]
    ]
  },
  {
    "kind": "code_result",
    "badge": "KHỞI ĐỘNG • SO SÁNH",
    "title": "TRƯỚC VÀ SAU KHI GẮN THẺ LIÊN KẾT",
    "sub": "Trực quan sự thay đổi từ văn bản tĩnh sang siêu văn bản",
    "theme": "blue",
    "filename": "CLB_demo.html",
    "code": "<!-- Trước: văn bản tĩnh -->\n<p>Xem lịch tập CLB Thể thao</p>\n<p>Xem trang Thông tin chi tiết</p>\n\n<!-- Sau: gắn siêu liên kết <a> -->\n<a href=\"#CLBTT\">Nhảy tới CLB Thể thao</a> | \n<a href=\"thong_tin.html\">Mở Thông tin CLB</a> |\n<a href=\"https://moet.gov.vn\" target=\"_blank\">\n  Cổng Bộ GD&ĐT\n</a>",
    "right_heading": "💡 NHẬN XÉT QUAN TRỌNG:",
    "notes": [
      "Mặc định liên kết có màu xanh dương và gạch chân.",
      "Khi rê chuột vào, con trỏ chuyển thành bàn tay.",
      "Chạm/bấm chuột sẽ nhảy đúng đích được khai báo ở href."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.1 • KIẾN THỨC MỚI",
    "title": "THẺ <a> & ĐƯỜNG DẪN URL",
    "subtitle": "Cú pháp tạo liên kết và cách xác định đường dẫn tuyệt đối / tương đối",
    "theme": "emerald",
    "pills": [
      [
        "Thẻ <a>",
        "Hyperlink Anchor: có cặp thẻ mở <a> và đóng </a>.",
        "blue"
      ],
      [
        "Thuộc tính href",
        "Chỉ địa chỉ URL đích khi người dùng nhấp chuột.",
        "emerald"
      ],
      [
        "Thuộc tính target",
        "target=\"_blank\" giúp mở liên kết ở một thẻ trình duyệt mới.",
        "purple"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • CÚ PHÁP CHUẨN",
    "title": "CẤU TRÚC THẺ <a> VÀ THUỘC TÍNH CHÍNH",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 57",
    "theme": "blue",
    "left": {
      "heading": "📌 Cú pháp tổng quát",
      "color": "blue",
      "bullets": [
        "<a href=\"URL\">Nội dung hiển thị</a>",
        "href (Hypertext Reference): bắt buộc chứa địa chỉ đích.",
        "Nội dung hiển thị có thể là chữ, cụm từ hoặc thẻ <img>.",
        "Nếu thiếu href, thẻ <a> không hoạt động như liên kết."
      ]
    },
    "right": {
      "heading": "⚙️ Thuộc tính target điều khiển cửa sổ",
      "color": "emerald",
      "bullets": [
        "target=\"_self\" (mặc định): mở ngay tại thẻ hiện tại.",
        "target=\"_blank\": mở sang một thẻ (tab) trình duyệt mới.",
        "Nên dùng _blank khi trỏ sang website bên ngoài.",
        "Thư mục & tên tệp phải gõ chính xác hoa/thường khi up host Linux."
      ]
    }
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • PHÂN LOẠI URL",
    "title": "ĐƯỜNG DẪN TUYỆT ĐỐI VS TƯƠNG ĐỐI",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 58",
    "theme": "emerald",
    "left": {
      "heading": "🌐 Đường dẫn Tuyệt đối (Absolute URL)",
      "color": "blue",
      "bullets": [
        "Chứa đầy đủ giao thức (https://, http://) và tên miền.",
        "Ví dụ: https://nxbgd.vn hoặc https://minda.io.vn.",
        "Bắt buộc dùng khi liên kết tới trang thuộc website khác.",
        "Không nên dùng đường dẫn ổ đĩa máy cá nhân (C:\\...)."
      ]
    },
    "right": {
      "heading": "📁 Đường dẫn Tương đối (Relative URL)",
      "color": "emerald",
      "bullets": [
        "Chỉ định đường dẫn tính từ vị trí tệp HTML đang đứng.",
        "Ví dụ: href=\"thong_tin.html\" hoặc href=\"img/logo.png\".",
        "Dùng cho các tài nguyên nội bộ trong cùng một website.",
        "Ưu điểm: ngắn gọn, di chuyển cả thư mục website vẫn chạy tốt."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • SƠ ĐỒ SGK",
    "title": "4 QUY TẮC VIẾT ĐƯỜNG DẪN TƯƠNG ĐỐI",
    "sub": "Quan sát cây thư mục website minh họa Hình 10.1 (Trang 58)",
    "theme": "blue",
    "heading": "🗺️ Từ trang hiện tại đi đến đích:",
    "bullets": [
      "Cùng thư mục: viết trực tiếp tên tệp (vd: thong_tin.html).",
      "Dưới 1 cấp (thư mục con): thumuc/tep.html.",
      "Dưới nhiều cấp: thumuc1/thumuc2/tep.html.",
      "Trên 1 cấp (thư mục cha): ../tep.html.",
      "Trên n cấp rồi xuống lại: ../../thumuc/tep.html."
    ],
    "image": "sgk_hinh10_1_sub.png",
    "caption": "Cấu trúc thư mục website chuẩn trong SGK Tin học 12 (trang 58)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • HÌNH MINH HỌA",
    "title": "VÍ DỤ LIÊN KẾT ĐA TRANG TRONG SGK",
    "sub": "SGK Tin học 12 – Trang 58",
    "theme": "emerald",
    "heading": "🔍 Giải mã Hộp xanh (SGK tr.58):",
    "bullets": [
      "Từ bai_tap/trang1.html trỏ ra index.html: dùng ../index.html.",
      "Nếu đổi thư mục chứa cả bộ web sang ổ D hoặc up lên host:",
      "-> Đường dẫn tương đối vẫn hoạt động chính xác 100%.",
      "-> Đường dẫn tuyệt đối kiểu file:///C:/... sẽ bị hỏng ngay!"
    ],
    "image": "sgk_hinh10_1.png",
    "caption": "Hình 10.1. Minh họa liên kết trang web (SGK Tin học 12 tr.58)"
  },
  {
    "kind": "quiz",
    "badge": "KIỂM TRA NHANH 2.1",
    "title": "CÂU HỎI TÌNH HUỐNG CẤU TRÚC THƯ MỤC",
    "sub": "Vận dụng quy tắc ../ trong bài thi TN THPT",
    "question": "Tệp baiviet/tintuc.html muốn liên kết tới tệp thuvien/tailieu.html (thư mục baiviet và thuvien cùng nằm trong thư mục gốc web). Thuộc tính href nào đúng?",
    "options": [
      "A. href=\"tailieu.html\"",
      "B. href=\"thuvien/tailieu.html\"",
      "C. href=\"../thuvien/tailieu.html\"",
      "D. href=\"../../tailieu.html\""
    ],
    "answer": [
      "Đáp án đúng: C (href=\"../thuvien/tailieu.html\").",
      "Giải thích: Từ thư mục con baiviet/ phải dùng ../ để lùi lên thư mục gốc web.",
      "Sau đó mới đi tiếp vào thư mục con thuvien/ để mở tailieu.html."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • KHÁM PHÁ CHUYÊN SÂU",
    "title": "LIÊN KẾT NEO (#ID) & HÌNH ẢNH",
    "subtitle": "Cuộn mượt đến vị trí bất kì và biến hình ảnh thành nút bấm điều hướng",
    "theme": "amber",
    "pills": [
      [
        "Bước 1: Gán id",
        "Đặt thuộc tính id=\"CLBTT\" cho thẻ tiêu đề đích.",
        "blue"
      ],
      [
        "Bước 2: Đặt #id",
        "Tạo <a href=\"#CLBTT\"> hoặc href=\"CLB.html#CLBTT\".",
        "emerald"
      ],
      [
        "Liên kết ảnh",
        "Đặt thẻ <img> vào giữa cặp thẻ mở-đóng <a>...</a>.",
        "amber"
      ]
    ]
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.2 • LIÊN KẾT CÙNG TRANG",
    "title": "KỸ THUẬT TẠO MỤC LỤC NHẢY TRONG TRANG",
    "sub": "SGK Tin học 12 – Trang 59–60",
    "theme": "amber",
    "filename": "CLB.html",
    "code": "<!-- Bước 2: Tạo mục lục ở đầu trang -->\n<nav>\n  <a href=\"#CLBTT\">Tới CLB Thể thao</a> |\n  <a href=\"#CLBNT\">Tới CLB Nghệ thuật</a>\n</nav>\n\n<!-- Bước 1: Gán định danh id ở phần tử đích -->\n<h2 id=\"CLBTT\">Câu lạc bộ Thể thao</h2>\n<p>Lịch tập bóng đá, cầu lông thứ 3, 5...</p>\n\n<h2 id=\"CLBNT\">Câu lạc bộ Nghệ thuật</h2>\n<p>Lịch sinh hoạt âm nhạc, hội họa thứ 7...</p>",
    "right_heading": "📌 LƯU Ý KỸ THUẬT:",
    "notes": [
      "Giá trị id là duy nhất trên một trang HTML (không trùng tên).",
      "Tên id không nên có dấu cách hoặc dấu tiếng Việt.",
      "Từ trang khác nhảy vào id này: href=\"CLB.html#CLBTT\"."
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • LIÊN KẾT TỪ TRANG KHÁC & ẢNH",
    "title": "LIÊN KẾT HÌNH ẢNH & GIẢI ĐÁP HỘP XANH",
    "sub": "SGK Tin học 12 – Trang 60",
    "theme": "purple",
    "heading": "🖼️ Biến hình ảnh thành liên kết:",
    "bullets": [
      "Cú pháp: <a href=\"thong_tin.html\"><img src=\"clb.jpg\" alt=\"CLB\"></a>",
      "Nếu ảnh là biểu tượng/banner, toàn bộ vùng ảnh đều bấm được.",
      "Hộp xanh tr.60: href=\"danh_sach.html#Muc2\" mở danh_sach.html và cuộn thẳng đến phần tử có id=\"Muc2\"."
    ],
    "image": "sgk_hinh10_2.png",
    "caption": "Hình 10.2. Liên kết tới một vị trí trong cùng trang web (SGK tr.60)"
  },
  {
    "kind": "section",
    "tag": "NHIỆM VỤ ĐÁNH GIÁ NHANH",
    "title": "PHIẾU BÀI TẬP BÀI 10",
    "subtitle": "Quét mã QR hoặc truy cập hd2-2.html -> phieu-bai-tap.html (6 câu chuẩn BGD&ĐT)",
    "theme": "blue",
    "pills": [
      [
        "4 Câu MCQ",
        "Kiến thức thẻ <a>, đường dẫn tuyệt đối/tương đối.",
        "blue"
      ],
      [
        "2 Câu Đúng/Sai",
        "Tình huống thiết kế cây thư mục website CLB.",
        "emerald"
      ],
      [
        "Chấm realtime",
        "Hệ thống tự động chấm & lưu bảng điểm giáo viên.",
        "purple"
      ]
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (30 PHÚT)",
    "title": "HOÀN THIỆN DỰ ÁN CLB.HTML",
    "subtitle": "Thực hành tự code độc lập trên hd3.html (SGK trang 60–61)",
    "theme": "purple",
    "pills": [
      [
        "Nhiệm vụ 1",
        "Gắn id=\"CLBTT\", id=\"CLBNT\" & tạo menu đầu trang.",
        "blue"
      ],
      [
        "Nhiệm vụ 2",
        "Gắn liên kết sang thong_tin.html & trang web ngoài.",
        "emerald"
      ],
      [
        "Nhiệm vụ 3",
        "Chèn ít nhất 1 hình ảnh lồng trong <a> & nộp bài.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 3 • HƯỚNG DẪN THỰC HÀNH",
    "title": "TIÊU CHÍ CHẤM BÀI THỰC HÀNH CLB.HTML",
    "sub": "8 tiêu chí kiểm tra tự động trước khi bấm Nộp bài",
    "theme": "purple",
    "left": {
      "heading": "📋 Tiêu chí 1 – 4 (Cấu trúc & Neo #id)",
      "color": "blue",
      "bullets": [
        "1. Khai báo chuẩn <!DOCTYPE html> và thẻ <head>/<title>.",
        "2. Giữ bảng hoặc danh sách lịch sinh hoạt CLB (Bài 9).",
        "3. Có ít nhất 2 phần tử mang thuộc tính id=\"CLBTT\", id=\"CLBNT\".",
        "4. Có menu/mục lục dùng href=\"#CLBTT\" nhảy trong trang."
      ]
    },
    "right": {
      "heading": "🔗 Tiêu chí 5 – 8 (Đa trang & Ảnh)",
      "color": "emerald",
      "bullets": [
        "5. Có liên kết tương đối sang trang href=\"thong_tin.html\".",
        "6. Có liên kết ngoài dùng đường dẫn tuyệt đối https://...",
        "7. Dùng target=\"_blank\" mở tab mới cho liên kết ngoài.",
        "8. Có liên kết bằng hình ảnh (<a ...><img ...></a>)."
      ]
    }
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC TỔNG HỢP",
    "title": "3 MẢNH GHÉP CỐT LÕI CỦA BÀI 10",
    "sub": "Ghi nhớ nhanh trước khi bước vào bài Kiểm tra KTTX2",
    "theme": "blue",
    "cols": [
      {
        "heading": "1. Cú pháp thẻ <a>",
        "color": "blue",
        "subhead": "Siêu liên kết cơ bản",
        "bullets": [
          "<a href=\"URL\">Nội dung</a>",
          "target=\"_blank\" mở tab mới.",
          "Chèn ảnh giữa <a>...</a> để tạo nút ảnh."
        ]
      },
      {
        "heading": "2. Quy tắc URL",
        "color": "emerald",
        "subhead": "Tuyệt đối vs Tương đối",
        "bullets": [
          "Tuyệt đối: https://... (liên kết ngoài).",
          "Cùng thư mục: thong_tin.html.",
          "Thư mục cha: ../index.html."
        ]
      },
      {
        "heading": "3. Liên kết neo #id",
        "color": "amber",
        "subhead": "Điều hướng tại chỗ",
        "bullets": [
          "Đặt id=\"CLBTT\" tại mục đích.",
          "Gọi href=\"#CLBTT\" trong cùng trang.",
          "Gọi CLB.html#CLBTT từ trang khác."
        ]
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • GIẢI ĐÁP SGK TRANG 61",
    "title": "ĐÁP ÁN LUYỆN TẬP & VẬN DỤNG",
    "sub": "Hệ thống câu hỏi cuối bài SGK Tin học 12 Kết nối tri thức",
    "theme": "emerald",
    "left": {
      "heading": "✏️ Luyện tập 1 & 2 (Trang 61)",
      "color": "blue",
      "bullets": [
        "LT1: Dùng URL tuyệt đối cho web ngoài; URL tương đối cho nội bộ để gọn và không lỗi khi đổi domain.",
        "LT2: Đường dẫn từ index.html -> thuvien/tailieu.html.",
        "LT2: Từ baiviet/tintuc.html về index.html -> ../index.html.",
        "LT2: Từ baiviet/tintuc.html sang thuvien/tailieu.html -> ../thuvien/tailieu.html."
      ]
    },
    "right": {
      "heading": "🚀 Vận dụng (Trang 61)",
      "color": "emerald",
      "bullets": [
        "Mở rộng trang index.html hoặc CLB.html hoàn chỉnh.",
        "Bổ sung thanh liên kết #gioi_thieu, #lich_hoc, #dang_ki.",
        "Kết nối chéo giữa index.html <-> thong_tin.html <-> CLB.html.",
        "Gắn logo trường học bấm về trang chủ trường."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "KIỂM TRA THƯỜNG XUYÊN 2 (15 PHÚT)",
    "title": "ĐÁNH GIÁ KIẾN THỨC BÀI 7 – BÀI 10",
    "subtitle": "Truy cập kttx2.html (hoặc quét QR) • 8 câu MCQ (6đ) + 2 câu Đúng/Sai (4đ)",
    "theme": "red",
    "pills": [
      [
        "Thời lượng 15 phút",
        "Đồng hồ đếm ngược tự động nộp khi hết giờ.",
        "red"
      ],
      [
        "Ma trận chuẩn BGD",
        "Bao quát cấu trúc HTML, định dạng, danh sách, bảng & liên kết.",
        "blue"
      ],
      [
        "Chấm & thống kê",
        "Điểm tự động cập nhật về bảng theo dõi GV.",
        "emerald"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP KTTX2 • ĐÚNG / SAI MẪU",
    "title": "TÌNH HUỐNG THIẾT KẾ CẤU TRÚC LIÊN KẾT",
    "sub": "Chuẩn đề tham khảo TN THPT 2025 môn Tin học",
    "question": "Một học sinh tạo thư mục DuAn/ chứa index.html và thư mục con trang/ chứa clb.html (có <h2 id='tt'>Thể thao</h2>). Khi viết mã trong index.html:",
    "options": [
      "a) Liên kết <a href='trang/clb.html'>CLB</a> mở đúng tệp.",
      "b) Để từ clb.html quay về index.html viết href='index.html'.",
      "c) Liên kết <a href='trang/clb.html#tt'> nhảy tới mục Thể thao.",
      "d) Dùng target='_blank' để mở trang ngoài trong thẻ mới."
    ],
    "answer": [
      "a) Đúng — clb.html nằm trong thư mục con trang/.",
      "b) Sai — clb.html ở thư mục con nên phải dùng ../index.html.",
      "c) Đúng — kết hợp đường dẫn tương đối và #id.",
      "d) Đúng — target='_blank' mở cửa sổ/thẻ mới."
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 10 & KIỂM TRA KTTX2!",
    "takeaways": [
      "Thuần thục thẻ <a href=\"URL\" target=\"_blank\"> và cách lồng <img> để tạo ảnh liên kết.",
      "Nắm vững nguyên tắc đường dẫn tương đối (thumuc/tep.html và ../tep.html) cho website đa trang.",
      "Hoàn thiện CLB.html (hd3.html) & kiểm tra lại kết quả bài KTTX2 (15 phút).",
      "Chuẩn bị cho Bài 11 (Tuần 12): Chèn tệp tin đa phương tiện & khung nội tuyến (<img>, <video>, <audio>, <iframe>)."
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
