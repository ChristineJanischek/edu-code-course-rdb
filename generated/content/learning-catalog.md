# Learning Content Catalog

Diese Datei wird aus der normalisierten JSON-Datenbank unter data/content-db erzeugt.

- Kontextanzahl: 4
- Themenanzahl: 6
- Stichwortanzahl: 7

## CTX-EERM: EERM und Modellierung

Kontext fuer Entitaeten, Beziehungen, Kardinalitaeten und Schluessel.

- Zeithorizont: kurzfristig
- Dokumente: 1
- Aufgaben: 2

### Dokumente

- Normalisierung bis 3NF (generated) -> generated/informationen/teil-b/03_normalisierung_bis_3nf.md | Themen: TOP-3NF, TOP-EERM

### Aufgaben und Loesungen

- Aufgabe: Kontext in EERM ueberfuehren (mittel)
  - Prompt: Extrahiere Entitaeten, Attribute und Beziehungen aus dem Fachtext und begruende die Kardinalitaeten.
  - Themen: TOP-EERM, TOP-CARD
  - Stichworte: EERM, Redundanz
  - Loesung 1.0: generated/klassenarbeiten/KA02_2025_2026_VERSION1_lsg.md
- Aufgabe: Bis 3NF normalisieren (hoch)
  - Prompt: Fuehre ein Tabellenmodell in die 3. Normalform ueber und dokumentiere die aufgeloesten Abhaengigkeiten.
  - Themen: TOP-3NF
  - Stichworte: 3NF, Redundanz
  - Loesung 1.0: generated/informationen/teil-b/03_normalisierung_bis_3nf.md

## CTX-GOV: Governance und Dokumentation

Kontext fuer Architektur, Prozesse, Redundanzmanagement und Qualitaetsgates.

- Zeithorizont: langfristig
- Dokumente: 2
- Aufgaben: 0

### Dokumente

- Architektur (handbuch) -> docs/handbuch/ARCHITEKTUR.md | Themen: TOP-GOV
- Redundanz-Management (handbuch) -> docs/handbuch/prozesse/redundanz-management.md | Themen: TOP-GOV

## CTX-KA: Klassenarbeit und Pruefungsartefakte

Kontext fuer Aufgaben, Loesungen, SQL-Dumps und Modellgrafiken.

- Zeithorizont: mittelfristig
- Dokumente: 2
- Aufgaben: 0

### Dokumente

- KA02 VERSION1 Aufgabenstellung (generated) -> generated/klassenarbeiten/KA02_2025_2026_VERSION1_aufg.md | Themen: TOP-EERM, TOP-JOIN
- KA02 VERSION1 Loesung (generated) -> generated/klassenarbeiten/KA02_2025_2026_VERSION1_lsg.md | Themen: TOP-3NF, TOP-GROUP

## CTX-SQL: SQL und Abfragekompetenz

Kontext fuer JOIN, Projektion, Selektion, Gruppierung und Auswertung.

- Zeithorizont: kurzfristig
- Dokumente: 1
- Aufgaben: 1

### Dokumente

- SQL ueber mehrere Tabellen (generated) -> generated/informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.md | Themen: TOP-JOIN, TOP-GROUP

### Aufgaben und Loesungen

- Aufgabe: Buchungen pro Raum zaehlen (mittel)
  - Prompt: Schreibe eine SQL-Abfrage mit JOIN und GROUP BY, die Buchungen je Raum ausgibt.
  - Themen: TOP-JOIN, TOP-GROUP
  - Stichworte: JOIN, GROUP BY
  - Loesung 1.0: generated/informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.md
