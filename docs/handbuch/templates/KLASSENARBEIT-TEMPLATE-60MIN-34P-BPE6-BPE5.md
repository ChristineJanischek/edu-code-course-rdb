---
titel: "Klassenarbeit: Relationale Datenbanken (60 Min)"
klasse: "BG12"
fach: "Informatik"
bearbeitungszeit: "60 Minuten"
erreichbare_punkte: 34
punkteherleitung:
  ausgangslage: "210 Minuten, 3 Aufgabenteile, je 40 Punkte"
  gesamtpunkte_pruefung: 120
  berechnung: "120 * (60/210) = 34,29"
  gerundet: 34
gewichtung:
  modellierung_normalisierung_anomalien: "40% = 14 Punkte"
  abfragen_mehrtabellen: "40% = 14 Punkte"
  theorie_mc: "10% = 3 Punkte"
  programmierung_struktogramm: "10% = 3 Punkte"
---

# Template Klassenarbeit 60 Minuten

## Rahmen

- Bearbeitungszeit: 60 Minuten
- Gesamtpunkte: 34
- Tool-Hinweis: Modellierung als EERM in MySQL Workbench
- Abgabe-Artefakte:
  - EERM-Modell als .mbw (schulinterner Standard)
  - Struktur- und Datendump als .sql

## Punkteverteilung

| Bereich | Anteil | Punkte |
|---|---:|---:|
| Modellierung, Normalisierung, Anomalien | 40% | 14 |
| SQL-Abfragen über viele Tabellen | 40% | 14 |
| Theorie (Multiple Choice) | 10% | 3 |
| Grundlagen Programmierung (Struktogramm) | 10% | 3 |
| Gesamt | 100% | 34 |

## Aufgabenteile

### Teil A: Theorie (3 Punkte, 5 Minuten)

#### Aufgabe 1: Theorie (Multiple Choice) – 3 Punkte
- 6 Aussagen zu PK/FK, JOIN, Normalformen, Integritaet, Index, NULL.
- Bewertung: 0,5 Punkte pro korrekter Aussage.

### Teil B: EERM + Normalisierung + Anomalien (14 Punkte, 25 Minuten)

#### Aufgabe 3: EERM in MySQL Workbench
Sachverhalt: Eine Kursplattform verwaltet Teilnehmende, Lehrkräfte, Kursangebote, Kursdurchführungen und Buchungen. Ein Kurs kann von mehreren Lehrkräften betreut werden, Lehrkräfte können mehrere Kurse übernehmen. Auswertungen sollen später beantworten, wer wann welchen Kurs gebucht hat und welche Lehrkräfte ohne Zuordnung bleiben.

- b1) EERM erstellen (8 Punkte)
  - Leiten Sie ein konsistentes EERM aus dem Sachverhalt ab und modellieren Sie es in MySQL Workbench.
- b2) Normalisierung begruenden bis 3NF (4 Punkte)
  - Funktionale Abhängigkeiten, Redundanzabbau.
- b3) Anomalien benennen (2 Punkte)
  - Einfüge-, Änderungs-, Löschanomalie mit je einem Beispiel.

### Teil C: SQL-Abfragen über viele Tabellen (14 Punkte, 25 Minuten)

#### Aufgabe 4: Mehrtabellenabfragen
Arbeitsgrundlage: bereitgestellter SQL-Dump.

- c1) JOIN über 4 Tabellen mit Filter und Sortierung (4 Punkte)
- c2) Aggregation pro Elternentitaet mit GROUP BY/HAVING (4 Punkte)
- c3) Unterabfrage oder CTE für Top-N/letzte Aktivität (3 Punkte)
- c4) Abfrage mit LEFT JOIN zur Identifikation fehlender Beziehungen (3 Punkte)

### Teil D: Grundlagen Programmierung (3 Punkte, 5 Minuten)

#### Aufgabe 2: Struktogramm (am Ende bearbeiten)
- Erstellen Sie ein Struktogramm für eine einfache Eingabeprüfung (z. B. Punkte 0-50).
- Muss enthalten: Eingabe, Schleife, Bedingung, Ausgabe.
- Keine Arrays und keine Listen verwenden (BPE 7, nicht BPE 5.1).
- Bewertung:
  - Logik korrekt: 1,5
  - Strukturblocke korrekt: 1,0
  - Lesbarkeit/Notation: 0,5

## Abgabeformat

1. Datei: KAxx_..._EERM.mbw
2. Datei: KAxx_..._schema_data_dump.sql
3. SQL-Loesungen als Text oder .sql

## Hinweise für Lehrkraft

- Parent-Tabellen im Dump mit ca. 20 Datensaetzen (z. B. mitglieder, dozenten).
- Aufgabenstellung knapp halten; Fokus auf Kernkompetenzen.
- In Workbench: EERM visuell prüfen (PK/FK, Kardinalitäten, N:M).
