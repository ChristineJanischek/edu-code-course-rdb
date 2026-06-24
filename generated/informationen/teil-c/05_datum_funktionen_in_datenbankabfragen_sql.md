# Informationsblatt Teil C: Datum-Funktionen in Datenbankabfragen (SQL)

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz

## Lernziele
- Du filterst und berechnest Daten mit Datumsfunktionen.
- Du nutzt aktuelle Zeitbezüge sicher.
- Du formulierst Zeiträume korrekt.

## Häufige Funktionen in MySQL
- CURDATE()
- NOW()
- YEAR()
- MONTH()
- DATEDIFF()
- DATE_ADD()

## Beispiele
```sql
SELECT *
FROM EINSATZ
WHERE Datum >= CURDATE();
```

```sql
SELECT EinsatzID, DATEDIFF(CURDATE(), ```sql
SELECT EinsatzID, DATEDIFF(CURDATE(), Datum) AS TageSeitEinsatz
FROM EINSATZ;
```klären, dann codieren.
- Bei Zeiträumen Grenzen eindeutig setzen.
- Datum und Zeit nicht unbewusst mischen.

## Typische Fehler
- Falscher Datentyp (TEXT statt DATE/DATETIME).
- Unscharfe Zeiträume („ab heute“) ohne genaue Bedingung.
- Jahres-/Monatsfilter ohne Indexbewusstsein bei großen Datenmengen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
