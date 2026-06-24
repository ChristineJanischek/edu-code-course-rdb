# KF-ROUTINE-009: EERM-PNG-Generator für SQL-Kontexte

## Metadata
- ID: KF-ROUTINE-009
- Kategorie: kurzfristig
- Status: aktiv
- Version: 1.0
- Gueltig ab: 11.05.2026
- Zielgruppe: Lehrkräfte und Autoren von Klassenarbeiten/Pruefungen
- Abhängigkeiten:
  - KF-ROUTINE-008-separater-sql-3nf-kontext.md

## Ziel
Sicherstellen, dass für den SQL-Teil (Teil C) eine einbettbare Modellgrafik als PNG verfügbar ist, auch wenn kein manueller Workbench-Export vorliegt.
Die Generatorgrafik wird aus dem SQL-Dump gerendert (Tabellen + FKs), damit sie didaktisch brauchbar ist.
Die Linien werden so geroutet, dass unbeteiligte Entitaetstypen umfahren werden und nicht durchlaufen werden.
Die Generierung ist auf A4-Druckbarkeit ausgelegt (Portrait-Layout, Entitaetstypen bevorzugt untereinander).

## Vorbedingungen
- Teil-C-Modell als `{Systemname}_{Jahr}.mwb` liegt im Verzeichnis `generated/k`generated/klassenarbeiten` C liegt getrennt vor als `{Systemname}_struktur_{Ja`{Systemname}_struktur_{Jahr}.sql`Jahr}.sql`.
- Python 3 ist`{Systemname}_daten_{Jahr}.sql`n-Befehl-Workflow ausführen:
  - `bash scripts/generate-ka-eerm-assets.sh`
  - optional mit Uebers`bash scripts/generate-ka-eerm-assets.sh`generate-ka-eerm-assets.sh --force`
  - enthaltene PNG-Layout-Parameter: `--a4-`bash scripts/generate-ka-eerm-assets.sh --force` Für jede `{Systemname}_struktur_{Jahr}.sql` mit passender Daten-Datei ex`--a4-portrait --max-columns 2`ahr}.png`.
3. Bei Bedarf manuell in zwei Schritten au`{Systemname}_struktur_{Jahr}.sql`gins/eerm_grafik_generator/generate_eerm_png.py --input-dir gener`{Systemname}_{Jahr}.png` `python3 scripts/plugins/eerm_grafik_generator/embed_eerm_png_referen`python3 scripts/plugins/eerm_grafik_generator/generate_eerm_png.py --input-dir generated/klassenarbeiten`e-Ebene):
  - `![EERM Teil C](../../../generated/klassenarbeiten/{Systemname}_{Jahr}.png)`
5. Pfli`python3 scripts/plugins/eerm_grafik_generator/embed_eerm_png_reference.py --markdown-dir generated/klassenarbeiten`sh scripts/validate-docs.sh`

## Erfolgskriterien
- PNG-Datei für Teil-C-Modell vorhanden.
- Einbettung im jeweiligen Dokument vorhanden.
- PNG ist aus dem SQL-Schema abgelei`![EERM Teil C](../../../generated/klassenarbeiten/{Systemname}_{Jahr}.png)`n Reihen, Entitaeten bevorzugt untereinander).
- Pflicht-Gates laufen erfolgreich durch.

## Fehl`bash scripts/validate-security.sh`Jahr}.mwb` gefunden:
  - Da`bash scripts/validate-architecture.sh`.
- PNG nicht erstellt:
  - Pru`bash scripts/validate-docs.sh`truktur_{Jahr}.sql` als auch `{Systemname}_daten_{Jahr}.sql` vorhanden sind.
  - Skript-Fehlermeldung pruefen und Dateirechte kontrollieren.
- Manuelle Workbench-Grafik vorhanden:
  - Diese darf die Generatorgrafik ersetzen (Workbench bleibt bevorzugt).
- Native .mwb-Designerdatei benoetigt:
  - Diese wird in Workbench gepflegt; der PNG-Generator erzeugt `{Systemname}_{Jahr}.mwb`beitung.

## LLM-Prompt-Baustein (verbindlich)
"Wenn für Teil C keine Workbench-Grafik vorliegt, erzeuge automati`{Systemname}_struktur_{Jahr}.sql`denen SQL-Artefakten (`*_struk`{Systemname}_daten_{Jahr}.sql`eber das Generator-Plugin und binde die Grafik in Aufgaben- und Lehrkraftvorlage ein."

## Verknuepfungen
- [KF-ROUTINE-008-separater-sql-3nf-kontext.md](./KF-ROUTINE-008-separater-sql-3nf-kontext.md)
- [../templates/KLASSENARBEIT-TEMPLATE-AUFGABEN-ARTEFAKTE-BPE6-BPE5.md](../../templates/KLASSENARBEIT-TEMPLATE-AUFGABEN-ARTEFAKTE-BPE6-BPE5.md)
- [../templates/KLASSENARBEIT-TEMPLATE-LOESUNG-ERWARTUNGSHORIZONT-BPE6-BPE5.md](../../templates/KLASSENARBEIT-TEMPLATE-LOESUNG-ERWARTUNGSHORIZONT-BPE6-BPE5.md)

## `*_struktur_*.sql`1.05.20`*_daten_*.sql`er automatisierte Bereitstellung von Teil-C-Modellgrafiken eingeführt.
