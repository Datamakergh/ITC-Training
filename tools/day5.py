"""Day 5: Vibe Coding.

Source (KENYA ITC/GUIDES/DAY 5): Vibe Coding Build Websites by Describing Them[02112026].pptx -> vibe

The deck is already designed slide-for-slide with full speaker notes, so its slides are
shown as-is (guide slides), with practice screens after each project. The slide text has no em dashes; the ones in the
speaker notes are rewritten by plain_dashes() at build time.
The original title (s1) and thank-you (s40) slides are replaced by this program's own.
"""
from deck import *

vb = Source(5, 'vibe')

S = []
S.append(title_slide(
    'd5-title', 5, 'Vibe Coding: Build Websites<br>by Describing Them', PARTNERS,
    [('code', 'Hands-on with Claude and Notepad'), ('globe', 'Kenya ITC Training 2026')], notes=vb.notes(1)))
S.append(content('d5-journey', 'Where We Are', 'Overview', f'''
  <p class="lede">The last day: you turn everything you know about prompting into working web apps.</p>
{journey(5)}''', eyebrow='Program Overview'))
S.append(vb.guide(2, 'Today&rsquo;s Plan', 'Overview'))

K = 'Getting Started'
S += vb.guides([(3, 'Part 1: Getting Started'), (4, 'What Is Vibe Coding?'), (5, 'Why It Matters'),
                (6, 'Ground Rules for Working With AI'), (7, 'Your AI Tools'), (8, 'Get Set Up')], K)
K = 'Writing Great Prompts'
S += vb.guides([(9, 'Part 2: Writing Great Prompts'), (10, 'What Is a Prompt? The Most Important Skill'),
                (11, 'CLEAR in Action, Step by Step'), (12, 'Bad Prompt vs Good Prompt')], K)
K = 'Project 1: Portfolio'
S += vb.guides([(13, 'Part 3: Your Portfolio Website'), (14, 'A Webpage Is Like a House'), (15, 'What Is the Portfolio?'),
                (16, 'Build It: Your Portfolio'), (17, 'Copy, Save, Open'), (18, 'Style Your Portfolio')], K)
S.append(practice('vb-p1', 'Build Your Portfolio', 'Write your CLEAR prompt, paste it into Claude, and save portfolio.html.',
                  ['CLEAR prompt filled in', 'Saved as .html, not .txt', 'Opens in the browser',
                   'Public email only', 'One change at a time', 'Save every working version'], kicker='Project 1'))
K = 'Make It Better'
S += vb.guides([(19, 'Part 4: Make It Better'), (20, 'The Refine Loop'), (21, 'Speak Human, Not Tech'),
                (22, 'Level Up: Try These Challenges'), (23, 'When the AI Gets It Wrong')], K)
K = 'Project 2: Expense Tracker'
S += vb.guides([(24, 'Part 5: The Expense Tracker'), (25, 'What Is the Expense Tracker App?'),
                (26, 'Build the Expense Tracker'), (27, 'Make It Smarter: Filters, Saving, Chart')], K)
S.append(practice('vb-p2', 'Build the Expense Tracker', 'New chat, new file: expenses.html. One feature at a time.',
                  ['Add 3 expenses', 'Total is correct', 'Delete updates the total',
                   'Empty form handled', 'Data survives a refresh', 'Chart updates'], kicker='Project 2'))
K = 'Project 3: Photo Album'
S += vb.guides([(28, 'Part 6: The Photo Album'), (29, 'What Is the Photo Album App?'),
                (30, 'Build the Gallery and the Lightbox'), (31, 'Upload, Search and Animations')], K)
S.append(practice('vb-p3', 'Build the Photo Album', 'New chat, new file: album.html. Gallery first, then the lightbox.',
                  ['Grid fits every screen', 'Click to enlarge', 'Escape closes the lightbox',
                   'Upload with captions', 'Search by caption', 'Gentle animations'], kicker='Project 3'))
K = 'Your Own App'
S += vb.guides([(32, 'Part 7: Your Own App'), (33, 'The Own Project: Freedom and Responsibility'),
                (34, 'Finding Your Idea'), (35, 'Plan Small: The MVP'), (36, 'The Planning Prompt: Before Any Code'),
                (37, 'When the AI Gets It Wrong: A Reminder')], K)
K = 'Wrap-Up'
S += vb.guides([(38, 'Show and Tell'), (39, 'You Built 3 Projects Today. Keep Going!')], K)

S.append(content('d5-complete', 'Five Days, Complete', 'Program Complete', f'''
  <p class="lede">From your first bounding box to your own web app.</p>
{journey(0)}
{note("Keep practising: label carefully, prompt clearly, and always check what the AI gives you.", "star")}''',
    eyebrow='Program Complete'))
S.append(section('d5-end', 'Thank You', 'End of the Program',
                 'Thank you for five days of hard work.<br>Questions? Let&rsquo;s discuss before we close.',
                 'star', 'check', notes=vb.notes(40), data_title='Thank You'))

write_deck('Day5.html', 'Day 5: Vibe Coding | Kenya ITC × datamaker', S)
