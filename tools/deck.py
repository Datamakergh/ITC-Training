"""Shared builder for the Kenya ITC HTML decks.

Each day script (day1.py, ...) builds a list of slide strings with the helpers
below and calls write_deck(). Styling, presenter JS and overlays are vendored
from the HQ Vietnam IAC package in tools/shell/ so every deck looks the same.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(ROOT, 'tools', 'shell')
META = os.path.join(ROOT, 'tools', 'meta')

PROGRAM = 'Data Labelling Training for AI'
PARTNERS = 'Kenya ITC &times; datamaker'
N_DAYS = 5

# Kenya-specific additions on top of the vendored HQ stylesheet.
EXTRA_CSS = """
/* ---- Kenya ITC additions ---- */
.icard-grid.compact{gap:14px}
.icard-grid.compact .icard{padding:16px 18px}
.icard-grid.compact .icard-ic{margin-bottom:8px}
.icard-grid.compact .icard-ic svg{width:26px;height:26px}
.icard-grid.compact .icard-t{font-size:16.5px;margin-bottom:4px}
.icard-grid.compact .icard-d{font-size:13.5px;line-height:1.4}
.agenda .a-row{padding:12px 4px}
.pr-title{line-height:1.14}
.icard-grid.cols-5{grid-template-columns:repeat(5,1fr)}
pre.code,.code-p{margin:0;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px;line-height:1.6;color:var(--text-1);white-space:pre-wrap}
.code-p{font-family:inherit;font-size:15px}
.prompt-box{background:var(--bg-soft);border:1px solid var(--border);border-radius:12px;padding:14px 18px;margin-bottom:12px}
.prompt-box.out{background:#fdf6dc;border-color:#ecdca0}
.prompt-box p{margin:0 0 8px;font-size:14.5px;line-height:1.55;color:var(--text-2)}
.prompt-box p:last-child{margin-bottom:0}
.prompt-box .pb-ask{color:var(--accent);font-weight:700}
.pb-label{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}
.prompt-box.out .pb-label{color:#8a6d00}
.vid-box{width:100%;max-width:760px;flex:0 1 430px;min-height:0;display:flex;flex-direction:column}
.vid-box>div{flex:1;min-height:0;display:flex}
.vid-box video{width:100%;height:100%;max-height:none!important;object-fit:contain}
.steps{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column;gap:12px}
.steps li{display:flex;align-items:flex-start;gap:14px;font-size:17px;line-height:1.5;color:var(--text-2)}
.steps .st-n{flex:0 0 auto;width:30px;height:30px;border-radius:9px;background:var(--accent);color:#fff;font-weight:800;font-size:14px;
  display:flex;align-items:center;justify-content:center;margin-top:-1px}
.journey{display:flex;align-items:stretch;gap:12px;margin:18px 0 14px}
.j-day{flex:1;border:1px solid var(--border);border-radius:12px;padding:14px 16px;background:var(--bg-soft);min-width:0}
.j-day.today{border-color:var(--accent);background:rgba(36,97,233,.05);box-shadow:var(--shadow)}
.j-label{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin-bottom:10px}
.j-day.today .j-label{color:var(--accent)}
.j-chips{display:flex;flex-direction:column;gap:6px}
.j-chips span{font-size:12.5px;font-weight:700;color:var(--text-1);background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:6px 9px;line-height:1.3}
.j-day.today .j-chips span{border-color:rgba(36,97,233,.45);color:var(--accent)}
@media print{ .j-day{-webkit-print-color-adjust:exact;print-color-adjust:exact} }
.a-tag{font-weight:700;font-size:12.5px;padding:4px 12px;border-radius:999px;color:var(--accent);background:rgba(36,97,233,.08)}
.a-tag.theory{color:var(--accent-2);background:var(--surface-2)}
.kbd{display:inline-flex;align-items:center;justify-content:center;min-width:26px;padding:2px 8px;border:1px solid var(--border-strong);
  border-bottom-width:3px;border-radius:7px;background:var(--surface);font-size:13px;font-weight:800;color:var(--text-1);font-family:inherit;white-space:nowrap}
.sc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px;flex:1;min-height:0}
.sc-card{background:var(--bg-soft);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;min-height:0}
.sc-head{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:9px}
.sc-row{display:flex;align-items:center;gap:10px;padding:5px 0;font-size:13.5px;color:var(--text-2);border-top:1px solid var(--border)}
.sc-row:first-of-type{border-top:none}
.sc-row .kbd{flex:0 0 auto}
.tree{display:flex;gap:22px;align-items:stretch;margin-top:14px}
.tree-root{flex:0 0 200px;display:flex;align-items:center;justify-content:center;background:var(--accent);color:#fff;border-radius:var(--radius);
  font-size:20px;font-weight:800;box-shadow:var(--shadow)}
.tree-kids{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tree-kid{background:var(--surface);border:1px solid var(--border);border-top:4px solid var(--accent);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow)}
.tree-kid b{display:block;font-size:17px;margin-bottom:10px}
.tree-kid span{display:inline-block;font-size:13px;font-weight:700;color:var(--accent);background:rgba(36,97,233,.08);border-radius:999px;padding:4px 11px;margin:0 6px 6px 0}
.tree-lvl{display:flex;gap:18px;margin-top:10px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--text-3)}
.warn-bar{border-left-color:var(--bad)}
.warn-bar b{color:var(--bad)}
.split-img{display:grid;grid-template-columns:1.1fr 1fr;gap:34px;align-items:center;flex:1;min-height:0}
.split-img img{width:100%;max-height:440px;object-fit:contain;border-radius:12px;box-shadow:var(--shadow)}
.link-chip{display:inline-flex;align-items:center;gap:8px;margin-top:10px;font-size:15px;font-weight:700;color:var(--accent);
  background:rgba(36,97,233,.08);border:1px solid rgba(36,97,233,.25);border-radius:999px;padding:7px 16px;text-decoration:none}
"""

# Lucide-style stroke icons (same drawing style as the HQ decks).
ICONS = {
    'layers': '<path d="M12 3 2 9l10 6 10-6-10-6Z"/><path d="m2 15 10 6 10-6"/><path d="m2 12 10 6 10-6"/>',
    'box': '<path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/>',
    'target': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
    'arrow': '<path d="M4 12h16M14 6l6 6-6 6"/>',
    'star': '<path d="M12 2.5 15 9l7 1-5 5 1.3 7.5L12 19l-6.3 3.5L7 15l-5-5 7-1 3-6.5Z"/>',
    'monitor': '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 18v3"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'keyboard': '<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
    'pen': '<path d="M4 20h4L18.5 9.5a2.1 2.1 0 0 0-3-3L5 17v3Z"/><path d="M14 6.5 17.5 10"/>',
    'shield': '<path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
    'alert': '<path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17h.01"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    'car': '<path d="M5 16h14M6 16l1.5-5h9L18 16"/><circle cx="8" cy="17.5" r="1.5"/><circle cx="16" cy="17.5" r="1.5"/>',
    'list': '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.6 2.6L16 9.5"/>',
    'x': '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
    'hand': '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12"/><path d="M11 11.5V4a1.5 1.5 0 0 1 3 0v7.5"/><path d="M14 11.5V6a1.5 1.5 0 0 1 3 0v8c0 4-2.7 7-6.5 7S5 18.5 4.2 16L3 12.5a1.5 1.5 0 0 1 2.7-1.2L8 14"/>',
    'clipboard': '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6"/>',
    'folder': '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"/>',
    'trend': '<path d="M4 16 10 10l4 4 6-7"/><path d="M15 7h5v5"/>',
    'cube': '<path d="M12 2.5 3 7v10l9 4.5 9-4.5V7l-9-4.5Z"/><path d="M3 7l9 4.5L21 7M12 11.5V21.5"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4V5Z"/>',
    'code': '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    'image': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="m21 16-5-5-9 9"/>',
}


def esc(s):
    return html.escape(s, quote=False)


def icon(name, size=24, cls=''):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def deco(name, size=110):
    return (f'<div class="title-deco"><svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.1">{ICONS[name]}</svg></div>')


def chrome(kicker):
    return ('<div class="deck-chrome">\n'
            '      <div class="dc-left"><span class="dc-logo"><img class="logo-light" src="assets/logo.svg" alt="datamaker">'
            '<img class="logo-dark" src="assets/logo-white.svg" alt="datamaker"></span><span class="dc-sep">|</span>'
            f'<span class="dc-kicker">{kicker}</span></div>\n'
            '      <div class="dc-right"><span class="slide-num" data-n=""></span></div>\n'
            '    </div>')


def plain_dashes(text):
    """House style: no em dashes. Used on notes copied from the PPTX files."""
    return text.replace(' — ', ', ').replace('—', ', ').replace('&mdash;', ', ')


def slide(sid, title, kicker, body, cls='light', notes='', body_style=''):
    notes = plain_dashes(notes)
    st = f' style="{body_style}"' if body_style else ''
    return (f'<section class="slide {cls}" id="{sid}" data-title="{esc(title)}">{chrome(kicker)}'
            f'<div class="slide-body"{st}>\n{body}\n</div><div class="notes" data-slide="">{esc(notes)}</div></section>')


# ---------- slide types ----------

def title_slide(sid, day, h1, sub, meta, wm=None, notes=''):
    meta_html = ''.join(f'<div>{icon(ic, 18)}<span>{t}</span></div>' for ic, t in meta)
    body = f'''  <div class="title-wm">{wm or f"{day:02d}"}</div>
  <div class="title-day">Day {day} of {N_DAYS} &nbsp;&middot;&nbsp; {PROGRAM}</div>
  <h1 class="title-h1">{h1}</h1>
  <p class="title-sub">{sub}</p>
  <div class="title-meta">{meta_html}</div>
  {deco('box', 120)}'''
    return slide(sid, 'Title', f'Day {day}', body, 'dark title-slide', notes)


def section(sid, title, kicker, lede='', ic='layers', deco_ic='box', notes='', data_title=None):
    body = f'''<div class="sec-wrap">
      <div class="sec-num">{icon(ic, 44)}</div>
      <div class="eyebrow">{kicker}</div>
      <h1 class="h1 sec-title">{title}</h1>
      {f'<p class="lede">{lede}</p>' if lede else ''}
    </div>{deco(deco_ic)}'''
    return slide(sid, data_title or title, kicker, body, 'dark section-slide', notes)


def guide(sid, title, kicker, img, notes=''):
    body = f'  <img class="guide-img" src="{img}" alt="{esc(title)}" loading="lazy">'
    return slide(sid, title, kicker, body, 'light guide', notes)


def content(sid, title, kicker, inner, eyebrow=None, notes='', h='h2', cls='light'):
    body = f'''  <div class="eyebrow">{eyebrow or kicker}</div>
  <h2 class="{h}">{title}</h2>
{inner}'''
    return slide(sid, title, kicker, body, cls, notes)


def practice(sid, title, sub, checks, kicker='Hands-on', notes=''):
    chips = ''.join(f'<span>{c}</span>' for c in checks)
    body = f'''<div class="pr-wrap">
      <span class="pr-badge">{icon('pen', 17)}Practice in progress</span>
      <h1 class="pr-title">{title}</h1>
      <p class="pr-sub">{sub}</p>
      <div class="pr-checks">{chips}</div>
      <div class="pr-help">Raise your hand at any time.</div>
    </div>'''
    return slide(sid, 'Labelling Practice', kicker, body, 'practice', notes)


# ---------- components ----------

def bullets(items):
    return '<ul class="bl">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def icards(cards, cols=3, extra=''):
    out = ''.join(f'<div class="icard"><div class="icard-ic">{icon(ic, 28)}</div>\n'
                  f'        <div class="icard-t">{t}</div><div class="icard-d">{d}</div></div>' for ic, t, d in cards)
    return f'  <div class="icard-grid cols-{cols} {extra}">{out}</div>'


def note(text, ic='star', warn=False):
    return f'  <div class="note-bar{" warn-bar" if warn else ""}">{icon(ic, 18)} {text}</div>'


def pipe(steps):
    parts = []
    for i, (t, d) in enumerate(steps):
        if i:
            parts.append(f'<div class="parrow">{icon("arrow", 20)}</div>')
        parts.append(f'<div class="pnode"><div class="pn-badge">{i + 1}</div>\n'
                     f'          <div class="pn-t">{t}</div><div class="pn-d">{d}</div></div>')
    return '  <div class="pipe">' + ''.join(parts) + '</div>'


def checklist(items):
    rows = ''.join(
        f'<li><span class="cl-ic {"good" if ok else "warn"}">{icon("check" if ok else "x", 20)}</span><span>{t}</span></li>'
        for ok, t in items)
    return f'  <ul class="checklist">{rows}</ul>'


def agenda(rows):
    out = ''
    for i, (t, tag) in enumerate(rows):
        cls = 'theory' if tag == 'Theory' else ''
        out += (f'<div class="a-row"><div class="a-idx">{i + 1}</div><div class="a-title">{t}</div>'
                f'<div class="a-tag {cls}">{tag}</div></div>')
    return f'  <div class="agenda">{out}</div>'


DAYS = [
    ('Day 1', ['Synapse Dashboard', 'Bounding Box', 'CCTV BBox Project']),
    ('Day 2', ['Polyline', 'Polygon', 'Traffic Flow', 'Rail &amp; Catenary']),
    ('Day 3', ['Semantic Segmentation', 'PCD (3D point cloud)', 'Photobooth Project']),
    ('Day 4', ['Interior Segmentation', 'Photobooth Project', 'Generative AI', 'Prompt Engineering']),
    ('Day 5', ['Vibe Coding']),
]


def journey(today):
    out = []
    for i, (label, chips) in enumerate(DAYS):
        cls = ' today' if i + 1 == today else ''
        out.append(f'<div class="j-day{cls}"><div class="j-label">{label}{" &middot; Today" if cls else ""}</div>'
                   f'<div class="j-chips">{"".join(f"<span>{c}</span>" for c in chips)}</div></div>')
    return '  <div class="journey">' + ''.join(out) + '</div>'


def kbd(k):
    return f'<span class="kbd">{k}</span>'


# ---------- source decks ----------

def meta(deck):
    """Slide text / notes extracted from a source PPTX (tools/meta/<deck>.json)."""
    with open(os.path.join(META, deck + '.json'), encoding='utf-8') as f:
        return {s['n']: s for s in json.load(f)}


class Source:
    """Turns original PPT slides into guide slides, carrying their notes along."""

    def __init__(self, day, deck):
        self.day, self.deck = day, deck
        self.m = meta(f'd{day}-{deck}')

    def img(self, n):
        return f'assets/day{self.day}/{self.deck}/s{n:02d}.jpg'

    def notes(self, n):
        return self.m[n]['notes']

    def guide(self, n, title, kicker):
        return guide(f'{self.deck}-s{n:02d}', title, kicker, self.img(n), self.notes(n))

    def guides(self, items, kicker):
        """items: list of (slide number, title)."""
        return [self.guide(n, t, kicker) for n, t in items]


# ---------- output ----------

def write_deck(filename, page_title, slides, num_offset=0, other=0):
    with open(os.path.join(SHELL, 'base.css'), encoding='utf-8') as f:
        css = f.read()
    with open(os.path.join(SHELL, 'overlays.html'), encoding='utf-8') as f:
        overlays = f.read()
    with open(os.path.join(SHELL, 'deck.js'), encoding='utf-8') as f:
        js = f.read().replace('__NUM_OFFSET__', str(num_offset)).replace('__OTHER__', str(other))
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page_title}</title>
<style>
{css}{EXTRA_CSS}</style>
</head>
<body class="">
<div class="deck">

{chr(10).join(slides)}
{overlays}
<script>
{js}</script>
</body>
</html>
'''
    if '—' in doc or '&mdash;' in doc:
        raise SystemExit(f'{filename}: em dash found; rewrite the sentence')
    with open(os.path.join(ROOT, filename), 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'{filename}: {len(slides)} slides')
    return len(slides)


# ---------- shared slide patterns ----------

def media(src, alt):
    """Image, or looping video with a still for print (video stills share the .mp4 name with .jpg)."""
    if src.endswith('.mp4'):
        return (f'<div><video src="{src}" autoplay muted loop playsinline style="width:100%;max-height:440px;border-radius:12px;'
                f'box-shadow:var(--shadow);display:block;background:#000"></video>'
                f'<img class="print-only" src="{src[:-4]}.jpg" alt="{alt}"></div>')
    return f'<img src="{src}" alt="{alt}">'


def split_media(sid, title, kicker, text_html, src, eyebrow=None, notes=''):
    return content(sid, title, kicker, f'''
  <div class="split-img">
    <div>{text_html}</div>
    {media(src, title)}
  </div>''', eyebrow=eyebrow, notes=notes)


def ip_notice(sid, kicker, notes=''):
    """The 'this file is for training datamaker workers' warning that opens each project guideline."""
    return content(sid, 'Before You Start', kicker, f'''
  <div class="cmp-col" style="max-width:860px"><div class="cmp-head">{icon("shield")}<span>Training Material</span></div>
    <ul class="bl"><li>This file is intended for training <b>datamaker</b> workers.</li>
    <li>All images and content used are the intellectual property of datamaker. Unauthorised distribution and reproduction may be subject to legal sanctions.</li></ul></div>''',
                   eyebrow='Warning', notes=notes)


def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'  <table class="dtbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def img_row(items, height=260):
    """items: list of (src, caption). Images side by side with captions."""
    figs = ''.join(f'<figure class="sol-fig" style="flex:1;min-width:0"><img src="{s}" alt="{c}" style="height:{height}px;object-fit:contain;background:#fff">'
                   f'<figcaption>{c}</figcaption></figure>' for s, c in items)
    return f'  <div style="display:flex;gap:16px;margin-top:14px">{figs}</div>'


def steps_list(items):
    return '  <ol class="steps">' + ''.join(f'<li><span class="st-n">{n}</span><span>{i}</span></li>' for n, i in enumerate(items, 1)) + '</ol>'
