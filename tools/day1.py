"""Day 1: Synapse Dashboard, Bounding Box, CCTV Bounding Box project.

Sources (KENYA ITC/GUIDES/DAY 1/DATA ANNOTATION):
  SYNAPSE DASHBOARD TRAINING.pptx      -> synapse
  BOUNDING BOX - SYNAPSE.pptx          -> bbox
  CCTV Bounding Box Project_Guideline  -> cctv
The MICROSOFT OFFICE SUITE FILES folder is intentionally not used.
"""
from deck import *

syn = Source(1, 'synapse')
bb = Source(1, 'bbox')
cc = Source(1, 'cctv')

S = []

# ---------------- opening ----------------
S.append(title_slide(
    'd1-title', 1, 'Synapse Platform &amp;<br>Bounding Box Annotation', PARTNERS,
    [('monitor', 'Hands-on in Datamaker Synapse, in the browser'),
     ('globe', 'Kenya ITC Training 2026')]))

S.append(content('d1-journey', 'Your Five-Day Journey', 'Overview', f'''
  <p class="lede">From your first bounding box today to generative AI and vibe coding on Day 5.</p>
{journey(1)}
{note("Each day builds on the last: the accuracy habits you form today carry into every tool that follows.", "trend")}''',
    eyebrow='Program Overview'))

S.append(content('d1-agenda', 'Today&rsquo;s Agenda', 'Overview', agenda([
    ('Synapse Platform Intro: environment, login &amp; language', 'Theory'),
    ('Labelling &amp; Review Dashboards', 'Theory'),
    ('Labelling Tools &amp; Keyboard Shortcuts', 'Theory'),
    ('Bounding Box Basics: draw, delete, move, zoom', 'Hands-on'),
    ('Categories &amp; Display Toggles (L / B / G)', 'Hands-on'),
    ('Using the Pen Tool', 'Hands-on'),
    ('CCTV Bounding Box Project: guideline &amp; practice', 'Hands-on'),
]), eyebrow='Day 1 Overview', h='h1'))

# ---------------- part 1: Synapse dashboard ----------------
K = 'Synapse Dashboard'
S.append(section('syn-sec', 'Synapse Dashboard Training', 'Session 1',
                 'The platform you will use for every labelling task this week', 'monitor', 'layers'))

S.append(content('syn-toc', 'What We Will Cover', K, icards([
    ('monitor', 'Platform Intro', 'User environment &middot; Main dashboard &middot; Project page'),
    ('pen', 'Labelling Tools', 'Top bar &middot; Tool bar &middot; Shortcuts / settings &middot; Preferences'),
    ('keyboard', 'Shortcuts', 'The keys that make you fast: create, select, revert, zoom, show / lock'),
]), eyebrow='Table of Contents', notes=syn.notes(2)))

S.append(section('syn-intro', 'Synapse Intro', 'Platform Intro', ic='monitor', deco_ic='globe'))

S.append(content('syn-env', 'The Synapse Environment', 'Platform Intro', f'''
  <div class="compare2">
    <div class="cmp-col"><div class="cmp-head">{icon("globe")}<span>Web App</span></div>
      <ul class="bl"><li>To use the Synapse platform for data labelling, log into the web app at:</li></ul>
      <a class="link-chip" href="http://platform.datamaker.io" target="_blank" rel="noopener">platform.datamaker.io</a></div>
    <div class="cmp-vs">{icon("arrow", 22)}</div>
    <div class="cmp-col accent"><div class="cmp-head">{icon("monitor")}<span>Required Browser</span></div>
      <ul class="bl"><li>The required browser for the Synapse web application is <b>Google Chrome</b>.</li>
      <li>Everything today runs in the browser. There is nothing to install.</li></ul></div>
  </div>''', eyebrow='Synapse Environment', notes=syn.notes(4)))

S += syn.guides([
    (5, 'Web App Login'),
    (6, 'Language Settings'),
    (7, 'Labelling Dashboard'),
    (8, 'Project Page: Start or Continue Labelling'),
    (9, 'Project Page: Search by Assignment ID'),
    (10, 'Project Page: Tasks per Page'),
    (11, 'Project Page: Filters'),
    (12, 'Project Page: Guidelines'),
    (13, 'Review Dashboard'),
    (14, 'Review Project Page: Worker'),
    (15, 'Review Project Page: Work Status'),
    (16, 'Review Project Page: Filters'),
], 'Platform Intro')

S.append(section('syn-tools', 'Labelling Tools', 'Synapse Tools', 'Seven annotation tools, one editor', 'pen', 'box'))
S.append(content('syn-tools-ov', 'Seven Tools in One Editor', 'Labelling Tools', icards([
    ('box', 'Bounding Box', 'Rectangles around objects (today&rsquo;s focus)'),
    ('layers', 'Polygon Segmentation', 'Exact outlines of object shapes (Day 2)'),
    ('trend', 'Polyline Segmentation', 'Lines for lanes, rails and edges (Day 2)'),
    ('target', 'Keypoints', 'Landmark points on people and objects'),
    ('cube', '3D Bounding Box', 'Cuboids in LiDAR point clouds (Day 3)'),
    ('image', '3D Semantic Segmentation', 'Per-point classes in point clouds (Day 3)'),
], cols=3, extra='compact') + '\n' + note('Plus <b>Classification</b>: tagging a whole image or scene with a label. The next slides show each tool in the editor.', 'list')))
S += syn.guides([
    (18, 'Bounding Box'),
    (19, 'Polygon Segmentation'),
    (20, 'Polyline Segmentation'),
    (21, 'Keypoints'),
    (22, '3D Bounding Box'),
    (23, '3D Semantic Segmentation'),
    (24, 'Classification'),
], 'Labelling Tools')

S.append(section('syn-sc', 'Shortcuts', 'Synapse Tools', 'Learn ten keys and you will label twice as fast', 'keyboard', 'keyboard'))
S += syn.guides([
    (26, 'Shortcuts: Create / Delete'),
    (27, 'Shortcuts: Select / Move'),
    (28, 'Shortcuts: Cancel / Revert'),
    (29, 'Shortcuts: Image Size'),
    (30, 'Shortcuts: Show / Lock'),
    (31, 'Shortcuts: Display Mode'),
    (32, 'Shortcuts: Etc.'),
], 'Shortcuts')


def sc_card(head, rows):
    r = ''.join(f'<div class="sc-row">{kbd(k)}<span>{d}</span></div>' for k, d in rows)
    return f'<div class="sc-card"><div class="sc-head">{head}</div>{r}</div>'


S.append(content('syn-cheat', 'Shortcut Cheat Sheet', 'Shortcuts', '  <div class="sc-grid">' + ''.join([
    sc_card('Create / Delete', [('Enter', 'Finish drawing / deselect'), ('Esc', 'Cancel drawing / deselect'),
                                ('D', 'Delete selected annotations'), ('Ctrl + C / V', 'Copy / paste annotations')]),
    sc_card('Cancel / Revert', [('Ctrl + Z', 'Undo'), ('Ctrl + Shift + Z', 'Redo'),
                                ('Backspace', 'Undo polygon / polyline point'), ('Ctrl + S', 'Save annotations')]),
    sc_card('Image Size', [('+ / &minus;', 'Zoom in / out'), ('Space + drag', 'Move the image'),
                           ('H / V', 'Fit image horizontally / vertically'), ('N', 'Fit image to natural size')]),
    sc_card('Select / Move', [('O / P', 'Select previous / next annotation'), ('F', 'Focus annotations'),
                              ('Arrow keys', 'Move selection 1px'), ('Shift + arrows', 'Move selection 10px')]),
    sc_card('Show / Lock', [('L', 'Show / hide labels'), ('B', 'Show / hide boundaries'),
                            ('G', 'Show / hide cross guides'), ('Ctrl + L / U', 'Lock / unlock selected')]),
    sc_card('Tasks &amp; Display', [('Ctrl + Alt + &rarr;', 'Next assignment task'), ('Ctrl + Alt + &larr;', 'Previous assignment task'),
                                   ('Shift + 1&ndash;4', 'Normal / mask display modes'), ('A', 'Toggle image smoothing')]),
]) + '</div>', eyebrow='Keep This Slide Open'))

# ---------------- part 2: bounding box ----------------
K = 'Bounding Box Basics'
S.append(section('bb-sec', 'Bounding Box Annotation', 'Session 2',
                 'Day 1 training practice session: the core skill behind most computer vision datasets', 'box', 'box'))

S.append(content('bb-what', 'What Is a Bounding Box?', K, f'''
  <div class="split-img">
    <div>
      <p class="lede">A bounding box is an imaginary rectangle that serves as a <b>point of reference</b> for object detection and creates a <b>collision box</b> for that object in image-processing projects.</p>
      {bullets(["Drawn <b>tightly</b> around the object, with edges touching its outermost pixels.",
                "Each box gets a <b>category</b> (class) so the AI learns what the object is.",
                "Fast to draw and used in a huge range of real projects."])}
    </div>
    <img src="assets/day1/media/bbox-example-street.png" alt="Street scene with bounding boxes on people and vehicles">
  </div>''', notes=bb.notes(3)))

S += bb.guides([
    (4, 'How to Draw a Box (1/3)'),
    (5, 'How to Draw a Box (2/3)'),
    (6, 'How to Draw a Box (3/3)'),
    (7, 'Example of Bounding Boxes'),
    (8, 'Example of Bounding Boxes'),
    (9, 'Example: Camera'),
    (10, 'Example: Chair'),
    (11, 'Example: Avocado'),
    (12, 'Example: Red Pepper'),
    (13, 'Example: Globe'),
    (14, 'Example: Clock'),
    (15, 'Example: Cone'),
    (16, 'Delete a Box: Select It'),
    (17, 'Delete a Box: Press D'),
    (18, 'Delete a Box: Right After Drawing'),
    (19, 'Reduce Image Transparency'),
    (20, 'Zoom In and Out'),
    (21, 'Move a Box (1/3)'),
    (22, 'Move a Box (2/3)'),
    (23, 'Move a Box (3/3)'),
], K)

S.append(content('bb-cat', 'Categories (Classes)', K, f'''
  <p class="lede">These are the objects you want the AI model to recognise. They are organised into <b>categories</b>, also known as <b>classes</b>, which may have different states or subcategories depending on the project. A project can have anywhere from 1 to 12 or more classes.</p>
  <div class="tree">
    <div class="tree-root">Vegetable</div>
    <div class="tree-kids">
      <div class="tree-kid"><b>Cabbage</b><span>Fresh</span><span>Not Fresh</span></div>
      <div class="tree-kid"><b>Lettuce</b><span>Green</span><span>Not Fresh</span></div>
      <div class="tree-kid"><b>Carrot</b><span>Fresh</span><span>Not Fresh</span></div>
    </div>
  </div>
  <div class="tree-lvl"><span>Main category</span>&rarr;<span>Subcategory</span>&rarr;<span>State</span></div>
{note("With many classes, organise your work, manage your time well and complete tasks within the given deadlines.", "clipboard")}''',
    notes=bb.notes(24)))

S += bb.guides([
    (25, 'Choosing the Main Category'),
    (26, 'Choosing the Subcategory'),
    (27, 'Choosing the Subcategory State'),
    (28, 'Toggle Labels  [L]'),
    (29, 'Toggle Borders  [B]'),
    (30, 'Toggle the White Guideline  [G]'),
], K)

S.append(content('bb-keys', 'Bounding Box Essentials', K, f'''
  <div class="icard-grid cols-3">
    <div class="icard"><div class="icard-ic">{icon("box", 28)}</div><div class="icard-t">Draw</div><div class="icard-d">Click and drag diagonally from one corner to the opposite corner.</div></div>
    <div class="icard"><div class="icard-ic">{icon("x", 28)}</div><div class="icard-t">{kbd("D")} Delete</div><div class="icard-d">Click the box to select it, then press D, or press D right after drawing.</div></div>
    <div class="icard"><div class="icard-ic">{icon("hand", 28)}</div><div class="icard-t">Move &amp; Zoom</div><div class="icard-d">Hold click and drag to move a box. Use the zoom buttons to check the edges.</div></div>
    <div class="icard"><div class="icard-ic">{icon("list", 28)}</div><div class="icard-t">{kbd("L")} Labels</div><div class="icard-d">Turn class labels on or off while labelling.</div></div>
    <div class="icard"><div class="icard-ic">{icon("eye", 28)}</div><div class="icard-t">{kbd("B")} Borders</div><div class="icard-d">Turn box borders on or off to see the object underneath.</div></div>
    <div class="icard"><div class="icard-ic">{icon("target", 28)}</div><div class="icard-t">{kbd("G")} Guideline</div><div class="icard-d">Turn the white cross guideline on or off for precise corners.</div></div>
  </div>''', eyebrow='Quick Recap'))

S.append(practice('bb-practice', 'Labelling Practice',
                  'Open Datamaker Synapse and draw boxes on your practice images.',
                  ['Box edges tight on the object', 'Correct category on each box', 'Zoom in before finalising',
                   'Use D to delete mistakes', 'Toggle L / B / G to check', 'Save often']))

# ---------------- pen tool ----------------
K = 'Using the Pen Tool'
S.append(section('pen-sec', 'Using the Pen Tool', 'Session 3',
                 'Good posture keeps you accurate and prevents strain over long sessions', 'pen', 'pen'))


def pen_slide(sid, n, title, media, text):
    if media.endswith('.mp4'):
        m = (f'<div><video src="assets/day1/media/{media}" autoplay muted loop playsinline style="width:100%;border-radius:12px;box-shadow:var(--shadow);display:block"></video>'
             f'<img class="print-only" src="assets/day1/media/{media[:-4]}.jpg" alt="{title}"></div>')
    else:
        m = f'<img src="assets/day1/media/{media}" alt="{title}">'
    return content(sid, title, K, f'''
  <div class="split-img">
    <div><p class="lede">{text}</p>
      <p class="img-cap" style="text-align:left">Source: <i>How to Hold a Stylus Pen Correctly (Prevent Carpal Tunnel!)</i>, nerdschalk.com</p></div>
    {m}
  </div>''', eyebrow='Stylus Grip', notes=bb.notes(n))


S.append(pen_slide('pen-1', 32, '1. Hold Your Pen Vertically', 'pen-s32.jpg',
                   'Keep the stylus upright rather than laid flat. It gives you finer control over the tip.'))
S.append(pen_slide('pen-2', 33, '2. Draw from the Shoulder', 'pen-s33.mp4',
                   'Move your whole arm from the shoulder for long strokes instead of flicking from the wrist.'))
S.append(pen_slide('pen-3', 34, '3. Don&rsquo;t Overuse the Wrist', 'pen-s34.mp4',
                   'Overusing the wrist leads to inflammation over long labelling sessions.'))
S.append(pen_slide('pen-4', 35, '4. Keep Your Grip as Light as Possible', 'pen-s35.mp4',
                   'A light grip reduces tension in your hand and forearm and keeps lines steady.'))

# ---------------- CCTV project ----------------
K = 'CCTV Project'
S.append(section('cctv-sec', 'Bounding Box Training Project', 'Session 4',
                 'CCTV Bounding Box Project, guideline ver. 1.3', 'clipboard', 'box'))

S.append(content('cctv-task', 'CCTV Bounding Box Project', K, f'''
  <div class="split-img">
    <div>
      <p class="lede">Bound each <b>person&rsquo;s face</b> and each <b>car plate</b> in a box, precisely.</p>
      {bullets([f"Choose the {kbd('face')} category for each person.",
                f"Choose {kbd('car_plate')} for every vehicle licence plate."])}
    </div>
    <img src="assets/day1/media/cctv-night.jpg" alt="CCTV night street scene">
  </div>''', eyebrow='Your Task', notes=bb.notes(38)))

S += bb.guides([
    (39, 'Open the Dashboard and Select the Project'),
    (40, 'Download the Project Guide'),
    (41, 'Start Work on the Project'),
    (42, 'Start Work on the Project'),
], K)

S.append(content('cctv-notice', 'Before You Start', K, f'''
  <div class="compare2">
    <div class="cmp-col"><div class="cmp-head">{icon("shield")}<span>Training Material</span></div>
      <ul class="bl"><li>This file is intended for training <b>datamaker</b> workers.</li>
      <li>All images and content are the intellectual property of datamaker; unauthorised distribution and reproduction may be subject to legal sanctions.</li></ul></div>
    <div class="cmp-vs">{icon("arrow", 22)}</div>
    <div class="cmp-col accent"><div class="cmp-head">{icon("alert")}<span>Personal Information</span></div>
      <ul class="bl"><li>This project highlights the importance of protecting personal information.</li>
      <li>Keep the data in this project <b>confidential</b>.</li>
      <li>Any data copied or exposed will be tracked.</li></ul></div>
  </div>''', eyebrow='Warning', notes=cc.notes(2)))

S.append(content('cctv-purpose', 'Purpose of the Project', K, icards([
    ('target', 'Purpose', 'A project to detect and encrypt personal information in CCTV footage, such as human faces and vehicle licence plates.'),
    ('user', 'Box the Face', 'The face is a labelling target and the <b>ears are included</b>. The back of a head is not a target. Faces that are tiny or unidentifiable are still targets.'),
    ('car', 'Box the Licence Plate', 'Include all letters and numbers. Label plates even if the characters are unreadable, as long as the plate edges are visible. Motorcycle plates are targets.'),
]), eyebrow='Project Overview', notes=cc.notes(5)))

S.append(content('cctv-criteria', 'Labelling Criteria at a Glance', K, checklist([
    (True, 'Only the face is the target, not the hair.'),
    (True, 'Masks and glasses on the face are included.'),
    (False, 'Earplugs, scarves, bags, umbrellas, helmets, hats and handheld accessories are not targets.'),
    (True, 'If earplugs or a phone cover the face, estimate the face range and label it.'),
    (False, 'The back of a person / back or top of the head without a face is not a target.'),
    (True, 'Faces reflected in glass, a mirror or an elevator wall are targets.'),
    (True, 'For side faces, include the ears.'),
    (True, 'No person in the image? Press <b>Skip</b> without labelling.'),
]) + '\n' + note('This is a <b>face</b> labelling project. When in doubt, ask: is there a face here?', 'user'),
    eyebrow='Labelling Target', notes=cc.notes(6)))

S += cc.guides([
    (6, 'Labelling Target: Examples'),
    (7, 'Labelling Criteria: Heads Without Faces'),
    (8, 'Labelling Criteria: No Person &rarr; Skip'),
    (9, 'Labelling Detail: Licence Plates'),
], 'Project Overview')

S.append(section('cctv-prec', 'Precautions', 'CCTV Project', 'Licence plate labelling', 'alert', 'car'))
S += cc.guides([
    (11, 'Include the Whole Plate'),
    (12, 'Obscured Plates: Estimate the Range'),
    (13, 'Motorbike Plates Are Targets'),
], 'Precaution')

S.append(practice('cctv-practice', 'CCTV Project Practice',
                  'Open the CCTV Bounding Box project in Synapse and start labelling.',
                  ['Every face boxed, ears included', 'Every plate boxed, incl. motorbikes', 'No hair, hats or helmets',
                   'Skip images with no person', 'Estimate obscured plates', 'Keep the data confidential']))

# ---------------- wrap-up ----------------
S.append(content('d1-recap', 'Day 1 Recap', 'Wrap-Up', icards([
    ('monitor', 'Synapse Platform', 'Login in Chrome, labelling and review dashboards, project pages and filters'),
    ('box', 'Bounding Boxes', 'Draw, delete, move, zoom, categories and the L / B / G toggles'),
    ('clipboard', 'A Real Project', 'CCTV faces and licence plates, following a project guideline'),
]) + '\n' + note('Well done! You went from &ldquo;what is a bounding box&rdquo; to working on a real guideline-driven project.')))

S.append(content('d1-ahead', 'Looking Ahead: Day 2', 'Wrap-Up', pipe([
    ('Polyline', 'Lines for lanes, edges and boundaries'),
    ('Traffic Flow Project', 'Polylines for autonomous-driving lanes'),
    ('Polygon', 'Exact outlines around object shapes'),
    ('Rail &amp; Catenary', 'Condition-awareness labelling project'),
]) + '\n' + note('The precision you practised with boxes today is the foundation for polylines and polygons tomorrow.', 'trend')))

S.append(section('d1-end', 'Thank You', 'End of Day 1',
                 'Questions? Let&rsquo;s discuss before we close for today.<br>See you tomorrow for Day 2: Polyline &amp; Polygon Annotation.',
                 'star', 'check', data_title='Thank You'))

write_deck('Day1.html', 'Day 1: Data Labelling Training for AI | Kenya ITC × datamaker', S)
