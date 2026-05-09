#!/usr/bin/env python3
"""
Konvertiert Muster-Klassenarbeit von Markdown zu verschiedenen Formaten.
Erstellt auch Validierungen und Metadaten.
"""

import os
import sys
import markdown
from pathlib import Path

def markdown_to_html(md_file, html_file):
    """Konvertiert Markdown zu HTML"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['tables', 'extra'])
    
    # Wrap mit HTML-Template
    full_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muster-Klassenarbeit: Relationale Datenbanken</title>
    <style>
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.6;
            margin: 2cm;
            color: #333;
        }}
        h1, h2, h3, h4 {{
            color: #1a5f8f;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        h1 {{ font-size: 24pt; border-bottom: 3px solid #1a5f8f; padding-bottom: 0.5em; }}
        h2 {{ font-size: 18pt; }}
        h3 {{ font-size: 14pt; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 0.5em;
            text-align: left;
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

def main():
    md_file = "/workspaces/edu-code-course-rdb/generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md"
    html_file = "/workspaces/edu-code-course-rdb/generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html"
    
    if not os.path.exists(md_file):
        print(f"❌ Datei nicht gefunden: {md_file}")
        sys.exit(1)
    
    print(f"🔍 Verarbeite: {md_file}\n")
    
    # Validierung
    validate_markdown(md_file)
    
    # Metadaten extrahieren
    extract_metadata(md_file)
    
    # Zu HTML konvertieren
    print(f"\n🔄 Konvertiere zu HTML...")
    markdown_to_html(md_file, html_file)
    print(f"✅ HTML erstellt: {html_file}")
    
    # Dateigröße anzeigen
    md_size = os.path.getsize(md_file) / 1024
    html_size = os.path.getsize(html_file) / 1024
    print(f"\n📊 Dateigröße:")
    print(f"  Markdown: {md_size:.1f} KB")
    print(f"  HTML: {html_size:.1f} KB")
    
    print(f"\n✨ Fertig! Dateien erstellt:")
    print(f"  - Markdown: {md_file}")
    print(f"  - HTML: {html_file}")
    print(f"\n💡 Um zu DOCX zu konvertieren: pandoc {html_file} -o Klassenarbeit.docx")

if __name__ == "__main__":
    main()
