"""Remove named text shapes from some slides of a PPTX export copy (the source PowerPoint is never changed).

A shape is removed only if its name matches --name and its text fully matches --text, so other
shapes on the slide are never touched. Run on the copy in the kenya-export folder before export_pdf.sh.

usage: python3 tools/drop_shapes.py <deck.pptx> --slides 43-57 --name "TextBox 24" --text "\\d{1,2}"
  (Day 1 part 1: the section numbers at the top left of the SYNAPSE slides)
"""
import argparse
import os
import re
import shutil
import tempfile
import zipfile

SP = re.compile(r'<p:sp>.*?</p:sp>', re.S)


def slide_range(spec):
    out = set()
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out.update(range(int(a), int(b or a) + 1))
    return out


def main(path, slides, name, text):
    src = zipfile.ZipFile(path)
    fixed = {}
    for n in sorted(slides):
        part = f'ppt/slides/slide{n}.xml'
        xml = src.read(part).decode('utf-8')

        def keep(m):
            e = m.group(0)
            nm = re.search(r'<p:cNvPr [^>]*name="([^"]*)"', e)
            t = ''.join(re.findall(r'<a:t>([^<]*)</a:t>', e)).strip()
            return '' if nm and nm.group(1) == name and re.fullmatch(text, t) else e

        new = SP.sub(keep, xml)
        if new != xml:
            fixed[part] = new
            print(f'slide {n}: removed {len(SP.findall(xml)) - len(SP.findall(new))} shape(s)')
        else:
            print(f'slide {n}: nothing to remove')
    if not fixed:
        return
    fd, tmp = tempfile.mkstemp(suffix='.pptx', dir=os.path.dirname(os.path.abspath(path)))
    os.close(fd)
    with zipfile.ZipFile(tmp, 'w') as out:
        for item in src.infolist():
            out.writestr(item, fixed[item.filename].encode('utf-8') if item.filename in fixed else src.read(item.filename))
    src.close()
    shutil.move(tmp, path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx')
    ap.add_argument('--slides', required=True, help='e.g. 43-57 or 3,5-7')
    ap.add_argument('--name', required=True, help='exact shape name')
    ap.add_argument('--text', required=True, help='regex the whole shape text must match')
    a = ap.parse_args()
    main(a.pptx, slide_range(a.slides), a.name, a.text)
