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
    "title": "BÀI 12: TẠO BIỂU MẪU (HTML FORM)",
    "subtitle": "Thu thập dữ liệu tương tác với <form>, <label>, <input>, <select>, <textarea> và <fieldset>",
    "meta": "Tiết 25–26 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/Bai12/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI HỌC & NĂNG LỰC SỐ",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.4.NC1.a",
    "cards": [
      {
        "heading": "1. Khung biểu mẫu <form>",
        "color": "blue",
        "bullets": [
          "Hiểu vai trò giao tiếp hai chiều với máy chủ.",
          "Viết đúng <form action=\"...\"> bao bọc phần tử.",
          "Gắn nhãn <label for=\"...\"> khớp với id ô nhập."
        ]
      },
      {
        "heading": "2. Các loại <input> (Bảng 12.1)",
        "color": "emerald",
        "bullets": [
          "text, password, date, email, file.",
          "radio (chọn 1 - cùng name) vs checkbox (chọn nhiều).",
          "button và submit để gửi dữ liệu."
        ]
      },
      {
        "heading": "3. Thẻ mở rộng & Gom nhóm",
        "color": "amber",
        "bullets": [
          "<select><option>: danh sách thả xuống.",
          "<textarea rows cols>: văn bản nhiều dòng.",
          "<fieldset><legend>: đóng khung chia nhóm."
        ]
      },
      {
        "heading": "4. Thực hành & Năng lực số",
        "color": "purple",
        "bullets": [
          "Hoàn thiện Đăng kí môn thi (Hình 12.3).",
          "Năng lực số 3.4.NC1.a tạo form hợp chuẩn.",
          "Phát hiện & sửa lỗi radio, label."
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
        "desc": "Quan sát form đăng kí CLB tương tác vs văn bản tĩnh; xác định vai trò biểu mẫu web."
      },
      {
        "stage": "2.1. <form> & <input> (20')",
        "color": "emerald",
        "desc": "Phân tích <form>, <label for> và toàn bộ Bảng 12.1 các kiểu <input>."
      },
      {
        "stage": "2.2. Thẻ mở rộng (15')",
        "color": "amber",
        "desc": "Tìm hiểu <select>, <textarea>, <fieldset>/<legend> và làm Phiếu bài tập qua QR."
      },
      {
        "stage": "3. Thực hành (35')",
        "color": "purple",
        "desc": "Tự gõ mã dang_ki_thi.html (Hình 12.3 SGK tr.70) đạt 8/8 tiêu chí và nộp bài."
      },
      {
        "stage": "4. Infographic & SGK (15')",
        "color": "red",
        "desc": "Hệ thống kiến thức, Flashcards bẫy radio/label và chữa bài tập SGK tr.70."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "BIỂU MẪU WEB LÀ GÌ?",
    "subtitle": "Cầu nối thu thập thông tin trực tiếp từ người dùng trên trình duyệt",
    "theme": "blue",
    "pills": [
      [
        "Đăng nhập / Đăng kí",
        "Tài khoản học trực tuyến, email, mạng xã hội.",
        "blue"
      ],
      [
        "Khảo sát & Đăng kí",
        "Điền phiếu CLB, đăng kí môn thi tốt nghiệp.",
        "emerald"
      ],
      [
        "Tìm kiếm & Đặt hàng",
        "Ô search Google, nhập địa chỉ giao nhận hàng.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • CẤU TRÚC BIỂU MẪU",
    "title": "CẤU TRÚC THẺ <FORM> VÀ NHÃN <LABEL>",
    "sub": "SGK Tin học 12 – Trang 67–68 (Hình 12.1)",
    "theme": "blue",
    "heading": "🧱 Thành phần nền tảng của Form:",
    "bullets": [
      "Mọi điều khiển nhập liệu đặt bên trong cặp <form>...</form>.",
      "action=\"URL\": chỉ định địa chỉ xử lý khi bấm nút Gửi.",
      "<label for=\"ten\"> gắn nhãn mô tả cho ô có id=\"ten\".",
      "Thuộc tính name đặt tên trường dữ liệu gửi đi."
    ],
    "image": "sgk_hinh12_1.png",
    "caption": "Hình 12.1. Minh họa các điều khiển cơ bản trong biểu mẫu (SGK tr.67)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • GẮN NHÃN <LABEL>",
    "title": "KẾT NỐI <LABEL FOR> VỚI <INPUT ID>",
    "sub": "Tăng khả năng tiếp cận (Accessibility) & độ chính xác khi nhập liệu",
    "theme": "blue",
    "filename": "label_form.html",
    "code": "<form action=\"xuly.html\" method=\"post\">\n  <label for=\"hoten\">Họ và tên thí sinh:</label><br>\n  <input id=\"hoten\" type=\"text\" name=\"hoten\" \n         placeholder=\"Nguyễn Văn An\"><br><br>\n\n  <label for=\"matkhau\">Mã dự thi:</label><br>\n  <input id=\"matkhau\" type=\"password\" name=\"pass\">\n</form>",
    "right_heading": "💡 TÁC DỤNG CẶP FOR – ID:",
    "notes": [
      "Thuộc tính for của <label> phải viết GIỐNG HỆT id của <input>.",
      "Nhấp vào chữ 'Họ và tên thí sinh:' con trỏ tự nhảy vào ô chữ.",
      "Rất hữu ích với nút radio/checkbox nhỏ trên màn hình điện thoại."
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • BẢNG 12.1 TRỌNG TÂM",
    "title": "CÁC KIỂU DỮ LIỆU CỦA THẺ <INPUT>",
    "sub": "SGK Tin học 12 – Trang 68 (Kiến thức cốt lõi thi TN THPT)",
    "theme": "emerald",
    "heading": "🎛️ Bảng phân loại type trong <input>:",
    "bullets": [
      "text: ô văn bản một dòng (Họ tên, Địa chỉ).",
      "password: ô mật khẩu (ẩn ký tự thành dấu •).",
      "radio: nút chọn ĐỘC NHẤT 1 phương án (cùng name!).",
      "checkbox: hộp tích chọn NHIỀU phương án.",
      "file / submit / button: chọn tệp, gửi form, nút bấm."
    ],
    "image": "sgk_bang12_1.png",
    "caption": "Bảng 12.1. Tổng hợp các loại phần tử input thông dụng (SGK tr.68)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • BẪY ĐỀ THI RADIO",
    "title": "BÍ QUYẾT DÙNG RADIO & CHECKBOX CHUẨN XÁC",
    "sub": "Lưu ý bắt buộc thuộc tính name trên nút radio",
    "theme": "blue",
    "filename": "chon_lua.html",
    "code": "<form>\n  <!-- Radio chọn 1: PHẢI CÙNG name=\"gt\" -->\n  <p>Giới tính:\n    <input type=\"radio\" id=\"nam\" name=\"gt\" value=\"Nam\">\n    <label for=\"nam\">Nam</label>\n    <input type=\"radio\" id=\"nu\" name=\"gt\" value=\"Nu\">\n    <label for=\"nu\">Nữ</label>\n  </p>\n  <!-- Checkbox chọn nhiều: name độc lập -->\n  <p>Sở thích:\n    <input type=\"checkbox\" name=\"bongda\"> Bóng đá\n    <input type=\"checkbox\" name=\"amnhac\"> Âm nhạc\n  </p>\n</form>",
    "right_heading": "⚠️ LỖI HAY GẶP NHẤT:",
    "notes": [
      "Nếu quên đặt hoặc đặt khác name trên radio -> người dùng tick được CẢ HAI nút Nam và Nữ!",
      "Mỗi <label for=\"X\"> phải khớp id=\"X\" của ô <input>.",
      "value quy định giá trị thực tế gửi về máy chủ."
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • CÁC KIỂU INPUT KHÁC",
    "title": "Ô CHỌN TỆP, NGÀY THÁNG & CÁC NÚT ĐIỀU KHIỂN",
    "sub": "Hoàn chỉnh bộ thuộc tính Bảng 12.1 SGK tr.68",
    "theme": "emerald",
    "left": {
      "heading": "📅 Nhập liệu chuyên biệt",
      "color": "blue",
      "bullets": [
        "type=\"date\": mở lịch chọn ngày/tháng/năm.",
        "type=\"email\": kiểm tra có ký tự @ hợp lệ.",
        "type=\"number\": ô nhập số có nút tăng giảm.",
        "type=\"file\": nút chọn tệp đính kèm từ máy."
      ]
    },
    "right": {
      "heading": "🚀 Các nút bấm hành động",
      "color": "emerald",
      "bullets": [
        "type=\"submit\": gửi toàn bộ dữ liệu form tới action.",
        "type=\"reset\": xóa sạch giá trị đã nhập về mặc định.",
        "type=\"button\": nút trống gắn sự kiện JavaScript.",
        "Thuộc tính value=\"...\" quy định nhãn chữ trên nút."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • THẺ MỞ RỘNG",
    "title": "SELECT, TEXTAREA & FIELDSET",
    "subtitle": "Tối ưu bố cục khi có nhiều lựa chọn hoặc cần nhập văn bản dài",
    "theme": "amber",
    "pills": [
      [
        "<select> & <option>",
        "Menu xổ xuống chọn lớp, tỉnh/thành, môn thi.",
        "blue"
      ],
      [
        "<textarea>",
        "Ô nhập nhiều dòng có thuộc tính rows và cols.",
        "emerald"
      ],
      [
        "<fieldset> & <legend>",
        "Vẽ khung viền gom nhóm và đặt tiêu đề khung.",
        "amber"
      ]
    ]
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.2 • CÚ PHÁP MỞ RỘNG",
    "title": "SỬ DỤNG <SELECT>, <TEXTAREA> VÀ <FIELDSET>",
    "sub": "SGK Tin học 12 – Trang 69",
    "theme": "amber",
    "filename": "form_morong.html",
    "code": "<form>\n  <fieldset>\n    <legend>Thông tin bổ sung</legend>\n    <label for=\"lop\">Chọn lớp:</label>\n    <select id=\"lop\" name=\"lop\">\n      <option value=\"12A1\">Lớp 12A1</option>\n      <option value=\"12A2\">Lớp 12A2</option>\n    </select><br><br>\n    <label for=\"gopy\">Ghi chú:</label><br>\n    <textarea id=\"gopy\" rows=\"3\" cols=\"30\"></textarea>\n  </fieldset>\n</form>",
    "right_heading": "📌 LƯU Ý CÚ PHÁP:",
    "notes": [
      "<textarea> là thẻ GHÉP (phải có </textarea>), khác với <input type=\"text\"> là thẻ đơn!",
      "<option selected> chọn sẵn mục mặc định.",
      "<legend> phải đặt ngay bên trong <fieldset>."
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • MINH HỌA SGK",
    "title": "GIAO DIỆN BIỂU MẪU VỚI FIELDSET & SELECT",
    "sub": "SGK Tin học 12 – Trang 69 (Hình 12.2)",
    "theme": "purple",
    "heading": "📐 Quan sát trực quan Hình 12.2:",
    "bullets": [
      "Đường viền mảnh bao quanh từng khối logic thông tin.",
      "Chữ của thẻ <legend> nằm vắt gọn ngay trên cạnh viền trên.",
      "Hộp chọn thả xuống giúp giao diện gọn gàng hơn nhiều nút radio."
    ],
    "image": "sgk_hinh12_2.png",
    "caption": "Hình 12.2. Biểu mẫu sử dụng <select>, <textarea> và <fieldset> (SGK tr.69)"
  },
  {
    "kind": "section",
    "tag": "NHIỆM VỤ ĐÁNH GIÁ NHANH",
    "title": "PHIẾU BÀI TẬP BÀI 12",
    "subtitle": "Quét mã QR hoặc truy cập hd2-2.html -> phieu-bai-tap.html (6 câu chuẩn BGD&ĐT)",
    "theme": "blue",
    "pills": [
      [
        "4 Câu MCQ",
        "Phân biệt password, fieldset/legend, select/option, label for.",
        "blue"
      ],
      [
        "2 Câu Đúng/Sai",
        "Đọc hiểu mã form & phân biệt thuộc tính name/type.",
        "emerald"
      ],
      [
        "Chấm realtime",
        "Điểm tự động cập nhật về bảng điều khiển Giáo viên.",
        "purple"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "KIỂM TRA NHANH 2.2",
    "title": "TÌNH HUỐNG SỬA LỖI BIỂU MẪU",
    "sub": "Chuẩn đề tham khảo TN THPT môn Tin học",
    "question": "Một bạn viết 2 nút chọn Đáp án nhưng trên trình duyệt lại tích được cả hai phương án cùng lúc:\n<input type=\"radio\" name=\"c1\" value=\"A\"> A\n<input type=\"radio\" name=\"c2\" value=\"B\"> B\nCần sửa gì để chỉ chọn được 1 đáp án?",
    "options": [
      "A. Đổi type=\"radio\" thành type=\"checkbox\"",
      "B. Đặt cùng giá trị thuộc tính name (ví dụ name=\"c1\") cho cả 2 thẻ",
      "C. Đặt cùng giá trị id cho cả 2 thẻ",
      "D. Đặt cùng thuộc tính value cho cả 2 thẻ"
    ],
    "answer": [
      "Đáp án đúng: B (Đặt cùng giá trị name).",
      "Giải thích: Trình duyệt nhóm các nút radio dựa vào thuộc tính name giống nhau; không được đặt trùng id."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (35 PHÚT)",
    "title": "BIỂU MẪU ĐĂNG KÍ MÔN THI TỐT NGHIỆP",
    "subtitle": "Thực hành tự code tệp dang_ki_thi.html theo Hình 12.3 SGK tr.70",
    "theme": "purple",
    "pills": [
      [
        "Khối 1: Thông tin TS",
        "Họ tên (text), Ngày sinh (date), Giới tính (radio).",
        "blue"
      ],
      [
        "Khối 2: Môn thi & Cụm",
        "checkbox chọn môn tự chọn, <select> chọn cụm thi.",
        "emerald"
      ],
      [
        "Gửi & Nhóm khung",
        "Dùng <fieldset>, <legend> và <input type=\"submit\">.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • MẪU THỰC HÀNH SGK",
    "title": "MỤC TIÊU GIAO DIỆN HÌNH 12.3 (SGK TR.70)",
    "sub": "Thực hành độc lập trên trình soạn mã trống hd3.html",
    "theme": "purple",
    "heading": "✅ Kiểm tra đủ 8 tiêu chí tự động:",
    "bullets": [
      "Có <form> và ít nhất 1 cặp <fieldset> + <legend>.",
      "Có cặp <label for=\"...\"> khớp với <input id=\"...\">.",
      "Có ô nhập chữ type=\"text\" (hoặc date/email).",
      "Có nhóm type=\"radio\" dùng chung thuộc tính name.",
      "Có type=\"checkbox\", <select>/<option> và nút type=\"submit\"."
    ],
    "image": "sgk_hinh12_3.png",
    "caption": "Hình 12.3. Giao diện Biểu mẫu Đăng kí môn thi tốt nghiệp (SGK tr.70)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 3 • GỢI Ý CẤU TRÚC FORM THI",
    "title": "PHÂN TÍCH MÃ NGUỒN ĐĂNG KÍ MÔN THI",
    "sub": "Tổ chức 2 khối <fieldset> rõ ràng, mạch lạc",
    "theme": "purple",
    "filename": "dang_ki_thi.html",
    "code": "<form action=\"xuly.html\">\n  <fieldset>\n    <legend>Thông tin thí sinh</legend>\n    <label for=\"ht\">Họ tên:</label>\n    <input id=\"ht\" type=\"text\" name=\"hoten\"><br>\n    <input type=\"radio\" name=\"gt\" value=\"Nam\"> Nam\n    <input type=\"radio\" name=\"gt\" value=\"Nu\"> Nữ\n  </fieldset>\n  <fieldset>\n    <legend>Môn tự chọn</legend>\n    <input type=\"checkbox\" name=\"m\" value=\"Tin\"> Tin\n    <input type=\"submit\" value=\"Gửi đăng kí\">\n  </fieldset>\n</form>",
    "right_heading": "🔍 KIỂM TRA TRƯỚC KHI NỘP:",
    "notes": [
      "Mỗi <input> nên có thuộc tính name và value rõ ràng.",
      "Bổ sung <select> chọn Cụm thi và <textarea> ghi chú.",
      "Chạy thử 'Kiểm tra tiêu chí' đạt 8/8 rồi mới nộp bài!"
    ]
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC",
    "title": "TỔNG HỢP BỘ THẺ TẠO BIỂU MẪU HTML5",
    "sub": "Nhớ nhanh cú pháp và công dụng từng thẻ",
    "theme": "blue",
    "cols": [
      {
        "heading": "Khung & Nhãn",
        "color": "blue",
        "subhead": "Nền tảng tổ chức",
        "bullets": [
          "<form action=\"...\" method=\"...\">",
          "<label for=\"id_o\">Nhãn</label>",
          "<fieldset> + <legend>"
        ]
      },
      {
        "heading": "Các kiểu <input>",
        "color": "emerald",
        "subhead": "Thẻ đơn linh hoạt",
        "bullets": [
          "text, password, date, file",
          "radio (1 chọn, chung name)",
          "checkbox (nhiều chọn), submit"
        ]
      },
      {
        "heading": "Phần tử mở rộng",
        "color": "amber",
        "subhead": "Menu & Văn bản lớn",
        "bullets": [
          "<select><option>...</option></select>",
          "<textarea rows cols></textarea>",
          "Nút reset / button tùy biến"
        ]
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • GIẢI ĐÁP SGK TRANG 70",
    "title": "ĐÁP ÁN LUYỆN TẬP & VẬN DỤNG",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 70",
    "theme": "emerald",
    "left": {
      "heading": "✏️ Luyện tập (Trang 70)",
      "color": "blue",
      "bullets": [
        "Vai trò của <label for=\"id\">: liên kết chữ mô tả với ô điều khiển có id tương ứng.",
        "Khi bấm chuột vào chữ nhãn -> tự động focus vào ô chữ hoặc đánh dấu radio/checkbox.",
        "Giúp nâng cao khả năng tiếp cận (Accessibility) cho người dùng."
      ]
    },
    "right": {
      "heading": "🚀 Vận dụng 1 & 2 (Trang 70)",
      "color": "emerald",
      "bullets": [
        "VD1: Tạo biểu mẫu đăng kí tham gia CLB (text Họ tên, radio Khối lớp, <select> chọn CLB, checkbox lịch rảnh, submit).",
        "VD2: Tạo form góp ý website dùng text, email, <textarea> nhập ý kiến đóng góp và nút submit."
      ]
    }
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP CHUẨN TN THPT",
    "title": "BẪY ĐỀ THI: CẤU TRÚC & THUỘC TÍNH FORM HTML",
    "sub": "Đọc hiểu đoạn mã biểu mẫu chuẩn đề 2025/2026",
    "question": "Cho đoạn mã: <form action=\"reg.html\"><label for=\"u\">Tên:</label><input id=\"u\" type=\"text\"><input type=\"radio\" name=\"c\" value=\"1\">KHTN <input type=\"radio\" name=\"c\" value=\"2\">KHXH <input type=\"submit\" value=\"Gửi\"></form>",
    "options": [
      "a) Bấm chữ 'Tên:' con trỏ nhảy vào ô có id=\"u\".",
      "b) Có thể chọn đồng thời cả KHTN và KHXH.",
      "c) Nút Gửi sẽ gửi dữ liệu đến reg.html.",
      "d) Dùng <textarea> để thay ô nhập nhiều dòng."
    ],
    "answer": [
      "a) Đúng — for=\"u\" khớp id=\"u\".",
      "b) Sai — hai radio cùng name=\"c\" nên chỉ chọn 1.",
      "c) Đúng — action=\"reg.html\" là đích nhận dữ liệu.",
      "d) Đúng — <textarea rows cols> nhập nhiều dòng."
    ]
  },
  {
    "kind": "two_col",
    "badge": "TỔNG KẾT PHẦN HTML (BÀI 7 – BÀI 12)",
    "title": "NHÌN LẠI CHẶNG ĐƯỜNG XÂY DỰNG WEB HTML5",
    "sub": "Sẵn sàng cho bài Thực hành tổng hợp HTML & Kiểm tra KTTX3",
    "theme": "purple",
    "left": {
      "heading": "🧱 Cấu trúc & Nội dung (Bài 7–10)",
      "color": "blue",
      "bullets": [
        "Cấu trúc <!DOCTYPE html>, <head>, <body>.",
        "Văn bản ngữ nghĩa <strong>, <em>, tiêu đề <h1>–<h6>.",
        "Danh sách <ol>, <ul>, <dl> và bảng rowspan/colspan.",
        "Siêu liên kết <a href>, #id, đường dẫn ../."
      ]
    },
    "right": {
      "heading": "🎛️ Đa phương tiện & Biểu mẫu (Bài 11–12)",
      "color": "emerald",
      "bullets": [
        "Chèn ảnh <img> tự co giãn đúng tỉ lệ.",
        "Âm thanh <audio>, video <video>, <source>.",
        "Nhúng khung <iframe> điều hướng bằng target.",
        "Tạo biểu mẫu tương tác <form>, <input>, <fieldset>."
      ]
    }
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 12: TẠO BIỂU MẪU HTML5!",
    "takeaways": [
      "Mọi phần tử nhập liệu đặt trong <form>; dùng <label for> khớp id của thẻ nhập.",
      "Nhóm nút radio bắt buộc dùng CHUNG thuộc tính name; checkbox dùng để chọn nhiều mục.",
      "Kết hợp <select>, <textarea>, <fieldset>, <legend> giúp biểu mẫu gọn gàng, trực quan.",
      "Chuẩn bị bài tiếp theo: Thực hành tổng hợp HTML (Bài 7–12) và Kiểm tra thường xuyên 3 (KTTX3)."
    ]
  }
]
LESSON_SHORT = "Bài 12: Tạo biểu mẫu"
OUT_PPTX_NAME = "Bai12_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
