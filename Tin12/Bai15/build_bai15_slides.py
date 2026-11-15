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
    "pill": "TIN HỌC 12 • KNTT • TUẦN 18 (TIẾT 35–36)",
    "title": "BÀI 15: TẠO MÀU CHO CHỮ VÀ NỀN",
    "subtitle": "Hệ màu RGB/Hex & HSL • Đường viền Border • Bộ chọn tổ hợp CSS • Thực hành Loi_ich_CSS.html",
    "meta": "Tuần 18 (Tiết 35–36) • Khép lại Học kì I",
    "url": "https://minda.io.vn/Tin12/Bai15/index.html"
  },
  {
    "kind": "objectives",
    "title": "YÊU CẦU CẦN ĐẠT BÀI 15",
    "sub": "Chuẩn Công văn 5512 & Khung Năng lực số 3.4.NC1.a",
    "cards": [
      {
        "heading": "1. Hệ màu trong CSS",
        "color": "blue",
        "bullets": [
          "Tên màu: 16/17 màu CSS2.1 & 140 màu CSS3.",
          "RGB/Hex: 256^3 = 16.777.216 màu; R=G=B cho 256 xám.",
          "HSL: Hue (0–360°), Saturation (%), Lightness (%)."
        ]
      },
      {
        "heading": "2. Chữ, Nền & Viền",
        "color": "emerald",
        "bullets": [
          "Thuộc tính color (CÓ kế thừa xuống thẻ con).",
          "background-color: tạo màu nền cho vùng/hộp.",
          "border: width style color (KHÔNG kế thừa!)."
        ]
      },
      {
        "heading": "3. Bộ chọn Tổ hợp",
        "color": "amber",
        "bullets": [
          "E F (hậu duệ) vs E > F (con trực tiếp).",
          "E + F (liền kề) vs E ~ F (mọi anh em sau).",
          "Mở rộng tổ hợp 3 phần tử E1 E2 E3, E > F + G."
        ]
      },
      {
        "heading": "4. Thực hành & NLS",
        "color": "purple",
        "bullets": [
          "Code Loi_ich_CSS.html chuẩn SGK tr.87–88.",
          "Giải LT1–2 (cây DOM) & VD1–2 tr.88.",
          "Năng lực số 3.4.NC1.a phối màu tương phản."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "LỘ TRÌNH 4 HOẠT ĐỘNG BÀI 15 (2 TIẾT)",
    "rows": [
      {
        "stage": "1. Khởi động (5')",
        "color": "blue",
        "desc": "So sánh trang đen trắng thô vs trang phối màu nền, chữ & viền CSS."
      },
      {
        "stage": "2.1. Hệ màu CSS (20')",
        "color": "emerald",
        "desc": "Tên màu (17/140), RGB/Hex (16,7M; 256 xám) & vòng màu HSL (0–360°)."
      },
      {
        "stage": "2.2. Nền & Tổ hợp (15')",
        "color": "amber",
        "desc": "border không kế thừa, 4 tổ hợp Bảng 15.1 (E F, E>F, E+F, E~F) & Phiếu BT QR."
      },
      {
        "stage": "3. Thực hành (35')",
        "color": "red",
        "desc": "Tự gõ mã tạo Loi_ich_CSS.html đạt 8/8 tiêu chí và nộp về máy chủ GV."
      },
      {
        "stage": "4. Tổng kết SGK (15')",
        "color": "purple",
        "desc": "AntV Infographic 4 chế độ, Flashcards & chữa LT1–2 (cây DOM), VD1–2 tr.88."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG (5 PHÚT)",
    "title": "NGHỆ THUẬT PHỐI MÀU TRÊN TRANG WEB",
    "subtitle": "Tại sao cần quy chuẩn hệ màu số và bộ chọn theo cấu trúc cây thẻ?",
    "theme": "blue",
    "pills": [
      [
        "Màu sắc",
        "Tạo phân cấp thị giác, dẫn dắt mắt người đọc.",
        "blue"
      ],
      [
        "Tương phản",
        "Chữ – nền đủ tương phản giúp bảo vệ mắt (3.4.NC1.a).",
        "emerald"
      ],
      [
        "Tổ hợp CSS",
        "Định dạng theo vị trí cây DOM không cần rải nhiều class.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 1 • QUAN SÁT THỰC TẾ",
    "title": "TỪ VĂN BẢN THÔ ĐẾN GIAO DIỆN ĐA SẮC",
    "sub": "Đặt vấn đề cho bài toán Loi_ich_CSS.html (SGK tr.87)",
    "left": {
      "heading": "⚠️ Trang chỉ dùng HTML thuần",
      "color": "red",
      "bullets": [
        "Nền trắng toàn trang, chữ đen đơn điệu.",
        "Khó phân tách đâu là hộp ghi chú hay tiêu đề mục.",
        "Không có viền khung tạo điểm nhấn cho vùng trọng tâm."
      ]
    },
    "right": {
      "heading": "✅ Trang áp dụng CSS Bài 15",
      "color": "emerald",
      "bullets": [
        "Nền dịu nhẹ (background-color), tiêu đề chữ đậm sắc nét.",
        "Đường viền border phân tách rạch ròi từng khối lợi ích.",
        "Dùng h2 + p tự động tạo điểm nhấn riêng đoạn văn đầu sau tiêu đề!"
      ]
    }
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.1 • HỆ MÀU TRONG CSS",
    "title": "3 CÁCH THIẾT LẬP MÀU SẮC TRONG CSS",
    "subtitle": "Tên màu chuẩn tiếng Anh • Hệ màu RGB / Hex • Hệ màu HSL",
    "theme": "emerald",
    "pills": [
      [
        "Tên màu",
        "16/17 màu CSS2.1 & 140 màu chuẩn CSS3.",
        "blue"
      ],
      [
        "RGB / Hex",
        "256^3 = 16.777.216 màu; R=G=B cho 256 sắc xám.",
        "emerald"
      ],
      [
        "HSL",
        "Hue (0–360°), Saturation (%), Lightness (%).",
        "amber"
      ]
    ]
  },
  {
    "kind": "three_col",
    "badge": "HĐ 2.1 • TỔNG QUAN 3 CÁCH GHI MÀU",
    "title": "SO SÁNH CÚ PHÁP TẠO CÙNG MỘT MÀU ĐỎ",
    "sub": "SGK Tin học 12 – Trang 83–84",
    "cols": [
      {
        "heading": "1. Tên màu tiếng Anh",
        "color": "blue",
        "subhead": "Chuẩn từ khóa CSS",
        "bullets": [
          "Ghi trực tiếp tên màu: red, blue, navy, orange...",
          "CSS2.1 định nghĩa 16 màu cơ bản + orange = 17 màu.",
          "CSS3 hỗ trợ tới 140 tên màu chuẩn quốc tế."
        ]
      },
      {
        "heading": "2. Hệ màu RGB & Hex",
        "color": "emerald",
        "subhead": "256 × 256 × 256 màu",
        "bullets": [
          "rgb(r, g, b): mỗi kênh từ 0 đến 255.",
          "Tổng số màu: 256^3 = 16.777.216 màu.",
          "Dạng Hex: #ff0000 (Đỏ), #00ff00 (Lục)."
        ]
      },
      {
        "heading": "3. Hệ màu HSL",
        "color": "amber",
        "subhead": "Hue • Sat • Light",
        "bullets": [
          "hsl(H, S%, L%): rất dễ chỉnh đậm nhạt.",
          "Đỏ chuẩn = hsl(0, 100%, 50%).",
          "Hết sức trực quan cho người thiết kế UI!"
        ]
      }
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • HỆ MÀU RGB",
    "title": "HỆ MÀU CỘNG RGB & THANG MÀU XÁM",
    "sub": "SGK Tin học 12 – Trang 83 (Hình 15.1)",
    "theme": "blue",
    "heading": "🖥️ Nguyên lý pha trộn 3 màu cơ bản R-G-B:",
    "bullets": [
      "rgb(255, 255, 255) = Trắng | rgb(0, 0, 0) = Đen.",
      "Khi R = G = B (từ 0 đến 255): tạo đúng 256 sắc độ màu Xám.",
      "Mã Hex viết tắt #rrggbb dùng cơ số 16 (0..9, a..f).",
      "Ví dụ: #1e3a8a (Xanh navy đậm), #ffffff (Trắng)."
    ],
    "image": "sgk_hinh15_1.png",
    "caption": "Hình 15.1. Biểu diễn màu sắc theo hệ RGB và giá trị thập lục phân (SGK tr.83)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • HỆ MÀU HSL",
    "title": "VÒNG MÀU HSL: HUE • SATURATION • LIGHTNESS",
    "sub": "SGK Tin học 12 – Trang 84 (Hình 15.2)",
    "theme": "emerald",
    "heading": "🎡 Thuộc lòng 6 mốc góc màu Hue (0°–360°):",
    "bullets": [
      "Hue (Vùng màu): 0°/360° Đỏ • 60° Vàng • 120° Lục.",
      "180° Xanh lơ (Cyan) • 240° Lam (Blue) • 300° Tím (Magenta).",
      "Saturation (Độ bão hòa): 0% là xám xịt, 100% là rực rỡ nhất.",
      "Lightness (Độ sáng): 0% đen tuyền, 50% chuẩn, 100% trắng tinh."
    ],
    "image": "sgk_hinh15_2.png",
    "caption": "Hình 15.2. Vòng tròn sắc màu Hue và tỉ lệ S, L trong hệ HSL (SGK tr.84)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • VÍ DỤ MINH HỌA MÀU",
    "title": "ỨNG DỤNG MÀU RGB / HSL VÀO THẺ HTML",
    "sub": "SGK Tin học 12 – Trang 84 (Hình 15.3)",
    "theme": "amber",
    "heading": "🎨 Lưu ý khi chọn bảng màu giao diện:",
    "bullets": [
      "Ưu tiên HSL khi muốn làm một tông màu nhạt/đậm đồng bộ.",
      "Giữ nguyên Hue và S, chỉ tăng/giảm Lightness (30% -> 85%).",
      "Luôn kiểm tra độ tương phản giữa màu chữ và màu nền."
    ],
    "image": "sgk_hinh15_3.png",
    "caption": "Hình 15.3. Minh họa hiển thị màu chữ và nền theo các hệ màu CSS (SGK tr.84)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.1 • MÃ MẪU PHỐI MÀU",
    "title": "ĐỒNG BỘ TÔNG MÀU BẰNG HSL & HEX",
    "sub": "Tạo biến thể sáng/tối từ cùng góc màu Hue = 220° (Xanh dương)",
    "theme": "blue",
    "filename": "palette.css",
    "code": ".box-light {\n  background-color: hsl(220, 90%, 95%);\n  color: hsl(220, 80%, 25%);\n  border: 2px solid #2563eb;\n}\n.gray-note {\n  color: rgb(100, 100, 100);\n}",
    "right_heading": "💡 MẸO HAY TỪ HSL:",
    "notes": [
      "Cùng Hue=220°: L=95% cho nền pastel dịu, L=25% cho chữ đậm!",
      ".gray-note có R = G = B = 100 nên chắc chắn ra màu xám trung tính."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • NỀN, VIỀN & TỔ HỢP",
    "title": "COLOR, BACKGROUND-COLOR, BORDER & TỔ HỢP",
    "subtitle": "Hiểu sâu tính kế thừa của viền và cách nhắm mục tiêu theo cây DOM",
    "theme": "amber",
    "pills": [
      [
        "color",
        "Có tính kế thừa xuống mọi thẻ con/cháu.",
        "blue"
      ],
      [
        "border",
        "KHÔNG có tính kế thừa xuống thẻ con!",
        "red"
      ],
      [
        "4 Tổ hợp",
        "E F  |  E > F  |  E + F  |  E ~ F",
        "emerald"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • TÍNH KẾ THỪA MÀU & VIỀN",
    "title": "COLOR, BACKGROUND-COLOR VÀ BORDER",
    "sub": "SGK Tin học 12 – Trang 85 (Hình 15.4)",
    "theme": "red",
    "heading": "📌 Bẫy kiến thức rất hay gặp trong đề thi:",
    "bullets": [
      "color: màu chữ CÓ tính kế thừa xuống phần tử bên trong.",
      "background-color: mặc định phần tử con trong suốt nên hiện nền cha.",
      "border: width style color (vd: 2px solid red) tạo khung viền.",
      "CHÚ Ý: Thuộc tính border KHÔNG có tính kế thừa xuống phần tử con!"
    ],
    "image": "sgk_hinh15_4.png",
    "caption": "Hình 15.4. Minh họa áp dụng color, background-color và border không kế thừa (SGK tr.85)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • BẢNG 15.1 CHUẨN SGK",
    "title": "4 BỘ CHỌN TỔ HỢP PHẦN TỬ (COMBINATORS)",
    "sub": "SGK Tin học 12 – Trang 86 (Bảng 15.1)",
    "theme": "blue",
    "heading": "🧬 Giải mã 4 phép tổ hợp kinh điển:",
    "bullets": [
      "E F (khoảng trắng): Mọi thẻ F nằm TRONG E (bất kể sâu mấy cấp).",
      "E > F (dấu lớn hơn): Chỉ chọn F là CON TRỰC TIẾP của E.",
      "E + F (dấu cộng): Chỉ chọn 1 thẻ F đứng NGAY SAU E (cùng cha).",
      "E ~ F (dấu ngã): Chọn MỌI thẻ F đứng SAU E (cùng cha)."
    ],
    "image": "sgk_bang15_1.png",
    "caption": "Bảng 15.1. Ý nghĩa các bộ chọn là tổ hợp các phần tử trong CSS (SGK tr.86)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • HẬU DUỆ VS CON TRỰC TIẾP",
    "title": "PHÂN BIỆT CHẶT CHẼ E F VÀ E > F",
    "sub": "SGK Tin học 12 – Trang 86 (Hình 15.5)",
    "theme": "emerald",
    "heading": "🌳 So sánh trên cây phân cấp HTML:",
    "bullets": [
      "div p -> chọn cả thẻ <p> con trực tiếp LẪN thẻ <p> nằm trong <section>.",
      "div > p -> CHỈ chọn thẻ <p> nằm ngay dưới <div> (bỏ qua cháu).",
      "Tương tự E1 E2 E3 là lồng sâu 3 cấp bất kỳ; E1 > E2 > E3 bắt buộc cha-con-cháu trực tiếp."
    ],
    "image": "sgk_hinh15_5.png",
    "caption": "Hình 15.5. Phân biệt bộ chọn hậu duệ (E F) và con trực tiếp (E > F) (SGK tr.86)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • ANH CHỊ EM CÙNG CHA",
    "title": "PHÂN BIỆT LIỀN KỀ E + F VÀ TỔNG QUÁT E ~ F",
    "sub": "SGK Tin học 12 – Trang 86 (Hình 15.6)",
    "theme": "amber",
    "heading": "👫 Điều kiện bắt buộc: CÙNG PHẦN TỬ CHA:",
    "bullets": [
      "h2 + p: Chỉ tác động lên thẻ <p> ĐẦU TIÊN đứng sát ngay dưới <h2>.",
      "Nếu giữa h2 và p có xen <div> thì h2 + p KHÔNG chọn được <p> đó!",
      "h2 ~ p: Chọn TẤT CẢ thẻ <p> phía dưới cùng cha với <h2>."
    ],
    "image": "sgk_hinh15_6.png",
    "caption": "Hình 15.6. Phân biệt bộ chọn anh em liền kề E + F và tổng quát E ~ F (SGK tr.86)"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 2.2 • CODE MẪU TỔ HỢP",
    "title": "VÍ DỤ THỰC CHIẾN BỘ CHỌN TỔ HỢP",
    "sub": "Áp dụng màu sắc chính xác không cần thêm nhiều class",
    "theme": "emerald",
    "filename": "combinators.html",
    "code": "<style>\n  .card > h3 { color: #1e3a8a; border-left: 4px solid #2563eb; }\n  h3 + p { color: #b91c1c; font-weight: 700; }\n  h3 ~ p { background-color: #f8fafc; }\n</style>\n<div class=\"card\">\n  <h3>Thông báo</h3>\n  <p>Đoạn 1: Chọn bởi cả h3 + p và h3 ~ p</p>\n  <p>Đoạn 2: Chỉ chọn bởi h3 ~ p (màu chữ thường)</p>\n</div>",
    "right_heading": "🔎 PHÂN TÍCH KẾT QUẢ:",
    "notes": [
      "Đoạn 1 nhận chữ đỏ đậm (do h3 + p) VÀ nền xám nhạt (do h3 ~ p).",
      "Đoạn 2 KHÔNG liền kề h3 nên chỉ nhận nền xám nhạt của h3 ~ p.",
      "Viền border-left chỉ gắn ở h3, hoàn toàn không lan xuống <p>."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH PHÒNG MÁY (35 PHÚT)",
    "title": "DỰ ÁN: LOI_ICH_CSS.HTML (SGK TR.87–88)",
    "subtitle": "Kết hợp hoàn chỉnh hệ màu RGB/HSL/Hex, đường viền và bộ chọn tổ hợp",
    "theme": "red",
    "pills": [
      [
        "Chuẩn file",
        "Tạo đúng tên tệp Loi_ich_CSS.html trên IDE hd3.html.",
        "blue"
      ],
      [
        "Phối màu + Viền",
        "Dùng background-color, color và border: width style color.",
        "emerald"
      ],
      [
        "Tổ hợp CSS",
        "Áp dụng ít nhất 1 tổ hợp (E > F, E + F hoặc E F) đạt 8/8 tiêu chí.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • ĐỀ BÀI THỰC HÀNH SGK",
    "title": "MỤC TIÊU BÀI THỰC HÀNH LỢI ÍCH CSS",
    "sub": "SGK Tin học 12 – Trang 87–88 (Hình 15.7)",
    "theme": "blue",
    "heading": "🎯 Yêu cầu thiết kế trang Loi_ich_CSS.html:",
    "bullets": [
      "Tiêu đề lớn nêu bật Lợi ích khi viết web bằng CSS.",
      "Các khối hộp trình bày từng lợi ích có màu nền dịu & viền border rõ.",
      "Dùng bộ chọn tổ hợp (như div > h2, h2 + p, ul li) tô màu chữ/nền có chọn lọc.",
      "Tự gõ mã trên IDE trống hd3.html -> đạt 8/8 -> Bấm Nộp bài!"
    ],
    "image": "sgk_hinh15_7.png",
    "caption": "Hình 15.7. Kết quả minh họa trang web Loi_ich_CSS.html (SGK tr.87)"
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 3 • HƯỚNG DẪN NHIỆM VỤ SGK",
    "title": "CHI TIẾT CÁC BƯỚC TRÌNH BÀY (TR.87–88)",
    "sub": "Kiểm tra tự động 8 tiêu chí trước khi nộp lên máy chủ THTH-DHSP",
    "theme": "emerald",
    "heading": "📝 Checklist nhanh cho HS:",
    "bullets": [
      "Khối <body> dùng font không chân dễ đọc và nền nhẹ (#f8fafc).",
      "Mỗi khối .benefit dùng background-color và border: 1px solid #cbd5e1.",
      "Đoạn văn ngay sau h2 dùng h2 + p để làm nổi bật ý tóm tắt."
    ],
    "image": "sgk_th15.png",
    "caption": "Yêu cầu thực hành phối màu và tổ hợp bộ chọn (SGK tr.87–88)"
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 4 • INFOGRAPHIC & CHỮA BÀI SGK",
    "title": "CÂY PHẦN TỬ HTML & TỔNG KẾT HỌC KÌ I",
    "subtitle": "Chữa Luyện tập 1–2 & Vận dụng 1–2 SGK Tin học 12 – Trang 88",
    "theme": "blue",
    "pills": [
      [
        "LT1 (tr.88)",
        "Bảng 17 tên màu chuẩn của CSS2.1.",
        "blue"
      ],
      [
        "LT2 (tr.88)",
        "Đọc cây phân cấp HTML áp dụng E F, E>F, E+F, E~F.",
        "emerald"
      ],
      [
        "VD1–2 (tr.88)",
        "Tổ hợp 3 phần tử & Phối màu Website CLB THTH-DHSP.",
        "amber"
      ]
    ]
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 4 • LUYỆN TẬP 2 (TRANG 88)",
    "title": "ĐỌC CÂY PHẦN TỬ HTML XÁC ĐỊNH BỘ CHỌN",
    "sub": "SGK Tin học 12 – Trang 88",
    "theme": "amber",
    "heading": "🌳 Quy tắc vàng khi đọc cây DOM:",
    "bullets": [
      "Mũi tên từ trên xuống biểu diễn quan hệ CHA -> CON TRỰC TIẾP (>).",
      "Các nút nằm cùng hàng dưới chung một cha là ANH EM (+ và ~).",
      "LT1 ghi nhớ: 16 màu cơ bản + orange = 17 tên màu CSS2.1.",
      "VD1: E1 E2 E3 (hậu duệ 3 cấp), E > F + G (con F của E, rồi chọn G ngay sau F)."
    ],
    "image": "sgk_hinh15_tree.png",
    "caption": "Sơ đồ cây cấu trúc phần tử HTML dùng luyện tập bộ chọn tổ hợp (SGK tr.88)"
  },
  {
    "kind": "quiz",
    "badge": "ÔN TẬP CHUẨN TN THPT",
    "title": "CÂU HỎI TỔNG HỢP BÀI 15",
    "sub": "Kiểm tra nhanh kiến thức Hệ màu, Border và Bộ chọn tổ hợp",
    "question": "Cho đoạn CSS:\ndiv { color: blue; border: 2px solid green; background-color: #f0fdf4; }\ndiv > p + span { color: rgb(255, 0, 0); }\nXét mã: <div><p>A</p><span>B</span><span>C</span></div>",
    "options": [
      "a) Mã màu rgb(255, 0, 0) có giá trị HSL tương đương là hsl(0, 100%, 50%).",
      "b) Thẻ <p> bên trong cũng tự động có đường viền xanh dày 2px nhờ kế thừa từ <div>.",
      "c) Cả thẻ <span>B</span> và <span>C</span> đều hiển thị chữ màu đỏ.",
      "d) Nếu muốn <div> chỉ có màu xám thuần, có thể viết rgb(128, 128, 128)."
    ],
    "answer": [
      "a) Đúng — rgb(255,0,0) = Đỏ thuần = hsl(0, 100%, 50%).",
      "b) Sai — Thuộc tính border KHÔNG có tính kế thừa xuống thẻ con.",
      "c) Sai — Do dùng p + span (liền kề ngay sau p) nên CHỈ <span>B</span> màu đỏ; <span>C</span> giữ màu xanh kế thừa từ div.",
      "d) Đúng — R = G = B luôn cho màu trong thang xám 256 cấp."
    ]
  },
  {
    "kind": "thank_you",
    "title": "CHÚC MỪNG HOÀN THÀNH CHƯƠNG TRÌNH HỌC KÌ I!",
    "takeaways": [
      "Nắm vững 3 cách biểu diễn màu: Tên màu (17/140), RGB/Hex (16,7M; R=G=B ra xám), HSL (0–360°).",
      "Phân biệt rạch ròi 4 bộ chọn tổ hợp (E F, E > F, E + F, E ~ F) & tính không kế thừa của border.",
      "Hoàn chỉnh dự án Website CLB Tin học 12 THTH-DHSP sẵn sàng bứt phá sang Học kì II (CSS Box Model & Bố cục)!"
    ]
  }
]
LESSON_SHORT = "Bài 15: Tạo màu cho chữ và nền"
OUT_PPTX_NAME = "Bai15_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
