---
name: pdf-to-pptx
description: Convert a compiled PDF slide deck (typically a Beamer deck's `presentations/<slug>/main.pdf`) into a PowerPoint `.pptx`, one full-bleed image per page, with the slide size matched to the PDF's aspect ratio. Use when the researcher wants "the slides as PowerPoint", "a pptx version of the deck", "something I can open in PowerPoint/Google Slides", or has to hand a deck to someone who needs a .pptx -- not for drafting or compiling the deck itself (that's `latex-presentation` / `latex-compile`).
---

# pdf-to-pptx

Thin wrapper over poppler (`pdftoppm`, via `pdf2image`) + `python-pptx`.
Every page of the PDF is rendered to a PNG and placed full-bleed on its own
blank slide. The slide size follows the PDF's first-page aspect ratio at a
fixed 7.5in height, so a default 4:3 Beamer deck lands on 10in x 7.5in and
an `aspectratio=169` deck on 13.333in x 7.5in -- never a hardcoded 16:9.

**The result is pictures of slides, not editable slides.** Text can't be
selected or edited in PowerPoint, and Beamer overlays (`\pause`, `<2->`)
arrive as the separate pages they already are in the PDF. Say this plainly
to the researcher the first time you use this skill together: it is for
presenting or sharing on a PowerPoint machine, not for editing the deck
there. Edits go into `main.tex`, then recompile and reconvert.

## Invocation

```bash
uv run .claude/skills/pdf-to-pptx/pdf_to_pptx.py presentations/<slug>/main.pdf
```

- `output_pptx` (optional second positional) -- defaults to the input path
  with a `.pptx` suffix, i.e. `presentations/<slug>/main.pptx`, next to the
  PDF. Use that default unless the researcher asks for somewhere else.
- `--width-px N` (default `3840`) -- render each page this many pixels
  wide; the DPI is derived from the PDF page width. A fixed DPI is a trap
  with Beamer: a 16:9 page is only 6.3in wide, so 200 DPI gives a soft
  1260px slide. 3840px stays sharp on 4K screens and projectors.
- `--dpi N` -- fixed render DPI instead; overrides `--width-px`.
- `--keep-images` -- keep the rendered PNGs; their directory is reported
  as `"images_dir"`. Only for debugging.

If the PDF doesn't exist yet or is older than `main.tex`, compile first
through `latex-compile` (see `latex-presentation`'s "Compiling" section) --
never convert a stale PDF without saying so.

## Output contract

Always exactly one JSON object on stdout, never a traceback:

```json
{
  "status": "ok" | "error",
  "output": "presentations/<slug>/main.pptx" | null,
  "pages": 12,
  "slide_size_in": [13.333, 7.5] | null,
  "dpi": 610,
  "images_dir": null,
  "message": "converted 12 page(s) to presentations/<slug>/main.pptx"
}
```

Exit code `0` for `"ok"`, `1` for `"error"`. On `"ok"`, tell the
researcher the output path and page count, and that they should open it
once in PowerPoint or LibreOffice Impress to confirm it looks right --
visual fidelity isn't checked automatically.

## Ask First

- **Missing poppler** -- `"message"` names `pdftoppm`/`pdfinfo` and points
  at `sudo apt install poppler-utils` (`SETUP.md` §2). Relay it and ask
  before running any `sudo` install; never guess another install route.
- **Existing `.pptx` at the output path** -- the script overwrites it
  silently. If one is already there and it's not simply the previous
  output of this skill for the same deck, confirm before re-running.
- Any other `"error"` (missing, unreadable, or zero-page PDF): relay
  `"message"` as-is and ask how to proceed.

## Notes

- `presentations/**/*.pptx` is gitignored, like the PDF it's built from --
  the `.tex` is the source of truth, and the `.pptx` is rebuilt from it.
- Out of scope: selectable/editable text, and carrying Beamer speaker notes
  into PowerPoint's notes field.
