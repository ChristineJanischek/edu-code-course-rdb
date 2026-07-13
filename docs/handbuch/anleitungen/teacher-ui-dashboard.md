# Anleitung: Teacher-UI Dashboard

**Zielpublikum:** Lehrkräfte, Didaktiker, Kursplaner

**Dauer:** 5 Min Einrichtung + beliebig lange Nutzung

---

## Übersicht

Das **Teacher-UI Dashboard** (`webapp/public/teacher-ui.php`) ist eine dedizierte Web-Seite für Lehrkräfte zur Verwaltung und Überwachung von Modulplanung, Lernzielen, Unterrichtsmodulen und Curriculum-Mapping – völlig unabhängig vom Schülerzugang.

**Wichtig:** Der Schülerzugang (`index.php` auf Port 8080) bleibt unverändert und wird nicht beeinflusst.

---

## Schnellstart

### 1. Webserver starten

```bash
bash scripts/start-services.sh
```

Dies startet:
- PHP-Webserver auf `http://localhost:8080`
- MySQL-Datenbank für die Wissensdatenbank
- Python-API auf `http://localhost:8000` (optional)

### 2. Teacher-UI Dashboard öffnen

Öffne im Browser:

```
http://localhost:8080/teacher-ui.php
```

---

## Funktionsbereiche

Das Dashboard ist in 6 Haupt-Sektionen unterteilt, erreichbar über die Navigationsleiste oben:

### 1. **Strategie** (`#strategie`)
- Importierte externe Quelle (z.B. ChatGPT Share)
- Beschreibung der übergeordneten Philosophie
- Gesamtliste der identifizierten Bedürfnisse

Basis: `webapp/public/data/teacher-ui-module-plan.json` → `meta.source` + `needs`

### 2. **Lehrplan-Mapping** (`#curriculum`)
- Curriculum-Empfehlungen pro Lehrplan-Kontext
- Fachliche Ziele und Kompetenzen aus dem Normallehrplan
- Didaktische Ableitungen pro Empfehlung

Basis: `webapp/public/data/teacher-ui-module-plan.json` → `curriculum_recommendations`

### 3. **Prozesse & Module** (`#prozesse`)
- 6 übergeordnete Prozess-Lanes (z.B. "Modellierung", "Didaktik", "Differenzierung")
- Module pro Lane mit Status (geplant, implementiert)
- Zuordnung zu Meilensteinen

Basis: `webapp/public/data/teacher-ui-module-plan.json` → `modules` (gruppiert nach `process`)

### 4. **Meilensteine** (`#meilensteine`)
- Status-Übersicht (MS-01, MS-02, MS-03, …)
- Implementierte und geplante Features pro Meilenstein
- Abhängigkeiten zwischen Meilensteinen

Basis: `webapp/public/data/teacher-ui-module-plan.json` → `milestones`

### 5. **Wochenbericht** (`#wochenbericht`)
- Wöchentliche Zusammenfassung
- Diese Woche implementierte Module
- Nächste Schritte für nächste Woche
- Aktualisiert automatisch durch `bash scripts/weiter.sh`

Basis: `webapp/public/data/teacher-ui-module-plan.json` → `weekly_report`

### 6. **Generierte Unterrichtsmodule** (`#unterrichtsmodule`)
- Strukturierte Lernmodule mit:
  - **Lernziele:** fachlich präzisierte Kompetenzen
  - **Aufgaben:** concretisiert aus Content-DB
  - **Bewertungskriterien:** Qualitäts-Rubric mit fachlichen Standards
  - **Lernhilfen:** Context-spezifische Lernhilfen
- Sortiert nach Schwierigkeitsgrad (leicht, mittel, schwer)

Basis: `webapp/public/data/teaching-modules.json` → `modules`

---

## Datenquellen

Das Dashboard lädt Daten aus zwei JSON-Dateien, die über die `TeacherUiModulePlanRepository` und `TeachingModuleRepository` PHP-Klassen bereitgestellt werden:

| Datei | Quelle | Generator | Zweck |
|-------|--------|-----------|-------|
| `webapp/public/data/teacher-ui-module-plan.json` | ChatGPT Share URL | `python3 scripts/import_teacher_ui_share.py <url>` | Strategie, Curriculum-Mapping, Module, Meilensteine |
| `webapp/public/data/teaching-modules.json` | Content-DB + Curriculum | `python3 scripts/generate_teaching_module.py` | Generierte Unterrichtsmodule (Lernziele, Aufgaben, Bewertung) |

---

## Externe Quelle importieren (ChatGPT Share)

### Vollständig neuen Modulplan importieren

```bash
python3 scripts/import_teacher_ui_share.py https://chatgpt.com/share/<SHARE_ID>
```

Dies:
1. Parst die ChatGPT-Share-URL
2. Extrahiert alle Nachrichten aus dem Chatverlauf
3. Strukturiert: Strategie, Bedürfnisse, Curriculum-Empfehlungen, Module, Meilensteine, Wochenbericht
4. Speichert in `webapp/public/data/teacher-ui-module-plan.json`
5. Dashboard lädt automatisch die neuen Daten nach Browser-Refresh

### Nach Import: Module generieren

```bash
python3 scripts/generate_teaching_module.py
```

Dies erzeugt strukturierte Unterrichtsmodule basierend auf:
- Tasks aus `data/content-db/tasks.json`
- Kontexten aus `data/content-db/contexts.json`
- Curriculum-Empfehlungen aus dem gerade importierten Plan

---

## Integration mit Student Portal (index.php)

Das **Teacher-UI Dashboard** ist völlig unabhängig, nutzt aber die gleichen Daten:

| Bereich | index.php | teacher-ui.php | Gemeinsame Basis |
|---------|-----------|----------------|-----------------|
| Strategie | Info-Panel (oben) | Vollständige Seite | `teacher-ui-module-plan.json` |
| Curriculum | Kurze Box | 6-Lane-Grid | `teacher-ui-module-plan.json` |
| Module | Integrated im Workflow | Dedizierte Karten-Grid | `teaching-modules.json` |

**→ Lehrkräfte können im teacher-ui.php planen, Schüler sehen die Ergebnisse passiv in index.php**

---

## Automatische wöchentliche Aktualisierung

Das System aktualisiert den Wochenbericht automatisch jeden **Montag um 06:00 UTC** via GitHub Actions (`.github/workflows/weekly-report.yml`):

```bash
# Ausgelöst automatisch oder manuell:
workflow_dispatch  # In GitHub Actions manuell starten
# oder: Cron Montags 06:00 UTC
```

Dies führt aus:
1. `python3 scripts/generate_teaching_module.py` – Neueste Module generieren
2. `bash scripts/generate-content-catalog.sh` – Content-DB aktualisieren
3. `bash scripts/weiter.sh` – Nächste Schritte ableiten
4. `bash scripts/sync-generated-html.sh --write` – Artefakte synchronisieren
5. Commit & Push von Änderungen

---

## Fehlerbehandlung

### "Noch keine externe Quelle importiert"
**Ursache:** `teacher-ui-module-plan.json` enthält `meta.source_connected=false`

**Lösung:**
```bash
python3 scripts/import_teacher_ui_share.py <SHARE_URL>
bash scripts/generate_teaching_module.py
```

### Leere Modul-Liste
**Ursache:** `teaching-modules.json` existiert nicht oder ist leer

**Lösung:**
```bash
python3 scripts/generate_teaching_module.py
```

### Daten nicht aktuell
**Lösung:** Browser-Cache leeren (Ctrl+Shift+Del) und Seite neu laden

---

## Technische Details

### Dateien

- **Seite:** `webapp/public/teacher-ui.php` (450+ Zeilen PHP)
- **Repositories:** `webapp/app/Repository/TeacherUiModulePlanRepository.php`, `webapp/app/Repository/TeachingModuleRepository.php`
- **Styling:** `webapp/public/style.css` (gemeinsam mit index.php)
- **Datenquellen:** `webapp/public/data/teacher-ui-module-plan.json`, `webapp/public/data/teaching-modules.json`

### Sicherheit

- Alle Benutzerdaten werden mit `htmlspecialchars(..., ENT_QUOTES, 'UTF-8')` escaped
- Keine SQL-Injection möglich (nur JSON-Dateien, keine DB-Abfragen)
- Keine Secrets im Code oder in JSON-Dateien

### Performance

- Statische JSON-Datei-Ladevorgänge (kein API-Overhead)
- Responsive CSS für Desktop und Tablet
- Keine JavaScript-Framework-Abhängigkeit

---

## Version

- **v1.0:** (13.07.2026) – Initial Release der Teacher-UI Dashboard-Seite
