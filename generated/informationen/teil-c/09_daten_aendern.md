# Informationsblatt Teil C: Daten ändern

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du aktualisierst Daten gezielt mit UPDATE.
- Du setzt sichere WHERE-Bedingungen.
- Du vermeidest unbeabsichtigte Massenänderungen.

## Grundmuster
```sql
UPDATE FOODTRUCK
SET Rating = 4.8
WHERE TruckID = 101;
```

## Mehrere Felder
```sql
UPDATE FOODTRUCK
SET Kategorie = 'Fusion', Ra```sql
UPDATE FOODTRUCK
SET Kategorie = 'Fusion', Rating = 4.6
WHERE TruckID = 102;
```n.
- Vor UPDATE die Zielmenge mit SELECT prüfen.
- Schlüsselbasierte Bedingungen sind am sichersten.

## Typische Fehler
- Unscharfe Filterbedingungen.
- Datentypverletzungen.
- Geschäftslogik im Nachhinein „korrigieren“ statt vorher prüfen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
