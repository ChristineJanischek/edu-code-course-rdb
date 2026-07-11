# Analyse BATCH-001

Zeitpunkt (UTC): 2026-07-11T15:18:46Z

## Best Practice

- Jede Idee getrennt als eindeutige TUI-Anforderung fuehren.
- Vor Implementierung Dopplungen zu bestehender UI pruefen.
- UI-Entscheidungen nur nach Arbeitsprozess, nicht nach Technikmodul.
- Akzeptanzkriterien pro Anforderung vor Implementierung fixieren.

## Prozess

- Idee erfassen
- Zielgruppe und Prozess zuordnen
- UI-Platzierung bestimmen
- Akzeptanzkriterien formulieren
- technische Teilaufgaben priorisieren

## Batch-Aufspaltung in TUI-Eintraege

1. TUI-001 Sprachaufnahme zu Struktur
2. TUI-002 Prozess- und UI-Zuordnung
3. TUI-003 Automatische To-do-Generierung
4. TUI-004 Kontextbezogene KI in Arbeitsfenstern
5. TUI-005 Milestone-Tracking mit Triggerwort weiter

## Zuordnung

- Core: wiederverwendbare UI-Logik, Rollen, Berechtigungen, Konfigurationsassistenten.
- Course: kursbezogene Inhalte, aufgabennahe Assistenz, fachspezifische Defaults.

Konkrete Einstufung:

- Core: TUI-001, TUI-002, TUI-003, TUI-005
- Course: TUI-004

## Usability

- Erst in bestehende Reiter/Fenster integrieren.
- Neue Hauptreiter nur bei eigenstaendigem Arbeitsprozess.
- Maximal kurze Klickpfade fuer haeufige Aufgaben.

Konkrete UX-Leitlinien fuer diese Batch:

- Keine neue Hauptnavigation fuer Einzelaktionen.
- Analyse und Priorisierung in einem kompakten Backlog-Panel.
- Kontext-KI als Inline-Aktion neben bestehenden Formularfeldern.

## Meilensteinvorschlag

- Milestone A: TUI-003 + TUI-005 stabilisieren (Backlog und Steuerung)
- Milestone B: TUI-001 + TUI-002 integrieren (Aufnahme und Zuordnung)
- Milestone C: TUI-004 in Course-Views einbetten

## Sinnvolle Tests

- Parser-Test: Spracheingabe mit Fuellwoertern wird in klare Anforderungen zerlegt.
- Routing-Test: Idee wird dem richtigen Prozess und UI-Bereich zugeordnet.
- Backlog-Test: To-do-Generierung liefert Prioritaet, Akzeptanzkriterien, Teilaufgaben.
- Integrationstest: Triggerwort weiter aktualisiert Statusbericht ohne Nebenwirkungen.
- UI-Test: Kontext-KI erscheint nur in passenden Course-Ansichten.

## Nächster Schritt

- Batch in einzelne TUI-Backlogeintraege ueberfuehren und mit Status Idee erfasst markieren.
