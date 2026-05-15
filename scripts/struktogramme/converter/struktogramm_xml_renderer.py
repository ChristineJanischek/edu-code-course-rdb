#!/usr/bin/env python3
"""
XML-Struktogramm zu SVG Renderer (BW-Standard konform)

Konvertiert XML-definierte Struktogramme zu professionellen SVG-Grafiken
nach Baden-Württemberg Abitur-Standards (Operatorenliste).

KORREKTE BW-FORMEN:
1. Anweisungen: Rechteck mit "Bezeichnung:" in Zeile 1, dann Formulierung
2. Alternative: Briefumschlag-Form (Dreieck oben mit Bedingung, links J, rechts N)
3. Schleife: Umgedrehtes L gespiegelt (Kopf oben, Körper darunter eingerückt)
4. Funktionsaufruf: Rechteck mit vertikalen Strichen links/rechts

Usage:
    python struktogramm_xml_renderer.py input.xml output.svg
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SVGConfig:
    """Rendering-Konfiguration nach BW-Standard"""
    WIDTH: int = 700
    HEIGHT: int = 1200
    BOX_WIDTH: int = 600
    BOX_HEIGHT: int = 50
    MARGIN_TOP: int = 80
    MARGIN_LEFT: int = 50
    FONT_SIZE: int = 13
    LINE_SPACING: int = 18
    STROKE_WIDTH: int = 2
    
    # Spezielle Höhen
    DECISION_TRIANGLE_HEIGHT: int = 40
    DECISION_BODY_HEIGHT: int = 80
    LOOP_HEADER: int = 40
    
    INDENT: int = 20  # Einrückung für Schleifenkörper


class BWStruktogrammRenderer:
    """SVG-Generator für BW-Standard Struktogramme"""
    
    def __init__(self):
        self.config = SVGConfig()
        self.current_y = self.config.MARGIN_TOP
        self.svg_parts = []
    
    def xml_to_svg(self, xml_file: str) -> str:
        """Konvertiere XML zu SVG nach BW-Standard"""
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Metadaten
        metadata = root.find("metadata")
        titel = metadata.find("titel").text if metadata is not None else "Struktogramm"
        
        # Reset für neues Rendering
        self.current_y = self.config.MARGIN_TOP
        
        # Inhalt zuerst rendern um Höhe zu messen
        inhalt = root.find("inhalt")
        inhalt_svg = ""
        if inhalt is not None:
            inhalt_svg = self._render_inhalt(inhalt, self.config.MARGIN_LEFT, self.config.BOX_WIDTH)
        
        # Berechne finale Höhe basierend auf Inhalt
        final_height = int(self.current_y) + 30  # 30px Puffer unten
        
        # SVG Header mit dynamischer Höhe
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
     width="{self.config.WIDTH}" 
     height="{final_height}" 
     viewBox="0 0 {self.config.WIDTH} {final_height}">
  
  <style>
    .box {{ stroke: #000; stroke-width: {self.config.STROKE_WIDTH}; fill: #fff; }}
    .text {{ font-family: Arial, sans-serif; font-size: {self.config.FONT_SIZE}px; fill: #000; }}
    .label {{ font-size: 11px; fill: #666; }}
    .bold {{ font-weight: bold; }}
  </style>
  
  <!-- Titel -->
  <text x="{self.config.WIDTH // 2}" y="30" class="text bold" text-anchor="middle" font-size="16">{titel}</text>
  <line x1="30" y1="50" x2="{self.config.WIDTH - 30}" y2="50" stroke="#000" stroke-width="1"/>
  
'''
        
        # Inhalt + Footer
        svg += inhalt_svg
        svg += "</svg>"
        
        return svg
    
    def _create_svg_header(self, titel: str) -> str:
        """Erstelle SVG-Header mit Titel"""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" 
     width="{self.config.WIDTH}" 
     height="{self.config.HEIGHT}" 
     viewBox="0 0 {self.config.WIDTH} {self.config.HEIGHT}">
  
  <style>
    .box {{ stroke: #000; stroke-width: {self.config.STROKE_WIDTH}; fill: #fff; }}
    .text {{ font-family: Arial, sans-serif; font-size: {self.config.FONT_SIZE}px; fill: #000; }}
    .label {{ font-size: 11px; fill: #666; }}
    .bold {{ font-weight: bold; }}
  </style>
  
  <!-- Titel -->
  <text x="{self.config.WIDTH // 2}" y="30" class="text bold" text-anchor="middle" font-size="16">{titel}</text>
  <line x1="30" y1="50" x2="{self.config.WIDTH - 30}" y2="50" stroke="#000" stroke-width="1"/>
  
'''
    
    def _render_inhalt(self, element: ET.Element, x: int, width: int) -> str:
        """Rendere Inhalts-Elemente rekursiv"""
        svg = ""
        
        for child in element:
            tag = child.tag
            
            if tag in ["prozess", "eingabe", "ausgabe", "rueckgabe"]:
                svg += self._render_anweisung(child, tag, x, width)
            
            elif tag == "wenn":
                svg += self._render_alternative(child, x, width)
            
            elif tag == "wiederhole":
                svg += self._render_while_schleife(child, x, width)
            
            elif tag == "zaehle":
                svg += self._render_for_schleife(child, x, width)
            
            elif tag == "wiederhole_von":
                svg += self._render_wiederhole_von_schleife(child, x, width)
            
            elif tag == "aufruf":
                svg += self._render_funktionsaufruf(child, x, width)
        
        return svg
    
    def _render_anweisung(self, element: ET.Element, typ: str, x: int, width: int) -> str:
        """
        Rendere Anweisung als Rechteck nach BW-Standard:
        Zeile 1: Bezeichnung: (z.B. "Zuweisung:", "Eingabe:")
        Zeile 2+: Formulierung (z.B. "alter als Ganzzahl")
        
        Differenzierte Bezeichnungen nach BW-Standard:
        - Deklaration: (nur Typ ohne Wert)
        - Deklaration und Initialisierung: (Typ mit Wert)
        - Einlesen: (Input ohne Typ)
        - Deklaration und Einlesen: (Input mit Typ)
        - Zuweisung: (Variable = Wert)
        - Ausgabe: (Output)
        - Rückgabe: (Return)
        """
        text = element.text.strip() if element.text else ""
        
        # Ermittle die genaue Bezeichnung basierend auf typ-Attribut
        typ_attr = self._ensure_typ_attr(element, typ)
        
        # Mapping für alle differenzierten Bezeichnungen
        bezeichnung_map = {
            # Prozess (Variable)
            "deklaration": "Deklaration",
            "deklaration_und_initialisierung": "Deklaration und Initialisierung",
            "zuweisung": "Zuweisung",
            "default": "Anweisung",
            
            # Eingabe
            "einlesen": "Einlesen",
            "deklaration_und_einlesen": "Deklaration und Einlesen",
            
            # Ausgabe
            "ausgabe": "Ausgabe",
            
            # Rückgabe
            "rueckgabe": "Rückgabe"
        }
        
        # Wähle Bezeichnung basierend auf typ-Attribut oder Fallback auf Element-Tag
        if typ_attr in bezeichnung_map:
            bezeichnung = bezeichnung_map[typ_attr]
        else:
            # Fallback: Basierend auf Tag-Namen
            tag_map = {
                "prozess": "Anweisung",
                "eingabe": "Einlesen",
                "ausgabe": "Ausgabe",
                "rueckgabe": "Rückgabe"
            }
            bezeichnung = tag_map.get(typ, "Anweisung")
        
        # Berechne Höhe (abhängig von Textlänge)
        lines = text.split('\n')
        height = max(self.config.BOX_HEIGHT, 30 + len(lines) * self.config.LINE_SPACING)
        
        # Rechteck
        svg = f'''  <!-- {typ.upper()} -->
  <rect x="{x}" y="{self.current_y}" width="{width}" height="{height}" class="box"/>
  
  <!-- Bezeichnung -->
  <text x="{x + 10}" y="{self.current_y + 18}" class="text label">{bezeichnung}:</text>
  
  <!-- Text -->
'''
        
        # Text-Zeilen
        text_y = self.current_y + 35
        for line in lines:
            svg += f'  <text x="{x + 10}" y="{text_y}" class="text">{self._escape_xml(line)}</text>\n'
            text_y += self.config.LINE_SPACING
        
        self.current_y += height
        return svg

    def _ensure_typ_attr(self, element: ET.Element, tag: str) -> str:
        """Setzt fehlende typ-Attribute anhand einfacher Heuristiken."""
        typ_attr = element.get("typ")
        if typ_attr:
            return typ_attr

        text = element.text.strip() if element.text else ""
        inferred = self._infer_typ_attr(text, tag)
        if inferred:
            element.set("typ", inferred)
            return inferred

        return "default"

    def _infer_typ_attr(self, text: str, tag: str) -> str:
        """Leitet den Typ aus Tag und Text ab, wenn kein Attribut vorhanden ist."""
        if tag == "ausgabe":
            return "ausgabe"
        if tag == "rueckgabe":
            return "rueckgabe"
        if tag == "eingabe":
            if " als " in text:
                return "deklaration_und_einlesen"
            return "einlesen"
        if tag == "prozess":
            if " als " in text and "=" in text:
                return "deklaration_und_initialisierung"
            if " als " in text:
                return "deklaration"
            if "=" in text:
                return "zuweisung"
            return "default"
        return "default"
    
    def _render_alternative(self, element: ET.Element, x: int, width: int) -> str:
        """
        Rendere Alternative als Briefumschlag-Form (BW-Standard):
        - Rechteck als Gesamtform
        - Eingebettetes gleichschenkliges Dreieck (Hypotenuse oben, Spitze unten)
        - Bedingung im Dreieck
        - Links unten: J-Zweig (Ecke)
        - Rechts unten: N-Zweig (Ecke)
        """
        bedingung_elem = element.find("bedingung")
        bedingung = bedingung_elem.text.strip() if bedingung_elem is not None else "?"
        
        dann_elem = element.find("dann")
        sonst_elem = element.find("sonst")
        
        triangle_h = self.config.DECISION_TRIANGLE_HEIGHT
        min_body_h = self.config.DECISION_BODY_HEIGHT
        branch_padding = 20
        
        start_y = self.current_y
        
        # Koordinaten berechnen
        mid_x = x + width // 2
        top_y = start_y
        triangle_bottom_y = start_y + triangle_h
        body_start_y = triangle_bottom_y
        half_width = width // 2
        
        # Inhalte vorab rendern, um die benötigte Höhe zu bestimmen
        branch_start_y = body_start_y + branch_padding
        svg_dann, dann_end_y = self._render_branch(dann_elem, x + 15, half_width - 25, branch_start_y)
        svg_sonst, sonst_end_y = self._render_branch(sonst_elem, mid_x + 15, half_width - 25, branch_start_y)
        
        content_end_y = max(dann_end_y, sonst_end_y)
        body_h = max(min_body_h, content_end_y - body_start_y)
        total_bottom_y = body_start_y + body_h
        
        svg = f'''  <!-- ALTERNATIVE (Briefumschlag - BW-Standard) -->
  <!-- Äußeres Rechteck -->
  <rect x="{x}" y="{top_y}" width="{width}" height="{triangle_h + body_h}" class="box"/>
  
  <!-- Eingebettetes Dreieck (Hypotenuse oben, Spitze unten) -->
  <polygon points="{x},{top_y} {x + width},{top_y} {mid_x},{triangle_bottom_y}" 
           fill="#fff" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>
  
  <!-- Bedingung im Dreieck (obere Hälfte) -->
  <text x="{mid_x}" y="{top_y + triangle_h // 3 + 5}" class="text" text-anchor="middle">{self._escape_xml(bedingung)}</text>
  
'''
        
        # Vertikale Trennlinie in der Mitte (vom Dreieck bis unten)
        svg += f'  <line x1="{mid_x}" y1="{triangle_bottom_y}" x2="{mid_x}" y2="{total_bottom_y}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        # J und N Labels in den Ecken unten
        svg += f'  <text x="{x + 10}" y="{triangle_bottom_y + 15}" class="text bold">J</text>\n'
        svg += f'  <text x="{mid_x + 10}" y="{triangle_bottom_y + 15}" class="text bold">N</text>\n'
        
        # Inhalte der Zweige
        svg += svg_dann
        svg += svg_sonst
        
        # Untere Abschlusslinie (setze current_y auf Ende der Alternative)
        self.current_y = total_bottom_y
        
        return svg

    def _render_branch(
        self,
        branch_elem: ET.Element,
        x: int,
        width: int,
        start_y: int,
    ) -> Tuple[str, int]:
        """Rendere einen Zweig ab start_y und gib SVG sowie Endposition zurück."""
        old_y = self.current_y
        self.current_y = start_y
        svg = ""
        if branch_elem is not None and len(branch_elem) > 0:
            svg = self._render_inhalt(branch_elem, x, width)
        end_y = self.current_y
        self.current_y = old_y
        return svg, end_y
    
    def _render_while_schleife(self, element: ET.Element, x: int, width: int) -> str:
        """
        Rendere While-Schleife als umgedrehtes L (gespiegelt):
        - Horizontale Linie oben (Schleifenkopf) mit Bedingung
        - Vertikale Linie links runter
        - Körper eingerückt
        """
        bedingung_elem = element.find("bedingung")
        bedingung = bedingung_elem.text.strip() if bedingung_elem is not None else "?"
        
        inhalt_elem = element.find("inhalt")
        
        loop_h = self.config.LOOP_HEADER
        start_y = self.current_y
        
        # Schleifenkopf (horizontale Linie + Text)
        svg = f'''  <!-- WHILE-SCHLEIFE (umgedrehtes L) -->
  <!-- Schleifenkopf -->
  <rect x="{x}" y="{start_y}" width="{width}" height="{loop_h}" class="box"/>
  <text x="{x + 10}" y="{start_y + loop_h // 2 + 5}" class="text">Wiederhole solange {self._escape_xml(bedingung)}</text>
  
'''
        
        self.current_y += loop_h
        
        # Schleifenkörper (eingerückt mit vertikaler Linie links)
        indent = self.config.INDENT
        body_start_y = self.current_y
        
        # Vertikale Linie links
        svg += f'  <line x1="{x}" y1="{start_y + loop_h}" x2="{x}" y2="{{BODY_END}}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        # Körper rendern (eingerückt)
        if inhalt_elem is not None and len(inhalt_elem) > 0:
            svg += self._render_inhalt(inhalt_elem, x + indent, width - indent)
        
        body_end_y = self.current_y
        
        # Ersetze Platzhalter mit tatsächlicher Endposition
        svg = svg.replace("{BODY_END}", str(body_end_y))
        
        # Untere Abschlusslinie
        svg += f'  <line x1="{x}" y1="{body_end_y}" x2="{x + width}" y2="{body_end_y}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        return svg
    
    def _render_for_schleife(self, element: ET.Element, x: int, width: int) -> str:
        """
        Rendere For-Schleife als umgedrehtes L (wie While):
        - Kopf: "Zähle variable von start bis ende, Schrittweite n"
        - Körper: eingerückt
        """
        variable = element.find("variable").text.strip() if element.find("variable") is not None else "i"
        von = element.find("von").text.strip() if element.find("von") is not None else "0"
        bis = element.find("bis").text.strip() if element.find("bis") is not None else "n"
        schrittweite_elem = element.find("schrittweite")
        schrittweite = schrittweite_elem.text.strip() if schrittweite_elem is not None else "1"
        
        inhalt_elem = element.find("inhalt")
        
        loop_h = self.config.LOOP_HEADER
        start_y = self.current_y
        
        # Schleifenkopf
        svg = f'''  <!-- FOR-SCHLEIFE (umgedrehtes L) -->
  <rect x="{x}" y="{start_y}" width="{width}" height="{loop_h}" class="box"/>
  <text x="{x + 10}" y="{start_y + loop_h // 2 + 5}" class="text">Zähle {variable} von {von} bis {bis}, Schrittweite {schrittweite}</text>
  
'''
        
        self.current_y += loop_h
        
        # Körper (eingerückt)
        indent = self.config.INDENT
        body_start_y = self.current_y
        
        svg += f'  <line x1="{x}" y1="{start_y + loop_h}" x2="{x}" y2="{{BODY_END}}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        if inhalt_elem is not None and len(inhalt_elem) > 0:
            svg += self._render_inhalt(inhalt_elem, x + indent, width - indent)
        
        body_end_y = self.current_y
        svg = svg.replace("{BODY_END}", str(body_end_y))
        
        svg += f'  <line x1="{x}" y1="{body_end_y}" x2="{x + width}" y2="{body_end_y}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        return svg
    
    def _render_wiederhole_von_schleife(self, element: ET.Element, x: int, width: int) -> str:
        """
        Rendere Wiederhole-von-Schleife (alternative For-Formulierung):
        Wiederhole von variable = start, solange bedingung, Schrittweite n
        Form: Umgedrehtes L (wie While/For)
        """
        variable = element.find("variable").text.strip() if element.find("variable") is not None else "i"
        start = element.find("start").text.strip() if element.find("start") is not None else "0"
        bedingung = element.find("bedingung").text.strip() if element.find("bedingung") is not None else "true"
        schrittweite_elem = element.find("schrittweite")
        schrittweite = schrittweite_elem.text.strip() if schrittweite_elem is not None else "1"
        
        inhalt_elem = element.find("inhalt")
        
        loop_h = self.config.LOOP_HEADER
        start_y = self.current_y
        
        # Schleifenkopf
        svg = f'''  <!-- WIEDERHOLE-VON-SCHLEIFE (umgedrehtes L) -->
  <rect x="{x}" y="{start_y}" width="{width}" height="{loop_h}" class="box"/>
  <text x="{x + 10}" y="{start_y + loop_h // 2 + 5}" class="text">Wiederhole von {variable} = {start}, solange {self._escape_xml(bedingung)}, Schrittweite {schrittweite}</text>
  
'''
        
        self.current_y += loop_h
        
        # Körper (eingerückt)
        indent = self.config.INDENT
        body_start_y = self.current_y
        
        svg += f'  <line x1="{x}" y1="{start_y + loop_h}" x2="{x}" y2="{{BODY_END}}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        if inhalt_elem is not None and len(inhalt_elem) > 0:
            svg += self._render_inhalt(inhalt_elem, x + indent, width - indent)
        
        body_end_y = self.current_y
        svg = svg.replace("{BODY_END}", str(body_end_y))
        
        svg += f'  <line x1="{x}" y1="{body_end_y}" x2="{x + width}" y2="{body_end_y}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>\n'
        
        return svg
    
    def _render_funktionsaufruf(self, element: ET.Element, x: int, width: int) -> str:
        """
        Rendere Funktionsaufruf als Rechteck mit vertikalen Strichen:
        | Aufruf: funktionsname(parameter) |
        """
        text = element.text.strip() if element.text else ""
        height = self.config.BOX_HEIGHT
        
        svg = f'''  <!-- FUNKTIONSAUFRUF -->
  <!-- Hauptrechteck -->
  <rect x="{x}" y="{self.current_y}" width="{width}" height="{height}" class="box"/>
  
  <!-- Vertikale Striche links und rechts -->
  <line x1="{x + 10}" y1="{self.current_y}" x2="{x + 10}" y2="{self.current_y + height}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>
  <line x1="{x + width - 10}" y1="{self.current_y}" x2="{x + width - 10}" y2="{self.current_y + height}" stroke="#000" stroke-width="{self.config.STROKE_WIDTH}"/>
  
  <!-- Text -->
  <text x="{x + width // 2}" y="{self.current_y + height // 2 + 5}" class="text" text-anchor="middle">Aufruf: {self._escape_xml(text)}</text>
  
'''
        
        self.current_y += height
        return svg
    
    def _escape_xml(self, text: str) -> str:
        """Escape XML-Sonderzeichen"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))
    
    def save_svg(self, filename: str, svg_content: str) -> None:
        """Speichere SVG in Datei"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ SVG gespeichert: {filename}")


def main():
    """Kommandozeilen-Interface"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Konvertiert XML-Struktogramme zu SVG-Grafiken (BW-Standard)"
    )
    parser.add_argument(
        "xml_file",
        help="Pfad zur XML-Struktogramm Datei"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        help="Ausgabe-SVG Datei (default: Eingabedatei mit .svg)"
    )
    
    args = parser.parse_args()
    
    # Bestimme Ausgabedatei
    if args.output_file is None:
        output_file = args.xml_file.replace('.xml', '.svg')
    else:
        output_file = args.output_file
    
    try:
        renderer = BWStruktogrammRenderer()
        print(f"📖 Parsing: {args.xml_file}")
        svg = renderer.xml_to_svg(args.xml_file)
        
        print(f"💾 Speichern: {output_file}")
        renderer.save_svg(output_file, svg)
        
        print(f"✅ Erfolgreich! ({len(svg)} Bytes)")
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Datei nicht gefunden: {e}")
        return 1
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
