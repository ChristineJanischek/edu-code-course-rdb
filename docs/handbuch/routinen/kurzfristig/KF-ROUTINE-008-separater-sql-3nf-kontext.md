# KF-ROUTINE-008: Separater SQL-3NF-Kontext für Klassenarbeiten

## Metadata
- ID: KF-ROUTINE-008
- Kategorie: kurzfristig
- Status: aktiv
- Version: 1.0
- Gueltig ab: 10.05.2026
- Zielgruppe: Lehrkräfte und Autoren von Klassenarbeiten/Pruefungen

## Ziel
Sicherstellen, dass Modellierungsaufgaben (Teil B) und SQL-Abfragen (Teil C) didaktisch sauber getrennt sind. Teil C nutzt immer eine andere, bereits normalisierte 3NF-Datenbank mit eigenem Sachverhalt.

## Vorbedingungen
- Klassenarbeitsdatei basiert auf dem 60-Minuten-Template.
- Dateibenennung folgt dem KA-Schema im Verzeichnis generated/klassenarbeiten.

## Schritte
1. Teil-B-Kontext festlegen.
   - Sachverhalt für EERM-Modellierung formulieren.
   - Keine fertige Tabellenstruktur für Schüler ausgeben.
2. Teil-C-Kontext festlegen.
   - Andere Domaine als Teil B verwenden.
   - Konkreten Sachverhalt mit 5 bis maximal 6 Entitaetstypen und klaren Beziehungen definieren.
3. SQL-Datenbank in 3NF erstellen.
   - Struktur in eigener Datei dokumentieren: `{Systemname}_struktur_{Jahr}.sql`.
   - Daten in eigener Datei dokumentieren: `{Systemname}_daten_{`{Systemname}_daten_{Jahr}.sql`n mit ca. 20 Datensaetzen befuellen.
4. EERM für SQL-Kontext erstellen.
   - Datei: KAxx_..._SQLDB_EERM.mwb (Workbench-Modellcontainer).
   - In Workbench Modell-Notation auf "Connect to columns" setzen.
   - Wenn Workbench verfügbar: Grafik exportieren als KAxx_..._SQLDB_EERM.png.
5. Klassenarbeitsdokument aktualisieren.
   - Teil C explizit als separaten SQL-Kontext kennzeichnen.
   - SQL-Artefakte in der Abgabe auffuehren.
6. Qualitaetsgate ausführen.
   - bash scripts/validate-ka-separate-context.sh
   - bash scripts/validate-security.sh
   - bash scripts/validate-architecture.sh
   - bash scripts/validate-docs.sh

## Erfolgskriterien
- Teil B und Teil C sind unterschiedliche Kontexte.
- SQL-Teil C liegt getrennt vor als Struktur- und Daten-Datei.
- SQL-Struktur Teil C hat 5 bis maximal 6 Entitaetstypen.
- SQLDB-EERM (.mwb) ist ein natives Workbench-Modell (enthaelt `document.mwb.xml`, keine Platzhalterda`document.mwb.xml`ench verfügbar: SQLDB-EERM-Grafik (.png) vorhanden.
- KA-Markdown (`*_aufg.md`, `*_lsg.md`) haben jeweils einen`*_aufg.md``*_lsg.md`port.
- Pflicht-Gates laufen ohne Fehler durch.

## LLM-Prompt-Baustein (verbindlich)
Bei der Generierung von Klassenarbeiten/Pruefungen immer ergaenzen:

"Teil B (Modellierung) und Teil C (SQL) müssen unterschiedliche Kontexte verwenden. Teil C basiert auf einer separaten, in 3NF normalisierten Datenbank mit eigenem Sachverhalt. Erzeuge für Teil C immer getrennte SQL-Dateien für Struktur und Daten (`*_struktur_*.sql`, `*_daten_*.sql`), E`*_struktur_*.sql`n moegl`*_daten_*.sql`rafik (.png) mit Notation 'Connect to columns'."

## Changelog
- 1.0 (10.05.2026): Initiale Routine für didaktisch getrennten SQL-3NF-Kontext eingeführt.
