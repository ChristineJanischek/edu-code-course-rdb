# Prozess: Teacher-UI Inhalts-Batches

Version: 1.2
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

## Changelog

- v1.0 (11.07.2026): Initiale Batch-Routine fuer Teacher-UI-Anforderungen.
- v1.1 (11.07.2026): TUI-001-Inkrement mit Intake-Skript fuer Sprach-zu-Struktur-Analyse ergaenzt.
- v1.2 (11.07.2026): TUI-002-Inkrement mit Routing-Skript fuer Prozess- und UI-Zuordnung ergaenzt.
