"""Builder for decks shown like a PowerPoint slideshow, on any screen.

Each slide is the whole slide image exported by PowerPoint (export_pdf.sh + render_layers.py):
  assets/day<day>/slides/sNN.jpg
scaled to fit the screen at its exact shape (16:9, or the deck's own, e.g. A4), with black bars where the screen shape differs,
plus the slide's GIFs and videos placed on top at their PowerPoint position and crop
(assets/day<day>/media/*, positions in tools/meta/d<day>-*.json from extract_pptx.py).
Media positions are percentages of the slide, so they scale with it.

Nothing is added to or dropped from the source deck: one HTML slide per PPTX slide, in order.
"""
import html
import json
import os

from deck import ROOT, SHELL, META, plain_dashes, deck_dirs

CSS = """
/* ---- slideshow decks ----
   Like PowerPoint's slideshow: the slide is scaled to fit the screen at its own shape (--ar, 16:9 unless the
   deck sets another, e.g. A4), black bars fill the rest.
   The menu button and slide number float in the corners and fade out when the mouse or finger is idle. */
.deck{height:100vh;height:100dvh;background:#000;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
html,body{background:#000}
.slide.fullslide{background:#000;color:#fff;transform:none;
  opacity:0;z-index:0;transition:opacity 0s linear .45s}  /* the slide being left stays whole under the new one */
.slide.fullslide.is-prev{transform:none}
.slide.fullslide.is-active{opacity:1;z-index:2;transition:opacity .45s ease}  /* the new slide fades in on top */
@media (prefers-reduced-motion:reduce){.slide.fullslide,.slide.fullslide.is-active{transition:none}}
.fs-area{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;container-type:size;z-index:1}
.fs-stage{position:relative;width:min(100cqw,calc(100cqh * var(--ar,1.7778)));aspect-ratio:var(--ar,1.7778);flex:0 0 auto}
.fs-img{position:absolute;inset:0;width:100%;height:100%;max-width:none;display:block;user-select:none;-webkit-user-drag:none}
.fs-media{position:absolute;overflow:hidden}
.fs-media>img,.fs-media>video{position:absolute;max-width:none;object-fit:fill;display:block;background:transparent}
.fs-media>video{cursor:pointer}
.fs-toast{position:fixed;left:50%;bottom:6%;transform:translateX(-50%);z-index:60;pointer-events:none;
  padding:.45em 1em;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;font:600 15px/1.2 system-ui,sans-serif;
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);opacity:0;transition:opacity .25s}
.fs-toast.show{opacity:1}
.fs-top{position:absolute;top:0;left:0;right:0;z-index:3;display:flex;align-items:flex-start;justify-content:space-between;
  gap:12px;padding:clamp(8px,1.4vh,14px) clamp(8px,1.2vw,16px);pointer-events:none;
  font-family:Pretendard,'Inter',system-ui,sans-serif;font-size:clamp(12px,1.5vh,15px);color:#fff}
.fs-menu,.fs-top .slide-num{pointer-events:auto;opacity:0;transition:opacity .35s ease}
body.ui-on .fs-menu,body.ui-on .fs-top .slide-num,body.nav-open .fs-menu{opacity:1}
.fs-menu{display:flex;align-items:center;gap:6px;min-width:0;padding:4px;border-radius:12px;background:rgba(0,0,0,.55);
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.fs-burger{flex:0 0 auto;display:flex;flex-direction:column;justify-content:center;gap:4px;width:38px;height:34px;padding:0 10px;
  border:0;border-radius:8px;background:transparent;color:inherit;cursor:pointer}
.fs-burger span{display:block;height:2px;border-radius:2px;background:currentColor;transition:transform .2s ease,opacity .2s ease}
.fs-burger:hover,.fs-burger:focus-visible{background:rgba(255,255,255,.16);outline:none}
body.nav-open .fs-burger{background:rgba(255,255,255,.16)}
body.nav-open .fs-burger span:nth-child(1){transform:translateY(6px) rotate(45deg)}
body.nav-open .fs-burger span:nth-child(2){opacity:0}
body.nav-open .fs-burger span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.fs-nav{display:none;align-items:center;gap:4px;min-width:0;overflow-x:auto;scrollbar-width:none}
body.nav-open .fs-nav{display:flex}
.fs-nav a{color:inherit;opacity:.7;text-decoration:none;font-weight:600;padding:6px 10px;border-radius:999px;white-space:nowrap}
.fs-nav a:hover{opacity:1;background:rgba(255,255,255,.16)}
.fs-nav a.on{opacity:1;font-weight:800;background:rgba(255,255,255,.16)}
.fs-nav .fs-sep{flex:0 0 1px;align-self:stretch;margin:4px 2px;background:rgba(255,255,255,.3)}
.fs-top .slide-num{position:static;top:0;display:inline-block;background:rgba(0,0,0,.55);padding:6px 12px;border-radius:999px;
  box-shadow:none;color:#fff;font-size:inherit;font-weight:700;letter-spacing:.04em;white-space:nowrap;font-variant-numeric:tabular-nums;
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.progress-bar{background:transparent;opacity:0;transition:opacity .35s ease}
body.ui-on .progress-bar{opacity:1}
.notes-overlay .nl-body,.note-page p{white-space:pre-line}
.notes-overlay{transform:translateY(calc(100% + 8px))}  /* hidden panel used to peek 3px above the bottom edge */
.notes-overlay.open{transform:translateY(0)}
.overview.open{grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px}
.overview .thumb{display:flex;align-items:center;justify-content:center;padding:0}
.overview .thumb .n{position:static;font-size:22px;color:#fff}
.overview .thumb .t{display:none}
.overview .thumb.cur{border-color:var(--accent);background:#1e2a4d}
@media (max-width:600px){.overview.open{padding:16px}}
@media print{
  .fs-top,.fs-media,.fs-toast{display:none}
  .slide.fullslide{background:#fff}
  .fs-area{position:static;display:block;container-type:normal}
  .fs-stage{width:1280px;height:calc(1280px / var(--ar,1.7778))}
}
"""

# Media playback, matching the PowerPoint settings:
#  - videos set to play "in click sequence": the next key/tap plays the video first, then moves on
#  - videos set to play automatically: start when the slide opens
#  - videos play with sound (unless muted in the PowerPoint); M mutes / unmutes all videos
#  - clicking (or tapping) a video pauses it if playing, plays it if paused
#  - leaving a slide stops and rewinds its videos
# Phones / tablets: tap the left third of the screen for the previous slide, anywhere else for the next.
# The menu button, slide number and progress bar show on mouse move or tap and fade after 2.5 s idle.
# The slides next to the current one are loaded and decoded ahead, so each change is a clean cross-fade.
# Esc goes back to the home page (or closes the day menu / overview if open).
# The hamburger button shows the day links; they hide again when the slide changes, but stay
# open after clicking a day link (the new day's page opens with the menu showing).
JS = r"""
(function(){
  const deck = document.querySelector('.deck');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const active = () => document.querySelector('.slide.is-active');
  // sound: on by default; M toggles it for every video (a video muted in the PowerPoint stays muted)
  let soundOn = true;
  const sound = v => { v.muted = !soundOn || v.dataset.mute === '1'; };
  function play(v){ v.dataset.started = '1'; sound(v); const p = v.play(); if(p) p.catch(()=>{ v.muted = true; v.play(); }); }
  const toast = document.createElement('div');
  toast.className = 'fs-toast'; toast.setAttribute('role', 'status');
  document.body.appendChild(toast);
  let toastT = null;
  function setSound(on){
    soundOn = on;
    document.querySelectorAll('.fs-media video').forEach(sound);
    toast.textContent = on ? 'Sound on' : 'Sound off (press M)';
    toast.classList.add('show'); clearTimeout(toastT);
    toastT = setTimeout(() => toast.classList.remove('show'), 1400);
  }
  function setNav(open){
    document.body.classList.toggle('nav-open', open);
    document.querySelectorAll('.fs-burger').forEach(b => b.setAttribute('aria-expanded', open ? 'true' : 'false'));
    if(!open) poke();
  }
  // controls: visible while the pointer moves, hidden after 2.5 s idle (kept while the menu is open or hovered)
  let idle = null, overMenu = false;
  function poke(){
    document.body.classList.add('ui-on');
    clearTimeout(idle);
    idle = setTimeout(() => { if(!overMenu && !document.body.classList.contains('nav-open')) document.body.classList.remove('ui-on'); }, 2500);
  }
  ['mousemove','pointerdown','wheel'].forEach(t => window.addEventListener(t, poke, {passive:true}));
  document.querySelectorAll('.fs-menu,.slide-num').forEach(m => {
    m.addEventListener('mouseenter', () => { overMenu = true; poke(); });
    m.addEventListener('mouseleave', () => { overMenu = false; poke(); });
  });
  document.querySelectorAll('.fs-burger').forEach(b => b.addEventListener('click', e => {
    e.stopPropagation(); setNav(!document.body.classList.contains('nav-open'));
  }));
  document.addEventListener('click', e => { if(!e.target.closest('.fs-menu') && document.body.classList.contains('nav-open')) setNav(false); });
  document.querySelectorAll('.fs-nav a:not(.fs-home)').forEach(a => a.addEventListener('click', () => {
    if(!/[?]/.test(a.getAttribute('href'))) a.setAttribute('href', a.getAttribute('href') + '?menu');
  }));
  // load and decode the slides around the current one so a change never fades in a blank slide
  function warm(i){
    for(let j = i - 1; j <= i + 2; j++){
      const s = slides[j]; if(!s) continue;
      s.querySelectorAll('img').forEach(img => {
        if(img.loading === 'lazy') img.loading = 'eager';
        if(img.decode) img.decode().catch(() => {});
      });
    }
  }
  let last = null;
  function sync(){
    const s = active();
    if(s === last) return;
    last = s;
    slides.forEach(o => { if(o !== s) o.querySelectorAll('video').forEach(v => {
      if(!v.paused) v.pause(); if(v.dataset.started){ v.currentTime = 0; v.dataset.started = ''; } }); });
    if(s) s.querySelectorAll('video[data-auto="1"]').forEach(play);
    if(document.body.classList.contains('nav-open')) setNav(false);  // the day menu hides itself when the slide changes
    const i = slides.indexOf(s);
    warm(i);
    document.querySelectorAll('.overview .thumb').forEach(t => t.classList.toggle('cur', +t.dataset.i === i));
  }
  new MutationObserver(sync).observe(deck, {subtree:true, attributes:true, attributeFilter:['class']});
  window.addEventListener('keydown', e => {
    if(e.key === 'Escape'){
      if(document.body.classList.contains('nav-open')){ e.preventDefault(); e.stopImmediatePropagation(); setNav(false); return; }
      const ov = document.getElementById('overviewGrid');
      if(ov && ov.classList.contains('open')) return;
      e.preventDefault(); e.stopImmediatePropagation(); location.href = '__HOME__'; return;
    }
    if((e.key === 'm' || e.key === 'M') && !e.ctrlKey && !e.metaKey && !e.altKey && !e.target.closest('input,textarea')){
      e.preventDefault(); setSound(!soundOn); return;
    }
    if(!(e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown')) return;
    const s = active();
    const v = s && Array.from(s.querySelectorAll('video[data-auto="0"]')).find(v => !v.dataset.started);
    if(v){ e.preventDefault(); e.stopImmediatePropagation(); play(v); }
  }, true);
  document.querySelectorAll('.fs-media video').forEach(v => {
    v.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); if(v.paused) play(v); else v.pause(); });
  });
  // tap to move: left third = previous slide, anywhere else = next (touch and pen only; swipes still work)
  let tap = null;
  deck.addEventListener('pointerdown', e => {
    tap = (e.pointerType === 'touch' || e.pointerType === 'pen') && e.isPrimary ? {x: e.clientX, y: e.clientY, t: Date.now()} : null;
  });
  deck.addEventListener('pointercancel', () => { tap = null; });
  deck.addEventListener('pointerup', e => {
    const t = tap; tap = null;
    if(!t || Math.hypot(e.clientX - t.x, e.clientY - t.y) > 12 || Date.now() - t.t > 600) return;
    if(e.target.closest('.fs-menu,.slide-num,video,a,button,input,label,.overview,.notes-overlay,.print-panel')) return;
    if(document.body.classList.contains('nav-open')){ setNav(false); return; }
    const key = e.clientX < window.innerWidth / 3 ? 'ArrowLeft' : 'ArrowRight';
    document.dispatchEvent(new KeyboardEvent('keydown', {key, bubbles:true, cancelable:true}));
  });
  sync();
  poke();
  // Arriving from a day link (?menu): keep the day menu open on the new day
  if(/[?&]menu\b/.test(location.search)){
    setNav(true);
    history.replaceState(null, '', location.pathname + location.hash);
  }
})();
"""

DAY_LINKS = [(f'Day {d}', f'Day{d}.html') for d in range(1, 6)]
# Training of Trainers: a separate programme with its own home page and day menu.
TOT_LINKS = [(f'ToT Day {d}', f'ToT-Day{d}.html') for d in range(1, 4)]
TOT_HOME = 'ToT.html'


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
        flags += ' data-mute="1"' if m.get('muted') else ''  # muted in the PowerPoint
        el = (f'<video src="{m["src"]}" poster="{m["poster"]}" preload="metadata" playsinline muted{flags} '
              f'data-auto="{1 if m.get("autoplay") else 0}" style="{inner}"></video>')
    return f'<div class="fs-media" style="{box}">{el}</div>'


def jpeg_size(path):
    """(width, height) of a JPEG, read from its SOF marker."""
    with open(path, 'rb') as f:
        data = f.read()
    i = 2
    while i < len(data):
        marker, seg = data[i + 1], int.from_bytes(data[i + 2:i + 4], 'big')
        if marker in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(data[i + 7:i + 9], 'big'), int.from_bytes(data[i + 5:i + 7], 'big')
        i += 2 + seg
    raise SystemExit(f'no size in {path}')


def build(day, filename, page_title, parts=('slides',), links=DAY_LINKS, home='index.html', skip=()):
    """day: ITC day number or deck key (see deck.deck_dirs).
    parts: meta files tools/meta/d<day>-<part>.json, shown one after another (a day may join decks).
    links: the (label, file) pairs in the menu; home: where Esc goes.
    skip: source slide numbers to leave out (e.g. an empty placeholder slide)."""
    adir, mpre = deck_dirs(day)
    slides = []
    for part in parts:
        with open(os.path.join(META, f'{mpre}-{part}.json'), encoding='utf-8') as f:
            slides += json.load(f)
    nav = ('<div class="fs-menu"><button class="fs-burger" type="button" aria-label="Show days" aria-expanded="false">'
           '<span></span><span></span><span></span></button><nav class="fs-nav">'
           f'<a class="fs-home" href="{home}">Home</a><span class="fs-sep" aria-hidden="true"></span>' + ''.join(
               '<a href="%s"%s>%s</a>' % (href, ' class="on"' if href == filename else '', label) for label, href in links)
           + '</nav></div>')
    out = []
    for s in slides:
        n = s['n']
        if s['hidden'] or n in skip:
            continue
        img = f'assets/{adir}/slides/s{n:02d}.jpg'
        if not os.path.exists(os.path.join(ROOT, img)):
            raise SystemExit(f'missing {img}')
        for m in s['media']:
            for k in ('src', 'poster'):
                if k in m and not os.path.exists(os.path.join(ROOT, m[k])):
                    raise SystemExit(f'missing {m[k]}')
        title = s['title'] or f'Slide {n}'
        alt = ' / '.join(s['text'])
        media = ''.join(media_html(m) for m in s['media'])
        lazy = '' if n <= 2 else ' loading="lazy"'
        out.append(f'<section class="slide fullslide" id="s{n}" data-title="{attr(title)}">'
                   f'<div class="fs-area">'
                   f'<div class="fs-stage"><img class="fs-img" src="{img}" alt="{attr(alt)}"'
                   f'{lazy}>{media}</div></div>'
                   f'<div class="fs-top">{nav}<span class="slide-num" data-n=""></span></div>'
                   f'<div class="notes" data-slide="">{html.escape(plain_dashes(s["notes"]), quote=False)}</div></section>')

    # slide shape from the exported images: 16:9 decks keep the default, others (e.g. A4) set --ar
    w, h = jpeg_size(os.path.join(ROOT, f'assets/{adir}/slides/s{slides[0]["n"]:02d}.jpg'))
    ar_style = '' if abs(w / h - 16 / 9) < 0.01 else f' style="--ar:{w / h:.4f}"'

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
<div class="deck"{ar_style}>

{chr(10).join(out)}
{overlays}
<script>
{js}</script>
<script>{JS.replace('__HOME__', home)}</script>
</body>
</html>
'''
    if '—' in doc or '&mdash;' in doc:
        raise SystemExit(f'{filename}: em dash found')
    with open(os.path.join(ROOT, filename), 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'{filename}: {len(out)} slides')
    return len(out)
