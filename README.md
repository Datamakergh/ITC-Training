# Data Labelling Training for AI: Kenya ITC 2026 (5 Days)

HTML slide decks for the Kenya ITC training, built from the PowerPoint guides in
`OneDrive / 2026 TRAINING FILES / TRAINING GUIDELINES - UPDATED / KENYA ITC / GUIDES`.
Same format as the HQ Vietnam IAC package: open in a browser, nothing to install.

## What is in here

| File | Day | Source PowerPoint | Slides |
|---|---|---|---|
| `Day1.html` | 1 | Synapse Dashboard, Bounding Box, Pen tool, CCTV Bounding Box project | 94 |
| `Day2.html` | 2 | `DAY 2/DAY 2 TRAINING MATERIAL.pptx` | 71 |
| `Day3.html` | 3 | `DAY 3/DAY 3 TRAINING MATERIAL.pptx` | 69 |
| `Day4.html` | 4 | `DAY 4/Generative AI & Prompt Engineering[04112026].pptx` | 62 |
| `Day5.html` | 5 | `DAY 5/AI-Essentials Vibe Coding[04112026].pptx` | 19 |
| `assets/` | | Slide images, GIFs and videos. **Keep next to the HTML files.** | |
| `tools/` | | The generator that builds the HTML (see Editing) | |

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

Speaker notes come only from the PowerPoint files.

On Days 2 to 5:

- The slide always fills the screen without being stretched: the slide's own background artwork
  covers the whole screen, and the slide content sits on it at its original 16:9 shape. The slide number
  is at the top right. The menu button (☰) at the top left shows links to each day; they hide again
  when you move to another slide, click elsewhere or press `Esc`.
- `Esc` goes back to the home page (or closes the overview). In fullscreen, the first `Esc`
  leaves fullscreen.
- The overview (`O`) shows slide numbers.
- Videos behave as they do in PowerPoint: the first Next (arrow / Space) on a video slide starts
  the video, the next one moves on. Click a video to pause or resume it; its controls appear when
  the mouse is over it. Every video starts muted; Day 2 and Day 3 videos have no sound at all.
  GIFs play on their own.

## Printing

Move the mouse to the bottom right corner to show the **Print** button.
Tick **Include speaker notes** for an instructor copy with a notes page after each slide.
Videos print as a still frame.

## How the slides are made

**Days 2 to 5** show every slide of the source PowerPoint, in order, exactly as designed:
nothing added, nothing removed.

- Every slide is exported by PowerPoint itself, so text, fonts, SmartArt, tables and layout match.
- Slides with a flat-colour background are shown as the original slide image
  (`assets/dayN/slides/sNN.jpg`) on that colour.
- Slides with background artwork (the blue and dark title/section slides) are exported as two layers:
  the background (`assets/dayN/bg/sNN.jpg`), which is cropped to cover any screen, and the content
  with transparency (`assets/dayN/slides/sNN.png`), always shown whole at 16:9. Nothing is redrawn:
  the layers are the same slides with some shapes hidden, and they stack back to the original.
- Each GIF and video is placed on top at its exact PowerPoint position and crop
  (`assets/dayN/media/`), so it animates and plays. Videos are re-encoded to web-size MP4; GIFs are
  the original files.
- To change a slide, change the PowerPoint and rebuild (see below).

**Day 1** (not yet rebuilt) mixes native HTML slides with slide images.

## Editing

The HTML files are build output. Rebuild a day after its PowerPoint changes:

1. Install the fonts the decks use, or PowerPoint substitutes them and text overflows:
   **Pretendard**, **Freesentation**, **Source Sans 3** (static OTF) and **NanumSquare_ac**.
2. Copy the PowerPoint to `~/Library/Containers/com.microsoft.Powerpoint/Data/kenya-export/v2/dN.pptx`
   (PowerPoint can only be scripted on files inside its own folder), then:

```
D=~/Library/Containers/com.microsoft.Powerpoint/Data/kenya-export/v2
python3 tools/split_layers.py $D/dN.pptx $D/dN          # makes dN-bg / dN-fgw / dN-fgb.pptx
tools/export_pdf.sh dN dN-bg dN-fgw dN-fgb              # PowerPoint exports each to PDF
python3 tools/render_layers.py N $D/dN                  # slide images + background/content layers
python3 tools/extract_pptx.py N $D/dN.pptx              # text, notes, GIFs, videos (needs ffmpeg)
python3 tools/dayN.py
```

- `tools/fullslide.py` builds the Day 2 to 5 decks; `tools/split_layers.py`, `export_pdf.sh` and
  `render_layers.py` make the slide images; `tools/extract_pptx.py` reads the PPTX.
- `tools/deck.py` and `tools/day1.py` build Day 1.
- `tools/shell/` holds the stylesheet and presenter script from the HQ package.
- `tools/meta/` holds the text, notes and media positions extracted from each PowerPoint.
- `check_layout.py` checks the native HTML slides of Day 1 for clipped or overlapping content.
- The build refuses to write a deck that contains an em dash (notes are rewritten with commas).

## Hosting

The repo is set up for GitHub Pages (Settings > Pages > Deploy from branch `main`, folder `/`).
`index.html` is the landing page linking every deck; `.nojekyll` makes Pages serve the files as-is.
