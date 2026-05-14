# 📚 Klassenarbeiten-Sammlung

Dieses Verzeichnis enthält Musterklassenarbeiten und Templates für den Unterricht im Fach Informatik (BG12), speziell für die Themen **Relationale Datenbanken (BPE 6)** und **Programmierung (BPE 5.1)**.

---

## 📁 Dateien

### Klassenarbeits-Set 2025/2026 (drei Versionen)

- **[KA02_BG12_2025_2026_VERSION1_aufg.md](./KA02_BG12_2025_2026_VERSION1_aufg.md)** / **[KA02_BG12_2025_2026_VERSION1_lsg.md](./KA02_BG12_2025_2026_VERSION1_lsg.md)**
  - VERSION1 (Haupttermin)
- **[KA02_BG12_2025_2026_VERSION2_aufg.md](./KA02_BG12_2025_2026_VERSION2_aufg.md)** / **[KA02_BG12_2025_2026_VERSION2_lsg.md](./KA02_BG12_2025_2026_VERSION2_lsg.md)**
  - VERSION2 (Nachtermin)
- **[KA02_BG12_2025_2026_VERSION3_aufg.md](./KA02_BG12_2025_2026_VERSION3_aufg.md)** / **[KA02_BG12_2025_2026_VERSION3_lsg.md](./KA02_BG12_2025_2026_VERSION3_lsg.md)**
  - VERSION3 (Muster/Uebung)

Automatische Generierung/Pruefung des Dreier-Sets:
```bash
bash ../../scripts/generate-ka-varianten.sh KA02_BG12_2025_2026
```

### Musterklassenarbeit (60 Minuten / 34 Punkte / EERM + SQL)

- **[KA02_BG12_2025_60min_34P_Muster_EERM_SQL.md](./KA02_BG12_2025_60min_34P_Muster_EERM_SQL.md)**
   - Markdown-Version (kompakt fuer 60 Minuten)
   - ✅ Gesamtpunkte aus Vorgaben hergeleitet: 34
   - ✅ Verteilung: 40% Modellierung, 40% Abfragen, 10% Theorie, 10% Struktogramm

- **KA02_BG12_2025_60min_34P_EERM.mwb**
   - EERM-Modellspezifikation Teil B (Lehrkraft-Referenz)

- **stadtfahrradverleih_struktur_2025.sql**
   - SQL-Struktur-Definition fuer Teil C (separater 3NF-Kontext: Stadtfahrradverleih)
   - Enthaelt: CREATE DATABASE, CREATE TABLE, Constraints (FK, Indizes)
   - ✅ Struktur-only (keine Daten)

- **stadtfahrradverleih_daten_2025.sql**
   - SQL-Daten fuer Teil C (Musterdatensaetze fuer Abfragen)
   - Enthaelt: USE-Statement, INSERT Statements
   - ✅ Parent-Tabellen mit ca. 20 Datensaetzen (`kunden`, `mitarbeitende`)
   - ✅ Separate Datei von der Struktur (KF-ROUTINE-010)

- **stadtfahrradverleih_2025.mwb**
   - EERM-Modellspezifikation fuer die SQL-Datenbank in Teil C
   - Muss als natives Workbench-Modell vorliegen (keine Platzhalterdatei)
    - Wird direkt aus den SQL-Strukturdumps erzeugt:
       `bash scripts/prepare-workbench-mwb.sh`

- **KA02_BG12_2025_60min_34P_SQLDB_EERM.png** (optional)
   - SQL-basiert gerenderte Referenzgrafik (oder exportierte Workbench-Grafik) fuer Unterrichtsmaterial

### Musterklassenarbeit (Online-Bücherverleih)

- **[KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md](./KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md)**
  - Markdown-Version (vollständig bearbeitbar)
  - ✅ 6 Aufgaben, 30 Punkte
  - ✅ BPE 6 (90%) + BPE 5.1 (10%)
  - ✅ Mit Lösungen und Bewertungskriterien

- **KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html**
  - HTML-Version (formatiert, druckbar)
  - Generiert von `convert_ka_markdown.py`
  - Verwendbar als Web-Version

---

## 📋 Schnelleinstieg

### Neue Klassenarbeit erstellen

1. **Musterklassenarbeit als Template verwenden:**
   ```bash
   cp KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md \
      KA02_BG12_2025_SCHULJAHR_NEU_[SZENARIO].md
   ```

2. **Szenario anpassen** (z.B. Hotel-Reservierung statt Bücherverleih)
   - Ändern Sie die Datenbankentitäten
   - Passen Sie die Aufgaben an
   - Behalten Sie die Struktur und Punkteverteilung

3. **Validierung durchführen:**
   ```bash
   python ../../scripts/convert_ka_markdown.py
   ```

4. **Zu DOCX konvertieren:**
   ```bash
   pandoc KA02_BG12_[...].html -o KA02_BG12_[...].docx
   ```

---

## 📖 Dokumentation

- **[Handbuch](../KLASSENAARBEIT-HANDBUCH.md)** – Vollständige Anleitung zur Verwendung
- **[Template](../templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md)** – Vorlage für neue Klassenarbeiten
- **[Template 60 Min / 34 Punkte](../../docs/handbuch/templates/KLASSENARBEIT-TEMPLATE-60MIN-34P-BPE6-BPE5.md)** – Kompakte Vorlage mit neuer Gewichtung

---

## 🎯 Aufbau einer Klassenarbeit

### BPE 6: Relationale Datenbanken (27 Punkte / 90%)

1. **Aufgabe 1** (3 Pkt) – Grundkonzepte (wahr/falsch)
2. **Aufgabe 2** (4 Pkt) – Datenbankdesign & Normalisierung
3. **Aufgabe 3** (5 Pkt) – SQL SELECT/JOIN
4. **Aufgabe 4** (6 Pkt) – Fehleranalyse & Integrität
5. **Aufgabe 5** (9 Pkt) – Performance & Indizes

### BPE 5.1: Programmierung (3 Punkte / 10%)

6. **Aufgabe 6** (3 Pkt) – I/O & Struktogramme

---

## ✨ Features

✅ **Strukturiert & Modular**
- Jede Aufgabe klar definiert
- Lösungen und Bewertungskriterien
- Checklisten für Lehrende

✅ **Kopierfertig**
- Markdown-Format (GitHub-kompatibel)
- HTML für Web/Print
- Leicht zu DOCX konvertierbar

✅ **Skalierbar**
- Template für neue Szenarien
- Konsistente Formatierung
- Versionskontrolle möglich

✅ **Best Practices**
- Basierend auf langjähriger Unterrichtserfahrung
- Lehrplan-konform (Baden-Württemberg)
- Mit Musterlösungen und Bewertungsrichtlinien

✅ **Didaktische Trennung**
- Teil B (Modellierung) und Teil C (SQL-Abfragen) nutzen unterschiedliche Kontexte.
- Dadurch wird keine Modellierungsloesung indirekt durch den SQL-Teil vorweggenommen.

---

## 🔄 Konvertierungs-Tools

**Script:** [../../scripts/convert_ka_markdown.py](../../scripts/convert_ka_markdown.py)

Konvertiert Markdown zu HTML und validiert die Struktur:
```bash
python ../../scripts/convert_ka_markdown.py
```

**Output:**
- HTML-Version mit Styling
- Validierungsbericht
- Metadaten-Extraktion

---

## 📊 Beispiel-Szenarien

Die Musterklassenarbeit kann leicht angepasst werden. Hier sind Ideen:

- 🏨 **Hotel-Reservierungssystem** – Zimmer, Gäste, Buchungen
- 🏪 **Supermarkt-Verwaltung** – Artikel, Bestände, Verkäufe
- 🎓 **Schulverwaltung** – Schüler, Kurse, Noten
- 🚗 **Autovermietung** – Fahrzeuge, Kunden, Mietverträge
- 📚 **Bibliotheks-System** – Bücher, Mitglieder, Ausleihvorgänge (bereits vorhanden!)

---

## � Benennungskonvention (KF-ROUTINE-010)

Alle Dateien in diesem Verzeichnis folgen einer strikten Benennungskonvention:

### Modell-Container (.mwb)
- Format: `{Systemname}_{Jahr}.mwb`
- Beispiel: `kursplattform_2025.mwb`, `stadtfahrradverleih_2025.mwb`
- Hinweis: Ein echter Workbench-Container enthaelt intern `document.mwb.xml`.
- Platzhalterdateien sind nicht zulaessig.
- Pruefung: `bash scripts/validate-mwb-native.sh`
- Falls nur Spezifikation vorliegt: `bash scripts/prepare-workbench-mwb.sh` ausfuehren und Anleitung in `WORKBENCH-MWB-WORKFLOW.md` verwenden.

### SQL-Struktur-Dumps (.sql)
- Format: `{Systemname}_struktur_{Jahr}.sql`
- Beispiel: `stadtfahrradverleih_struktur_2025.sql`
- Enthaelt: CREATE DATABASE, CREATE TABLE, Constraints

### SQL-Daten-Dumps (.sql)
- Format: `{Systemname}_daten_{Jahr}.sql`
- Beispiel: `stadtfahrradverleih_daten_2025.sql`
- Enthaelt: USE, INSERT Statements (Musterdaten)
- **Wichtig:** Struktur und Daten sind immer in separaten Dateien!

### Klassenarbeits-Dokumente (.md)
- **Aufgaben-Version:** `KA0x_{Zielgruppe}_{Schuljahr}_{Version}_aufg.md`
  - Beispiel: `KA02_BG12_2025_2026_VERSION1_aufg.md`
  - Enthaelt: Aufgabenstellen + Artefakt-Verweise (OHNE Loesung)

- **Loesung-Version:** `KA0x_{Zielgruppe}_{Schuljahr}_{Version}_lsg.md`
  - Beispiel: `KA02_BG12_2025_2026_VERSION1_lsg.md`
  - Enthaelt: Aufgabenstellung + Musterloesung + Erwartungshorizont + Bewertung

**[Vollständige Dokumentation der Benennungskonvention](../../docs/handbuch/routinen/kurzfristig/KF-ROUTINE-010-datei-bezeichnungskonvention.md)**

---

## �📞 Support

Bei Fragen oder Verbesserungsvorschlägen:
- Siehe [KLASSENAARBEIT-HANDBUCH.md](../KLASSENAARBEIT-HANDBUCH.md)
- Repository: [GitHub](https://github.com/ChristineJanischek/edu-code-course-rdb)

---

## 📝 Lizenz & Attribution

Diese Klassenarbeiten basieren auf:
- Lehrplan Baden-Württemberg (BPE 6: Relationale Datenbanken, BPE 5.1: Programmierung)
- Best Practices aus dem Repository [python-algorithmen-datenstrukturen](https://github.com/ChristineJanischek/python-algorithmen-datenstrukturen)
- Jahrelanger Unterrichtserfahrung

---

**Erstellt:** 2025-05-09
**Versio:** 1.0
