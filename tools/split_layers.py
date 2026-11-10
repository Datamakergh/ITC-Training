"""Split a PPTX into a background deck and a content deck, so each slide can be shown as two
layers: the background covers the whole screen, the content keeps the slide's exact shape.

usage: python3 tools/split_layers.py <in.pptx> <out-prefix>

Background = the slide/layout/master fill plus any full-bleed shape or picture (one that covers
the whole slide, like the wave artwork). Content = everything else, on a transparent background.
Nothing is redrawn: both decks are the original XML with some shapes hidden, exported by PowerPoint.
"""
import re
import sys
import zipfile

TOP = ('p:sp', 'p:pic', 'p:grpSp', 'p:graphicFrame', 'p:cxnSp', 'p:contentPart', 'mc:AlternateContent')


def children(tree):
    """Top-level shape elements inside <p:spTree>…</p:spTree>: list of (start, end, xml)."""
    out, i = [], 0
    pat = re.compile(r'<(%s)[\s>/]' % '|'.join(re.escape(t) for t in TOP))
    while True:
        m = pat.search(tree, i)
        if not m:
            return out
        tag, start = m.group(1), m.start()
        if tree[start:tree.index('>', start) + 1].endswith('/>'):
            end = tree.index('>', start) + 1
        else:
            depth, j = 0, start
            rx = re.compile(r'<%s[\s>/]|</%s>' % (re.escape(tag), re.escape(tag)))
            while True:
                n = rx.search(tree, j)
                if n.group(0).startswith('</'):
                    depth -= 1
                    if depth == 0:
                        end = n.end()
                        break
                else:
                    close = tree.index('>', n.start())
                    if tree[close - 1] != '/':
                        depth += 1
                j = n.end()
        out.append((start, end, tree[start:end]))
        i = end


def full_bleed(el, sw, sh):
    if '<p:ph' in el:
        return False
    m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"', el)
    if not m:
        return False
    x, y, w, h = map(int, m.groups())
    return x <= sw * 0.005 and y <= sh * 0.005 and x + w >= sw * 0.995 and y + h >= sh * 0.995


def rewrite(xml, sw, sh, content, bg_fill=None):
    """Background mode keeps only full-bleed artwork. Content mode hides full-bleed artwork and
    everything it covers (shapes below it, and layout/master shapes), and can replace every
    background with a solid colour."""
    a = xml.index('<p:spTree>')
    b = xml.index('</p:spTree>')
    tree = xml[a:b]
    kids = children(tree)
    bleed = [full_bleed(el, sw, sh) for _, _, el in kids]
    top = max((i for i, f in enumerate(bleed) if f), default=-1)  # highest full-bleed shape
    parts, last = [], 0
    for i, (s, e, el) in enumerate(kids):
        parts.append(tree[last:s])
        show = (not bleed[i] and i > top) if content else bleed[i]
        if show:
            parts.append(el)
        else:  # hide rather than delete: PowerPoint flags decks with removed shapes for repair
            parts.append(re.sub(r'<p:cNvPr (?![^>]*hidden=)', '<p:cNvPr hidden="1" ', el))
        last = e
    parts.append(tree[last:])
    xml = xml[:a] + ''.join(parts) + xml[b:]
    if content and top >= 0:  # layout/master shapes are under the full-bleed artwork too
        xml = re.sub(r'<p:(sld|sldLayout)\b(?![^>]*showMasterSp=)', r'<p:\1 showMasterSp="0"', xml, count=1)
    if bg_fill and '<p:bg>' in xml:  # parts without <p:bg> inherit the master's, which is replaced too
        solid = f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg_fill}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
        xml = re.sub(r'<p:bg>.*?</p:bg>', solid, xml, count=1, flags=re.S)
    return xml


def main(src, prefix):
    """Writes <prefix>-bg.pptx (background only) and <prefix>-fgw.pptx / <prefix>-fgb.pptx (content
    only, on pure white / pure black). PowerPoint's PDF export always paints the page, so the content
    layer's transparency is recovered afterwards by comparing the white and black versions."""
    z = zipfile.ZipFile(src)
    sw, sh = map(int, re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', z.read('ppt/presentation.xml').decode()).groups())
    part = re.compile(r'ppt/(slides/slide|slideLayouts/slideLayout|slideMasters/slideMaster)\d+\.xml$')
    outs = {
        'bg': lambda xml: rewrite(xml, sw, sh, False),
        'fgw': lambda xml: rewrite(xml, sw, sh, True, 'FFFFFF'),
        'fgb': lambda xml: rewrite(xml, sw, sh, True, '000000'),
    }
    zips = {k: zipfile.ZipFile(f'{prefix}-{k}.pptx', 'w') for k in outs}
    for info in z.infolist():
        data = z.read(info.filename)
        xml = data.decode('utf-8') if part.match(info.filename) else None
        for k, fn in outs.items():
            # each archive needs its own entry record (writestr fills in offsets and checksums)
            zi = zipfile.ZipInfo(info.filename, info.date_time)
            zi.compress_type = zipfile.ZIP_STORED if info.filename.startswith('ppt/media/') else zipfile.ZIP_DEFLATED
            zips[k].writestr(zi, fn(xml).encode('utf-8') if xml is not None else data)
    for zf in zips.values():
        zf.close()


if __name__ == '__main__':
    main(*sys.argv[1:3])
