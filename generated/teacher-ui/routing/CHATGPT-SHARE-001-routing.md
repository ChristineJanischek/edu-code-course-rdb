# CHATGPT-SHARE-001 Prozess- und UI-Zuordnung

Erstellt am (UTC): 2026-07-13T11:27:07Z

Quelle: /workspaces/edu-code-course-rdb/generated/teacher-ui/intake/CHATGPT-SHARE-001-structured.md

## Routing-Ergebnis

### Anforderung 1

- Text: Quelle: ChatGPT - Automatisierte UI-Entwicklung
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Kontextdialog
- Prioritaet: Hoch

### Anforderung 2

- Text: Lehrkraefte sollen paedagogische Ideen, Aenderungswuensche und Funktionsvorschlaege frei per Text oder Sprache erfassen koennen
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Assistent
- Prioritaet: Hoch

### Anforderung 3

- Text: Das System soll die Eingaben automatisch sprachlich bereinigen, strukturieren, in Einzelanforderungen zerlegen, Beduerfnisse und Prozesse erkennen, geeignete Funktionalitaeten ableiten, UI-Bereiche pro Taetigkeit zuordnen, Module fuer Backend und Frontend planen, Meilensteine bestimmen, Tests festlegen und Wochenberichte mit aktuellem Stand, umgesetzten Modulen und naechsten logischen Schritten erzeugen
- Prozess: Kurs verwalten
- UI-Hauptbereich: Kursverwaltung > Uebersicht
- Darstellungsform: Assistent
- Prioritaet: Hoch

### Anforderung 4

- Text: Lehrplaene, Kompetenzziele, Differenzierung, Kursveroeffentlichung, Bewertungsraster, Musterloesungen und KI-Feedback muessen als wiederholbare Prozesskette beruecksichtigt werden
- Prozess: Feedback geben
- UI-Hauptbereich: Abgaben > Rueckmeldung
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
