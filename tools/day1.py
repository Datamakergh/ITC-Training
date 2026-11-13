"""Day 1: Data Labeling Training.

Sources (KENYA ITC/GUIDES/DAY 1/DATA ANNOTATION), shown in this order:
  1. Day 1 new.pptx                  -> tools/meta/d1-p1.json (75 slides)
  2. DAY 1 TRAINING MATERIAL.pptx    -> tools/meta/d1-p2.json (slide numbers continue from part 1)
Every slide of both PowerPoints, in order, shown exactly as designed (see fullslide.py).
"""
from fullslide import build

build(1, 'Day1.html', 'Day 1: Data Labeling Training | Kenya ITC × datamaker', parts=('p1', 'p2'))
