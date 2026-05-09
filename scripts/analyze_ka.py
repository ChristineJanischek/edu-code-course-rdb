#!/usr/bin/env python3
"""
Analysiert die Struktur der Klassenarbeit KA02 und extrahiert:
- Aufgabentitel und -struktur
- Punkteverteilung pro BPE
- Zeitaufwand
- Aufgabentypen (Struktogramm, Code, Analyse)
"""

from docx import Document
from docx.text.paragraph import Paragraph
import json
import sys

def analyze_docx(filepath):
    """Extrahiert strukturierte Informationen aus einer DOCX-Datei"""
    doc = Document(filepath)
    
    content = {
        "title": "",
        "metadata": {},
        "aufgaben": [],
        "gesamt_punkte": 0,
        "bpe_verteilung": {},
    }
    
    current_aufgabe = None
    in_aufgabe = False
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            continue
            
        # Titel erkennen
        if para.style.name.startswith('Heading 1'):
            content["title"] = text
        
        # Aufgaben erkennen
        if text.startswith('Aufgabe') or text.startswith('Task'):
            if current_aufgabe:
                content["aufgaben"].append(current_aufgabe)
            
            current_aufgabe = {
                "title": text,
                "punkte": 0,
                "bpe": "",
                "text": [],
                "has_strukturgram": False,
                "has_code": False,
                "has_sql": False
            }
            in_aufgabe = True
        elif in_aufgabe:
            # Punkte extrahieren
            if "Punkt" in text or "Point" in text:
                try:
                    punkte = [int(s) for s in text.split() if s.isdigit()]
                    if punkte:
                        current_aufgabe["punkte"] = max(punkte)
                        content["gesamt_punkte"] += current_aufgabe["punkte"]
                except:
                    pass
            
            # BPE erkennen
            if "BPE" in text or "bpe" in text.lower():
                current_aufgabe["bpe"] = text
            
            # Aufgabentyp erkennen
            if "Struktogramm" in text or "Flowchart" in text:
                current_aufgabe["has_strukturgram"] = True
            if "Code" in text or "Python" in text or "Java" in text:
                current_aufgabe["has_code"] = True
            if "SQL" in text or "Datenbank" in text:
                current_aufgabe["has_sql"] = True
            
            current_aufgabe["text"].append(text)
    
    if current_aufgabe:
        content["aufgaben"].append(current_aufgabe)
    
    # Zusammenfassung
    print(f"\n✅ Datei analysiert: {filepath}")
    print(f"📝 Titel: {content['title']}")
    print(f"📊 Aufgaben: {len(content['aufgaben'])}")
    print(f"⭐ Gesamt Punkte: {content['gesamt_punkte']}")
    print(f"\n📋 Aufgabendetails:")
    
    for i, aufgabe in enumerate(content['aufgaben'], 1):
        print(f"\n  Aufgabe {i}: {aufgabe['title']}")
        print(f"    - Punkte: {aufgabe['punkte']}")
        print(f"    - BPE: {aufgabe['bpe']}")
        print(f"    - Struktogramm: {aufgabe['has_strukturgram']}")
        print(f"    - Code: {aufgabe['has_code']}")
        print(f"    - SQL: {aufgabe['has_sql']}")
    
    return content

def main():
    ka_file = "/workspaces/edu-code-course-rdb/uploads/klassenarbeiten-und-unterrichtsmaterialien/KA02_INF_BG12_2024_2025_CJ_LSG_VERSION3.docx"
    
    print("🔍 Analysiere Klassenarbeit...")
    try:
        result = analyze_docx(ka_file)
        with open("/tmp/ka_analysis.json", "w") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
