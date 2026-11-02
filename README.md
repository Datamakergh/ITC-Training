# Data Labelling Training for AI: Kenya ITC 2026 (5 Days)

HTML slide decks for the Kenya ITC training, built from the PowerPoint guides in
`OneDrive / 2026 TRAINING FILES / TRAINING GUIDELINES - UPDATED / KENYA ITC / GUIDES`.
Same format as the HQ Vietnam IAC package: open in a browser, nothing to install.

## What is in here

| File | Day | Content | Slides |
|---|---|---|---|
| `Day1.html` | 1 | Synapse Dashboard, Bounding Box, Pen tool, CCTV Bounding Box project | 94 |
| `Day2.html` | 2 | Polyline, Traffic Flow project, Polygon, Rail &amp; Catenary project | 108 |
| `Day3.html` | 3 | Semantic Segmentation, 3D &amp; LiDAR, PCD project | 62 |
| `Day3-Photobooth.html` | 3 | Photobooth Image Labelling project, Day 3 wrap-up | 64 |
| `Day4-Labeling.html` | 4 | Interior Segmentation, Photobooth project | 75 |
| `Day4-GenAI.html` | 4 | Introduction to Generative AI, Prompt Engineering, Day 4 wrap-up | 121 |
| `Day5.html` | 5 | Vibe Coding, program close | 45 |
| `assets/` | | Slide images and short videos. **Keep next to the HTML files.** | |
| `tools/` | | The generator that builds the HTML (see Editing) | |

Day 3 and Day 4 are each two files numbered as one sequence (for example Day 3 runs 1 to 126
across both files), the same way HQ split their Day 1.

Day 1 does not use the `MICROSOFT OFFICE SUITE FILES` folder.

## Presenting

Open any `DayN.html` in Chrome.

| Key | Does |
|---|---|
| Arrows / Space | Previous / next slide |
| `F` | Fullscreen |
| `N` | Speaker notes (hidden from the projector by default) |
| `O` | Slide overview grid; click a slide to jump to it |
| `Home` / `End` | First / last slide |

The URL keeps the slide number (`Day2.html#40`), so a refresh stays on the same slide.

Speaker notes come only from the PowerPoint files. The Generative AI, Prompt Engineering
and Vibe Coding decks have full notes; the labelling guides have almost none.

## Printing

Move the mouse to the bottom right corner to show the **Print** button.
Tick **Include speaker notes** for an instructor copy with a notes page after each slide.
Videos print as a still frame.

## How the slides are made

- **Native slides** (title, agenda, section dividers, concept and rules slides, practice
  screens, recap) are written in HTML and can be edited as text.
- **Guide slides** are the original PowerPoint slides shown as images: step-by-step
  screenshots, examples, and the already-designed Generative AI, Prompt Engineering and
  Vibe Coding decks. To change one of these, change the PowerPoint and re-export it.
- Day 5 uses the updated Vibe Coding deck (`[02112026]`). Its slides have no em dashes;
  the few in its speaker notes are rewritten at build time.

## Editing

The HTML files are build output. Change the Python in `tools/` and rebuild:

```
cd tools
python3 day1.py            # or day2.py ... day5.py
python3 check_layout.py ../Day*.html
```

- `tools/deck.py` has the shared styles and slide helpers.
- `tools/dayN.py` lists the slides for each day; `tools/photobooth.py` is shared by Days 3 and 4.
- `tools/shell/` holds the stylesheet and presenter script from the HQ package.
- `tools/meta/` holds the text and notes extracted from each PowerPoint.
- `check_layout.py` opens each deck in headless Chrome at 1280x720 and reports any text
  or element that is clipped, outside the slide, or overlapping something else.
- The build refuses to write a deck that contains an em dash.

Slide numbers are filled in automatically. For split days, the second file's numbering
offset is computed from the first file's slide count, so adding slides needs no manual fix.

### Re-exporting slide images from PowerPoint

Slide images in `assets/dayN/<deck>/sNN.jpg` were exported from PowerPoint as PDF and
rendered at 1600px. Install the **Pretendard** font before exporting; without it
PowerPoint substitutes Calibri and text overflows its boxes.

## Hosting

The repo is set up for GitHub Pages (Settings > Pages > Deploy from branch `main`, folder `/`).
`index.html` is the landing page linking every deck; `.nojekyll` makes Pages serve the files as-is.
