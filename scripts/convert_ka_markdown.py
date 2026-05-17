#!/usr/bin/env python3
"""
Konvertiert Muster-Klassenarbeit von Markdown zu verschiedenen Formaten.
Erstellt auch Validierungen und Metadaten.
"""

import os
import re
from html import escape
import markdown
from pathlib import Path


def _extract_alt_text(img_attrs: str) -> str:
    alt_match = re.search(r'alt\s*=\s*"([^"]*)"', img_attrs, re.IGNORECASE)
    if alt_match:
        return alt_match.group(1).strip() or "Grafik"
    return "Grafik"


def _is_external_src(src: str) -> bool:
    src_lower = src.lower()
    return src_lower.startswith("http://") or src_lower.startswith("https://") or src_lower.startswith("data:")


def _resolve_local_path(md_file: str, src: str) -> Path:
    src_path = Path(src)
    if src_path.is_absolute():
        return src_path
    return (Path(md_file).parent / src_path).resolve()


def _read_svg(svg_path: Path) -> str | None:
    if not svg_path.exists() or svg_path.suffix.lower() != ".svg":
        return None
    svg_markup = svg_path.read_text(encoding="utf-8")
    # XML-Header entfernen, damit valides Inline-SVG in HTML entsteht.
    svg_markup = re.sub(r"^\s*<\?xml[^>]*>\s*", "", svg_markup)
    return svg_markup.strip()


def _render_svg_from_xml(xml_path: Path) -> str | None:
    if not xml_path.exists() or xml_path.suffix.lower() != ".xml":
        return None

    try:
        import sys

        converter_dir = Path(__file__).resolve().parent / "struktogramme" / "converter"
        if str(converter_dir) not in sys.path:
            sys.path.insert(0, str(converter_dir))
        from struktogramm_xml_renderer import BWStruktogrammRenderer

        renderer = BWStruktogrammRenderer()
        return renderer.xml_to_svg(str(xml_path)).strip()
    except Exception as err:  # pragma: no cover - defensiver Fallback
        print(f"⚠️  XML->SVG Konvertierung fehlgeschlagen: {xml_path} ({err})")
        return None


def _to_rel_posix(base_dir: Path, target: Path) -> str:
    return Path(os.path.relpath(target, base_dir)).as_posix()


def _normalize_table_style(existing_style: str) -> str:
    required_props = [
        "width:100%",
        "max-width:100%",
        "table-layout:fixed",
        "border-collapse:collapse",
        "mso-table-lspace:0pt",
        "mso-table-rspace:0pt",
    ]
    existing_chunks = [chunk.strip() for chunk in existing_style.split(";") if chunk.strip()]
    existing_lower = {chunk.lower() for chunk in existing_chunks}
    for prop in required_props:
        if prop.lower() not in existing_lower:
            existing_chunks.append(prop)
    return "; ".join(existing_chunks)


def _ensure_table_fit_to_page_and_word(html_content: str) -> str:
    # Erzwingt robuste Tabellenbreite fuer Print-A4 und Word-Paste (Groesse an Fenster).
    table_open_pattern = re.compile(r"<table\b([^>]*)>", re.IGNORECASE)

    def _replace_table_open(match: re.Match[str]) -> str:
        attrs = match.group(1) or ""

        if re.search(r'\bwidth\s*=\s*"[^"]*"', attrs, re.IGNORECASE):
            attrs = re.sub(r'\bwidth\s*=\s*"[^"]*"', 'width="100%"', attrs, flags=re.IGNORECASE)
        else:
            attrs += ' width="100%"'

        style_match = re.search(r'\bstyle\s*=\s*"([^"]*)"', attrs, re.IGNORECASE)
        if style_match:
            merged_style = _normalize_table_style(style_match.group(1))
            attrs = re.sub(
                r'\bstyle\s*=\s*"[^"]*"',
                f'style="{escape(merged_style, quote=True)}"',
                attrs,
                flags=re.IGNORECASE,
            )
        else:
            merged_style = _normalize_table_style("")
            attrs += f' style="{escape(merged_style, quote=True)}"'

        return f"<table{attrs}>"

    return table_open_pattern.sub(_replace_table_open, html_content)


def _embed_graphics(html_content: str, md_file: str) -> str:
    img_pattern = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*)/?>', re.IGNORECASE)
    base_dir = Path(md_file).parent.resolve()

    def _replace_img(match: re.Match[str]) -> str:
        before_attrs = match.group(1) or ""
        src = match.group(2)
        after_attrs = match.group(3) or ""
        full_attrs = f"{before_attrs} {after_attrs}"
        alt_text = _extract_alt_text(full_attrs)

        if _is_external_src(src):
            return match.group(0)

        local_src = _resolve_local_path(md_file, src)
        src_suffix = local_src.suffix.lower()

        svg_candidates: list[Path] = []
        xml_candidates: list[Path] = []
        png_candidates: list[Path] = []

        if src_suffix == ".svg":
            svg_candidates.append(local_src)
            xml_candidates.append(local_src.with_suffix(".xml"))
            png_candidates.append(local_src.with_suffix(".png"))
        elif src_suffix == ".xml":
            xml_candidates.append(local_src)
            svg_candidates.append(local_src.with_suffix(".svg"))
            png_candidates.append(local_src.with_suffix(".png"))
        elif src_suffix == ".png":
            png_candidates.append(local_src)
            svg_candidates.append(local_src.with_suffix(".svg"))
            xml_candidates.append(local_src.with_suffix(".xml"))
        else:
            svg_candidates.append(local_src.with_suffix(".svg"))
            xml_candidates.append(local_src.with_suffix(".xml"))
            png_candidates.append(local_src.with_suffix(".png"))

        # 1) Bevorzugt SVG inline einbetten
        for svg_path in svg_candidates:
            svg_markup = _read_svg(svg_path)
            if svg_markup:
                print(f"🖼️  Inline-SVG eingebettet: {svg_path}")
                return (
                    f'<figure class="ka-figure" aria-label="{escape(alt_text, quote=True)}">\n'
                    f"{svg_markup}\n"
                    "</figure>"
                )

        # 2) XML zur Laufzeit in SVG wandeln und inline einbetten
        for xml_path in xml_candidates:
            svg_markup = _render_svg_from_xml(xml_path)
            if svg_markup:
                print(f"🧩 XML zu Inline-SVG konvertiert: {xml_path}")
                return (
                    f'<figure class="ka-figure" aria-label="{escape(alt_text, quote=True)}">\n'
                    f"{svg_markup}\n"
                    "</figure>"
                )

        # 3) Fallback auf PNG
        for png_path in png_candidates:
            if png_path.exists():
                rel_src = _to_rel_posix(base_dir, png_path.resolve())
                print(f"🖼️  PNG-Fallback verwendet: {png_path}")
                return (
                    "<figure class=\"ka-figure\">"
                    f"<img alt=\"{escape(alt_text, quote=True)}\" src=\"{escape(rel_src, quote=True)}\" />"
                    "</figure>"
                )

        return match.group(0)

    return img_pattern.sub(_replace_img, html_content)


def _wrap_tables(html_content: str) -> str:
    # Tabellen in einen responsiven Container setzen, damit sie immer zur Seitenbreite passen.
    return re.sub(r"(?is)(<table\b.*?</table>)", r'<div class="table-wrap">\1</div>', html_content)

def markdown_to_html(md_file, html_file):
    """Konvertiert Markdown zu HTML"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['tables', 'extra'])
    html_content = _embed_graphics(html_content, md_file)
    html_content = _ensure_table_fit_to_page_and_word(html_content)
    html_content = _wrap_tables(html_content)
    
    # Wrap mit HTML-Template (A4-druckoptimiert)
    full_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muster-Klassenarbeit: Relationale Datenbanken</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 12mm;
        }}
        html, body {{
            padding: 0;
        }}
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.45;
            margin: 0;
            width: 100%;
            max-width: none;
            box-sizing: border-box;
            padding: 0 12mm;
            color: #222;
            font-size: 11pt;
        }}
        h1, h2, h3, h4 {{
            color: #1a5f8f;
            margin-top: 1em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
        }}
        h1 {{ font-size: 20pt; border-bottom: 3px solid #1a5f8f; padding-bottom: 0.35em; }}
        h2 {{ font-size: 15pt; }}
        h3 {{ font-size: 12.5pt; }}
        p, li {{
            orphans: 3;
            widows: 3;
        }}
        .table-wrap {{
            width: 100%;
            max-width: 100%;
            overflow-x: auto;
            margin: 1em 0;
            page-break-inside: avoid;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            min-width: 100%;
            margin: 0;
            table-layout: fixed;
            page-break-inside: avoid;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 0.4em 0.45em;
            text-align: left;
            vertical-align: top;
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 10.5pt;
            overflow-wrap: anywhere;
            word-break: break-word;
        }}
        table th {{
            background-color: #e8f1f7;
            font-weight: bold;
        }}
        pre {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1em;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 2px;
            font-family: 'Courier New', monospace;
        }}
        .box {{
            border-left: 4px solid #1a5f8f;
            padding: 1em;
            margin: 1em 0;
            background-color: #f0f5fa;
        }}
        .hint {{ border-left-color: #ffa500; background-color: #fffaf0; }}
        .warning {{ border-left-color: #ff6b6b; background-color: #ffe0e0; }}
        img {{
            display: block;
            max-width: 100%;
            height: auto;
            margin: 0.6em auto;
            border: 1px solid #d3dbe8;
            border-radius: 6px;
            page-break-inside: avoid;
        }}
        .ka-figure {{
            margin: 0.8em 0;
            page-break-inside: avoid;
        }}
        .ka-figure svg {{
            display: block;
            width: 100%;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            border: 1px solid #d3dbe8;
            border-radius: 6px;
            background: #fff;
        }}
        @media print {{
            body {{
                max-width: none;
                margin: 0;
            }}
            .table-wrap {{
                overflow: visible;
            }}
            pre, blockquote, table, img {{
                page-break-inside: avoid;
            }}
            h2, h3 {{
                break-after: avoid-page;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return html_file

def validate_markdown(md_file):
    """Führt grundlegende Validierungen durch"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    validation = {
        "has_frontmatter": content.startswith("---"),
        "has_aufgaben": content.count("## Aufgabe") > 0,
        "table_count": content.count("|"),
        "code_block_count": content.count("```"),
        "heading_count": content.count("# "),
        "link_count": content.count("[") and content.count("]"),
    }
    
    print("✅ Markdown-Validierung:")
    for key, value in validation.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}: {value}")
    
    return validation

def extract_metadata(md_file):
    """Extrahiert Metadaten aus Frontmatter"""
    import re
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        print("\n📋 Metadaten:")
        for line in frontmatter.split('\n'):
            if line.strip():
                print(f"  {line}")
    
    # Extrahiere Aufgaben
    aufgaben = re.findall(r'## Aufgabe (\d+):(.*?)\n\n', content)
    print(f"\n📝 Aufgaben gefunden: {len(aufgaben)}")
    for num, title in aufgaben:
        print(f"  Aufgabe {num}: {title.strip()[:60]}...")

def find_ka_markdown_files(base_dir: Path) -> list[Path]:
    """Find KA markdown files following KF-ROUTINE-010 naming.

    Allowed suffixes:
    - *_aufg.md
    - *_lsg.md
    """
    files: list[Path] = []
    for md_file in sorted(base_dir.glob("KA*_*.md")):
        name = md_file.name
        if name.endswith("_aufg.md") or name.endswith("_lsg.md"):
            files.append(md_file)
    return files


def main():
    base_dir = Path("/workspaces/edu-code-course-rdb/generated/klassenarbeiten")
    md_files = find_ka_markdown_files(base_dir)

    if not md_files:
        print(f"❌ Keine KA-Markdown-Dateien gefunden in: {base_dir}")
        raise SystemExit(1)

    print(f"🔍 Gefundene KA-Markdown-Dateien: {len(md_files)}")

    generated_html: list[Path] = []
    for md_file in md_files:
        html_file = md_file.with_suffix(".html")
        print(f"\n🔄 Verarbeite: {md_file}")

        # Validierung
        validate_markdown(str(md_file))

        # Metadaten extrahieren
        extract_metadata(str(md_file))

        # Zu HTML konvertieren
        markdown_to_html(str(md_file), str(html_file))
        print(f"✅ HTML erstellt: {html_file}")
        generated_html.append(html_file)

    print("\n✨ Fertig! Dateien erstellt:")
    for html_file in generated_html:
        print(f"  - {html_file}")
    if generated_html:
        print(f"\n💡 Um zu DOCX zu konvertieren: pandoc {generated_html[0]} -o Klassenarbeit.docx")

if __name__ == "__main__":
    main()
