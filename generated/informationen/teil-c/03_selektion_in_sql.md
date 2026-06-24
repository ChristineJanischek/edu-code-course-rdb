# Informationsblatt Teil C: Selektion in SQL

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du filterst Datensätze mit WHERE korrekt.
- Du kombinierst Bedingungen mit AND, OR, NOT.
- Du nutzt Vergleichsoperatoren zielgerichtet.

## Kernidee
Selektion bedeutet: Welche Zeilen sollen im Ergebnis enthalten sein?

## Beispiele
```sql
SELECT Name, Kategorie
FROM FOODTRUCK
WHERE Kategorie = 'Vegan';
```

```sql
SELECT Name
FROM FOODTRUCK
WHERE Kategorie = 'Vegan' AN```sql
SELECT Name
FROM FOODTRUCK
WHERE Kategorie = 'Vegan' AND Rating >= 4.5;
```- LIKE
- IS NULL

## Merksätze
- WHERE filtert Zeilen vor Gruppierung.
- Klammern erhöhen Lesbarkeit und Sicherheit.
- Textwerte immer in Anführungszeichen.

## Typische Fehler
- AND/OR ohne Klammern falsch kombinieren.
- NULL mit = statt IS NULL prüfen.
- Tippfehler in Literalen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
