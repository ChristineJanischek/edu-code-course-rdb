# Informationsblatt Teil C: Gruppierung in SQL

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du bildest Gruppen mit GROUP BY.
- Du wertest Gruppen mit Aggregatfunktionen aus.
- Du filterst Gruppen mit HAVING.

## Grundmuster
```sql
SELECT Stadt, COUNT(*) AS Einsaetze
FROM STANDORT s
JOIN EINSATZ e ON e.StandortID = s.StandortID
GROUP BY Stadt;
```

## HAVING statt WHERE
- WHERE filtert einzelne Zeilen vor der Gruppierung.
- HAVING filtert bereits gebildete Gruppen.

Beispiel:
```sql
SELECT Stadt, COUNT(*) AS Einsaetze
FROM STANDORT s
JOIN EINSATZ e ON e.StandortID = s.StandortID
GROUP ```sql
SELECT Stadt, COUNT(*) AS Einsaetze
FROM STANDORT s
JOIN EINSATZ e ON e.StandortID = s.StandortID
GROUP BY Stadt
HAVING COUNT(*) >= 5;
```icht.
- HAVING prüft Gruppenbedingungen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
