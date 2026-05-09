---
titel: "Klassenarbeit 02: Relationale Datenbanken (BPE 6) + Programmierung (BPE 5.1)"
schuljahr: "2024-2025"
klasse: "BG12"
fach: "Informatik"
bearbeitungzeit: "90 Minuten"
erreichbare_punkte: 30
gewichtung:
  bpe6_rdb: "90% (27 Punkte)"
  bpe5_programmierung: "10% (3 Punkte)"
---

# Klassenarbeit: Relationale Datenbanken & Programmierung

**Klasse/Kurs:** BG12  
**Schuljahr:** 2024-2025  
**Bearbeitungszeit:** 90 Minuten  
**Erreichbare Punkte:** 30  

---

## Anleitung für Schülerinnen und Schüler

- **Bearbeiten Sie alle Aufgaben** in der vorgegebenen Reihenfolge.
- **Benutzen Sie für Struktogramme** die Standard-Notationen nach dem Baden-Württemberg Lehrplan.
- **Bei Datenbankaufgaben:** Geben Sie vollständige SQL-Anweisungen oder aussagekräftige Entwürfe an.
- **Zeit-Management:** Verteilen Sie die Zeit entsprechend der Punktegrenzen (ca. 3 Minuten pro Punkt).

---

# BPE 6: Relationale Datenbanken (27 Punkte / 90%)

## Aufgabe 1: Konzepte der Relationalen Datenbanken

**Punkte: 3**  
**BPE:** 6 – Relationale Datenbanken / Grundkonzepte

### Problemstellung

Bewerten Sie die folgenden Aussagen zu Relationalen Datenbanken als **richtig (r)** oder **falsch (f)**:

| Nr. | Aussage | r/f |
|-----|---------|-----|
| 1.1 | Eine Auswahl­abfrage beginnt in der Regel mit der Klausel SELECT. |  |
| 1.2 | Die WHERE-Klausel einer Datenbankabfrage wird immer ausgeführt, unabhängig davon, ob eine Bedingung erfüllt ist. |  |
| 1.3 | Die referentielle Integrität besagt, dass Attributwerte eines Fremdschlüssels auch als Attributwert eines Primärschlüssels vorhanden sein müssen. |  |
| 1.4 | Ein Primärschlüssel kann in einer Tabelle mehrmals vorkommen. |  |
| 1.5 | Eine Normalisierung von Daten ist immer notwendig und führt zu besserer Datenbankperformance. |  |

### Bewertung

**3 Punkte:** Alle 5 Aussagen korrekt bewertet  
**2 Punkte:** 4 Aussagen korrekt  
**1 Punkt:** 3 Aussagen korrekt  
**0 Punkte:** Weniger als 3 Aussagen korrekt

---

## Aufgabe 2: Datenbankmodellierung und Normalisierung

**Punkte: 4**  
**BPE:** 6.3 – Normalisierung und Datenbankdesign

### Szenario

Die Hector-Kinderakademie verwaltet Förderkurse mit einem Datenbanksystem. **Bisherige Struktur:**

- Jeder Kurs wird von genau **einem** Dozenten unterrichtet.
- Ein Dozent kann **mehrere** Kurse leiten.

**Neue Anforderung:**
- Ein Kurs soll von **mehreren** Dozenten betreut werden können **(Team-Teaching)**.
- Ein Dozent kann gleichzeitig **mehrere** Kurse durchführen.

### Aufgabenteile

#### a) Normalisierungsproblem identifizieren (1 Punkt)

**Frage:** Beschreiben Sie, warum die bisherige 1:N-Beziehung zwischen Dozent und Kurs **nicht mehr ausreichend** ist.

**Erwartete Antwort:**
- Begründung: 1:N erlaubt nur einen Dozenten pro Kurs
- Neue Anforderung: N:M ist notwendig (mehrere Dozenten pro Kurs, mehrere Kurse pro Dozent)

#### b) Normalisierungslösung (2 Punkte)

**Frage:** Beschreiben Sie die notwendige Umstrukturierung. Was wird sich ändern? Welche neuen Tabellen entstehen?

**Erwartete Antwort (Punkte):**
- 1 Punkt: Identifikation einer Zwischentabelle (z.B. `kurs_dozent`, `kurs_dozenten`)
- 1 Punkt: Korrekte Beschreibung der neuen N:M-Beziehung mit Fremdschlüsseln

#### c) EERM-Skizze (1 Punkt)

**Frage:** Erstellen Sie ein erweitertes Entity-Relationship-Diagramm (EERM) für die neue Struktur mit mindestens den Tabellen `kurs`, `dozent` und `kurs_dozent`. Verwenden Sie die Modellierung in MySQL Workbench.

**Bewertungskriterien:**
- ✅ Alle drei Tabellen vorhanden
- ✅ Primärschlüssel gekennzeichnet (unterstrichen oder PK)
- ✅ Fremdschlüssel gekennzeichnet (FK)
- ✅ Beziehungen/Kardinalitäten erkennbar (1:N, N:M)

---

## Aufgabe 3: Datenbankabfragen – SQL SELECT

**Punkte: 5**  
**BPE:** 6.4 – SQL-Abfragen (SELECT, WHERE, JOIN)

### Szenario

Gegeben ist folgende Datenbankstruktur für die Hector-Kinderakademie:

```sql
-- Tabelle: kinder
CREATE TABLE kinder (
    kind_id INT PRIMARY KEY,
    name VARCHAR(100),
    geburtsdatum DATE,
    eltern_id INT
);

-- Tabelle: kurse
CREATE TABLE kurse (
    kurs_id INT PRIMARY KEY,
    titel VARCHAR(100),
    fachbereich VARCHAR(50),
    max_teilnehmer INT
);

-- Tabelle: anmeldungen
CREATE TABLE anmeldungen (
    anmeldung_id INT PRIMARY KEY,
    kind_id INT,
    kurs_id INT,
    anmeldedatum DATE,
    FOREIGN KEY (kind_id) REFERENCES kinder(kind_id),
    FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id)
);
```

### Aufgabenteile

#### a) Einfache SELECT-Abfrage (1 Punkt)

**Frage:** Schreiben Sie eine SQL-Abfrage, die alle **Kurse im Fachbereich "Mathematik"** anzeigt.

```sql
-- Ihre Lösung:
```

#### b) SELECT mit WHERE und Bedingung (1,5 Punkte)

**Frage:** Schreiben Sie eine SQL-Abfrage, die alle **Kinder anzeigt, die sich für den Kurs mit der ID `5` angemeldet haben**.

```sql
-- Ihre Lösung:
```

#### c) SELECT mit JOIN (2 Punkte)

**Frage:** Schreiben Sie eine SQL-Abfrage, die für jedes **Kind** den **Namen des Kindes** und alle **Kurse**, für die es angemeldet ist, anzeigt. Verwenden Sie einen JOIN.

```sql
-- Ihre Lösung:
```

#### d) Aggregation (0,5 Punkte Bonus)

**Frage (optional, +0,5 Punkte):** Wie viele Kinder haben sich insgesamt angemeldet?

```sql
-- Ihre Lösung:
```

### Bewertung

| Aufgabe | Punkte | Kriterien |
|---------|--------|----------|
| a) | 1 | SELECT und WHERE korrekt; Bedingung erfüllt |
| b) | 1,5 | Die abgerufenen Zeilen (Kinder) sind korrekt kombiniert; Syntax ok |
| c) | 2 | JOIN korrekt; Verknüpfung zwischen Tabellen funktioniert |
| d) | +0,5 | COUNT und GROUP BY (optional) |

---

## Aufgabe 4: Fehleranalyse – Referentielle Integrität

**Punkte: 6**  
**BPE:** 6.2 – Integrität und Constraints

### Szenario

Ein Benutzer versucht, einen Datensatz aus der Tabelle `kinder` zu löschen und erhält folgende Fehlermeldung:

```
Error: Cannot delete or update a parent row: a foreign key constraint fails 
('hector_akademie.anmeldungen', CONSTRAINT 'fk_anmeldungen_kind' 
FOREIGN KEY ('kind_id') REFERENCES 'kinder' ('kind_id'))
```

### Aufgabenteile

#### a) Fehlmeldung interpretieren (2 Punkte)

**Frage:** Erklären Sie diese Fehlermeldung in eigenen Worten. Was bedeutet "foreign key constraint fails"? Warum kann das Kind nicht gelöscht werden?

**Erwartete Antwort (Punkte):**
- 1 Punkt: Verständnis von Fremdschlüsseln und referentieller Integrität
- 1 Punkt: Begründung, warum das Löschen fehlschlägt (anmeldungen-Datensätze verweisen noch auf dieses Kind)

#### b) Lösungsmöglichkeiten (2 Punkte)

**Frage:** Nennen Sie mindestens **zwei Möglichkeiten**, wie dieses Problem gelöst werden könnte, und erklären Sie die Vor- und Nachteile jeder Lösung.

**Erwartete Antworten:**
1. **Cascading Delete:** Alle Anmeldungen des Kindes zuerst löschen, dann das Kind.
   - Vorteil: Eindeutige Lösung, Datenbank-Integrität bleibt erhalten
   - Nachteil: Datenverlust möglich
2. **ON DELETE CASCADE:** Datenbankregel, dass abhängige Datensätze automatisch gelöscht werden.
   - Vorteil: Automatisch, konsistent
   - Nachteil: Unkontrollierter Datenverlust möglich
3. **Soft Delete:** Statt zu löschen, einen Status-Flag setzen (z.B. `aktiv = 0`).
   - Vorteil: Keine Datenverluste, Audit-Trail möglich
   - Nachteil: Zusätzliche Komplexität

#### c) Praktische Umsetzung (2 Punkte)

**Frage:** Schreiben Sie die SQL-Befehle auf, um das Kind mit der ID `42` zu löschen, nachdem Sie alle problematischen Abhängigkeiten aufgelöst haben.

```sql
-- Schritt 1: Anmeldungen des Kindes löschen
-- Ihre Lösung:

-- Schritt 2: Kind löschen
-- Ihre Lösung:
```

### Bewertung

- **2 Punkte:** Korrekte und verständliche Erklärung
- **2 Punkte:** Mindestens zwei sinnvolle Lösungsmöglichkeiten mit Vor-/Nachteilen
- **2 Punkte:** Praktische SQL-Befehle korrekt und vollständig

---

## Aufgabe 5: Datenbankoptimierung – Indizes

**Punkte: 9**  
**BPE:** 6.5 – Performance und Datenbankoptimierung

### Szenario

Ein Unternehmen führt ein Online-System für die Verwaltung großer Mengen an Lernmaterialien. Die Datenbank enthält über 500.000 Datensätze. Die Abfrage nach materialien nach `kategorie_id` dauert mehrere Sekunden.

### Aufgabenteile

#### a) Problem identifizieren (1,5 Punkte)

**Frage:** Warum dauert eine Abfrage wie `SELECT * FROM materialien WHERE kategorie_id = 5` mehrere Sekunden bei 500.000 Datensätzen?

**Erwartete Antwort (Punkte):**
- 1 Punkt: Verständnis von Datenbanksuche ohne Index (serielles Durchsuchen aller Zeilen)
- 0,5 Punkte: Gegensatz zu indizierter Suche (logarithmischer Zugriff)

#### b) Lösungsvorschlag – Index erstellen (2 Punkte)

**Frage:** Schreiben Sie einen SQL-Befehl, um einen Index auf der Spalte `kategorie_id` zu erstellen. Nennen Sie den Index aussagekräftig.

```sql
-- Ihre Lösung:
```

**Erwartete Lösung:**
```sql
CREATE INDEX idx_materialien_kategorie_id ON materialien(kategorie_id);
```

#### c) Weitere Optimierungsmöglichkeiten (2 Punkte)

**Frage:** Nennen Sie zwei weitere Optimierungsmöglichkeiten zur Verbesserung der Datenbankperformance und erklären Sie jeweils kurz, wie sie funktioniert.

**Mögliche Antworten:**
1. **Composite Index:** Index auf mehreren Spalten für häufige Multi-Column-Queries
2. **Partitionierung:** Große Tabellen in kleinere, verwaltbare Teile aufteilen
3. **Caching:** Häufig abgerufene Daten im Cache speichern
4. **Query-Optimierung:** Ineffiziente Queries umschreiben (z.B. unnötige JOINs vermeiden)
5. **Denormalisierung:** Kontrollierte Redundanz für häufige Abfragen (Trade-off)

#### d) Kritische Überlegungen (1,5 Punkte)

**Frage:** Indizes beschleunigen Lesezugriffe, können aber auch Nachteile haben. Nennen Sie zwei Nachteile von Indizes und erklären Sie diese.

**Erwartete Antwort (Punkte):**
- 1,5 Punkte kombiniert:
  - **Speicherplatz:** Indizes benötigen zusätzlichen Speicher
  - **Schreibperformance:** INSERT, UPDATE, DELETE sind langsamer, da der Index auch aktualisiert werden muss
  - **Wartungsaufwand:** Indizes müssen ggf. regelmäßig optimiert werden

### Bewertung

- **1,5 Punkte:** Korrektes Verständnis des Problems
- **2 Punkte:** Korrekter SQL CREATE INDEX Befehl
- **2 Punkte:** Zwei sinnvolle Optimierungsmöglichkeiten mit Erklärungen
- **1,5 Punkte:** Kritische Reflexion über Nachteile von Indizes

---

# BPE 5.1: Programmierung & Struktogramme (3 Punkte / 10%)

## Aufgabe 6: Programmierung mit Benutzereingabe – Validierung

**Punkte: 3**  
**BPE:** 5.1 – Programme mit Benutzereingabe/-ausgabe und Struktogramme

### Szenario

Sie sollen ein Programm schreiben, das **Prüfungspunkte** einliest und validiert. Die Eingabe soll nur Werte zwischen **0 und 50 Punkten** akzeptieren. Bei ungültiger Eingabe soll das Programm den Benutzer auffordern, erneut einzugeben.

### Aufgabenteile

#### a) Struktogramm (1,5 Punkte)

**Aufgabe:** Erstellen Sie ein **Struktogramm** (nach Baden-Württemberg Standard-Notation) für die Validierungslogik nach folgender Spezifikation:

**Anforderungen:**
1. Benutzer wird aufgefordert, Punkte einzugeben
2. **Bedingung prüfen:** Wert zwischen 0 und 50?
   - Wenn JA: "Eingabe gültig" ausgeben, ende Programm
   - Wenn NEIN: "Ungültige Eingabe! Bitte erneut eingeben." ausgeben
3. Die Eingabe soll so lange wiederholt werden, bis ein gültiger Wert eingegeben wird

**Notationshinweise:**
- Verwenden Sie **rechtwinklige Rechtecke** für Eingabe/Ausgabe
- Verwenden Sie **Rauten** für Bedingungen
- Verwenden Sie **Pfeile** oder **Verbindungslinien** korrekt
- Strukturblock müssen vollständig geschlossen sein (keine offenen Enden)

**Handgezeichnete Struktogramme sind akzeptabel, solange die Symbole erkennbar und die Logik nachvollziehbar ist.**

#### b) Python-Code (1,5 Punkte)

**Aufgabe:** Schreiben Sie den Python-Code basierend auf Ihrem Struktogramm.

```python
# Ihre Lösung:
```

**Anforderungen (Bewertung):**
- ✅ Input-Schleife funktioniert (while oder for)
- ✅ Validierungsbedingung korrekt (0 <= wert <= 50)
- ✅ Fehlerbehandlung: Ungültige Eingaben werden abgefangen
- ✅ Ausgabe entspricht der Aufgabenstellung

**Musterlösung (Beispiel):**
```python
while True:
    punkte_eingabe = input("Geben Sie die Prüfungspunkte ein (0-50): ")
    try:
        punkte = int(punkte_eingabe)
        if 0 <= punkte <= 50:
            print("Eingabe gültig!")
            break
        else:
            print("Ungültige Eingabe! Bitte zwischen 0 und 50 eingeben.")
    except ValueError:
        print("Ungültige Eingabe! Bitte eine Zahl eingeben.")
```

### Bewertung

| Kriterium | Punkte |
|-----------|--------|
| Struktogramm logisch korrekt | 1,0 |
| Struktogramm Notation/Symbole | 0,5 |
| Python-Code funktioniert | 1,0 |
| Python-Code erfüllt Anforderungen | 0,5 |
| **Gesamt** | **3,0** |

---

# Zusammenfassung und Bewertungsraster

## Punkte-Verteilung

| Aufgabe | Thema | Punkte | BPE |
|---------|-------|--------|-----|
| 1 | RDB-Konzepte | 3 | BPE 6 |
| 2 | Datenbankmodellierung | 4 | BPE 6 |
| 3 | SQL SELECT & JOIN | 5 | BPE 6 |
| 4 | Fehleranalyse | 6 | BPE 6 |
| 5 | Performance & Indizes | 9 | BPE 6 |
| 6 | Programmierung & Struktogrammw | 3 | BPE 5.1 |
| **Gesamt** | | **30** | **BPE 6: 27 (90%) / BPE 5.1: 3 (10%)** |

## Notenskala (Beispiel: 15-Punkte-System)

| Punkte | 0-6 | 7-9 | 10-12 | 13-15 | 16-19 | 20-23 | 24-26 | 27-28 | 29-30 |
|--------|-----|-----|-------|-------|-------|-------|-------|-------|-------|
| Note | 6 | 5 | 5 | 4 | 3 | 2 | 2 | 1 | 1 |

---

# Hinweise für Lehrende

## Vorbereitung

1. **Datenbank-Demo:** Richten Sie eine Live-Demo-Datenbank ein, damit Schüler die Queries testen können (optional).
2. **Struktogramm-Vorlage:** Bereitstellung des Operatorenliste-Dokuments als Referenz.
3. **Syntax-Toleranz:** In Programmieraufgaben kleine Syntaxfehler teilweise verzeihen, wenn die Logik klar ist.

## Bewertung

### Allgemeine Prinzipien

- ✅ **Struktur vor Perfektionismus:** Handgezeichnete Struktogramme OK, Symbole müssen erkennbar sein
- ✅ **Nachvollziehbarkeit:** Jeder Schritt muss lesbar und logisch sein
- ✅ **Logik vor Syntax:** Logikfehler: -1 bis -2 Punkte; Syntaxfehler: -0,25 bis -0,5 Punkte
- ✅ **Teilpunkte vergeben:** Nicht alles-oder-nichts (außer explizit markiert)

### Häufige Fehler und Punktabzug

| Fehler | Fachgebiet | Abzug |
|--------|-----------|-------|
| SELECT-Syntax vergessen (z.B. WHERE vor FROM) | SQL | -0,5 |
| JOIN nicht korrekt | SQL | -0,5 bis -1 |
| Fremdschlüssel vergessen im EERM | Datenbank-Design | -0,5 |
| Struktogramm-Symbole nicht erkennbar | Programmierung | -0,5 |
| `input()` vergessen oder falsch | Python | -0,5 bis -1 |
| Schleife logisch falsch (endlos, etc.) | Programmierung | -1 bis -1,5 |

### Checkliste für Lehrende

- [ ] Alle 5 Konzept-Fragen in Aufgabe 1 sind eindeutig beantwortet
- [ ] EERM in Aufgabe 2 zeigt N:M-Beziehung
- [ ] SQL-Befehle in Aufgabe 3 sind syntaktisch und logisch korrekt
- [ ] Fehlermeldung in Aufgabe 4 ist korrekt interpretiert
- [ ] Indizes in Aufgabe 5 sind praktisch anwendbar
- [ ] Struktogramm in Aufgabe 6 ist nach Standard gelesen- und nachvollziehbar
- [ ] Python-Code ist testbar und funktionsfähig

---

# Anhang: Musterlösungen (Auszug)

## Aufgabe 3a – Musterlösung

```sql
SELECT * FROM kurse WHERE fachbereich = 'Mathematik';
```

## Aufgabe 3c – Musterlösung

```sql
SELECT k.name, ku.titel
FROM kinder k
INNER JOIN anmeldungen a ON k.kind_id = a.kind_id
INNER JOIN kurse ku ON a.kurs_id = ku.kurs_id
ORDER BY k.name;
```

## Aufgabe 6b – Musterlösung (Python)

```python
while True:
    punkte_eingabe = input("Geben Sie die Prüfungspunkte ein (0-50): ")
    try:
        punkte = int(punkte_eingabe)
        if 0 <= punkte <= 50:
            print("Eingabe gültig!")
            break  # Bricht Schleife ab
        else:
            print("Ungültige Eingabe! Bitte zwischen 0 und 50 eingeben.")
    except ValueError:
        print("Ungültige Eingabe! Bitte eine Zahl eingeben.")

# Optional: Eingabe verarbeiten
print(f"Sie haben {punkte} Punkte eingegeben.")
```

---

## Änderungshistorie

| Version | Datum | Änderungen |
|---------|-------|-----------|
| 1.0 | 2025-05-09 | Template erstellt; BPE 6 (90%) + BPE 5.1 (10%) |

