# Stichwortverzeichnis Relationale Datenbanken (BPE 3)

Dieses Dokument unterstützt dich beim selbstgesteuerten Lernen im Fernstudium.
Alle Begriffe sind alphabetisch sortiert und schülergerecht erklärt.

## So nutzt du dieses Dokument

- Lese bei einer Aufgabe zuerst den Begriff nach, den du nicht verstehst.
- Nutze danach die Beispielzeile, um den Begriff direkt in SQL oder im EERM wiederzuerkennen.
- Arbeite beim Modellieren immer mit dem 3NF-Fokus: erst fachlich korrekt, dann technisch umsetzen.

> **Tipp: Suchfunktion nutzen**
> Die durchsuchbare Version mit Live-Filter findest du in der HTML-Datei:
> `stichwortverzeichnis_relationale_datenbanken.html`
> Rechtsklick auf die Datei im Explorer → **„Open with Live Server"** → Begriff eintippen, fertig.
> Eine ausführliche Schritt-für-Schritt-Anleitung steht in der [README.md](./README.md).

## Lernweg zur 3. Normalform (3NF)

1. Sachverhalt in Entitäten, Attribute und Beziehungen zerlegen.
2. Primärschlüssel und Fremdschlüssel sauber festlegen.
3. Redundanzen und Anomalien sichtbar machen.
4. 1NF, 2NF und 3NF nacheinander prüfen.
5. Danach SQL für Erfassung, Änderung, Löschung und Auswertung formulieren.

## Alphabetisches Stichwortverzeichnis

| Begriff | Definition (verständlich) | Beispiel |
|---|---|---|
| 1. Normalform (1NF) | In jeder Zelle steht genau ein einzelner Wert, keine Liste und kein Mehrfachwert. | Statt "Mathe, Informatik" in einer Zelle: eigene Tabelle mit mehreren Zeilen je Person. |
| 2. Normalform (2NF) | Alle Nichtschlüsselattribute hängen vom gesamten Primärschlüssel ab, nicht nur von einem Teil. | Bei (SchülerID, KursID) darf "Schülername" nicht in derselben Tabelle stehen. |
| 3. Normalform (3NF) | Es gibt keine indirekten Abhängigkeiten zwischen Nichtschlüsselattributen. | Raumname gehört in die Tabelle RAUM, nicht zusätzlich in KURS. |
| Aggregatfunktion | Funktion, die viele Zeilen zu einem Ergebnis zusammenfasst. | COUNT(*), SUM(preis), AVG(punkte). |
| ALTER TABLE | SQL-Befehl zum Ändern einer vorhandenen Tabelle. | Spalte hinzufügen: ALTER TABLE kunde ADD telefon VARCHAR(30). |
| AND | Verknüpft Bedingungen, sodass alle Bedingungen wahr sein müssen. | WHERE ort='Stuttgart' AND aktiv=1 |
| Anomalie | Unerwünschter Nebeneffekt durch schlechte Datenstruktur. | Beim Löschen einer Bestellung verschwindet versehentlich auch die letzte Produktinfo. |
| AS (Alias) | Vergibt einen Kurznamen für Spalten oder Tabellen. | SELECT k.name AS kundenname FROM kunden k |
| Attribut | Eigenschaft einer Entität oder Tabelle. | Kundennummer, Nachname, Geburtsdatum. |
| Atomarität | Eigenschaft, dass ein Attribut nicht weiter zerlegt als Einzelwert gespeichert ist. | Telefon nur als ein Wert pro Feld, nicht mehrere Nummern in einer Zelle. |
| BETWEEN | Prüft, ob ein Wert in einem Bereich liegt. | WHERE preis BETWEEN 10 AND 50 |
| Beziehung (Relationship) | Fachlicher Zusammenhang zwischen Entitäten. | Ein Kunde hat viele Bestellungen. |
| Cardinality/Kardinalität | Gibt an, wie viele Objekte auf beiden Seiten einer Beziehung möglich sind. | 1:1, 1:n, n:m. |
| CHECK | Bedingung auf Spaltenebene für gültige Werte. | CHECK (punkte >= 0) |
| COUNT | Zählt Datensätze oder Werte. | SELECT COUNT(*) FROM bestellung |
| CREATE DATABASE | Erstellt eine neue Datenbank. | CREATE DATABASE schulshop_db; |
| CREATE TABLE | Erstellt eine neue Tabelle mit Spalten und Datentypen. | CREATE TABLE kunde (kunde_id INT PRIMARY KEY, name VARCHAR(100)); |
| Datenbank | Strukturierte, dauerhaft gespeicherte Datensammlung. | Eine Schulverwaltung mit Tabellen für Schüler, Klassen und Noten. |
| Datenbankmanagementsystem (DBMS) | Software zum Verwalten von Datenbanken. | MySQL, MariaDB, PostgreSQL. |
| Datenkonsistenz | Daten widersprechen sich nicht und erfüllen die Regeln. | Kunde hat genau eine gültige Kundennummer in allen Tabellen. |
| Datensatz (Tupel) | Eine Zeile in einer Tabelle. | Eine konkrete Bestellung mit Datum und Betrag. |
| Datentyp | Legt fest, welche Art Wert gespeichert wird. | INT, VARCHAR, DATE, BOOLEAN. |
| DELETE | Löscht Datensätze aus einer Tabelle. | DELETE FROM bestellung WHERE bestellung_id=17; |
| DISTINCT | Entfernt doppelte Werte im Ergebnis. | SELECT DISTINCT ort FROM kunden |
| DDL (Data Definition Language) | SQL-Befehle für Strukturänderungen. | CREATE, ALTER, DROP. |
| DML (Data Manipulation Language) | SQL-Befehle für Inhalte/Datensätze. | INSERT, UPDATE, DELETE. |
| DROP TABLE | Entfernt eine Tabelle komplett aus der Datenbank. | DROP TABLE archiv_bestellungen; |
| Einfügeanomalie | Problem: Daten können nicht sinnvoll eingefügt werden, ohne andere Daten zu erfinden. | Neuer Kurs kann nicht angelegt werden, weil noch kein Teilnehmer existiert. |
| Entität | Konkretes Objekt der realen Welt. | Eine bestimmte Kundin, ein konkretes Fahrrad. |
| Entitätstyp | Klasse ähnlicher Entitäten, wird meist als Tabelle modelliert. | KUNDE, PRODUKT, RECHNUNG. |
| ER-Modell/EERM | Modell zur Planung von Entitäten, Attributen und Beziehungen. | Vor dem SQL-Umsetzen wird ein EERM in Workbench gezeichnet. |
| FD (Funktionale Abhängigkeit) | Ein Attribut bestimmt ein anderes eindeutig. | kunde_id -> kundename |
| Feld (Spalte) | Eine Spalte in einer Tabelle. | "email" in der Tabelle "kunde". |
| FOREIGN KEY | Fremdschlüssel, der auf Primärschlüssel einer anderen Tabelle zeigt. | bestellung.kunde_id verweist auf kunde.kunde_id |
| FROM | Legt fest, aus welcher Tabelle Daten gelesen werden. | SELECT * FROM kunde |
| GROUP BY | Bildet Gruppen mit gleichen Werten für Auswertungen. | GROUP BY stadt |
| HAVING | Filtert Gruppen nach GROUP BY. | HAVING COUNT(*) >= 2 |
| IN | Prüft, ob ein Wert in einer vorgegebenen Liste enthalten ist. | WHERE stadt IN ('Ulm','Heilbronn') |
| Index | Beschleunigt Suchzugriffe auf Spalten. | Index auf kundennummer für schnelle Suche. |
| INNER JOIN | Liefert nur Zeilen mit Treffern in beiden Tabellen. | Kunden mit vorhandenen Bestellungen. |
| INSERT | Fügt neue Datensätze in eine Tabelle ein. | INSERT INTO kunde (kunde_id, name) VALUES (1, 'Mina'); |
| Integritätsregel | Regel, die gültige Daten sicherstellt. | Primärschlüssel darf nicht NULL sein. |
| IS NULL | Prüft auf fehlende Werte. | WHERE lieferdatum IS NULL |
| JOIN | Verbindet Tabellen über Schlüsselbeziehungen. | kunde JOIN bestellung ON ... |
| Kardinalität | Anzahl möglicher Zuordnungen zwischen Entitäten. | Ein Kurs hat viele Termine (1:n). |
| Kandidatenschlüssel | Attribut oder Attributkombination, die einen Datensatz eindeutig identifiziert. | E-Mail kann Kandidatenschlüssel sein, wenn sie eindeutig ist. |
| LEFT JOIN | Liefert alle Zeilen links, auch ohne Treffer rechts. | Alle Kunden, auch wenn sie nichts bestellt haben. |
| LIKE | Mustervergleich für Texte. | WHERE name LIKE 'Sch%'; |
| Löschanomalie | Beim Löschen gehen unbeabsichtigt weitere wichtige Informationen verloren. | Löschen der letzten Ausleihe löscht indirekt Infos zum Fahrradtyp. |
| MAX | Größter Wert in einer Spalte. | MAX(preis) |
| MIN | Kleinster Wert in einer Spalte. | MIN(preis) |
| n:m-Beziehung | Viele Objekte stehen mit vielen anderen in Beziehung. | Viele Schüler besuchen viele Kurse. |
| Normalisierung | Schrittweises Verbessern der Tabellenstruktur zur Redundanzvermeidung. | Zerlegung einer großen Sammel-Tabelle in mehrere 3NF-Tabellen. |
| NOT | Negiert eine Bedingung. | WHERE NOT status='inaktiv' |
| NOT NULL | Spalte darf keinen leeren Wert enthalten. | name VARCHAR(100) NOT NULL |
| ON | Definiert die Verknüpfungsbedingung bei JOIN. | ON b.kunde_id = k.kunde_id |
| OR | Verknüpft Bedingungen, sodass mindestens eine wahr sein muss. | WHERE ort='Freiburg' OR ort='Karlsruhe' |
| ORDER BY | Sortiert Ergebnisse auf- oder absteigend. | ORDER BY nachname ASC |
| OUTER JOIN | Liefert zusätzlich Zeilen ohne Treffer (je nach LEFT/RIGHT/FULL). | LEFT JOIN zeigt auch Datensätze ohne Beziehung. |
| Primärschlüssel (PRIMARY KEY) | Eindeutiger Schlüssel einer Tabelle. | kunde_id identifiziert jeden Kunden genau einmal. |
| Projektion | Auswahl bestimmter Spalten in einer Abfrage. | SELECT name, stadt FROM kunde |
| Redundanz | Mehrfachspeicherung derselben Information. | Kundename steht unnötig in mehreren Tabellenzeilen. |
| Referentielle Integrität | Fremdschlüssel darf nur auf vorhandene Primärschlüssel zeigen. | Bestellung darf nur existierende Kunde-ID enthalten. |
| Relation | Tabellenartige Darstellung von Daten im relationalen Modell. | Tabelle KUNDE ist eine Relation. |
| RIGHT JOIN | Liefert alle Zeilen rechts, auch ohne Treffer links. | Alle Datensätze der rechten Tabelle bleiben erhalten. |
| Schema | Gesamter Strukturplan der Datenbank. | Enthält Tabellen, Spalten, Schlüssel und Beziehungen. |
| Selektion | Auswahl von Zeilen über Bedingungen. | SELECT * FROM kunde WHERE ort='Mannheim' |
| SELECT | Liest Daten aus einer oder mehreren Tabellen. | SELECT name FROM kunde |
| SQL (Structured Query Language) | Standardsprache für relationale Datenbanken. | Mit SQL werden Daten definiert, geändert und ausgewertet. |
| Subquery (Unterabfrage) | Abfrage innerhalb einer anderen Abfrage. | WHERE preis > (SELECT AVG(preis) FROM produkt) |
| SUM | Bildet die Summe numerischer Werte. | SUM(umsatz) pro Monat. |
| Tabelle | Struktur aus Spalten und Zeilen. | Tabelle "ausleihe" mit Startzeit und Endzeit. |
| Transitive Abhängigkeit | Attribut hängt über ein anderes Nichtschlüsselattribut ab. | kurs_id -> raum_id -> raumname |
| Tupel | Fachbegriff für einen Datensatz (eine Zeile). | Eine einzelne Zeile in BESTELLUNG. |
| UNION | Vereint Ergebnisse zweier SELECTs ohne Duplikate. | Kundenorte aus zwei Tabellen zusammenführen. |
| UNIQUE | Erzwingt eindeutige Werte in einer Spalte. | E-Mail darf nur einmal vorkommen. |
| UPDATE | Ändert bestehende Datensätze. | UPDATE kunde SET ort='Ulm' WHERE kunde_id=3; |
| WHERE | Filtert Zeilen vor Gruppierung. | WHERE aktiv=1 |
| Änderungsanomalie | Eine Änderung muss an vielen Stellen erfolgen und erzeugt leicht Widersprüche. | Neue Telefonnummer müsste in 20 Zeilen korrigiert werden. |

## SQL-Klausel-Kompass (schneller Überblick)

- Struktur aufbauen: CREATE DATABASE, CREATE TABLE, ALTER TABLE, DROP TABLE
- Daten erfassen: INSERT
- Daten ändern: UPDATE
- Daten löschen: DELETE
- Daten auswerten: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY
- Logik und Filter: AND, OR, NOT, IN, BETWEEN, LIKE, IS NULL
- Auswertung: COUNT, SUM, AVG, MIN, MAX, DISTINCT

## Externe Ergänzung

Wenn du zusätzliche Beispiele brauchst, kannst du SQL-Befehle auch in kompakter Form bei W3Schools nachschlagen:
https://www.w3schools.com/sql/

Wichtig: Dieses Stichwortverzeichnis bleibt deine primäre Quelle, weil es an eure Aufgabenkontexte, den 3NF-Fokus und den Bildungsplan angepasst ist.
