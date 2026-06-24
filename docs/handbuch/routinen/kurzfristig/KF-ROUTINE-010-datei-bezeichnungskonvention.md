# KF-ROUTINE-010: Benennungskonvention für Klassenarbeits-Artefakte

## Metadata
- ID: KF-ROUTINE-010
- Kategorie: kurzfristig
- Status: aktiv
- Version: 1.1
- Gueltig ab: 11.05.2026
- Zielgruppe: Lehrkräfte und Autoren von Klassenarbeiten/Pruefungen
- Abhängigkeiten:
  - KF-ROUTINE-008-separater-sql-3nf-kontext.md
  - KF-ROUTINE-009-eerm-png-generator.md

## Ziel
Einheitliche, aussagekraeftige Benennung aller Dateiartefakte im Klassenaarbeitsverzeichnis (`generated/klassenarbeiten`), damit Lehrkräfte und Schüler sofort erkennen, um welche Dateiart es sich handelt und für welchen Sachverhalt/Schuljahr.

## Namenskonvention

### A) Modell-Container (.mwb)
**Format:** `{Systemname}_`{Systemname}_{Jahr}.mwb` `kursplattform_2025.mwb`

`kursplattform_2025.mwb`mlauten (z.B. `kursplattform`, `stadtfahrradverleih`kursplattform`ljah`stadtfahrradverleih`026)
- Kurz und aussagekraeftig, keine Jahrspannen oder Versionsindizes im Dateinamen

### B) SQL-Struktur-Dumps (.sql)
**Format:** `{Systemname}_struktur_{Jahr}.sql`
**Beispiel:*`{Systemname}_struktur_{Jahr}.sql`25.sql`

- Enthaelt: CREATE DATABASE`stadtfahrradverleih_struktur_2025.sql`emdschluessel, Indizes)
- KEINE INSERT/UPDATE/DELETE Statements
- Eine Datei pro Sachverhalt/Modell
- Klar identifizierbar als Struktur-Definition

### C) SQL-Daten-Dumps (.sql)
**Format:** `{Systemname}_daten_{Jahr}.sql`
**Beispiel:** `stadtfahrradverleih_daten_2025.sql`

- Enthaelt`{Systemname}_daten_{Jahr}.sql`ements
- KEINE CREATE TABLE oder `stadtfahrradverleih_daten_2025.sql`fuer Abfragen und Tests
- Separate Datei von der Struktur

### D) Klassenarbeit-Aufgaben-Markdown (.md)
**Format:** `KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_aufg.md`
**Beispiel:** `KA02_2025_2026_VERSION1_aufg.md`

- KANummer: z.B. KA02 (`KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_aufg.md` (Berufsgymnasium Klasse 12)
- Schuljahr: z.B. 2025_2026 (v`KA02_2025_2026_VERSION1_aufg.md`ION1, VERSION2 etc.
- Suffix `_aufg`: kennzeichnet die Schuelerfassung (Aufgabenstellung + Artefakt-Hinweise, OHNE Lösung)
- Enthaelt: Aufgabenstellung, Arbeitsblatt-Hinweise, Artefakt-Verweise (mwb, PNG, SQL-Dumps)

### E) Klassen`_aufg`Loesung-Markdown (.md)
**Format:** `KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_lsg.md`
**Beispiel:** `KA02_2025_2026_VERSION1_lsg.md`

- Selbe Struktur wie `_aufg.md`, aber mit Suffix `_lsg`
- Enthaelt: Aufgabenstellung +`KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_lsg.md` Lehrkraftfassung (vertraulich)
- Dieselben Artefakt-Verw`KA02_2025_2026_VERSION1_lsg.md` Klassenarbeit-HTML-Export (.html)
**Format Au`_aufg.md``KA{KANummer}_`_lsg`ruppe}_{Schuljahr}_{Version}_aufg.html`
**Format Lösung:** `KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_lsg.html`

- Für jede KA-Markdown-Datei`_aufg`fg.md`, `*_lsg.md`) muss eine gleichnamige HTML-Datei existieren.
`KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_aufg.html`rkdown-Quelle im Verzeichnis liegen.
- Erzeugung über: `python sc`KA{KANummer}_{Zielgruppe}_{Schuljahr}_{Version}_lsg.html`axis:
1. Neuer Sachverhalt erstellen (z.B. `Fahrradvermietung`, `Kursplattfor`*_aufg.md`_PROTECT_20__schreiben -> speichern als `{System}_struktur_{Jahr}.sql`
3. SQL-Daten schreiben -> speichern als `{System}_daten_{Jahr}.sql`
4. In Workbench modellieren oder `python scripts/convert_ka_markdown.py`em}_{Jahr}.mwb`
5. PNG-Generator ausführen -> `{System}_{Jahr}.mwb` -> `{System}_{Jahr}.png`
6. `Fahrradvermietung`ritt-fü`Kursplattform`ellen -> `KA0x_{ZG}_{Jahr}_{Version}_aufg.md`
`{System}_struktur_{Jahr}.sql`ufgabe ableiten -> `KA0x_{ZG}_{Jahr}_{Version}_lsg.md`
8.`{System}_daten_{Jahr}.sql`- und Loesungsfassung erzeugen -> `KA0x_{ZG}_{Jahr}_{Version}_{aufg|lsg}.html`

`{System}_{Jahr}.mwb`idierungen:
- Generatoren pruefen auf ``{System}_{Jahr}.mwb`` + `*_date`{System}_{Jahr}.png` Validierungsskripte pruefen auf eindeutige Benennung innerha`KA0x_{ZG}_{Jahr}_{Version}_aufg.md`sionen für denselben Sachverhalt/Schuljahr werden gekennzeichnet

## Er`KA0x_{ZG}_{Jahr}_{Version}_lsg.md`n folgen Format `{Systemname}_{Jahr}.mwb`
- Alle SQL-Dumps liegen als Struktur+Daten-`KA0x_{ZG}_{Jahr}_{Version}_{aufg|lsg}.html`{System}_daten_{Jahr}.sql`
- Alle Klassenarbeits-Markdown-Dateien folgen `KA0x_{ZG}_{Jahr}_`*_struktur_{Jahr}.sql`- Alle Klass`*_daten_{Jahr}.sql`en folgen `KA0x_{ZG}_{Jahr}_{Version}_aufg/lsg.html`
- Im Verzeichnis `generated/klassenarbeiten` keine veralteten oder abweichenden Namensmuster mehr
- Pflicht-Gates laufen erfolgreich durch

## Fehlerbeh`.mwb`g
- Datei mit a`{Systemname}_{Jahr}.mwb`n: umbenennen oder loeschen
- Struktur und Daten ungekoppelt: als`{System}_struktur_{Jahr}.sql`utig: Version im Da`{System}_daten_{Jahr}.sql`- Markdown ohne HTML-Paar: `python scripts/convert_ka_markdo`KA0x_{ZG}_{Jahr}_{Version}_aufg/lsg.md`uelle: verwaiste HTML entfernen oder Quelle wiederherstellen

## LLM-`KA0x_{ZG}_{Jahr}_{Version}_aufg/lsg.html`ller neuen Artefakte in `generated/klassenarbe`generated/klassenarbeiten`tion: `.mwb`-Dateien als `{System}_{Jahr}.mwb`, SQL-Dumps immer als Struktur+Daten-Paar (`{System}_struktur_{Jahr}.sql` und `{System}_daten_{Jahr}.sql`), KA-Markdown-Dateien als `KA0x_{ZG}_{Schuljahr}_{Version}_aufg/lsg.md`, HTML-Dateien als `KA0x_{ZG}_{Schuljahr}_{Version}_aufg/lsg.html`. Im Verzeichnis gibt es keine Duplikate, kein`python scripts/convert_ka_markdown.py`ischten Dumpformate."

## Verknuepfungen
- [KF-ROUTINE-008-separater-sql-3nf-kontext.md](./KF-ROUTINE-008-separater-sql-3nf-kontext.md)
- [KF-ROUTINE-009-eerm-png-generator.md](./KF-ROUTINE-009-`generated/klassenarbeiten`./templates/KLASSENARBEIT-TEMPLATE-AUFGAB`.mwb`EFAKT`{System}_{Jahr}.mwb`/templates/KLASSENARBEIT-TEMPLATE-AUFGABEN-ARTEFAK`{System}_struktur_{Jahr}.sql`es/KLASSENARBEIT-TEMP`{System}_daten_{Jahr}.sql`ZONT-BPE6-BPE5.md](../../templates/KLASS`KA0x_{ZG}_{Schuljahr}_{Version}_aufg/lsg.md`BPE6-BPE5.md)

## Changelog
- 1.0 (11.05.2026): Be`KA0x_{ZG}_{Schuljahr}_{Version}_aufg/lsg.html`L-Dumps (Struktur+Daten), und KA-Markdown-Dateien.
- 1.1 (11.05.2026): HTML-Benennung und Pflicht-Paarung (MD/HTML) als verbindliche Regel ergaenzt.
