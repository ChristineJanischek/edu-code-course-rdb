# Prozess: Wiederholbare Implementierungsroutine fuer KI-Assistenten

Version: 1.0
Status: Aktiv
Gueltig ab: 01.07.2026

---

## Ziel

Eine wiederholbare, dokumentierte Routine bereitstellen, um den KI-Assistenten fuer neue Fachthemen auf Basis desselben Vorgehens zu erweitern.

---

## Eingaben

- Fachthema (z. B. relationale Datenbanken)
- Referenzquellen (intern und extern)
- Kompetenzraster
- Bewertungsrubriken
- Datenschutzvorgaben

---

## Standardschritte

1. Anforderungsstand in einem fachspezifischen Pflichtenheft dokumentieren.
2. Snapshot-Tag fuer den Ausgangszustand setzen.
3. Architekturinkrement in Route/Service/Repository/Model planen.
4. Frontend-MVC-Pendant fuer Nutzerinteraktion planen.
5. Hint-Policy definieren (keine Komplettloesung).
6. Wissens-Ingestion mit Quellenprovenienz implementieren.
7. Interaktionslogging und Audit-Trail aktivieren.
8. Lehrkraftfunktionen fuer Erstellung, Bewertung und Korrektur anbinden.
9. Sicherheits- und Doku-Gates ausfuehren.
10. Ergebnisse committen, pushen, im Marschplan fortschreiben.

---

## Artefakte je Durchlauf

- Fach-Pflichtenheft
- Marschplan fuer Fach-Inkrement
- API-Endpunkte + OpenAPI-Erweiterung
- Frontend-Controller/Model/View
- Logging-Schema fuer Interaktionen
- Changelog-Eintraege

---

## Definition of Done

- Assistent liefert didaktische Hinweise statt Loesungen.
- Quellen und Versionen sind nachvollziehbar.
- Lehrkraft- und Schuelerpfade sind getrennt.
- Pflicht-Gates laufen erfolgreich.
- Schritte sind so dokumentiert, dass sie fuer ein neues Thema wiederholbar sind.

---

## Reuse-Checkliste fuer neues Thema

- Fachliches Kompetenzmodell ersetzt
- Neue Quellen eingebunden
- Bewertungsrubriken angepasst
- Beispielaufgaben migriert
- Sicherheitsanalyse aktualisiert
- Pilot-Feedback eingeholt

---

## Changelog

- v1.0 (01.07.2026): Initiale wiederholbare Implementierungsroutine.
