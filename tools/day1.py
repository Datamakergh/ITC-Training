"""Day 1: Data Labeling Training.

Sources (KENYA ITC/GUIDES/DAY 1/DATA ANNOTATION), shown in this order:
  1. Labeling Training Introduction Day 1 [13112026].pptx-> tools/meta/d1-p1.json (75 slides)
  2. DAY 1 TRAINING MATERIAL.pptx    -> tools/meta/d1-p2.json (slide numbers continue from part 1)
Every slide of both PowerPoints, in order, shown exactly as designed (see fullslide.py).
"""
from fullslide import build

build(1, 'Day1.html', 'Day 1: Data Labeling Training | Kenya ITC × datamaker', parts=('p1', 'p2'),
      skip={36})  # part 1 slide 36 repeats slide 37 (same Kenya AI Strategy text; 37 wraps the vision line cleanly)
