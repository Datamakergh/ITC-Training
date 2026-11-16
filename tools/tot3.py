"""ToT Day 3 (Training of Trainers, separate from the ITC Day 1-5 decks).

Source (KENYA ITC/GUIDES/DAY 1/DATA ANNOTATION/ToT Decks - Consistent): ToT Day 3 Participant Manual.pptx
Every slide of the PowerPoint, in order, shown exactly as designed (see fullslide.py).
Its menu lists only the ToT days, and Esc goes to ToT.html.
"""
from fullslide import build, TOT_LINKS, TOT_HOME

build('tot3', 'ToT-Day3.html', 'ToT Day 3: Participant Manual | Kenya ITC × datamaker', links=TOT_LINKS, home=TOT_HOME)
