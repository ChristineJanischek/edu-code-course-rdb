# PROZESS: Review & Genehmigung

**Dokumentversion:** 1.0
**Ziel:** Standardisierte Qualitätsprüfung aller Routinen
**Zielgruppe:** Reviewer, Approver, Dokumentatoren

---

## 🎯 Überblick

Der Review-Prozess sichert die **Qualität, Konsistenz und Korrektheit** aller Routinen vor Veröffentlichung.

**Rollen:**
- **Autor:** Schreibt die neue/geänderte Routine
- **Reviewer:** Technische Prüfung (min. 1 Person)
- **Approver:** Finale Genehmigung (Process Owner oder Team Lead)

**Dauer:** 1-2 Tage typisch

---

## 📋 Review-Checkliste für Reviewer

### A. GRUNDLAGEN (5-10 Min)

- [ ] **Eindeutige ID**
  - Keine doppelte ID in der Kategorie
  - Format: `[KÜRZEL]-ROUTINE-[NR]`

- [ ] **Klarer Name**
  - Aussagekräftig (versteht man sofort, worum es geht?)
  - Konkret (nicht zu allgemein)
  - Konsistent mit anderen Routine-Namen

- [ ] **Richtige Kategorie**
  - kurzfristig / mittelfristig / langfristig macht Sinn?
  - Häufigkeit passt zur Kategorie?

### B. INHALT (15-30 Min)

- [ ] **Ziel ist klar**
  - Kurz zusammengefasst (1-2 Sätze)
  - Beantwortbar: "Warum diese Routine?"
  - Nutzen ist erkennbar

- [ ] **Vorbedingungen dokumentiert**
  - Was muss vorhanden sein?
  - Abhängigkeiten vollständig aufgelistet?
  - Links zu Abhängigkeiten korrekt?

- [ ] **Schritte sind konkret & nachvollziehbar**
  - Nicht zu vage ("mach das" vs. "führe Kommando X aus")
  - Messbar/überprüfbar
  - Richtige Reihenfolge?
  - Keine wichtigen Schritte vergessen?

- [ ] **Erfolgskriterien sind messbar**
  - [ ] nicht "gut" oder "fertig"
  - [ ] "100% Tests bestanden" oder "Code-Review-Approval erhalten"
  - [ ] Klare Zustände (bestanden/nicht bestanden)

- [ ] **Fehlerbehandlung dokumentiert**
  - Was kann schiefgehen?
  - Wie wird damit umgegangen?
  - Sind Fallback-Szenarien berücksichtigt?

- [ ] **Ausgaben/Ergebnisse klar**
  - Was ist das Resultat?
  - Wo werden Artefakte gespeichert?
  - Format und Anforderung?

### C. STRUKTUR & FORMAT (10-15 Min)

- [ ] **Template wurde korrekt genutzt**
  - Alle Section vorhanden?
  - Struktur konsistent?
  - Markdown korrekt formatiert?

- [ ] **Verlinkungen korrekt**
  - Keine Dead Links
  - Interne Links zeigen auf existierende Dateien
  - Externe Links sind erreichbar
  - Abhängigkeits-Links sind alle aktuell?

- [ ] **Formatierung korrekt**
  - Keine Typos/Grammatik-Fehler
  - Konsistente Schreibweise
  - Code-Blöcke richtig formatiert
  - Tabellen lesbar

- [ ] **Metadata vollständig**
  - Alle Felder ausgefüllt
  - Keine Platzhalter ("TODO", "FIXME")
  - Versionsnummer (1.0) gesetzt
  - Datum eingetragen

### D. QUALITÄT & WARTBARKEIT (10-20 Min)

- [ ] **Keine Redundanzen erkannt**
  - Ähnelt nicht einer anderen Routine?
  - Sind Abgrenzungen zu ähnlichen Routinen klar?
  - (Wenn ja: Redundanz-Management einleiten)

- [ ] **Wiederverwendbar & wartbar**
  - Könnte diese Routine erweitert werden?
  - Ist sie flexibel genug für Variationen?
  - Sind Abhängigkeiten locker gekoppelt?

- [ ] **Zeitaufwand realistisch**
  - Kann man die Routine in dieser Zeit durchführen?
  - Ist der Aufwand proportional zum Nutzen?
  - Könnten Schritte optimiert werden?

- [ ] **Sicherheit & Best Practices**
  - Werden Best Practices eingehalten?
  - Sind Sicherheitsbedenken adressiert?
  - Entspricht sie den Governance-Richtlinien?

### E. VERKNÜPFUNGEN (5-10 Min)

- [ ] **Abhängigkeiten vollständig**
  - Alle erforderlichen vorgelagerten Routinen eingetragen?
  - Nachgelagerte Routinen berücksichtigt?

- [ ] **Verwandte Routinen verlinkt**
  - Ähnliche Routinen erwähnt?
  - Alternativen aufgezeigt?
  - Kontext hergestellt?

- [ ] **Changelog korrekt**
  - v1.0 mit Initialpublikation
  - Falls Updates: Alle Versionen dokumentiert
  - Datum und Autor eingetragen

---

## 🔍 Review-Feedback geben

### Feedback-Typen

| Typ | Priorität | Bedeutung | Beispiel |
|-----|-----------|-----------|---------|
| 🔴 **BLOCKER** | MUSS | Muss geändert werden | "Kritische Sicherheits-Lücke" |
| 🟠 **SOLLTE** | SCHWER | Sollte geändert werden | "Schritt 3 ist unklar" |
| 🟡 **KÖNNTE** | MITTEL | Wäre eine Verbesserung | "Vielleicht noch ein Beispiel?" |
| 🟢 **INFO** | LEICHT | Nur informativ | "Guter Punkt!" |

### Feedback-Template

```markdown
## Review-Feedback für [ROUTINE-ID]

### ✅ Was gut ist
- Punkt 1
- Punkt 2

### 🟠 Was geändert werden muss (BLOCKER)
1. Punkt 1
   - Grund: ...
   - Suggestion: ...

### 🟡 Was verbessert könnte (OPTIONAL)
1. Punkt 1
   - Suggestion: ...

### 💬 Fragen
1. Frage 1?
2. Frage 2?

### Gesamteindruck
[Kurze zusammenfassung]

---
Status: 🔴 Änderungen erforderlich / 🟡 Änderungen empfohlen / 🟢 Approved
```

---

## 👤 Reviewer-Rollen & -Anforderungen

### Wer kann reviewer sein?

✅ **Geeignet:**
- Personen mit Tiefenwissen zum Thema
- Prozess-Owner/Tech Leads
- Erfahrene Dokumentatoren
- Mindestens 1 andere Person als Autor

❌ **Nicht geeignet:**
- Der Autor selbst
- Jemand ohne Kontext zum Thema
- Personen, die keine Zeit für gründliche Prüfung haben

### Reviewer-Checkliste vor Feedback

Vor dem Review sicherstellen:
- [ ] Ich habe Zeit für gründliche Prüfung (min. 30 Min)?
- [ ] Ich kenne mich im Thema aus?
- [ ] Ich bin nicht befangen (Autor oder sehr ähnliche Routine)?
- [ ] Ich kann konstruktives Feedback geben?

---

## ⏱️ Review-Zeitplan

**Optimaler Workflow:**

```
Tag 1 __`
Tag 1 (Morgens):
  → Autor öffnet PR

Tag 1 (Mittags):
  → Reviewer macht erste Review (1-2h)

Tag 1-2 (Nachmittag):
  → Autor sieht Feedback & plant Changes

Tag 2 (Morgens):
  → Autor macht Änderungen & pushed

Tag 2 (Mittags):
  → Reviewer macht Final-Review (30 Min)

Tag 2 (Nachmittag):
  → Approver kann mergen

Tag 3 (Morgens):
  → In Produktion
````

**Maximale Dauer:** 5 Arbeitstage (s```
Tag 1 (Morgens):
  → Autor öffnet PR

Tag 1 (Mittags):
  → Reviewer macht erste Review (1-2h)

Tag 1-2 (Nachmittag):
  → Autor sieht Feedback & plant Changes

Tag 2 (Morgens):
  → Autor macht Änderungen & pushed

Tag 2 (Mittags):
  → Reviewer macht Final-Review (30 Min)

Tag 2 (Nachmittag):
  → Approver kann mergen

Tag 3 (Morgens):
  → In Produktion
```. ✅ **Changelog** ist dokumentiert
8. ✅ **Mindestens 1 Reviewer** hat `Approved` geclickt

---

## 🚫 Rejection-Gründe

Eine Routine wird **REJECTED** (müssen Überarbeitungen erfolgen), wenn:

- 🔴 **Massive Redundanz** mit anderer Routine
- 🔴 **Sicherheits-Bedenken** nicht adressiert
- 🔴 *``emplate gravierend nicht** genutzt
- 🔴 **Inhalt ist unleserlich** oder unklar
- 🔴 **Keine Erfolgskriterien** d`Approved` 🔴 **Kritische Fehler** im Prozess/Technik

**Feedback dann:** "Bitte komplett überarbeiten und neu einreichen"

---

## 🔄 Iterativer Feedback-Prozess

```
PR opened
  ↓
Review #1
  ├─ BLOCKER found → Autor macht Changes
  ├─ Return to Step 2
  ├─ SOLLTE Punkte: Autor kann optional ändern
  └─ KÖNNTE Punkte: Ignorieren erlaubt
  ↓
Review #2 (Final)
  ├─ All fixed? → Approved ✅
  └─ Still issues? → Rejection 🔴
  ↓
Merge & Publish
```

---

## 📊 Review-Metriken

**Track diese M__`
PR opened
  ↓
Review #1
  ├─ BLOCKER found → Autor macht Changes
  ├─ Return to Step 2
  ├─ SOLLTE Punkte: Autor kann optional ändern
  └─ KÖNNTE Punkte: Ignorieren erlaubt
  ↓
Review #2 (Final)
  ├─ All fixed? → Approved ✅
  └─ Still issues? → Rejection 🔴
  ↓
Merge & Publish
`| Lösung |
|---------|--------|
| Reviewer hat keine Zeit | Anderen Reviewer zuweisen / Deadline verlängern |
| Feedback ist zu harsch | Direkt be```
PR opened
  ↓
Review #1
  ├─ BLOCKER found → Autor macht Changes
  ├─ Return to Step 2
  ├─ SOLLTE Punkte: Autor kann optional ändern
  └─ KÖNNTE Punkte: Ignorieren erlaubt
  ↓
Review #2 (Final)
  ├─ All fixed? → Approved ✅
  └─ Still issues? → Rejection 🔴
  ↓
Merge & Publish
```len.md](neue-routine-erstellen.md) - Kurz-Anleitung nächster Schritt
- 📖 [redundanz-management.md](redundanz``anagement.md) - Redundanz behandeln
- 📖 [PFLIC`Durchschnittliche Review-Dauer`) - Anforderungen
- 📖 [ARCHITEKTUR.md]`% Routinen mit >1 Review`em-Design

---

**Version:**`% Routinen mit Redundanzen`:** 23.03.2026
`Review-Feedback-Kategorien``Rejection Rate`
