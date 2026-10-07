# Mszalik – Latin–Polish wedding missal

A booklet (A5 pages, printed as folded A4 sheets) for a wedding in the Traditional Latin Mass (1962 rite): introduction texts, the marriage rite, and the Missa pro Sponso et Sponsa (Ordo Missæ) in two parallel columns, Latin and Polish. All content is in Polish/Latin; talk to the user in English.

## How it is built

- **One HTML file = one A5 page.** `1.html … 22.html` are the content pages, all styled by `styles.css` (`@page` size 148×210 mm). `0.html` is an empty template page.
- `htmltopdf.py` uses headless Chrome (Selenium + CDP `Page.printToPDF`) to render each `N.html` to `N.pdf`, then merges them into `missale_ready.pdf`. `save_html_as_pdf(html, pdf)` is the reusable function.
- `pages_alghoritm.py` does the saddle-stitch imposition. It pads the page count to a multiple of 4 (`None` = blank page), puts 2 A5 pages on each A4 side with `mergea5toa4.py`, and writes `sheet_<BR><BL><L><R>.pdf` (one double-sided A4 sheet each). It prints an `index.html` with links to them.
- `megre_cover.py` builds `okladka.pdf` (the cover) from `Barbara.pdf`, using background `#FEFAF2`.
- CI (`.github/workflows/main.yml`): on every push it runs `htmltopdf.py` and `pages_alghoritm.py` and deploys the PDFs plus `index.html` to GitHub Pages (repo `AntonyFFC/mszalik`).
- `*.pdf` is gitignored, so all PDFs are local build output. The old `sheet_*.pdf`, `NNN.pdf`, `None*.pdf` files in the root are stale leftovers from earlier runs.
- The venv is `.venv` (Python 3.14). It has pypdf, selenium, webdriver-manager and watchdog installed. `megre_cover.py` also needs reportlab.

## Live preview workflow (Ctrl+S → Sumatra refresh)

```
.venv\Scripts\python.exe watch_render.py
```

`watch_render.py` watches the repo root with watchdog. When a file named `<digits>.html` is saved, it re-renders only that page's `N.pdf` (1 s debounce, about 15–20 s per render because Chrome starts each time). SumatraPDF auto-reloads open PDFs, so the user keeps `N.pdf` open and sees each save.
- It does **not** react to changes in `styles.css` or the images. After a CSS change, run `python htmltopdf.py` (re-renders everything and rebuilds `missale_ready.pdf`), or re-save the affected pages.
- To render a single page by hand: `python -c "from htmltopdf import save_html_as_pdf; save_html_as_pdf('12.html','12.pdf')"` (run from the repo root, because paths are relative).

## Page conventions (important when editing or moving content)

- **Printed page number = file number + 2.** The two cover pages come first. The number is hard-coded in each file as `<div class="page-number">N+2</div>`. If pages are inserted, removed or renumbered, every later file's number must be updated by hand.
- **Column order depends on page parity**, because Latin is always the column nearer the spine:
  - Odd file number (odd printed page, a right-hand page): `.latin` first, then `.polish`.
  - Even file number (even printed page, a left-hand page): `.polish-r` first, then `.latin-r`.
  - Header lines (`.naglowek-liturgiczny`) are mirrored too: on odd pages the reference comes first and the title last; on even pages the title comes first and the reference last.
  - **When text moves to a page of the other parity, swap the column order and classes.**
- **Checking the fit:** `python check_fit.py [first [last]]` renders the pages in one Chrome session and prints the PDF page count and the approximate free space for each page. "free" is pessimistic by about 5–7 mm: about −3 mm can still fit, and `pages=1` is what decides it. The only judge is `pages`.
- **Reflow procedure after adding or moving content:** edit the page, then run `check_fit.py` from that page onward. If a page overflows, move its last block(s) to the top of the next file, swapping `.latin`/`.polish` ↔ `.polish-r`/`.latin-r` order if the parity changes. Repeat until every page shows `pages=1`.
- **Blank 2nd page trap:** text can end above the bottom edge and Chrome still emits an empty second page. The cause is the last `.parallel-container`'s 25 px `margin-bottom` plus the body's 20 px padding. Fix it with `style="margin-bottom: 0;"` on the page's last container before moving any content.
- **Each page must fit on one A5 page.** Overflow makes Chrome output a 2-page PDF, and the imposition uses only the first page. Check that `N.pdf` has 1 page after a change. Text that doesn't fit is moved by hand to the start of the next file, and that may cascade through later pages.
- Spacing is tuned per element with inline `style="margin-top:-15px"` and similar. Existing negative margins are intentional.

## Markup vocabulary (styles.css)

| Element / class | Meaning |
|---|---|
| `h1` | Red uppercase section title (e.g. "Ordo Missæ") |
| `h3` / `h4` | Section / sub-section headings (black, centred) |
| `.parallel-container` > `.latin` + `.polish` (or `.polish-r` + `.latin-r`) | Two-column Latin/Polish text |
| `.red-info` | Rubric: red instructions, not read aloud |
| `.naglowek-liturgiczny` | Flex header line: bold title + scripture reference (2.8 mm span) |
| `<b style="color: #ee1d23;">&emsp;S. </b>` / `M.` (Latin), `K.` / `W.` (Polish) | Dialogue speaker labels: priest / server (Latin), priest / faithful (Polish) |
| `.dialog` | One-line Q&A row (vows / scrutinium), label left, answer right-aligned |
| `<img class="posture-sep" src="...">` | Posture symbols: `klk.png` kneel, `kon_klk.png` rise from kneeling, `wst.png` stand, `sdn.png` sit |
| `<span class="cross"><img src="img.png"></span>` | Small red cross: the celebrant makes the sign of the cross here |
| `.lettrine` | Large red initial letter |

Paragraphs start with `&emsp;` for the indent. The fonts are Century Schoolbook, with red `#ee1d23`.

Known quirks (left as they are, because fixing them would shift the layout everywhere): in `styles.css`, `h3` is missing `;` after `color: black`, so its `margin-top: 17mm` is ignored.

## Page map (file → printed page → content)

1→3 How to use the missal · 2→4 Marriage (intro) · 3→5 Graces of the sacrament, rite, Veni Creator · 4→6 Ephesians / Matthew readings · 5→7 Scrutinium · 6→8 Exchange of consent, rings · 7→9 Confirmation of the marriage, Ps 127 · 8→10 Ps 127 end + closing prayers of the rite · 9→11 Ordo Missæ: Introit, Kyrie, Gloria · 10→12 Collect · 11→13 Epistle, Gradual · 12→14 Gradual/Alleluia, Gospel · 13→15 Offertory, Secret · 14→16 Preface, Sanctus, Canon · 15→17 Consecration · 16→18 Pater noster, nuptial blessing · 17→19 Nuptial blessing (Deus qui potestate…) · 18→20 Fraction, prayers before Communion · 19→21 Communion · 20→22 Postcommunion · 21→23 Blessing, Last Gospel · 22→24 Last Gospel (end)

## History

- Mar–Apr 2026: initial build pipeline, CI, imposition, cover, and the bulk of the texts.
- Jul 29: Latin translations added to the readings.
- Aug 13: corrections, movement and margin fixes.
- Aug 14: posture separators, `watch_render.py`, the instructions page (1.html), and page re-flow.
- Aug 17: quiet (grey) parts marked with `.quiet-part`. Reverted on Oct 7 (commit 7a11084), so these classes no longer exist.
