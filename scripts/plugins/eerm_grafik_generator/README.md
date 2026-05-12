# EERM Grafik Generator (Plugin)

Dieses Plugin erzeugt PNG-Modellgrafiken fuer SQL-Kontexte von Klassenarbeiten auf Basis des SQL-Dumps.

## Ziel

- Lesbare EERM-Referenzgrafik aus Tabellen und Fremdschluesseln des SQL-Dumps
- Stabiler Generator fuer `{Systemname}_struktur_{Jahr}.sql` + `{Systemname}_daten_{Jahr}.sql`

## Voraussetzung

- Python-Paket `Pillow` (PIL)
  - Installation: `pip install Pillow`

## Aufruf

Ein-Befehl-Variante (empfohlen):

```bash
bash scripts/generate-ka-eerm-assets.sh
```

Optional mit Ueberschreiben bestehender PNGs:

```bash
bash scripts/generate-ka-eerm-assets.sh --force
```

Manuell in zwei Schritten:

```bash
python3 scripts/plugins/eerm_grafik_generator/generate_eerm_png.py \
  --input-dir generated/klassenarbeiten
```

Danach PNG-Referenz automatisch in Klassenarbeits-Markdown einbetten:

```bash
python3 scripts/plugins/eerm_grafik_generator/embed_eerm_png_reference.py \
  --markdown-dir generated/klassenarbeiten
```

Optional:

```bash
python3 scripts/plugins/eerm_grafik_generator/generate_eerm_png.py \
  --input-dir generated/klassenarbeiten \
  --a4-portrait \
  --max-columns 2 \
  --force
```

## Verhalten

- Sucht rekursiv nach `*_struktur_*.sql`
- Prueft zu jeder Strukturdatei die passende Daten-Datei `*_daten_*.sql`
- Rendert daraus Tabellenkarten und FK-Beziehungen als PNG
- Standard-Workflow erzeugt A4-portrait-freundliche Diagramme (Entitaetstypen staerker untereinander)
- Routed FK-Linien orthogonal um unbeteiligte Tabellen herum, statt Karten zu kreuzen
- Reserviert bereits verwendete Routing-Zellen pro Verbindung, damit FK-Linien nicht deckungsgleich aufeinander liegen
- Begrenzt Routing-Korridore auf den Diagrammbereich, um lange Aussenumwege (insbesondere rechts) zu reduzieren
- Ueberschreibt bestehende PNGs nur mit `--force`
- Betroffene Markdown-Dateien erhalten (falls fehlend) einen Abschnitt "Modellgrafik Teil C" mit PNG-Einbettung

Hinweis: Falls MySQL Workbench verfuegbar ist, kann ein nativer Export weiterhin verwendet werden.
