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


def add_code_panel(slide, left, top, width, height, code_str, filename="index.html", light_mode=False):
    panel_bg = RGBColor(241, 245, 249) if light_mode else COLOR_CODE_BG
    panel_border = RGBColor(147, 197, 253) if light_mode else RGBColor(51, 65, 85)
    hdr_bg = RGBColor(226, 232, 240) if light_mode else RGBColor(30, 41, 59)
    fn_color = RGBColor(51, 65, 85) if light_mode else RGBColor(148, 163, 184)
    tag_color = RGBColor(29, 78, 216) if light_mode else RGBColor(125, 211, 252)
    plain_color = RGBColor(30, 41, 59) if light_mode else COLOR_CODE_TEXT

    add_card(slide, left, top, width, height, bg=panel_bg, border=panel_border, bw=1.5)
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.42))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = hdr_bg
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
    ph.font.color.rgb = fn_color

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
        p.font.color.rgb = tag_color if "<" in line and ">" in line else plain_color


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


def build_from_slides_data(slides_data, lesson_short, assets_dir, out_pptx, light_mode=False):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides_data)

    for idx, sd in enumerate(slides_data, start=1):
        sl = prs.slides.add_slide(blank)
        kind = sd["kind"]

        if kind == "cover":
            if light_mode:
                set_bg(sl, RGBColor(239, 246, 255))
                bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
                bar.fill.solid(); bar.fill.fore_color.rgb = COLOR_ROYAL; bar.line.fill.background()

                add_card(sl, Inches(0.55), Inches(0.45), Inches(12.23), Inches(6.6), bg=COLOR_WHITE, border=RGBColor(191, 219, 254), bw=1.8)
                has_img = bool(sd.get("image") and os.path.exists(os.path.join(assets_dir, sd["image"])))
                left_w = Inches(5.65) if has_img else Inches(11.3)

                pill = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.85), min(left_w, Inches(5.55)), Inches(0.46))
                pill.fill.solid(); pill.fill.fore_color.rgb = RGBColor(219, 234, 254)
                pill.line.color.rgb = COLOR_ROYAL; pill.line.width = Pt(1.2)
                pp = pill.text_frame.paragraphs[0]
                pp.text = sd["pill"]
                pp.font.name = FONT_HEADING; pp.font.size = Pt(12.5); pp.font.bold = True; pp.font.color.rgb = COLOR_PRIMARY
                pp.alignment = PP_ALIGN.CENTER

                tb = sl.shapes.add_textbox(Inches(0.9), Inches(1.52), left_w, Inches(2.5))
                tf = tb.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; p.text = sd["title"]
                p.font.name = FONT_HEADING; p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY
                p2 = tf.add_paragraph(); p2.text = "\n" + sd["subtitle"]
                p2.font.name = FONT_BODY; p2.font.size = Pt(16.5); p2.font.color.rgb = COLOR_TEXT_BODY

                meta = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.05), left_w, Inches(1.55))
                meta.fill.solid(); meta.fill.fore_color.rgb = RGBColor(239, 246, 255)
                meta.line.color.rgb = RGBColor(147, 197, 254); meta.line.width = Pt(1.2)
                mtf = meta.text_frame; mtf.word_wrap = True
                mp = mtf.paragraphs[0]
                mp.text = f"  Trường: THTH-DHSP  •  {sd['meta']}"
                mp.font.name = FONT_HEADING; mp.font.size = Pt(14.5); mp.font.bold = True; mp.font.color.rgb = COLOR_PRIMARY
                mp2 = mtf.add_paragraph()
                mp2.text = "  Giáo viên: Nguyễn Lê Minh Ngọc"
                mp2.font.name = FONT_BODY; mp2.font.size = Pt(14); mp2.font.bold = True; mp2.font.color.rgb = COLOR_ROYAL; mp2.space_before = Pt(4)
                mp3 = mtf.add_paragraph()
                mp3.text = f"  Web: {sd['url']}"
                mp3.font.name = FONT_BODY; mp3.font.size = Pt(13); mp3.font.color.rgb = COLOR_TEXT_MUTED; mp3.space_before = Pt(4)

                if has_img:
                    add_card(sl, Inches(6.78), Inches(0.85), Inches(5.68), Inches(5.75), bg=RGBColor(248, 250, 252), border=RGBColor(191, 219, 254), bw=1.2)
                    add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(6.92), Inches(1.0), Inches(5.4), Inches(5.45))
            else:
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

                meta = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.35), Inches(11.6), Inches(1.25))
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
            add_code_panel(sl, Inches(0.65), Inches(1.72), Inches(6.25), Inches(5.1), sd["code"], sd.get("filename", "index.html"), light_mode=light_mode)

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
            if light_mode:
                add_card(sl, Inches(0.65), Inches(1.68), Inches(3.65), Inches(5.18), border=COLOR_ROYAL, bw=1.6)
                add_bullets_box(sl, Inches(0.84), Inches(1.86), Inches(3.27), Inches(4.82),
                                sd["heading"], sd["bullets"], heading_color=COLOR_PRIMARY, body_size=15)

                add_card(sl, Inches(4.52), Inches(1.68), Inches(8.16), Inches(5.18), border=COLOR_CARD_BORDER, bw=1.5)
                add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(4.62), Inches(1.80), Inches(7.96), Inches(4.52))
                if sd.get("caption"):
                    tb = sl.shapes.add_textbox(Inches(4.62), Inches(6.38), Inches(7.96), Inches(0.42))
                    p = tb.text_frame.paragraphs[0]; p.text = sd["caption"]
                    p.font.name = FONT_BODY; p.font.size = Pt(13); p.font.italic = True; p.font.color.rgb = COLOR_TEXT_MUTED; p.alignment = PP_ALIGN.CENTER
            else:
                add_card(sl, Inches(0.65), Inches(1.72), Inches(5.15), Inches(5.1), border=COLOR_ROYAL, bw=1.8)
                add_bullets_box(sl, Inches(0.9), Inches(1.92), Inches(4.65), Inches(4.7),
                                sd["heading"], sd["bullets"], heading_color=COLOR_PRIMARY, body_size=15.5)

                add_card(sl, Inches(6.02), Inches(1.72), Inches(6.66), Inches(5.1), border=COLOR_CARD_BORDER, bw=1.5)
                add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(6.22), Inches(1.9), Inches(6.26), Inches(4.25))
                if sd.get("caption"):
                    tb = sl.shapes.add_textbox(Inches(6.2), Inches(6.28), Inches(6.3), Inches(0.45))
                    p = tb.text_frame.paragraphs[0]; p.text = sd["caption"]
                    p.font.name = FONT_BODY; p.font.size = Pt(13.5); p.font.italic = True; p.font.color.rgb = COLOR_TEXT_MUTED; p.alignment = PP_ALIGN.CENTER

        elif kind == "visual_hero":
            set_bg(sl)
            col = COLOR_MAP.get(sd.get("theme", "blue"), COLOR_ROYAL)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            add_card(sl, Inches(0.65), Inches(1.66), Inches(12.03), Inches(5.22), border=col, bw=1.6)
            add_picture_fitted(sl, os.path.join(assets_dir, sd["image"]), Inches(0.86), Inches(1.78), Inches(11.61), Inches(4.52))
            if sd.get("caption"):
                tb = sl.shapes.add_textbox(Inches(0.9), Inches(6.36), Inches(11.53), Inches(0.44))
                p = tb.text_frame.paragraphs[0]; p.text = sd["caption"]
                p.font.name = FONT_BODY; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.alignment = PP_ALIGN.CENTER

        elif kind == "dual_image":
            set_bg(sl)
            col = COLOR_MAP.get(sd.get("theme", "blue"), COLOR_ROYAL)
            add_header(sl, sd["badge"], sd["title"], sd.get("sub", ""), sd.get("theme", "blue"))
            add_footer(sl, idx, total, lesson_short)
            panels = [
                (Inches(0.65), sd.get("left_title", ""), sd["left_image"], sd.get("left_caption", ""), COLOR_ROYAL),
                (Inches(6.80), sd.get("right_title", ""), sd["right_image"], sd.get("right_caption", ""), COLOR_EMERALD),
            ]
            for px, ptitle, pimg, pcap, pcol in panels:
                add_card(sl, px, Inches(1.68), Inches(5.88), Inches(5.18), border=pcol, bw=1.6)
                if ptitle:
                    pt = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.18), Inches(1.82), Inches(5.52), Inches(0.42))
                    pt.fill.solid(); pt.fill.fore_color.rgb = RGBColor(239, 246, 255) if pcol == COLOR_ROYAL else RGBColor(236, 253, 245)
                    pt.line.color.rgb = pcol; pt.line.width = Pt(1)
                    pp = pt.text_frame.paragraphs[0]; pp.text = ptitle
                    pp.font.name = FONT_HEADING; pp.font.size = Pt(13.5); pp.font.bold = True; pp.font.color.rgb = COLOR_PRIMARY if pcol == COLOR_ROYAL else COLOR_DARK_GREEN
                    pp.alignment = PP_ALIGN.CENTER
                add_picture_fitted(sl, os.path.join(assets_dir, pimg), px + Inches(0.18), Inches(2.34), Inches(5.52), Inches(3.98))
                if pcap:
                    tb = sl.shapes.add_textbox(px + Inches(0.18), Inches(6.38), Inches(5.52), Inches(0.40))
                    p = tb.text_frame.paragraphs[0]; p.text = pcap
                    p.font.name = FONT_BODY; p.font.size = Pt(12); p.font.italic = True; p.font.color.rgb = COLOR_TEXT_MUTED; p.alignment = PP_ALIGN.CENTER

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
            if light_mode:
                set_bg(sl, RGBColor(240, 253, 244))
                bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
                bar.fill.solid(); bar.fill.fore_color.rgb = COLOR_EMERALD; bar.line.fill.background()

                add_card(sl, Inches(0.85), Inches(0.55), Inches(11.63), Inches(6.4), bg=COLOR_WHITE, border=RGBColor(134, 239, 172), bw=2.0)

                tb = sl.shapes.add_textbox(Inches(1.15), Inches(0.95), Inches(11.03), Inches(1.0))
                tf = tb.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; p.text = sd["title"]
                p.font.name = FONT_HEADING; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = COLOR_DARK_GREEN; p.alignment = PP_ALIGN.CENTER

                add_card(sl, Inches(1.25), Inches(2.1), Inches(10.83), Inches(2.75), bg=RGBColor(236, 253, 245), border=COLOR_EMERALD, bw=1.6)
                tbm = sl.shapes.add_textbox(Inches(1.55), Inches(2.28), Inches(10.2), Inches(2.4))
                tfm = tbm.text_frame; tfm.word_wrap = True
                pm0 = tfm.paragraphs[0]; pm0.text = "📌 GHI NHỚ NHANH & DẶN DÒ:"
                pm0.font.name = FONT_HEADING; pm0.font.size = Pt(17); pm0.font.bold = True; pm0.font.color.rgb = COLOR_DARK_GREEN
                for point in sd["takeaways"]:
                    pm = tfm.add_paragraph(); pm.text = f"• {point}"
                    pm.font.name = FONT_BODY; pm.font.size = Pt(15.5); pm.font.color.rgb = COLOR_TEXT_BODY; pm.space_before = Pt(7)

                tb_end = sl.shapes.add_textbox(Inches(1.15), Inches(5.3), Inches(11.03), Inches(1.15))
                tfe = tb_end.text_frame
                pe = tfe.paragraphs[0]; pe.text = "TRÂN TRỌNG CẢM ƠN CÁC EM ĐÃ THAM GIA TIẾT HỌC!"
                pe.font.name = FONT_HEADING; pe.font.size = Pt(19.5); pe.font.bold = True; pe.font.color.rgb = COLOR_ROYAL; pe.alignment = PP_ALIGN.CENTER
                pe2 = tfe.add_paragraph(); pe2.text = "THTH-DHSP • Giáo viên: Nguyễn Lê Minh Ngọc"
                pe2.font.name = FONT_BODY; pe2.font.size = Pt(14.5); pe2.font.bold = True; pe2.font.color.rgb = COLOR_PRIMARY; pe2.alignment = PP_ALIGN.CENTER; pe2.space_before = Pt(4)
            else:
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
    "subtitle": "Siêu văn bản • Đường dẫn Tuyệt đối & Tương đối • Website Đa tệp HTML",
    "meta": "Tiết 19–20 (2 tiết)",
    "url": "https://minda.io.vn/Tin12/Bai10/index.html",
    "image": "illus_10_sieu_van_ban_la_gi.png"
  },
  {
    "kind": "objectives",
    "title": "I. MỤC TIÊU BÀI HỌC (KHBD CV 5512)",
    "sub": "Bám sát Giáo án Tin học 12 & Khung Năng lực số",
    "cards": [
      {
        "heading": "1. Năng lực Tin học (1)–(3)",
        "color": "blue",
        "bullets": [
          "(1) Hiểu siêu văn bản & siêu liên kết.",
          "(2) Viết thẻ <a>, href, #id, <img>.",
          "(3) Chọn URL tuyệt đối / tương đối."
        ]
      },
      {
        "heading": "2. Năng lực số 3.4.NC1.a",
        "color": "emerald",
        "bullets": [
          "Phát triển nội dung số đa trang.",
          "Tạo Website >= 2 tệp HTML.",
          "Liên kết logic theo cây thư mục."
        ]
      },
      {
        "heading": "3. Năng lực chung (4)–(6)",
        "color": "amber",
        "bullets": [
          "(4) Tự học trên Sandbox tương tác.",
          "(5) Hợp tác cặp đôi hiệu quả.",
          "(6) Xử lí lỗi 404 / ổ đĩa D:\\."
        ]
      },
      {
        "heading": "4. Phẩm chất (7)",
        "color": "purple",
        "bullets": [
          "(7) Chăm chỉ, thực hiện nghiêm túc.",
          "Đặt tên tệp chuẩn không dấu.",
          "Trung thực tự kiểm tra tiêu chí."
        ]
      }
    ]
  },
  {
    "kind": "roadmap",
    "title": "TIẾN TRÌNH 4 HOẠT ĐỘNG (THEO KHBD.DOCX)",
    "rows": [
      {
        "stage": "HĐ 1: Khởi động (5')",
        "color": "blue",
        "desc": "Trang web khác gì sách, báo giấy? (SGK tr.57)"
      },
      {
        "stage": "HĐ 2.1: Khám phá 1 (15')",
        "color": "emerald",
        "desc": "Mục 1: Siêu văn bản, .docx vs .txt, thẻ <a> & Đường dẫn (tr.57–58)"
      },
      {
        "stage": "HĐ 2.2: Khám phá 2 (20')",
        "color": "amber",
        "desc": "Mục 2: 4 kiểu liên kết, Hình 10.1, neo #id, ảnh & Phiếu BT (tr.58–60)"
      },
      {
        "stage": "HĐ 3: Luyện tập (35')",
        "color": "purple",
        "desc": "Mục 3: Tạo Website >= 2 tệp HTML (CLB.html ⇄ thong_tin.html) (tr.61)"
      },
      {
        "stage": "HĐ 4: Infographic (15')",
        "color": "red",
        "desc": "AntV Infographic Studio & Luyện tập 1–2, Vận dụng tr.61"
      }
    ]
  },
  {
    "kind": "visual_hero",
    "badge": "HĐ 1 • KHỞI ĐỘNG (5')",
    "title": "SÁCH / BÁO GIẤY VS TRANG WEB (SIÊU VĂN BẢN)",
    "sub": "SGK Tin học 12 • Trang 57",
    "theme": "blue",
    "image": "illus_10_sach_vs_web.png",
    "caption": "Sách đọc tuần tự bằng tay — Trang web nhảy tức thì qua siêu liên kết"
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.1 • KHÁM PHÁ 1 (15')",
    "title": "1. SIÊU VĂN BẢN VÀ ĐƯỜNG DẪN",
    "subtitle": "SGK tr.57–58 • Hoạt động 1 (.docx vs .txt) • Thẻ <a> • Tuyệt đối & Tương đối",
    "theme": "emerald",
    "pills": [
      [
        "Siêu văn bản",
        "Chữ + Ảnh + Video + Link",
        "blue"
      ],
      [
        "Thẻ <a href>",
        "<a href=\"URL\">Nội dung</a>",
        "emerald"
      ],
      [
        "2 loại URL",
        "Tuyệt đối vs Tương đối",
        "purple"
      ]
    ]
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 1 • HOẠT ĐỘNG 1 (TR.57)",
    "title": "ĐỌC TỆP .DOCX (WORD) KHÁC GÌ TỆP .TXT (NOTEPAD)?",
    "sub": "Quan sát cửa sổ thực tế",
    "theme": "blue",
    "image": "illus_10_docx_vs_txt.png",
    "caption": ".docx bấm Ctrl + Click mở ngay web • .txt chỉ lưu chữ đen tĩnh"
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 1 • MỤC 1 (TR.57)",
    "title": "SIÊU VĂN BẢN (HYPERTEXT) LÀ GÌ?",
    "heading": "3 từ khóa cốt lõi:",
    "bullets": [
      "Tích hợp chữ, ảnh, video.",
      "Gắn mạng lưới siêu liên kết.",
      "VD: Wikipedia, Hành trang số."
    ],
    "image": "illus_10_sieu_van_ban_la_gi.png",
    "caption": "4 thành phần trực quan trên một trang Siêu văn bản HTML5"
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 1 • CÚ PHÁP THẺ <a>",
    "title": "SIÊU LIÊN KẾT (HYPERLINK): CÚ PHÁP <A> & 3 VÍ DỤ",
    "sub": "Di chuột hóa bàn tay • Nhấp chuột chuyển trang",
    "theme": "emerald",
    "image": "illus_10_sieu_lien_ket_anatomy.png",
    "caption": "<a href=\"URL\">Nội dung chữ hoặc ảnh <img></a>"
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 1 • MỤC 1 (TR.58)",
    "title": "ĐƯỜNG DẪN TUYỆT ĐỐI (ABSOLUTE URL)",
    "heading": "Khi nào dùng?",
    "bullets": [
      "Đủ https:// + tên miền.",
      "Dùng trỏ ra Website ngoài.",
      "VD: https://www.nxbgd.vn/"
    ],
    "image": "illus_10_duong_dan_tuyet_doi.png",
    "caption": "Cấu trúc URL tuyệt đối trên Internet & cảnh báo đường dẫn ổ D:\\"
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 1 • MỤC 1 (TR.58)",
    "title": "ĐƯỜNG DẪN TƯƠNG ĐỐI (RELATIVE URL)",
    "heading": "3 hướng đi nội bộ:",
    "bullets": [
      "Cùng cấp: thong_tin.html",
      "Xuống con: bai_tap/bt1.html",
      "Lùi lên cha: ../index.html"
    ],
    "image": "illus_10_duong_dan_tuong_doi.png",
    "caption": "Tính từ thư mục chứa tệp HTML hiện tại — gọn & không gãy link"
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 1 • LƯU Ý QUAN TRỌNG",
    "title": "TẠI SAO CẤM DÙNG ĐƯỜNG DẪN Ổ ĐĨA D:\\... TRONG WEB?",
    "sub": "SGK Tin học 12 • Trang 58",
    "theme": "red",
    "image": "illus_10_so_sanh_di_chuyen_web.png",
    "caption": "Ổ D:\\ hỏng ngay khi sang máy khác • Tương đối chạy 100% mọi nơi"
  },
  {
    "kind": "quiz",
    "badge": "KHÁM PHÁ 1 • CÂU HỎI MỤC 1 (TR.58)",
    "title": "PHÂN LOẠI ĐƯỜNG DẪN & CHỌN CÁCH VIẾT CHUẨN",
    "question": "Phân loại 3 đường dẫn sau và chỉ ra đường dẫn không nên dùng cho website:",
    "options": [
      "a) http://hocmai.vn/khoahoc",
      "b) bai_tap/bai_tap_1.html",
      "c) D:\\TinHoc12\\index.html"
    ],
    "answer": [
      "a) Tuyệt đối (Internet) — dùng mở trang ngoài.",
      "b) Tương đối (thư mục con) — chuẩn cho web nội bộ.",
      "c) Tuyệt đối ổ đĩa cá nhân — KHÔNG NÊN DÙNG!"
    ]
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 2.2 • KHÁM PHÁ 2 (20')",
    "title": "2. CÁC CÁCH TẠO LIÊN KẾT TỚI TRANG WEB",
    "subtitle": "SGK tr.58–60 • Web ngoài (2a) • Cùng website Hình 10.1 (2b) • Neo #id & Ảnh",
    "theme": "purple",
    "pills": [
      [
        "2a) Web ngoài",
        "Đủ giao thức https://",
        "blue"
      ],
      [
        "2b) Hình 10.1",
        "Tương đối: tên tệp, /, ../",
        "emerald"
      ],
      [
        "Neo & Ảnh",
        "#id và <a><img></a>",
        "amber"
      ]
    ]
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 2 • HOẠT ĐỘNG 2 (TR.58)",
    "title": "4 KIỂU SIÊU LIÊN KẾT THƯỜNG GẶP TRÊN WEB",
    "sub": "Hoạt động 2 • SGK tr.58",
    "theme": "purple",
    "image": "illus_10_4_kieu_lien_ket_web.png",
    "caption": "Web ngoài • Cùng website • Vị trí #id • Hình ảnh liên kết"
  },
  {
    "kind": "dual_image",
    "badge": "KHÁM PHÁ 2 • MỤC 2a (TR.59)",
    "title": "LIÊN KẾT TỚI TRANG WEB KHÁC & BẪY QUÊN HTTPS://",
    "theme": "blue",
    "left_title": "1. Kết nối ra Internet (Đúng chuẩn)",
    "left_image": "illus_10_22_lien_ket_ngoai_browser.png",
    "left_caption": "Mở thẳng website ngoài nhờ URL tuyệt đối",
    "right_title": "2. So sánh Có https:// vs Thiếu https://",
    "right_image": "illus_10_22_loi_quyen_https.png",
    "right_caption": "Thiếu https:// trình duyệt tìm nhầm thành tệp 404!"
  },
  {
    "kind": "dual_image",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (HÌNH 10.1 TR.59)",
    "title": "CÂY THƯ MỤC HÌNH 10.1: CÙNG CẤP & THƯ MỤC CON",
    "theme": "emerald",
    "left_title": "1. Cấu trúc cây thư mục Website (Hình 10.1 SGK)",
    "left_image": "sgk_hinh10_1.png",
    "left_caption": "web/ chứa index.html, thong_tin.html, bai_tap/...",
    "right_title": "2. Liên kết cùng cấp & Đi xuống thư mục con (/)",
    "right_image": "illus_10_22_cung_thu_muc_va_con.png",
    "right_caption": "thong_tin.html • bai_tap/on_tap/bai_tap_on_tap.html"
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.59)",
    "title": "ĐI NGƯỢC LÊN THƯ MỤC CHA BẰNG ../ VÀ ../../",
    "sub": "Khi trang nguồn nằm trong thư mục con",
    "theme": "purple",
    "image": "illus_10_22_lui_thu_muc_cha.png",
    "caption": "Mỗi ../ bước lùi lên 1 cấp thư mục cha"
  },
  {
    "kind": "dual_image",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.59–60)",
    "title": "LIÊN KẾT VỊ TRÍ CỤ THỂ BẰNG MÃ ĐỊNH DANH ID VÀ #",
    "theme": "blue",
    "left_title": "1. Nhảy trên CÙNG trang (#id)",
    "left_image": "illus_10_22_neo_cung_trang.png",
    "left_caption": "Đặt id=\"CLB_TinHoc\" rồi gọi href=\"#CLB_TinHoc\"",
    "right_title": "2. Nhảy tới vị trí trên TRANG KHÁC (tep.html#id)",
    "right_image": "illus_10_22_neo_khac_trang.png",
    "right_caption": "Ghép tên tệp + #id: thong_tin.html#CLBTT"
  },
  {
    "kind": "visual_hero",
    "badge": "KHÁM PHÁ 2 • MỤC 2b (TR.60)",
    "title": "SỬ DỤNG HÌNH ẢNH LÀM SIÊU LIÊN KẾT",
    "sub": "Đặt thẻ <img> bên trong cặp thẻ <a>...</a>",
    "theme": "amber",
    "image": "illus_10_22_hinh_anh_lam_lien_ket.png",
    "caption": "Tránh đặt href trực tiếp lên <img> — phải bọc trong <a href=\"...\">"
  },
  {
    "kind": "image_focus",
    "badge": "KHÁM PHÁ 2 • CÂU HỎI MỤC 2 (TR.60)",
    "title": "THỬ THÁCH HÌNH 10.1 & PHIẾU BÀI TẬP",
    "heading": "Yêu cầu thực hiện:",
    "bullets": [
      "Viết <ul> đặt tại index.html.",
      "Nối tới bai_tap_1.html & ôn tập.",
      "Quét QR làm Phiếu BT 6 câu!"
    ],
    "image": "illus_10_22_cau_hoi_ul_hinh10_1.png",
    "caption": "Xác định href đúng cho 2 tệp trong bai_tap/ rồi đối chiếu trên web"
  },
  {
    "kind": "section",
    "tag": "HOẠT ĐỘNG 3 • LUYỆN TẬP (35')",
    "title": "THỰC HÀNH WEBSITE NHIỀU TỆP HTML",
    "subtitle": "Mục 3 SGK tr.61 • Phòng Luyện tập Đa tệp (hd3.html)",
    "theme": "emerald",
    "pills": [
      [
        "Tạo >= 2 tệp",
        "CLB.html & thong_tin.html",
        "blue"
      ],
      [
        "Gắn liên kết",
        "thong_tin.html#CLBTT & https://",
        "emerald"
      ],
      [
        "Kiểm thử & Nộp",
        "Chấm 8 tiêu chí & lưu ZIP",
        "purple"
      ]
    ]
  },
  {
    "kind": "visual_hero",
    "badge": "HOẠT ĐỘNG 3 • MẪU KẾT QUẢ BIÊN DỊCH",
    "title": "MẪU KẾT QUẢ SAU KHI BIÊN DỊCH FILE 1 ⇄ FILE 2",
    "sub": "Quan sát giao diện đích trước khi gõ mã trên hd3.html",
    "theme": "blue",
    "image": "illus_10_hd3_mau_file1_va_file2.png",
    "caption": "Bấm liên kết giữa CLB.html (File 1) và thong_tin.html#CLBTT (File 2)"
  },
  {
    "kind": "dual_image",
    "badge": "HOẠT ĐỘNG 3 • HƯỚNG DẪN 2 NHIỆM VỤ",
    "title": "MINH HỌA NHIỆM VỤ 1 (FILE 2) & NHIỆM VỤ 2 (FILE 1)",
    "theme": "emerald",
    "left_title": "Nhiệm vụ 1: Soạn File 2 (thong_tin.html) & tạo thêm tệp",
    "left_image": "illus_10_hd3_nv1_tao_2_file.png",
    "left_caption": "Đặt id=\"CLBTT\" và link quay về CLB.html",
    "right_title": "Nhiệm vụ 2: Soạn File 1 (CLB.html) & nối liên kết",
    "right_image": "illus_10_hd3_nv2_gan_lien_ket_clb.png",
    "right_caption": "Gắn link chéo #CLBTT, URL https:// và neo #id"
  },
  {
    "kind": "visual_hero",
    "badge": "HOẠT ĐỘNG 4 • INFOGRAPHIC & VẬN DỤNG (15')",
    "title": "TỔNG KẾT BÀI 10 & VẬN DỤNG HỒ SƠ CLB ĐA TỆP",
    "sub": "AntV Infographic Studio & Câu hỏi SGK tr.61 (hd4.html)",
    "theme": "purple",
    "image": "illus_10_hd4_tong_ket_van_dung.png",
    "caption": "Ghi nhớ 4 quy tắc vàng & Thiết kế Website Hồ sơ thành viên (ho_so/an.html)"
  },
  {
    "kind": "thank_you",
    "title": "HOÀN THÀNH BÀI 10: TẠO LIÊN KẾT",
    "takeaways": [
      "Cú pháp: <a href=\"URL\">Nội dung chữ hoặc <img></a>.",
      "Ngoài: https://... • Nội bộ cùng website: tên tệp, thu_muc/tệp, ../tệp.",
      "Hoàn thành dự án ≥ 2 tệp trên hd3.html & Hồ sơ CLB tr.61 trên hd4.html."
    ]
  }
]
LESSON_SHORT = "Bài 10: Tạo liên kết"
OUT_PPTX_NAME = "Bai10_TrinhChieu.pptx"
LIGHT_MODE = True

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(here, "assets", "sgk")
    out_pptx = os.path.join(here, OUT_PPTX_NAME)
    build_from_slides_data(SLIDES_DATA, LESSON_SHORT, assets_dir, out_pptx, light_mode=LIGHT_MODE)
