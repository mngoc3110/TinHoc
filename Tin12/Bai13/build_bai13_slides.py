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
    "pill": "TIN HỌC 12 • KẾT NỐI TRI THỨC • TUẦN 16",
    "title": "BÀI 13: KHÁI NIỆM, VAI TRÒ CỦA CSS",
    "subtitle": "Cascading Style Sheets — Tách biệt định dạng khỏi HTML, Cấu trúc quy tắc & 3 cách thiết lập CSS",
    "meta": "Tuần 16 (Tiết 31–32)",
    "url": "https://minda.io.vn/Tin12/Bai13/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI HỌC & NĂNG LỰC SỐ",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.1.NC1b",
    "cards": [
      {
        "heading": "1. Khái niệm & Cấu trúc CSS",
        "color": "blue",
        "bullets": [
          "Hiểu CSS (Cascading Style Sheets) là gì.",
          "Viết đúng bộ chọn + vùng mô tả { ... }.",
          "Biết gộp bộ chọn & viết chú thích /* ... */."
        ]
      },
      {
        "heading": "2. Ba cách thiết lập CSS",
        "color": "emerald",
        "bullets": [
          "CSS trong (Internal): <style> trong <head>.",
          "CSS ngoài (External): <link> hoặc @import.",
          "CSS nội tuyến (Inline): thuộc tính style."
        ]
      },
      {
        "heading": "3. Vai trò & Ý nghĩa thực tiễn",
        "color": "amber",
        "bullets": [
          "Tách rời nội dung (HTML) và trình bày (CSS).",
          "Đồng bộ giao diện cho cả trăm trang web.",
          "Tiết kiệm công sức bảo trì, chỉnh sửa mã."
        ]
      },
      {
        "heading": "4. Thực hành & Năng lực số",
        "color": "purple",
        "bullets": [
          "Tự code Lich_su_CSS.html (SGK tr.74–75).",
          "Năng lực số 3.1.NC1b thiết kế bố cục số.",
          "Sửa lỗi cú pháp CSS chuẩn xác."
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
        "desc": "So sánh trang HTML thuần (Hình 13.1) với trang đã định dạng CSS (Hình 13.2)."
      },
      {
        "stage": "2.1. Cấu trúc CSS (20')",
        "color": "emerald",
        "desc": "Cú pháp bộ chọn { thuộc tính: giá trị; }, gộp bộ chọn và chú thích /* ... */."
      },
      {
        "stage": "2.2. 3 cách & Vai trò (15')",
        "color": "amber",
        "desc": "Phân biệt Internal, External, Inline CSS; vai trò CSS và làm Phiếu bài tập qua QR."
      },
      {
        "stage": "3. Thực hành CSS (35')",
        "color": "purple",
        "desc": "Tự gõ mã tạo bài viết Lịch sử CSS (Lich_su_CSS.html) đạt 8/8 tiêu chí."
      },
      {
        "stage": "4. Infographic & SGK (15')",
        "color": "red",
        "desc": "Hệ thống kiến thức 4 chế độ & giải Luyện tập 1–2, Vận dụng 1–2 (tr.75)."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "VÌ SAO PHẢI HỌC CSS?",
    "subtitle": "Khi HTML lo cấu trúc khung xương, CSS chính là nhà thiết kế giao diện",
    "theme": "blue",
    "pills": [
      [
        "HTML: Nội dung",
        "Đoạn văn, tiêu đề, danh sách, bảng, biểu mẫu.",
        "blue"
      ],
      [
        "CSS: Trình bày",
        "Màu sắc, phông chữ, viền, nền, khoảng cách.",
        "emerald"
      ],
      [
        "Đồng bộ hóa",
        "Một tệp CSS điều khiển giao diện toàn website.",
        "purple"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 1 • SO SÁNH TRỰC QUAN",
    "title": "TRƯỚC KHI ÁP DỤNG CSS (HÌNH 13.1)",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 71",
    "theme": "amber",
    "heading": "📄 Trang HTML thuần (chưa có CSS):",
    "bullets": [
      "Chữ màu đen đơn điệu trên nền trắng.",
      "Phông chữ mặc định Times New Roman.",
      "Không có viền trang trí, khoảng cách dòng sát nhau.",
      "Muốn tô màu từng thẻ phải chép style=\"...\" lặp lại rất dài."
    ],
    "image": "sgk_hinh13_1.png",
    "caption": "Hình 13.1. Giao diện trang web chỉ dùng HTML mặc định (SGK tr.71)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 1 • SAU KHI CÓ CSS",
    "title": "SAU KHI ÁP DỤNG CSS (HÌNH 13.2)",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 71",
    "theme": "emerald",
    "heading": "✨ Sức mạnh biến đổi của CSS:",
    "bullets": [
      "Nội dung HTML hoàn toàn giữ nguyên không bị phình to.",
      "Tiêu đề, đoạn văn có màu sắc, căn lề, phông chữ hài hòa.",
      "Dễ dàng thay đổi toàn bộ diện mạo chỉ bằng chỉnh vài dòng CSS!"
    ],
    "image": "sgk_hinh13_2.png",
    "caption": "Hình 13.2. Trang web trở nên sinh động, chuyên nghiệp nhờ CSS (SGK tr.71)"
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.1 • CÚ PHÁP CSS",
    "title": "CẤU TRÚC MẪU ĐỊNH DẠNG CSS",
    "subtitle": "Ngôn ngữ độc lập với HTML — Quy tắc viết đúng từng dấu chấm phẩy",
    "theme": "emerald",
    "pills": [
      [
        "Bộ chọn (Selector)",
        "Chỉ định những phần tử HTML nào được áp dụng.",
        "blue"
      ],
      [
        "Vùng mô tả { ... }",
        "Chứa 1 hoặc nhiều khai báo: thuộc_tính: giá_trị;",
        "emerald"
      ],
      [
        "Chú thích /* ... */",
        "Ghi chú không ảnh hưởng đến việc hiển thị.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • CẤU TRÚC TỔNG QUÁT",
    "title": "GIẢI PHẪU MỘT MẪU ĐỊNH DẠNG CSS (HÌNH 13.3)",
    "sub": "SGK Tin học 12 – Trang 72",
    "theme": "blue",
    "heading": "🧩 Ghi nhớ 3 thành phần chính:",
    "bullets": [
      "Bộ chọn: tên thẻ HTML (ví dụ h1, p) hoặc nhóm thẻ h1, h2.",
      "Thuộc tính & Giá trị cách nhau bởi dấu HAI CHẤM (:).",
      "Các khai báo cách nhau bởi dấu CHẤM PHẨY (;).",
      "Toàn bộ vùng mô tả đặt trong cặp ngoặc nhọn { }."
    ],
    "image": "sgk_hinh13_3.png",
    "caption": "Hình 13.3. Cấu trúc tổng quát của mẫu định dạng CSS (SGK tr.72)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • GỘP BỘ CHỌN & CHÚ THÍCH",
    "title": "VIẾT CSS GỌN ĐẸP VỚI BỘ CHỌN GỘP",
    "sub": "Thay vì viết lặp lại, gộp nhiều bộ chọn bằng dấu phẩy (,)",
    "theme": "emerald",
    "filename": "styles.css",
    "code": "/* Chú thích CSS nằm giữa /* và */ */\nh1, h2, h3 {\n  color: #1e3a8a;\n  font-family: Arial, sans-serif;\n}\n\np {\n  color: #334155;\n  line-height: 1.6;\n}",
    "right_heading": "⚠️ TRÁNH LỖI CÚ PHÁP HAY GẶP:",
    "notes": [
      "KHÔNG dùng <!-- --> hay // để chú thích trong CSS (phải dùng /* ... */).",
      "Quên dấu ; giữa hai khai báo khiến cả hai khai báo đều bị lỗi.",
      "Khi gộp h1, h2 phải có dấu phẩy ngăn cách tên các thẻ."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • CÁCH THIẾT LẬP",
    "title": "3 CÁCH NHÚNG CSS VÀO TRANG HTML",
    "subtitle": "Internal CSS, External CSS và Inline CSS (SGK trang 73)",
    "theme": "amber",
    "pills": [
      [
        "CSS trong (Internal)",
        "Đặt cặp thẻ <style>...</style> bên trong <head>.",
        "blue"
      ],
      [
        "CSS ngoài (External)",
        "Tệp .css tách biệt, gọi qua <link> hoặc @import.",
        "emerald"
      ],
      [
        "CSS nội tuyến (Inline)",
        "Viết thuộc tính style=\"...\" thẳng trên thẻ mở HTML.",
        "purple"
      ]
    ]
  },
  {
    "kind": "three_col",
    "badge": "HĐ 2.2 • SO SÁNH 3 CÁCH THIẾT LẬP",
    "title": "KHI NÀO NÊN DÙNG INTERNAL, EXTERNAL, INLINE?",
    "sub": "SGK Tin học 12 – Trang 73–74",
    "theme": "blue",
    "cols": [
      {
        "heading": "1. CSS trong (Internal)",
        "color": "blue",
        "subhead": "<style> trong <head>",
        "bullets": [
          "Phù hợp trang web đơn độc lập.",
          "Quản lý chung toàn bộ thẻ trên trang đó.",
          "Không chia sẻ sang tệp HTML khác được."
        ]
      },
      {
        "heading": "2. CSS ngoài (External)",
        "color": "emerald",
        "subhead": "<link href='s.css'>",
        "bullets": [
          "Khuyên dùng cho mọi dự án web!",
          "Một tệp .css áp dụng cho cả website.",
          "Sửa 1 chỗ -> cập nhật hàng loạt trang."
        ]
      },
      {
        "heading": "3. CSS nội tuyến (Inline)",
        "color": "amber",
        "subhead": "style=\"color:red;\"",
        "bullets": [
          "Chỉ tác dụng lên đúng thẻ chứa nó.",
          "Khó bảo trì, trộn lẫn HTML & CSS.",
          "Chỉ dùng thử nhanh hoặc chỉnh ngoại lệ."
        ]
      }
    ]
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.2 • EXTERNAL CSS CHUẨN",
    "title": "2 CÁCH GỌI TỆP CSS NGOÀI VÀO HTML",
    "sub": "Sử dụng thẻ <link> (ưu tiên) hoặc lệnh @import",
    "theme": "emerald",
    "filename": "index.html",
    "code": "<head>\n  <meta charset=\"UTF-8\">\n  <!-- Cách 1 (Phổ biến): Dùng thẻ đơn <link> -->\n  <link href=\"styles.css\" rel=\"stylesheet\" type=\"text/css\">\n\n  <!-- Cách 2: Dùng @import bên trong <style> -->\n  <style>\n    @import \"styles.css\";\n  </style>\n</head>",
    "right_heading": "💡 GHI NHỚ THUỘC TÍNH <LINK>:",
    "notes": [
      "rel=\"stylesheet\": báo trình duyệt tệp đích là bảng định kiểu CSS.",
      "href=\"styles.css\": đường dẫn tới tệp .css (cùng cơ chế ../ như <a>).",
      "<link> đặt bên trong thẻ <head> của mọi trang muốn đồng bộ."
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.2 • VAI TRÒ CỦA CSS",
    "title": "4 LỢI ÍCH CỐT LÕI KHI TÁCH CSS KHỎI HTML",
    "sub": "SGK Tin học 12 – Trang 74",
    "theme": "purple",
    "left": {
      "heading": "🎯 Đối với Lập trình viên & Thiết kế",
      "color": "blue",
      "bullets": [
        "Tách bạch Nội dung (HTML) và Hình thức (CSS).",
        "Một tệp HTML sạch sẽ, dễ đọc cấu trúc ngữ nghĩa.",
        "Chỉnh màu sắc, phông chữ hàng loạt chỉ trong tích tắc."
      ]
    },
    "right": {
      "heading": "⚡ Đối với Hệ thống Web & Người dùng",
      "color": "emerald",
      "bullets": [
        "Giảm lặp mã -> tệp HTML nhẹ, tải trang nhanh hơn.",
        "Trình duyệt lưu cache tệp .css dùng lại cho các trang sau.",
        "Dễ dàng tùy biến giao diện thích ứng đa màn hình."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "NHIỆM VỤ ĐÁNH GIÁ NHANH",
    "title": "PHIẾU BÀI TẬP BÀI 13",
    "subtitle": "Quét mã QR hoặc mở hd2-2.html -> phieu-bai-tap.html (6 câu chuẩn BGD&ĐT)",
    "theme": "blue",
    "pills": [
      [
        "4 Câu MCQ",
        "Cấu trúc CSS, chú thích /* */, Internal/External/Inline.",
        "blue"
      ],
      [
        "2 Câu Đúng/Sai",
        "Đọc hiểu tệp styles.css và phát hiện lỗi cú pháp.",
        "emerald"
      ],
      [
        "Chấm realtime",
        "Tự động lưu kết quả về bảng điều khiển Giáo viên.",
        "purple"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "KIỂM TRA NHANH 2.2",
    "title": "PHÁT HIỆN LỖI CÚ PHÁP CSS",
    "sub": "Dạng câu hỏi phổ biến đề TN THPT",
    "question": "Một học sinh viết quy tắc CSS trong thẻ <style> như sau nhưng không có hiệu lực:\np { color = blue, font-size: 16px }\nCần sửa những lỗi cú pháp nào?",
    "options": [
      "A. Đổi p thành body",
      "B. Thay dấu = thành dấu : và thay dấu , thành dấu ;",
      "C. Thêm dấu ngoặc kép quanh chữ blue",
      "D. Đổi ngoặc nhọn { } thành ngoặc vuông [ ]"
    ],
    "answer": [
      "Đáp án đúng: B.",
      "Cú pháp chuẩn: p { color: blue; font-size: 16px; }",
      "Giữa thuộc tính và giá trị phải dùng dấu hai chấm (:); giữa các khai báo dùng chấm phẩy (;)."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (35 PHÚT)",
    "title": "TẠO TRANG LỊCH SỬ CSS (LICH_SU_CSS.HTML)",
    "subtitle": "Thực hành tự code độc lập trên hd3.html (SGK trang 74–75)",
    "theme": "purple",
    "pills": [
      [
        "Nội dung chuẩn SGK",
        "Trình bày bài viết Håkon Wium Lie (1994), CSS1, CSS2, CSS3.",
        "blue"
      ],
      [
        "Internal CSS <style>",
        "Định dạng h1, h2, p, ul bên trong khối <style> ở <head>.",
        "emerald"
      ],
      [
        "Gộp & Chú thích",
        "Dùng bộ chọn gộp (h1, h2) và chú thích /* ... */.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • VĂN BẢN THỰC HÀNH SGK",
    "title": "NỘI DUNG BÀI THỰC HÀNH LỊCH SỬ CSS",
    "sub": "SGK Tin học 12 – Trang 74–75",
    "theme": "purple",
    "heading": "📜 Các ý chính cần đưa vào trang:",
    "bullets": [
      "Năm 1994: Håkon Wium Lie đề xuất ý tưởng CSS tại CERN.",
      "Năm 1996: W3C chính thức công bố chuẩn CSS1.",
      "CSS2 (1998) và CSS2.1 bổ sung định vị, phương tiện in ấn.",
      "CSS3 phát triển theo từng mô-đun hiện đại (hỗ trợ HTML5)."
    ],
    "image": "sgk_lichsu_css.png",
    "caption": "Trích đoạn thực hành Lịch sử CSS trong SGK Tin học 12 (tr.74–75)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 3 • RUBRIC CHẤM BÀI",
    "title": "8 TIÊU CHÍ TỰ ĐỘNG CHO LICH_SU_CSS.HTML",
    "sub": "Kiểm tra đạt 8/8 trước khi bấm Nộp bài thực hành",
    "theme": "purple",
    "left": {
      "heading": "📄 Tiêu chí 1 – 4 (HTML & Nội dung)",
      "color": "blue",
      "bullets": [
        "1. Cấu trúc chuẩn <!DOCTYPE html>, <html>, <head>, <body>.",
        "2. Có tiêu đề chính <h1>Lịch sử CSS</h1>.",
        "3. Có các tiêu đề mục <h2> và đoạn văn <p> hoặc <ul>.",
        "4. Nhắc đúng tên tác giả CSS hoặc tổ chức W3C."
      ]
    },
    "right": {
      "heading": "🎨 Tiêu chí 5 – 8 (Quy tắc CSS)",
      "color": "emerald",
      "bullets": [
        "5. Có khối <style>...</style> đặt trong <head>.",
        "6. Có chú thích CSS chuẩn /* ... */.",
        "7. Có sử dụng bộ chọn gộp nhiều thẻ (h1, h2).",
        "8. Có khai báo thuộc tính color hoặc font-family chuẩn ;."
      ]
    }
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC",
    "title": "3 ĐIỂM NHỚ TRỌNG TÂM CỦA BÀI 13",
    "sub": "Nền móng trước khi học sâu các thuộc tính CSS ở Bài 14–15",
    "theme": "blue",
    "cols": [
      {
        "heading": "Cú pháp 1 quy tắc",
        "color": "blue",
        "subhead": "Selector + Declaration",
        "bullets": [
          "bộ_chọn { tt1: gt1; tt2: gt2; }",
          "Gộp bộ chọn bằng dấu phẩy (,).",
          "Chú thích bằng /* ... */."
        ]
      },
      {
        "heading": "3 Cách thiết lập",
        "color": "emerald",
        "subhead": "Internal - External - Inline",
        "bullets": [
          "Internal: <style> trong <head>.",
          "External: <link rel='stylesheet'>.",
          "Inline: thuộc tính style='...'."
        ]
      },
      {
        "heading": "Vai trò vượt trội",
        "color": "amber",
        "subhead": "Vì sao dùng External CSS?",
        "bullets": [
          "Tách nội dung khỏi định dạng.",
          "1 tệp .css dùng chung nhiều trang.",
          "Sửa 1 nơi cập nhật toàn website."
        ]
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • GIẢI ĐÁP SGK TRANG 75",
    "title": "ĐÁP ÁN LUYỆN TẬP & VẬN DỤNG",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 75",
    "theme": "emerald",
    "left": {
      "heading": "✏️ Luyện tập 1 & 2 (Trang 75)",
      "color": "blue",
      "bullets": [
        "LT1: Gồm bộ chọn + vùng mô tả; 3 cách: Internal, External, Inline.",
        "LT2: Kiểm tra dấu : (thay =), dấu ; kết thúc khai báo, ngoặc { } và chú thích /* */."
      ]
    },
    "right": {
      "heading": "🚀 Vận dụng 1 & 2 (Trang 75)",
      "color": "emerald",
      "bullets": [
        "VD1: Tạo tệp css/style.css chứa quy tắc chung cho trang CLB.",
        "VD2: Chèn <link rel='stylesheet' href='styles.css'> vào mọi trang index.html, CLB.html, the_thao.html."
      ]
    }
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP CHUẨN TN THPT",
    "title": "ĐỌC HIỂU ĐOẠN MÃ THIẾT LẬP EXTERNAL CSS",
    "sub": "Củng cố câu hỏi Đúng/Sai thường gặp",
    "question": "Trong tệp index.html đặt thẻ <link href=\"css/chung.css\" rel=\"stylesheet\"> trong <head>, và tệp chung.css có: /* Mau chung */ h1, h2 { color: navy; }",
    "options": [
      "a) Cách trên thiết lập CSS theo kiểu CSS ngoài (External CSS).",
      "b) Nội dung trong /* Mau chung */ gây lỗi biên dịch CSS.",
      "c) Cả thẻ <h1> và thẻ <h2> trên index.html đều có chữ màu xanh navy.",
      "d) Các trang khác có thể gắn cùng thẻ <link> trên để đồng bộ màu tiêu đề."
    ],
    "answer": [
      "a) Đúng — Dùng thẻ <link> trỏ tệp .css rời.",
      "b) Sai — /* ... */ là cú pháp chú thích hợp lệ của CSS.",
      "c) Đúng — Bộ chọn gộp h1, h2 áp dụng cho cả hai thẻ.",
      "d) Đúng — Tái sử dụng 1 tệp CSS cho nhiều trang web."
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 13: KHÁI NIỆM & VAI TRÒ CSS!",
    "takeaways": [
      "Cú pháp chuẩn: bộ_chọn { thuộc_tính: giá_trị; } với chú thích /* ... */.",
      "Ưu tiên External CSS (<link rel=\"stylesheet\" href=\"...\">) để đồng bộ nhiều trang web.",
      "Chuẩn bị Bài 14 (Tuần 17): Định dạng văn bản bằng CSS (font, text-align, kế thừa & Cascading!)."
    ]
  }
]
LESSON_SHORT = "Bài 13: Khái niệm, vai trò của CSS"
OUT_PPTX_NAME = "Bai13_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
