# TUI-003 Automatische To-do-Generierung

Erstellt am (UTC): 2026-07-11T15:44:14Z

Quelle: generated/teacher-ui/routing/TUI-002-routing.md

## Priorisierte To-do-Eintraege

### Task 1

- Ausgangsanforderung: Lehrkraefte sollen Ideen per Sprache erfassen koennen
- Prioritaet: Hoch
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 2

- Ausgangsanforderung: Die Eingabe wird transkribiert, sprachlich bereinigt und in einzelne Anforderungen zerlegt
- Prioritaet: Hoch
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 3

- Ausgangsanforderung: Das System soll Zielgruppe, Prozess und passende UI-Zuordnung vorschlagen
- Prioritaet: Mittel
- Status: Offen
- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen
- Technischer Schritt: Controller/Service-Schnittstelle planen
- Testschritt: Routing + Ergebnisdarstellung pruefen

### Task 4

- Ausgangsanforderung: Danach soll automatisch eine priorisierte To-do-Liste mit Akzeptanzkriterien und technischen Aufgaben erzeugt werden
- Prioritaet: Kritisch
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
