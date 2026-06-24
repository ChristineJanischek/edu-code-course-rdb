# Übungen: SQL-Abfragen über mehrere Tabellen

> Hinweis: Zentraler Einstieg für Lernende ist [../README.md](../README.md).
> Diese Seite ist die Detailübersicht für Übungen.

## Übungsblätter

| Blatt | Kontext | Themen | Aufgaben | HTML |
|---|---|---|---|---|
| [UE01 FoodTruckNetz](./UE01_foodtrucknetz_sql_abfragen.html) | foodtrucknetzdb_2025 | JOIN, WHERE, OR, GROUP BY, HAVING, AVG, SUM, MONTH | 10 | ✔ |
| [UE02 Stadtfahrradverleih](./UE02_stadtfahrradverleih_sql_abfragen.html) | stadtfahrradverleihdb_2025 | JOIN (5 Tabellen), LEFT JOIN, IS NULL, HAVING, AVG, MAX, MIN | 10 | ✔ |

## So öffnest du ein Übungsblatt

1. Explorer öffnen (Symbol links oben in VS Code).
2. Datei `UE01_foodtrucknetz_sql_abfragen.html` suchen.
3. Rechtsklick → **„Open with Live Server"**.
4. Aufgabe lesen, Lösung in das Textfeld schreiben.
5. **„Musterlösung"** oder **„Erwartetes Ergebnis"** aufklappen, um deine Antwort zu vergleichen.

## Datenbanken einrichten (MySQL Workbench)

Für jedes Übungsblatt gibt es im Ordner `daten/` einen vollständi`daten/`Dump:

```bash
# 1. Struktur einlesen (aus generated/klassenarbeiten/)
mysql -u root -p < ../klassenarbeiten/foodtrucknetz_struktur_2025.sql

# 2. Erweiterte Übungsdaten einlesen
mysql -u root -p < daten/foodtrucknetz_uebung_daten.sql
```

```bash
mysql -u roo__`bash
mysql -u root -p < ../klassenarbeiten/stadtfahrradverleih_struktur_2025.sql
mysql -u root -p < daten/stadtfahrradverleih_uebung_daten.sql
`emenabdeckung

| Thema | UE01 | UE02 |
|---|---|---|
| WHERE +```bash
mysql -u root -p < ../klassenarbeiten/stadtfahrradverleih_struktur_2025.sql
mysql -u root -p < daten/stadtfahrradverleih_uebung_daten.sql
```|
| AVG + GROUP BY | A5, A10 | A7, A9 |
| HAVING | A4, A1``| A5, A6 |
| MAX / MIN | A9 | A10 |
| LEFT JOIN + IS NULL | — | A8 |
| ORDER BY | alle | alle |

## Lernziel

Nach Bearbeitung aller Aufgaben bist du in der Lage:
- mehrtabellige SELECT-Abfragen sicher aufzubauen
- WHERE, AND, OR korrekt zu kombinieren (mit Klammerung)
- Aggregatfunktionen COUNT, SUM, AVG, MAX, MIN anzuwenden
- Datumsfunktionen YEAR() und MONTH() für Zeitraumfilter einzusetzen
- GROUP BY und HAVING zu unterscheiden und richtig einzusetzen
- ORDER BY für Sortierung zu nutzen

## Verknüpfte Hilfsmittel

- [Stichwortverzeichnis Relationale Datenbanken](../informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html)
- [Informationsblatt: JOIN und mehrere Tabellen](../informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.md)
- [Informationsblatt: Gruppierung in SQL](../informationen/teil-c/06_gruppierung_in_sql.md)
- [Informationsblatt: Selektion in SQL](../informationen/teil-c/03_selektion_in_sql.md)
