"""Photobooth Image Labeling Project (ver. 2.0), shared by Day 3 and Day 4.

The DAY 3 and DAY 4 copies of 'Photobooth Image Labeling Project.pptx' have the same
slides and text, so both days are built from the Day 3 renders in assets/day3/photobooth.
"""
from deck import *

AGE_GROUPS = [
    (11, 'Age: Under 10', range(12, 20)),
    (20, 'Age: Teen', range(21, 25)),
    (25, 'Age: 20s', range(26, 33)),
    (33, 'Age: 30s', range(34, 45)),
    (45, 'Age: 40 and Above', range(46, 61)),
]


def photobooth_slides(day, session):
    pb = Source(3, 'photobooth')
    p = f'd{day}pb'
    K = 'Photobooth Project'
    S = [section(f'{p}-sec', 'Photobooth Image Labelling Project', session,
                 'Bounding box and polygon project guideline, ver. 2.0', 'image', 'user')]
    S.append(ip_notice(f'{p}-notice', K, pb.notes(2)))
    S.append(content(f'{p}-purpose', 'Purpose of the Project', K, f'''
  <p class="lede">Create a dataset for AI to <b>recognise people</b>, and use the AI to create a photobooth-type media art experience that can be combined with various IPs.</p>
{table(['Platform', 'Annotation type', 'Classes', 'Labelling target'], [
    ['Synapse', 'Bounding box &middot; Polygon', 'Face, Body, Age, Gender, Image brightness', 'Person'],
])}
{note("<b>All people</b> in the image are labelling targets.", "user")}''', eyebrow='Project Overview', notes=pb.notes(4)))
    S.append(pb.guide(5, 'All People Are Labelling Targets', 'Project Overview'))

    S.append(section(f'{p}-criteria', 'Labelling Criteria', K, ic='list', deco_ic='user'))
    S += pb.guides([
        (7, '1. Bounding Box: Face'),
        (8, '2. Attributes: Gender, Age, Image Brightness'),
        (9, '3. Polygon: Body'),
        (10, 'Task Completion Screen'),
    ], 'Labelling Criteria')
    S.append(content(f'{p}-rules', 'Photobooth Rules at a Glance', K, checklist([
        (True, '<b>Face box:</b> head, face and neck inside the box (neck up to the forehead).'),
        (False, 'Hair, hats, headbands and bags are <b>not</b> part of the face box.'),
        (True, '<b>Body polygon:</b> the whole-body outline of every person.'),
        (True, 'Hair, bags, hats and headbands <b>are</b> part of the body polygon.'),
        (True, 'Set <b>gender</b>, <b>age</b> and <b>image brightness</b> for each face.'),
        (True, 'Every person in the image is a labelling target.'),
    ]) + '\n' + note('Age bands: under 10 &middot; teen &middot; 20s &middot; 30s &middot; 40 and above. The next slides show examples of each.', 'list'),
        eyebrow='Quick Recap'))

    for sec_n, title, rng in AGE_GROUPS:
        S.append(section(f'{p}-age{sec_n}', title, 'Age Examples', 'Example images with their age and gender labels',
                         'user', 'image', notes=pb.notes(sec_n)))
        S += [pb.guide(n, f'{title} ({i + 1}/{len(rng)})', 'Age Examples') for i, n in enumerate(rng)]

    S.append(practice(f'{p}-practice', 'Photobooth Practice',
                      'Open the Photobooth project in Synapse and start labelling.',
                      ['Face box: neck to forehead', 'Body polygon on every person', 'Gender, age, brightness set',
                       'No hair or hats in the face box', 'Zoom in on edges', 'Save often']))
    return S
