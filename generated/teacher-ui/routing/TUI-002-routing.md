# TUI-002 Prozess- und UI-Zuordnung

Erstellt am (UTC): 2026-07-11T15:42:01Z

Quelle: generated/teacher-ui/intake/TUI-001-structured.md

## Routing-Ergebnis

### Anforderung 1

- Text: Lehrkraefte sollen Ideen per Sprache erfassen koennen
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Assistent
- Prioritaet: Hoch

### Anforderung 2

- Text: Die Eingabe wird transkribiert, sprachlich bereinigt und in einzelne Anforderungen zerlegt
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Assistent
- Prioritaet: Hoch

### Anforderung 3

- Text: Das System soll Zielgruppe, Prozess und passende UI-Zuordnung vorschlagen
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 4

- Text: Danach soll automatisch eine priorisierte To-do-Liste mit Akzeptanzkriterien und technischen Aufgaben erzeugt werden
- Prozess: Aufgabe erstellen
- UI-Hauptbereich: Aufgabeneditor > Erstellung
- Darstellungsform: Seitenleiste
- Prioritaet: Hoch

## Routing-Qualitaetskriterien

1. Jede Anforderung enthaelt Prozesszuordnung.
2. Jede Anforderung enthaelt UI-Hauptbereich und Darstellungsform.
3. Zuordnung folgt Prozess statt Technikmodul.
4. Haeufige Funktionen landen in schnell erreichbaren Bereichen.

## Testvorschlaege

- Mapping-Test: Prozesszuordnung fuer typische Lehreraufgaben.
- UI-Zuordnungstest: Hauptbereich bleibt stabil bei Synonymen.
- Robustheitstest: Eingaben ohne Prozesswoerter fallen auf Default-Kursverwaltung.
