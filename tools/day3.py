"""Day 3: Semantic Segmentation, PCD (3D point cloud), Photobooth project.

Sources (KENYA ITC/GUIDES/DAY 3):
  SEMANTIC SEGMENTATION.pptx              -> semantic
  PCD TRAINING MANUAL.pptx                -> pcd
  Photobooth Image Labeling Project.pptx  -> photobooth (see photobooth.py)

Day 3 is two files numbered as one sequence, like the HQ Day 1:
  Day3.html            Semantic + PCD
  Day3-Photobooth.html Photobooth project + wrap-up
"""
from deck import *
from photobooth import photobooth_slides

sm = Source(3, 'semantic')
pc = Source(3, 'pcd')
M = 'assets/day3/media/'


def video_slide(sid, title, kicker, src, caption, notes=''):
    return content(sid, title, kicker, f'''
  <div style="flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <div class="vid-box">{media(src, title)}</div>
    <p class="img-cap">{caption}</p>
  </div>''', notes=notes)


A = []

# ---------------- opening ----------------
A.append(title_slide(
    'd3-title', 3, 'Semantic Segmentation,<br>PCD &amp; Photobooth', PARTNERS,
    [('monitor', 'Hands-on in Datamaker Synapse'), ('globe', 'Kenya ITC Training 2026')]))
A.append(content('d3-journey', 'Where We Are', 'Overview', f'''
  <p class="lede">From outlines to whole scenes, and from flat images into 3D.</p>
{journey(3)}''', eyebrow='Program Overview'))
A.append(content('d3-agenda', 'Today&rsquo;s Agenda', 'Overview', agenda([
    ('Semantic Segmentation: drawing, editing, front and rear mode', 'Hands-on'),
    ('Understanding 3D and LiDAR fundamentals', 'Theory'),
    ('PCD (Point Cloud Data) project guideline and dashboard', 'Theory'),
    ('PCD practice', 'Hands-on'),
    ('Photobooth Image Labelling project: guideline and practice', 'Hands-on'),
]), eyebrow='Day 3 Overview', h='h1'))

# ---------------- semantic segmentation ----------------
K = 'Semantic Segmentation'
A.append(section('sm-sec', 'Semantic Segmentation', 'Session 1',
                 'Pixel-level labelling of every object in the scene', 'image', 'layers'))
A.append(split_media('sm-what', 'What Is Semantic Segmentation?', K, f'''
      <p class="lede">Semantic segmentation is a <b>group of pixels</b> that acts as a <b>reference point for object detection</b> and produces a <b>mesh-like map</b> for that object.</p>
      {bullets(["Annotators group the pixels by drawing over the image.",
                "Every pixel of the object gets the object&rsquo;s class, for example <b>body</b>."])}''',
    M + 'semantic-mask.jpg', notes=sm.notes(2)))
A.append(section('sm-how', 'How to Draw in Semantic Segmentation', K, 'Six steps from tool to class', 'pen', 'image',
                 notes=sm.notes(3)))
A += sm.guides([
    (4, 'Step 1: Select the Polygon Tool'),
    (5, 'Step 2: Click Along the Edges'),
    (6, 'Step 3: Continue Along the Edges'),
    (7, 'Step 3: Continue Along the Edges'),
    (8, 'Step 3: Continue Along the Edges'),
    (9, 'Step 3: Continue Along the Edges'),
    (10, 'Step 3: Close the Shape'),
    (11, 'Step 4: Press Enter When Complete'),
    (12, 'Step 5: Open the Class Dropdown'),
    (13, 'Step 6: Select the Class'),
    (14, 'Result: The Labelled Mask'),
    (15, 'Result: Mask View'),
], 'How to Draw')


def backspace_slide(sid, n, step):
    return split_media(sid, f'Remove the Current Point ({step}/3)', K,
                       f'<p class="lede">Made a wrong click while drawing? Press {kbd("Backspace")} on the keyboard to remove the current point.</p>'
                       f'<p class="lede">The red arrow shows the point that will be removed.</p>',
                       M + f'semantic-backspace-{n}.jpg', eyebrow='Delete a Point', notes=sm.notes(n))


A += [backspace_slide('sm-bs1', 16, 1), backspace_slide('sm-bs2', 17, 2), backspace_slide('sm-bs3', 18, 3)]
A += sm.guides([
    (19, 'Reduce Image Brightness'),
    (20, 'Increase Image Brightness'),
    (21, 'Zoom In and Out'),
], 'Image Controls')

A.append(section('sm-other', 'Other Tools for Annotation', K, 'Front mode and rear mode', 'layers', 'layers',
                 notes=sm.notes(22)))
A.append(content('sm-fr', 'Front and Rear Mode', K, f'''
  <div class="compare2">
    <div class="cmp-col accent"><div class="cmp-head">{icon("layers")}<span>Front Mode {kbd("Shift + F")}</span></div>
      <ul class="bl"><li>If there is an existing shape, you <b>draw on top</b> of that shape.</li></ul></div>
    <div class="cmp-vs">{icon("arrow", 22)}</div>
    <div class="cmp-col"><div class="cmp-head">{icon("layers")}<span>Rear Mode {kbd("Shift + R")}</span></div>
      <ul class="bl"><li>If there is an existing shape, you <b>draw behind</b> that shape.</li></ul></div>
  </div>
  <ul class="bl" style="margin-top:18px">
    <li>These modes apply to all the main tools. You can only use one at a time.</li>
    <li>If no shape is drawn in that region yet, front or rear mode gives the same result.</li>
    <li>You can leave it in rear mode, so that every new shape falls behind the others.</li>
  </ul>''', eyebrow='Other Tools', notes=sm.notes(24)))
A += sm.guides([
    (26, 'Example: Polygon in Front Mode'),
    (27, 'The First Person Is Already Labelled'),
    (28, 'Front Mode Draws on Top'),
    (29, 'Rear Mode Draws Behind'),
], 'Front and Rear Mode')
A.append(section('sm-ex', 'Other Examples', K, ic='image', deco_ic='layers', notes=sm.notes(30)))
A += sm.guides([
    (31, 'If the Other Person Is Drawn First'),
    (32, 'Label the Next Person in Rear Mode'),
    (33, 'Without Worrying About the Existing Object'),
    (34, 'Finished Scene'),
    (35, 'Annotate to Front'),
    (36, 'Annotate to Back'),
], 'Front and Rear Mode')
A.append(practice('sm-practice', 'Semantic Practice',
                  'Open your semantic segmentation task in Synapse and label every person.',
                  ['Polygon tool selected', 'Points along the true edge', 'Enter to finish, then pick the class',
                   'Backspace to remove a wrong point', 'Use front / rear mode for overlaps', 'Save often']))

# ---------------- PCD: 3D and LiDAR ----------------
K = '3D &amp; LiDAR'
A.append(section('pc-sec', 'Understanding 3D and LiDAR Fundamentals', 'Session 2',
                 'Introduction to three-dimensional space and the principles of LiDAR', 'cube', 'cube', notes=pc.notes(1)))
A.append(split_media('pc-3d', 'Introduction to Three-Dimensional Space', K, f'''
      <p class="lede"><b>3D (three-dimensional):</b> we normally talk about dimensions as measurements in a direction.</p>
      <p class="lede">Real-world objects exist in 3D space, allowing deeper perception through <b>height, width and depth</b>.</p>''',
    M + 'pcd-s02-1.jpg', eyebrow='3D Space', notes=pc.notes(2)))
A.append(content('pc-xyz', 'Spatial Coordinates and Dimensions', K, f'''
  <p class="lede">Spatial coordinates use the <b>X, Y and Z axes</b> to locate points in 3D space.</p>
{icards([
    ('arrow', 'X: Horizontal', 'The horizontal position (left or right).'),
    ('trend', 'Y: Vertical', 'The vertical position (up or down).'),
    ('cube', 'Z: Depth', 'The depth, or position along the third dimension.'),
])}''', eyebrow='Basics', notes=pc.notes(3)))
A.append(content('pc-uses', 'Uses of Spatial Coordinates and Dimensions', K, f'''
  <p class="lede">Dimensions add depth to objects, enhancing realism.</p>
{icards([
    ('monitor', 'Technology and Computing', 'Computer graphics, VR and simulation: realistic 3D environments, robotics and automation, VR / AR and GPS navigation.'),
    ('globe', 'Navigation and Mapping', 'Accurate navigation and mapping: find locations, plan routes and understand geographic relationships.'),
    ('car', 'Autonomous Vehicles', 'Mapping, navigation and object detection; localisation, map creation, path planning and safe intersection management.'),
])}''', eyebrow='Uses', notes=pc.notes(4)))
A.append(split_media('pc-lidar', 'LiDAR Fundamentals', K, f'''
      <p class="lede"><b>LiDAR</b> (Light Detection and Ranging) is a remote sensing technology that uses <b>laser pulses</b> to measure distances to objects or surfaces.</p>
      {bullets(["It creates detailed 3D maps.", "Used for mapping, navigation and urban planning."])}''',
    M + 'pcd-s06-1.png', eyebrow='LiDAR', notes=pc.notes(6)))
A.append(video_slide('pc-v1', 'LiDAR in Action', K, M + 'pcd-s07-1.mp4', 'A LiDAR point cloud of a street scene.', pc.notes(7)))
A.append(video_slide('pc-v2', 'LiDAR in Action', K, M + 'pcd-s08-1.mp4', 'A self-driving car scanning its surroundings with LiDAR.', pc.notes(8)))
A.append(content('pc-uses2', 'Uses of LiDAR Technology', K, icards([
    ('car', 'Autonomous Vehicles', 'LiDAR helps AVs &ldquo;see&rdquo; and navigate by detecting objects and creating maps.'),
    ('globe', 'Aerial Surveying', 'LiDAR-equipped aircraft and drones accurately map terrain, forests and cities.'),
    ('layers', 'GIS', 'Detailed maps for urban planning and environmental management.'),
    ('target', 'Archaeology', 'Uncovers hidden archaeological sites by scanning terrain with precision.'),
    ('spark', 'Forestry Monitoring', 'Measures tree heights and monitors forest health.'),
    ('alert', 'Disaster Management', 'Maps disaster areas to aid rescue operations and assess damage.'),
], extra='compact'), eyebrow='Applications', notes=pc.notes(9)))
A.append(video_slide('pc-v3', 'LiDAR Detects People', K, M + 'pcd-s11-1.mp4', 'Real-time detection of people.', pc.notes(11)))
A.append(video_slide('pc-v4', 'A City in Point Clouds', K, M + 'pcd-s12-1.mp4', 'A 3D point cloud of city streets and buildings.', pc.notes(12)))
A.append(content('pc-role', 'LiDAR&rsquo;s Role in Capturing 3D Data', K, '''  <div class="sc-grid">
    <div class="sc-card"><div class="sc-head">1. LiDAR Basics</div><div class="sc-row">Uses laser pulses for distance measurement</div><div class="sc-row">Creates detailed 3D maps</div></div>
    <div class="sc-card"><div class="sc-head">2. Distance Measurement</div><div class="sc-row">Measures the time for laser pulses to travel</div><div class="sc-row">Enables precise distance calculations</div></div>
    <div class="sc-card"><div class="sc-head">3. 360-Degree Coverage</div><div class="sc-row">Scans a wide field of view</div><div class="sc-row">Captures data from various angles</div></div>
    <div class="sc-card"><div class="sc-head">4. Real-time Data</div><div class="sc-row">Rapid data collection</div><div class="sc-row">Ideal for real-time applications</div></div>
    <div class="sc-card"><div class="sc-head">5. Obstacle Detection</div><div class="sc-row">Crucial for autonomous vehicles</div><div class="sc-row">Aids navigation in complex environments</div></div>
    <div class="sc-card"><div class="sc-head">6. Environmental Monitoring</div><div class="sc-row">Forestry, agriculture and urban planning</div><div class="sc-row">Assesses terrain, vegetation and structures</div></div>
  </div>''' + '\n' + note('<b>3D point clouds:</b> LiDAR captures reflections that form point clouds, each point a specific location in 3D, with high-precision measurements.', 'cube'),
    eyebrow='3D Data', notes=pc.notes(14)))
A.append(pc.guide(17, 'Conclusion', K))

# ---------------- PCD project ----------------
K = 'PCD Project'
A.append(section('pc-proj', 'Point Cloud Data (PCD) Project', 'Session 3',
                 'Introduction to the PCD project, guide, and the process of labelling', 'cube', 'cube', notes=pc.notes(18)))
A.append(content('pc-intro', 'Introduction to the PCD Project', K, f'''
  <p class="lede"><b>PCD</b> stands for <b>Point Cloud Data</b>: points that represent data picked up by a LiDAR signal.</p>
{img_row([(M + 'pcd-s19-1.jpg', 'A vehicle as a point cloud'), (M + 'pcd-s19-2.jpg', 'People as point clouds')], 240)}''',
    eyebrow='Introduction', notes=pc.notes(19)))
A.append(content('pc-why', 'Why Does This PCD Project Exist?', K, icards([
    ('target', 'Object Detection and Recognition', 'Autonomous vehicles must detect pedestrians, vehicles, cyclists and obstacles.'),
    ('eye', 'Depth Perception', 'Knowing the distance to objects is crucial for braking, lane changes and avoiding collisions.'),
    ('globe', 'Environment Understanding', 'Road boundaries, lane markings, traffic signs and other infrastructure.'),
    ('shield', 'Safety and Reliability', 'Accurate labels reduce the risk of misinterpreting the surroundings.'),
], cols=2, extra='compact'), eyebrow='Purpose', notes=pc.notes(20)))
A.append(section('pc-guide', 'PCD Project Guideline', K, 'Introduction to the PCD project guideline', 'clipboard', 'cube',
                 notes=pc.notes(22)))
A += pc.guides([
    (23, 'Project Overview: About the Project'),
    (24, 'Project Overview: Feedback We Need'),
    (25, 'Labelling Targets: 13 Classes'),
    (26, 'Labelling Targets: 2D Examples'),
], 'Project Overview')
A.append(section('pc-dash', 'Labelling Dashboard', K, 'The PCD tool and moving the camera', 'monitor', 'cube', notes=pc.notes(27)))
A += pc.guides([
    (28, 'Labelling Tool Description'),
    (29, 'Moving the Viewpoint'),
], 'Labelling Dashboard')
A.append(practice('pc-practice', 'PCD Practice',
                  'Open the PCD project in Synapse and start labelling the point cloud.',
                  ['Right class out of 13', 'Rotate the camera to check', 'Use the 2D projection',
                   'Report tool errors in detail', 'Suggest workflow ideas', 'Save often']))

# ---------------- second file: photobooth + wrap-up ----------------
B = photobooth_slides(3, 'Session 4')
B.append(content('d3-recap', 'Day 3 Recap', 'Wrap-Up', icards([
    ('image', 'Semantic Segmentation', 'Polygon masks for whole objects, Backspace fixes, and front / rear mode for overlaps'),
    ('cube', '3D and PCD', 'X, Y, Z coordinates, how LiDAR builds point clouds, and the 13-class PCD project'),
    ('user', 'Photobooth Project', 'Face boxes, body polygons and age / gender / brightness attributes'),
]) + '\n' + note('You have now labelled in 2D and 3D, the two worlds most AI vision systems live in.')))
B.append(content('d3-ahead', 'Looking Ahead: Day 4', 'Wrap-Up', pipe([
    ('Interior Segmentation', 'Segmentation project guideline for indoor scenes'),
    ('Photobooth Project', 'More practice on the photobooth dataset'),
    ('Generative AI', 'What generative AI is and how it works'),
    ('Prompt Engineering', 'How to write prompts that get good results'),
]) + '\n' + note('Tomorrow we finish the labelling projects and step into generative AI.', 'trend')))
B.append(section('d3-end', 'Thank You', 'End of Day 3',
                 'Questions? Let&rsquo;s discuss before we close for today.<br>See you tomorrow for Day 4: Interior Segmentation, Generative AI &amp; Prompt Engineering.',
                 'star', 'check', data_title='Thank You'))

write_deck('Day3.html', 'Day 3: Data Labelling Training for AI | Kenya ITC × datamaker', A, other=len(B))
write_deck('Day3-Photobooth.html', 'Day 3: Photobooth Project | Kenya ITC × datamaker', B, num_offset=len(A))
