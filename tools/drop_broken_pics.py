"""Remove broken pictures (a picture shape with no image attached) from a PPTX export copy.

PowerPoint draws such a shape as a "The picture can't be displayed" box. Run this on the copy in
the kenya-export folder before export_pdf.sh; the source PowerPoint is never changed.

usage: python3 tools/drop_broken_pics.py <deck.pptx>
"""
import os
import re
import shutil
import sys
import tempfile
import zipfile

PIC = re.compile(r'<p:pic>.*?</p:pic>', re.S)
PART = re.compile(r'ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml$')


def broken(pic):
    return 'r:embed="' not in pic and 'r:link="' not in pic


def main(path):
    src = zipfile.ZipFile(path)
    fixed = {}
    for name in src.namelist():
        if PART.match(name):
            xml = src.read(name).decode('utf-8')
            new = PIC.sub(lambda m: '' if broken(m.group(0)) else m.group(0), xml)
            if new != xml:
                fixed[name] = new
                print(f'{name}: removed {len(PIC.findall(xml)) - len(PIC.findall(new))} broken picture(s)')
    if not fixed:
        print('no broken pictures')
        return
    fd, tmp = tempfile.mkstemp(suffix='.pptx', dir=os.path.dirname(os.path.abspath(path)))
    os.close(fd)
    with zipfile.ZipFile(tmp, 'w') as out:
        for item in src.infolist():
            data = fixed[item.filename].encode('utf-8') if item.filename in fixed else src.read(item.filename)
            out.writestr(item, data)
    src.close()
    shutil.move(tmp, path)


if __name__ == '__main__':
    main(sys.argv[1])
