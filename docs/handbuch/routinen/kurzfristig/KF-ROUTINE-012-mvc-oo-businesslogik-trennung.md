# KF-ROUTINE-012: MVC- und OOP-Trennung fuer interaktive Oberflaechen

## Metadata
- **ID:** KF-ROUTINE-012
- **Kategorie:** kurzfristig
- **Haeufigkeit:** bei jeder UI-Interaktivitaet
- **Zeitaufwand:** 15-30 Minuten
- **Verantwortlicher:** Autor der Aenderung
- **Abhaengigkeiten:** ARCHITEKTUR.md, review-prozess.md
- **Version:** 1.0
- **Letzte Aktualisierung:** 25.06.2026

## Ziel
Business-Logik konsequent aus Markup und View-Code auslagern und interaktive Features nach MVC und OOP umsetzen.

## Vorbedingungen
- Zielseite und Interaktionsfall sind klar beschrieben.
- Bestehende Komponenten und Patterns wurden im Repo geprueft.

## Schritte
1. Domane und Use-Case schneiden: Datenlogik, Darstellungslogik und Steuerung trennen.
2. **Model** anlegen: reine Business-Logik ohne DOM-Zugriffe.
3. **View** anlegen: nur Rendering/DOM-Updates, keine Fachregeln.
4. **Controller** anlegen: Events entgegennehmen, Model aufrufen, View aktualisieren.
5. OOP anwenden: klare Klassenverantwortung, keine globalen mutable Zustaende.
6. Markup schlank halten: Seite bindet nur den Controller als Einstiegspunkt ein.
7. Redundanzpruefung: gemeinsame Logik in wiederverwendbare Module verschieben.
8. Handbuch und betroffene Routinen/Anleitungen aktualisieren.
9. Pflicht-Gates ausfuehren: Security, Architektur, Doku.

## Erfolgskriterien
- Kein Inline-Business-Code in HTML/Markdown.
- Model ist test- und wiederverwendbar.
- View ist austauschbar, Controller bleibt stabil.
- Pflicht-Gates sind erfolgreich.

## Fehlerbehandlung
- Vermischte Verantwortungen entdeckt: Klassen neu schneiden und Responsibilities verkleinern.
- Doppelte Logik gefunden: in gemeinsames Modul extrahieren.
- Gate fehlschlaegt: Ursache beheben, dann erneut validieren.

## Ausgaben/Ergebnisse
- Interaktive Funktion als MVC-Struktur mit klarer OOP-Kapselung.
- Nachvollziehbare Dokumentation im Handbuch.

## Verknuepfungen
- [ARCHITEKTUR.md](../../ARCHITEKTUR.md)
- [review-prozess.md](../../prozesse/review-prozess.md)

## Changelog
- v1.0 (25.06.2026): Initiale Routine erstellt
