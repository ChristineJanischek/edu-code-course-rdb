# KF-ROUTINE-011: Drei-Versionen-Automatismus für Klassenarbeiten

## Metadata
- ID: KF-ROUTINE-011
- Kategorie: kurzfristig
- Status: aktiv
- Version: 1.0
- Gueltig ab: 11.05.2026
- Zielgruppe: Lehrkräfte und Autoren von Klassenarbeiten/Pruefungen
- Abhängigkeiten:
  - KF-ROUTINE-008-separater-sql-3nf-kontext.md
  - KF-ROUTINE-009-eerm-png-generator.md
  - KF-ROUTINE-010-datei-bezeichnungskonvention.md

## Ziel
Für jede Klassenarbeit werden immer drei Versionen gepflegt und erzeugt:
1. VERSION1 für den 1. Haupttermin
2. VERSION2 für den 2. Nachtermin
3. VERSION3 als Muster/Übung vorab

Alle Versionen haben denselben Erwartungshorizont (Punkte, Aufgabenstruktur, Zeitrahmen), aber unterschiedliche Aufgabenkontexte und unterschiedliche SQL-Datenquellen.

## Verbindliche Regeln
- Es existieren immer sechs Markdown-Dateien pro Set:
  - `..._VERSION1_aufg.md`, `..._VERS`..._VERSION1_lsg.md`_VERSION2_auf`..._VERSION2_aufg.md`sg.md`
  - `..._VERSION2_lsg.md``, `..._VERSI`..._VERSION3_aufg.md`ION ist der`..._VERSION3_lsg.md` (Teil B) unterschiedlich.
- Pro VERSION ist der SQL-Kontext (Teil C) unterschiedlich.
- Erwartungshorizont bleibt gleich:
  - Gesamtpunkte
  - Teilstruktur
  - Zeitbudget
  - Kompetenzniveau
- Zu jeder Markdown-Datei existiert eine gleichnamige HTML-Datei.

## Automatismus
Script:
- `scripts/generate-ka-varianten.sh`

Aufruf:
__PROTE`scripts/generate-ka-varianten.sh`VERSION1/2/3 in aufg+lsg vorhanden sind,
2. prueft, ob Modell- und SQL-Kontexte nicht doppelt verwendet werden,
3. erzeugt HTML-Exporte,
4. erzeugt/aktualisiert EERM-PNG-Artefakte.

## Erfolgskriterien
- Alle drei Versionen sind vorhanden und vollstaendig (aufg+lsg+html).
- Kontexte von VERSION1/2/3 sind nicht identisch.
- SQL-Artefakte folgen Struktur+Daten-Trennung.
- Pflicht-Gates laufen erfolgreich durch.

## LLM-Prompt-Baustein (verbindlich)
"Erzeuge für jede Klassenarbeit drei Versionen (VERSION1/2/3) mit identischem Erwartungshorizont, aber unterschiedlichen Sachverhalten und unterschiedlichen SQL-Kontexten. Nutze die Benennung nach KF-ROUTINE-010 und fuehre den Automatismus über `scripts/generate-ka-varianten.sh` aus."

## Verknuepfungen
- [KF-ROUTIN`scripts/generate-ka-varianten.sh`](./KF-ROUTINE-008-separater-sql-3nf-kontext.md)
- [KF-ROUTINE-009-eerm-png-generator.md](./KF-ROUTINE-009-eerm-png-generator.md)
- [KF-ROUTINE-010-datei-bezeichnungskonvention.md](./KF-ROUTINE-010-datei-bezeichnungskonvention.md)

## Changelog
- 1.0 (11.05.2026): Drei-Versionen-Automatismus für Haupttermin, Nachtermin und Musterfassung eingeführt.
