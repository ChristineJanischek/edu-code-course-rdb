# Teacher UI Master Backlog

Aktualisiert am (UTC): 2026-07-11T15:18:46Z

## Batches

- BATCH-001 (erstellt 20260711-151846)

## TUI-Eintraege aus BATCH-001

### TUI-001 Sprachaufnahme zu Struktur

- Prioritaet: Kritisch
- Zielbereich: Core
- Prozess: Unterricht planen, Material erstellen
- Status: In Umsetzung

Akzeptanzkriterien:

1. Spracheingabe wird in strukturierte Textform normalisiert.
2. Einzelanforderungen werden nachvollziehbar gelistet.
3. Zu jeder Intake-Ausfuehrung entsteht eine standardisierte To-do-Liste.
4. Akzeptanzkriterien und Testvorschlaege werden automatisch dokumentiert.

Technische Teilaufgaben:

- Intake-Skript bereitstellen: `scripts/teacher-ui-intake.sh`
- Ergebnisartefakt unter `generated/teacher-ui/intake/` erzeugen
- Prozessdokumentation fuer TUI-001 aktualisieren

Sinnvolle Tests:

- Parser-Test auf Fuellwoerter und Leerzeichen-Normalisierung
- Segmentierungs-Test fuer mehrere Einzelanforderungen
- Fehlerfall-Test fuer ungueltige Input-Datei

### TUI-002 Prozess- und UI-Zuordnung

- Prioritaet: Hoch
- Zielbereich: Core
- Prozess: Aufgabe erstellen, Aufgabe veroeffentlichen, Feedback geben
- Status: Idee erfasst

### TUI-003 To-do-Generierung je Funktionswunsch

- Prioritaet: Kritisch
- Zielbereich: Core
- Prozess: Backlog-Management, Release-Planung
- Status: Idee erfasst

### TUI-004 Kontextbezogene KI im Arbeitsfenster

- Prioritaet: Hoch
- Zielbereich: Course
- Prozess: Kurs verwalten, Aufgabe differenzieren, Bewertung vorbereiten
- Status: Idee erfasst

### TUI-005 Milestone-Tracking mit Triggerwort weiter

- Prioritaet: Hoch
- Zielbereich: Core
- Prozess: Entwicklungssteuerung, Qualitaetssicherung
- Status: In Umsetzung
