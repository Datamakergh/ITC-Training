"""Day 4: Interior Segmentation, Photobooth, Introduction to Generative AI, Prompt Engineering.

Sources (KENYA ITC/GUIDES/DAY 4):
  Interior Segmentation Guideline.pptx                  -> interior
  Photobooth Image Labeling Project.pptx                -> photobooth (see photobooth.py)
  Introduction to Generative AI [02112026].pptx         -> genai
  Introduction to Prompt Engineering[02112026].pptx     -> prompt

The GenAI and Prompt Engineering decks are already designed slide-for-slide with full
speaker notes, so their slides are shown as-is (guide slides). The few slides whose text
ran past its box in the original are rebuilt natively below.

Two files, numbered as one sequence:
  Day4-Labeling.html  Interior + Photobooth
  Day4-GenAI.html     Generative AI + Prompt Engineering + wrap-up
"""
from deck import *
from photobooth import photobooth_slides

it = Source(4, 'interior')
ga = Source(4, 'genai')
pe = Source(4, 'prompt')


def takeaways(sid, src, n, points, footer_label, footer_text):
    cards = [('check', f'{i + 1}', t) for i, t in enumerate(points)]
    return content(sid, 'Four Things to Remember', 'Key Takeaways',
                   icards(cards, cols=4) + '\n' + note(f'<b>{footer_label}:</b> {footer_text}', 'arrow'),
                   eyebrow='Key Takeaways', notes=src.notes(n))


A = []

# ---------------- opening ----------------
A.append(title_slide(
    'd4-title', 4, 'Interior Segmentation,<br>Generative AI &amp; Prompting', PARTNERS,
    [('monitor', 'Hands-on in Synapse and AI chat tools'), ('globe', 'Kenya ITC Training 2026')]))
A.append(content('d4-journey', 'Where We Are', 'Overview', f'''
  <p class="lede">We finish the labelling projects, then learn how the AI that uses our labels actually works.</p>
{journey(4)}''', eyebrow='Program Overview'))
A.append(content('d4-agenda', 'Today&rsquo;s Agenda', 'Overview', agenda([
    ('Interior Segmentation project guideline', 'Theory'),
    ('Interior Segmentation practice', 'Hands-on'),
    ('Photobooth Image Labelling project practice', 'Hands-on'),
    ('Introduction to Generative AI: AI, ML, deep learning, transformers, hallucinations', 'Theory'),
    ('Introduction to Prompt Engineering: elements, tips, techniques, practice', 'Hands-on'),
]), eyebrow='Day 4 Overview', h='h1'))

# ---------------- interior segmentation ----------------
K = 'Interior Segmentation'
A.append(section('it-sec', 'Interior Segmentation Project', 'Session 1',
                 'Polygon project guideline, ver. 2.0', 'layers', 'layers'))
A.append(ip_notice('it-notice', K, it.notes(2)))
A.append(content('it-purpose', 'Purpose of the Project', K, f'''
  <p class="lede">Label <b>interior spaces</b> with the <b>polygon</b> tool and classify every object into <b>42 classes</b>. You view photos and tag objects to create the training dataset.</p>
{table(['Tool', 'Classes', 'Tips'], [
    ['Polygon', '42', 'Label complex borders (such as trees) in as much detail as possible.'],
    ['', '', 'Label distant objects first: they may overlap with nearby objects.'],
    ['', '', 'Every single object must be labelled separately.'],
])}''', eyebrow='Project Overview', notes=it.notes(4)))
A += it.guides([
    (6, 'Classes 1 to 11'),
    (7, 'Classes 12 to 22: Furniture'),
    (8, 'Classes 23 to 42: Computer, Appliance, Unknown'),
], 'Classes')
A.append(content('it-undefined', 'Use &ldquo;undefined&rdquo; Only When Nothing Fits', K, checklist([
    (False, 'Do not tag a category as <b>undefined</b> if a matching class already exists.'),
    (True, '<b>Door:</b> wooden doors, Turkish doors, etc.'),
    (True, '<b>Glass wall:</b> building exterior walls, meeting room walls (not glass in partitions).'),
    (True, '<b>Glass door:</b> all glass doors and frames connected to elevator spaces.'),
    (True, '<b>Signage:</b> ceiling bar, vertical, or anything advertising something.'),
    (True, '<b>Furniture: partition</b> includes glass partitions.'),
    (True, '<b>Appliance: floor vent / floor outlet:</b> air holes and power holes, even when closed.'),
    (True, '<b>Appliance: vending machine:</b> any vending machine type.'),
]), eyebrow='Class Rules', notes=it.notes(6)))
A += it.guides([
    (9, 'Shortcut: Shift + 1 / 2 / 3 Display Modes'),
    (10, 'How to Label: Polygons, Then Classes'),
], 'Labelling Order')
A.append(content('it-order', 'Labelling Order', K, pipe([
    ('Raw data', 'Study the whole interior scene first.'),
    ('Create polygons', 'One polygon per object, distant objects first, with no gaps between polygons.'),
    ('Tag classes', 'Pick the right class out of 42 for every polygon.'),
    ('Check colours', f'{kbd("Shift + 2")} / {kbd("Shift + 3")} show the colour mask, so gaps stand out.'),
]) + '\n' + note('Be careful not to leave any spaces between polygons.', 'alert', warn=True),
    eyebrow='Quick Recap', notes=it.notes(10)))
A.append(practice('it-practice', 'Interior Practice',
                  'Open the Interior Segmentation project in Synapse and start labelling.',
                  ['Distant objects first', 'Every object its own polygon', 'No gaps between polygons',
                   'Right class out of 42', 'Undefined only as last resort', 'Check with Shift + 2 / 3']))

A += photobooth_slides(4, 'Session 2')

# ---------------- second file: GenAI + Prompt Engineering ----------------
B = []
K = 'Generative AI'
B.append(section('ga-sec', 'Introduction to Generative AI', 'Session 3',
                 'From artificial intelligence and machine learning to deep learning, transformers and hallucinations',
                 'spark', 'spark', notes=ga.notes(1)))
GA = [
    (2, 'Overview'), (3, 'Part 1: Artificial Intelligence'), (4, 'What Is Artificial Intelligence?'),
    (5, 'A Short History of AI'), (6, 'Is a Plane&rsquo;s Autopilot AI?'), (7, 'Automated vs Autonomous'),
    (8, 'Core Concepts of AI (1 of 2)'), (9, 'Core Concepts of AI (2 of 2)'), (10, 'How Artificial Intelligence Works'),
    (11, 'Practical 1: AI or Not AI?'), (12, 'Part 2: Machine Learning'), (13, 'What Is Machine Learning?'),
    (14, 'Traditional Programming vs Machine Learning'), (15, 'Why Do We Need Machine Learning? (1 of 2)'),
    (16, 'Why Do We Need Machine Learning? (2 of 2)'), (17, 'What Makes a Machine &ldquo;Learn&rdquo;?'),
    (18, 'The Machine Learning Workflow'), (19, 'Why Data Is the Foundation'), (20, 'Types of Machine Learning'),
    (21, 'Supervised Learning: What It Is'), (22, 'Supervised Learning: How the Model Learns'),
    (23, 'Two Kinds of Supervised Learning'), (24, 'Supervised Learning Examples'),
    (25, 'Unsupervised Learning: What It Is'), (26, 'Unsupervised Learning'),
    (27, 'Reinforcement Learning: Trial and Error'), (28, 'Reinforcement Learning: How the Loop Works'),
    (29, 'Semi-Supervised Learning'), (30, 'Practical 2: Which Type of Learning Is It?'),
    (31, 'Where Machine Learning Is Used'), (32, 'Benefits and Challenges of Machine Learning'),
    (33, 'Part 3: Deep Learning'), (34, 'What Is Deep Learning?'), (35, 'How a Network Decides: Dog or Cat?'),
    (36, 'Two Kinds of Deep Learning Model'), (37, 'Discriminative Models: Telling Things Apart'),
    (38, 'Generative Models: Creating Something New'), (39, 'Generative vs Discriminative: Side by Side'),
    (40, 'Practical 3: Stand Up for Generative'), (41, 'Part 4: Generative AI'), (42, 'What Is Generative AI?'),
    (43, 'How Generative AI Creates: Predicting What Comes Next'), (44, 'The Power of Generative AI: Transformers'),
    (45, 'Why Transformers Were a Breakthrough: Attention'), (46, 'Inside a Transformer: Encoder and Decoder'),
    (47, 'Advantages and Disadvantages of Transformers'), (48, 'Practical 4: Be the Transformer'),
    (49, 'Part 5: Hallucinations'), (50, 'What Are AI Hallucinations?'), (51, 'Why Do Hallucinations Happen?'),
    (52, 'How to Reduce Hallucinations'), (53, 'Practical 5: Hallucination Hunt'),
    (54, 'Using Generative AI Responsibly'), (55, 'Exit Quiz'),
]
B += ga.guides(GA, K)
B.append(takeaways('ga-take', ga, 56, [
    'AI learns patterns from examples instead of following fixed rules.',
    'Data and labels shape everything a model learns. Good labelling makes good AI.',
    'Generative AI creates new content by predicting what comes next, powered by transformers.',
    'Fluent is not the same as true. Always check what AI produces.',
], 'Next module', 'Introduction to Prompt Engineering: how to ask generative AI for exactly what you need.'))

K = 'Prompt Engineering'
B.append(section('pe-sec', 'Introduction to Prompt Engineering', 'Session 4',
                 'Basic level: how to ask generative AI for exactly what you need', 'chat', 'chat', notes=pe.notes(1)))
PE1 = [
    (2, 'Overview'), (3, 'Part 1: What Is Prompt Engineering?'), (4, 'What Is Prompt Engineering?'),
    (5, 'Why Prompt Engineering Matters'), (6, 'Basics of Prompting'), (7, 'A Vague Prompt vs an Engineered Prompt'),
    (8, 'The Four Elements of a Prompt'), (9, 'The Elements in a Real Prompt'), (10, 'Adding Context, and When You Need It'),
    (11, 'Practical 1: Spot the Elements'), (12, 'Part 2: General Tips for Designing Prompts'),
    (13, 'Tip 1: Start Simple, Then Improve'), (14, 'Tip 2: Write a Clear Instruction'), (15, 'Tip 3: Be Specific'),
    (16, 'Tip 4: Avoid Imprecise Wording'), (17, 'Tip 5: Say What to Do, Not What Not to Do'),
]
B += pe.guides(PE1, K)

FORMULA = [('user', 'Role', 'Who should the AI act as?'), ('target', 'Task', 'What exactly should it do?'),
           ('globe', 'Context', 'Who is it for, and why?'), ('list', 'Format', 'What shape should the answer take?'),
           ('shield', 'Limits', 'Length, tone, and what to do if unsure.')]
B.append(content('pe-formula', 'Putting It Together: A Simple Prompt Formula', K, f'''
{icards(FORMULA, cols=5, extra='compact')}
  <div class="compare2" style="margin-top:16px">
    <div class="cmp-col"><div class="cmp-head">{icon("code")}<span>Template</span></div>
      <pre class="code">Act as [role].
[Task] for [audience / purpose].
Use [format].
[Length, tone, other limits].
If you are not sure, say so.</pre></div>
    <div class="cmp-vs">{icon("arrow", 22)}</div>
    <div class="cmp-col accent"><div class="cmp-head">{icon("pen")}<span>Filled In</span></div>
      <p class="code-p">Act as a customer service trainer. Write 5 polite replies to a customer complaining about a late delivery, for new staff at an online shop in Kumasi. Use a numbered list. Keep each reply under 40 words and offer a solution in every reply.</p></div>
  </div>''', eyebrow='Part 2', notes=pe.notes(18)))
B += pe.guides([(19, 'Practical 2: Fix the Bad Prompt'), (20, 'Part 3: Examples of Prompts'),
                (21, 'Example 1: Text Summarisation'), (22, 'Summarising Further: One Sentence')], K)
B.append(content('pe-extract', 'Example 2: Information Extraction', K, f'''
  <div class="split-img" style="grid-template-columns:1fr 1.5fr;align-items:start">
    <div>
      <p class="lede">Language models are trained to <b>generate</b> text, but they are also very good at other language tasks, such as <b>pulling specific information</b> out of a paragraph.</p>
      <p class="lede">Useful for finding names, dates, amounts, places or products in long documents.</p>
      <p class="img-cap" style="text-align:left">Source of the paragraph: Nature, 2023 (nature.com/articles/d41586-023-00288-7)</p>
    </div>
    <div>
      <div class="prompt-box"><div class="pb-label">Prompt</div>
        <p>Author-contribution statements and acknowledgements in research papers should state clearly and specifically whether, and to what extent, the authors used AI technologies such as ChatGPT in the preparation of their manuscript and analysis. They should also indicate which LLMs were used. &hellip;</p>
        <p class="pb-ask">Mention the large language model-based product mentioned in the paragraph above:</p></div>
      <div class="prompt-box out"><div class="pb-label">Output</div>
        <p>The large language model-based product mentioned in the paragraph above is ChatGPT.</p></div>
    </div>
  </div>''', eyebrow='Part 3', notes=pe.notes(23)))
PE2 = [
    (24, 'Example 3: Question Answering'), (25, 'Example 4: Text Classification'), (26, 'Classification with an Example'),
    (27, 'Spot the Problem'), (28, 'Example 5: Conversation and Role Prompting'), (29, 'Same Question, Different Audience'),
    (30, 'Example 6: Code Generation'), (31, 'Example 7: Reasoning'), (32, 'Practical 3: Prompt Stations'),
    (33, 'Part 4: Prompt Engineering Techniques'), (34, 'A Map of Prompt Engineering Techniques'),
    (35, 'Zero-Shot Prompting'), (36, 'Few-Shot Prompting'), (37, 'Chain-of-Thought (CoT) Prompting'),
    (38, 'Meta Prompting and Role Instructions'), (39, 'Self-Consistency'), (40, 'Generate Knowledge Prompting'),
    (41, 'Prompt Chaining'), (42, 'Tree of Thoughts'), (43, 'Retrieval Augmented Generation (RAG)'),
    (44, 'Letting the Model Use Tools and Code'), (45, 'Automatic Prompt Engineer and Active-Prompt'),
    (46, 'Directional Stimulus and Graph Prompting'), (47, 'ReAct and Reflexion'), (48, 'Multimodal Chain-of-Thought'),
    (49, 'Cheat Sheet: Which Technique When?'), (50, 'Practical 4: Technique Challenge'),
    (51, 'Part 5: Practical Applications'), (52, 'Students: Learning with AI'), (53, 'Students: Homework Help, Step by Step'),
    (54, 'Project Managers: Reports, Decisions and Meetings'), (55, 'Project Managers: Automating a Weekly Report'),
    (56, 'Accountants: Categorising Expenses'), (57, 'Researchers: Literature Reviews'),
    (58, 'Data Labelers: Prompting in Your Own Work'), (59, 'Practical 5: Build a Prompt for Your Own Work'),
    (60, 'Prompting Responsibly'), (61, 'Exit Quiz'),
]
B += pe.guides(PE2, K)
B.append(takeaways('pe-take', pe, 62, [
    'A prompt is built from instruction, context, input data and output indicator.',
    'Be specific: role, task, context, format and limits. Then test and improve.',
    'Pick the technique for the problem: examples, step by step, chaining or sources.',
    'You are responsible for what AI produces. Verify it and protect private data.',
], 'Keep practising', 'Start a personal prompt library: save every prompt that works well, and improve it each time you use it.'))

# ---------------- wrap-up ----------------
B.append(content('d4-recap', 'Day 4 Recap', 'Wrap-Up', icards([
    ('layers', 'Interior Segmentation', '42 classes, distant objects first, and no gaps between polygons'),
    ('spark', 'Generative AI', 'How AI, ML and deep learning connect, how transformers predict, and why AI hallucinates'),
    ('chat', 'Prompt Engineering', 'The four elements, the role-task-context-format-limits formula, and core techniques'),
]) + '\n' + note('Your labels train the models; your prompts direct them. Today you saw both sides.')))
B.append(content('d4-ahead', 'Looking Ahead: Day 5', 'Wrap-Up', pipe([
    ('Vibe Coding', 'Build websites by describing them in plain English'),
    ('Three projects', 'A portfolio, an expense tracker and a photo album'),
    ('Your own app', 'Plan and build something you choose'),
]) + '\n' + note('Tomorrow your prompting skills turn into working web apps.', 'trend')))
B.append(section('d4-end', 'Thank You', 'End of Day 4',
                 'Questions? Let&rsquo;s discuss before we close for today.<br>See you tomorrow for Day 5: Vibe Coding.',
                 'star', 'check', data_title='Thank You'))

write_deck('Day4-Labeling.html', 'Day 4: Data Labelling Training for AI | Kenya ITC × datamaker', A, other=len(B))
write_deck('Day4-GenAI.html', 'Day 4: Generative AI & Prompt Engineering | Kenya ITC × datamaker', B, num_offset=len(A))
