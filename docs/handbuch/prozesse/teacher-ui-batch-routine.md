# Prozess: Teacher-UI Inhalts-Batches

Version: 1.5
Status: Aktiv
Gueltig ab: 11.07.2026

---

## Ziel

Sprach- oder Textideen in strukturierte, priorisierte und umsetzbare Teacher-UI-Anforderungen ueberfuehren.

---

## Eingabeformat je Idee

1. Titel
2. Freitext oder Sprachtranskript
3. Prioritaet (Kritisch/Hoch/Mittel/Niedrig)
4. Zielbereich (Core/Course/Unklar)
5. Betroffener Prozess
6. Optionaler UI-Bereich

---

## Ausfuehrung

```bash
bash scripts/teacher-ui-batch.sh BATCH-001
```

Erzeugte Artefakte:

- `generated/teacher-ui/batches/BATCH-001.md`
- `generated/teacher-ui/analysen/BATCH-001-analyse.md`
- `generated/teacher-ui/backlog/TEACHER_UI_MASTER_BACKLOG.md`

---

## TUI-001 Implementierungsinkrement (Sprachaufnahme zu Struktur)

Ausfuehrung:

```bash
bash scripts/teacher-ui-intake.sh --id TUI-001
```

Optional mit eigener Spracheingabe-Datei:

```bash
bash scripts/teacher-ui-intake.sh --id TUI-001 --input /pfad/zum/transkript.txt
```

Ergebnisdatei:

- `generated/teacher-ui/intake/TUI-001-structured.md`

Inhalt der Ergebnisdatei:

- normalisierte Eingabe
- erkannte Einzelanforderungen
- standardisierte To-do-Liste
- Akzeptanzkriterien
- Testvorschlaege

---

## TUI-002 Implementierungsinkrement (Prozess- und UI-Zuordnung)

Ausfuehrung:

```bash
bash scripts/teacher-ui-routing.sh --id TUI-002
```

Optional mit expliziter Eingabe:

```bash
bash scripts/teacher-ui-routing.sh --id TUI-002 --input generated/teacher-ui/intake/TUI-001-structured.md
```

Ergebnisdatei:

- `generated/teacher-ui/routing/TUI-002-routing.md`

Inhalt der Ergebnisdatei:

- Anforderungsbezogene Prozesszuordnung
- UI-Hauptbereichszuordnung
- Darstellungsform (Assistent, Seitenleiste, Kontextdialog)
- Routing-Qualitaetskriterien
- Testvorschlaege

---

## TUI-003 Implementierungsinkrement (To-do-Generierung je Funktionswunsch)

Ausfuehrung:

```bash
bash scripts/teacher-ui-todo.sh --id TUI-003
```

Optional mit expliziter Eingabe:

```bash
bash scripts/teacher-ui-todo.sh --id TUI-003 --input generated/teacher-ui/routing/TUI-002-routing.md
```

Ergebnisdatei:

- `generated/teacher-ui/todos/TUI-003-todo.md`

Inhalt der Ergebnisdatei:

- priorisierte To-do-Eintraege je Ausgangsanforderung
- Akzeptanzkriterien
- technische Teilaufgaben
- Testvorschlaege

---

## TUI-004 Implementierungsinkrement (Kontextbezogene KI im Arbeitsfenster)

Ausfuehrung:

```bash
bash scripts/teacher-ui-context.sh --id TUI-004
```

Optional mit expliziten Quellen:

```bash
bash scripts/teacher-ui-context.sh --id TUI-004 --routing generated/teacher-ui/routing/TUI-002-routing.md --todo generated/teacher-ui/todos/TUI-003-todo.md
```

Ergebnisdatei:

- `generated/teacher-ui/context/TUI-004-context.md`

Inhalt der Ergebnisdatei:

- Kontext-KI-Zuordnung pro Arbeitsfenster
- Usability-Regeln ohne neue Hauptnavigation
- UI-Smoke-Test-Checkliste
- Testvorschlaege fuer Integration und Robustheit

---

## TUI-005 Implementierungsinkrement (Milestone-Tracking mit Triggerwort weiter)

Ausfuehrung:

```bash
bash scripts/teacher-ui-milestone.sh --id TUI-005
```

Ergebnisdatei:

- `generated/teacher-ui/milestones/TUI-005-milestone.md`

Inhalt der Ergebnisdatei:

- Acceptance-Check fuer den weiter-Trigger
- naechster Milestone aus dem aktuellen Statusreport
- Regressionstestpfad fuer die komplette TUI-Kette (001 bis 005)
- Konsolidierungsregeln fuer reproduzierbare Laeufe

---

## Analysekriterien

### Best Practice

- Keine Direktimplementierung aus Rohideen.
- Jede Anforderung mit Akzeptanzkriterien und Abhaengigkeiten versehen.

### Prozess

- Zuordnung zu einem klaren Lehrerprozess.
- Priorisierung nach Nutzen, Haeufigkeit, Risiko und Abhaengigkeiten.

### Zuordnung

- Core: wiederverwendbare UI-Komponenten, Rollenmodell, Assistenten-Framework.
- Course: kurs- und fachspezifische Inhalte, Eingabemasken, Lernpfadlogik.

### Usability

- Reiter/Fenster nur bei echtem Bedarf erweitern.
- Hohe Frequenzfunktionen in 1-2 Interaktionen erreichbar halten.

---

## Definition of Done je Batch

- Batch-Datei angelegt
- Analyse-Datei angelegt
- Master-Backlog aktualisiert
- `bash scripts/weiter.sh` ausgefuehrt
- Pflicht-Gates vor Abschluss erfolgreich

---

## Externe ChatGPT-Share-Quelle andocken

Wenn eine externe ChatGPT-Share-Konversation als Strategie- oder Ideenquelle fuer Teacher-UI, Kurseditor oder Modulplanung genutzt werden soll, kann sie direkt in die bestehende TUI-Kette importiert werden.

Ausfuehrung:

```bash
python3 scripts/import_teacher_ui_share.py <share-url>
```

Wirkung:

- importiert die Share-Quelle als versioniertes Artefakt unter `generated/teacher-ui/sources/`
- erzeugt ein Batch-Input unter `generated/teacher-ui/batches/`
- fuehrt Intake, Routing, To-do, Kontext und Milestone fuer die Quelle aus
- schreibt einen strukturierten Modulplan nach `webapp/public/data/teacher-ui-module-plan.json`
- erzeugt einen Wochenbericht unter `generated/teacher-ui/reports/`

Ziel:

- Ideen/Vorgaenge/Beduerfnisse aus der Quelle reproduzierbar sichern
- daraus Module, Tests und Meilensteine ableiten
- den aktuellen Entwicklungsplan direkt im Web-Frontend sichtbar machen

---

## Changelog

- v1.0 (11.07.2026): Initiale Batch-Routine fuer Teacher-UI-Anforderungen.
- v1.1 (11.07.2026): TUI-001-Inkrement mit Intake-Skript fuer Sprach-zu-Struktur-Analyse ergaenzt.
- v1.2 (11.07.2026): TUI-002-Inkrement mit Routing-Skript fuer Prozess- und UI-Zuordnung ergaenzt.
- v1.3 (11.07.2026): TUI-003-Inkrement mit To-do-Generator fuer priorisierte Taskableitung ergaenzt.
- v1.4 (11.07.2026): TUI-004-Inkrement mit Kontext-KI-Zuordnung und UI-Smoke-Checkliste ergaenzt.
- v1.5 (11.07.2026): TUI-005-Inkrement mit Milestone-Konsolidierung, Acceptance-Check und Regressionstestpfad ergaenzt.
