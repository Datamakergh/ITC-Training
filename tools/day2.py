"""Day 2: Polyline, Traffic Flow project, Polygon, Rail & Catenary project.

Sources (KENYA ITC/GUIDES/DAY 2):
  POLYLINE SEGMENTATION.pptx                         -> polyline
  Traffic Flow for Autonomous Driving Polyline.pptx  -> traffic
  POLYGON SEGMENTATION.pptx                          -> polygon
  Rail & Catenary Condition Awareness Project.pptx   -> rail
"""
from deck import *

pl = Source(2, 'polyline')
tf = Source(2, 'traffic')
pg = Source(2, 'polygon')
rc = Source(2, 'rail')
M = 'assets/day2/media/'

S = []

# ---------------- opening ----------------
S.append(title_slide(
    'd2-title', 2, 'Polyline &amp;<br>Polygon Segmentation', PARTNERS,
    [('monitor', 'Hands-on in Datamaker Synapse'), ('globe', 'Kenya ITC Training 2026')]))
S.append(content('d2-journey', 'Where We Are', 'Overview', f'''
  <p class="lede">Yesterday you drew boxes. Today you trace lines and outline exact shapes.</p>
{journey(2)}''', eyebrow='Program Overview'))
S.append(content('d2-agenda', 'Today&rsquo;s Agenda', 'Overview', agenda([
    ('Polyline Segmentation: draw, edit and zoom', 'Hands-on'),
    ('Traffic Flow for Autonomous Driving: project guideline', 'Theory'),
    ('Traffic Flow practice', 'Hands-on'),
    ('Polygon Segmentation: draw, edit and precise labelling', 'Hands-on'),
    ('Rail &amp; Catenary Condition Awareness: project guideline', 'Theory'),
    ('Rail &amp; Catenary practice', 'Hands-on'),
]), eyebrow='Day 2 Overview', h='h1'))

# ---------------- polyline ----------------
K = 'Polyline Basics'
S.append(section('pl-sec', 'Polyline Segmentation', 'Session 1',
                 'Lines for lanes, rails and other long, narrow shapes', 'trend', 'trend'))
S.append(split_media('pl-what', 'What Is Polyline Annotation?', K, f'''
      <p class="lede">Polyline annotation is used to annotate <b>long, narrow shapes</b> in an image. You place a series of points along the object and connect them to follow its path accurately.</p>
      {bullets(["Marking a road lane: points are placed along the lane and joined to match its direction.",
                "Useful for road lanes, railway tracks and pipelines."])}
      <p class="img-cap" style="text-align:left">Source: <i>Polyline Annotation and Automated Vehicles</i>, keymakr.com</p>''',
    M + 'polyline-rail.png', notes=pl.notes(3)))
S += pl.guides([
    (5, 'Drawing a Polyline (1/4)'),
    (6, 'Drawing a Polyline (2/4)'),
    (7, 'Drawing a Polyline (3/4)'),
    (8, 'Drawing a Polyline (4/4)'),
    (9, 'Example: Railway Track'),
    (10, 'Example: Railway Track'),
    (11, 'Example: Railway Junction'),
    (12, 'Example: Road Lanes'),
    (13, 'Delete a Polyline: Select It'),
    (14, 'Delete a Polyline: Press D'),
    (15, 'Resize a Polyline (1/3)'),
    (16, 'Resize a Polyline (2/3)'),
    (17, 'Resize a Polyline (3/3)'),
    (18, 'Add a Point: Ctrl + Click'),
    (19, 'Add a Point: Ctrl + Click'),
    (20, 'Delete a Point: Alt + Click'),
    (21, 'Delete a Point: Alt + Click'),
    (22, 'Delete a Point: Alt + Click'),
    (23, 'Reduce Image Transparency'),
    (24, 'Zoom In and Out'),
], K)
S.append(content('pl-keys', 'Polyline Essentials', K, f'''
  <div class="icard-grid cols-3">
    <div class="icard"><div class="icard-ic">{icon("trend", 28)}</div><div class="icard-t">Draw</div><div class="icard-d">Click through the <b>centre</b> of the shape to place points, then {kbd("Enter")} to finish.</div></div>
    <div class="icard"><div class="icard-ic">{icon("x", 28)}</div><div class="icard-t">{kbd("D")} Delete</div><div class="icard-d">Select the line, then press D. Or press D right after drawing.</div></div>
    <div class="icard"><div class="icard-ic">{icon("hand", 28)}</div><div class="icard-t">Resize</div><div class="icard-d">Click and drag a point to reshape the line.</div></div>
    <div class="icard"><div class="icard-ic">{icon("spark", 28)}</div><div class="icard-t">{kbd("Ctrl")} + Click</div><div class="icard-d">Add a point on the polyline.</div></div>
    <div class="icard"><div class="icard-ic">{icon("target", 28)}</div><div class="icard-t">{kbd("Alt")} + Click</div><div class="icard-d">Delete a point from the polyline.</div></div>
    <div class="icard"><div class="icard-ic">{icon("eye", 28)}</div><div class="icard-t">Check</div><div class="icard-d">Use brightness and zoom to see the line clearly before you submit.</div></div>
  </div>''', eyebrow='Quick Recap'))
S += pl.guides([(25, 'Log In to the Dashboard'), (26, 'Practice: NIA_Polyline')], 'Hands-on')
S.append(practice('pl-practice', 'Polyline Practice',
                  'Open the NIA_Polyline project in Synapse and start your task.',
                  ['Points through the centre of the line', 'Follow the full length', 'Ctrl + click to add a point',
                   'Alt + click to remove a point', 'Zoom in on curves', 'Save often']))

# ---------------- traffic flow project ----------------
K = 'Traffic Flow Project'
S.append(section('tf-sec', 'Traffic Flow for Autonomous Driving', 'Session 2',
                 'Polyline project guideline, ver. 2.0', 'car', 'trend'))
S.append(ip_notice('tf-notice', K, tf.notes(2)))
S.append(split_media('tf-purpose', 'Purpose of the Project', K, bullets([
    'At present, there is a global trend of cars using AI for autonomous driving instead of relying on humans.',
    'The purpose of this project is to create learning data for autonomous driving AI.']),
    M + 'traffic-purpose.png', eyebrow='Project Overview', notes=tf.notes(4)))
S.append(content('tf-target', 'Labelling Target', K, f'''
  <p class="lede">The assignment requires working with <b>6 types of objects</b>.</p>
{table(['Category', 'Sub-category', 'Class'], [
    ['Lane', 'Lane type', 'Solid &middot; Dotted &middot; Stop-line'],
    ['', 'Lane colour', 'White &middot; Yellow &middot; Other (blue, red)'],
])}
{note("Every lane gets <b>both</b> a type and a colour, for example: Lane / Dotted / White.", "list")}''',
    eyebrow='Project Overview', notes=tf.notes(5)))
S.append(content('tf-solid', 'Labelling Target: Solid Line', K, f'''
  <img src="{M}traffic-solid.png" alt="Solid lane examples" style="width:100%;max-height:300px;object-fit:contain;border-radius:10px;margin-top:6px">
{note("For a <b>double</b> solid line, label each line separately.", "alert")}''', eyebrow='Project Overview', notes=tf.notes(6)))
S += tf.guides([
    (7, 'Labelling Target: Dotted Line'),
    (8, 'Labelling Target: Stop-line'),
    (9, 'Labelling Target: Lane Colours'),
], 'Project Overview')

S.append(section('tf-criteria', 'Labelling Criteria', K, ic='list', deco_ic='trend'))
S += tf.guides([
    (11, 'U-turn Line = White, Dotted'),
    (12, 'Outermost Line: Often Solid Yellow'),
], 'Labelling Criteria')
S.append(content('tf-blocked', 'Lanes Blocked by Obstacles', K, f'''
  <p class="lede">Even when lanes are blocked by obstacles (fences, cars, etc.), consider which lane it originally was and label it accordingly.</p>
  <div class="split-img" style="grid-template-columns:1.6fr 1fr">
    <img src="{M}traffic-blocked.png" alt="Lanes behind a safety fence">
    <div>{note("Although it appears as a <b>dotted line</b> because of the safety fence, or looks short, label it as a <b>solid line</b>.", "alert")}</div>
  </div>''', eyebrow='Labelling Criteria', notes=tf.notes(13)))
S += tf.guides([
    (14, 'Consider the Whole Scene'),
    (15, 'Road Leaders and Bus Parking Lines'),
], 'Labelling Criteria')

S.append(section('tf-prec', 'Precautions', K, ic='alert', deco_ic='car'))
S += tf.guides([
    (17, 'Correct vs Wrong'),
    (18, 'Do Not Label These'),
    (19, 'Discard Standard'),
    (20, 'Not Labelling Targets'),
    (21, 'Not Labelling Targets'),
    (22, 'Parking Lots'),
], 'Precaution')


def err_slide(sid, n, a, b):
    return content(sid, 'Commonly Found Errors', K, f'''
  <p class="lede">High contrast can make lane colours look different. Remember: the <b>outermost lane is often a solid yellow line</b>, and <b>Y-shaped lanes are often solid yellow lines</b>.</p>
{img_row([(M + a, "Labelled colour looks wrong"), (M + b, "Check the colour against the rule")], 250)}''',
                   eyebrow='Precaution', notes=tf.notes(n))


S.append(err_slide('tf-err1', 23, 'traffic-err1a.png', 'traffic-err1b.png'))
S.append(err_slide('tf-err2', 24, 'traffic-err2a.png', 'traffic-err2b.png'))
S.append(content('tf-rules', 'Traffic Flow Rules at a Glance', K, checklist([
    (True, 'Label every lane with a type (solid, dotted, stop-line) and a colour.'),
    (True, 'Label each line of a double solid line separately.'),
    (True, 'A U-turn line is a white, dotted line.'),
    (True, 'Lanes hidden by fences or cars: label what the lane originally was.'),
    (False, 'Do not label road leaders, bus parking lines, crossings, bike lanes or road text.'),
    (True, 'Parking on the road: label the vertical line only.'),
    (False, 'Discard tasks with no target, a flipped image, or only dim, broken lanes.'),
    (True, 'Outermost and Y-shaped lanes are usually solid yellow.'),
]), eyebrow='Quick Recap'))
S.append(practice('tf-practice', 'Traffic Flow Practice',
                  'Open the Traffic Flow project in Synapse and start labelling lanes.',
                  ['Type and colour on every lane', 'Double lines labelled separately', 'Points through the line centre',
                   'Skip non-targets', 'Discard unusable images', 'Save often']))

# ---------------- polygon ----------------
K = 'Polygon Basics'
S.append(section('pg-sec', 'Polygon Segmentation', 'Session 3',
                 'Exact outlines for objects with irregular or complex shapes', 'layers', 'layers'))
S.append(split_media('pg-what', 'What Is Polygon Annotation?', K, f'''
      <p class="lede">Polygon annotation marks an object by clicking to create <b>points around its edges</b>. Connected, the points form a shape that closely follows the real outline of the object.</p>
      {bullets(["Unlike a rectangle, a polygon can change direction and create different angles.",
                "Ideal for objects with irregular or complex shapes."])}''',
    M + 'polygon-banana.png', notes=pg.notes(2)))
S += pg.guides([
    (3, 'Drawing a Polygon: Backspace Undoes a Point'),
    (4, 'Drawing a Polygon (2/8)'),
    (5, 'Drawing a Polygon (3/8)'),
    (6, 'Drawing a Polygon (4/8)'),
    (7, 'Drawing a Polygon (5/8)'),
    (8, 'Drawing a Polygon (6/8)'),
    (9, 'Drawing a Polygon (7/8)'),
    (10, 'Drawing a Polygon (8/8)'),
    (11, 'Example of Polygon Segmentation'),
    (12, 'Example: Banana'),
    (13, 'Example: Cups'),
    (14, 'Example: Football'),
    (15, 'Resize a Polygon'),
    (16, 'Resize a Polygon'),
    (17, 'Add a Point: Ctrl + Click'),
    (18, 'Delete a Point: Alt + Click'),
    (19, 'Delete a Point: Alt + Click'),
    (20, 'Reduce Image Transparency'),
], K)

S.append(section('pg-precise', 'Precise Labelling', 'Polygon', 'Accuracy matters more than speed', 'target', 'check',
                 notes=pg.notes(21)))
K = 'Precise Labelling'
S.append(split_media('pg-p1', 'Make Sure the Work Is Precise', K,
                     '<p class="lede">Make sure the work is <b>precise</b> before you proceed.</p>',
                     M + 'polygon-s22.mp4', notes=pg.notes(22)))
S.append(split_media('pg-p2', 'Do Not Label Like This!', K,
                     f'<p class="lede">Loose points that cut across the object or miss its edges are rejected.</p>{note("Make sure the work is precise before you proceed.", "x", warn=True)}',
                     M + 'polygon-s23.mp4', notes=pg.notes(23)))
S.append(split_media('pg-p3', 'Delete a Shape', K,
                     f'<p class="lede">Press {kbd("Esc")} on your keyboard so you can select the shape, then delete it.</p>',
                     M + 'polygon-s24.mp4', notes=pg.notes(24)))
S.append(split_media('pg-p4', 'Check the Edges with B', K,
                     f'<p class="lede">Press {kbd("B")} repeatedly to check the <b>precision</b> on the edges of your shape.</p>',
                     M + 'polygon-s25.mp4', notes=pg.notes(25)))
S.append(split_media('pg-p5', 'Shorter Segments on Curves', K,
                     '<p class="lede">On curves, reduce the length of each polygon line (more, closer points) to get an accurate outline.</p>',
                     M + 'polygon-s26.mp4', notes=pg.notes(26)))
S.append(content('pg-keys', 'Polygon Essentials', 'Polygon Basics', f'''
  <div class="icard-grid cols-3">
    <div class="icard"><div class="icard-ic">{icon("layers", 28)}</div><div class="icard-t">Draw</div><div class="icard-d">Click points around the edges and close the shape on the first point.</div></div>
    <div class="icard"><div class="icard-ic">{icon("arrow", 28)}</div><div class="icard-t">{kbd("Backspace")}</div><div class="icard-d">Undo the last point while drawing.</div></div>
    <div class="icard"><div class="icard-ic">{icon("x", 28)}</div><div class="icard-t">{kbd("Esc")} then Delete</div><div class="icard-d">Select the finished shape, then delete it.</div></div>
    <div class="icard"><div class="icard-ic">{icon("spark", 28)}</div><div class="icard-t">{kbd("Ctrl")} / {kbd("Alt")} + Click</div><div class="icard-d">Add or remove a point on the outline.</div></div>
    <div class="icard"><div class="icard-ic">{icon("eye", 28)}</div><div class="icard-t">{kbd("B")} Borders</div><div class="icard-d">Toggle borders repeatedly to check the edges.</div></div>
    <div class="icard"><div class="icard-ic">{icon("target", 28)}</div><div class="icard-t">Zoom on Curves</div><div class="icard-d">Zoom in and use shorter segments where the edge bends.</div></div>
  </div>''', eyebrow='Quick Recap'))
S.append(content('pg-demo', 'Practical Demonstration', 'Hands-on', f'''
{steps_list(["Go to your Dashboard projects.", "Select the <b>NIA_Polygon</b> project.", "Click on <b>Start Task</b>.", "Hold on for further instructions."])}
{note("To label precisely, <b>zoom in</b> and label the edges.", "target")}''', eyebrow='Polygon', notes=pg.notes(28)))
S.append(pg.guide(31, 'Log In to the Dashboard', 'Hands-on'))
S.append(practice('pg-practice', 'Polygon Practice',
                  'Open the NIA_Polygon project in Synapse and start your task.',
                  ['Points on the object edge', 'Shorter segments on curves', 'Zoom in before closing',
                   'Press B to check edges', 'Fix points with Ctrl / Alt + click', 'Save often']))

# ---------------- rail & catenary ----------------
K = 'Rail &amp; Catenary'
S.append(section('rc-sec', 'Rail &amp; Catenary Condition Awareness', 'Session 4',
                 'Bounding box and polygon project guideline, ver. 2.0', 'shield', 'layers'))
S.append(ip_notice('rc-notice', K, rc.notes(2)))
S.append(split_media('rc-purpose', 'Purpose of the Project', K, f'''
      <p class="lede">The purpose is to <b>identify damaged tools</b> in the rail stations that could cause train accidents.</p>
      {bullets(["This is a <b>bounding box</b> and <b>polygon</b> project.",
                "Two areas: the <b>rail</b> (pandrol e-clip, insulation block) and the <b>catenary</b> (long ear, insulator)."])}''',
    M + 'rail-tunnel.png', eyebrow='Project Overview', notes=rc.notes(4)))
S.append(pg.guide(30, 'This Project Has Two Categories', 'Project Overview'))
S.append(section('rc-rail', 'Rail', K, 'pandrol_e-clip &middot; insulation_block', 'box', 'box', notes=rc.notes(5)))
S += rc.guides([
    (6, 'Rail: Tools, Classes and States'),
    (7, 'pandrol_e-clip: Normal'),
    (8, 'pandrol_e-clip: Abnormal'),
    (9, 'insulation_block: Normal'),
    (10, 'insulation_block: Abnormal'),
    (11, 'insulation_block: Abnormal, Moved'),
], 'Rail')
S.append(section('rc-cat', 'Catenary', K, 'long_ear &middot; insulator', 'layers', 'layers', notes=rc.notes(12)))
S.append(content('rc-cat-criteria', 'Catenary: Labelling Criteria', 'Catenary', f'''
  <div class="split-img" style="grid-template-columns:1fr 1.1fr">
{table(['Tool', 'Class', 'State'], [
    ['Polygon', 'long_ear', 'normal &middot; abnormal'],
    ['B-box', 'insulator', 'normal &middot; abnormal'],
])}
    <img src="{M}rail-catenary.png" alt="Catenary with insulator and long ear labelled">
  </div>''', eyebrow='Labelling Criteria', notes=rc.notes(13)))
S += rc.guides([
    (14, 'long_ear: Polygon Along the Outline'),
    (15, 'long_ear: Normal or Abnormal'),
    (16, 'long_ear: Examples'),
    (17, 'Insulator: Box Along the Outline'),
    (18, 'Insulator: Normal or Abnormal'),
    (19, 'Insulator: Broken Is Abnormal'),
], 'Catenary')
S.append(content('rc-rules', 'Common Rules', K, steps_list([
    'Label with one bounding box per object.',
    'Annotations are tagged for each end of the object, and multiple annotations can overlap.',
    'If part of the object is invisible or occluded, label the visible part only.',
    'Label the object as far as it is visible, regardless of its visible range.',
]) + '\n' + note('Choose <b>normal</b> or <b>abnormal</b> for every object based on its condition.', 'check'),
    eyebrow='Precaution', notes=rc.notes(21)))
S.append(practice('rc-practice', 'Rail &amp; Catenary Practice',
                  'Open the Rail &amp; Catenary project in Synapse and start labelling.',
                  ['Right tool per class', 'normal / abnormal on every object', 'Visible part only when occluded',
                   'Moved parts: follow the guide', 'Zoom in on small clips', 'Save often']))

# ---------------- wrap-up ----------------
S.append(content('d2-recap', 'Day 2 Recap', 'Wrap-Up', icards([
    ('trend', 'Polylines', 'Draw through the centre, edit points, and label lanes by type and colour'),
    ('layers', 'Polygons', 'Trace exact outlines with shorter segments on curves, and check edges with B'),
    ('clipboard', 'Two Projects', 'Traffic Flow lanes and Rail &amp; Catenary condition checks'),
]) + '\n' + note('Precision is the habit that carries into every project from here on.')))
S.append(content('d2-ahead', 'Looking Ahead: Day 3', 'Wrap-Up', pipe([
    ('Semantic Segmentation', 'Pixel-level labelling of whole scenes'),
    ('PCD Training', '3D point-cloud annotation from LiDAR'),
    ('Photobooth Project', 'Image labelling project guideline and practice'),
]) + '\n' + note('Tomorrow your polygon skills scale up to full scenes and into 3D.', 'trend')))
S.append(section('d2-end', 'Thank You', 'End of Day 2',
                 'Questions? Let&rsquo;s discuss before we close for today.<br>See you tomorrow for Day 3: Semantic Segmentation, PCD &amp; Photobooth.',
                 'star', 'check', data_title='Thank You'))

write_deck('Day2.html', 'Day 2: Data Labelling Training for AI | Kenya ITC × datamaker', S)
