"""Builder for decks shown exactly as the PowerPoint, filling any screen without stretching.

Each slide is two layers exported by PowerPoint (split_layers.py, export_pdf.sh, render_layers.py):
  assets/day<day>/bg/sNN.jpg      the slide background (fill + full-bleed artwork): covers the screen
  assets/day<day>/slides/sNN.png  everything else, transparent: shown whole at the slide's 16:9 shape
  assets/day<day>/slides/sNN.jpg  the whole original slide, used instead when the background is one
                                  flat colour (nothing to extend, and no matting edges)
plus the slide's GIFs and videos placed on top at their PowerPoint position and crop
(assets/day<day>/media/*, positions in tools/meta/d<day>-slides.json from extract_pptx.py).

Nothing is added to or dropped from the source deck: one HTML slide per PPTX slide, in order.
"""
import html
import json
import os
import subprocess

from deck import ROOT, SHELL, META, plain_dashes

CSS = """
/* ---- full-slide decks ----
   The slide's own background artwork covers the whole screen (cropped, never stretched). The slide
   content sits on it at its exact 16:9 shape, below a transparent top bar (day links + counter). */
.slide.fullslide{background:#fff;color:var(--fg)}
.fs-bg{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;display:block;z-index:0;user-select:none;
  transform:scale(1.006)}  /* hides the 1-2px seam PowerPoint leaves on some artwork edges */
.fs-top{flex:0 0 clamp(34px,4.4vh,48px);display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:0 clamp(14px,2vw,28px);color:var(--fg);font-family:Pretendard,'Inter',system-ui,sans-serif;
  font-size:clamp(12px,1.5vh,15px);position:relative;z-index:3}
.fs-menu{display:flex;align-items:center;gap:clamp(6px,1vw,12px);min-width:0}
.fs-burger{flex:0 0 auto;display:flex;flex-direction:column;justify-content:center;gap:4px;width:34px;height:30px;padding:0 8px;
  border:0;border-radius:8px;background:transparent;color:inherit;cursor:pointer;opacity:.7}
.fs-burger span{display:block;height:2px;border-radius:2px;background:currentColor;transition:transform .2s ease,opacity .2s ease}
.fs-burger:hover,.fs-burger:focus-visible{opacity:1;background:var(--hl);outline:none}
body.nav-open .fs-burger{opacity:1;background:var(--hl)}
body.nav-open .fs-burger span:nth-child(1){transform:translateY(6px) rotate(45deg)}
body.nav-open .fs-burger span:nth-child(2){opacity:0}
body.nav-open .fs-burger span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.fs-nav{display:flex;align-items:center;gap:clamp(4px,.8vw,10px);min-width:0;overflow:hidden;
  opacity:0;visibility:hidden;transform:translateX(-8px);transition:opacity .2s ease,transform .2s ease,visibility 0s linear .2s}
body.nav-open .fs-nav{opacity:1;visibility:visible;transform:none;transition:opacity .2s ease,transform .2s ease}
.fs-nav a{color:inherit;opacity:.62;text-decoration:none;font-weight:600;padding:4px 10px;border-radius:999px;white-space:nowrap}
.fs-nav a:hover{opacity:1;background:var(--hl)}
.fs-nav a.on{opacity:1;font-weight:800;background:var(--hl)}
.fs-top .slide-num{position:static;display:inline;background:none;padding:0;border-radius:0;box-shadow:none;
  color:inherit;opacity:.75;font-size:inherit;font-weight:700;letter-spacing:.04em;white-space:nowrap;font-variant-numeric:tabular-nums}
.fs-area{flex:1;min-height:0;position:relative;z-index:1;display:flex;align-items:center;justify-content:center;container-type:size}
.fs-stage{position:relative;width:min(100cqw,calc(100cqh * 16 / 9));aspect-ratio:16/9}
.fs-img{position:absolute;inset:0;width:100%;height:100%;max-width:none;display:block;user-select:none}
.fs-media{position:absolute;overflow:hidden}
.fs-media>img,.fs-media>video{position:absolute;max-width:none;object-fit:fill;display:block;background:transparent}
.fs-media>video{cursor:pointer}
.notes-overlay .nl-body,.note-page p{white-space:pre-line}
.notes-overlay{transform:translateY(calc(100% + 8px))}  /* hidden panel used to peek 3px above the bottom edge */
.notes-overlay.open{transform:translateY(0)}
.progress-bar{background:transparent}
.overview.open{grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px}
.overview .thumb{display:flex;align-items:center;justify-content:center;padding:0}
.overview .thumb .n{position:static;font-size:22px;color:#fff}
.overview .thumb .t{display:none}
.overview .thumb.cur{border-color:var(--accent);background:#1e2a4d}
@media print{
  .fs-top,.fs-media{display:none}
  .fs-area{display:block;container-type:normal}
  .fs-stage{width:1280px;height:720px}
}
"""

# Media playback, matching the PowerPoint settings:
#  - videos set to play "in click sequence": the next key plays the video first, then moves on
#  - videos set to play automatically: start when the slide opens
#  - every video starts muted; the viewer can unmute it with its controls
#  - clicking a video pauses / resumes it (PowerPoint's toggle trigger); controls show on hover
#  - leaving a slide stops, rewinds and re-mutes its videos
# Esc goes back to the home page (or closes the day menu / overview if open).
# The hamburger button shows the day links; they hide again when the slide changes, but stay
# open after clicking a day link (the new day's page opens with the menu showing).
JS = r"""
(function(){
  const deck = document.querySelector('.deck');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const active = () => document.querySelector('.slide.is-active');
  function play(v){ v.dataset.started = '1'; const p = v.play(); if(p) p.catch(()=>{ v.muted = true; v.play(); }); }
  function setNav(open){
    document.body.classList.toggle('nav-open', open);
    document.querySelectorAll('.fs-burger').forEach(b => b.setAttribute('aria-expanded', open ? 'true' : 'false'));
  }
  document.querySelectorAll('.fs-burger').forEach(b => b.addEventListener('click', e => {
    e.stopPropagation(); setNav(!document.body.classList.contains('nav-open'));
  }));
  document.addEventListener('click', e => { if(!e.target.closest('.fs-menu')) setNav(false); });
  document.querySelectorAll('.fs-nav a').forEach(a => a.addEventListener('click', () => {
    if(!/[?]/.test(a.getAttribute('href'))) a.setAttribute('href', a.getAttribute('href') + '?menu');
  }));
  let last = null;
  function sync(){
    const s = active();
    if(s === last) return;
    last = s;
    slides.forEach(o => { if(o !== s) o.querySelectorAll('video').forEach(v => {
      if(!v.paused) v.pause(); v.muted = true; if(v.dataset.started){ v.currentTime = 0; v.dataset.started = ''; } }); });
    if(s) s.querySelectorAll('video[data-auto="1"]').forEach(play);
    setNav(false);  // the day menu hides itself whenever the slide changes
    const i = slides.indexOf(s);
    document.querySelectorAll('.overview .thumb').forEach(t => t.classList.toggle('cur', +t.dataset.i === i));
  }
  new MutationObserver(sync).observe(deck, {subtree:true, attributes:true, attributeFilter:['class']});
  window.addEventListener('keydown', e => {
    if(e.key === 'Escape'){
      if(document.body.classList.contains('nav-open')){ e.preventDefault(); e.stopImmediatePropagation(); setNav(false); return; }
      const ov = document.getElementById('overviewGrid');
      if(ov && ov.classList.contains('open')) return;
      e.preventDefault(); e.stopImmediatePropagation(); location.href = 'index.html'; return;
    }
    if(!(e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown')) return;
    const s = active();
    const v = s && Array.from(s.querySelectorAll('video[data-auto="0"]')).find(v => !v.dataset.started);
    if(v){ e.preventDefault(); e.stopImmediatePropagation(); play(v); }
  }, true);
  document.querySelectorAll('.fs-media video').forEach(v => {
    v.muted = true;
    v.addEventListener('click', () => { if(v.paused) play(v); else v.pause(); });
    v.addEventListener('mouseenter', () => { v.controls = true; });
    v.addEventListener('mouseleave', () => { v.controls = false; });
  });
  sync();
  // Arriving from a day link (?menu): keep the day menu open on the new day
  if(/[?&]menu\b/.test(location.search)){
    setNav(true);
    history.replaceState(null, '', location.pathname + location.hash);
  }
})();
"""

DAY_LINKS = [(d, f'Day{d}.html') for d in range(1, 6)]


def plain_background(bg_path):
    """True when the slide background is one flat colour (no artwork)."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', bg_path, '-vf', 'scale=32:18,format=rgb24',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return all(max(raw[c::3]) - min(raw[c::3]) <= 6 for c in range(3))


def bar_colours(bg_path):
    """Text colour for the top bar: light on a dark background, dark on a light one."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', bg_path, '-vf', 'crop=iw:ih*0.05:0:0,scale=1:1,format=rgb24',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    r, g, b = raw[:3]
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    fg, hl = ('#ffffff', 'rgba(255,255,255,.16)') if lum < 0.55 else ('#182034', 'rgba(24,32,52,.08)')
    return f'--fg:{fg};--hl:{hl}'


def attr(s):
    return html.escape(plain_dashes(s), quote=True)


def pct(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') + '%'


def media_html(m):
    x, y, w, h = m['box']
    c = m['crop']
    fw, fh = 1 - c['l'] - c['r'], 1 - c['t'] - c['b']
    inner = (f'left:{pct(-c["l"] / fw * 100)};top:{pct(-c["t"] / fh * 100)};'
             f'width:{pct(100 / fw)};height:{pct(100 / fh)}')
    rot = f';transform:rotate({m["rot"]:g}deg)' if m.get('rot') else ''
    box = f'left:{pct(x)};top:{pct(y)};width:{pct(w)};height:{pct(h)}{rot}'
    if m['kind'] == 'gif':
        el = f'<img src="{m["src"]}" alt="" style="{inner}">'
    else:
        flags = ' loop' if m.get('loop') else ''
        flags += ' muted'  # always start muted; the viewer can unmute
        el = (f'<video src="{m["src"]}" poster="{m["poster"]}" preload="metadata" playsinline{flags} '
              f'data-auto="{1 if m.get("autoplay") else 0}" style="{inner}"></video>')
    return f'<div class="fs-media" style="{box}">{el}</div>'


def build(day, filename, page_title):
    with open(os.path.join(META, f'd{day}-slides.json'), encoding='utf-8') as f:
        slides = json.load(f)
    nav = ('<div class="fs-menu"><button class="fs-burger" type="button" aria-label="Show days" aria-expanded="false">'
           '<span></span><span></span><span></span></button><nav class="fs-nav">' + ''.join(
               '<a href="%s"%s>Day %d</a>' % (href, ' class="on"' if d == day else '', d) for d, href in DAY_LINKS)
           + '</nav></div>')
    out = []
    for s in slides:
        n = s['n']
        if s['hidden']:
            continue
        bg = f'assets/day{day}/bg/s{n:02d}.jpg'
        # plain background: the original slide image as is; artwork background: the transparent layer
        plain = plain_background(os.path.join(ROOT, bg))
        img = f'assets/day{day}/slides/s{n:02d}.{"jpg" if plain else "png"}'
        for f in (img, bg):
            if not os.path.exists(os.path.join(ROOT, f)):
                raise SystemExit(f'missing {f}')
        for m in s['media']:
            for k in ('src', 'poster'):
                if k in m and not os.path.exists(os.path.join(ROOT, m[k])):
                    raise SystemExit(f'missing {m[k]}')
        title = s['title'] or f'Slide {n}'
        alt = ' / '.join(s['text'])
        media = ''.join(media_html(m) for m in s['media'])
        lazy = '' if n <= 2 else ' loading="lazy"'
        out.append(f'<section class="slide fullslide" id="s{n}" data-title="{attr(title)}" '
                   f'style="{bar_colours(os.path.join(ROOT, bg))}">'
                   f'<img class="fs-bg" src="{bg}" alt=""{lazy}>'
                   f'<div class="fs-top">{nav}<span class="slide-num" data-n=""></span></div>'
                   f'<div class="fs-area">'
                   f'<div class="fs-stage"><img class="fs-img" src="{img}" alt="{attr(alt)}"'
                   f'{lazy}>{media}</div></div>'
                   f'<div class="notes" data-slide="">{html.escape(plain_dashes(s["notes"]), quote=False)}</div></section>')

    with open(os.path.join(SHELL, 'base.css'), encoding='utf-8') as f:
        css = f.read()
    with open(os.path.join(SHELL, 'overlays.html'), encoding='utf-8') as f:
        overlays = f.read()
    with open(os.path.join(SHELL, 'deck.js'), encoding='utf-8') as f:
        js = f.read().replace('__NUM_OFFSET__', '0').replace('__OTHER__', '0')
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page_title}</title>
<style>
{css}{CSS}</style>
</head>
<body class="">
<div class="deck">

{chr(10).join(out)}
{overlays}
<script>
{js}</script>
<script>{JS}</script>
</body>
</html>
'''
    if '—' in doc or '&mdash;' in doc:
        raise SystemExit(f'{filename}: em dash found')
    with open(os.path.join(ROOT, filename), 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'{filename}: {len(out)} slides')
    return len(out)
