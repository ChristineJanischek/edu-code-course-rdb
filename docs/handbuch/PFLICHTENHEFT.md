# PFLICHTENHEFT: Lernroutinen-Wissensdatenbank

**Dokumentversion:** 1.0
**Datum:** 23. März 2026
**Status:** In Bearbeitung
**Letzter Autor:** System-Setup

---

## 1. Zielstellung & Motivation

### 1.1 Allgemeines Ziel
Aufbau einer strukturierten, wiederverwendbaren Wissensdatenbank zur **Verwaltung und Dokumentation von Lernroutinen** mit verschiedenen Zeithorizonten (kurz-, mittel-, langfristig). Das System soll dem kontinuierlichen Lernen von Systemen dienen und Best Practices standardisieren.

### 1.2 Spezifische Ziele
- **Effizienz:** Routinen ohne Redundanzen gestalten
- **Wiederverwendbarkeit:** Templates und Vorlagen für neue Routinen erstellen
- **Erweiterbarkeit:** Einfaches Hinzufügen neuer Routinen und Kategorien
- **Wartbarkeit:** Klare Struktur, Versionierung, Changelog
- **Sicherheit:** Kontrolle von Zugriff und Änderungen
- **Nachvollziehbarkeit:** Vollständige Dokumentation aller Schritte und Entscheidungen

---

## 2. Anforderungen

### 2.1 Funktionale Anforderungen (FA)

#### FA1: Routine-Management
- **FA1.1:** Kurzfristige Routinen (täglich/wöchentlich) verwaltbar machen
- **FA1.2:** Mittelfristige Routinen (monatlich/quartalsweise) dokumentieren
- **FA1.3:** Langfristige Routinen (jährlich/strategisch) festhalten
- **FA1.4:** Hierarchische Struktur für Kategorisierung (Projekt → Prozess → Routine)

#### FA2: Template-System
- **FA2.1:** Standardisiertes Template für alle Routinen-Typen
- **FA2.2:** Metadaten: ID, Titel, Beschreibung, Kategorie, Zeitraum, Verantwortlicher
- **FA2.3:** Struktur: Ziel, Schritte, Erfolgskriterien, Häufigkeit, Abhängigkeiten
- **FA2.4:** Versioning mit Changelog für alle Routinen

#### FA3: Prozess-Dokumentation
- **FA3.1:** Wie man neue Routinen erstellt (Leitfaden)
- **FA3.2:** Wie man Routinen aktualisiert und pflegt
- **FA3.3:** Wie man Redundanzen identifiziert und eliminiert
- **FA3.4:** Review- und Genehmigungsprozesse

#### FA4: Marschpläne
- **FA4.1:** Milestones definieren und verfolgen
- **FA4.2:** Todo-Listen mit Prioritäten und Zuständigkeiten
- **FA4.3:** Zeitpläne und Meilenstein-Termine
- **FA4.4:** Machbarkeitsanalysen für neue Routinen

#### FA5: Verwaltung und Governance
- **FA5.1:** Zugriffskontrolle (wer darf lesen/schreiben/genehmigen)
- **FA5.2:** Änderungshistorie und Audit-Log
- **FA5.3:** Redundanz-Analyse und Konsolidierungsprozesse
- **FA5.4:** Performance-Metriken für Routinen

#### FA6: Relationale-Datenbanken-Lernplattform
- **FA6.1:** Lehrpläne werden getrennt in `uploads/lehrplaene/` verortet und als curriculare Primärquellen behandelt.
- **FA6.2:** Die Webapp stellt didaktisch sinnvolle Lernpfade für EERM, 3. Normalform und SQL bereit.
- **FA6.3:** Im Übungsbereich stehen Code-Inboxen, Infoboxen, Selbstkontrolle und konstruktive Lösungshinweise bereit.
- **FA6.4:** Eine Docker-basierte Live-Testumgebung prüft PHP-Webapp, Python-API, MySQL und fachliche Beispieldaten reproduzierbar.
- **FA6.5:** Die technische Dokumentation beschreibt Webserver-Voraussetzungen und Schritt-für-Schritt-Setups für Apache, MySQL, phpMyAdmin und MySQL Workbench.

### 2.2 Nicht-funktionale Anforderungen (NFA)

#### NFA1: Qualität
- **NFA1.1:** Keine Redundanzen zwischen Routinen
- **NFA1.2:** DRY-Prinzip (Don't Repeat Yourself) konsequent anwenden
- **NFA1.3:** Maximale Wartbarkeit durch Modularität
- **NFA1.4:** Klare, verständliche Schreibweise

#### NFA2: Sicherheit
- **NFA2.1:** Versionskontrolle über Git
- **NFA2.2:** Automatische Backups und Recovery-Möglichkeiten
- **NFA2.3:** Schutz vor Datenverlust
- **NFA2.4:** Transparenz in allen Änderungen (Changelog)

#### NFA3: Performance & Skalierbarkeit
- **NFA3.1:** System skalierbar auf 100+ Routinen
- **NFA3.2:** Schnelle Suche und Navigation
- **NFA3.3:** Automatisierte Validierung und Prüfung

#### NFA4: Wartbarkeit
- **NFA4.1:** Klare Verzeichnisstruktur
- **NFA4.2:** Konsistente Namenskonventionen
- **NFA4.3:** Dokumentation aller Entscheidungen
- **NFA4.4:** Regelmäßige Reviews und Aktualisierungen

---

## 3. Systemarchitektur

### 3.1 Verzeichnisstruktur

```
docs/handbuch/
├── PFLICHTENHEFT.md              # Dieses Dokument
├── ARCHITEKTUR.md                # Technische Architektur
├── README.md                     # Übersicht und Quick-Start
├── MARSCHPLAN.md                 # Milestones und Roadmap
│
├── routinen/                     # Alle praktischen Routinen
│   ├── kurzfristig/              # Täglich/Wöchentlich
│   ├── mittelfristig/            # Monatlich/Quartalsweise
│   └── langfristig/              # Jährlich/Strategisch
│
├── templates/                    # Vorlagen und Blueprints
│   ├── routine-template.md       # Standard-Routine-Template
│   └── beispiel-routine.md       # Dokumentiertes Beispiel
│
├── prozesse/                     # Prozess & Governance
│   ├── neue-routine-erstellen.md # Leitfaden für neue Routinen
│   ├── routine-aktualisieren.md  # Updating & Maintenance
│   ├── redundanz-management.md   # Redundanzen eliminieren
│   └── review-prozess.md         # Review- und Genehmigungen
│
└── marschplaene/                 # Marschpläne & Planung
    ├── phase1-setup.md           # Phase 1: Grundstruktur
    ├── phase2-expansion.md       # Phase 2: Routinen-Katalog
    └── machbarkeit.md            # Machbarkeitsanalysen
```

### 3.2 Datenfluss

```
Neue__`
Neue Anforderung
    ↓
Leitfaden nutzen (neue-routine-erstellen.md)
    ↓
Template ausfüllen (routine-template.md)
    ↓
Review Process (review-prozess.md)
    ↓
In Kategorie einordnen (kurzfristig/mittelfristig/langfristig)
    ↓
Redundanzen-Analyse (redundanz-management.md)
    ↓
Genehmigung & Veröffentlichung
    ↓
Changelog aktualisieren
    ↓
Git Commit & Push
`h
```

### 3.3 Abhängigkeitsmodell

- **Routinen:** Basieren auf Templates
- **Templates:** Folgen Standard-Format
- **Prozesse:** Regeln die Verwaltung
- **Marschpläne:** Steuern die Umsetzung

---

## 4. Erfolgskriterien

### 4.1 Phase 1: Grundstruktur (Wochen 1-2)
- [ ] Alle Verzeichnisse erstellt
- [ ] Alle Template-Dokumente vorliegen
- [ ] Prozess-Do``mentation vollständig
- [ ] Review-Prozess definiert

### 4.2 Phase 2: Erste Routinen (Wochen 3-4)
- [ ] Mindestens 5 kurzfristige Routinen dokumentiert
- [ ] 3 mittelfristige Routinen
- [ ] 2 langfristige Routinen
- [ ] Keine Redundanzen zwischen Routinen

### 4.3 Phase 3: Optimierung (Wochen 5-6)
- [ ] Redundanz-Analyse durchgeführt
- [ ] System-Performance optimiert
- [ ] Automatisierte Validierung implementiert
- [ ] Vollständige Dokumentation aller Entscheidungen

```
Neue Anforderung
    ↓
Leitfaden nutzen (neue-routine-erstellen.md)
    ↓
Template ausfüllen (routine-template.md)
    ↓
Review Process (review-prozess.md)
    ↓
In Kategorie einordnen (kurzfristig/mittelfristig/langfristig)
    ↓
Redundanzen-Analyse (redundanz-management.md)
    ↓
Genehmigung & Veröffentlichung
    ↓
Changelog aktualisieren
    ↓
Git Commit & Push
```dundanz-Management
- Curriculare Lehrplanablage und lehrplangestützte Inhaltsentwicklung für relationale Datenbanken
- Webapp mit selbstgesteuerten Lernpfaden und Selbstkontrolle
- Docker-Testumgebung für relationale Datenbanken, EERM- und SQL-Lernszenarien

### 5.2 Out of Scope
- Automatisierte Workflow-Engine (kann später folgen)
- Datenbank-System (aktuell: Markdowneine)
- Mobile App (kann später folgen)
- Automatische Routine-Ausführung

---

## 6. Ressourcen & Aufwand

### 6.1 Zeitschätzung
- **Phase 1 (Grundstruktur):** 2 Wochen
- **Phase 2 (Routinen):** 2 Wochen
- **Phase 3 (Optimierung):** 2 Wochen
- **Phase 4 (Wartung):** Laufend
- **Gesamt:** 6 Wochen + Pflege

### 6.2 Ressourcen
- 1 Projektleiter/Dokumentateur
- Zugang zu Git Repository
- Markdown-Editor (VS Code)
- Test-Umgebung für Validierung

---

## 7. Risiken & Mitigationsmaßnahmen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|-----------|
| Redundanzen entstehen trotz System | Hoch | Mittel | Regelmäßige Audits, Checklisten |
| Dokumentation wird nicht gepflegt | Mittel | Hoch | Review-Prozess,Ownerschaft |
| System wird zu komplex | Mittel | Mittel | Iteratives Design, Feedback |
| Git-Konflikte | Niedrig | Mittel | Templates, Konventionen, PRs |

---

## 8. Nächste Schritte

1. ✅ Verzeichnisstruktur aufgebaut
2. ⏳ Architektur-Dokument erstellen
3. ⏳ Templates definieren und dokumentieren
4. ⏳ Prozesse schreiben
5. ⏳ Marschplan mit konkreten Todos
6. ⏳ Erste Routinen-Beispiele dokumentieren
7. ⏳ Review- und Genehmigungsprozess starten

---

**Kontakt & Support:**
Für Fragen zur Wissensdatenbank: Siehe MARSCHPLAN.md und prozesse/neue-routine-erstellen.md

**Version History:**
- v1.0 (23.03.2026): Initiales Pflichtenheft erstellt
