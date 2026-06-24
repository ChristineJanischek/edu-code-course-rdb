# Informationsblatt Teil C: Redundanzen in Abfrageergebnissen

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du erkennst doppelte Ergebnisse in SQL-Abfragen.
- Du erklärst Ursachen (JOIN-Struktur, Projektion).
- Du reduzierst Duplikate fachgerecht.

## Warum entstehen Duplikate?
- m:n-Beziehungen liefern pro Kombination eine Zeile.
- Zu wenige Spalten in der Projektion lassen Unterschiede „unsichtbar“.
- Falsche Join-Bedingungen vervielfachen Daten.

## Beispiele
```sql
SELECT f.Name
FROM FOODTRUCK f
JOIN EINSATZ e ON e.TruckID = f.TruckID;
```
Ein Truck mit mehreren Einsätzen erscheint mehrfach.

Duplikatbereinigung:
```sql
SELECT DISTINCT f.Name
FROM FOODTRUCK f
JOIN EINSATZ e ON e.Tr```sql
SELECT DISTINCT f.Name
FROM FOODTRUCK f
JOIN EINSATZ e ON e.TruckID = f.TruckID;
```omatisch Fehler.
- DISTINCT ist ein Werkzeug, kein Ersatz für korrektes JOIN-Design.
- Erst Ursache verstehen, dann bereinigen.

## Typische Fehler
- DISTINCT pauschal überall einsetzen.
- Join-Logik nicht am Datenmodell prüfen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
