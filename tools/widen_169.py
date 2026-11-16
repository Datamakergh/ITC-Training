"""Widen a non-16:9 PPTX export copy (e.g. A4 landscape) to 16:9 so it fills the screen like the other decks.

The slide height stays the same and the width grows to height * 16 / 9. On every slide, layout and master:
  - full-width shapes (backgrounds, wave pictures) are stretched to the new width;
  - small shapes in the top or bottom right corner (logos) move with the right edge;
  - everything else moves right by half the extra width, so the content stays centred.
Text boxes keep their size, so no text re-wraps. Run on the copy in the kenya-export folder before
export_pdf.sh; the source PowerPoint is never changed.

usage: python3 tools/widen_169.py <deck.pptx>
"""
import os
import re
import shutil
import sys
import tempfile
import zipfile

PART = re.compile(r'ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml$')
SHAPES = {'p:sp', 'p:pic', 'p:grpSp', 'p:graphicFrame', 'p:cxnSp'}
TAG = re.compile(r'<(/?)([\w:]+)(?:\s[^>]*?)?(/?)>', re.S)
OFF = re.compile(r'<a:off x="(-?\d+)" y="(-?\d+)"/>(\s*<a:ext cx="(\d+)" cy="(\d+)"/>)?')


def top_shapes(xml):
    """(start, end) of each shape that is a direct child of p:spTree."""
    out, depth, start = [], None, None
    for m in TAG.finditer(xml):
        close, name, selfclose = m.group(1), m.group(2), m.group(3)
        if name == 'p:spTree':
            depth = 0 if not close else None
            continue
        if depth is None or selfclose:
            continue
        if not close:
            if depth == 0 and name in SHAPES:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None and name in SHAPES:
                out.append((start, m.end()))
                start = None
    return out


def widen(xml, w0, w1, h):
    pad = (w1 - w0) // 2
    pieces, last = [], 0
    for s, e in top_shapes(xml):
        shape = xml[s:e]
        m = OFF.search(shape)
        if m and m.group(4):
            x, y, cx, cy = int(m.group(1)), int(m.group(2)), int(m.group(4)), int(m.group(5))
            corner = y + cy <= 0.1 * h or y >= 0.9 * h            # top or bottom edge strip (logos)
            if x <= 0.02 * w0 and x + cx >= 0.98 * w0:          # full width: stretch
                nx, ncx = x, cx + (w1 - w0)
            elif corner and x >= 0.75 * w0 and cx <= 0.25 * w0:  # right-corner logo: keep at the right edge
                nx, ncx = x + 2 * pad, cx
            else:                                                 # content: keep centred
                nx, ncx = x + pad, cx
            new = f'<a:off x="{nx}" y="{m.group(2)}"/>' + m.group(3).replace(f'cx="{cx}"', f'cx="{ncx}"')
            shape = shape[:m.start()] + new + shape[m.end():]
        pieces += [xml[last:s], shape]
        last = e
    pieces.append(xml[last:])
    return ''.join(pieces)


def main(path):
    src = zipfile.ZipFile(path)
    pres = src.read('ppt/presentation.xml').decode('utf-8')
    m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres)
    w0, h = int(m.group(1)), int(m.group(2))
    w1 = round(h * 16 / 9)
    if abs(w0 - w1) < w1 * 0.005:
        print('already 16:9')
        return
    fixed = {'ppt/presentation.xml': pres.replace(m.group(0), f'<p:sldSz cx="{w1}" cy="{h}"', 1)}
    for name in src.namelist():
        if PART.match(name):
            fixed[name] = widen(src.read(name).decode('utf-8'), w0, w1, h)
    fd, tmp = tempfile.mkstemp(suffix='.pptx', dir=os.path.dirname(os.path.abspath(path)))
    os.close(fd)
    with zipfile.ZipFile(tmp, 'w') as out:
        for item in src.infolist():
            out.writestr(item, fixed[item.filename].encode('utf-8') if item.filename in fixed else src.read(item.filename))
    src.close()
    shutil.move(tmp, path)
    print(f'{path}: {w0} x {h} -> {w1} x {h} (16:9)')


if __name__ == '__main__':
    main(sys.argv[1])
