"""Extract slide metadata and animated media (GIF / video) from a PPTX.

usage: python3 tools/extract_pptx.py <day> <deck.pptx>

Writes tools/meta/d<day>-slides.json and copies media into assets/day<day>/media/:
  - GIFs unchanged
  - videos re-encoded to H.264 MP4 (web size, trimmed as in the PPTX), plus a poster .jpg;
    Day 2 and Day 3 videos have their sound removed (NO_AUDIO_DAYS)

Per slide: title (for the overview), all slide text (image alt text), speaker notes, and
each GIF / video with its frame as % of the slide, its crop (srcRect) and playback flags.
"""
import json
import os
import posixpath
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
}
R = '{%s}' % NS['r']
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
# Days whose videos are published without sound.
NO_AUDIO_DAYS = {2, 3}
ANIM = re.compile(r'\.(gif|mp4|mov|m4v|avi|wmv)$', re.I)


def rels(z, part):
    path = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
    if path not in z.namelist():
        return {}
    out = {}
    for r in ET.fromstring(z.read(path)).findall('{%s}Relationship' % REL):
        t = r.get('Target')
        if r.get('TargetMode') != 'External':
            t = posixpath.normpath(posixpath.join(posixpath.dirname(part), t))
        out[r.get('Id')] = (t, r.get('Type', ''))
    return out


def para_text(el):
    lines = []
    for p in el.iter('{%s}p' % NS['a']):
        s = ''.join(t.text or '' for t in p.iter('{%s}t' % NS['a']))
        if s.strip():
            lines.append(s.strip())
    return lines


def xfrm_box(el):
    x = el.find('a:xfrm', NS)
    if x is None:
        return None
    off, ext = x.find('a:off', NS), x.find('a:ext', NS)
    box = [int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))]
    ch_off, ch_ext = x.find('a:chOff', NS), x.find('a:chExt', NS)
    child = None
    if ch_off is not None:
        child = [int(ch_off.get('x')), int(ch_off.get('y')), int(ch_ext.get('cx')), int(ch_ext.get('cy'))]
    return box, child, int(x.get('rot', 0))


def walk(tree, transforms, out):
    """Yield (pic element, absolute box) for every picture, applying group transforms."""
    for el in tree:
        tag = el.tag.split('}')[1]
        if tag == 'grpSp':
            box, child, _ = xfrm_box(el.find('p:grpSpPr', NS))
            walk(el, transforms + [(box, child)], out)
        elif tag == 'pic':
            box, _, rot = xfrm_box(el.find('p:spPr', NS))
            x, y, w, h = box
            for gbox, gchild in reversed(transforms):
                sx = gbox[2] / gchild[2] if gchild[2] else 1
                sy = gbox[3] / gchild[3] if gchild[3] else 1
                x = gbox[0] + (x - gchild[0]) * sx
                y = gbox[1] + (y - gchild[1]) * sy
                w, h = w * sx, h * sy
            out.append((el, (x, y, w, h), rot))
        elif tag == 'AlternateContent':
            choice = el.find('{http://schemas.openxmlformats.org/markup-compatibility/2006}Choice')
            walk(choice if choice is not None else el, transforms, out)


def media_timing(root, spid):
    """Return (autoplay, loop, muted) for a video shape from the slide's p:timing."""
    timing = root.find('p:timing', NS)
    autoplay, loop, muted = False, False, False
    if timing is None:
        return autoplay, loop, muted
    for v in timing.iter('{%s}video' % NS['p']):
        node = v.find('p:cMediaNode', NS)
        tgt = node.find('.//p:spTgt', NS)
        if tgt is None or tgt.get('spid') != spid:
            continue
        muted = node.get('mute') == '1'
        ctn = node.find('p:cTn', NS)
        if ctn is not None and ctn.get('repeatCount') == 'indefinite':
            loop = True
    for cmd in timing.iter('{%s}cmd' % NS['p']):
        tgt = cmd.find('.//p:spTgt', NS)
        if tgt is None or tgt.get('spid') != spid or not (cmd.get('cmd') or '').startswith('playFrom'):
            continue
        # walk up: the enclosing effect's nodeType tells click vs automatic
        parent_map = {c: p for p in timing.iter() for c in p}
        n = cmd
        while n is not None:
            ctn = n.find('p:cTn', NS) if n.tag.endswith('}par') else None
            if ctn is not None and ctn.get('nodeType') in ('clickEffect', 'afterEffect', 'withEffect'):
                autoplay = ctn.get('nodeType') != 'clickEffect'
                # an effect in the first click group with no delay after slide start counts as automatic
                break
            n = parent_map.get(n)
    return autoplay, loop, muted


def ffprobe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height:format=duration',
                          '-of', 'json', path], capture_output=True, text=True).stdout
    return json.loads(out)


def encode_video(src, dst, trim, keep_audio=True):
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        return
    info = ffprobe(src)
    has_audio = keep_audio and any(s['codec_type'] == 'audio' for s in info['streams'])
    cmd = ['ffmpeg', '-y', '-v', 'error']
    if trim and trim[0]:
        cmd += ['-ss', f'{trim[0] / 1000:.3f}']
    cmd += ['-i', src]
    if trim and trim[1]:
        dur = float(info['format']['duration']) - trim[1] / 1000 - (trim[0] or 0) / 1000
        cmd += ['-t', f'{dur:.3f}']
    cmd += ['-vf', "scale='min(1920,iw)':-2,format=yuv420p", '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
            '-movflags', '+faststart']
    cmd += ['-c:a', 'aac', '-b:a', '128k'] if has_audio else ['-an']
    subprocess.run(cmd + [dst], check=True)


def main(day, pptx):
    z = zipfile.ZipFile(pptx)
    sw, sh = map(int, re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', z.read('ppt/presentation.xml').decode()).groups())
    pres = ET.fromstring(z.read('ppt/presentation.xml'))
    prel = rels(z, 'ppt/presentation.xml')
    order = [prel[s.get(R + 'id')][0] for s in pres.find('p:sldIdLst', NS)]
    mdir = os.path.join(ROOT, 'assets', f'day{day}', 'media')
    os.makedirs(mdir, exist_ok=True)
    tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), f'kenya-d{day}-media')
    os.makedirs(tmp, exist_ok=True)

    slides = []
    for n, part in enumerate(order, 1):
        root = ET.fromstring(z.read(part))
        srel = rels(z, part)
        hidden = root.get('show') == '0'
        tree = root.find('p:cSld/p:spTree', NS)

        title = ''
        for sp in tree.iter('{%s}sp' % NS['p']):
            ph = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
            if ph is not None and ph.get('type') in ('title', 'ctrTitle'):
                title = ' '.join(para_text(sp))
                break
        text = para_text(tree)
        if not title:
            title = text[0] if text else ''

        notes = ''
        for t, typ in srel.values():
            if typ.endswith('/notesSlide'):
                nroot = ET.fromstring(z.read(t))
                for sp in nroot.iter('{%s}sp' % NS['p']):
                    ph = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
                    if ph is not None and ph.get('type') == 'body':
                        notes = '\n'.join(para_text(sp))

        pics = []
        walk(tree, [], pics)
        media = []
        for pic, (x, y, w, h), rot in pics:
            nv = pic.find('p:nvPicPr', NS)
            spid = nv.find('p:cNvPr', NS).get('id')
            blip = pic.find('p:blipFill/a:blip', NS)
            embed = srel.get(blip.get(R + 'embed'), ('', ''))[0] if blip is not None else ''
            vid = nv.find('p:nvPr/a:videoFile', NS)
            p14 = nv.find('p:nvPr/p:extLst/p:ext/p14:media', NS)
            target = None
            if p14 is not None and p14.get(R + 'embed') in srel:
                target = srel[p14.get(R + 'embed')][0]
            elif vid is not None and vid.get(R + 'link') in srel:
                target = srel[vid.get(R + 'link')][0]
            kind = None
            if target and ANIM.search(target):
                kind = 'video'
            elif ANIM.search(embed) and embed.lower().endswith('.gif'):
                kind, target = 'gif', embed
            if not kind:
                continue
            sr = pic.find('p:blipFill/a:srcRect', NS)
            crop = {k: int(sr.get(k, 0)) / 100000 if sr is not None else 0 for k in 'ltrb'}
            item = {'kind': kind, 'box': [x / sw * 100, y / sh * 100, w / sw * 100, h / sh * 100],
                    'crop': crop, 'rot': rot / 60000}
            base = os.path.splitext(posixpath.basename(target))[0]
            if kind == 'gif':
                name = f'{base}.gif'
                with open(os.path.join(mdir, name), 'wb') as f:
                    f.write(z.read(target))
                item['src'] = f'assets/day{day}/media/{name}'
            else:
                trim_el = p14.find('p14:trim', NS) if p14 is not None else None
                trim = None
                if trim_el is not None:
                    trim = (float(trim_el.get('st', 0)), float(trim_el.get('end', 0)))
                raw = os.path.join(tmp, posixpath.basename(target))
                if not os.path.exists(raw):
                    with z.open(target) as fi, open(raw, 'wb') as fo:
                        while chunk := fi.read(1 << 22):
                            fo.write(chunk)
                encode_video(raw, os.path.join(mdir, f'{base}.mp4'), trim, keep_audio=day not in NO_AUDIO_DAYS)
                poster = f'{base}-poster.jpg'
                with open(os.path.join(tmp, 'poster' + os.path.splitext(embed)[1]), 'wb') as f:
                    f.write(z.read(embed))
                subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f.name, '-q:v', '3', os.path.join(mdir, poster)], check=True)
                autoplay, loop, muted = media_timing(root, spid)
                item.update(src=f'assets/day{day}/media/{base}.mp4', poster=f'assets/day{day}/media/{poster}',
                            autoplay=autoplay, loop=loop, muted=muted, trim=trim)
            media.append(item)
        slides.append({'n': n, 'hidden': hidden, 'title': title, 'text': text, 'notes': notes, 'media': media})
        if media:
            print(f's{n:02d}', [(m['kind'], m['src'].rsplit('/', 1)[1], m.get('autoplay'), m.get('loop')) for m in media])

    out = os.path.join(ROOT, 'tools', 'meta', f'd{day}-slides.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(slides, f, ensure_ascii=False, indent=1)
    print(f'{out}: {len(slides)} slides, {sum(s["hidden"] for s in slides)} hidden')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
