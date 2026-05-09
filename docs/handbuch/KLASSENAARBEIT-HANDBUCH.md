# Handbuch: Klassenarbeiten-Template & Musterklassenarbeit

**Erstellt:** 2025-05-09  
**Version:** 1.0  
**Fachbereich:** Informatik BG12 – Relationale Datenbanken (BPE 6) + Programmierung (BPE 5.1)

---

## 📖 Überblick

Dieses Handbuch erklärt:
1. **Wie Sie das Klassenarbeits-Template verwenden**
2. **Wie Sie eine neue Klassenarbeit auf Basis der Mustervorlage erstellen**
3. **Best Practices für Qualität und Formatierung**
4. **Wie Sie die Dateien in verschiedene Formate konvertieren**

---

## 1️⃣ Verfügbare Dateien

### 60-Minuten-Variante (neu)
- **Pfad:** [docs/handbuch/templates/KLASSENARBEIT-TEMPLATE-60MIN-34P-BPE6-BPE5.md](templates/KLASSENARBEIT-TEMPLATE-60MIN-34P-BPE6-BPE5.md)
- **Format:** Markdown (.md)
- **Punkteherleitung:** `120 * (60/210) = 34,29` -> gerundet **34 Punkte**
- **Gewichtung:**
   - 40% Modellierung/Normalisierung/Anomalien = 14 Punkte
   - 40% SQL-Abfragen ueber viele Tabellen = 14 Punkte
   - 10% Theorie (MC) = 3 Punkte
   - 10% Struktogramm = 3 Punkte

### 60-Minuten-Muster inkl. Datenartefakte
- **Pruefungsdatei:** [generated/klassenarbeiten/KA02_BG12_2025_60min_34P_Muster_EERM_SQL.md](../generated/klassenarbeiten/KA02_BG12_2025_60min_34P_Muster_EERM_SQL.md)
- **EERM-Datei (.mbw):** [generated/klassenarbeiten/KA02_BG12_2025_60min_34P_EERM.mbw](../generated/klassenarbeiten/KA02_BG12_2025_60min_34P_EERM.mbw)
- **Struktur- und Datendump (.sql):** [generated/klassenarbeiten/KA02_BG12_2025_60min_34P_schema_data_dump.sql](../generated/klassenarbeiten/KA02_BG12_2025_60min_34P_schema_data_dump.sql)
- **Datentiefe:** Parent-Tabellen enthalten ca. 20 Datensaetze.

### Template-Datei
- **Pfad:** [docs/handbuch/templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md](../../templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md)
- **Format:** Markdown (.md)
- **Inhalt:** 
  - Struktur mit Platzhaltern
  - Vollständige Aufgaben-Vorlage
  - Bewertungsrichtlinien
  - Häufige Fehler und Lösungen
- **Zweck:** Als Schablone für neue Klassenarbeiten

### Musterklassenarbeit
- **Pfad:** [generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md](../KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md)
- **Format:** Markdown (.md) + HTML (.html)
- **Inhalt:**
  - Konkrete Aufgaben mit Lösungen
  - Beispiel-Szenarien (Online-Bücherverleih)
  - Detaillierte Bewertungskriterien
  - Testfälle und Checklisten
- **Zweck:** Zeigt die erwartete Qualität und Struktur

---

## 2️⃣ Schritt-für-Schritt: Neue Klassenarbeit erstellen

### Schritt 1: Template kopieren

```bash
# Kopieren Sie das Template als Basis
cp docs/handbuch/templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md \
   generated/klassenarbeiten/KA02_BG12_[SCHULJAHR]_NEU_[SZENARIO].md
```

### Schritt 2: Frontmatter aktualisieren

Ändern Sie die Metadaten am Anfang der Datei:

```yaml
---
titel: "Klassenarbeit: [IHR SZENARIO] (BPE 6 & 5.1)"
schuljahr: "2024-2025"
klasse: "BG12"
fach: "Informatik"
bearbeitungzeit: "90 Minuten"
erreichbare_punkte: 30
---
```

### Schritt 3: Aufgaben anpassen

#### Option A: Szenario ändern (empfohlen)
- **Behalten Sie** die Struktur und Punkteverteilung
- **Ändern Sie** das Szenario (z.B. statt "Online-Bücherverleih" → "Hotel-Reservierungssystem")
- **Aktualisieren Sie** die Datenbankschema und SQL-Beispiele

**Beispiele für neue Szenarien:**
- 🏨 **Hotel-Reservierungssystem:** Zimmer, Gäste, Buchungen, Verfügbarkeit
- 🏪 **Supermarkt-Verwaltung:** Artikel, Bestandsverwaltung, Verkäufe, Kunden
- 🎓 **Schulverwaltung:** Schüler, Kurse, Noten, Lehrer
- 🚗 **Autovermietung:** Fahrzeuge, Kunden, Mietverträge, Reparaturen

#### Option B: Aufgaben teilweise austauschen
- Behalten Sie die BPE 6 / BPE 5.1 Verteilung (90% / 10%)
- Erneuern Sie einzelne Aufgaben (z.B. nur Aufgabe 3)

### Schritt 4: Lösungen einfügen

Suchen Sie nach `**Musterlösung:**` und `**Ihre Lösung:**` und füllen Sie ein:

```markdown
### Aufgabenteile

#### a) Beschreibung (1 Punkt)

**Frage:** [Ihre Frage]

**Musterlösung:**

[Fügen Sie die Lösung hier ein]
```

### Schritt 5: Konvertierung durchführen

```bash
# Validierung und HTML-Konvertierung
python /workspaces/edu-code-course-rdb/scripts/convert_ka_markdown.py
```

### Schritt 6: Qualitätskontrolle

**Checkliste:**

- [ ] Alle 6 Aufgaben vorhanden
- [ ] Punktegrenzen korrekt (BPE 6: 27 Punkte, BPE 5.1: 3 Punkte, Gesamt: 30)
- [ ] Zeitaufwand pro Aufgabe notiert (~5-15 min)
- [ ] Mindestens eine Musterlösung pro Aufgabe
- [ ] EERM im Diagramm vorhanden
- [ ] SQL-Beispiele syntaktisch korrekt
- [ ] Python-Code testbar
- [ ] Struktogramm logisch geschlossen
- [ ] Lehrendendokument mit Bewertungsrichtlinien

---

## 3️⃣ Struktur und Bedeutung

### BPE 6: Relationale Datenbanken (27 Punkte / 90%)

| Aufgabe | BPE-Fokus | Typische Punkte | Dauer |
|---------|-----------|-----------------|-------|
| 1 | 6.0 – Grundkonzepte | 3 | ~5 min |
| 2 | 6.3 – Normalisierung | 4 | ~8 min |
| 3 | 6.4 – SQL SELECT/JOIN | 5 | ~12 min |
| 4 | 6.2 – Integrität & Fehler | 6 | ~10 min |
| 5 | 6.5 – Performance & Indizes | 9 | ~15 min |
| **Gesamt BPE 6** | | **27** | **~50 min** |

### BPE 5.1: Programmierung (3 Punkte / 10%)

| Aufgabe | BPE-Fokus | Typische Punkte | Dauer |
|---------|-----------|-----------------|-------|
| 6 | 5.1 – I/O & Struktogramme | 3 | ~15 min |
| **Gesamt BPE 5.1** | | **3** | **~15 min** |

### Zeitaufwand insgesamt: ~90 Minuten (inklusive Lesen, Pausen)

---

## 4️⃣ Best Practices

### ✅ Qualitätsstandards

1. **Klare Aufgabenstellung**
   - Wer? Was? Mit welchen Mitteln?
   - Szenario muss realistisch und verständlich sein

2. **Progessive Schwierigkeit**
   - Aufgabe 1-3: Einstieg
   - Aufgabe 4-5: Vertiefung
   - Aufgabe 6: Programmierung

3. **Vielfalt der Aufgabentypen**
   - Konzeptfragen (wahr/falsch)
   - Praktisches Datenbankdesign (EERM)
   - SQL-Abfragen (SELECT, JOIN, WHERE)
   - Fehleranalyse
   - Performance & Optimierung
   - Programmierung & Struktogramme

4. **Bewertungsklarheit**
   - Punkteschema pro Aufgabe klar
   - Häufige Fehler dokumentiert
   - Lösungen verfügbar

5. **Formatierung**
   - Code in Code-Blöcken mit Sprache (```sql, ```python)
   - Tabellen für strukturierte Daten
   - Hervorhebungen für wichtige Konzepte

### ⚠️ Häufige Fehler

| Problem | Lösung |
|---------|--------|
| Zu viele SQL-Aufgaben | Aufgaben variieren: Design, Analyse, Performance |
| Unklar Szenario | Mit Kontext starten, Domäne einführen |
| Zu lange Bearbeitungszeit | Pro Punkt ~3 Minuten kalkulieren |
| Keine Lösungen | Mindestens Musterlösungen für Lehrende |
| Syntax-Fehler in Code-Beispielen | Code vor Veröffentlichung testen |
| Struktogramme zu kompakt | Symbole müssen erkennbar sein |

---

## 5️⃣ Dateiformate und Konvertierung

### Verfügbare Formate

| Format | Zweck | Wo verfügbar |
|--------|-------|--------------|
| **Markdown (.md)** | Versionskontrolle, GitHub, einfache Bearbeitung | `/generated/klassenarbeiten/*.md` |
| **HTML (.html)** | Webversion, Print-preview | `/generated/klassenarbeiten/*.html` |
| **DOCX (.docx)** | Word-Format für Lehrer | Manuell via Pandoc oder Online-Konverterer |
| **PDF (.pdf)** | Druckversion, Austausch | Über Word oder Browser Print |

### Konvertierung zu DOCX

**Option 1: Lokal mit Pandoc**

```bash
# Installieren (einmalig)
apt update && apt install pandoc texlive-latex-extra -y

# Konvertieren
pandoc KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html \
       -o KA02_BG12_2024-2025_Muster_Online-Buecherverleih.docx \
       --reference-doc=template.docx  # Optional: Template verwenden
```

**Option 2: Online-Konverterer**

- [cloudconvert.com](https://cloudconvert.com) – Markdown → DOCX
- [zamzar.com](https://www.zamzar.com) – HTML → DOCX
- [pandoc.org/try](https://pandoc.org/try) – Online Pandoc

**Option 3: Microsoft Word**

1. HTML-Datei in Word öffnen
2. Formatierung anpassen
3. Als DOCX speichern

---

## 6️⃣ Beispiel-Szenarien zum Anpassen

### Szenario 1: 🏨 Hotel-Reservierungssystem

**Datenbankentitäten:**
- Zimmer (zimmer_id, typ, preis, anzahl_betten)
- Gäste (gast_id, name, email, telefon)
- Buchungen (buchung_id, gast_id, zimmer_id, ankunftsdatum, abreisedatum)
- Rechnungen (rechnung_id, buchung_id, betrag, datum)

**Aufgabe-Ankler:**
- Aufgabe 2: N:M-Beziehung → Ein Gast kann mehrere Zimmer buchen, ein Zimmer von mehreren Gästen
- Aufgabe 3: JOIN → Alle Gäste und ihre Zimmer für einen Zeitraum
- Aufgabe 4: Fehler → Versuch, eine Rechnung zu löschen, obwohl noch Buchungen existieren
- Aufgabe 5: Index → Schnelle Suche nach Gast-Buchungen oder verfügbaren Zimmern

### Szenario 2: 🏪 Supermarkt-Verwaltung

**Datenbankentitäten:**
- Artikel (artikel_id, name, kategorie, preis)
- Bestände (bestand_id, artikel_id, lager, mindestbestand)
- Verkäufe (verkauf_id, artikel_id, menge, datum, kassierer_id)
- Kassierer (kassierer_id, name, abteilung)

---

## 7️⃣ Checkliste für Lehrende vor der Klassenarbeit

### Vorbereitung

- [ ] Klassenarbeit 2-3 Wochen vorher ankündigen
- [ ] Lehrmaterial bereitstellen (Struktogramm-Operatorenliste, SQL-Syntax)
- [ ] Prüfungs-Demo-Datenbank einrichten (optional)
- [ ] Arbeitsumgebung testen (Python-IDE, SQL-Editor, Struktogramm-Tools)

### Durante Klassenarbeit

- [ ] Zeitvorgabe einhalten (90 min)
- [ ] Stille bewahren, keine Hilfeblätter erlaubt
- [ ] Fragen dürfen geklärt werden (Verständnis, nicht Lösung)

### Nach Klassenarbeit

- [ ] Korrektur nach Bewertungsrichtlinien durchführen
- [ ] Häufige Fehler notieren → Für nächste Schuljahr verbessern
- [ ] Feedback an Schüler geben
- [ ] Notenstatistik auswerten (Durchschnitt, Verteilung)

---

## 📚 Zusätzliche Ressourcen

### Im Repository

- **Lehrplan:** [uploads/pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/BG2-AG-EG-SG-WG_Informatik_18_3992k_NEU_Abitur2021.pdf](../../uploads/pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/BG2-AG-EG-SG-WG_Informatik_18_3992k_NEU_Abitur2021.pdf)
- **Operatorenliste Struktogramme:** [uploads/klassenarbeiten-und-unterrichtsmaterialien/operatorenliste-fuer-struktogramme-v2-2.pdf](../../uploads/klassenarbeiten-und-unterrichtsmaterialien/operatorenliste-fuer-struktogramme-v2-2.pdf)
- **Klassenaarbeit-Archiv:** [uploads/klassenarbeiten-und-unterrichtsmaterialien/](../../uploads/klassenarbeiten-und-unterrichtsmaterialien/)

### Externe Ressourcen

- **SQL-Syntax:** [w3schools.com/sql](https://w3schools.com/sql)
- **Python Dokumentation:** [python.org/docs](https://python.org/docs)
- **Normalisierung Visualizer:** [dataedo.com](https://dataedo.com)
- **ERD-Tools:** [lucidchart.com](https://lucidchart.com), [draw.io](https://draw.io)

---

## 🎯 Kontakt & Feedback

Bei Fragen oder Verbesserungsvorschlägen:
- Siehe: [Repository](https://github.com/ChristineJanischek/edu-code-course-rdb)
- Issues: [GitHub Issues](https://github.com/ChristineJanischek/edu-code-course-rdb/issues)

---

## Versionshistorie

| Version | Datum | Änderungen |
|---------|-------|-----------|
| 1.0 | 2025-05-09 | Handbuch erstellt; Template & Musterklassenarbeit |

