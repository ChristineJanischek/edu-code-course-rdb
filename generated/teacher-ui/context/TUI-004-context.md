# TUI-004 Kontextbezogene KI im Arbeitsfenster

Erstellt am (UTC): 2026-07-11T15:51:13Z

Quellen:

- Routing: generated/teacher-ui/routing/TUI-002-routing.md
- To-do: generated/teacher-ui/todos/TUI-003-todo.md

## Zusammenfassung

- Erkannte Anforderungen: 4
- Generierte To-do-Tasks: 4
- Ziel: KI-Hinweise direkt in bestehende Arbeitsfenster integrieren, ohne neue Hauptreiter einzufuehren.

## Kontext-KI-Zuordnung pro Arbeitsfenster

### Kurseditor > Planung

- KI-Aktion: Lernziel-Check und Themenreihenfolge-Hinweis
- Trigger: Bei Modulwechsel oder leerem Planungsfeld
- Ausgabe: Kurzvorschlag mit 1-3 konkreten naechsten Schritten

### Aufgabeneditor > Erstellung

- KI-Aktion: Aufgabendifferenzierung und Schwierigkeitsabgleich
- Trigger: Beim Speichern oder Check der Aufgabenformulierung
- Ausgabe: Hinweise zu Klarheit, Taxonomiestufe und moeglichen Hilfestellungen

### Abgaben > Rueckmeldung

- KI-Aktion: Feedback-Bausteine und Fehlercluster-Hinweise
- Trigger: Nach Bewertungseingabe oder bei haeufigen Fehlern
- Ausgabe: knappe Feedback-Optionen mit Lernfokus

## Usability-Regeln

1. Keine neue Hauptnavigation fuer einzelne KI-Funktionen.
2. KI-Ausgaben bleiben kompakt und kontextnah (maximal 5 Punkte).
3. Jede KI-Aktion hat klaren Trigger und sichtbare Rueckmeldung.
4. Lehrkraft kann Hinweise uebernehmen, anpassen oder verwerfen.

## UI-Smoke-Test-Checkliste

- [ ] Kurseditor zeigt Kontext-KI-Hinweis bei relevanten Planungsaktionen.
- [ ] Aufgabeneditor zeigt Differenzierungs-Hinweise ohne Layoutbruch.
- [ ] Abgabenbereich zeigt Feedback-Hilfen kontextbezogen.
- [ ] Bestehende Navigation bleibt unveraendert und uebersichtlich.
- [ ] Fehlerfall wird nutzerfreundlich angezeigt (ohne interne Details).

## Testvorschlaege

- Integrationstest: Pro Arbeitsfenster wird genau eine passende KI-Aktion angeboten.
- UI-Test: Kein neuer Hauptreiter entsteht durch TUI-004.
- Robustheitstest: Bei fehlenden Daten bleibt die Seite bedienbar und zeigt fallback-Hinweis.
