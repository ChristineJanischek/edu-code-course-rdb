<!-- CENTRAL_ENTRYPOINT -->

# 📚 Lernroutinen-Wissensdatenbank

**Willkommen!** Dies ist die zentrale Dokumentation für alle Lernroutinen - systematisch, wartbar, redundanzfrei.

---

## 🚀 Quick-Start (5 Minuten)

### Ich möchte... eine neue Routine erstellen

1. **Prozess vorbereiten** (2 Min):
   - Lesen: [prozesse/neue-routine-erstellen.md](prozesse/neue-routine-erstellen.md)
   - Fragen? Siehe Beispiel unten

2. **Datei erstellen** (1 Min):
   ```bash
   # Kopiere Template
   cp templates/ROUTINE-TEMPLATE.md \
      routinen/[kategorie]/[ROUTINE-ID]-Name.md
   ```

3. **Ausfüllen & Review** (2 Min Setup):
   - Nutze [templates/ROUTINE-TEMPLATE.md](templates/ROUTINE-TEMPLATE.md)
   - Siehe Beispiel: [templates/beispiel-routine.md](templates/beispiel-routine.md)
   - Öffne Pull Request zum Review

### Ich möchte... eine existierende Routine finden

```bash
# Nach Keyword suchen
grep -r "Keyword" routinen/

# Nach Kategorie anschauen
ls routinen/kurzfristig/        # Täglich/Wöchentlich
ls routinen/mittelfristig/      # Monatlich/Quartalsweise
ls routinen/langfristig/        # Jährlich/Strategisch
```

### Ich möchte... Redundanzen finden/beheben

→ Siehe: [prozesse/redundanz-management.md](prozesse/redundanz-management.md)

### Ich möchte... eine Routine updaten

→ Siehe: [prozesse/routine-aktualisieren.md](prozesse/routine-aktualisieren.md)

---

## 📖 Dokumentation

### 🧪 Live-Tests & Anleitungen
- **[anleitungen/java-live-test.md](anleitungen/java-live-test.md)** - Java-App testen: Headless-Test im Codespace & GUI lokal starten
- **[anleitungen/rdb-live-test-und-webserver-setup.md](anleitungen/rdb-live-test-und-webserver-setup.md)** - Docker-Testumgebung, Webserver-Voraussetzungen, Apache/MySQL/phpMyAdmin/Workbench-Setup fuer relationale Datenbanken

### 🔧 Grundlagen & Setup
- **[PFLICHTENHEFT.md](PFLICHTENHEFT.md)** - Alles über das System & Anforderungen
- **[ARCHITEKTUR.md](ARCHITEKTUR.md)** - Wie das System funktioniert
- **[MARSCHPLAN.md](marschplaene/HAUPTMARSCHPLAN.md)** - Zeitplan & Meilenstones

### 📋 Prozesse
- **[prozesse/neue-routine-erstellen.md](prozesse/neue-routine-erstellen.md)** - Anleitung neue Routine
- **[prozesse/lehrplanbasierte-inhaltserweiterung.md](prozesse/lehrplanbasierte-inhaltserweiterung.md)** - Curriculare Analyse, ML/RAG-Verfahren und Ableitung neuer Lernpfade, Aufgaben und Loesungen
- **[prozesse/redundanz-management.md](prozesse/redundanz-management.md)** - Redundanzen eliminieren
- **[prozesse/review-prozess.md](prozesse/review-prozess.md)** - Review & Genehmigung
- **[prozesse/routine-aktualisieren.md](prozesse/routine-aktualisieren.md)** - Bestehende Routine ändern
- **[prozesse/qualitaets-gates-automatisierung.md](prozesse/qualitaets-gates-automatisierung.md)** - Automatische Pflicht-Gates

### 📐 Templates & Beispiele
- **[templates/ROUTINE-TEMPLATE.md](templates/ROUTINE-TEMPLATE.md)** - Standard-Vorlage für alle Routinen
- **[templates/beispiel-routine.md](templates/beispiel-routine.md)** - Dokumentiertes Beispiel

### 📚 Routinen nach Kategorie
- **[routinen/kurzfristig/](routinen/kurzfristig/)** - Täglich/Wöchentlich
- **[routinen/mittelfristig/](routinen/mittelfristig/)** - Monatlich/Quartalsweise
- **[routinen/langfristig/](routinen/langfristig/)** - Jährlich/Strategisch

---

## 📊 Struktur Übersicht

```
docs/handbuch/
├── README.md (du bist hier)
├── PFLICHTENHEFT.md          ← Anforderungen & Ziele
├── ARCHITEKTUR.md            ← System-Design
│
├── routinen/                 ← ALLE Lernroutinen
│   ├── kurzfristig/          ← Täglich/Wöchentlich
│   ├── mittelfristig/        ← Monatlich/Quartalsweise
│   └── langfristig/          ← Jährlich/Strategisch
│
├── templates/                ← Vorlagen & Blueprints
│   ├── ROUTINE-TEMPLATE.md   ← Standard-Template
│   └── beispiel-routine.md   ← Dokumentiertes Beispiel
│
├── prozesse/                 ← Governance & Prozesse
│   ├── neue-routine-erstellen.md
│   ├── routine-aktualisieren.md
│   ├── redundanz-management.md
│   ├── review-prozess.md
│   └── qualitaets-gates-automatisierung.md
│
└── marschplaene/             ← Planung & Tracking
    └── HAUPTMARSCHPLAN.md    ← Milestones & Todos
```

---

## 🎯 Schlüsselkonzepte

### Routine-Kategorien

| Kategorie | Häufigkeit | Verwendung |
|-----------|-----------|-----------|
| **Kurzfristig** | Täglich / Wöchentlich | Regelmäßige operativ Aufgaben |
| **Mittelfristig** | Monatlich / Quartalsweise | Regelmäßige Reviews & Planung |
| **Langfristig** | Jährlich / Strategisch | Strategische Reviews & Planung |

### Routine-Bestandteile

Jede Routine hat:
- ✅ **Ziel** - Was soll erreicht werden?
- ✅ **Schritte** - Wie wird es praktisch gemacht?
- ✅ **Erfolgskriterien** - Wann ist es erfolgreich?
- ✅ **Fehlerbehandlung** - Was kann schiefgehen?
- ✅ **Abhängigkeiten** - Welche Routinen sind verknüpft?

### Design-Prinzipien

- **DRY (Don't Repeat Yourself)** - Keine Redundanzen
- **SSOT (Single Source of Truth)** - Jede Info nur 1x
- **Wartbar** - Leicht zu verstehen & zu ändern
- **Erweiterbar** - Neue Routinen können einfach hinzugefügt werden

---

## 🔄 Typische Workflows

### Workflow 1: Neue Routine erstellen

```
1. Lese: prozesse/neue-routine-erstellen.md
2. Kopiere Template aus templates/
3. Fülle Vorlage aus
4. Check auf Redundanzen
5. Öffne Pull Request
6. Reviewer macht Qualitäts-Check
7. Nach Approval → Merge in main
```

**Dauer:** ca. 2 Stunden
**Unterstützung:** See "neue-routine-erstellen.md"

### Workflow 2: Redundanz gefunden?

```
1. Lese: prozesse/redundanz-management.md
2. Analysiere Überlappung
3. Entscheide: Löschen / Zusammenführen / Refaktorieren
4. Führe Eliminierung durch
5. Update Abhängigkeiten
6. Dokumentiere in Changelog
7. Merge & Publikation
```

**Dauer:** ca. 1-3 Stunden
**Unterstützung:** See "redundanz-management.md"

### Workflow 3: Routine aktualisieren

```
1. Lese: prozesse/routine-aktualisieren.md
2. Öffne Feature Branch
3. Mache Änderungen
4. Update Versionsnummer & Changelog
5. Test Änderungen
6. Öffne PR für Review
7. Nach Approval → Merge & Auto-Publikation
```

**Dauer:** ca. 1-2 Stunden
**Unterstützung:** See "routine-aktualisieren.md"

---

## 📈 Aktueller Status

### Phase 1: Grundstruktur ✅ LIVE
- ✅ Verzeichnisstruktur aufgebaut
- ✅ Dokumentation erstellt (PFLICHTENHEFT, ARCHITEKTUR, etc.)
- ✅ Templates definiert
- ✅ Prozesse dokumentiert
- ⏳ Marschplan in Betrieb

### Phase 2: Routinen-Katalog 🔄 IN BEARBEITUNG
- ⏳ Kurzfristige Routinen hinzufügen (Ziel: 5+)
- ⏳ Mittelfristige Routinen (Ziel: 3+)
- ⏳ Langfristige Routinen (Ziel: 2+)

### Phase 3: Optimierung 📅 GEPLANT
- ⏳ Redundanz-Analyse durchführen
- ⏳ Automatisierte Validierung aufsetzen
- ⏳ Performance optimieren

### Phase 4: Wartung & Monitoring 📅 GEPLANT
- ⏳ Monatliche Audits durchführen
- ⏳ Performance-Metriken tracken
- ⏳ Feedback-Prozess implementieren

**➜ Siehe:** [marschplaene/HAUPTMARSCHPLAN.md](marschplaene/HAUPTMARSCHPLAN.md)

---

## 💡 Best Practices

### Beim Erstellen einer Routine
- ✅ Bestehe Routinen IMMER prüfen (Redundanzen vermeiden)
- ✅ Template konsequent nutzen (Konsistenz)
- ✅ Konkrete Schritte schreiben (nicht vage)
- ✅ Abhängigkeiten vollständig dokumentieren
- ✅ Review-Prozess ernst nehmen (Qualität)

### Bei der Verwaltung
- ✅ Changelog aktualisieren bei jeder Änderung
- ✅ Links & Metadaten korrekt halten
- ✅ Veraltete Routinen archivieren (nicht löschen)
- ✅ Regelmäßige Redundanz-Audits durchführen
- ✅ Feedback sammeln & einarbeiten

### Bei Redundanz-Fällen
- ✅ Nicht einfach löschen (könnte abhängig sein)
- ✅ Abhängigkeiten vor Änderung überprüfen
- ✅ Entscheidung in Changelog dokumentieren
- ✅ Alle Beteiligten kommunizieren
- ✅ Alte Routine archivieren (nicht komplett löschen)

---

## 🆘 Häufige Fragen

### F: Wie erstelle ich schnell eine neue Routine?
**A:** Kopiere [templates/ROUTINE-TEMPLATE.md](templates/ROUTINE-TEMPLATE.md), fülle es aus, lese [prozesse/neue-routine-erstellen.md](prozesse/neue-routine-erstellen.md) durch.

### F: Was ist eine Redundanz und wie behebe ich das?
**A:** Wenn sich zwei Routinen stark ähneln. Lösung: [prozesse/redundanz-management.md](prozesse/redundanz-management.md)

### F: Ich bin unsicher, ob meine Routine gut dokumentiert ist?
**A:** Review-Prozess nutzen! [prozesse/review-prozess.md](prozesse/review-prozess.md) - Andere schauen drüber.

### F: Darf ich bestehende Routinen löschen?
**A:** Nein, archivieren. Siehe [prozesse/routine-aktualisieren.md](prozesse/routine-aktualisieren.md)

### F: Wie mache ich ein Update an einer Routine?
**A:** Siehe [prozesse/routine-aktualisieren.md](prozesse/routine-aktualisieren.md)

### F: Brauche ich für alles einen Review?
**A:** Ja, alle neuen/geänderten Routinen. Siehe [prozesse/review-prozess.md](prozesse/review-prozess.md)

---

## 🔗 Wichtige Links

| Link | Beschreibung |
|------|-------------|
| [PFLICHTENHEFT.md](PFLICHTENHEFT.md) | Anforderungen, Ziele, Risiken |
| [ARCHITEKTUR.md](ARCHITEKTUR.md) | System-Aufbau, Komponenten |
| [marschplaene/HAUPTMARSCHPLAN.md](marschplaene/HAUPTMARSCHPLAN.md) | Milestones, Todos, Zeitplan |
| [prozesse/](prozesse/) | Alle Prozess-Dokumentationen |
| [templates/](templates/) | Vorlagen und Beispiele |

---

## 📞 Support & Fragen

**Fragen zu Routinen?**
→ Siehe FAQ oben oder konkrete Prozess-Dokumentation

**Fragen zum System?**
→ [ARCHITEKTUR.md](ARCHITEKTUR.md)

**Fragen zu Prozessen?**
→ [prozesse/](prozesse/) - Relevantes Dokument suchen

**Fragen zu Zeitplan/Meilestones?**
→ [marschplaene/HAUPTMARSCHPLAN.md](marschplaene/HAUPTMARSCHPLAN.md)

**Direkter Kontakt:** [Team Lead / Process Owner]

---

## ✅ Checklist: System vorbereiten

Folge diese Schritte, um loszulegen:

- [ ] Lese [PFLICHTENHEFT.md](PFLICHTENHEFT.md)
- [ ] Lese [ARCHITEKTUR.md](ARCHITEKTUR.md)
- [ ] Schaue [marschplaene/HAUPTMARSCHPLAN.md](marschplaene/HAUPTMARSCHPLAN.md) für Phasen
- [ ] Wenn neue Routine: Lies [prozesse/neue-routine-erstellen.md](prozesse/neue-routine-erstellen.md)
- [ ] Nutze [templates/ROUTINE-TEMPLATE.md](templates/ROUTINE-TEMPLATE.md) als Vorlage
- [ ] Schaue [templates/beispiel-routine.md](templates/beispiel-routine.md) als Beispiel
- [ ] Öffne PR & nutze [prozesse/review-prozess.md](prozesse/review-prozess.md)

---

## 🎓 Lernpfад

**Anfänger (alles neu)?**
1. Lese README.md (du bist hier)
2. Lese PFLICHTENHEFT.md
3. Lese ARCHITEKTUR.md
4. Lies ein Beispiel-Template

**Fortgeschrittene (neue Routine)?**
1. Öffne [prozesse/neue-routine-erstellen.md](prozesse/neue-routine-erstellen.md)
2. Kopiere [templates/ROUTINE-TEMPLATE.md](templates/ROUTINE-TEMPLATE.md)
3. Fülle aus & öffne PR
4. Lese [prozesse/review-prozess.md](prozesse/review-prozess.md) falls Feedback

**Experte (System optimieren)?**
1. Lese [ARCHITEKTUR.md](ARCHITEKTUR.md)
2. Lese [prozesse/redundanz-management.md](prozesse/redundanz-management.md)
3. Führe Audits durch
4. Optimiere & refaktoriere

---

**Version:** 1.0
**Erstellt:** 23.03.2026
**Status:** Live & Einsatzbereit

**Viel Erfolg!** 🚀
