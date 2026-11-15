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
    "pill": "TIN HỌC 12 • KẾT NỐI TRI THỨC • ÔN TẬP HỌC KÌ I",
    "title": "ÔN TẬP HỌC KỲ 1 & ĐỀ THI THỬ CUỐI HK1",
    "subtitle": "Tổng hợp trọn bộ Chủ đề A (AI), B (Mạng), D (Đạo đức số), F (HTML5) & Đề thi thử 45 phút (28 câu)",
    "meta": "Tiết 29–30 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/OnTap_HK1/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU ÔN TẬP HỌC KỲ 1",
    "sub": "Chuẩn bị toàn diện về kiến thức và kỹ năng làm bài thi 45 phút",
    "cards": [
      {
        "heading": "1. Chủ đề A – Trí tuệ nhân tạo",
        "color": "blue",
        "bullets": [
          "5 đặc trưng AI & phân loại AI hẹp vs rộng.",
          "Ứng dụng trong y tế, giáo dục, giao thông.",
          "Cảnh báo thiên lệch, bảo mật & đạo đức AI."
        ]
      },
      {
        "heading": "2. Chủ đề B – Mạng máy tính",
        "color": "emerald",
        "bullets": [
          "Switch, Access Point, Router, Modem.",
          "Giao thức TCP/IP, địa chỉ IPv4, DNS.",
          "Chia sẻ tệp, thư mục & máy in trong LAN."
        ]
      },
      {
        "heading": "3. Chủ đề D – Giao tiếp mạng",
        "color": "amber",
        "bullets": [
          "Tính nhân văn, ứng xử văn minh trực tuyến.",
          "Bảo vệ thông tin cá nhân & quyền tác giả.",
          "Phòng chống tin giả và bắt nạt mạng."
        ]
      },
      {
        "heading": "4. Chủ đề F – HTML5 & Thi thử",
        "color": "purple",
        "bullets": [
          "Thành thạo thẻ từ Bài 7 đến Bài 12.",
          "Đọc hiểu & phát hiện lỗi mã nguồn HTML.",
          "Chinh phục Đề thi thử 28 câu chuẩn BGD&ĐT."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "CẤU TRÚC TIẾT ÔN TẬP & THI THỬ (2 TIẾT)",
    "rows": [
      {
        "stage": "1. Ma trận đề HK1 (5')",
        "color": "blue",
        "desc": "Nắm rõ 24 câu MCQ (6đ) + 4 câu Đúng/Sai chấm phân bậc BGD&ĐT (4đ)."
      },
      {
        "stage": "2.1. Ôn Chủ đề A, B, D (15')",
        "color": "emerald",
        "desc": "Chốt lại lý thuyết AI, thiết bị mạng, giao thức TCP/IP & ứng xử mạng."
      },
      {
        "stage": "2.2. Ôn HTML & Thi 45p (45')",
        "color": "red",
        "desc": "Hệ thống HTML Bài 7–12 & làm Đề thi thử Cuối HK1 trực tuyến (28 câu)."
      },
      {
        "stage": "3. Thực hành kiểm chứng (15')",
        "color": "purple",
        "desc": "Luyện gõ OnTap_HK1.html kiểm chứng trực tiếp các đoạn mã hay ra thi."
      },
      {
        "stage": "4. Chữa câu bẫy (10')",
        "color": "amber",
        "desc": "Tổng kết bằng Infographic 4 trụ cột & phân tích các ý Đúng/Sai dễ nhầm."
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 1 • CẤU TRÚC ĐỀ THI CHUẨN 2025/2026",
    "title": "QUY TẮC TÍNH ĐIỂM & CHIẾN LƯỢC LÀM BÀI",
    "sub": "Định hướng đề kiểm tra định kỳ và Tốt nghiệp THPT môn Tin học",
    "theme": "blue",
    "left": {
      "heading": "📊 Tỉ trọng điểm số (Tổng 10.0 điểm)",
      "color": "blue",
      "bullets": [
        "Phần I: 24 câu nhiều lựa chọn × 0.25đ = 6.0 điểm.",
        "Phần II: 4 câu Đúng/Sai × 1.0đ = 4.0 điểm.",
        "Mỗi câu Đ/S: đúng 1 ý = 0.1đ; đúng 2 ý = 0.25đ;",
        "Đúng 3 ý = 0.50đ; đúng cả 4 ý = 1.00 điểm!"
      ]
    },
    "right": {
      "heading": "⏱️ Phân bổ 45 phút thông minh",
      "color": "emerald",
      "bullets": [
        "18–20 phút đầu: Giải quyết gọn 24 câu Phần I.",
        "20 phút tiếp theo: Đọc thật kỹ từng dòng Phần II Đ/S.",
        "Cẩn trọng từng thuộc tính nhỏ trong câu đọc hiểu code.",
        "5 phút cuối: Rà soát lại toàn bộ phiếu trước khi Nộp."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "PHẦN 1 • CHỦ ĐỀ A",
    "title": "TRÍ TUỆ NHÂN TẠO (BÀI 1 & BÀI 2)",
    "subtitle": "Khả năng, Ứng dụng thực tế và Cảnh báo đạo đức trong kỷ nguyên AI",
    "theme": "blue",
    "pills": [
      [
        "5 Khả năng đặc trưng",
        "Học, suy luận, nhận thức môi trường, hiểu ngôn ngữ, giải quyết vấn đề.",
        "blue"
      ],
      [
        "AI Hẹp vs AI Tổng quát",
        "AI hiện nay là AI hẹp (chuyên biệt từng tác vụ).",
        "emerald"
      ],
      [
        "Rủi ro & Trách nhiệm",
        "Deepfake, lộ dữ liệu riêng tư, thiên lệch dữ liệu.",
        "red"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "ÔN TẬP CHỦ ĐỀ A • AI",
    "title": "TRỌNG TÂM BÀI 1 & BÀI 2 CẦN NHỚ",
    "sub": "Những điểm hay xuất hiện trong câu MCQ và Đúng/Sai",
    "theme": "blue",
    "left": {
      "heading": "🤖 Khái niệm & Ứng dụng AI",
      "color": "blue",
      "bullets": [
        "AI giúp máy móc thực hiện công việc đòi hỏi trí tuệ con người.",
        "Học máy (Machine Learning) trích xuất tri thức từ dữ liệu lớn.",
        "Y tế: chẩn đoán ảnh X-quang; Giáo dục: gia sư ảo, cá nhân hóa.",
        "Giao thông: xe tự hành nhận diện biển báo, vật cản."
      ]
    },
    "right": {
      "heading": "⚠️ Cảnh báo & Sử dụng AI có trách nhiệm",
      "color": "amber",
      "bullets": [
        "AI có thể 'ảo giác' (tạo thông tin sai nhưng nghe rất thuyết phục).",
        "Nguy cơ mất việc làm lặp lại và xâm phạm bản quyền tác giả.",
        "Deepfake giả mạo giọng nói, khuôn mặt để lừa đảo trực tuyến.",
        "Con người luôn phải kiểm chứng và chịu trách nhiệm cuối cùng."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "PHẦN 2 • CHỦ ĐỀ B",
    "title": "MẠNG MÁY TÍNH & GIAO THỨC (BÀI 3 – 5)",
    "subtitle": "Thiết bị kết nối mạng, giao thức TCP/IP và thực hành kết nối chia sẻ tài nguyên",
    "theme": "emerald",
    "pills": [
      [
        "Thiết bị nội bộ LAN",
        "Switch (có dây), Access Point (Wi-Fi) nối thiết bị cùng mạng.",
        "blue"
      ],
      [
        "Kết nối liên mạng",
        "Router định tuyến IP; Modem điều chế tín hiệu nhà mạng.",
        "emerald"
      ],
      [
        "Giao thức & Tài nguyên",
        "IP định danh địa chỉ; TCP truyền tin cậy; chia sẻ tệp/máy in.",
        "purple"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "ÔN TẬP CHỦ ĐỀ B • THIẾT BỊ MẠNG",
    "title": "PHÂN BIỆT SWITCH, ACCESS POINT, ROUTER, MODEM",
    "sub": "Bảng đối chiếu chức năng cốt lõi (Bài 3 SGK)",
    "theme": "emerald",
    "left": {
      "heading": "🔌 Hub / Switch & Access Point",
      "color": "blue",
      "bullets": [
        "Hub phát tín hiệu đến MỌI cổng -> dễ xung đột mạng.",
        "Switch dùng bảng địa chỉ MAC gửi đúng cổng đích -> giảm nghẽn.",
        "Access Point (AP) chuyển kết nối mạng dây thành sóng Wi-Fi.",
        "Cả Switch và AP hoạt động trong phạm vi mạng cục bộ LAN."
      ]
    },
    "right": {
      "heading": "🌐 Router & Modem",
      "color": "emerald",
      "bullets": [
        "Router dùng địa chỉ IP tìm đường đi tối ưu giữa các mạng khác nhau.",
        "Router Wi-Fi gia đình thường tích hợp chức năng của Router + Switch + AP.",
        "Modem chuyển đổi tín hiệu số <-> tín hiệu tương tự/quang từ nhà cung cấp ISP."
      ]
    }
  },
  {
    "kind": "two_col",
    "badge": "ÔN TẬP CHỦ ĐỀ B & D",
    "title": "GIAO THỨC MẠNG & TÍNH NHÂN VĂN KHÔNG GIAN MẠNG",
    "sub": "Trọng tâm Bài 4, 5, 6 SGK Tin học 12",
    "theme": "amber",
    "left": {
      "heading": "📡 Giao thức & Chia sẻ LAN (Bài 4–5)",
      "color": "blue",
      "bullets": [
        "Địa chỉ IPv4 gồm 4 số nguyên 0..255 (vd: 192.168.1.1).",
        "Giao thức IP chịu trách nhiệm định tuyến & gắn địa chỉ gói tin.",
        "TCP kiểm soát truyền tin cậy, chia gói và ghép đủ thứ tự.",
        "Chia sẻ máy in / thư mục LAN giúp tiết kiệm chi phí thiết bị."
      ]
    },
    "right": {
      "heading": "🤝 Đạo đức & Văn hóa số (Bài 6)",
      "color": "emerald",
      "bullets": [
        "Tôn trọng quyền riêng tư, không tung ảnh/tin chưa xin phép.",
        "Ứng xử lịch sự, đồng cảm; không tham gia bắt nạt mạng.",
        "Kiểm chứng nguồn tin, không lan truyền tin giả (Fake News).",
        "Cảnh giác lừa đảo (Phishing) mạo danh người thân, ngân hàng."
      ]
    }
  },
  {
    "kind": "section",
    "tag": "PHẦN 3 • CHỦ ĐỀ F",
    "title": "TỔNG ÔN THIẾT KẾ WEB HTML5 (BÀI 7 – 12)",
    "subtitle": "Chuẩn hóa từng thẻ, từng thuộc tính phục vụ 12 MCQ + 2 câu Đúng/Sai HTML",
    "theme": "purple",
    "pills": [
      [
        "Bài 7 – 9",
        "Cấu trúc trang, định dạng chữ, danh sách & bảng rowspan/colspan.",
        "blue"
      ],
      [
        "Bài 10 – 11",
        "Siêu liên kết (../, #id), ảnh tỉ lệ, audio/video/source, iframe.",
        "emerald"
      ],
      [
        "Bài 12",
        "Biểu mẫu <form>, <label for>, Bảng 12.1 <input>, <select>, <fieldset>.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "ÔN TẬP CHỦ ĐỀ F • BÀI 7–9",
    "title": "CẤU TRÚC, VĂN BẢN, DANH SÁCH & BẢNG",
    "sub": "Rà soát kiến thức HTML nền tảng",
    "theme": "blue",
    "left": {
      "heading": "📄 Cấu trúc & Danh sách",
      "color": "blue",
      "bullets": [
        "<!DOCTYPE html> khai báo chuẩn HTML5; UTF-8 đặt ở <meta> trong <head>.",
        "<strong> và <em> thay cho <b>/<i> để chuẩn ngữ nghĩa.",
        "<ol type='1|a|A|i|I' start='n'> đánh số thứ tự.",
        "<ul> danh sách không thứ tự; <dl><dt><dd> mô tả thuật ngữ."
      ]
    },
    "right": {
      "heading": "📊 Bảng dữ liệu <table>",
      "color": "emerald",
      "bullets": [
        "<caption> đặt ngay sau <table> để làm tiêu đề bảng.",
        "<th> tạo ô tiêu đề: mặc định chữ IN ĐẬM và CĂN GIỮA.",
        "colspan=\"n\": gộp ngang n cột; xóa (n-1) ô cùng hàng.",
        "rowspan=\"n\": gộp dọc n hàng; xóa 1 ô ở (n-1) hàng tiếp theo."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "ÔN TẬP CHỦ ĐỀ F • BÀI 10",
    "title": "SIÊU LIÊN KẾT & ĐƯỜNG DẪN THƯ MỤC",
    "sub": "Phân biệt tuyệt đối, tương đối và neo #id",
    "theme": "emerald",
    "heading": "🔗 Quy tắc viết href chuẩn xác:",
    "bullets": [
      "URL ngoài: https://... (nên kèm target=\"_blank\").",
      "Vào thư mục con: sub/file.html; Lên cha: ../file.html.",
      "Neo cùng trang: gắn id=\"x\" ở đích và viết href=\"#x\".",
      "Ảnh bấm được: đặt <img> nằm trong cặp <a>...</a>."
    ],
    "image": "sgk_hinh10_1.png",
    "caption": "Ôn tập sơ đồ đường dẫn website (SGK Bài 10)"
  },
  {
    "kind": "image_focus",
    "badge": "ÔN TẬP CHỦ ĐỀ F • BÀI 11",
    "title": "ĐA PHƯƠNG TIỆN & KHUNG <IFRAME>",
    "sub": "Tính tỉ lệ ảnh và phân biệt <audio> với <video>",
    "theme": "blue",
    "heading": "🎬 Nhớ nhanh 4 ý cốt lõi Bài 11:",
    "bullets": [
      "<img> chỉ đặt 1 chiều width/height -> chiều kia tự giữ tỉ lệ!",
      "Chỉ <video> có width, height, poster; <audio> KHÔNG có.",
      "<source> khai báo nhiều nguồn phát dự phòng.",
      "<a target=\"ten\"> mở trang vào <iframe name=\"ten\">."
    ],
    "image": "sgk_hinh11_1.png",
    "caption": "Các định dạng ảnh và thuộc tính thẻ <img> (SGK Bài 11)"
  },
  {
    "kind": "image_focus",
    "badge": "ÔN TẬP CHỦ ĐỀ F • BÀI 12",
    "title": "BẢNG TỔNG HỢP PHẦN TỬ BIỂU MẪU",
    "sub": "Bảng 12.1 & Cấu trúc <form>, <fieldset>, <select>",
    "theme": "purple",
    "heading": "📝 Điểm trọng tâm về Biểu mẫu:",
    "bullets": [
      "<label for=\"id_o\"> nối tới ô nhập có cùng id.",
      "radio chọn 1 phương án -> Bắt buộc cùng thuộc tính name.",
      "checkbox cho phép tích chọn nhiều phương án cùng lúc.",
      "<select><option> danh sách thả xuống; <textarea> nhiều dòng."
    ],
    "image": "sgk_bang12_1.png",
    "caption": "Bảng 12.1. Các kiểu phần tử <input> thông dụng (SGK Bài 12)"
  },
  {
    "kind": "section",
    "tag": "CHỈNH ĐỐN LỖI HAY GẶP • CHUẨN BỊ THI THỬ",
    "title": "ĐỀ THI THỬ CUỐI HỌC KỲ 1 (45 PHÚT)",
    "subtitle": "Truy cập phieu-bai-tap.html (hoặc quét QR ở HĐ 2.2) • 28 câu chuẩn BGD&ĐT = 10.0 điểm",
    "theme": "red",
    "pills": [
      [
        "24 Câu MCQ (6.0đ)",
        "Phủ AI (4), Mạng (5), Đạo đức (3), HTML (12).",
        "blue"
      ],
      [
        "4 Câu Đúng/Sai (4.0đ)",
        "Chấm phân bậc BGD&ĐT 10% – 25% – 50% – 100%.",
        "emerald"
      ],
      [
        "45 Phút đếm ngược",
        "Chấm điểm & hiện giải thích ngay khi nộp bài.",
        "red"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "GIẢI MẪU CÂU HỎI CHỦ ĐỀ B",
    "title": "CÂU HỎI TÌNH HUỐNG THIẾT BỊ MẠNG",
    "sub": "Trích dạng Đúng/Sai Đề minh họa BGD&ĐT",
    "question": "Một phòng thực hành Tin học có 24 máy tính bàn kết nối dây qua một Switch, và Switch này nối vào Router có đường truyền cáp quang qua Modem ra Internet:",
    "options": [
      "a) Switch giúp các máy tính trong phòng trao đổi tệp nội bộ với nhau.",
      "b) Để lắp thêm Wi-Fi cho giáo viên dùng laptop trong phòng có thể cắm thêm Access Point vào Switch.",
      "c) Router thực hiện định tuyến gói tin giữa mạng LAN phòng máy với Internet theo địa chỉ MAC.",
      "d) Các máy trong cùng phòng LAN muốn in chung 1 máy in cắm vào máy chủ chỉ cần bật chia sẻ máy in."
    ],
    "answer": [
      "a) Đúng — Switch kết nối máy trong LAN.",
      "b) Đúng — Access Point mở rộng kết nối Wi-Fi cho LAN.",
      "c) Sai — Router định tuyến giữa các mạng dựa trên địa chỉ IP (Switch mới dùng MAC).",
      "d) Đúng — Cho phép chia sẻ thiết bị ngoại vi qua LAN."
    ]
  },
  {
    "kind": "quiz",
    "badge": "GIẢI MẪU CÂU HỎI CHỦ ĐỀ F",
    "title": "ĐỌC HIỂU MÃ NGUỒN BẢNG, MEDIA & FORM",
    "sub": "Phân tích kỹ từng thuộc tính trước khi chọn Đúng / Sai",
    "question": "Cho mã: <table border=\"1\"><tr><th>Môn</th><th>Điểm</th></tr><tr><td>Tin</td><td>10</td></tr></table> <img src=\"a.jpg\" width=\"400\"> (ảnh gốc 800x600).",
    "options": [
      "a) Hàng đầu của bảng hiển thị chữ 'Môn' và 'Điểm' in đậm, căn giữa.",
      "b) Thẻ <td> hiển thị chữ in đậm mặc định giống thẻ <th>.",
      "c) Chiều cao hiển thị thực tế của bức ảnh trên là 300 px.",
      "d) Thêm alt=\"Ảnh minh họa\" vào thẻ <img> giúp tăng tính trợ năng."
    ],
    "answer": [
      "a) Đúng — <th> mặc định in đậm, căn giữa.",
      "b) Sai — <td> hiển thị chữ thường, căn lề trái.",
      "c) Đúng — giữ đúng tỉ lệ: 400 × 600 / 800 = 300 px.",
      "d) Đúng — alt hiển thị thay thế khi ảnh lỗi & hỗ trợ đọc màn hình."
    ]
  },
  {
    "kind": "code_result",
    "badge": "HĐ 3 • KIỂM CHỨNG CODE HTML",
    "title": "LUYỆN VIẾT ĐOẠN MÃ TỔNG HỢP ONTAP_HK1.HTML",
    "sub": "Tự kiểm chứng lại các tình huống hay hỏi trong đề thi trên hd3.html",
    "theme": "purple",
    "filename": "OnTap_HK1.html",
    "code": "<table border=\"1\">\n  <caption>Bảng tổng hợp</caption>\n  <tr><th colspan=\"2\">Thông tin</th></tr>\n  <tr><td>Mã</td><td>12A1</td></tr>\n</table>\n<form>\n  <input type=\"radio\" name=\"gt\"> Nam\n  <input type=\"radio\" name=\"gt\"> Nữ\n  <input type=\"submit\" value=\"Gửi\">\n</form>",
    "right_heading": "🔍 TỰ KIỂM CHỨNG TRÊN IDE:",
    "notes": [
      "Quan sát ngay <th> tự căn giữa trong khi <td> căn trái.",
      "Thử bỏ name=\"gt\" để thấy lỗi chọn cả Nam và Nữ.",
      "Hoàn thành 8/8 tiêu chí trên hd3.html để củng cố thực hành."
    ]
  },
  {
    "kind": "three_col",
    "badge": "HĐ 4 • INFOGRAPHIC TỔNG ÔN HK1",
    "title": "3 TRỤ CỘT KIẾN THỨC CHINH PHỤC ĐIỂM 10",
    "sub": "Tóm tắt cô đọng toàn bộ Học kỳ 1 Tin học 12 KNTT",
    "theme": "emerald",
    "cols": [
      {
        "heading": "AI & Đạo đức số",
        "color": "blue",
        "subhead": "Chủ đề A & D",
        "bullets": [
          "Đặc trưng & ứng dụng AI hẹp.",
          "Kiểm chứng thông tin AI tạo sinh.",
          "Văn minh, tôn trọng bản quyền & dữ liệu."
        ]
      },
      {
        "heading": "Mạng máy tính",
        "color": "emerald",
        "subhead": "Chủ đề B",
        "bullets": [
          "Switch (MAC LAN), AP (Wi-Fi).",
          "Router (IP liên mạng), Modem (ISP).",
          "TCP/IP & chia sẻ máy in/thư mục LAN."
        ]
      },
      {
        "heading": "Thiết kế Web HTML5",
        "color": "amber",
        "subhead": "Chủ đề F (Bài 7–12)",
        "bullets": [
          "<ol>/<ul>, <table> rowspan/colspan.",
          "<a href> (../, #id), <img> đúng tỉ lệ.",
          "<video>/<audio>/<iframe>, <form> chuẩn."
        ]
      }
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • RÚT KINH NGHIỆM SAU THI THỬ",
    "title": "5 LỖI MẤT ĐIỂM OAN CẦN TUYỆT ĐỐI TRÁNH",
    "sub": "Tổng hợp bẫy kinh điển trong đề thi Tin học 12",
    "theme": "red",
    "left": {
      "heading": "🚫 Bẫy Chủ đề A, B, D",
      "color": "red",
      "bullets": [
        "Nhầm Router dùng địa chỉ MAC (đúng: dùng IP!).",
        "Nhầm Switch và Hub (Hub phát mọi cổng, Switch gửi đúng đích).",
        "Tin tuyệt đối kết quả AI mà không kiểm chứng nguồn gốc."
      ]
    },
    "right": {
      "heading": "🚫 Bẫy Chủ đề F (HTML5)",
      "color": "amber",
      "bullets": [
        "Nhầm colspan (ngang) với rowspan (dọc).",
        "Tưởng <audio> có poster/width giống <video>.",
        "Quên radio phải CÙNG name mới chọn được duy nhất 1."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HƯỚNG TỚI CHẶNG CSS (BÀI 13 – 15)",
    "title": "BƯỚC TIẾP THEO SAU KỲ THI HK1: THẾ GIỚI CSS!",
    "sub": "Bài 13, 14, 15 mở ra nghệ thuật tạo kiểu dáng website",
    "theme": "purple",
    "heading": "🎨 Nội dung chặng CSS tiếp theo (Bài 13–15):",
    "bullets": [
      "Bài 13: Khái niệm, vai trò & 3 cách nhúng CSS.",
      "Bài 14: Định dạng chữ (font, line-height, text-align, kế thừa).",
      "Bài 15: Hệ màu RGB/HSL, border và bộ chọn tổ hợp."
    ],
    "image": "sgk_hinh15_tree.png",
    "caption": "Minh họa cây phần tử HTML – Nền tảng cho bộ chọn CSS (Bài 13–15)"
  },
  {
    "kind": "code_result",
    "badge": "BẬT MÍ CSS (BÀI 13)",
    "title": "XEM TRƯỚC SỨC MẠNH CỦA CSS TRÊN TRANG HTML",
    "sub": "Từ trang HTML thô sang giao diện màu sắc, bo góc chuyên nghiệp",
    "theme": "blue",
    "filename": "preview_css.html",
    "code": "<style>\n  h2 { color: #1e3a8a; font-family: sans-serif; }\n  .card { background: #eff6ff; border: 2px solid #2563eb;\n          padding: 12px; border-radius: 10px; }\n</style>\n<div class=\"card\">\n  <h2>Chúc các em thi HK1 đạt điểm 10!</h2>\n  <p>Tách riêng định dạng giúp code sạch và đẹp.</p>\n</div>",
    "right_heading": "✨ CHUẨN BỊ SẴN SÀNG:",
    "notes": [
      "Kiến thức HTML vững vàng là bệ phóng học CSS cực nhanh.",
      "Ôn lại Đề thi thử 28 câu để nắm chắc mọi dạng câu hỏi."
    ]
  },
  {
    "kind": "two_col",
    "badge": "CHECKLIST ÔN THI CUỐI HK1",
    "title": "DANH SÁCH RÀ SOÁT TRƯỚC KHI VÀO PHÒNG THI",
    "sub": "Tự kiểm tra bản thân với 6 câu hỏi ngắn",
    "theme": "emerald",
    "left": {
      "heading": "🧠 Về Lý thuyết (A, B, D)",
      "color": "blue",
      "bullets": [
        "Phân biệt rành mạch 4 thiết bị: Hub, Switch, AP, Router, Modem?",
        "Hiểu vai trò của IP, TCP và chia sẻ máy in qua LAN?",
        "Nhận diện được lợi ích & rủi ro đạo đức của AI/Deepfake?"
      ]
    },
    "right": {
      "heading": "💻 Về Mã nguồn HTML (Chủ đề F)",
      "color": "emerald",
      "bullets": [
        "Tính chuẩn kích thước ảnh co giãn giữ nguyên tỉ lệ?",
        "Viết được đường dẫn tương đối qua nhiều cấp với ../ ?",
        "Nhìn mã biết ngay số hàng/cột bảng gộp ô và lỗi form radio?"
      ]
    }
  },
  {
    "kind": "thank_you",
    "title": "CHÚC CÁC EM THI CUỐI HỌC KỲ 1 ĐẠT KẾT QUẢ CAO!",
    "takeaways": [
      "Đã nắm vững ma trận 28 câu = 10 điểm chuẩn Bộ GD&ĐT (24 MCQ + 4 Đúng/Sai).",
      "Làm lại Đề thi thử 45 phút (phieu-bai-tap.html) đến khi nắm chắc lời giải mọi câu hỏi.",
      "Chuẩn bị cho Bài 13: Khái niệm, vai trò của CSS — mở đầu chặng thiết kế giao diện web!"
    ]
  }
]
LESSON_SHORT = "Ôn tập & Đề thi thử Cuối HK1 (45p)"
OUT_PPTX_NAME = "OnTapHK1_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
