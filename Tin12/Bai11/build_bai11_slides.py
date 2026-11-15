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
    "title": "BÀI 11: CHÈN TỆP TIN ĐA PHƯƠNG TIỆN VÀ KHUNG NỘI TUYẾN",
    "subtitle": "Làm chủ thẻ <img>, <audio>, <video>, <source> và <iframe> điều hướng thông minh",
    "meta": "Tiết 23–24 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/Bai11/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI HỌC & NĂNG LỰC SỐ",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.2.NC1a, 3.3.NC1a",
    "cards": [
      {
        "heading": "1. Chèn hình ảnh với <img>",
        "color": "blue",
        "bullets": [
          "Nắm thuộc tính src, alt, width, height.",
          "Hiểu quy tắc tự co giãn giữ đúng tỉ lệ gốc.",
          "Biết định dạng JPEG, PNG, GIF, WebP."
        ]
      },
      {
        "heading": "2. Âm thanh & Video HTML5",
        "color": "emerald",
        "bullets": [
          "Dùng <audio> và <video> kèm controls.",
          "Dùng <source> hỗ trợ nhiều định dạng.",
          "Phân biệt poster, autoplay, muted."
        ]
      },
      {
        "heading": "3. Khung nội tuyến <iframe>",
        "color": "amber",
        "bullets": [
          "Nhúng trang HTML/video qua <iframe src>.",
          "Gán name cho iframe & target cho thẻ <a>.",
          "Thiết kế bố cục đa trang mượt mà."
        ]
      },
      {
        "heading": "4. Năng lực số 3.2 & 3.3.NC1a",
        "color": "purple",
        "bullets": [
          "Biết chọn định dạng tối ưu hiệu năng web.",
          "Tôn trọng bản quyền ảnh, nhạc, video số.",
          "Tự code the_thao.html đạt 8/8 tiêu chí."
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
        "desc": "So sánh trang CLB chỉ có văn bản với trang đa phương tiện có ảnh, âm thanh, video."
      },
      {
        "stage": "2.1. Ảnh, Audio, Video (20')",
        "color": "emerald",
        "desc": "Tìm hiểu <img>, bài toán tỉ lệ kích thước, <audio>, <video> và thẻ dự phòng <source>."
      },
      {
        "stage": "2.2. Khung <iframe> (15')",
        "color": "amber",
        "desc": "Nhúng <iframe> kết hợp target và hoàn thành Phiếu bài tập thống nhất qua QR."
      },
      {
        "stage": "3. Thực hành CLB (35')",
        "color": "purple",
        "desc": "Tự gõ mã the_thao.html chèn ảnh, nhạc, video, iframe trên hd3.html và nộp bài."
      },
      {
        "stage": "4. Infographic & SGK (15')",
        "color": "red",
        "desc": "Tổng kết 4 chế độ Infographic, Flashcards 3D và chữa LT1, LT2, Vận dụng SGK tr.66."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "TỪ VĂN BẢN ĐẾN ĐA PHƯƠNG TIỆN",
    "subtitle": "Làm trang web CLB Trường học trở nên trực quan và thu hút",
    "theme": "blue",
    "pills": [
      [
        "Hình ảnh <img>",
        "Minh họa sân thi đấu, logo, ảnh hoạt động ngoại khóa.",
        "blue"
      ],
      [
        "Audio & Video",
        "Phát Quốc ca, bản tin hoặc clip highlight CLB.",
        "emerald"
      ],
      [
        "Khung <iframe>",
        "Nhúng bản đồ, clip YouTube hoặc trang con trong trang chính.",
        "purple"
      ]
    ]
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • HÌNH ẢNH",
    "title": "CHÈN HÌNH ẢNH VỚI THẺ <IMG>",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 62–63",
    "theme": "blue",
    "filename": "the_thao.html",
    "code": "<!-- Thẻ đơn <img> không có thẻ đóng -->\n<img src=\"bong_da.jpg\" \n     alt=\"Đội tuyển bóng đá THTH-DHSP\" \n     width=\"600\">\n\n<!-- Nếu đặt cả width và height không đúng tỉ lệ\n     thì hình ảnh dễ bị méo (kéo dãn) -->\n<img src=\"cau_long.png\" alt=\"Cầu lông\" \n     width=\"400\" height=\"250\">",
    "right_heading": "📌 GHI NHỚ QUAN TRỌNG:",
    "notes": [
      "<img> là thẻ trống (không có </img>).",
      "src (bắt buộc): đường dẫn ảnh (.jpg, .png, .webp, .gif).",
      "alt: chữ thay thế khi ảnh lỗi hoặc đọc màn hình.",
      "Chỉ đặt 1 chiều width -> height tự co đúng tỉ lệ gốc!"
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • ĐỊNH DẠNG ẢNH SGK",
    "title": "CÁC ĐỊNH DẠNG ẢNH & THUỘC TÍNH KÍCH THƯỚC",
    "sub": "SGK Tin học 12 – Trang 62–63 (Hình 11.1 & 11.2)",
    "theme": "blue",
    "heading": "🖼️ So sánh nhanh định dạng ảnh web:",
    "bullets": [
      "JPEG (.jpg): nhẹ, giữ nhiều màu, hợp ảnh chụp.",
      "PNG (.png): sắc nét, hỗ trợ nền trong suốt (logo).",
      "GIF (.gif): hỗ trợ ảnh động ngắn.",
      "WebP (.webp): nén tốt hơn JPEG/PNG, tối ưu tốc độ web."
    ],
    "image": "sgk_hinh11_1.png",
    "caption": "Hình 11.1. Định dạng tệp tin ảnh và cách dùng thẻ <img> (SGK tr.62)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • QUY TẮC TỈ LỆ",
    "title": "CO GIÃN KÍCH THƯỚC ẢNH KHÔNG BỊ MÉO",
    "sub": "Bài toán trọng tâm đề thi TN THPT & Luyện tập 1 tr.66",
    "theme": "emerald",
    "heading": "📐 Quy tắc giữ tỉ lệ khung hình:",
    "bullets": [
      "Đặt cả width & height khác tỉ lệ -> ảnh bị méo.",
      "Chỉ đặt width (hoặc chỉ height) -> chiều kia tự tính.",
      "Ví dụ (LT1 tr.66): Ảnh gốc 720 x 450 px.",
      "Đặt width=\"600\" (bỏ height) -> height = 600 × 450 / 720 = 375 px!"
    ],
    "image": "sgk_hinh11_2.png",
    "caption": "Hình 11.2. Hiển thị ảnh giữ nguyên tỉ lệ trên trình duyệt (SGK tr.63)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • ÂM THANH & VIDEO",
    "title": "SO SÁNH THẺ <AUDIO> VÀ THẺ <VIDEO>",
    "sub": "SGK Tin học 12 – Trang 63–64 (Tránh bẫy thuộc tính)",
    "theme": "emerald",
    "left": {
      "heading": "🔊 Thẻ <audio> (Âm thanh)",
      "color": "blue",
      "bullets": [
        "Định dạng phổ biến: MP3, WAV, OGG.",
        "Thuộc tính: src, controls, autoplay, muted, loop.",
        "QUAN TRỌNG: Bắt buộc có controls để hiện thanh phát.",
        "KHÔNG có thuộc tính width, height, poster!"
      ]
    },
    "right": {
      "heading": "🎬 Thẻ <video> (Hình ảnh động)",
      "color": "emerald",
      "bullets": [
        "Định dạng phổ biến: MP4, WebM, Ogg.",
        "Thuộc tính chung: src, controls, autoplay, muted.",
        "Thuộc tính RIÊNG: width, height và poster=\"anh_bia.jpg\".",
        "Trình duyệt thường chỉ cho autoplay nếu kèm muted."
      ]
    }
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • THẺ <SOURCE>",
    "title": "KỸ THUẬT CHÈN NHIỀU NGUỒN VỚI <SOURCE>",
    "sub": "SGK Tin học 12 – Trang 63–64 & Luyện tập 2 tr.66",
    "theme": "emerald",
    "filename": "media.html",
    "code": "<audio controls>\n  <source src=\"nhac.mp3\" type=\"audio/mpeg\">\n  <source src=\"nhac.ogg\" type=\"audio/ogg\">\n  Trình duyệt không hỗ trợ audio.\n</audio>\n\n<video width=\"480\" height=\"270\" controls poster=\"bia.jpg\">\n  <source src=\"video.mp4\" type=\"video/mp4\">\n  <source src=\"video.webm\" type=\"video/webm\">\n</video>",
    "right_heading": "💡 TẠI SAO DÙNG <SOURCE>?",
    "notes": [
      "Mỗi trình duyệt hỗ trợ bộ định dạng codec khác nhau.",
      "<source> đặt bên trong <audio> hoặc <video>.",
      "Trình duyệt thử từ trên xuống, phát nguồn đầu tiên đọc được.",
      "Nếu đều không hỗ trợ, hiển thị dòng văn bản dự phòng."
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • MINH HỌA SGK",
    "title": "CHÈN AUDIO VÀ VIDEO TRONG DỰ ÁN CLB",
    "sub": "SGK Tin học 12 – Trang 63–64",
    "theme": "amber",
    "heading": "🎵 Quan sát sản phẩm SGK (Hình 11.3 & 11.4):",
    "bullets": [
      "Thanh điều khiển controls gồm Play/Pause, thanh tua, âm lượng.",
      "Thuộc tính poster hiển thị ảnh chờ đẹp mắt trước khi bấm Play.",
      "Luôn khai báo width/height phù hợp tỉ lệ video (thường 16:9)."
    ],
    "image": "sgk_hinh11_4.png",
    "caption": "Hình 11.4. Kết quả chèn video vào trang web giới thiệu CLB (SGK tr.64)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • THỰC HÀNH AUDIO SGK",
    "title": "CHÈN ÂM THANH VÀO TRANG CLBVN (HÌNH 11.3)",
    "sub": "SGK Tin học 12 – Trang 63",
    "theme": "emerald",
    "heading": "🎶 Ví dụ chèn bài hát Quốc ca:",
    "bullets": [
      "<audio src=\"quoc_ca.mp3\" controls></audio>",
      "Đặt tệp .mp3 cùng thư mục trang HTML hoặc trong thư mục audio/.",
      "Không tự ý bật autoplay khi chưa được người dùng cho phép."
    ],
    "image": "sgk_hinh11_3.png",
    "caption": "Hình 11.3. Chèn hình ảnh và âm thanh vào trang web CLB (SGK tr.63)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • ĐA DẠNG ĐỊNH DẠNG & BẢN QUYỀN",
    "title": "TỐI ƯU TÀI NGUYÊN & TÔN TRỌNG BẢN QUYỀN SỐ",
    "sub": "Thực hành Năng lực số 3.2.NC1a & 3.3.NC1a",
    "theme": "blue",
    "left": {
      "heading": "⚡ Tối ưu dung lượng & hiệu năng",
      "color": "blue",
      "bullets": [
        "Ảnh chụp web: ưu tiên WebP hoặc JPEG thay vì BMP nặng.",
        "Video độ phân giải HD vừa phải (MP4 H.264/WebM).",
        "Cung cấp thuộc tính poster giúp khung hình không bị đen."
      ]
    },
    "right": {
      "heading": "©️ Bản quyền & An toàn nguồn nhúng",
      "color": "emerald",
      "bullets": [
        "Chỉ dùng ảnh, nhạc, video tự tạo hoặc giấy phép Creative Commons.",
        "Ghi rõ nguồn trích dẫn khi sử dụng tư liệu học tập.",
        "Chỉ nhúng <iframe> từ các trang web tin cậy (YouTube, Maps, trường học)."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • KHUNG NỘI TUYẾN",
    "title": "NHÚNG TRANG WEB BẰNG <IFRAME>",
    "subtitle": "Hiển thị trang HTML con hoặc tài nguyên ngoài trong khung chữ nhật",
    "theme": "amber",
    "pills": [
      [
        "Thẻ <iframe>",
        "Tạo vùng khung nhúng trực tiếp trang URL khác.",
        "blue"
      ],
      [
        "Thuộc tính name",
        "Đặt tên định danh cho khung (vd: name=\"khung\").",
        "emerald"
      ],
      [
        "Kết hợp target",
        "<a href=\"...\" target=\"khung\"> mở ngay vào khung.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • THẺ <IFRAME> SGK",
    "title": "CÚ PHÁP <IFRAME> & ĐIỀU HƯỚNG TARGET",
    "sub": "SGK Tin học 12 – Trang 64–65 (Hình 11.5)",
    "theme": "purple",
    "heading": "🪟 Điều khiển khung nội tuyến:",
    "bullets": [
      "<iframe src=\"gioi_thieu.html\" width=\"100%\" height=\"380\" name=\"khung\"></iframe>",
      "Tạo liên kết: <a href=\"the_thao.html\" target=\"khung\">Thể thao</a>.",
      "Khi bấm liên kết, chỉ nội dung trong iframe đổi, trang ngoài giữ nguyên!",
      "Ứng dụng nhúng YouTube Embed hoặc Google Maps dễ dàng."
    ],
    "image": "sgk_hinh11_5.png",
    "caption": "Hình 11.5. Kết hợp liên kết thẻ <a> mở trang con bên trong <iframe> (SGK tr.65)"
  },
  {
    "kind": "section",
    "tag": "NHIỆM VỤ ĐÁNH GIÁ NHANH",
    "title": "PHIẾU BÀI TẬP BÀI 11",
    "subtitle": "Quét mã QR hoặc truy cập hd2-2.html -> phieu-bai-tap.html (6 câu chuẩn BGD&ĐT)",
    "theme": "blue",
    "pills": [
      [
        "4 Câu MCQ",
        "Tính tỉ lệ ảnh <img>, thuộc tính <audio>/<video> và <iframe>.",
        "blue"
      ],
      [
        "2 Câu Đúng/Sai",
        "Đọc hiểu đoạn mã nhúng ảnh, source và iframe target.",
        "emerald"
      ],
      [
        "Chấm realtime",
        "Điểm tự động cập nhật về bảng theo dõi Giáo viên.",
        "purple"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "KIỂM TRA NHANH 2.2",
    "title": "CÂU HỎI TÌNH HUỐNG TỈ LỆ ẢNH & IFRAME",
    "sub": "Trích dạng đề thi TN THPT 2025",
    "question": "Một bức ảnh có kích thước gốc 1200 x 800 pixel được chèn bằng thẻ <img src=\"clb.jpg\" height=\"400\"> (không ghi thuộc tính width). Chiều rộng hiển thị là bao nhiêu?",
    "options": [
      "A. 400 px",
      "B. 600 px",
      "C. 800 px",
      "D. 1200 px"
    ],
    "answer": [
      "Đáp án đúng: B (600 px).",
      "Giải thích: Trình duyệt giữ nguyên tỉ lệ gốc 1200 / 800 = 1.5.",
      "Vì height mới là 400 nên width mới = 400 × 1.5 = 600 px."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (35 PHÚT)",
    "title": "XÂY DỰNG THE_THAO.HTML ĐA PHƯƠNG TIỆN",
    "subtitle": "Tự gõ mã trên phòng thực hành trống hd3.html (SGK trang 65–66)",
    "theme": "purple",
    "pills": [
      [
        "Chèn Hình ảnh",
        "Thẻ <img> đủ src, alt mô tả và width hợp lý.",
        "blue"
      ],
      [
        "Audio & Video",
        "Có <audio controls> và <video controls poster> kèm <source>.",
        "emerald"
      ],
      [
        "Khung <iframe>",
        "Khai báo <iframe name=\"...\"> + liên kết <a target=\"...\">.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 3 • TIÊU CHÍ ĐÁNH GIÁ",
    "title": "8 TIÊU CHÍ TỰ ĐỘNG CHO THE_THAO.HTML",
    "sub": "Hoàn thiện đầy đủ các tiêu chí trước khi bấm Nộp bài",
    "theme": "purple",
    "left": {
      "heading": "🖼️ Tiêu chí 1 – 4 (Ảnh & Âm thanh)",
      "color": "blue",
      "bullets": [
        "1. Khai báo chuẩn <!DOCTYPE html>, <html>, <body>.",
        "2. Có thẻ <img src=\"...\"> chèn hình hoạt động CLB.",
        "3. Có thuộc tính alt=\"...\" và width (không méo ảnh).",
        "4. Có thẻ <audio> sử dụng thuộc tính controls."
      ]
    },
    "right": {
      "heading": "🎥 Tiêu chí 5 – 8 (Video & Iframe)",
      "color": "emerald",
      "bullets": [
        "5. Có thẻ <video> kèm controls và width/height.",
        "6. Có thẻ <source src=\"...\" type=\"...\">.",
        "7. Có khung nội tuyến <iframe ... name=\"...\">.",
        "8. Có thẻ <a href=\"...\" target=\"...\"> trỏ vào iframe."
      ]
    }
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC",
    "title": "TỔNG HỢP BỘ THẺ ĐA PHƯƠNG TIỆN BÀI 11",
    "sub": "Hệ thống hóa ngắn gọn cú pháp & thuộc tính dễ nhầm lẫn",
    "theme": "blue",
    "cols": [
      {
        "heading": "Hình ảnh <img>",
        "color": "blue",
        "subhead": "Thẻ đơn (Self-closing)",
        "bullets": [
          "Bắt buộc có src=\"...\".",
          "Nên luôn có alt=\"...\".",
          "Đặt 1 chiều width để tự giữ tỉ lệ."
        ]
      },
      {
        "heading": "<audio> & <video>",
        "color": "emerald",
        "subhead": "Thẻ ghép có </audio>, </video>",
        "bullets": [
          "Phải có controls để hiện nút bấm.",
          "Chỉ <video> có width, height, poster.",
          "Lồng <source> khai báo nhiều nguồn."
        ]
      },
      {
        "heading": "Khung <iframe>",
        "color": "amber",
        "subhead": "Nhúng nội dung trong trang",
        "bullets": [
          "<iframe src=\"...\" name=\"khung\">",
          "Kết hợp <a target=\"khung\">.",
          "Thuận tiện nhúng bản đồ, video clip."
        ]
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • GIẢI BÀI TẬP SGK TRANG 66",
    "title": "ĐÁP ÁN LUYỆN TẬP & VẬN DỤNG",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 66",
    "theme": "emerald",
    "left": {
      "heading": "✏️ Luyện tập 1 & 2 (Trang 66)",
      "color": "blue",
      "bullets": [
        "LT1: Ảnh gốc 720×450 đặt width=\"600\" -> height = 600 × 450 / 720 = 375 px.",
        "Kích thước ảnh hiển thị: 600 × 375 pixel.",
        "LT2: Thẻ <source> khai báo nhiều định dạng dự phòng giúp mọi trình duyệt đều phát được tệp media đầu tiên nó hỗ trợ."
      ]
    },
    "right": {
      "heading": "🚀 Vận dụng (Trang 66)",
      "color": "emerald",
      "bullets": [
        "Nâng cấp trang giới thiệu CLB ở Bài 10.",
        "Đặt <iframe name=\"vung_xem\"> hiển thị các trang con.",
        "Nhúng clip YouTube hoặc video hoạt động CLB qua src của iframe hoặc thẻ <video poster=\"...\">."
      ]
    }
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP CHUẨN TN THPT",
    "title": "BẪY ĐỀ THI: THUỘC TÍNH CỦA <AUDIO> VÀ <VIDEO>",
    "sub": "Phân tích nhận định Đúng / Sai thường gặp",
    "question": "Khi chèn tệp âm thanh và video vào trang web bằng HTML5, hãy xác định tính Đúng/Sai của 4 phát biểu sau:",
    "options": [
      "a) Thẻ <img> không cần thẻ đóng </img> và bắt buộc có thuộc tính src.",
      "b) Thẻ <audio controls poster=\"bia.jpg\"> hiển thị ảnh bìa cho bản nhạc.",
      "c) Nếu thiếu controls, trình duyệt có thể không hiển thị thanh phát nhạc/video.",
      "d) Dùng <a href=\"clip.html\" target=\"khung\"> sẽ mở trang vào <iframe name=\"khung\">."
    ],
    "answer": [
      "a) Đúng — <img> là thẻ rỗng.",
      "b) Sai — poster chỉ dùng cho <video>, không dùng cho <audio>.",
      "c) Đúng — controls tạo nút Play/Pause, âm lượng.",
      "d) Đúng — target trùng khớp name của iframe."
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 11: ĐA PHƯƠNG TIỆN & IFRAME!",
    "takeaways": [
      "<img> là thẻ trống: đặt 1 kích thước width/height để ảnh tự co giãn đúng tỉ lệ.",
      "<audio> và <video> cần controls để điều khiển; chỉ <video> có width, height, poster.",
      "<iframe name=\"...\"> kết hợp <a target=\"...\"> giúp mở trang con ngay trong khung.",
      "Chuẩn bị cho Bài 12: Tạo biểu mẫu (<form>, <input>, <select>, <textarea>, <fieldset>)."
    ]
  }
]
LESSON_SHORT = "Bài 11: Chèn tệp tin đa phương tiện và khung nội tuyến vào trang web"
OUT_PPTX_NAME = "Bai11_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
