# Data Labelling Training for AI: Kenya ITC 2026 (5 Days)

HTML slide decks for the Kenya ITC training, built from the PowerPoint guides in
`OneDrive / 2026 TRAINING FILES / TRAINING GUIDELINES - UPDATED / KENYA ITC / GUIDES`.
Same format as the HQ Vietnam IAC package: open in a browser, nothing to install.

## What is in here

| File | Day | Source PowerPoint | Slides |
|---|---|---|---|
| `Day1.html` | 1 | `DAY 1/DATA ANNOTATION/Labeling Training Introduction Day 1 [13112026].pptx`, then `DAY 1/DATA ANNOTATION/DAY 1 TRAINING MATERIAL.pptx` | 107 (74 + 33; slide 36 of part 1 repeats slide 37 and is left out) |
| `Day2.html` | 2 | `DAY 2/DAY 2 TRAINING MATERIAL.pptx` | 62 |
| `Day3.html` | 3 | `DAY 3/DAY 3 TRAINING MATERIAL.pptx` | 63 |
| `Day4.html` | 4 | `DAY 4/Generative AI & Prompt Engineering[11112026].pptx` | 62 |
| `Day5.html` | 5 | `DAY 5/AI-Essentials Vibe Coding[14112026].pptx` | 19 |
| `assets/` | | Slide images, GIFs and videos. **Keep next to the HTML files.** | |
| `tools/` | | The generator that builds the HTML (see Editing) | |

Day 1 joins its two PowerPoints into one deck; slide numbers continue from the first into the second.

### Training of Trainers (ToT)

A separate three-day programme with its own home page, `ToT.html` (linked once from `index.html`).
The menu in a ToT deck lists only the ToT days, and `Esc` returns to `ToT.html`.
Sources (revamped 2026-11-16) are in `~/Documents/`, same file names.

| File | Day | Source PowerPoint | Slides |
|---|---|---|---|
| `ToT-Day1.html` | ToT 1 | `TOT Program Introduction Day 1.pptx` | 86 |
| `ToT-Day2.html` | ToT 2 | `ToTDay 2 AnnotationQualityProject Management_and_Operational_Control.pptx` | 27 |
| `ToT-Day3.html` | ToT 3 | `ToT Day 3 Participant Manual.pptx` | 32 |

## Presenting

Open any `DayN.html` in Chrome (or Safari / Chrome on a phone or tablet).

| Key | Does |
|---|---|
| Arrows / Space | Previous / next slide |
| `F` | Fullscreen |
| `N` | Speaker notes (hidden from the projector by default) |
| `M` | Mute / unmute the videos |
| `O` | Slide overview grid; click a slide to jump to it |
| `Home` / `End` | First / last slide |

On a phone or tablet: **tap the left third** of the screen for the previous slide, **tap anywhere else**
for the next one. Swiping left / right also works.

The URL keeps the slide number (`Day2.html#40`), so a refresh stays on the same slide.

Speaker notes come only from the PowerPoint files.

On every day:

- Slides behave like a PowerPoint slideshow: the whole slide is scaled to fit any screen at its
  16:9 shape, never stretched or cropped, with black bars where the screen is a different shape.
  GIFs and videos scale with the slide and stay exactly in place.
- Each slide cross-fades into the next; the slides around the current one are loaded ahead, so
  there is never a blank or black frame between slides.
- The menu button (☰, top left) and the slide number (top right) appear when the mouse moves or the
  screen is tapped, and fade away after a moment so nothing covers the slide. The menu shows a Home
  link (the home page, or `ToT.html` in a ToT deck) and links to each day; it hides again when you move to another slide, click elsewhere or press `Esc`.
- `Esc` goes back to the home page (or closes the overview). In fullscreen, the first `Esc`
  leaves fullscreen.
- The overview (`O`) shows slide numbers.
- Videos behave as they do in PowerPoint: the first Next (arrow / Space / tap) on a video slide starts
  the video, the next one moves on. Click or tap a video to pause it, and again to play it.
  Videos play with sound (unless muted in the PowerPoint); `M` mutes or unmutes them all.
  Day 2 and Day 3 videos have no sound, except Day 3 slides 46 and 49 (`KEEP_AUDIO` in
  `tools/extract_pptx.py`).
  GIFs play on their own.

## Printing

Move the mouse to the bottom right corner to show the **Print** button.
Tick **Include speaker notes** for an instructor copy with a notes page after each slide.
Videos print as a still frame.

## How the slides are made

**Every day** shows every slide of its source PowerPoint(s), in order, exactly as designed:
nothing added, nothing removed.

- Every slide is exported by PowerPoint itself, so text, fonts, SmartArt, tables and layout match.
  Each slide is one image (`assets/dayN/slides/sNN.jpg`, 2400 px wide).
- Each GIF and video is placed on top at its exact PowerPoint position and crop
  (`assets/dayN/media/`), so it animates and plays. Videos are re-encoded to web-size MP4; GIFs are
  the original files.
- To change a slide, change the PowerPoint and rebuild (see below).

**Day 1** is built from two PowerPoints, shown one after the other.

## Editing

The HTML files are build output. Rebuild a day after its PowerPoint changes:

1. Install the fonts the decks use, or PowerPoint substitutes them and text overflows:
   **Pretendard**, **Freesentation**, **Source Sans 3** (static OTF) and **NanumSquare_ac**.
2. Copy the PowerPoint to `~/Library/Containers/com.microsoft.Powerpoint/Data/kenya-export/v2/dN.pptx`
   (PowerPoint can only be scripted on files inside its own folder), then:

```
D=~/Library/Containers/com.microsoft.Powerpoint/Data/kenya-export/v2
tools/export_pdf.sh dN                                  # PowerPoint exports the deck to PDF
python3 tools/render_layers.py N $D/dN                  # slide images
python3 tools/extract_pptx.py N $D/dN.pptx              # text, notes, GIFs, videos (needs ffmpeg)
python3 tools/dayN.py
```

Day 1 is two PowerPoints (`d1a` = Labeling Training Introduction Day 1 [13112026], `d1b` = Day 1 Training Material).
Before exporting `d1a`, remove its broken layout logo (a picture with no image, which PowerPoint draws as
"The picture can't be displayed" on slide 41): `python3 tools/drop_broken_pics.py $D/d1a.pptx`.
Also remove the section numbers at the top left of its SYNAPSE slides (source slides 43-57):
`python3 tools/drop_shapes.py $D/d1a.pptx --slides 43-57 --name "TextBox 24" --text '\d{1,2}'`.
Export each, then number part 2 after part 1 (75 slides at the time of writing):

```
python3 tools/render_layers.py 1 $D/d1a
python3 tools/render_layers.py 1 $D/d1b --start 76
python3 tools/extract_pptx.py 1 $D/d1a.pptx --part p1
python3 tools/extract_pptx.py 1 $D/d1b.pptx --start 76 --part p2
python3 tools/day1.py
```

ToT decks use a name instead of a day number (`tot1`, `tot2`, `tot3`; assets in `assets/totN/`).
ToT Days 2 and 3 are designed on A4 landscape pages; widen their copies to 16:9 before exporting so they fill
the screen like the other decks (backgrounds stretch, content stays centred, logos stay in the corners):
`python3 tools/widen_169.py $D/tot2.pptx` (and `tot3`).

```
tools/export_pdf.sh tot1
python3 tools/render_layers.py tot1 $D/tot1
python3 tools/extract_pptx.py tot1 $D/tot1.pptx
python3 tools/tot1.py
```

- `tools/fullslide.py` builds every deck; `export_pdf.sh` and `render_layers.py` make the slide images; `tools/extract_pptx.py` reads the PPTX.
- `tools/deck.py` holds shared paths and helpers (and the old native-slide builder, no longer used).
- `tools/shell/` holds the stylesheet and presenter script from the HQ package.
- `tools/meta/` holds the text, notes and media positions extracted from each PowerPoint.
- The build refuses to write a deck that contains an em dash (notes are rewritten with commas).

## Hosting

The repo is set up for GitHub Pages (Settings > Pages > Deploy from branch `main`, folder `/`).
`index.html` is the landing page linking every deck; `.nojekyll` makes Pages serve the files as-is.
