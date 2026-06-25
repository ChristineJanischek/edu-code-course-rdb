# KF-ROUTINE-013: Repo-weite OOP/MVC-Guardrails

## Metadata
- **ID:** KF-ROUTINE-013
- **Kategorie:** kurzfristig
- **Haeufigkeit:** bei jeder Codeaenderung in src/, services/, webapp/, scripts/
- **Zeitaufwand:** 10-20 Minuten
- **Verantwortlicher:** Autor der Aenderung
- **Abhaengigkeiten:** KF-ROUTINE-006, KF-ROUTINE-012, ARCHITEKTUR.md
- **Version:** 1.0
- **Letzte Aktualisierung:** 25.06.2026

## Ziel
OOP- und MVC-Prinzipien fuer das gesamte Repository verbindlich und wiederholbar sicherstellen.

## Vorbedingungen
- Geplante Aenderung ist klar abgegrenzt.
- Betroffene Schicht (Model, View, Controller/Route, Service, Repository) ist festgelegt.

## Schritte
1. Schichten-Schnitt bestimmen: Fachlogik nie in Bootstrap/Markup.
2. Python-API-Regel anwenden: `app.py` nur Einstiegspunkt, Business-Logik in `learning_api/`.
3. Webapp-Regel anwenden: `webapp/public/app.js` nur Bootstrap, Logik in `webapp/public/js/*.mjs`.
4. Frontend-MVC durchsetzen: Models in `webapp/public/js/models/`, Views in `webapp/public/js/views/`, Controller in `webapp/public/js/controllers/`.
5. Python-API-Schichten durchsetzen: Controller/Routes, Services und DB-nahe Logik in separaten Modulen halten.
6. Interaktive Doku-Seiten nach MVC/OOP aufteilen (Model/View/Controller).
7. Doppelte Logik in gemeinsame Module extrahieren.
8. Handbuch/Index bei neuen Mustern aktualisieren.
9. Pflichtchecks ausfuehren:
   - `bash scripts/validate-security.sh`
   - `bash scripts/validate-architecture.sh`
   - `bash scripts/validate-docs.sh`

## Erfolgskriterien
- Keine Business-Logik in Bootstrap-Dateien.
- Klare Trennung von Controller/Service/Repository in der Python-API.
- Interaktive Frontend-Logik in modularen Dateien, nicht inline.
- Alle Pflichtchecks gruen.

## Fehlerbehandlung
- Vermischte Schichten erkannt: Refactoring vor Merge.
- Wiederholte Regelverletzung: Guardrail-Skript erweitern.
- Gate fehlgeschlagen: Ursache beheben, dann erneuter Lauf.

## Ausgaben/Ergebnisse
- Nachvollziehbare, wartbare und testbare Struktur.
- Konsistente Architektur ueber alle Teilbereiche.

## Verknuepfungen
- [KF-ROUTINE-006-qualitaetsgate-pruefung.md](./KF-ROUTINE-006-qualitaetsgate-pruefung.md)
- [KF-ROUTINE-012-mvc-oo-businesslogik-trennung.md](./KF-ROUTINE-012-mvc-oo-businesslogik-trennung.md)
- [ARCHITEKTUR.md](../../ARCHITEKTUR.md)

## Changelog
- v1.0 (25.06.2026): Initiale Routine erstellt
