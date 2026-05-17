---
titel: "Klassenarbeit BG12 2025/2026: EERM und SQL (60 Min)"
klasse: "BG12"
schuljahr: "2025-2026"
fach: "Informatik"
bearbeitungszeit: "60 Minuten"
erreichbare_punkte: 34
verteilung:
  modellierung_normalisierung_anomalien: 14
  abfragen_mehrtabellen: 14
  theorie_mc: 3
  struktogramm: 3
artefakte:
  modellierung_eerm_lehrkraft: "kursplattform_2025.mwb"
  sql_db_dump: "stadtfahrradverleih_struktur_2025.sql"
  sql_db_daten: "stadtfahrradverleih_daten_2025.sql"
  sql_db_eerm: "stadtfahrradverleih_2025.mwb"
  sql_db_eerm_grafik: "stadtfahrradverleih_2025.png"
fassung: aufgaben
---

# Klassenarbeit (60 Minuten)

**Klasse/Kurs:** BG12 | **Schuljahr:** 2025/2026 | **Bearbeitungszeit:** 60 Minuten | **Erreichbare Punkte:** 34

---

## Struktur

| Teil | Inhalte | Punkte | Zeit |
|---|---|---:|---:|
| A | Theorie (MC) | 3 | 5 Min |
| B | EERM, Normalisierung, Anomalien | 14 | 25 Min |
| C | SQL-Abfragen über mehrere Tabellen | 14 | 25 Min |
| D | Grundlagen Programmierung (Struktogramm) | 3 | 5 Min |
| **Gesamt** |  | **34** | **60 Min** |

---

## Teil A (3 Punkte)

### Aufgabe 1: Theorie (Multiple Choice) – 3 Punkte
Markieren Sie richtig/falsch. (0,5 Punkte je Aussage)

| Nr. | Aussage | r/f |
|-----|---------|-----|
| 1 | Ein Fremdschlüssel darf mehrfach vorkommen. | |
| 2 | Eine N:M-Beziehung wird in relationalen Modellen direkt ohne Zwischentabelle gespeichert. | |
| 3 | Ein LEFT JOIN kann Datensätze ohne Partner auf der rechten Seite sichtbar machen. | |
| 4 | Die 3NF reduziert Redundanz und Anomalien. | |
| 5 | Ein Primärschlüssel darf NULL sein. | |
| 6 | HAVING filtert Gruppen nach GROUP BY. | |

---

## Teil B (14 Punkte): EERM in MySQL Workbench

**Wichtig:** Teil B ist eine reine Modellierungsaufgabe. Es wird bewusst kein fertiges SQL-Schema vorgegeben. Die Struktur muss selbst aus dem Sachverhalt entwickelt werden.

### Aufgabe 3.1: EERM modellieren – 8 Punkte

**Sachverhalt Modellierung (Kontext 1):**

Eine Bildungseinrichtung betreibt eine Kursplattform. Teilnehmende buchen Kurse zu konkreten Terminen. Lehrkräfte betreuen Kurse, zum Teil im Team. Die Schulleitung benötigt später Auswertungen zu Buchungen pro Person, Terminen pro Kurs und Lehrkräften ohne aktive Zuordnung.

**Auftrag:** Leiten Sie aus dem Sachverhalt ein geeignetes EERM in MySQL Workbench ab. Begruenden Sie Ihre Modellierungsentscheidungen kurz.

### Aufgabe 3.2: Normalisierung bis 3NF – 4 Punkte
- Benennen Sie 2 funktionale Abhängigkeiten.
- Begruenden Sie, warum das Modell in 3NF liegt.

### Aufgabe 3.3: Anomalien – 2 Punkte
Nennen Sie je ein Beispiel:
- Einfügeanomalie
- Änderungsanomalie
- Löschanomalie

---

## Teil C (14 Punkte): SQL-Abfragen über mehrere Tabellen

**Separater SQL-Kontext (3NF, Kontext 2) – anderen Kontext als Modellierung:**
Fuer Teil C wird absichtlich einen anderen Kontext verwendet als in Teil B (Kontext 1), damit die Modellierungslösung aus Teil B nicht indirekt vorgegeben wird.
Die didaktische Trennung ist essenziell für die Unabhaengigkeit der Aufgabenteile.

**Konkreter Sachverhalt:**
Ein kommunaler Stadtfahrradverleih verwaltet Kundinnen und Kunden, Stationen, Fahrräder, Ausleihen, Zahlungen und Wartungen (6 Entitätstypen). Die bereitgestellte Übungsdatenbank ist bereits in 3NF modelliert.

**Arbeitsgrundlage:**
- SQL-Struktur: `stadtfahrradverleih_struktur_2025.sql`
- SQL-Daten: `stadtfahrradverleih_daten_2025.sql`
- EERM-Referenzgrafik: `stadtfahrradverleih_2025.png`

![EERM Teil C - separater SQL-Kontext](./stadtfahrradverleih_2025.png)

### Aufgabe 4.1 (4 Punkte)
Geben Sie für jede abgeschlossene Ausleihe den Kundennamen, die Fahrradnummer, den Fahrradtyp, Start- und Zielstation sowie den Zahlbetrag aus.
Sortierung: Kundennachname, Startzeit.

### Aufgabe 4.2 (4 Punkte)
Ermitteln Sie je Kundin/Kunde die Anzahl abgeschlossener Ausleihen. Zeigen Sie nur Personen mit mindestens 2 abgeschlossenen Ausleihen.

### Aufgabe 4.3 (3 Punkte)
Geben Sie pro Station den letzten Ausleihstart und die Anzahl unterschiedlicher Kundinnen/Kunden aus, die dort gestartet sind.

### Aufgabe 4.4 (3 Punkte)
Finden Sie Fahrräder ohne dokumentierte Wartung (LEFT JOIN).

---

## Teil D (3 Punkte): Grundlagen Programmierung

### Aufgabe: Struktogramm – Fahrradverleih Kostenberechnung

Ein Kunde möchte wissen, wie viel eine Fahrradausleihe kostet.
Erstellen Sie ein **Struktogramm** (gemäß Operatorenliste für Struktogramme) für folgende Verarbeitung:

- **Eingabe:** Anzahl der Ausleih-Tage und Tagespreis in Euro
- **Verarbeitung:** Berechnung der Gesamtkosten
- **Ausgabe:** Gesamtkosten in Euro

**Hinweis:** Verwenden Sie ausschliesslich Sequenz-Bloecke (EVA-Prinzip).
Kontrollstrukturen (Schleifen, Verzweigungen) werden **nicht** bewertet und sind nicht erforderlich.

| Bewertungskriterium | Punkte |
|---|---:|
| Struktogramm-Rahmen (ANFANG/ENDE) und 3 Sequenzblöcke vollständig | 1,0 |
| Berechnungsformel korrekt (Zuweisung mit :=) | 1,5 |
| Variablennamen und Lesbarkeit | 0,5 |
| **Gesamt** | **3,0** |

---

## Abgabe

- EERM-Modellierung Teil B (von Schuelern erstellt): als `.mwb`-Datei abgeben
- SQL-Lösungen Teil C: als Datei oder Text
