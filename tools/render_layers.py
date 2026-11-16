"""Render a day's PowerPoint PDF export into slide images.

usage: python3 tools/render_layers.py <day|key> <pdf-prefix> [--start N]   (--start: number slides from N)
  reads  <prefix>.pdf (the deck exported by PowerPoint, see export_pdf.sh)
  writes assets/day<day>/slides/sNN.jpg   the whole slide, exactly as PowerPoint draws it

The deck shows each image whole at 16:9, scaled to fit the screen (black bars elsewhere),
like a PowerPoint slideshow.
"""
import os
import subprocess
import sys
import tempfile

from deck import deck_dirs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 2400


def pages(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True, check=True).stdout
    return int(next(l.split()[-1] for l in out.splitlines() if l.startswith('Pages:')))


def main(day, prefix, start=1):
    pdf = f'{prefix}.pdf'
    n = pages(pdf)
    out_dir = os.path.join(ROOT, 'assets', deck_dirs(day)[0], 'slides')
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=88', '-scale-to-x', str(WIDTH), '-scale-to-y', '-1',
                        pdf, os.path.join(tmp, 'full')], check=True)
        w = len(str(n))  # pdftoppm pads page numbers to the page count's width
        for i in range(1, n + 1):
            os.replace(os.path.join(tmp, f'full-{i:0{w}d}.jpg'),
                       os.path.join(out_dir, f's{i + start - 1:02d}.jpg'))
    print(f'day {day}: {n} slides (s{start:02d}-s{start + n - 1:02d}) -> {out_dir}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == '--start' else 1)
