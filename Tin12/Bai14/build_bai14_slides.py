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
    "pill": "TIN HỌC 12 • KẾT NỐI TRI THỨC • TUẦN 17",
    "title": "BÀI 14: ĐỊNH DẠNG VĂN BẢN BẰNG CSS",
    "subtitle": "Làm chủ Phông chữ (font-*), Dòng văn bản (text-*), Tính kế thừa & Thứ tự ưu tiên Cascading",
    "meta": "Tuần 17 (Tiết 33–34)",
    "url": "https://minda.io.vn/Tin12/Bai14/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI HỌC & NĂNG LỰC SỐ",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.1.NC1a",
    "cards": [
      {
        "heading": "1. Thuộc tính Phông chữ",
        "color": "blue",
        "bullets": [
          "5 họ phông CSS (serif, sans-serif, monospace...).",
          "Đơn vị font-size: px, pt, cm, em, rem, %.",
          "font-style: italic & font-weight (500+ đậm)."
        ]
      },
      {
        "heading": "2. Thuộc tính Dòng văn bản",
        "color": "emerald",
        "bullets": [
          "line-height điều chỉnh chiều cao dòng.",
          "text-align: left | center | right | justify.",
          "text-decoration & text-indent (thụt lề âm)."
        ]
      },
      {
        "heading": "3. Kế thừa & Cascading",
        "color": "amber",
        "bullets": [
          "Phân biệt thuộc tính kế thừa vs không kế thừa.",
          "Thứ tự ưu tiên: viết sau thắng viết trước.",
          "Biết ý nghĩa bộ chọn * và từ khóa !important."
        ]
      },
      {
        "heading": "4. Thực hành & Năng lực số",
        "color": "purple",
        "bullets": [
          "Hoàn thành Chia_de_tri.html (SGK tr.80–81).",
          "Giải bài Trời Hà Nội xanh (LT2 tr.82).",
          "Năng lực số 3.1.NC1a định dạng văn bản số."
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
        "desc": "So sánh bài viết Kĩ thuật chia để trị bản mộc vs bản định dạng Typography CSS."
      },
      {
        "stage": "2.1. Phông & Màu (20')",
        "color": "emerald",
        "desc": "5 họ phông, quy đổi px/pt/em, font-style: italic, font-weight 100–900, color."
      },
      {
        "stage": "2.2. Dòng & Ưu tiên (15')",
        "color": "amber",
        "desc": "line-height, text-align/decoration/indent, Tính kế thừa, Cascading & Phiếu BT QR."
      },
      {
        "stage": "3. Thực hành (35')",
        "color": "purple",
        "desc": "Tự gõ mã tạo trang Chia_de_tri.html (Hình 14.7–14.8 SGK) đạt 8/8 tiêu chí."
      },
      {
        "stage": "4. Infographic & SGK (15')",
        "color": "red",
        "desc": "Tổng kết 4 chế độ Infographic, Flashcards & chữa LT1, LT2 (Trời Hà Nội xanh)."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "TYPOGRAPHY TRONG THIẾT KẾ WEB",
    "subtitle": "Chữ dễ đọc, bố cục thoáng sẽ giữ chân người xem lâu hơn",
    "theme": "blue",
    "pills": [
      [
        "Phông chữ phù hợp",
        "Chọn họ phông chuẩn (sans-serif cho màn hình, monospace cho code).",
        "blue"
      ],
      [
        "Nhịp điệu dòng",
        "Giãn dòng line-height và căn lề text-align hài hòa.",
        "emerald"
      ],
      [
        "Kế thừa thông minh",
        "Đặt ở body/div cha để toàn trang tự đồng bộ.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • HỌ PHÔNG CHỮ",
    "title": "5 HỌ PHÔNG CHỮ CƠ BẢN (FONT-FAMILY)",
    "sub": "SGK Tin học 12 – Trang 76 (Hình 14.1)",
    "theme": "blue",
    "heading": "🔤 Đặc điểm 5 họ phông CSS:",
    "bullets": [
      "serif: có chân (Times New Roman, Georgia) -> hợp văn bản dài.",
      "sans-serif: không chân (Arial, Roboto) -> rõ nét trên màn hình.",
      "monospace: độ rộng ký tự đều (Consolas) -> dùng hiển thị code.",
      "cursive / fantasy: chữ viết tay / trang trí nghệ thuật.",
      "Tên phông có dấu cách phải đặt trong nháy kép: \"Times New Roman\"."
    ],
    "image": "sgk_hinh14_1.png",
    "caption": "Hình 14.1. Năm họ phông chữ cơ bản trong CSS (SGK tr.76)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • ĐƠN VỊ CỠ CHỮ",
    "title": "CỠ CHỮ (FONT-SIZE) VÀ ĐƠN VỊ ĐO",
    "sub": "SGK Tin học 12 – Trang 77 (Hình 14.2)",
    "theme": "emerald",
    "heading": "📏 Phân nhóm đơn vị tuyệt đối & tương đối:",
    "bullets": [
      "Tuyệt đối: px (= 1/96 inch), pt (= 1/72 inch), cm, mm, in.",
      "Tương đối: em (so với cha), rem (so với html gốc), %.",
      "Từ khóa: xx-small, small, medium (mặc định), large, xx-large.",
      "Mẹo thi: 1pt lớn hơn 1px (vì 1/72 > 1/96)."
    ],
    "image": "sgk_hinh14_2.png",
    "caption": "Hình 14.2. Các loại đơn vị kích thước chữ (SGK tr.77)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • KIỂU & ĐỘ DÀY CHỮ",
    "title": "FONT-STYLE, FONT-WEIGHT VÀ COLOR",
    "sub": "SGK Tin học 12 – Trang 77 (Hình 14.3)",
    "theme": "blue",
    "heading": "✒️ Lưu ý giá trị chuẩn trong CSS3:",
    "bullets": [
      "font-style: normal (thường), italic (nghiêng), oblique.",
      "CHÚ Ý: Chuẩn CSS viết italic (không có chữ 's' ở cuối!).",
      "font-weight: normal (=400), bold (=700), hoặc 100..900.",
      "Từ mức 500 trở lên hiển thị chữ in đậm (theo chuẩn SGK)."
    ],
    "image": "sgk_hinh14_3.png",
    "caption": "Hình 14.3. Kết quả áp dụng kiểu chữ & độ dày nét chữ (SGK tr.77)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • MÃ MẪU PHÔNG CHỮ",
    "title": "KHAI BÁO FONT DỰ PHÒNG AN TOÀN",
    "sub": "Thực hành viết nhiều tên phông cách nhau bằng dấu phẩy",
    "theme": "emerald",
    "filename": "fonts.css",
    "code": "h1 {\n  font-family: \"Segoe UI\", Arial, sans-serif;\n  font-size: 24px;\n  font-weight: 700;\n  color: #1e3a8a;\n}\np.note {\n  font-family: \"Courier New\", monospace;\n  font-style: italic;\n}",
    "right_heading": "📌 NGUYÊN TẮC DỰ PHÒNG:",
    "notes": [
      "Trình duyệt thử từng phông từ trái sang phải.",
      "Nếu máy thiếu 'Segoe UI' -> dùng Arial; thiếu tiếp -> lấy sans-serif.",
      "Tên nhiều từ ('Courier New') luôn đặt trong dấu ngoặc kép."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • DÒNG & ƯU TIÊN",
    "title": "ĐỊNH DẠNG DÒNG, KẾ THỪA & CASCADING",
    "subtitle": "Kiểm soát khoảng cách dòng, căn lề và giải quyết xung đột quy tắc CSS",
    "theme": "amber",
    "pills": [
      [
        "Thuộc tính dòng",
        "line-height, text-align, text-decoration, text-indent.",
        "blue"
      ],
      [
        "Tính kế thừa",
        "Thẻ con thừa hưởng font/color; KHÔNG kế thừa text-decoration.",
        "emerald"
      ],
      [
        "Thứ tự ưu tiên",
        "Sau thắng trước • * thấp nhất • !important cao nhất.",
        "red"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • CHIỀU CAO DÒNG",
    "title": "LINE-HEIGHT VÀ ĐƯỜNG CƠ SỞ BASELINE",
    "sub": "SGK Tin học 12 – Trang 78 (Hình 14.4)",
    "theme": "blue",
    "heading": "📐 Khái niệm line-height:",
    "bullets": [
      "Là khoảng cách giữa hai đường cơ sở (baseline) kế tiếp.",
      "Mặc định trình duyệt theo SGK thường là 2em.",
      "Độ cao thoáng dễ đọc thường đặt từ 1.5 đến 1.8 (hoặc 150%)."
    ],
    "image": "sgk_hinh14_4.png",
    "caption": "Hình 14.4. Minh họa line-height trong CSS (SGK tr.78)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • CĂN LỀ, GẠCH CHỮ & THỤT LỀ",
    "title": "TEXT-ALIGN, TEXT-DECORATION & TEXT-INDENT",
    "sub": "SGK Tin học 12 – Trang 78 (Hình 14.5)",
    "theme": "emerald",
    "heading": "📑 3 thuộc tính text-* thông dụng:",
    "bullets": [
      "text-align: left | center | right | justify (căn đều 2 biên).",
      "text-decoration: none (bỏ gạch chân link), underline, overline, line-through.",
      "text-indent: thụt lề dòng đầu tiên (số âm tạo kiểu thụt lồi ra ngoài)."
    ],
    "image": "sgk_hinh14_5.png",
    "caption": "Hình 14.5. Trình bày đoạn văn bản với text-* (SGK tr.78)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.2 • TÍNH KẾ THỪA & CASCADING",
    "title": "AI THẮNG KHI NHIỀU QUY TẮC CSS TRÙNG NHAU?",
    "sub": "SGK Tin học 12 – Trang 79–80 (Trọng tâm đề thi TN THPT)",
    "theme": "red",
    "left": {
      "heading": "🧬 Tính kế thừa (Inheritance)",
      "color": "blue",
      "bullets": [
        "Con tự động nhận font-*, color, line-height, text-align từ cha.",
        "KHÔNG kế thừa: text-decoration, border, background.",
        "Bộ chọn toàn cục * áp dụng tất cả thẻ (ưu tiên THẤP NHẤT)."
      ]
    },
    "right": {
      "heading": "⚖️ Thứ tự ưu tiên (Cascading)",
      "color": "red",
      "bullets": [
        "Cùng mức bộ chọn: quy tắc viết SAU thắng quy tắc TRƯỚC.",
        "Cụ thể hơn thắng chung chung (* < p < Inline).",
        "Từ khóa !important thắng TẤT CẢ (trừ !important sau nó)."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • VÍ DỤ CASCADING SGK",
    "title": "PHÂN TÍCH XUNG ĐỘT MẪU CSS (HÌNH 14.6)",
    "sub": "SGK Tin học 12 – Trang 79",
    "theme": "amber",
    "heading": "⚡ Quy tắc thực thi từ trên xuống dưới:",
    "bullets": [
      "Nếu p { color: red; } đứng trước p { color: blue; } -> chữ màu xanh dương!",
      "Nếu dòng trên ghi p { color: red !important; } -> chữ BẮT BUỘC màu đỏ!",
      "Nên hạn chế lạm dụng !important để CSS dễ bảo trì."
    ],
    "image": "sgk_hinh14_6.png",
    "caption": "Hình 14.6. Minh họa thứ tự áp dụng Cascading trong CSS (SGK tr.79)"
  },
  {
    "kind": "quiz",
    "badge": "KIỂM TRA NHANH 2.2",
    "title": "TÍNH MÀU HIỂN THỊ KHI CÓ CASCADING & !IMPORTANT",
    "sub": "Câu hỏi phân loại cao đề thi Tin học 12",
    "question": "Trong phần <style> viết:\n* { color: gray; }\np { color: blue !important; }\np { color: red; }\nĐoạn văn trong thẻ <p> sẽ có chữ màu gì?",
    "options": [
      "A. gray (xám)",
      "B. blue (xanh lam)",
      "C. red (đỏ)",
      "D. black (màu mặc định)"
    ],
    "answer": [
      "Đáp án đúng: B (blue).",
      "Giải thích: Tuy p { color: red; } viết sau nhưng p { color: blue !important; } mang từ khóa !important có độ ưu tiên cao nhất!"
    ]
  },
  {
    "kind": "section",
    "tag": "NHIỆM VỤ ĐÁNH GIÁ NHANH",
    "title": "PHIẾU BÀI TẬP BÀI 14",
    "subtitle": "Quét QR hoặc truy cập hd2-2.html -> phieu-bai-tap.html (6 câu chuẩn BGD&ĐT)",
    "theme": "blue",
    "pills": [
      [
        "4 Câu MCQ",
        "5 họ phông, đơn vị đo, text-decoration & Cascading.",
        "blue"
      ],
      [
        "2 Câu Đúng/Sai",
        "Đọc hiểu kế thừa HTML-CSS và thứ tự !important.",
        "emerald"
      ],
      [
        "Chấm realtime",
        "Tự động lưu kết quả về bảng điểm Giáo viên.",
        "purple"
      ]
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (35 PHÚT)",
    "title": "ĐỊNH DẠNG BÀI VIẾT 'KĨ THUẬT CHIA ĐỂ TRỊ'",
    "subtitle": "Tự gõ mã tạo Chia_de_tri.html trên phòng thực hành trống hd3.html (SGK tr.80–82)",
    "theme": "purple",
    "pills": [
      [
        "Nhiệm vụ 1",
        "Tạo cấu trúc bài Kĩ thuật chia để trị (h1, h2, p, ul).",
        "blue"
      ],
      [
        "Nhiệm vụ 2",
        "Áp dụng font-family, line-height, text-align, text-indent.",
        "emerald"
      ],
      [
        "Kiểm tra 8 tiêu chí",
        "Đạt đủ 8/8 tick xanh trước khi Nộp bài.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • SẢN PHẨM MẪU NV1",
    "title": "GIAO DIỆN THỰC HÀNH CHIA ĐỂ TRỊ (HÌNH 14.7)",
    "sub": "SGK Tin học 12 – Trang 80",
    "theme": "purple",
    "heading": "📝 Nhiệm vụ 1 cần đạt:",
    "bullets": [
      "Soạn nội dung bài viết 3 bước Chia để trị (Chia -> Trị -> Kết hợp).",
      "Tạo khung <style> trong <head> định dạng tiêu đề & đoạn văn."
    ],
    "image": "sgk_hinh14_7.png",
    "caption": "Hình 14.7. Định dạng văn bản bước đầu trong thực hành Bài 14 (SGK tr.80)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • SẢN PHẨM MẪU NV2",
    "title": "HOÀN THIỆN BỐ CỤC ĐẸP MẮT (HÌNH 14.8)",
    "sub": "SGK Tin học 12 – Trang 81",
    "theme": "emerald",
    "heading": "✨ Tinh chỉnh nâng cao ở Nhiệm vụ 2:",
    "bullets": [
      "Thêm text-indent thụt lề dòng đầu cho các đoạn <p>.",
      "Đặt line-height thoáng mắt (1.5–1.7) và text-align: justify.",
      "Tạo điểm nhấn font-style: italic hoặc màu khác cho ghi chú."
    ],
    "image": "sgk_hinh14_8.png",
    "caption": "Hình 14.8. Kết quả hoàn thiện trang Kĩ thuật chia để trị (SGK tr.81)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 3 • RUBRIC 8 TIÊU CHÍ",
    "title": "KIỂM TRA ĐỦ 8 TIÊU CHÍ CHO CHIA_DE_TRI.HTML",
    "sub": "Rà soát trước khi gửi bài lên máy chủ GV",
    "theme": "blue",
    "left": {
      "heading": "📌 Tiêu chí 1 – 4 (Cấu trúc & Phông)",
      "color": "blue",
      "bullets": [
        "1. Cấu trúc <!DOCTYPE html>, <head>, <body>, <style>.",
        "2. Có nội dung Kĩ thuật chia để trị (h1, h2, p).",
        "3. Có khai báo font-family với họ phông chuẩn.",
        "4. Có font-size và font-weight hoặc font-style: italic."
      ]
    },
    "right": {
      "heading": "📐 Tiêu chí 5 – 8 (Dòng & Căn lề)",
      "color": "emerald",
      "bullets": [
        "5. Có khai báo color tạo màu nhấn tiêu đề/chữ.",
        "6. Có khai báo line-height giãn dòng hợp lý.",
        "7. Có khai báo text-align căn lề (center / justify).",
        "8. Có text-indent hoặc text-decoration."
      ]
    }
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC",
    "title": "3 MẢNH GHÉP ĐỊNH DẠNG VĂN BẢN CSS",
    "sub": "Tổng hợp cô đọng kiến thức Bài 14",
    "theme": "blue",
    "cols": [
      {
        "heading": "Phông chữ (font-*)",
        "color": "blue",
        "subhead": "Nét chữ & Kích thước",
        "bullets": [
          "font-family (5 họ chuẩn)",
          "font-size (px, pt, em, rem)",
          "font-style: italic | normal",
          "font-weight: 500..900 đậm"
        ]
      },
      {
        "heading": "Dòng văn bản (text-*)",
        "color": "emerald",
        "subhead": "Bố cục đoạn văn",
        "bullets": [
          "line-height (giãn dòng)",
          "text-align (left/center/justify)",
          "text-decoration (ko kế thừa!)",
          "text-indent (âm -> thò lề)"
        ]
      },
      {
        "heading": "Quy tắc áp dụng",
        "color": "amber",
        "subhead": "Kế thừa & Cascading",
        "bullets": [
          "Con kế thừa font, color từ cha.",
          "Cùng cấp -> quy tắc sau thắng.",
          "* ưu tiên thấp nhất.",
          "!important ưu tiên cao nhất."
        ]
      }
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 4 • GIẢI LUYỆN TẬP 2 TRANG 82",
    "title": "BÀI TẬP ĐỊNH DẠNG BÀI HÁT 'TRỜI HÀ NỘI XANH'",
    "sub": "SGK Tin học 12 Kết nối tri thức – Trang 82",
    "theme": "emerald",
    "heading": "🎵 Phân tích cách định dạng chuẩn:",
    "bullets": [
      "Tên bài hát <h1>: color xanh lam, text-align: center.",
      "Tác giả (Nhạc sĩ Văn Ký): font-style: italic.",
      "Lời bài hát đặt trong các đoạn <p>: kế thừa font-family từ body/div.",
      "Dùng line-height: 1.7 để từng câu hát tách thoáng rõ ràng."
    ],
    "image": "sgk_lt14_2.png",
    "caption": "Minh họa Luyện tập 2: Trình bày lời bài hát Trời Hà Nội xanh (SGK tr.82)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • GIẢI ĐÁP SGK TRANG 82",
    "title": "ĐÁP ÁN LUYỆN TẬP 1 & VẬN DỤNG 1, 2",
    "sub": "Chốt lại kiến thức trọng tâm cuối bài",
    "theme": "blue",
    "left": {
      "heading": "✏️ Luyện tập 1 (Trang 82)",
      "color": "blue",
      "bullets": [
        "Xác định màu khi nhiều quy tắc trùng bộ chọn: áp dụng mẫu định dạng xuất hiện SAU CÙNG.",
        "Nếu quy tắc ở trên có !important thì được ưu tiên cao nhất, bất chấp vị trí sau."
      ]
    },
    "right": {
      "heading": "🚀 Vận dụng 1 & 2 (Trang 82)",
      "color": "emerald",
      "bullets": [
        "VD1: Trích bài thơ/bài văn dùng text-indent và font-family.",
        "VD2: Nâng cấp dự án website CLB thêm tệp CSS chuẩn font chữ, giãn dòng & màu tiêu đề."
      ]
    }
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP CHUẨN TN THPT",
    "title": "TỔNG ÔN KẾ THỪA & KHÔNG KẾ THỪA",
    "sub": "Phân biệt rõ đặc tính của các thuộc tính văn bản",
    "question": "Cho HTML: <div class=\"box\"><p>Tin học 12</p></div> và CSS:\ndiv { font-family: Arial; color: navy; border: 1px solid blue; text-indent: 20px; }",
    "options": [
      "a) Thẻ <p> kế thừa font-family: Arial và color: navy từ thẻ <div>.",
      "b) Thẻ <p> cũng tự động có đường viền riêng giống <div> do kế thừa border.",
      "c) Dòng đầu trong thẻ <p> sẽ thụt lề 20px nhờ kế thừa text-indent.",
      "d) Muốn thẻ <p> màu đỏ dù sau này đổi màu div, viết p { color: red !important; }."
    ],
    "answer": [
      "a) Đúng — font-family và color có tính kế thừa.",
      "b) Sai — border (và text-decoration) KHÔNG kế thừa xuống thẻ con.",
      "c) Đúng — text-indent có tính kế thừa.",
      "d) Đúng — !important bảo vệ độ ưu tiên cao nhất."
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 14: ĐỊNH DẠNG VĂN BẢN CSS!",
    "takeaways": [
      "Thuộc lòng 5 họ phông chữ, cách dùng font-style: italic, font-weight >= 500 để in đậm.",
      "Nhớ text-decoration KHÔNG kế thừa; Cascading viết sau thắng trước; !important cao nhất.",
      "Chuẩn bị cho Bài 15 (Tuần 18 - Tiết cuối HK1): Hệ màu RGB/HSL, border và Bộ chọn tổ hợp!"
    ]
  }
]
LESSON_SHORT = "Bài 14: Định dạng văn bản bằng CSS"
OUT_PPTX_NAME = "Bai14_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
