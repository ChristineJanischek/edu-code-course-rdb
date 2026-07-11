# Prozess: Teacher-UI Inhalts-Batches

Version: 1.0
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
