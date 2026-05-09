---
titel: "Muster-Klassenarbeit: Online-Bücherverleih (BPE 6 & 5.1)"
schuljahr: "2024-2025"
klasse: "BG12"
fach: "Informatik"
bearbeitungzeit: "90 Minuten"
erreichbare_punkte: 30
gewichtung:
  bpe6_rdb: "90% (27 Punkte)"
  bpe5_programmierung: "10% (3 Punkte)"
version: "1.0 (Muster)"
---

# Muster-Klassenarbeit: Online-Bücherverleih

**Klasse/Kurs:** BG12  
**Schuljahr:** 2024-2025  
**Bearbeitungszeit:** 90 Minuten  
**Erreichbare Punkte:** 30  

> 📌 **Hinweis:** Diese Musterklassenarbeit zeigt die erwartete Struktur und Schwerpunkte. Sie kann als Vorlage für weitere Klassenarbeiten genutzt werden.

---

## 📖 Allgemeine Anleitung

Bearbeiten Sie alle Aufgaben in der vorgegebenen Reihenfolge. Sie haben **90 Minuten** Zeit. Die Aufgaben bauen teilweise aufeinander auf.

**Materialien, die Sie benötigen:**
- Schreibzeug (Bleistift/Stift für Struktogramme)
- ggf. SQL-Editor oder Terminal für Code-Tests

---

# TEIL A: Relationale Datenbanken (27 Punkte / 90%)

## Aufgabe 1: Grundkonzepte Relationale Datenbanken

**Punkte: 3**  
**BPE:** 6 – Grundkonzepte  
**Zeit:** ~5 Minuten

### Aufgabenstellung

Eine Bücherei betreibt ein Datenbanksystem zur Verwaltung von Büchern, Mitarbeitern und Ausleihvorgängen. 

Bewerten Sie die folgenden Aussagen zu Relationalen Datenbanken als **richtig (r)** oder **falsch (f)**:

| Nr. | Aussage | r/f |
|-----|---------|-----|
| 1.1 | Ein Primärschlüssel identifiziert eindeutig jeden Datensatz in einer Tabelle. |  |
| 1.2 | Ein Fremdschlüssel kann mehrfach in einer Tabelle vorkommen. |  |
| 1.3 | Normalisierung verhindert immer vollständig Datenredundanz. |  |
| 1.4 | Eine Relation in der Datenb ist gleichbedeutend mit einer Tabelle. |  |
| 1.5 | Ein NULL-Wert in einem Primärschlüssel ist nicht erlaubt. |  |

### Musterlösung

| Nr. | Aussage | r/f |
|-----|---------|-----|
| 1.1 | Ein Primärschlüssel identifiziert eindeutig jeden Datensatz in einer Tabelle. | **r** |
| 1.2 | Ein Fremdschlüssel kann mehrfach in einer Tabelle vorkommen. | **r** |
| 1.3 | Normalisierung verhindert immer vollständig Datenredundanz. | **f** (Vereinigung ist ein Kompromiss) |
| 1.4 | Eine Relation in der Datenbank ist gleichbedeutend mit einer Tabelle. | **r** |
| 1.5 | Ein NULL-Wert in einem Primärschlüssel ist nicht erlaubt. | **r** |

### Bewertung

- **3 Punkte:** Alle 5 Aussagen korrekt
- **2 Punkte:** 4 Aussagen korrekt
- **1 Punkt:** 3 Aussagen korrekt
- **0 Punkte:** Weniger als 3 korrekt

---

## Aufgabe 2: Datenbankdesign – Normalisierung

**Punkte: 4**  
**BPE:** 6.3 – Normalisierung  
**Zeit:** ~8 Minuten

### Szenario

Die Bücherei hat folgende **bisherige Tabellenstruktur**:

```
Tabelle: Ausleihen
┌─────────┬────────────┬───────────────┬─────────────────┬────────────────────┐
│ aus_id  │ buch_titel │ mitarbeiter   │ ausleihdatum    │ rueckgabedatum     │
├─────────┼────────────┼───────────────┼─────────────────┼────────────────────┤
│ 1001    │ Java Basics│ Anna Müller   │ 2025-01-15      │ 2025-02-15         │
│ 1002    │ Python Pro │ Anna Müller   │ 2025-01-16      │ 2025-02-20         │
│ 1003    │ SQL Expert │ Max Schneider │ 2025-01-20      │ 2025-02-10         │
└─────────┴────────────┴───────────────┴─────────────────┴────────────────────┘
```

**Probleme mit dieser Struktur:**
- Bücherdaten sind redundant (Titel wird wiederholt)
- Kundendaten sind nicht separat gespeichert
- Keine Unterscheidung zwischen Kunde (Mitglied) und Mitarbeiter möglich

**Neue Anforderung:** Die Struktur soll **normalisiert** werden zur **3. Normalform (3NF)**.

### Aufgabenteile

#### a) Identifikation des Normalisierungsproblems (1 Punkt)

**Frage:** In welcher Normalform befindet sich die aktuelle Struktur? Begründen Sie Ihre Antwort.

**Musterlösung:**
- **Antwort:** 1. Normalform (1NF) oder gar nicht normalisiert
- **Begründung:** 
  - Alle Attribute sind atomar ✅
  - Aber: Partielle Abhängigkeiten vorhanden (buch_titel hängt nicht vollständig vom Primärschlüssel ab)
  - Transitive Abhängigkeiten möglich (Redundanzen)

#### b) Normalisierung durchführen (2 Punkte)

**Frage:** Beschreiben Sie die notwendigen Tabellen für eine normalisierte Struktur (3NF). Nennen Sie die Tabellen und deren Beziehungen.

**Musterlösung:**

Notwendige Tabellen:
1. **Bücher (buch_id, titel, autor, isbn, kategorie)**
2. **Mitglieder (mitglied_id, name, adresse, telefon)**
3. **Ausleihvorgänge (aus_id, mitglied_id, buch_id, ausleihdatum, rueckgabedatum)**

**Beziehungen:**
- 1:N zwischen Mitglieder und Ausleihen
- 1:N zwischen Bücher und Ausleihen

#### c) EERM erstellen (1 Punkt)

**Frage:** Erstellen Sie ein erweitertes Entity-Relationship-Diagramm (EERM) für die normalisierte Struktur in MySQL Workbench.

**Musterlösung (Text-Notation):**

```
┌──────────────────────────────────────────────────────────────┐
│                        MITGLIEDER                            │
├──────────────────────────────────────────────────────────────┤
│ PK: mitglied_id (INT)                                        │
│     name (VARCHAR)                                           │
│     adresse (VARCHAR)                                        │
│     anmeldedatum (DATE)                                      │
└──────────────────────────────────────────────────────────────┘
                            │
                      1     │ N
                            │ (has)
                            ▼
      ┌──────────────────────────────────────────────────────┐
      │                  AUSLEIHVORGÄNGE                     │
      ├──────────────────────────────────────────────────────┤
      │ PK: aus_id (INT)                                     │
      │ FK: mitglied_id       ──────► MITGLIEDER             │
      │ FK: buch_id           ──────► BÜCHER                 │
      │     ausleihdatum (DATE)                              │
      │     rueckgabedatum (DATE)                            │
      └──────────────────────────────────────────────────────┘
                  △
            1     │    N
                  │ (contains)
      ┌──────────┴────────────────────────────────────────┐
      │                    BÜCHER                          │
      ├───────────────────────────────────────────────────┤
      │ PK: buch_id (INT)                                 │
      │     titel (VARCHAR)                               │
      │     autor (VARCHAR)                               │
      │     isbn (VARCHAR)                                │
      │     kategorie (VARCHAR)                           │
      └───────────────────────────────────────────────────┘
```

### Bewertung

- a) 1 Punkt: Korrekte Normalform mit Begründung
- b) 2 Punkte: Mindestens 3 Tabellen mit Beziehungen
- c) 1 Punkt: EERM mit Primär-/Fremdschlüsseln und Kardinalitäten

---

## Aufgabe 3: SQL-Abfragen – SELECT, WHERE, JOIN

**Punkte: 5**  
**BPE:** 6.4 – SQL-Abfragen  
**Zeit:** ~12 Minuten

### Datenbankschema

```sql
CREATE TABLE buecher (
    buch_id INT PRIMARY KEY,
    titel VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    kategorie VARCHAR(50),
    preis DECIMAL(8,2)
);

CREATE TABLE mitglieder (
    mitglied_id INT PRIMARY KEY,
    name VARCHAR(100),
    stadt VARCHAR(50),
    anmeldedatum DATE
);

CREATE TABLE ausleihvorgaenge (
    aus_id INT PRIMARY KEY,
    mitglied_id INT NOT NULL,
    buch_id INT NOT NULL,
    ausleihdatum DATE,
    rueckgabedatum DATE,
    FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id),
    FOREIGN KEY (buch_id) REFERENCES buecher(buch_id)
);
```

### Aufgabenteile

#### a) Einfache SELECT-Abfrage mit WHERE (1 Punkt)

**Frage:** Schreiben Sie eine SQL-Abfrage, die alle **Bücher der Kategorie "Science Fiction"** anzeigt.

**Ihre Lösung:**
```sql
SELECT * FROM buecher WHERE kategorie = 'Science Fiction';
```

**Bewertung:** Syntax korrekt + WHERE-Bedingung funktioniert = 1 Punkt

#### b) SELECT mit spezifischen Spalten (1 Punkt)

**Frage:** Zeigen Sie den **Namen aller Mitglieder** und ihr **Anmeldedatum** an.

**Ihre Lösung:**
```sql
SELECT name, anmeldedatum FROM mitglieder;
```

**Bewertung:** Spaltenselektion korrekt = 1 Punkt

#### c) JOIN – Mitglieder mit ihren Ausleihvorgängen (2 Punkte)

**Frage:** Schreiben Sie eine Abfrage, die für jeden Ausleihvorgang den **Namen des Mitglieds**, den **Buchtitel** und das **Ausleihdatum** zeigt. Verwenden Sie mindestens einen JOIN.

**Ihre Lösung:**
```sql
SELECT m.name, b.titel, a.ausleihdatum
FROM ausleihvorgaenge a
INNER JOIN mitglieder m ON a.mitglied_id = m.mitglied_id
INNER JOIN buecher b ON a.buch_id = b.buch_id
ORDER BY m.name;
```

**Bewertung:**
- 1 Punkt: Beiden JOINs korrekt
- 1 Punkt: Alle gewünschten Spalten im SELECT

#### d) Aggregation und GROUP BY (1 Punkt – Bonus)

**Frage (Bonus, +1 Punkt):** Wie viele Bücher hat jedes Mitglied ausgeliehen? Zeigen Sie Mitgliedname und Anzahl.

**Ihre Lösung:**
```sql
SELECT m.name, COUNT(a.aus_id) AS anzahl_ausleihvorgaenge
FROM mitglieder m
LEFT JOIN ausleihvorgaenge a ON m.mitglied_id = a.mitglied_id
GROUP BY m.mitglied_id, m.name;
```

**Bewertung:** COUNT, GROUP BY, LEFT JOIN korrekt = 1 Bonus-Punkt

### Bewertung (Gesamt 5 Punkte)

| Aufgabe | Punkte | Kriterien |
|---------|--------|----------|
| a) | 1 | SELECT + WHERE + Bedingung korrekt |
| b) | 1 | SELECT mit Spalten-Liste |
| c) | 2 | Zwei JOINs + alle Spalten |
| d) | +1 | GROUP BY + COUNT + HAVING |

---

## Aufgabe 4: Fehleranalyse – Referentielle Integrität

**Punkte: 6**  
**BPE:** 6.2 – Datenintegrität  
**Zeit:** ~10 Minuten

### Szenario

Ein Nutzer versucht, ein Mitglied aus der Datenbank zu löschen und erhält folgende Fehlermeldung:

```
Error Code: 1451. 
Cannot delete or update a parent row: a foreign key constraint fails 
(`buecher_verleih`.`ausleihvorgaenge`, 
CONSTRAINT `fk_ausleihvorgaenge_mitglied` 
FOREIGN KEY (`mitglied_id`) REFERENCES `mitglieder` (`mitglied_id`))
```

### Aufgabenteile

#### a) Fehlermeldung interpretieren (2 Punkte)

**Frage:** Erklären Sie diese Fehlermeldung in Ihren eigenen Worten.
1. Was ist das Grundproblem?
2. Welche Konzepte sind hier relevant (Fremdschlüssel, referentielle Integrität)?

**Musterlösung:**

**Grundproblem:**
- Das Mitglied kann nicht gelöscht werden, da noch Ausleihvorgänge auf dieses Mitglied verweisen.
- Diese Ausleihvorgänge nutzen die `mitglied_id` als Fremdschlüssel.

**Relevante Konzepte:**
- **Fremdschlüssel:** Der Fremdschlüssel `mitgliel_id` in der Tabelle `ausleihvorgaenge` verweist auf `mitglieder.mitglied_id`
- **Referentielle Integrität:** Diese wird durch die Fremdschlüssel-Constraint gewährleistet. Gelöschte Referenzen würden die Integrität verletzen.

#### b) Praktische Lösungen (2 Punkte)

**Frage:** Nennen Sie mindestens **zwei verschiedene Wege**, dieses Problem zu beheben. Bewerten Sie jeweils Vor- und Nachteile.

**Musterlösung:**

**Option 1: Kaskadierendes Löschen (Cascading Delete)**

```sql
-- Die Ausleihvorgänge erst manuell löschen:
DELETE FROM ausleihvorgaenge WHERE mitglied_id = 42;
-- Dann das Mitglied:
DELETE FROM mitglieder WHERE mitglied_id = 42;
```

| Vorteil | Nachteil |
|---------|---------|
| Datenbank bleibt konsistent | Datenverlust möglich |
| Einfache kontrollierte Löschung | Mehrere Schritte nötig |
|  | Fehleranfällig |

**Option 2: ON DELETE CASCADE (Automatische Löschung)**

```sql
-- Constraint umgestellen:
ALTER TABLE ausleihvorgaenge 
DROP FOREIGN KEY fk_ausleihvorgaenge_mitglied;

ALTER TABLE ausleihvorgaenge 
ADD CONSTRAINT fk_ausleihvorgaenge_mitglied
FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id)
ON DELETE CASCADE;
```

| Vorteil | Nachteil |
|---------|---------|
| Automatische Löschung | Unkontrollierter Datenverlust möglich |
| Weniger manuelle Schritte | Schema-Änderung erforderlich |
|  | Datenverlust schwer zu verhindern |

**Option 3: Soft Delete (Status-Flag)**

```sql
-- Statt zu löschen, Status ändern:
UPDATE mitglieder SET status = 'inaktiv' WHERE mitglied_id = 42;

-- Bei Abfragen nur aktive Mitglieder abfragen:
SELECT * FROM mitglieder WHERE status = 'aktiv';
```

| Vorteil | Nachteil |
|---------|---------|
| Keine Datenverluste | Zusätzliche Komplexität |
| Audit-Trail möglich | Abfragen müssen Filter setzten |
| Historische Daten erhalten | Zusätzliche Spalte nötig |

#### c) SQL-Befehle für Löschung (2 Punkte)

**Frage:** Schreiben Sie die SQL-Befehle auf, um das Mitglied mit ID `42` **sicher zu löschen**, nachdem Sie alle Abhängigkeiten behandelt haben.

**Musterlösung:**

```sql
-- Schritt 1: Alle Ausleihvorgänge für Mitglied 42 löschen
DELETE FROM ausleihvorgaenge WHERE mitglied_id = 42;

-- Schritt 2: Mitglied löschen
DELETE FROM mitglieder WHERE mitglied_id = 42;

-- Verifizierung:
SELECT * FROM mitglieder WHERE mitglied_id = 42;  -- Sollte leer sein
```

**Bewertung:**
- 1 Punkt: Zunächst Ausleihvorgänge löschen
- 1 Punkt: Dann Mitglied löschen (oder Verifizierung)

### Bewertung (Gesamt 6 Punkte)

| Teil | Punkte | Kriterien |
|------|--------|----------|
| a) | 2 | Fremdschlüssel + Integrität erklärt |
| b) | 2 | Zwei Lösungen mit Pro/Contra |
| c) | 2 | DELETE-Befehle in korrekter Reihenfolge |

---

## Aufgabe 5: Datenbankoptimierung – Indizes

**Punkte: 9**  
**BPE:** 6.5 – Performance  
**Zeit:** ~15 Minuten

### Szenario

Die Bücherei-Datenbank hat jetzt **500.000 Ausleihvorgänge** im letzten Jahr. Die Abfrage nach Ausleihen eines bestimmten Mitglieds dauert mehrere Sekunden:

```sql
SELECT * FROM ausleihvorgaenge WHERE mitglied_id = 1234;
```

### Aufgabenteile

#### a) Performance-Problem analysieren (1,5 Punkte)

**Frage:** Warum dauert diese Abfrage mehrere Sekunden bei 500.000 Einträgen? Erklären Sie den Unterschied zwischen indexierter und nicht-indexierter Suche.

**Musterlösung:**

**Ohne Index:**
- Datenbankengine muss **alle 500.000 Zeilen durchlaufen** (Full Table Scan)
- Für jede Zeile wird die `WHERE`-Bedingung überprüft
- Komplexität: **O(n)** – linear

**Mit Index:**
- Der Index ist wie ein **Inhaltsverzeichnis** in einem Buch
- Datenbankengine kann direkt auf die relevanten Einträge zugreifen (B-Tree oder Hash)
- Komplexität: **O(log n)** – logarithmisch
- Typischer Speedup: 100-1000x schneller bei großen Datenmengen

#### b) Index erstellen (2 Punkte)

**Frage:** Schreiben Sie einen SQL-Befehl, um einen Index auf der Spalte `mitglied_id` zu erstellen. Warum ist ein aussagekräftiger Name wichtig?

**Musterlösung:**

```sql
-- Index erstellen
CREATE INDEX idx_ausleihvorgaenge_mitglied_id 
ON ausleihvorgaenge(mitglied_id);
```

**Namenskonvention:**
- `idx_` = Präfix für Index
- `ausleihvorgaenge` = Tabellenname
- `mitglied_id` = Spalte(n), die indexiert werden

**Warum aussagekräftig:**
- Dokumentation: Andere Entwickler erkennen schnell, welche Abfragen optimiert werden
- Fehlersuche: Bei Performance-Problemen leicht zu finden
- Wartbarkeit: Indizes können gezielt verwaltet/gelöscht werden

#### c) Multi-Column Index (2 Punkte)

**Frage:** Die Bücherei nutzt häufig diese Abfrage:

```sql
SELECT * FROM ausleihvorgaenge 
WHERE mitglied_id = 1234 AND buch_id = 5;
```

Würde der Index aus Aufgabe b) für diese Abfrage reichen? Falls nein, wie würde Sie ihn optimieren?

**Musterlösung:**

**Würde der Index reichen?** Teilweise ja, aber nicht optimal.
- Der Index auf `mitglied_id` hilft, aber nicht für die `buch_id`-Bedingung
- Die Datenbankengine könnte die 500.000 Zeilen einmal auf `mitglied_id` filtern, dann die Ergebnisse nochmal auf `buch_id` filtern

**Bessere Lösung: Composite Index**

```sql
-- Composite (Multi-Column) Index
CREATE INDEX idx_ausleihvorgaenge_mitglied_buch 
ON ausleihvorgaenge(mitglied_id, buch_id);
```

**Warum besser:**
- Beide Bedingungen werden in einem Schritt verarbeitet
- Weniger Zeilen-Scans notwendig
- Komplexität bleibt **O(log n)**, aber mit kürzeren Zugriffszeiten

#### d) Nachteile von Indizes (1,5 Punkte)

**Frage:** Indizes beschleunigen Lesezugriffe, haben aber auch Nachteile. Nennen Sie zwei Nachteile und erklären Sie diese.

**Musterlösung:**

**Nachteil 1: Speicherplatz**
- Jeder Index benötigt zusätzlichen Festplattenspeicher
- Mit 500.000 Ausleihvorgängen kann ein Index mehrere GB belegen
- Bei vielen Indizes kann der Speicherverbrauch problematisch werden

**Nachteil 2: Schreibperformance & Maintenance**
- **INSERT:** Wenn ein neuer Ausleihvorgang hinzukommt, muss der Index auch aktualisiert werden
- **UPDATE:** Wenn `mitglied_id` geändert wird, müssen beide Original- und neuer Indexeintrag aktualisiert werden
- **DELETE:** Der Indexeintrag muss auch gelöscht werden
- **Resultat:** INSERT/UPDATE/DELETE werden 10-50% langsamer

**Trade-off:**
- Indizes sind nur sinnvoll, wenn es **viele Lesezugriffe** (SELECT) und **wenige Schreib­zugriffe** (INSERT/UPDATE/DELETE) gibt
- Für Abfragen mit häufigen Änderungen: Indizes sind kontraproduktiv

#### e) Weitere Optimierungen (2 Punkte)

**Frage:** Nennen Sie zwei weitere Möglichkeiten zur Datenbankoptimierung (ohne Indizes).

**Musterlösung:**

| Optimierungsmethode | Erklärung | Anwendung |
|---------------------|-----------|-----------|
| **Query-Optimierung** | Umschreiben von ineffizienten SQL-Befehlen | Unnötige JOINs entfernen, WHERE-Bedingungen optimieren |
| **Partitionierung** | Große Tabellen in kleinere Teile aufteilen (z.B. nach Jahr) | 500.000 Zeilen → 5 Partition × 100.000 Zeilen |
| **Caching** | Häufig abgerufene Daten im RAM speichern | Redis, Memcached für Queries mit konstanten Ergebnissen |
| **Denormalisierung** | Kontrollierte Redundanz für häufige Abfragen | Aggregates speichern statt zu berechnen |
| **Archivierung** | Alte Daten in separate Tabelle verschieben | 2023-2024 Ausleihvorgänge in `archive_ausleihvorgaenge` |

### Bewertung (Gesamt 9 Punkte)

| Teil | Punkte | Kriterien |
|------|--------|----------|
| a) | 1,5 | O(n) vs. O(log n) erklärt |
| b) | 2 | CREATE INDEX korrekt + Namenskonvention |
| c) | 2 | Composite Index + Begründung |
| d) | 1,5 | Zwei Nachteile mit Erklärung |
| e) | 2 | Zwei weitere Optimierungen |

---

# TEIL B: Programmierung mit I/O & Struktogramme (3 Punkte / 10%)

## Aufgabe 6: Programmierung – Benutzereingabe & Validierung

**Punkte: 3**  
**BPE:** 5.1 – Programme mit I/O und Struktogramme  
**Zeit:** ~15 Minuten

### Aufgabenstellung

Sie sollen ein Programm schreiben, das eine **Postleitzahl** validiert. Eine gültige deutsche Postleitzahl:
- Hat genau **5 Ziffern**
- Besteht **nur aus Ziffern** (keine Buchstaben)
- Beginnt nicht mit **"0"** (führende Null nicht erlaubt)

Das Programm soll den Benutzer solange auffordern, eine gültige Postleitzahl einzugeben, bis eine korrekte Eingabe erfolgt.

### Aufgabenteile

#### a) Struktogramm (1,5 Punkte)

**Aufgabe:** Erstellen Sie ein **Struktogramm** nach BW-Standard-Notation für die Validierungslogik.

**Sollte enthalten:**
1. Eingabeaufforderung
2. Validierungsprüfungen (alle drei Bedingungen)
3. Wiederholungsschleife bei ungültiger Eingabe
4. Ausgabe bei erfolgreicher Validierung

**Hinweis:** Handgezeichnete Struktogramme sind **völlig akzeptabel!**

**Musterlösung (Text-Notation):**

```
┌─────────────────────────────────────────────┐
│ START                                       │
└─────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ WIEDERHOLE (DO-WHILE)                      │
└─────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ Eingabe: "PLZ (5 Ziffern):"                │
│ plz_eingabe                                 │
└─────────────────────────────────────────────┘
               │
               ▼
        ┌──────┴──────┐
        │  IST         │ NEIN
        │  len(plz) ═ 5? →─────┐
        │ UND          │        │
        │  alle Ziffern? │        │
        │ UND          │        │
        │  plz[0] ≠ '0'? │        │
        ├──────┤        │
        │      │        │
       JA      │        │
        │      │        │
        ▼      │    ┌───┴────────────────────┐
     gültig=  │    │ Ausgabe:               │
     WAHR     │    │ "Ungültiges Format!"  │
        │      │    │ gültig = FALSCH       │
        │      │    └───┬────────────────────┘
        │      │        │
        └──────┴────────┘
               │
        ▼ (gültig = WAHR)
┌─────────────────────────────────────────────┐
│ Ausgabe: "Postleitzahl gültig: " plz       │
└─────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ END                                         │
└─────────────────────────────────────────────┘
```

**Bewertung (a):**
- ✅ **1,0 Punkt:** Schleife, Bedingung, Ausgabe korrekt strukturiert
- ✅ **0,5 Punkte:** Symbole erkennbar (auch handgezeichnet OK)

#### b) Python-Code (1,5 Punkte)

**Aufgabe:** Implementieren Sie das Struktogramm in Python. Der Code soll:
1. Benutzer zur Eingabe auffordern
2. **Alle drei Validierungskriterien** prüfen
3. Bei Fehler informative Fehlermeldung ggeben
4. Bei Erfolg die PLZ bestätigen und Programm beenden

**Ihre Lösung:**

```python
# Ihre Lösung:
```

**Musterlösung:**

```python
# Postleitzahl-Validator
valid = False

while not valid:
    plz_eingabe = input("Geben Sie eine Postleitzahl (5 Ziffern) ein: ")
    
    # Bedingungen prüfen
    if len(plz_eingabe) != 5:
        print("Fehler: Postleitzahl muss genau 5 Ziffern haben.")
    elif not plz_eingabe.isdigit():
        print("Fehler: Postleitzahl darf nur Ziffern enthalten.")
    elif plz_eingabe[0] == '0':
        print("Fehler: Postleitzahl darf nicht mit 0 beginnen.")
    else:
        # Alle Bedingungen erfüllt
        valid = True
        print(f"✓ Postleitzahl gültig: {plz_eingabe}")

# Optional: PLZ verarbeiten
import datetime
print(f"Eingabe erfolgreich abgeschlossen um {datetime.datetime.now().strftime('%H:%M:%S')}")
```

**Alternativer kompakterer Code:**

```python
valid = False

while not valid:
    plz = input("PLZ (5 Ziffern): ")
    
    # Alle Bedingungen in einer if-else prüfen
    if len(plz) == 5 and plz.isdigit() and plz[0] != '0':
        print(f"✓ {plz} ist gültig!")
        valid = True
    else:
        print("Ungültig! Bitte 5-stellige PLZ ohne führende Null eingeben.")
```

**Bewertung (b):**

| Kriterium | Punkte |
|----------|--------|
| Schleife funktioniert | 0,5 |
| Alle 3 Validierungen + logische Verknüpfung | 0,75 |
| Fehlerbehandlung & aussagekräftige Ausgaben | 0,25 |
| **Gesamt** | **1,5** |

### Testfall-Beispiel

```
Input:  "02345"
Output: "Fehler: Postleitzahl darf nicht mit 0 beginnen."

Input:  "2A3B5"
Output: "Fehler: Postleitzahl darf nur Ziffern enthalten."

Input:  "23"
Output: "Fehler: Postleitzahl muss genau 5 Ziffern haben."

Input:  "75001"
Output: "✓ Postleitzahl gültig: 75001"
```

---

# ZUSAMMENFASSUNG

## Punkte-Übersicht

| Aufgabe | Thema | Punkte | BPE |
|---------|-------|--------|-----|
| 1 | Grundkonzepte RDB | 3 | BPE 6 |
| 2 | Datenbankdesign & Normalisierung | 4 | BPE 6 |
| 3 | SQL SELECT & JOIN | 5 | BPE 6 |
| 4 | Fehleranalyse & Integrität | 6 | BPE 6 |
| 5 | Performance & Indizes | 9 | BPE 6 |
| 6 | Programmierung & Struktogramme | 3 | BPE 5.1 |
| **GESAMT** | | **30** | **BPE 6: 27 (90%) / BPE 5.1: 3 (10%)** |

## Bewertungsrichtlinien für Lehrende

### Allgemeine Prinzipien

✅ **Struktur vor Perfektionismus:** Handgezeichnete Struktogramme sind OK  
✅ **Nachvollziehbarkeit:** Jeder Schritt muss lesbar sein  
✅ **Logik vor Syntax:** Logikfehler −1 bis −2 Pkte; Syntaxfehler −0,25 bis −0,5 Pkte  
✅ **Teilpunkte:** Nicht alles-oder-nichts vergeben (außer explizit markiert)  

### Häufige Fehler und Punktabzug

| Fehler | Fachgebiet | Abzug | Beispiel |
|--------|-----------|-------|---------|
| WHERE vor FROM (SQL-Syntax) | SQL | −0,5 | `FROM ... WHERE` statt `WHERE ... FROM` |
| Fremdschlüssel in JOIN vergessen | SQL | −0,5 bis −1 | `FROM t1, t2` statt JOIN |
| Primärschlüssel in EERM nicht gekennzeichnet | Design | −0,5 | Keine Unterstreichung oder PK-Notation |
| Struktogramm-Symbole unklar | Programmierung | −0,5 | Rautenform nicht erkennbar |
| `input()` oder `while` vergessen | Python | −0,5 bis −1 | Nur Print-Statement, keine Interaktion |
| Logik-Fehler (endlosSchleife, falsche Bedingung) | Programmierung | −1 bis −1,5 | `while True` ohne `break` |
| Keine Fehlerbehandlung (try/except) | Python | −0,25 (nicht schlecht) | Aber Robustheit wichtiger als try/except |

### Checkliste für Lehrende

- [ ] Aufgabe 1: Alle 5 Konzept-Aussagen eindeutig mit r/f bewertet
- [ ] Aufgabe 2: ERD zeigt 1:N oder N:M Beziehungen mit Kardinalitäten
- [ ] Aufgabe 3: Abfrage c) hat mindestens 2 JOINs und alle gewünschten Spalten
- [ ] Aufgabe 4: Fehlermeldung wird korrekt interpretiert (FK + Referentielle Integrität)
- [ ] Aufgabe 5: Index-Plan ist sinnvoll; Nachteile realistisch erwähnt
- [ ] Aufgabe 6: Struktogramm logisch geschlossen; while-Schleife funktioniert

---

# Anhang: Lösungsblatt (gekürzt)

## Aufgabe 2b – Tabellen-Struktur (Lösung)

```sql
CREATE TABLE buecher (
    buch_id INT PRIMARY KEY AUTO_INCREMENT,
    titel VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    isbn VARCHAR(13),
    kategorie VARCHAR(50),
    preis DECIMAL(8,2)
);

CREATE TABLE mitglieder (
    mitglied_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    adresse VARCHAR(200),
    stadt VARCHAR(50),
    anmeldedatum DATE DEFAULT CURDATE()
);

CREATE TABLE ausleihvorgaenge (
    aus_id INT PRIMARY KEY AUTO_INCREMENT,
    mitglied_id INT NOT NULL,
    buch_id INT NOT NULL,
    ausleihdatum DATE DEFAULT CURDATE(),
    rueckgabedatum DATE,
    FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id),
    FOREIGN KEY (buch_id) REFERENCES buecher(buch_id)
);
```

---

## Änderungshistorie

| Version | Datum | Autor | Änderungen |
|---------|-------|-------|-----------|
| 1.0 | 2025-05-09 | KI-Generation | Muster-Klassenarbeit erstellt; Online-Bücherverleih Szenario |

---

**Hinweis für die Nutzung:** Diese Musterklassenarbeit kann als Vorlage für weitere Klassenarbeiten genutzt werden. Ändern Sie das Szenario (z.B. andere Domäne wie "Hotelreservierungssystem", "Produktverwaltung"), behalten Sie aber die Struktur und Schwerpunkte (BPE 6: 90%, BPE 5.1: 10%) bei.

