"""Render the layer PDFs of a day into slide images.

usage: python3 tools/render_layers.py <day> <pdf-prefix>
  reads  <prefix>.pdf (the deck as is) and <prefix>-bg.pdf, <prefix>-fgw.pdf, <prefix>-fgb.pdf
         (from split_layers.py + export_pdf.sh)
  writes assets/day<day>/bg/sNN.jpg       background (fills the screen, cropped as needed)
         assets/day<day>/slides/sNN.png   content with transparency (always shown whole, 16:9)
         assets/day<day>/slides/sNN.jpg   the whole slide (used when the background is a flat colour)

The content transparency is recovered by difference matting: the same content exported on white
and on black differs exactly where it is transparent. alpha = 1 - (white - black), colour = black / alpha.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 2400
MATTE = ('[0]format=gbrp[w];[1]format=gbrp,split[b1][b2];'
         '[w][b1]blend=all_mode=difference,format=gray,negate[a];'
         '[b2][a]alphamerge,unpremultiply=inplace=1,format=rgba')


def pages(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True, check=True).stdout
    return int(next(l.split()[-1] for l in out.splitlines() if l.startswith('Pages:')))


def main(day, prefix):
    pdfs = {k: f'{prefix}-{k}.pdf' for k in ('bg', 'fgw', 'fgb')}
    pdfs['full'] = f'{prefix}.pdf'
    counts = {k: pages(p) for k, p in pdfs.items()}
    if len(set(counts.values())) != 1:
        raise SystemExit(f'page counts differ: {counts}')
    n = counts['bg']
    bg_dir = os.path.join(ROOT, 'assets', f'day{day}', 'bg')
    fg_dir = os.path.join(ROOT, 'assets', f'day{day}', 'slides')
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(fg_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=85', '-scale-to-x', str(WIDTH), '-scale-to-y', '-1',
                        pdfs['bg'], os.path.join(tmp, 'bg')], check=True)
        subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=88', '-scale-to-x', str(WIDTH), '-scale-to-y', '-1',
                        pdfs['full'], os.path.join(tmp, 'full')], check=True)
        for k in ('fgw', 'fgb'):
            subprocess.run(['pdftoppm', '-png', '-scale-to-x', str(WIDTH), '-scale-to-y', '-1',
                            pdfs[k], os.path.join(tmp, k)], check=True)
        w = len(str(n))  # pdftoppm pads page numbers to the page count's width
        for i in range(1, n + 1):
            tag = f'{i:0{w}d}'
            os.replace(os.path.join(tmp, f'bg-{tag}.jpg'), os.path.join(bg_dir, f's{i:02d}.jpg'))
            os.replace(os.path.join(tmp, f'full-{tag}.jpg'), os.path.join(fg_dir, f's{i:02d}.jpg'))
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(tmp, f'fgw-{tag}.png'),
                            '-i', os.path.join(tmp, f'fgb-{tag}.png'), '-filter_complex', MATTE,
                            os.path.join(fg_dir, f's{i:02d}.png')], check=True)
    print(f'day {day}: {n} slides -> {bg_dir}, {fg_dir}')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
