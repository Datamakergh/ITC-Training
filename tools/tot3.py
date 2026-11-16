"""ToT Day 3 (Training of Trainers, separate from the ITC Day 1-5 decks).

Source (~/Documents, revamped 2026-11-16): ToT Day 3 Participant Manual.pptx
Every slide of the PowerPoint, in order, shown exactly as designed (see fullslide.py).
The source is A4 landscape; its export copy is widened to 16:9 first (tools/widen_169.py).
Its menu lists only the ToT days, and Esc goes to ToT.html.
"""
from fullslide import build, TOT_LINKS, TOT_HOME

build('tot3', 'ToT-Day3.html', 'ToT Day 3: Participant Manual | Kenya ITC × datamaker', links=TOT_LINKS, home=TOT_HOME)
