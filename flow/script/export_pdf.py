#!/usr/bin/env python3
"""
Export Markdown notes to A4 PDF for printing.
Usage: uv run flow/script/export_pdf.py <input_dir> [output_dir]
"""
import sys
import os
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

A4_CSS = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}
body {
    font-family: "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #222;
}
h1 {
    font-size: 18pt;
    font-weight: bold;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
    margin-top: 0;
    page-break-before: always;
}
h1:first-of-type {
    page-break-before: auto;
}
h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #333;
}
h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    color: #444;
}
p {
    margin: 0.6em 0;
    text-align: justify;
}
ul, ol {
    margin: 0.5em 0;
    padding-left: 2em;
}
li {
    margin: 0.3em 0;
}
code {
    font-family: "Courier New", Consolas, monospace;
    font-size: 10pt;
    background: #f4f4f4;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}
pre {
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.8em;
    overflow-x: auto;
    font-size: 10pt;
    line-height: 1.4;
    white-space: pre-wrap;
    word-wrap: break-word;
}
blockquote {
    margin: 1em 0;
    padding: 0.5em 1em;
    border-left: 4px solid #ccc;
    background: #f9f9f9;
    color: #555;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
}
th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}
th {
    background: #f0f0f0;
    font-weight: bold;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
.mermaid, .math {
    overflow-x: auto;
}
"""


def md_to_html(md_path: Path) -> str:
    """Read markdown and convert to HTML body via pandoc."""
    import subprocess
    result = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html", "--mathjax", str(md_path)],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed: {result.stderr}")
    return result.stdout


def build_combined_html(md_files: list[Path], title: str) -> str:
    bodies = []
    for f in md_files:
        bodies.append(f"<h1>{f.stem}</h1>")
        bodies.append(md_to_html(f))
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
{chr(10).join(bodies)}
</body>
</html>"""
    return html


def sort_md_files(files: list[Path]) -> list[Path]:
    """
    Sort files in print order:
    1. 课程大纲 (syllabus)
    2. 知识地图_MOC (MOC)
    3. Ch_XX_... chapters in numeric order
    4. Anki_... flashcards last
    """
    def sort_key(f: Path) -> tuple:
        name = f.name
        if "课程大纲" in name:
            return (0, 0, name)
        if "知识地图_MOC" in name or "_MOC" in name:
            return (1, 0, name)
        if name.startswith("Anki_"):
            return (3, 0, name)
        # Ch_XX_... extract chapter number
        m = re.search(r'Ch_(\d+)', name)
        if m:
            return (2, int(m.group(1)), name)
        return (2, 999, name)

    return sorted(files, key=sort_key)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run flow/script/export_pdf.py <input_dir> [output_dir]")
        sys.exit(1)

    input_dir = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    md_files = sort_md_files(list(input_dir.glob("*.md")))
    if not md_files:
        print(f"No .md files found in {input_dir}")
        sys.exit(1)

    course_name = input_dir.name
    output_pdf = output_dir / f"{course_name}_打印版.pdf"

    print(f"Found {len(md_files)} markdown files in {input_dir}")
    print("Print order:")
    for i, f in enumerate(md_files, 1):
        print(f"  {i}. {f.name}")
    print("Converting to HTML via pandoc...")

    html_content = build_combined_html(md_files, course_name)

    print("Rendering PDF with WeasyPrint (A4)...")
    font_config = FontConfiguration()
    HTML(string=html_content).write_pdf(
        str(output_pdf),
        stylesheets=[CSS(string=A4_CSS, font_config=font_config)],
        font_config=font_config
    )

    print(f"Done: {output_pdf}")
    print(f"File size: {output_pdf.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
