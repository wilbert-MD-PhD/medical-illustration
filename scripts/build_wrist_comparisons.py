#!/usr/bin/env python3
"""Typeset documentary comparison plates from immutable reference images.

Requires reportlab and pypdfium2. Supply an installed, embeddable proportional
CJK TrueType font; no font binaries are distributed with the repository.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

import pypdfium2 as pdfium
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/showcase/wrist'
W, H = 1000, 600
INK, TEAL, MUTED = '#263A40', '#236C67', '#586A70'

BOARDS = [
    ('hand', '第1页：全手骨骼的分区', [
        ('artwork/B01.png', (0, 0, 1, 1), 'B01 · 全手掌面彩稿'),
        ('scaffolds/M01.png', (0, 0, 1, 1), 'M01 · 右手掌面模型投影'),
        ('references/gray219.jpg', (0, 0, 1, 1), 'Gray219 · 掌面骨骼图版')],
     '核对指骨、掌骨和腕骨的分区与邻接。右手侧别和机位由模型确定；Gray 原图保留原方向，不直接照搬屏幕左右。'),
    ('rows', '第2页：两排腕骨的邻接与遮挡', [
        ('artwork/B02.png', (.12, .20, .72, .66), 'B02 · 两排腕骨彩稿'),
        ('scaffolds/M02.png', (.12, .20, .72, .66), 'M02 · 右腕掌面模型投影'),
        ('references/gray219.jpg', (.27, 0, .75, .29), 'Gray219 · 掌面腕骨局部')],
     '核对近排、远排与豌豆骨的掌侧遮挡。教学色组和编号由制作另加；图谱与彩稿上下方向不同，均保留原貌。'),
    ('dorsal', '第3页：从背面观察腕骨', [
        ('artwork/B03.png', (0, 0, 1, 1), 'B03 · 腕骨背面彩稿'),
        ('scaffolds/M03.png', (0, 0, 1, 1), 'M03 · 右腕背面模型投影'),
        ('references/springer-p52.png', (.086, .073, .491, .386), '教材 Fig.4.18a · 背侧腕部')],
     '核对背面所见骨关系与遮挡。教材含背侧韧带，辅助核对骨性背景；Gray220 也曾附入原始生成，另见完整来源表。'),
    ('pisiform', '第3页：三角骨与豌豆骨的位置', [
        ('artwork/B04.png', (.19, .22, .44, .50), 'B04 · 豌豆骨与后方三角骨'),
        ('scaffolds/M04.png', (.19, .22, .44, .50), 'M04 · 掌尺侧模型投影'),
        ('references/springer-p52.png', (.086, .389, .491, .700), '教材 Fig.4.18b · 掌侧腕部')],
     '彩稿和模型按同一机位比较，教材补充掌侧位置关系。教材有韧带遮挡、观察角度不同，不作为裸骨轮廓的逐像素母版。'),
    ('interfaces', '第4–5页：桡侧关节面与尺侧关节盘', [
        ('artwork/B05.png', (.24, .36, .86, .73), 'B05 · 桡骨、舟月骨与关节盘'),
        ('scaffolds/M06.png', (.24, .36, .86, .73), 'M06 · 解释性冠状定位线稿'),
        ('references/gray336.png', (.19, .14, .72, .52), 'Gray336 · 腕关节冠状关系')],
     '核对桡骨、近排腕骨和尺侧关节盘。线稿用于定位；图谱近端在上、彩稿近端在下，均未镜像，不作为真实切片。'),
]


def lines(text, width, size):
    # Wrap Latin words as units, CJK at character boundaries; never justify text.
    tokens = re.findall(r'[A-Za-z0-9][A-Za-z0-9./_-]*|\s+|.', text)
    line = ''
    for token in tokens:
        if line and pdfmetrics.stringWidth(line + token, 'Body', size) > width:
            yield line.rstrip()
            line = token.lstrip()
        else:
            line += token
    if line:
        yield line.rstrip()


def text(c, x, top, value, size=15, color=INK, bold=False):
    c.setFillColor(HexColor(color))
    c.setFont('Heading' if bold else 'Body', size)
    c.drawString(x, H - top - size, value)


def image_clip(c, path, clip, x, top, width, height):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    left, upper, right, lower = clip
    assert 0 <= left < right <= 1 and 0 <= upper < lower <= 1
    cw, ch = iw * (right - left), ih * (lower - upper)
    scale = min(width / cw, height / ch)
    dx, dy = x + (width - cw * scale) / 2, H - top - height + (height - ch * scale) / 2
    c.saveState()
    region = c.beginPath()
    region.rect(dx, dy, cw * scale, ch * scale)
    c.clipPath(region, stroke=0)
    c.drawImage(image, dx - iw * left * scale, dy - ih * (1 - lower) * scale,
                width=iw * scale, height=ih * scale, mask='auto')
    c.restoreState()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--bold-font', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('Body', str(args.font)))
    pdfmetrics.registerFont(TTFont('Heading', str(args.bold_font or args.font)))
    # Detect the fixed-width Latin behavior that made the previous plates unreadable.
    assert pdfmetrics.stringWidth('iiii', 'Body', 14) < pdfmetrics.stringWidth('WWWW', 'Body', 14) * .6
    pdf_path = args.output / 'reference-details.pdf'
    c = canvas.Canvas(str(pdf_path), pagesize=(W, H), pageCompression=1)
    c.setTitle('腕骨与关节组成：五组解剖参考对照')
    c.setAuthor('wilbert; source attribution on each plate and in CREDITS.md')
    records = []
    for key, title, items, note in BOARDS:
        c.setFillColor(HexColor('#FFFFFF'))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        text(c, 32, 23, title, 26, TEAL, True)
        text(c, 32, 67, '展示用参考对照 · 原图保留观察方向 · 详细用途与原始附件见来源表', 14, MUTED)
        roles = ['漫画彩稿', '几何参考' if key != 'interfaces' else '定位线稿', '图谱 / 教材']
        for i, (fn, clip, caption) in enumerate(items):
            x, width = 32 + i * 320, 296
            text(c, x, 103, roles[i], 15, TEAL, True)
            image_clip(c, SOURCE / fn, clip, x + 8, 137, width - 16, 282)
            c.setStrokeColor(HexColor('#D9E4E3'))
            c.setLineWidth(.7)
            c.rect(x, H - 126 - 310, width, 310, fill=0, stroke=1)
            assert pdfmetrics.stringWidth(caption, 'Body', 15) <= width, caption
            text(c, x, 450, caption, 15)
            records.append({'board': key, 'source': fn, 'source_sha256': hashlib.sha256((SOURCE / fn).read_bytes()).hexdigest(),
                            'normalized_clip': clip, 'purpose': 'display_only_not_original_generation_attachment',
                            'transform': 'PDF clipping and proportional display; no rotation or mirror'})
        wrapped = list(lines(note, 936, 14))
        assert len(wrapped) <= 2, wrapped
        for i, value in enumerate(wrapped):
            text(c, 32, 493 + i * 22, value, 14, MUTED)
        c.setStrokeColor(HexColor('#D9E4E3'))
        c.line(32, H - 554, 968, H - 554)
        footer = ('BodyParts3D © DBCLS · Gray: Public Domain · 教材 © The Author(s) 2021, CC BY 4.0'
                  if key in ('dorsal', 'pisiform') else 'BodyParts3D © DBCLS · Gray: Public Domain')
        text(c, 32, 566, footer, 10.5, MUTED)
        text(c, 748, 566, '逐项许可见 CREDITS.md · 医学待审', 10.5, MUTED)
        c.showPage()
    c.save()
    doc = pdfium.PdfDocument(str(pdf_path))
    for index, (key, *_rest) in enumerate(BOARDS):
        page = doc[index]
        bitmap = page.render(scale=2)
        bitmap.to_pil().save(args.output / (key + '.png'))
        bitmap.close()
        page.close()
    doc.close()
    (args.output / 'crop-map.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'boards': len(BOARDS), 'source_placements': len(records), 'pdf_bytes': pdf_path.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    main()
