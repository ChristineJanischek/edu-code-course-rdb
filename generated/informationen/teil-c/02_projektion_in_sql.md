# Informationsblatt Teil C: Projektion in SQL

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du wählst gezielt benötigte Spalten aus.
- Du unterscheidest Projektion von Selektion.
- Du nutzt DISTINCT bei Bedarf.

## Kernidee
Projektion bedeutet: Welche Spalten sollen im Ergebnis sichtbar sein?

## Beispiel
```sql
SELECT Name, Kategorie
FROM FOODTRUCK;
```

Nur die Spalten Name und Kategorie werden ausgegeben.

## Mit DISTINCT
```sql
SELECT DISTINCT Stadt
FROM ST```sql
SELECT DISTINCT Stadt
FROM STANDORT;
```Spalten, nicht Zeilen.
- SELECT * nur in der Analyse, nicht in der sauberen Lösung.
- DISTINCT nur verwenden, wenn fachlich nötig.

## Typische Fehler
- Projektion und Filter verwechseln.
- Zu viele Spalten auswählen.
- DISTINCT einsetzen, um Modellfehler zu kaschieren.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
