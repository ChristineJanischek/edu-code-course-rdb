# Informationsblatt Teil C: SQL-Abfragen über mehrere Tabellen

Zielgruppe: Sekundarstufe II (Abschlussjahr)  
Kontext Teil C: FoodTruckNetz (separat von Teil B)

## Lernziele
- Du verbindest Tabellen fachlich korrekt mit JOIN.
- Du liest Join-Bedingungen sicher aus dem Schema.
- Du vermeidest ungewollte kartesische Produkte.

## Kernidee
Daten liegen in normalisierten Tabellen verteilt. Für Auswertungen müssen Tabellen über Schlüssel verbunden werden.

## EERM-Übersicht für Teil C (PK/FK sichtbar)

Nutze diese Grafik während der Bearbeitung als Arbeitsgrundlage für JOIN-Ketten und Fremdschlüsselpfade:

![EERM Stadtfahrradverleih mit Attributen und PK/FK-Verbindungen](../../klassenarbeiten/stadtfahrradverleih_2025.png)

Arbeitsroutine mit der Grafik:
- Markiere zuerst Starttabelle und Zielattribute aus der Aufgabe.
- Verfolge danach den PK/FK-Pfad im EERM und notiere die Join-Reihenfolge.
- Formuliere erst dann `FROM` und `JOIN`, anschließend Filter, Gruppierung und Sortierung.

## Beispielkontext
- FOODTRUCK(TruckID, Name)
- STANDORT(StandortID, Stadt)
- EINSATZ(EinsatzID, TruckID, StandortID, Datum)

## Standardmuster
```sql
SELECT f.Name, s.Stadt, e.Datum
FROM EINSATZ e
JOIN FOODTRUCK f ON f.TruckID = e.TruckID
JOIN STANDORT s ON s.StandortID = e.StandortID;
```

## Merksätze
- JOIN immer über PK/FK-Beziehungen.
- Ohne ON-Bedingung droht Datenexplosion.
- Erst FROM/JOIN sauber, dann WHERE ergänzen.

## Typische Fehler
- Falsche Join-Spalten.
- Alias vergessen oder uneinheitlich.
- Filterbedingungen in ON und WHERE unklar mischen.

## Begriffshilfe
- [Stichwortverzeichnis Relationale Datenbanken](../begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
