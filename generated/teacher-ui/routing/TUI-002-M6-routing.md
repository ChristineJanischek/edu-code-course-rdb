# TUI-002-M6 Prozess- und UI-Zuordnung

Erstellt am (UTC): 2026-07-11T20:42:24Z

Quelle: /workspaces/edu-code-course-rdb/generated/teacher-ui/intake/TUI-001-M6-structured.md

## Routing-Ergebnis

### Anforderung 1

- Text: Titel: M6 Schulbetrieb-Features in Teilaufgaben Freitext: Wir wollen im nächsten Inkrement drei Schienen sauber trennen
- Prozess: Aufgabe erstellen
- UI-Hauptbereich: Aufgabeneditor > Erstellung
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 2

- Text: Erstens Avatar und Voice als optionale Lehrkraftfunktionen mit klarer DSGVO-konformer Speicherung, Löschkonzept, Rollenrechten und Opt-in
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 3

- Text: Zweitens Governance für Prompt-, Wissens- und Modellupdates mit Vier-Augen-Freigabe, Versionierung, Rollback und Audit-Trail
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 4

- Text: Drittens Pilotbetrieb mit Feedbackzyklus über zwei Klassen, definierten Erfolgsmetriken, wöchentlichem Review und priorisierter Nachsteuerung
- Prozess: Feedback geben
- UI-Hauptbereich: Abgaben > Rueckmeldung
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 5

- Text: Prioritaet: Hoch Zielbereich: Core Betroffener Prozess: Schulbetrieb und Qualitätssteuerung Optionaler UI-Bereich: Lehrkraft-Dashboard, Kurseditor, Admin-Konsole
- Prozess: Unterricht planen
- UI-Hauptbereich: Kurseditor > Planung
- Darstellungsform: Kontextdialog
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
