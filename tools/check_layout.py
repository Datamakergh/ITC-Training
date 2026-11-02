"""Layout check: loads a deck in headless Chrome at 1280x720 and reports, per slide,
clipped content, elements outside the slide, overflowing cards and overlapping elements.

usage: python3 tools/check_layout.py Day1.html [Day2.html ...]
"""
import html
import json
import os
import re
import subprocess
import sys

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECK_JS = r"""
<script>
window.addEventListener('load', () => setTimeout(() => {
  const out = [];
  const CARDS = '.icard,.cmp-col,.sc-card,.sc-row,.pnode,.tree-kid,.task-card,.a-row,.j-day,.j-chips span,.kbd,.pr-checks span,.mod-card,.reason-item,.tbl-wrap,.lede,.h1,.h2,.pr-title,.title-h1';
  const ownText = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  document.querySelectorAll('.slide').forEach((s, i) => {
    const id = s.id, issues = [];
    const sr = s.getBoundingClientRect();
    const body = s.querySelector('.slide-body');
    if (body && (body.scrollHeight > body.clientHeight + 2 || body.scrollWidth > body.clientWidth + 2))
      issues.push(`content clipped: body ${body.scrollWidth}x${body.scrollHeight} > ${body.clientWidth}x${body.clientHeight}`);
    const leaves = [];
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('.notes') || el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return;
      if (getComputedStyle(el).visibility === 'hidden') return;
      if (r.right > sr.right + 1 || r.bottom > sr.bottom + 1 || r.left < sr.left - 1 || r.top < sr.top - 1)
        issues.push(`outside slide: <${el.tagName.toLowerCase()} class="${el.className.baseVal ?? el.className}">`);
      const tag = el.tagName.toLowerCase();
      if (ownText(el) || tag === 'img' || tag === 'video' || tag === 'svg') leaves.push([el, r]);
    });
    s.querySelectorAll(CARDS).forEach(el => {
      // a few px of descender overflow on tight-leading headings is not visible
      const dx = el.scrollWidth - el.clientWidth, dy = el.scrollHeight - el.clientHeight;
      if (dx > 2 || dy > 4)
        issues.push(`overflows its box by ${dx}x${dy}px: .${[...el.classList].join('.')} "${el.textContent.trim().slice(0, 40)}"`);
    });
    for (let a = 0; a < leaves.length; a++) for (let b = a + 1; b < leaves.length; b++) {
      const [ea, ra] = leaves[a], [eb, rb] = leaves[b];
      if (ea.contains(eb) || eb.contains(ea)) continue;
      // inline runs on neighbouring lines of the same paragraph share line boxes
      const inl = e => getComputedStyle(e).display === 'inline';
      const blk = e => { let p = e; while (p && inl(p)) p = p.parentElement; return p; };
      if (blk(ea) === blk(eb) && (inl(ea) || inl(eb))) continue;
      if (ea.closest('.title-wm,.title-deco') || eb.closest('.title-wm,.title-deco')) continue;
      const w = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
      const h = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      if (w > 3 && h > 3)
        issues.push(`overlap: "${(ea.textContent || ea.tagName).trim().slice(0, 30)}" x "${(eb.textContent || eb.tagName).trim().slice(0, 30)}"`);
    }
    if (issues.length) out.push({n: i + 1, id, issues: [...new Set(issues)].slice(0, 8)});
  });
  const pre = document.createElement('pre'); pre.id = 'layout-report';
  pre.textContent = JSON.stringify(out); document.body.appendChild(pre);
}, 300));
</script>
"""


def check(path):
    src = open(path, encoding='utf-8').read()
    # Lazy images would otherwise never load on hidden slides.
    src = src.replace(' loading="lazy"', '').replace('</body>', CHECK_JS + '</body>')
    tmp = os.path.join(os.path.dirname(os.path.abspath(path)), '.layout-check.html')
    open(tmp, 'w', encoding='utf-8').write(src)
    try:
        dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1280,720',
                              '--virtual-time-budget=15000', '--dump-dom', 'file://' + tmp],
                             capture_output=True, text=True, timeout=180).stdout
    finally:
        os.remove(tmp)
    m = re.search(r'<pre id="layout-report">(.*?)</pre>', dom, re.S)
    if not m:
        print(f'{path}: no report (page failed to load?)')
        return 1
    report = json.loads(html.unescape(m.group(1)))
    print(f'{os.path.basename(path)}: {len(report)} slide(s) with issues')
    for r in report:
        print(f"  #{r['n']} {r['id']}")
        for i in r['issues']:
            print('     -', i)
    return len(report)


if __name__ == '__main__':
    bad = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if bad else 0)
