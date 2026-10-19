# /// script
# requires-python = ">=3.12"
# dependencies = ["pdf2image", "python-pptx"]
# ///
"""pdf_to_pptx.py -- image-based PDF -> PPTX converter for the `pdf-to-pptx`
Claude Code skill.

Renders every page of a PDF (typically a compiled Beamer deck,
`presentations/<slug>/main.pdf`) to a PNG via poppler (`pdftoppm`, through
`pdf2image`) and places each one full-bleed on its own blank slide. The
slide size follows the source PDF's first-page aspect ratio (from
`pdfinfo`'s page size in points) -- never a hardcoded 16:9 -- using a fixed
7.5in height, so 4:3 and 16:9 sources land on PowerPoint's own standard
10in x 7.5in and 13.333in x 7.5in sizes.

Output is intentionally image-only: no selectable/editable text, no speaker
notes.

Always prints a single JSON object to stdout:
    {"status": "ok"|"error", "output": str|null, "pages": int,
     "slide_size_in": [w, h]|null, "dpi": int, "images_dir": str|null,
     "message": str}

Exit codes mirror latex_compile.py's status-driven convention:
  0  "status": "ok"
  1  "status": "error" (missing input, missing poppler, zero-page or
     unreadable PDF -- always reported, never a raw traceback)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches

REQUIRED_TOOLS = ("pdftoppm", "pdfinfo")
SLIDE_HEIGHT_IN = 7.5
BLANK_LAYOUT_INDEX = 6
# Beamer pages are tiny (a 16:9 deck is 6.3in wide), so a fixed DPI gives
# soft slides: 200 DPI is only 1260px. Render to a pixel width instead.
DEFAULT_WIDTH_PX = 3840


def report(status: str, message: str, **fields: Any) -> int:
    result = {
        "status": status,
        "output": None,
        "pages": 0,
        "slide_size_in": None,
        "dpi": None,
        "images_dir": None,
        "message": message,
    }
    result.update(fields)
    print(json.dumps(result, indent=2))
    return 0 if status == "ok" else 1


def page_ratio(info: dict[str, Any], first_image: str) -> float:
    """Width/height of the first page, from pdfinfo's exact point size when
    available -- the rendered PNG's pixel size drifts with DPI rounding."""
    try:
        width_pt, _, height_pt = info["Page size"].split()[:3]
        return float(width_pt) / float(height_pt)
    except (KeyError, ValueError):
        with Image.open(first_image) as first:
            return first.size[0] / first.size[1]


def dpi_for_width(info: dict[str, Any], width_px: int) -> int:
    """DPI that renders the first page at `width_px` pixels wide."""
    width_pt = float(info["Page size"].split()[0])
    return max(1, round(width_px / (width_pt / 72)))


def convert(
    pdf: Path, out: Path, dpi: int, images_dir: Path, info: dict[str, Any]
) -> tuple[int, tuple[float, float]]:
    # paths_only + output_folder streams pages to disk instead of holding
    # every rendered page in memory at once.
    image_paths = convert_from_path(
        pdf, dpi=dpi, output_folder=images_dir, fmt="png", paths_only=True
    )
    if not image_paths:
        raise ValueError("PDF has zero pages")

    ratio = page_ratio(info, image_paths[0])

    prs = Presentation()
    prs.slide_width = Emu(round(Inches(SLIDE_HEIGHT_IN) * ratio))
    prs.slide_height = Inches(SLIDE_HEIGHT_IN)
    blank = prs.slide_layouts[BLANK_LAYOUT_INDEX]

    for image_path in image_paths:
        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(
            image_path, 0, 0, width=prs.slide_width, height=prs.slide_height
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return len(image_paths), (
        round(prs.slide_width / Inches(1), 3),
        round(prs.slide_height / Inches(1), 3),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument(
        "output_pptx",
        type=Path,
        nargs="?",
        help="defaults to the input path with a .pptx suffix",
    )
    parser.add_argument(
        "--width-px",
        type=int,
        default=DEFAULT_WIDTH_PX,
        help=f"render each page this many pixels wide (default {DEFAULT_WIDTH_PX})",
    )
    parser.add_argument("--dpi", type=int, help="fixed render DPI; overrides --width-px")
    parser.add_argument(
        "--keep-images",
        action="store_true",
        help="keep the rendered PNGs (path reported in the JSON) instead of deleting them",
    )
    args = parser.parse_args()

    pdf: Path = args.input_pdf
    out: Path = args.output_pptx or pdf.with_suffix(".pptx")

    if args.dpi is not None and args.dpi <= 0:
        return report("error", f"--dpi must be positive, got {args.dpi}", dpi=args.dpi)
    if args.width_px <= 0:
        return report("error", f"--width-px must be positive, got {args.width_px}")

    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    if missing:
        return report(
            "error",
            f"{', '.join(missing)} not found on PATH -- install poppler-utils "
            "(sudo apt install poppler-utils; see SETUP.md section 2)",
            dpi=args.dpi,
        )

    if not pdf.is_file():
        return report("error", f"input PDF not found: {pdf}", dpi=args.dpi)

    try:
        info = pdfinfo_from_path(pdf)
        if int(info.get("Pages", 0)) == 0:
            return report("error", f"PDF has zero pages: {pdf}", dpi=args.dpi)
    except (PDFPageCountError, PDFInfoNotInstalledError) as exc:
        return report("error", f"could not read PDF {pdf}: {exc}".strip(), dpi=args.dpi)

    try:
        dpi = args.dpi or dpi_for_width(info, args.width_px)
    except (KeyError, ValueError, IndexError):
        dpi = 600  # page size unknown; high enough for a Beamer-sized page

    images_dir = Path(tempfile.mkdtemp(prefix="pdf_to_pptx_"))
    try:
        pages, slide_size = convert(pdf, out, dpi, images_dir, info)
    except Exception as exc:  # reported as JSON, never a traceback
        shutil.rmtree(images_dir, ignore_errors=True)
        return report("error", f"conversion failed: {exc}", dpi=dpi)

    if not args.keep_images:
        shutil.rmtree(images_dir, ignore_errors=True)

    return report(
        "ok",
        f"converted {pages} page(s) to {out}",
        output=str(out),
        pages=pages,
        slide_size_in=list(slide_size),
        dpi=dpi,
        images_dir=str(images_dir) if args.keep_images else None,
    )


if __name__ == "__main__":
    sys.exit(main())
