import argparse
import shutil
import subprocess
from pathlib import Path

from TemplateProvider import get_template
from strictyaml import load, Map, Str, Int, Seq, YAMLError


TRANSLATIONS = {
    "de": {
        "languages": "Sprachen",
        "skills": "Developer Skills [Auszug]",
        "interests": "Interessen",
        "work_experience": "Berufserfahrung",
        "educational_path": "Bildungsweg",
        "international_experience": "Internationale Erfahrungen",
    },
    "en": {
        "languages": "Languages",
        "skills": "Developer Skills (Excerpt)",
        "interests": "Interests",
        "work_experience": "Work Experience",
        "educational_path": "Education",
        "international_experience": "International Experience",
    },
}


def start_generation(input_path='CVs/input.yaml', output_path='output.html'):
    with open(input_path,'r') as f:
        cv_input = load(f.read()).data

    with open('main.css', 'r') as f:
        style_sheet = f.read()

    language = cv_input.get('language', 'de')
    if language not in TRANSLATIONS:
        raise ValueError(f"Unknown language '{language}', expected one of: {', '.join(TRANSLATIONS)}")

    with open(output_path, 'w') as f:
        f.write(get_template().render(style=style_sheet, t=TRANSLATIONS[language], **cv_input))

def export_pdf(html_path='output.html', pdf_path='output.pdf'):
    """Print the generated HTML to PDF using headless Chromium.

    Equivalent to: browser print with Background graphics on, Borders: None,
    Header and Footer off, and CSS page size respected.
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(Path(html_path).resolve().as_uri())
        page.pdf(
            path=pdf_path,
            print_background=True,   # "Print Background" on
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},  # "Borders: None"
            prefer_css_page_size=True,  # use @page size from CSS
            # no header/footer arguments => none printed
        )
        browser.close()


def compress_pdf(input_pdf='output.pdf', output_pdf='output.pdf'):
    """Compress a PDF using Ghostscript (same settings as before)."""
    if shutil.which('gs') is None:
        print("Warning: Ghostscript (gs) not found on PATH, skipping compression.")
        return
    subprocess.run([
        'gs',
        '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/printer',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_pdf}', input_pdf,
    ], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate CV HTML from a YAML input file.')
    parser.add_argument('input', nargs='?', default='CVs/input.yaml',
                        help='Path to the input YAML file (default: CVs/input.yaml)')
    parser.add_argument('--output', default='output.html', metavar='PATH',
                        help='Path for the generated HTML file (default: output.html). '
                             'PDF output names are derived from this path. '
                             'When compressing, the compressed PDF is written to this path.')
    parser.add_argument('--pdf', action='store_true',
                        help='Also export the HTML to PDF via headless Chromium')
    parser.add_argument('--compress', action='store_true',
                        help='Compress the PDF with Ghostscript (requires gs installed)')
    args = parser.parse_args()

    output = Path(args.output)
    if args.pdf and output.suffix.lower() == '.pdf':
        # The requested output is the PDF; put the intermediate HTML next to it.
        html_path = output.with_suffix('.html')
    else:
        html_path = output

    start_generation(args.input, str(html_path))

    if args.pdf:
        pdf_path = output.with_suffix('.pdf')
        export_pdf(str(html_path), str(pdf_path))
        if args.compress:
            tmp_path = pdf_path.with_name(pdf_path.stem + '.tmp-compressed.pdf')
            compress_pdf(str(pdf_path), str(tmp_path))
            tmp_path.replace(pdf_path)
            print(f'Compressed PDF written to {pdf_path}')
        else:
            print(f'PDF written to {pdf_path}')
