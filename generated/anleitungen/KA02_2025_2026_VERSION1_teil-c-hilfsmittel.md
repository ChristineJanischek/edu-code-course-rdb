# Hilfsmittel Teil C: SQL-Abfragen über mehrere Tabellen

Diese Anleitung führt dich von der Aufgabenstellung über das Schema bis zur Abfrage. Der Fokus liegt auf der sauberen Join-Kette und auf den richtigen Filter- und Aggregationsschritten.

## Ausgehend von diesen Quellen arbeiten

- [Aufgaben VERSION1](../klassenarbeiten/KA02_2025_2026_VERSION1_aufg.md)
- [Lösung VERSION1](../klassenarbeiten/KA02_2025_2026_VERSION1_lsg.md)
- [Teil C: Abfragen über mehrere Tabellen](../informationen/teil-c/01_sql_abfragen_ueber_mehrere_tabellen.md)
- [Teil C: Selektion in SQL](../informationen/teil-c/03_selektion_in_sql.md)
- [Teil C: Gruppierung in SQL](../informationen/teil-c/06_gruppierung_in_sql.md)
- [Stichwortverzeichnis Relationale Datenbanken](../informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.md)
- [Stichwortverzeichnis (suchbare HTML-Ansicht)](../informationen/begrifflichkeiten/stichwortverzeichnis_relationale_datenbanken.html)

## 1. Zuerst das Schema lesen

Die technische Grundlage liegt getrennt in:

- [SQL-Struktur](../klassenarbeiten/stadtfahrradverleih_struktur_2025.sql)
- [SQL-Daten](../klassenarbeiten/stadtfahrradverleih_daten_2025.sql)
- [EERM-Referenzgrafik](../klassenarbeiten/stadtfahrradverleih_2025.png)

EERM direkt im Dokument (mit Attributen sowie PK/FK-Verbindungen):

![EERM Stadtfahrradverleih mit Attributen und PK/FK-Verbindungen](../klassenarbeiten/stadtfahrradverleih_2025.png)

Tipp für die Klassenarbeit: Du kannst die Join-Kette auch handschriftlich vorplanen, indem du die beteiligten Tabellen im EERM markierst und die PK/FK-Verbindungen als Pfad nachzeichnest.

Wichtige Tabellen und Rollen:

| Tabelle | Wozu sie dient | Wichtige Schlüsselspalten |
|---|---|---|
| kunden | Personen | kunde_id |
| stationen | Start- und Zielorte | station_id |
| fahrraeder | Fahrräder und Typen | fahrrad_id, station_id |
| ausleihen | Vorgänge | ausleihe_id, kunde_id, fahrrad_id, start_station_id, ziel_station_id |
| wartungen | Wartungshistorie | wartung_id, fahrrad_id |
| zahlungen | Zahlungsdaten | zahlung_id, ausleihe_id |

Wichtige Ergänzung aus dem Strukturdump:

- Der Zielkontext ist eine eigene 3NF-Datenbank mit dem Namen stadtfahrradverleihdb_2025.
- Start- und Zielstation sind zwei Rollen derselben Tabelle stationen, deshalb brauchst du zwei Aliase.
- Für Auswertungen zählen nur abgeschlossene Ausleihen.

## 2. Aufgabe 4.1 Schritt für Schritt

Ziel: Kundennamen, Fahrradnummer, Fahrradtyp, Start- und Zielstation sowie Zahlbetrag ausgeben.

Arbeitsreihenfolge:

1. Nimm ausleihen als Basistabelle.
2. Verbinde kunden über kunde_id.
3. Verbinde fahrraeder über fahrrad_id.
4. Verbinde stationen zweimal, einmal für start_station_id und einmal für ziel_station_id.
5. Verbinde zahlungen über ausleihe_id.
6. Filtere auf status = abgeschlossen.
7. Sortiere nach Kundennachname und startzeit.

Kontrollfrage:

- Wenn ein Ausgabefeld aus einer anderen Tabelle kommt, fehlt meist genau dieser Join.

## 3. Aufgabe 4.2 Schritt für Schritt

Ziel: je Person die Anzahl abgeschlossener Ausleihen, aber nur ab 2.

Arbeitsreihenfolge:

1. Starte wieder bei kunden und ausleihen.
2. Begrenze die Zeilen auf abgeschlossene Ausleihen.
3. Bilde die Gruppen pro Person.
4. Zähle die Ausleihen je Gruppe.
5. Filtere die Gruppen mit mindestens 2 über HAVING.

Merksatz:

- WHERE filtert Zeilen.
- HAVING filtert Gruppen.

## 4. Aufgabe 4.3 Schritt für Schritt

Ziel: pro Station den letzten Ausleihstart und die Anzahl unterschiedlicher Kundinnen und Kunden.

Arbeitsreihenfolge:

1. Verbinde stationen mit ausleihen über start_station_id.
2. Gib pro Station genau eine Ergebniszeile aus.
3. Ermittle den letzten Start mit MAX(startzeit).
4. Zähle unterschiedliche Personen mit COUNT(DISTINCT kunde_id).
5. Gruppiere nach station_id und stationsname.

Kontrollfrage:

- Wenn du mehr als eine Zeile pro Station erhältst, fehlt die Gruppierung oder sie ist zu grob.

## 5. Aufgabe 4.4 Schritt für Schritt

Ziel: Fahrräder ohne dokumentierte Wartung.

Arbeitsreihenfolge:

1. Nimm fahrraeder als Basistabelle.
2. Verbinde wartungen per LEFT JOIN über fahrrad_id.
3. Suche die Fahrräder, bei denen keine Wartung gefunden wurde.
4. Prüfe dafür das NULL-Feld aus der Wartungstabelle.

Merksatz:

- Ein LEFT JOIN behält die linke Tabelle vollständig und zeigt rechts NULL, wenn kein Treffer existiert.

## 6. Prüfstrategie vor dem Abgeben

- Stimmen alle Join-Spalten mit den Fremdschlüsseln aus dem Strukturdump überein?
- Ist die Rolle der stationen-Tabelle zweimal sauber getrennt?
- Ist der Statusfilter nur bei abgeschlossenen Ausleihen gesetzt?
- Werden Gruppen erst nach dem GROUP BY mit HAVING geprüft?
- Ist die Abfrage ohne unnötige Wiederholungen gebaut?
