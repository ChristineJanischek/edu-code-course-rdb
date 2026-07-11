# TUI-003-M6 Automatische To-do-Generierung

Erstellt am (UTC): 2026-07-11T20:42:34Z

Quelle: /workspaces/edu-code-course-rdb/generated/teacher-ui/routing/TUI-002-M6-routing.md

## Priorisierte To-do-Eintraege

### Task 1

- Ausgangsanforderung: Titel: M6 Schulbetrieb-Features in Teilaufgaben Freitext: Wir wollen im nächsten Inkrement drei Schienen sauber trennen
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 2

- Ausgangsanforderung: Erstens Avatar und Voice als optionale Lehrkraftfunktionen mit klarer DSGVO-konformer Speicherung, Löschkonzept, Rollenrechten und Opt-in
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 3

- Ausgangsanforderung: Zweitens Governance für Prompt-, Wissens- und Modellupdates mit Vier-Augen-Freigabe, Versionierung, Rollback und Audit-Trail
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 4

- Ausgangsanforderung: Drittens Pilotbetrieb mit Feedbackzyklus über zwei Klassen, definierten Erfolgsmetriken, wöchentlichem Review und priorisierter Nachsteuerung
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 5

- Ausgangsanforderung: Prioritaet: Hoch Zielbereich: Core Betroffener Prozess: Schulbetrieb und Qualitätssteuerung Optionaler UI-Bereich: Lehrkraft-Dashboard, Kurseditor, Admin-Konsole
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

## Akzeptanzkriterien

1. Jede Routing-Anforderung erzeugt genau einen To-do-Eintrag.
2. Jeder To-do-Eintrag enthaelt Prioritaet, fachlichen Schritt, technischen Schritt und Testschritt.
3. Kritische Anforderungen werden vorrangig vor Mittel priorisiert.
4. Ausgabe ist als markdownbasiertes Artefakt versionierbar.

## Technische Teilaufgaben

- Parser fuer Routing-Textfelder
- Priorisierungsregel nach Schluesselbegriffen
- Ausgabe-Renderer fuer standardisierte Taskstruktur

## Testvorschlaege

- Vollstaendigkeitstest: Anzahl Tasks entspricht Anzahl Routing-Anforderungen.
- Priorisierungstest: To-do-bezogene Anforderungen werden als Kritisch markiert.
- Robustheitstest: Fehler bei leerem/ungueltigem Input wird sauber ausgegeben.
