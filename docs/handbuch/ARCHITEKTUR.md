# ARCHITEKTUR: Lernroutinen-Wissensdatenbank

**Dokumentversion:** 1.1
**Datum:** 25. März 2026

---

## 1. Systemüberblick

Das Lernroutinen-System ist eine dokumentenbasierte Wissensdatenbank, die Lernprozesse in strukturierter Form erfasst, organisiert und wartbar hält.

### Kernprinzipien
- **Single Source of Truth (SSOT):** Jede Routine existiert in genau einer Datei
- **DRY (Don't Repeat Yourself):** Wiederverwendbare Templates und Komponenten
- **Git-First:** Vollständige Versionskontrolle und Audit-Trail
- **Markdown-basiert:** Einfach zu lesen, einfach zu versionieren
- **Hierarchisch:** Klare Struktur nach Zeit und Kategorie

---

## 2. Komponenten

### 2.1 Routinen-Struktur

Jede Routine folgt diesem Format:

```markdown
# [ROUTINE-ID]: [NAME]

## Metadata
- **ID:** ROUTINE-001
- **Kategorie:** kurzfristig/mittelfristig/langfristig
- **Häufigkeit:** täglich/wöchentlich/monatlich/jährlich
- **Zeitaufwand:** X Minuten/Stunden
- **Verantwortlicher:** Person/Team
- **Abhängigkeiten:** [Liste von anderen Routinen]
- **Version:** 1.0
- **Letzte Aktualisierung:** Datum

## Ziel
Prägnante Beschreibung, was diese Routine erreichen soll.

## Vorbedingungen
Was muss vorhanden sein, bevor diese Routine durchgeführt wird?

## Schritte
1. **Schritt 1:** Beschreibung
2. **Schritt 2:** Beschreibung
3. ...

## Erfolgskriterien
- Kriterium 1
- Kriterium 2

## Fehlerbehandlung
Wie werden Fehler behandelt?

## Ausgaben/Ergebnisse
Was ist das Ergebnis dieser Routine?

## Verknüpfungen
- 🔗 [verknüpfte Routine 1](link)
- 🔗 [verknüpfte Routine 2](link)

## Changelog
- v1.0 (Datum): Initiale Version
- v1.1 (Datum): [Änderungen]
```

### 2.2 Template-System

**Zweck:** Konsistenz und Wiederverwendbarkeit sicherstellen

**Verwaltung:**
- Master-Template in `templates/routine-template.md`
- Beispiel-Implementierung in `templates/beispiel-routine.md`
- Spezialvorlagen für unterschiedliche Routine-Typen (Code, Prozess, Analyse)

### 2.3 Kategorisierung nach Zeithorizont

```
KURZFRISTIG (täglich/wöchentlich)
  ├── Daily Routines (Morgens/Abends)
  ├── Weekly Reviews
  └── Incident Response

MITTELFRISTIG (monatlich/quartalsweise)
  ├── Monatliche Reviews
  ├── Optimierungszyklen
  └── Trainings- und Lern-Sprints

LANGFRISTIG (jährlich/strategisch)
  ├── Strategische Planung
  ├── Architektur-Reviews
  └── Jahresberichte
```

### 2.4 RDB-Lernplattform und Teststack

Fuer dieses Repository ist die fachliche Domäne strikt auf relationale Datenbanken begrenzt. Daraus ergibt sich ein technischer Kernstack mit klarer Verantwortungstrennung:

- **Uploads:** `uploads/lehrplaene/` fuer curriculare Primärquellen, `uploads/pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/` fuer Prüfungsreferenzen und Analysegrundlagen, `uploads/klassenarbeiten-und-unterrichtsmaterialien/` fuer Archivmaterial.
- **Webapp:** PHP-Frontend mit didaktischen Lernpfaden, Info-Boxen, Code-Inboxen und Selbstkontrolle.
- **Python-API:** Zentrale Service-Schicht für strukturierte Datenlieferung und spätere Analyse-/Generierungsfunktionen.
- **MySQL:** Ausführungs- und Testumgebung für 3NF-Strukturen, Abfragen, Referenzdaten und fachliche Validierung.
- **Docker Compose:** Reproduzierbarer Live-Test für Schulen, Lehrkräfte und lokale Entwicklungsumgebungen.

Architekturregel fuer Interaktivitaet und API-Implementierung:

- **Frontend-Bootstrap:** `webapp/public/app.js` und `webapp/public/js/main.mjs` enthalten nur Initialisierung.
- **Portal-Modulwahl:** In `webapp/public/index.php` wird die Übungsmodul-Auswahl (UE01/UE02) als Dropdown geführt; die Link- und Ladelogik wird über den Workflow-Controller (`webapp/public/js/controllers/course-workflow.controller.mjs`) synchronisiert.
- **Integrierter Modulmodus:** Aufgaben aus `generated/uebungen/UE01_*` und `generated/uebungen/UE02_*` werden im Portal linear (1 bis 14) verarbeitet: Aufgabenstellung links, SQL-Editor rechts, Test-/Hint-/Musterloesung-/Ergebnisfluss im Footer-Assistenten.
- **Frontend-MVC:** Fachlogik in `webapp/public/js/models/`, DOM-Darstellung in `webapp/public/js/views/`, Steuerlogik in `webapp/public/js/controllers/`.
- **Python-API-Bootstrap:** `services/python-api/app.py` bleibt schlanker Einstiegspunkt.
- **Python-API-Schichten:** Routing/Controller in `services/python-api/learning_api/routes.py`, Services in `services/python-api/learning_api/*_service.py`, DB/Repository-nahe Logik in `services/python-api/learning_api/db.py`.

Devcontainer- und Port-Richtlinie für lokale Nutzung:

- **Webapp-Port 8080:** wird beim Start automatisch im Browser geöffnet (`onAutoForward=openBrowser`) und als öffentlich sichtbar markiert (`visibility=public`), damit Unterrichts-Demos ohne zusätzliche VS-Code-Klickpfade starten.
- **Python-API-Port 8000:** bleibt auf stille Weiterleitung (`onAutoForward=silent`), ist aber ebenfalls öffentlich sichtbar (`visibility=public`), damit externe Aufrufer und Integrations-Tests konsistent erreichbar bleiben.

---

## 3. Prozess-Schichten

### Layer 1: Definition (Templates)
- Standard-Format für alle Routinen
- Konsistente Metadaten
- Versionierung von Anfang an

### Layer 2: Dokumentation (Markdown)
- Menschlich lesbar
- Git-versionierbar
- Suchbar und linkbar

### Layer 3: Verwaltung (Git)
- Änderungshistorie
- Branching für Entwicklung
- Pull-Request-Review-Prozess

### Layer 4: Governance (Prozesse)
- Neue-Routine-Prozess
- Review und Genehmigung
- Redundanz-Management
- Qualitaets-Gates-Automatisierung
- Audit und Compliance

---

## 4. Redundanz-Management

### Ziel
Sicherstellen, dass keine doppelten oder überlappenden Routinen existieren.

### Strategien

**A. Verhinderung**
- Template erzwingt Eindeutigkeit (ID, Name)
- Review-Prozess prüft auf Redundanzen
- Dependency-Matrix zeigt Beziehungen

**B. Erkennung**
- Monatliche Redundanz-Audits
- Automated Checks (Skripts)
- Manuelle Konsolidierungsanalyse

**C. Elimination**
- Merge-Decision-Prozess
- Rerouting von Abhängigkeiten
- Changelog mit Begründung
- Deprecation-Phase für alte Routinen

### Redundanz-Index

```yaml
# redundanz-matrix.yaml
routine_001:
  ähnlich_zuWie:
    - routine_005 (95% Überlappung)
    - routine_012 (40% Überlappung)
  status: "zu prüfen"
  empfehlung: "mit 005 zusammenführen"
```

---

## 5. Erweiterungspunkte

Das System ist für folgende Erweiterungen ausgelegt:

### 5.1 Kurz- und Mittelfristig
- [x] README mit Quick-Start-Guide
- [x] Index/Übersichtsseite aller Routinen
- [ ] Automatische Inhaltsverzeichnisse
- [ ] Tag-basierte Filterung
- [ ] Abhängigkeitsvisualisierung

### 5.2 Mittelfristig
- [x] Automatisierte Validierung (Linting)
- [ ] Automatisierte Redundanz-Erkennung
- [ ] Dashboards für Ziele/KPIs
- [ ] Automatisierte Test-Routinen
- [ ] Integration mit Projektmanagement-Tools
- [ ] Curriculare Upload-Analyse fuer neue Lehrplaene und Ableitung neuer RDB-Lernpfade

### 5.3 Langfristig
- [ ] Workflow-Automation (z.B. Automatische Erinnerungen)
- [ ] Datenbank-Migrations-Pfad
- [ ] API-Zugang zu Routinen
- [ ] Retrieval-gestuetzte Lehrplananalyse mit mehrsprachigen Embeddings und didaktischem Regelwerk
- [ ] Intelligente Routine-Vorschläge

---

## 6. Sicherheit & Governance

### 6.1 Zugriffskontrolle

```
Git Repository Level:
├── main branch
│   └── Nach Approval mergen (geschützt)
├── develop branch
│   └── Feature Branches + PRs
└── feature/* branches
    └── Frei für Entwickler
```

### 6.2 Audit Trail

Alle Änderungen werden protokolliert durch:
- Git Commit-History
- Changelog in jeder Routine
- PR-Review-Kommentare
- Automatisierte Logs

### 6.3 Backup & Recovery

- Automatische Git-Backups
- Regelmäßige Snapshots
- Konflikt-Auflösungs-Verfahren

### 6.4 Template-Synchronisation

Dieses Repository wird auch als Template für Student-Repositories verwendet. Dafür gilt:

- Änderungen in `generated/uebungen/` und den übrigen verfolgten Template-Dateien sind Teil der Versionierung und werden mit dem nächsten Sync verteilt.
- Der Workflow `.github/workflows/template-sync-pr.yml` prüft regelmäßig das Upstream-Repository.
- Bei konfliktfreien Änderungen wird direkt auf `main` gepusht; wenn Branch-Schutzregeln das verhindern, wird automatisch ein Pull Request erstellt.

### 6.5 Auslieferung generierter Inhalte

- Die Web-App liest Übungen, Klassenarbeiten und Hilfsmittel aus der gemeinsamen `generated/`-Quelle.
- Im Container wird der Pfad explizit über `GENERATED_BASE_PATH=/var/www/html/generated` gesetzt.
- Die Portal-Initialisierung prüft zur Laufzeit mehrere sinnvolle Basispfade, damit lokale Entwicklung und Containerbetrieb identisch funktionieren.

---

## 7. Performance & Skalierbarkeit

### 7.1 Aktuelle Grenzen
- Unbegrenzte Anzahl Routinen
- Schnelle Suche via grep/git
- Markdown-Parser für Navigation

### 7.2 Optimierungen für Skalierung

Bei 100+ Routinen:
- Automatisierte Index-Generierung
- Tag-basierte Kategorisierung
- Snippet-Extraktion für Übersichten
- Datenbankoptimiert (können später folgen)

---

## 8. Qualitätssicherung

### Checklisten für jede Routine

**Vor Veröffentlichung:**
- [ ] Eindeutige ID zugewiesen
- [ ] Template vollständig ausgefüllt
- [ ] Abhängigkeiten dokumentiert
- [ ] Kein Redundanzen mit anderen Routinen
- [ ] Erfolgskriterien messbar
- [ ] Spellcheck bestanden
- [ ] Formatierung überprüft

**Review-Prozess:**
- [ ] Von mindestens 1 anderen Person reviewed
- [ ] Feedback eingearbeitet
- [ ] Changelog aktualisiert
- [ ] Genehmigt

---

## 9. Integration mit Entwicklung

### Workflow für neue Routinen

```
1. Feature Branch erstellen
   git checkout -b routine/ROUTINE-XXX-name

2. Datei erstellen
   docs/handbuch/routinen/[kategorie]/ROUTINE-XXX.md

3. Template ausfüllen
   (Nach templates/routine-template.md)

4. Lokal testen & Review
   - Formatierung prüfen
   - Links validieren
   - Redundanzen prüfen
   - `bash scripts/validate-security.sh`
   - `bash scripts/validate-architecture.sh`
   - `bash scripts/validate-docs.sh`

5. Pull Request öffnen
   - Beschreibung: Was wurde am System gelernt?
   - Reviewer: Min. 1 Person

6. Merge in develop
   - Nach Approval
   - Changelog aktualisieren

7. Release in main
   - Via Release-PR
   - Tags für Versionen
```

---

## 10. Metriken & Monitoring

### Zu verfolgende Metriken

- **Anzahl Routinen** (gesamt, pro Kategorie)
- **Redundanz-Index** (% Redundanzen)
- **Wartbarkeits-Index** (Durchschnittsgröße, Komplexität)
- **Abdeckungs-Rate** (Geplante vs. dokumentierte Routinen)
- **Update-Häufigkeit** (Aktualität)

---

## 11. Nächste Schritte

1. ✅ Architektur definiert
2. ✅ Implementierung gestartet (Phase 1)
3. ✅ Automatisierte Validierung aufgesetzt
4. ✅ Erste operative Routine fuer Qualitaets-Gates erstellt
5. ✅ Review-Prozess in Betrieb
6. ⏳ Automatisierte Redundanz-Erkennung ausbauen

---

**Version History:**
- v1.0 (23.03.2026): Initiale Architektur dokumentiert
- v1.1 (25.03.2026): Qualitaets-Gates als Pflichtprozess und Validierungsschritte integriert
