#!/usr/bin/env python3
"""Render a print-ready HTML page to PDF with headless Chromium, optionally with PNG page previews.

Usage: python3 scripts/make_pdf.py input.html output.pdf [--format Letter|A4] [--png-preview DIR]

Needs Python Playwright and an already-installed Chromium (this script never downloads one).
Set MYELINATE_CHROMIUM (or CHROMIUM_PATH) to use a specific browser executable.
Paper size: --format if given, else the page's CSS @page size, else Letter.
If the page's CSS has no @page margin boxes (@bottom-*), a footer with the
document title and "Page X of Y" is added.
"""
import argparse
import html
import os
import shutil
import subprocess
import sys
from pathlib import Path

HAS_MARGIN_BOXES = """() => {
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const r of rules) if (r.type === 6 && /@(bottom|top)-/.test(r.cssText)) return true;
  }
  return false;
}"""


def footer_template(title):
    style = "font-family: Inter, Arial, sans-serif; font-size: 8pt; color: #16313b; width: 100%; padding: 0 0.75in;"
    return (f'<div style="{style} display: flex; justify-content: space-between;">'
            f'<span>{html.escape(title)}</span>'
            '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


def render_pdf(src, out, fmt):
    from playwright.sync_api import sync_playwright
    exe = os.environ.get('MYELINATE_CHROMIUM') or os.environ.get('CHROMIUM_PATH') or None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe)
        try:
            page = browser.new_page()
            page.emulate_media(media='print')
            page.goto(src.resolve().as_uri(), wait_until='networkidle', timeout=30000)
            page.evaluate('document.fonts.ready.then(() => true)')
            css_footer = page.evaluate(HAS_MARGIN_BOXES)
            title = page.title() or src.stem
            page.pdf(path=str(out), format=fmt or 'Letter', print_background=True, prefer_css_page_size=fmt is None,
                     display_header_footer=not css_footer,
                     header_template='<span></span>', footer_template=footer_template(title),
                     margin=None if css_footer else {'top': '0.6in', 'bottom': '0.75in',
                                                     'left': '0.6in', 'right': '0.6in'})
        finally:
            browser.close()


def render_png(pdf, outdir, dpi=110):
    """Write page-01.png, page-02.png, ... Returns the list of files, or [] if no renderer works."""
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob('page-*.png'):
        old.unlink()
    if shutil.which('pdftoppm'):
        subprocess.run(['pdftoppm', '-png', '-r', str(dpi), str(pdf), str(outdir / 'page')], check=True)
        files = sorted(outdir.glob('page-*.png'))
        for f in files:  # normalize pdftoppm's variable zero padding to two digits
            f.rename(outdir / f'page-{int(f.stem.split("-")[-1]):02d}.png')
        return sorted(outdir.glob('page-*.png'))
    try:
        import fitz  # pymupdf
    except ImportError:
        return []
    files = []
    with fitz.open(pdf) as doc:
        for i, pg in enumerate(doc, 1):
            f = outdir / f'page-{i:02d}.png'
            pg.get_pixmap(dpi=dpi).save(f)
            files.append(f)
    return files


def page_count(pdf):
    if shutil.which('pdfinfo'):
        out = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.startswith('Pages:'):
                return int(line.split()[1])
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('input', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--format', choices=['Letter', 'A4'],
                    help='Paper size; overrides CSS @page size (default: CSS size, else Letter)')
    ap.add_argument('--png-preview', type=Path, metavar='DIR', help='Also render each page to DIR/page-NN.png')
    a = ap.parse_args()
    if not a.input.is_file():
        sys.exit(f'error: input not found: {a.input}')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        render_pdf(a.input, a.output, a.format)
    except ImportError:
        sys.exit('error: Python Playwright is not installed (pip install playwright). '
                 'Fallback: open the HTML in a browser and use Print -> Save as PDF.')
    except Exception as e:  # browser missing, page error, timeout
        sys.exit(f'error: PDF rendering failed: {e}')
    n = page_count(a.output)
    print(f'wrote {a.output}' + (f' ({n} pages)' if n else ''))
    if a.png_preview:
        try:
            files = render_png(a.output, a.png_preview)
        except Exception as e:
            print(f'warning: PNG preview failed: {e}', file=sys.stderr)
            files = []
        if files:
            print(f'previews: {len(files)} PNG files in {a.png_preview}')
        else:
            print('warning: no PNG renderer (install poppler-utils or pymupdf); PDF written without previews',
                  file=sys.stderr)


if __name__ == '__main__':
    main()
