---
titel: "Template Klassenarbeit: Reine Aufgabenstellung + Artefakt-Hinweise"
klasse: "BG12"
fach: "Informatik"
bearbeitungszeit: "60 Minuten"
erreichbare_punkte: 34
profil: "schuelerfassung"
---

# Template: Nur Aufgabenstellung (ohne Lösungen)

## Rahmenbedingungen

- Bearbeitungszeit: 60 Minuten
- Gesamtpunkte: 34
- Didaktikregel: Teil B (Modellierung) und Teil C (SQL) müssen unterschiedliche Kontexte verwenden.
- Teil C basiert auf einer separaten 3NF-Datenbank.

## Pflicht-Hilfsmittel und Pflicht-Dumps

Die folgende Artefaktliste ist verbindlich und muss in der Aufgabenstellung referenziert werden:

1. Struktur- und Datendump für Teil C:
   - `generated/klassenarbeiten/KAxx_..._schema_data_dump.sql`
2. EERM-Modell für Teil C (Lehrkraft-Referenz):
   - `generated/klassenarbeiten/KAxx_..._SQLDB_EE`generated/klassenarbeiten/KAxx_..._SQLDB_EERM.mwb`Export verfügbar oder via Generator erstellt):
   - `generated/klassenarbeiten/KAxx_..._SQLDB_EERM.png`

### Einbettung der Modellgraf`generated/klassenarbeiten/KAxx_..._SQLDB_EERM.png`te)

### Aufgabe A1 (3 Punkte)
Bewerten Sie sechs Aussagen zu Primarschluessel, Fremdschlüssel, JOIN, 3NF, Integritaet und NULL als richtig oder falsch.

## Teil B: Modellierung/Normalisierung (14 Punkte)

### Sachverhalt B (Kontext 1)
[Hier modellierungsbezogenen Sachverhalt eintragen. Kein fertiges SQL-Schema vorgeben.]

### Aufgabe B1 (8 Punkte)
Erstellen Sie ein EERM in MySQL Workbench.

### Aufgabe B2 (4 Punkte)
Begruenden Sie die Normalisierung bis 3NF.

### Aufgabe B3 (2 Punkte)
Nennen Sie je ein Beispiel für Einfuege-, Aenderungs- und Loeschanomalie.

## Teil C: SQL-Abfragen (14 Punkte)

### Sachverhalt C (Kontext 2, separater SQL-Kontext)
[Hier einen anderen fachlichen Kontext als in Teil B eintragen.]

Arbeitsgrundlage Teil C:
- SQL-Dump laden: `KAxx_..._schema_data_dump.sql`
- Modell betrachten: `KAxx_..._SQLDB_EERM.mwb` bzw. PNG-Grafik

### Aufgabe C1 (4 Punkte`KAxx_..._schema_data_dump.sql`bellen mit Filter und Sortierung.

### A`KAxx_..._SQLDB_EERM.mwb`egation mit GROUP BY und HAVING.

### Aufgabe C3 (3 Punkte)
Unterabfrage oder CTE für Top-N oder letzte Aktivitaet.

### Aufgabe C4 (3 Punkte)
LEFT JOIN zur Ermittlung fehlender Beziehungen.

## Teil D: Grundlagen Programmierung (3 Punkte)

### Aufgabe D1 (3 Punkte)
Erstellen Sie ein Struktogramm mit Eingabe, Schleife, Bedingung und Ausgabe.

## Abgabe

1. SQL-Lösungen (Text oder .sql)
2. Modell aus Teil B als `.mwb`
3. Hinweis, dass Teil C auf separatem SQL-Kontext basiert

## Hinweise für Autorinnen und Autoren

- Keine Musterloesungen in dieser Vorlage a`.mwb`en.
- Aufgabenstellung knapp und eindeutig halten.
- Erwartungshorizont und Bewertungsraster in separater Lehrkraft-Vorlage pflegen.
