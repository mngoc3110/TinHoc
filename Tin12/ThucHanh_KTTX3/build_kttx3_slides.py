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
    "title": "THỰC HÀNH TỔNG HỢP HTML & KIỂM TRA KTTX3",
    "subtitle": "Tổng hợp kiến thức Bài 7–12: Website_CLB.html đa phương tiện + Kiểm tra thường xuyên 3 (15 phút)",
    "meta": "Tiết 27–28 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/ThucHanh_KTTX3/index.html"
  },
  {
    "kind": "objectives",
    "title": "MỤC TIÊU BÀI THỰC HÀNH & ĐÁNH GIÁ KTTX3",
    "sub": "Hoàn thiện chặng HTML5 trước khi sang Ôn thi Cuối HK1",
    "cards": [
      {
        "heading": "1. Tổng ôn Bài 7 – 10",
        "color": "blue",
        "bullets": [
          "Cấu trúc tài liệu, thẻ ngữ nghĩa <strong>/<em>.",
          "Danh sách <ol>/<ul>/<dl> và bảng gộp ô.",
          "Siêu liên kết <a href>, #id, đường dẫn ../."
        ]
      },
      {
        "heading": "2. Tổng ôn Bài 11 – 12",
        "color": "emerald",
        "bullets": [
          "Ảnh <img> đúng tỉ lệ, audio/video/source.",
          "Khung nội tuyến <iframe> điều hướng target.",
          "Biểu mẫu <form>, Bảng 12.1, select, fieldset."
        ]
      },
      {
        "heading": "3. Dự án Website_CLB.html",
        "color": "purple",
        "bullets": [
          "Tích hợp tất cả thành phần trên 1 trang chuẩn.",
          "Đạt 8/8 tiêu chí tự động trên hd3.html.",
          "Nộp tệp về máy chủ GV đánh giá thực hành."
        ]
      },
      {
        "heading": "4. Đề Kiểm tra KTTX3 (15p)",
        "color": "red",
        "bullets": [
          "8 câu Trắc nghiệm 4 lựa chọn (6.0 điểm).",
          "2 câu Đúng/Sai chuẩn TN THPT (4.0 điểm).",
          "Phủ Bài 7–12, trọng tâm Bài 10, 11, 12."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "TIẾN TRÌNH TỔ CHỨC TIẾT HỌC (2 TIẾT)",
    "rows": [
      {
        "stage": "1. Khởi động (5')",
        "color": "blue",
        "desc": "Quan sát mô phỏng ghép 5 mảng thẻ thành Cổng thông tin Website_CLB.html."
      },
      {
        "stage": "2.1. Ôn Bài 7–10 (15')",
        "color": "emerald",
        "desc": "Chốt lại bẫy <th>, rowspan/colspan, đường dẫn tương đối ../ và neo #id."
      },
      {
        "stage": "2.2. Ôn 11–12 & Thi KTTX3 (25')",
        "color": "red",
        "desc": "Ôn đa phương tiện/biểu mẫu và làm bài KTTX3 (15 phút) trực tuyến qua QR."
      },
      {
        "stage": "3. Thực hành CLB (35')",
        "color": "purple",
        "desc": "Tự gõ mã tạo Website_CLB.html tích hợp đầy đủ 8 tiêu chí HTML5."
      },
      {
        "stage": "4. Tổng kết (10')",
        "color": "amber",
        "desc": "Chốt kiến thức bằng Infographic 4 chế độ & giải đáp câu hỏi bẫy."
      }
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 1 • KHỞI ĐỘNG",
    "title": "MỘT WEBSITE HOÀN CHỈNH CẦN GÌ?",
    "subtitle": "Kết nối đồng bộ toàn bộ thẻ HTML từ Bài 7 đến Bài 12",
    "theme": "blue",
    "pills": [
      [
        "Điều hướng & Cấu trúc",
        "Menu <a href=\"#id\"> + Bố cục bảng lịch <table>.",
        "blue"
      ],
      [
        "Truyền thông",
        "Hình ảnh <img>, video <video> hoặc <iframe>.",
        "emerald"
      ],
      [
        "Tương tác hai chiều",
        "Biểu mẫu <form> cho học sinh gửi đăng kí.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • RÀ SOÁT BÀI 7 – 9",
    "title": "ĐIỂM NÓNG CẤU TRÚC, DANH SÁCH & BẢNG",
    "sub": "Các kiến thức dễ mất điểm nhất trong phần đầu Chủ đề F",
    "theme": "blue",
    "left": {
      "heading": "📄 Cấu trúc & Văn bản (Bài 7–8)",
      "color": "blue",
      "bullets": [
        "<title> nằm trong <head>, nội dung hiển thị ở <body>.",
        "<h1> lớn nhất, <h6> nhỏ nhất; <p> tạo đoạn tách dòng.",
        "<strong> / <em> mang ngữ nghĩa quan trọng / nhấn mạnh.",
        "<ol type=\"1|a|A|i|I\" start=\"số\"> đánh số thứ tự."
      ]
    },
    "right": {
      "heading": "📊 Kỹ thuật Bảng HTML (Bài 9)",
      "color": "emerald",
      "bullets": [
        "<caption> đặt ngay dưới <table> để ghi tiêu đề bảng.",
        "<th> mặc định IN ĐẬM và CĂN GIỮA; <td> thường.",
        "colspan=\"n\": gộp n cột ngang -> bớt (n-1) ô cùng hàng.",
        "rowspan=\"n\": gộp n hàng dọc -> bớt 1 ô ở (n-1) hàng sau."
      ]
    }
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.1 • RÀ SOÁT BÀI 10",
    "title": "CHUẨN HÓA ĐƯỜNG DẪN TƯƠNG ĐỐI & #ID",
    "sub": "Quy tắc vàng giải mọi bài tập điều hướng thư mục",
    "theme": "emerald",
    "left": {
      "heading": "🧭 Đường dẫn URL",
      "color": "blue",
      "bullets": [
        "Tuyệt đối: https://... (trỏ ra ngoài website).",
        "Cùng thư mục: ten_tep.html.",
        "Vào thư mục con: con/ten_tep.html.",
        "Lùi lên thư mục cha: ../ten_tep.html."
      ]
    },
    "right": {
      "heading": "📌 Neo trong trang & Ảnh",
      "color": "emerald",
      "bullets": [
        "Gắn id=\"CLBTT\" vào thẻ tiêu đề đích.",
        "Nhảy cùng trang: href=\"#CLBTT\".",
        "Nhảy từ trang khác: href=\"CLB.html#CLBTT\".",
        "Ảnh bấm được: <a href><img src></a>."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.1 • ÔN HÌNH SGK BÀI 10",
    "title": "MINH HỌA CÂY THƯ MỤC & NEO LIÊN KẾT",
    "sub": "Đọc kỹ cấu trúc trước khi xác định đường dẫn ../",
    "theme": "blue",
    "heading": "🔍 Câu hỏi kiểm tra nhanh:",
    "bullets": [
      "Từ thuvien/sach.html quay về trangchu.html -> ../trangchu.html.",
      "Từ thuvien/sach.html tới anh/bia.png -> ../anh/bia.png.",
      "Dùng target=\"_blank\" khi muốn mở trang ở thẻ mới."
    ],
    "image": "sgk_hinh10_1.png",
    "caption": "Sơ đồ liên kết nhiều trang và mục trong dự án CLB (SGK Bài 10)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.2 • RÀ SOÁT BÀI 11",
    "title": "ĐA PHƯƠNG TIỆN (<IMG>, <AUDIO>, <VIDEO>, <IFRAME>)",
    "sub": "Phân biệt chính xác từng thuộc tính hợp lệ của mỗi thẻ",
    "theme": "amber",
    "left": {
      "heading": "🖼️ Ảnh & Âm thanh / Video",
      "color": "blue",
      "bullets": [
        "<img> chỉ đặt 1 kích thước -> chiều kia tự giữ đúng tỉ lệ!",
        "Thẻ <audio> KHÔNG có width, height, poster.",
        "Cả <audio> và <video> đều cần controls để hiện nút.",
        "<source> cung cấp nhiều định dạng (mp4/webm, mp3/ogg)."
      ]
    },
    "right": {
      "heading": "🪟 Khung nội tuyến <iframe>",
      "color": "emerald",
      "bullets": [
        "<iframe src=\"...\" width=\"...\" height=\"...\" name=\"khung\">",
        "Kết hợp <a href=\"...\" target=\"khung\"> để mở trong khung.",
        "Dùng nhúng trang web con, Google Maps, clip YouTube.",
        "Luôn thêm alt cho <img> và kiểm tra bản quyền tệp."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • ÔN TẬP IFRAME SGK",
    "title": "CƠ CHẾ HOẠT ĐỘNG TARGET + IFRAME",
    "sub": "Nhắc lại Hình 11.5 SGK Tin học 12",
    "theme": "amber",
    "heading": "🎯 Luồng thực thi khi nhấp liên kết:",
    "bullets": [
      "Bước 1: Trình duyệt tìm xem có iframe nào có name khớp target không.",
      "Bước 2: Nếu khớp, tải tệp đích vào bên trong khung chữ nhật đó.",
      "Bước 3: Toàn bộ thanh menu và tiêu đề trang ngoài vẫn đứng yên!"
    ],
    "image": "sgk_hinh11_5.png",
    "caption": "Kết hợp thẻ <a> target với <iframe> (SGK Bài 11)"
  },
  {
    "kind": "two_col",
    "badge": "HĐ 2.2 • RÀ SOÁT BÀI 12",
    "title": "HOÀN THIỆN BIỂU MẪU HTML5 (<FORM>)",
    "sub": "Những điểm cốt lõi cần nhớ về Form trong đề thi",
    "theme": "purple",
    "left": {
      "heading": "📋 Điều khiển nhập liệu",
      "color": "blue",
      "bullets": [
        "<label for=\"id\"> gắn với ô có id tương ứng.",
        "radio: chọn 1 -> CÁC NÚT PHẢI CÙNG name.",
        "checkbox: chọn nhiều phương án.",
        "password: che ký tự; file: chọn tệp đính kèm."
      ]
    },
    "right": {
      "heading": "📦 Gom nhóm & Mở rộng",
      "color": "emerald",
      "bullets": [
        "<select><option>: danh sách chọn thả xuống.",
        "<textarea rows cols></textarea>: văn bản nhiều dòng.",
        "<fieldset> + <legend>: đóng khung chia nhóm.",
        "<input type=\"submit\">: gửi dữ liệu tới action."
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 2.2 • MẪU FORM CHUẨN",
    "title": "PHÂN TÍCH MẪU FORM ĐĂNG KÍ (HÌNH 12.3)",
    "sub": "Nhận diện từng loại thẻ từ giao diện hoàn chỉnh",
    "theme": "purple",
    "heading": "🔎 Đọc giao diện suy ra thẻ HTML:",
    "bullets": [
      "Khung viền + chữ 'Thông tin...' -> <fieldset> + <legend>.",
      "Ô chữ 1 dòng -> <input type=\"text\">.",
      "Nút tròn chọn 1 -> <input type=\"radio\" name=\"...\">.",
      "Ô vuông nhiều lựa chọn -> <input type=\"checkbox\">."
    ],
    "image": "sgk_hinh12_3.png",
    "caption": "Mẫu biểu mẫu nhiều nhóm thông tin chuẩn SGK Bài 12"
  },
  {
    "kind": "section",
    "tag": "KIỂM TRA THƯỜNG XUYÊN 3 (15 PHÚT)",
    "title": "BẮT ĐẦU BÀI THI KTTX3 TRỰC TUYẾN",
    "subtitle": "Truy cập phieu-bai-tap.html (hoặc quét QR ở HĐ 2.2) • 8 MCQ (6đ) + 2 Đúng/Sai (4đ)",
    "theme": "red",
    "pills": [
      [
        "Thời gian: 15 phút",
        "Đồng hồ đếm ngược, tự động thu bài khi hết giờ.",
        "red"
      ],
      [
        "Phần I (6.0 điểm)",
        "8 câu trắc nghiệm 4 lựa chọn (0.75đ/câu).",
        "blue"
      ],
      [
        "Phần II (4.0 điểm)",
        "2 câu Đúng/Sai 4 ý chấm phân bậc BGD&ĐT.",
        "emerald"
      ]
    ]
  },
  {
    "kind": "quiz",
    "badge": "LUYỆN PHẢN XẠ KTTX3 • CÂU MẪU",
    "title": "TÍNH TOÁN BẢNG GỘP Ô & ĐA PHƯƠNG TIỆN",
    "sub": "Kiểm tra nhanh trước khi bấm làm bài thi 15 phút",
    "question": "Một bức ảnh có kích thước gốc 1600 × 900 px được chèn bằng <img src=\"hero.jpg\" width=\"800\" alt=\"Hero\"> (không đặt height). Độ cao hiển thị của ảnh là:",
    "options": [
      "A. 300 px",
      "B. 450 px",
      "C. 600 px",
      "D. 900 px"
    ],
    "answer": [
      "Đáp án đúng: B (450 px).",
      "Vì chiều rộng giảm một nửa (1600 -> 800) nên chiều cao tự động giảm một nửa (900 -> 450 px)."
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • THỰC HÀNH (35 PHÚT)",
    "title": "XÂY DỰNG CỔNG THÔNG TIN WEBSITE_CLB.HTML",
    "subtitle": "Tự gõ mã trên trình soạn thảo trống hd3.html — Đạt đủ 8/8 tiêu chí HTML5",
    "theme": "purple",
    "pills": [
      [
        "Bảng & Liên kết",
        "Mục lục #id + <table> gộp ô lịch sinh hoạt CLB.",
        "blue"
      ],
      [
        "Đa phương tiện",
        "Ảnh <img> (kèm alt) + <video>/<audio>/<iframe>.",
        "emerald"
      ],
      [
        "Form đăng kí",
        "<form> có radio, checkbox và nút submit hoàn chỉnh.",
        "amber"
      ]
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 3 • RUBRIC 8 TIÊU CHÍ",
    "title": "YÊU CẦU KỸ THUẬT WEBSITE_CLB.HTML",
    "sub": "Rà soát đủ 8 gạch đầu dòng trước khi nộp lên máy chủ GV",
    "theme": "purple",
    "left": {
      "heading": "🧱 Phần 1: Bố cục, Bảng & Media (1–4)",
      "color": "blue",
      "bullets": [
        "1. Cấu trúc chuẩn <!DOCTYPE html>, <html>, <body>.",
        "2. Có bảng lịch <table> có thẻ <th> và colspan (hoặc rowspan).",
        "3. Có menu điều hướng nội bộ <a href=\"#...\"> trỏ đúng id.",
        "4. Có <img> (kèm alt) và <video>/<audio>/<iframe>."
      ]
    },
    "right": {
      "heading": "📝 Phần 2: Biểu mẫu Đăng kí CLB (5–8)",
      "color": "emerald",
      "bullets": [
        "5. Có khung <form> bao toàn bộ phần đăng kí.",
        "6. Có ít nhất 1 cặp <input type=\"radio\"> cùng name.",
        "7. Có nhóm chọn nhiều <input type=\"checkbox\">.",
        "8. Có nút gửi <input type=\"submit\"> hoàn chỉnh."
      ]
    }
  },
  {
    "kind": "code_result",
    "badge": "HĐ 3 • KHUNG SƯỜN GỢI Ý",
    "title": "CẤU TRÚC TỔNG THỂ WEBSITE_CLB.HTML",
    "sub": "Tham khảo tổ chức bố cục (học sinh tự gõ nội dung đầy đủ)",
    "theme": "blue",
    "filename": "Website_CLB.html",
    "code": "<nav><a href=\"#lich\">Lịch CLB</a> | <a href=\"#dk\">Đăng kí</a></nav>\n<h2 id=\"lich\">1. Lịch sinh hoạt</h2>\n<table border=\"1\"><tr><th colspan=\"2\">CLB Trường</th></tr>...</table>\n<img src=\"clb.jpg\" alt=\"CLB\" width=\"320\">\n<h2 id=\"dk\">2. Đăng kí tham gia</h2>\n<form>\n  <input type=\"radio\" name=\"khoi\"> K12 ...\n  <input type=\"checkbox\"> Tin học\n  <input type=\"submit\" value=\"Gửi\">\n</form>",
    "right_heading": "💡 MẸO LÀM BÀI NHANH:",
    "notes": [
      "Viết từng phần theo thứ tự: Nav -> Bảng -> Ảnh/Video -> Form.",
      "Nhấn 'Chạy & Biên dịch' sau mỗi phần để kiểm tra hiển thị.",
      "Nhấn 'Kiểm tra tiêu chí' xem tick xanh 8/8 rồi mới Nộp bài."
    ]
  },
  {
    "kind": "three_col",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC CHẶNG HTML",
    "title": "BẢN ĐỒ TRỌN BỘ HTML5 (BÀI 7 – BÀI 12)",
    "sub": "Hành trang vững vàng chuẩn bị ôn thi Cuối Học kỳ 1",
    "theme": "emerald",
    "cols": [
      {
        "heading": "Văn bản & Dữ liệu",
        "color": "blue",
        "subhead": "Bài 7, 8, 9",
        "bullets": [
          "<html>, <head>, <body>",
          "<h1>–<h6>, <p>, <strong>, <em>",
          "<ol>, <ul>, <dl>, <table> gộp ô"
        ]
      },
      {
        "heading": "Liên kết & Media",
        "color": "emerald",
        "subhead": "Bài 10, 11",
        "bullets": [
          "<a href> (tuyệt đối, ../, #id)",
          "<img src alt> giữ đúng tỉ lệ",
          "<audio>, <video>, <iframe> + target"
        ]
      },
      {
        "heading": "Biểu mẫu Tương tác",
        "color": "amber",
        "subhead": "Bài 12",
        "bullets": [
          "<form>, <label for=\"id\">",
          "<input>: text, radio, checkbox",
          "<select>, <textarea>, <fieldset>"
        ]
      }
    ]
  },
  {
    "kind": "quiz",
    "badge": "HĐ 4 • GIẢI MÃ BẪY KTTX3",
    "title": "ĐỌC HIỂU MÃ NGUỒN PHẦN ĐÚNG / SAI",
    "sub": "Tổng hợp cả bảng, liên kết và đa phương tiện",
    "question": "Cho mã: <a href=\"../index.html\">Về</a> <table border=\"1\"><tr><th colspan=\"2\">Lịch</th></tr><tr><td>T2</td><td>Bóng đá</td></tr></table>",
    "options": [
      "a) Liên kết trên trỏ ra tệp index.html ở thư mục cha trực tiếp.",
      "b) Ô 'Lịch' nằm căn trái và chữ không in đậm.",
      "c) Ô 'Lịch' gộp 2 cột ngang khớp với 2 ô <td> hàng dưới.",
      "d) Thêm <a href=\"#top\"> giúp cuộn đến id=\"top\"."
    ],
    "answer": [
      "a) Đúng — ../ lùi lên 1 cấp thư mục.",
      "b) Sai — thẻ <th> mặc định IN ĐẬM và CĂN GIỮA.",
      "c) Đúng — colspan=\"2\" cân xứng 2 cột dưới.",
      "d) Đúng — #top trỏ đến phần tử mang id=\"top\"."
    ]
  },
  {
    "kind": "two_col",
    "badge": "HĐ 4 • ĐỊNH HƯỚNG ÔN TẬP HK1",
    "title": "CHUẨN BỊ CHO ÔN TẬP & THI THỬ HK1",
    "sub": "Hệ thống kiến thức 4 chủ đề A, B, D và F",
    "theme": "blue",
    "left": {
      "heading": "📚 Nội dung cần ôn lại",
      "color": "blue",
      "bullets": [
        "Chủ đề A: Trí tuệ nhân tạo & Ứng dụng (Bài 1–2).",
        "Chủ đề B: Thiết bị mạng & Giao thức mạng (Bài 3–5).",
        "Chủ đề D: Đạo đức, văn hóa số trên mạng (Bài 6).",
        "Chủ đề F: Toàn bộ thẻ HTML5 (Bài 7–12)."
      ]
    },
    "right": {
      "heading": "📝 Cấu trúc Đề thi HK1 (45 phút)",
      "color": "emerald",
      "bullets": [
        "Tổng 28 câu theo đúng mẫu TN THPT 2025/2026.",
        "Phần I: 24 câu MCQ (0.25đ × 24 = 6.0 điểm).",
        "Phần II: 4 câu Đúng/Sai (1.0đ × 4 = 4.0 điểm).",
        "Sẵn sàng làm đề thi thử trực tuyến Cuối Học kì 1!"
      ]
    }
  },
  {
    "kind": "image_focus",
    "badge": "HĐ 4 • GHI NHỚ TỔNG KẾT",
    "title": "MỐI QUAN HỆ GIỮA CÁC THẺ & BỐ CỤC",
    "sub": "Kết thúc phần HTML cấu trúc — Chuẩn bị bước vào CSS",
    "theme": "emerald",
    "heading": "🎨 Vì sao chặng tiếp theo ta cần học CSS?",
    "bullets": [
      "HTML giúp tổ chức khung xương, nội dung, ảnh và biểu mẫu.",
      "Tuy nhiên dùng HTML thuần khiến trang thiếu màu sắc, bố cục cứng.",
      "Từ Bài 13–15, CSS sẽ làm đẹp toàn bộ dự án trên!"
    ],
    "image": "sgk_hinh10_2.png",
    "caption": "Minh họa kết cấu siêu liên kết nội bộ hoàn thiện phần HTML"
  },
  {
    "kind": "code_result",
    "badge": "HĐ 4 • SỬA LỖI THƯỜNG GẶP",
    "title": "3 LỖI KINH ĐIỂN TRONG CODE HTML HỌC SINH",
    "sub": "Kiểm tra chéo để không bị mất điểm oan",
    "theme": "red",
    "filename": "sua_loi.html",
    "code": "<!-- Lỗi 1: Quên đóng thẻ </a> -->\n<a href=\"home.html\">Trang chủ  <!-- THIẾU </a> -->\n\n<!-- Lỗi 2: Radio khác name -->\n<input type=\"radio\" name=\"a\"> Nam\n<input type=\"radio\" name=\"b\"> Nữ\n\n<!-- Lỗi 3: Audio dùng poster -->\n<audio controls poster=\"bia.jpg\" src=\"nhac.mp3\"></audio>",
    "right_heading": "✅ CÁCH KHẮC PHỤC CHUẨN:",
    "notes": [
      "Lỗi 1: Luôn đóng thẻ </a> ngay sau chữ/ảnh liên kết.",
      "Lỗi 2: Đặt chung name=\"gt\" cho cả 2 nút radio Nam & Nữ.",
      "Lỗi 3: Bỏ poster khỏi <audio> (chỉ dùng cho <video>)."
    ]
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH THỰC HÀNH TỔNG HỢP & KTTX3!",
    "takeaways": [
      "Đảm bảo đã nộp đủ bài KTTX3 (phieu-bai-tap.html) và bài code Website_CLB.html (hd3.html).",
      "Ôn tập kỹ 4 bước sửa lỗi HTML thường gặp: đóng thẻ, rowspan/colspan, ../ và radio chung name.",
      "Chuẩn bị chuyên đề tiếp theo: Ôn tập Học kỳ 1 & Thi thử Cuối HK1 (45 phút – 28 câu chuẩn BGD&ĐT)."
    ]
  }
]
LESSON_SHORT = "Thực hành tổng hợp HTML & KTTX3"
OUT_PPTX_NAME = "KTTX3_TrinhChieu.pptx"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx)
